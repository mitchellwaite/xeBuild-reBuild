"""fl10m.py: without findField, sec's comma has to be inlined before its nul (gimple_expand_calls_inline walks a BB backwards, so the later call gets the lower numbers; a helper's nested call is only reached later).
A small helper round a NUL search, at subsets of its uses, in place of findField."""
import itertools, sys
import fllib as L, fl10lib as F, fl10h as H

B = H.state('ff')
DEF = "static int fieldLen(unsigned char *p, int rem)\n{\n\treturn memFindChar(p, 0, rem);\n}\n\n"
A0 = B.index("uint32_t parseIni(char *path)")
A0 = B.rindex("/* read the file list ini:", 0, A0)

# section boundaries
SECS = {'ver': "/* [version] */", 'bl': "/* [<console>bl<blSuffix>]", 'raw': "/* [rawpatch]: name,offset */", 'flash': "/* [flashfs]: name[,crc]", 'sec': "/* [security]: name[,crc] */", 'end': "/* offset of the value after"}
ORDER = ['ver', 'bl', 'raw', 'flash', 'sec', 'end']


def pieces(s):
    pos = [s.index(SECS[k]) for k in ORDER]
    r = {'pre': s[:pos[0]]}
    for i, k in enumerate(ORDER[:-1]):
        r[k] = s[pos[i]:pos[i + 1]]
    r['post'] = s[pos[-1]:]
    return r


NUL = "nul = memFindChar(p, 0, size - pos);"
NULH = "nul = fieldLen(p, size - pos);"
CRC = "n = memFindChar(&buf[pos], 0, size - pos);"
CRCH = "n = fieldLen(&buf[pos], size - pos);"


def mk(heads, crcs, name=DEF):
    p = pieces(B)
    for k in ('bl', 'raw', 'flash', 'sec'):
        if k in heads:
            p[k] = p[k].replace(NUL, NULH)
        if k in crcs:
            p[k] = p[k].replace(CRC, CRCH)
    s = p['pre'] + ''.join(p[k] for k in ORDER[:-1]) + p['post']
    return L.sub(s, "/* read the file list ini:", name + "/* read the file list ini:")


V = {}
KS = ['bl', 'raw', 'flash', 'sec']
subs = [c for r in range(0, 5) for c in itertools.combinations(KS, r)]
for h in subs:
    for c in subs:
        if h or c:
            V['h=%s c=%s' % ('+'.join(h), '+'.join(c))] = mk(h, c)

if __name__ == '__main__':
    print(len(V))
    F.run(V, 'm', show=15)
