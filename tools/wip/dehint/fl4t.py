"""fl4t.py: findKey forms with the key tests in or out: test-first loops (remap order, as setupFiles), a helper for the match at i, a helper for the value."""
import itertools
import fllib as L, fl4lib as F, fl4final as Z

S = Z.build()
FOR = '\tfor (i = 0; i < xb.iniSize - len; i++) {\n\t\tif (key[0] == buf[i]) {\n\t\t\tp = &buf[i];\n'
K1 = "\t\t\t\t/* defensive, and dead (key was read above): VRP removes it, and\n\t\t\t\t   until then it sets findKey's SSA numbers in the getters */\n\t\t\t\tif (key == NULL)\n\t\t\t\t\treturn -1;\n"
K2 = "\t/* defensive and dead, as in findKey: sets the order of this function's\n\t   buf[i]/key[0] compare */\n\tif (key == NULL)\n\t\treturn NULL;\n"
assert FOR in S and K1 in S and K2 in S
TAIL = '''			if (j == len) {
				unsigned char *q = &buf[i + len];

				if (*q != 0)
					return i + len;
			}
'''
LOOPS = {
    'for': FOR,
    'brk': '\tfor (i = 0; ; i++) {\n\t\tif (i >= xb.iniSize - len)\n\t\t\tbreak;\n\t\tif (key[0] == buf[i]) {\n\t\t\tp = &buf[i];\n',
    'ret': '\tfor (i = 0; ; i++) {\n\t\tif (i >= xb.iniSize - len)\n\t\t\treturn -1;\n\t\tif (key[0] == buf[i]) {\n\t\t\tp = &buf[i];\n',
}
V = {}
for lp, kf, ku in itertools.product(LOOPS, (0, 1), (0, 1)):
    s = S
    if not kf:
        s = L.sub(s, K1, '')
    if not ku:
        s = L.sub(s, K2, '')
    s = L.sub(s, FOR, LOOPS[lp])
    V['%s kf=%d ku=%d' % (lp, kf, ku)] = s
    if not kf:
        s2 = L.sub(s, '\t\t\t\tunsigned char *q = &buf[i + len];\n\n\t\t\t\tif (*q != 0)\n\t\t\t\t\treturn i + len;\n', '\t\t\t\tif (buf[i + len] != 0)\n\t\t\t\t\treturn i + len;\n')
        V['%s kf=0 ku=%d noq' % (lp, ku)] = s2
    # the getters through one helper for the common head
HEAD = '\tif (xb.iniSize == 0)\n\t\treturn %s;\n\toff = FIND;\n\tif (off == -1)\n\t\treturn %s;\n'
F.run(V, 't', show=24)
