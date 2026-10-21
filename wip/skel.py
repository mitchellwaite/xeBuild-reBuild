"""skel.py fn [gcc flags]: diff the original's and a draft's sequence of calls,
string literals (by content) and jumps for one function; ignores registers, so it
shows block order and duplication.  SRC= the draft (default
wip/app/filelist_ini.c), OBJ= its object (default app/filelist_ini)."""
import difflib, os, re, subprocess, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fn = sys.argv[1]
flags = sys.argv[2:] or ['-O3']
src = os.environ.get('SRC', os.path.join(R, 'wip', 'app', 'filelist_ini.c'))
obj = os.environ.get('OBJ', 'app/filelist_ini')


def strings(lines, labre):
    out, cur, acc = {}, [], ''
    for l in lines:
        m = re.match(labre, l)
        if m:
            if not acc:
                cur.append(m.group(1))
            continue
        m = re.match(r'\s*\.(string|ascii)\s+"(.*)"', l)
        if not (m and cur):
            cur, acc = [], ''
            continue
        acc += m.group(2).encode().decode('unicode_escape')
        if m.group(1) == 'string' or acc.endswith(chr(0)):
            v = acc.rstrip(chr(0))
            for c in cur:
                # shortcut: filelist_ini's .data (file names) ends below 0x44f000; per object
                if not (c.startswith('L_') and int(c[2:], 16) < 0x44f000):
                    out[c] = v[:40]
            cur, acc = [], ''
    return out


def toks(body, strs):
    out = []
    for l in body:
        l = l.split('#')[0].strip()
        m = re.match(r'call\s+(\S+)', l)
        if m:
            out.append('call ' + m.group(1).lower())
            continue
        for s in re.findall(r'(?:OFFSET\s+(?:FLAT:)?)?(\bL_[0-9a-f]+|\bLC\d+)', l):
            if s in strs:
                out.append('str "%s"' % strs[s])
        if re.match(r'(j\w+|cmov\w+)\s', l):
            out.append(l.split()[0])
        if l.startswith('ret'):
            out.append('ret')
    return out


s = open(os.path.join(R, 'src', obj + '.s')).read().split('\n')
ostr = strings(s, r'^(L_[0-9a-f]+|_\w+):')
a = s.index('_%s:' % fn)
b = next(i for i in range(a + 1, len(s)) if re.match(r'^(_\w+:|#@C)', s[i]))
orig = toks(s[a + 1:b], ostr)
BIN = os.path.join(R, 'tools', 'toolchain-4745', 'mingw32', 'bin')
env = dict(os.environ, PATH=BIN + os.pathsep + os.environ['PATH'])
g = subprocess.run([os.path.join(BIN, 'gcc.exe'), '-S', '-masm=intel', '-fno-asynchronous-unwind-tables',
                    '-I', os.path.dirname(src)] + flags + [src, '-o', '-'],
                   capture_output=True, text=True, env=env).stdout.split('\n')
mstr = strings(g, r'^(LC\d+):')
a = g.index('_%s:' % fn)
b = next(i for i in range(a + 1, len(g)) if re.match(r'\s*\.(def|globl|ident)\b', g[i]))
mine = toks(g[a + 1:b], mstr)
# jcc spellings
cc = {'jnb': 'jae', 'jnbe': 'ja', 'jnae': 'jb', 'jna': 'jbe', 'jz': 'je', 'jnz': 'jne'}
mine = [cc.get(t, t) for t in mine]
orig = [cc.get(t, t) for t in orig]
d = list(difflib.unified_diff(orig, mine, 'original', 'mine', lineterm='', n=int(os.environ.get('CTX', 3))))
print('\n'.join(d) if d else 'SKELETON MATCH')
sm = difflib.SequenceMatcher(None, orig, mine, autojunk=False)
print('# %d/%d tokens equal' % (sum(x.size for x in sm.get_matching_blocks()), len(orig)), file=sys.stderr)
