"""fl4v.py: with `buf[i] == key[0]`: findKey's last test out or spelled otherwise, tail and loop forms."""
import itertools
import fllib as L, fl4lib as F, fl4final as Z

S = Z.build()
K1 = "\t\t\t\t/* defensive, and dead (key was read above): VRP removes it, and\n\t\t\t\t   until then it sets findKey's SSA numbers in the getters */\n\t\t\t\tif (key == NULL)\n\t\t\t\t\treturn -1;\n"
Q = '\t\t\t\tunsigned char *q = &buf[i + len];\n\n'
Q2 = '\t\t\t\tif (*q != 0)\n\t\t\t\t\treturn i + len;\n'
assert K1 in S
TAILS = {
    'none': Q + Q2,
    'noq': '\t\t\t\tif (buf[i + len] != 0)\n\t\t\t\t\treturn i + len;\n',
    'val': '\t\t\t\tunsigned char c = buf[i + len];\n\n\t\t\t\tif (c != 0)\n\t\t\t\t\treturn i + len;\n',
    'cont': '\t\t\t\tif (buf[i + len] == 0)\n\t\t\t\t\tcontinue;\n\t\t\t\treturn i + len;\n',
    'qcont': Q + '\t\t\t\tif (*q == 0)\n\t\t\t\t\tcontinue;\n\t\t\t\treturn i + len;\n',
    'off': '\t\t\t\tint off = i + len;\n\n\t\t\t\tif (buf[off] != 0)\n\t\t\t\t\treturn off;\n',
    'qoff': Q + '\t\t\t\tif (*q != 0)\n\t\t\t\t\treturn q - buf;\n',
}
for c in ['buf == NULL', 'xb.iniBuf == NULL', 'len < 0', 'i < 0', 'xb.iniSize == 0', 'buf != xb.iniBuf']:
    TAILS['t:' + c] = Q + '\t\t\t\tif (%s)\n\t\t\t\t\treturn -1;\n' % c + Q2
OLD = Q + K1 + Q2
assert OLD in S
FOR = '\tfor (i = 0; i < xb.iniSize - len; i++) {\n\t\tif (buf[i] == key[0]) {\n'
LOOPS = {'for': FOR, 'brk': '\tfor (i = 0; ; i++) {\n\t\tif (i >= xb.iniSize - len)\n\t\t\tbreak;\n\t\tif (buf[i] == key[0]) {\n'}
V = {}
for t, l in itertools.product(TAILS, LOOPS):
    s = L.sub(S, OLD, TAILS[t])
    s = L.sub(s, FOR, LOOPS[l])
    V['%s %s' % (t, l)] = s
F.run(V, 'v', show=16)
