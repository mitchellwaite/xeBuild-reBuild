"""fl3final.py: writes attempt 3's draft and verifies it whole-object and per section.
build() = src plus the getters' edits (fl3g.py and friends start from this); final() adds parseIni's.
Add accepted edits here, not to the draft."""
import os, re, subprocess
import fllib as L

UNR = '''				unsigned char *q = &buf[i + len];

				if (q == 0)
					__builtin_unreachable();
				if (*q != 0)
					return i + len;
'''
GOOD = '''				unsigned char *q = &buf[i + len];

				/* defensive, and dead (key was read above): VRP removes it, and
				   until then it sets findKey's SSA numbers in the getters */
				if (key == NULL)
					return -1;
				if (*q != 0)
					return i + len;
'''
COMMENT_OLD = '''/* getters' own helper (not memFindStr).  The ebx pins fix RA ties; findKey's
   has an output (kept by the unreachable) so it is no sched2 barrier */
'''
COMMENT_NEW = '''/* getters' own helper (not memFindStr) */
'''
PIN = '\t__asm__("" :: "b"(val));\n'
U_OLD = '''char *iniU32Invalid(const char *key)
{
	int off;
	char *val;
	if (xb.iniSize == 0)
		return NULL;
	off = FIND;
	if (off == -1)
		return NULL;
'''
U_NEW = U_OLD + '''	/* defensive and dead, as in findKey: sets the order of this function's
	   buf[i]/key[0] compare */
	if (key == NULL)
		return NULL;
'''
EDITS = [(UNR, GOOD), (COMMENT_OLD, COMMENT_NEW), (PIN, ''), (U_OLD, U_NEW)]

# parseIni: smaller arms, natural spellings where they behave the same.
# In source order: comma i nul off3 off4 len x; (cond or None, stores)
TESTS = [('nbl != 6 && nbl != 9', ['xb.nFiles = 0']), ('i < 0', ['xb.nRawPatches = 0']), ('nul < -1', ['*buf = 0']), ('off < -1', ['buf[size] = 0', '*buf = 0']),
         ('off < -1', ['*buf = 0']), ('len < 0', ['*buf = 0']), ('off < 0', ['*buf = 0', 'buf[1] = 0'])]
OLD_C = re.compile(r'\t\t/\* this and the other `< -1` tests are dead.*?\*/\n', re.S)
NEW_C = '''\t\t/* this and the other can't-happen tests below are dead, and they steer gcc:
\t\t   the SSA names they free, so their stores count too, decide what dom2, dom3
\t\t   and vrp2 number next, which sets the comma/nul compares, the rawpatch lea
\t\t   and the copy order on flashfs's threaded path (notes/filelist_ini.md) */
'''


def build():
    s = L.base()
    for o, n in EDITS:
        s = L.sub(s, o, n)
    return s


def final():
    s = build()
    s, c = OLD_C.subn(NEW_C, s)
    assert c == 1
    rx = re.compile(r'([ \t]*)if \(\w+ < -1\) \{\n(?:[ \t]*buf\[\d\] = 1;\n)+[ \t]*\}\n')
    ms = list(rx.finditer(s))
    assert len(ms) == len(TESTS), len(ms)
    out, last = [], 0
    for m, (cond, k) in zip(ms, TESTS):
        out.append(s[last:m.start()])
        ind = m.group(1)
        if cond:
            out.append('%sif (%s) {\n%s%s}\n' % (ind, cond, ''.join('%s\t%s;\n' % (ind, a) for a in k), ind))
        last = m.end()
    out.append(s[last:])
    return ''.join(out)


if __name__ == '__main__':
    s = final()
    open(L.DRAFT, 'w', newline='\n').write(s)
    o = L.compile(s, ['-O3'], 'final')
    print('whole object identical:', L.same(o))
    a, b = L.sections(L.REF), L.sections(o)
    for k in sorted(set(a) | set(b)):
        print(' ', k, len(a.get(k, b'')), 'same' if a.get(k) == b.get(k) else 'DIFF')
    print('asm:', s.count('__asm__'), 'unreachable:', s.count('__builtin_unreachable'), 'tests < -1:', len(re.findall(r'< -1\)', s)))
    p = subprocess.run([L.GCC, '-c', '-O3', '-Wall', '-Wextra', '-I' + os.path.join(L.R, 'src'), '-x', 'c', L.DRAFT, '-o', os.path.join(L.OUT, 'w.o')],
                       stderr=subprocess.PIPE, cwd=L.OUT)
    print('\n'.join(l for l in p.stderr.decode(errors='replace').splitlines() if 'uninit' in l))
