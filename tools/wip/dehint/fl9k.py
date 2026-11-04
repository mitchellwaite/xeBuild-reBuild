"""fl9k.py: at the draft's shape, can the numbering helpers go too?  Axes: ff (findField or inline), pre, loop (setupFiles' form or inline in parseIni), which of bl's three
&xb.files[..].name uses are unsigned (chains: c copy, e err, l log), pv=v and unsigned chains in other sections' indexes."""
import itertools, os, sys
os.environ.setdefault('FLA', 'a9')
import fllib as L, fl6lib as F, fl8lib as G, fl9f, fl9i

T = 'T1,T2,T3'
S = F.drop(F.S0, T.split(','))
LOOPHEAD = "\tfor (i = 0; ; i++) {\n\t\tif (i >= xb.nFiles)\n\t\t\tbreak;\n"


def looponly(s):
    return L.sub(s, LOOPHEAD, "\tfor (i = 0; i < xb.nFiles; i++) {\n")


def inlineSetup(s):
    a = s.index('/* the files this build type uses.')
    b = s.find("/* an entry's name,crc separators.")
    if b < 0:
        b = s.index(F.HEAD)
    body = s[a:b]
    s = s[:a] + s[b:]
    i = body.index('\tfor (i = 0; ; i++) {')
    j = body.rindex('}\n\n}') if '}\n\n}' in body else body.rindex('\n}')
    loop = body[i:j + 1]
    s = L.sub(s, "\tsetupFiles();\n", loop + "\n")
    s = L.sub(s, "\tchar label[50];\n", "\tstruct fileent *e;\n\tchar label[50];\n")
    return s


CH = {'c': 1, 'e': 8, 'l': 64}
OPT = {
    'ff': {'y': lambda s: s, 'n': F.ffinline},
    'pre': {'y': lambda s: s, 'n': F.prein},
    'lp': {'first': lambda s: s, 'for': looponly, 'in': inlineSetup},
    'pv': {'': lambda s: s, 'v': fl9f.pv('v')},
}
chains = ['', 'c', 'e', 'l', 'ce', 'cl', 'el', 'cel']

if __name__ == '__main__':
    V = {}
    for ff, pre, lp, pv, ch in itertools.product(OPT['ff'], OPT['pre'], OPT['lp'], OPT['pv'], chains):
        s = S
        s = OPT['ff'][ff](s)
        s = OPT['pre'][pre](s)
        s = OPT['lp'][lp](s)
        s = OPT['pv'][pv](s)
        s = fl9i.ui(sum(CH[c] for c in ch))(s)
        V['ff=%s,pre=%s,lp=%s,pv=%s,ch=%s' % (ff, pre, lp, pv, ch)] = s
    print(len(V))
    rs = G.run(V, 'k', 40)
