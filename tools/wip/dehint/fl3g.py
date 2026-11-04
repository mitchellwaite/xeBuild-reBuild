"""fl3g.py: parseIni's dead tests as natural checks.  gen(state) builds source from the findKey-fixed base;
state = {site: (cond, arm)}; a site left out has no test; arm is int k (k stores to buf) or statements.
Sites as in src's tests, in order: comma i nul off3 off4 len x, plus off5 (too-long name's error arm)
and any EXTRA site added with mark().  Tie vector: flx7's t1 t2 t3, reimplemented (flx7 imports stale code).
main: one-site substitutions from the matching state."""
import itertools, re, sys
import fllib as L, fl3final as F

L.FLAGS[:] = ['-O3']
S0 = F.build()
RX = re.compile(r'(?:[ \t]*/\* this and the other `< -1` tests.*?\*/\n)?([ \t]*)if \((\w+) < -1\) \{\n((?:[ \t]*buf\[\d\] = 1;\n)+)[ \t]*\}\n', re.S)
SITES = ['comma', 'i', 'nul', 'off3', 'off4', 'len', 'x']
ms = list(RX.finditer(S0))
assert len(ms) == 7, len(ms)
parts, last = [], 0
INDENT = {}
for name, m in zip(SITES, ms):
    parts.append(S0[last:m.start()])
    parts.append('@@%s@@' % name)
    INDENT[name] = m.group(1)
    last = m.end()
parts.append(S0[ms[-1].end():])
MARKED = ''.join(parts)
CUR = {n: ('%s < -1' % m.group(2), m.group(3).count('buf[')) for n, m in zip(SITES, ms)}


def mark(name, before, ind, nth=0):
    """adds site `name` just before the nth occurrence of text `before`"""
    global MARKED
    k = -1
    for _ in range(nth + 1):
        k = MARKED.index(before, k + 1)
    MARKED = MARKED[:k] + '@@%s@@' % name + MARKED[k:]
    SITES.append(name)
    INDENT[name] = ind


mark('off5', '\t\t\t\t\t\treturn 0;\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t\tpos = pos + len + 1;', '\t\t\t\t\t\t')

T1 = ('cmp    edx,ebx', 'mov    DWORD PTR [esp+0x34],0x1', 'jle')
T2 = 'lea    ebp,[ebx+ebp*1+0x1]'
T3 = ('mov    ebx,0xffffffff', 'xor    edi,edi')


def vec(o):
    d = L.dis(o)['_parseIni']
    t1 = any(d[i] == T1[0] and d[i + 1] == T1[1] and d[i + 2].startswith(T1[2]) for i in range(len(d) - 2))
    t2 = T2 in d
    t3 = any(d[i] == T3[0] and d[i + 1] == T3[1] for i in range(len(d) - 1))
    return ('1' if t1 else '-') + ('2' if t2 else '-') + ('3' if t3 else '-')


def arm_text(arm, ind):
    if isinstance(arm, int):
        return ''.join('%s\tbuf[%d] = 1;\n' % (ind, j) for j in range(arm))
    return ''.join('%s\t%s;\n' % (ind, a.strip()) for a in arm.split(';') if a.strip())


def test(name, cond, arm):
    ind = INDENT[name]
    return '%sif (%s) {\n%s%s}\n' % (ind, cond, arm_text(arm, ind), ind)


def gen(state):
    s = MARKED
    for n in SITES:
        t = state.get(n)
        s = s.replace('@@%s@@' % n, test(n, *t) if t else '')
    return s


def st(label):
    """'len=3,off3=5' -> state with each site's old `< -1` test, k stores."""
    r = {}
    for kv in label.split(','):
        n, k = kv.split('=')
        v = {'comma': 'comma', 'i': 'i', 'nul': 'nul', 'len': 'len'}.get(n, 'off')
        r[n] = ('%s < -1' % v, int(k))
    return r


if __name__ == '__main__':
    for lab in ['comma=3,i=1,len=1,nul=1,off3=2,off4=2,x=4', 'comma=1,i=1,len=1,nul=1,off3=2,off4=1,x=2', 'len=3,off3=5,off4=1,off5=4']:
        o = L.compile(gen(st(lab)), None, 'g0')
        sc = L.score(o)
        print(lab, sc[0], sc[2], vec(o))
