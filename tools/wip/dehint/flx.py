"""flx.py: attempt 2's edits on the current src/filelist_ini.c (no flags: plain -O3).

gen(dead=(names to remove), flen='asm'|'nest'|'plain', edits=[names in EDITS]) -> whole source.
Dead tests: comma i nul off3 off4 off5 t len.
"""
import itertools, re, sys
import fllib as L

L.FLAGS[:] = ['-O3']

COMMA_C = re.compile(r'\t\t/\* this and the other `< -1` stores.*?\*/\n\t\tif \(comma < -1\) \{\n\t\t\tbuf\[0\] = 1;\n\t\t\tbuf\[1\] = 1;\n\t\t\}\n', re.S)
T_C = re.compile(r'\t\t\t\t/\* dead only from the strlen.*?\t\t\t\t\{\n\t\t\t\t\tchar t_\[4\];.*?\t\t\t\t\}\n', re.S)
DEADS = {
 'i': ('\tif (i < -1)\n\t\tbuf[0] = 1;\n', ''),
 'nul': ('\t\t\tif (nul < -1)\n\t\t\t\tbuf[0] = 1;\n', ''),
 'off3': ('\t\t\tif (off < -1)\n\t\t\t\tbuf[0] = 1;\n\t\t\tif (len > 21) {', '\t\t\tif (len > 21) {'),
 'off4': ('\t\t\t\tif (off < -1)\n\t\t\t\t\tbuf[0] = 1;\n\t\t\t\t/* dead only', '\t\t\t\t/* dead only'),
 'len': ('\t\t\t\tif (len < -1)\n\t\t\t\t\tbuf[0] = 1;\n', ''),
 'off5': ('\t\t\t\t\tif (off < -1)\n\t\t\t\t\t\tbuf[0] = 1;\n', ''),
}
ALLDEAD = ['comma', 'i', 'nul', 'off3', 'off4', 'off5', 't', 'len']
FLEN_C = re.compile(r'\t\t\t/\* the original checks the path length.*?return 0;\n\t\t\t\}\n', re.S)
PATHERR = '''log_printf(0, "\\n******* ERROR: file in [flashfs] has greater than %d chars in it's path!\\n", 1023);
				free(buf);
				return 0;
'''


def rmdead(s, names):
    names = list(names)
    # order matters: off4 before t (its text ends in the t comment)
    for n in ['off3', 'off4', 'off5', 'i', 'nul', 'len']:
        if n in names:
            s = L.sub(s, *DEADS[n])
    if 't' in names:
        s, c = T_C.subn('', s)
        assert c == 1
    if 'comma' in names:
        s, c = COMMA_C.subn('', s)
        assert c == 1
    return s


def flen(s, how):
    m = FLEN_C.search(s)
    assert m
    if how == 'asm':
        return s
    if how == 'plain':
        return s[:m.start()] + '\t\t\tif (len > 1023) {\n\t\t\t\t' + PATHERR + '\t\t\t}\n' + s[m.end():]
    s = s[:m.start()] + '\t\t\tif (len <= 1023) {\n' + s[m.end():]
    k = s.index("\t\t\tlog_printf(1, \"found (%d) '%s' crc: 0x%08x\\n\", ++xb.nFirmware")
    k2 = s.index('\t\t\tif (pos >= size)\n', k)
    return s[:k2] + '\t\t\t} else {\n\t\t\t\t' + PATHERR + '\t\t\t}\n' + s[k2:]


def gen(dead=(), fl='asm', edits=(), src=None):
    s = src if src is not None else L.base()
    s = rmdead(s, dead)
    s = flen(s, fl)
    for e in edits:
        for o, w in (EDITS[e] if isinstance(e, str) else e):
            if s.count(o) < 1:
                raise ValueError('%s: %r' % (e, o[:60]))
            s = s.replace(o, w, 1)
    return s


EDITS = {}


def write(rs, name):
    with open(L.BD + '/' + name, 'w', newline='\n') as f:
        for n, (sc, st, fd, sd) in rs:
            f.write('%s %s %s %s\n' % (sc, n, fd, sd))


if __name__ == '__main__':
    fls = sys.argv[1].split(',') if len(sys.argv) > 1 else ['asm', 'nest', 'plain']
    V = {}
    for fl in fls:
        for r in range(len(ALLDEAD) + 1):
            for rm in itertools.combinations(ALLDEAD, r):
                V[fl + '__' + '+'.join(rm)] = gen(rm, fl)
    print(len(V))
    rs = L.sweep(V, prefix='x', show=25)
    write(rs, 'x_sub_%s.txt' % '_'.join(fls))
    # MATCHes
    for n, r in rs:
        if r[0] == 0:
            print('MATCH', n)
