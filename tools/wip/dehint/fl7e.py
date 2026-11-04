"""fl7e.py: what sets findKey's frequencies is P(head) (28% as ==), P(match) (28%) and the exit share (4.5%).  In findKey's own estimate, with the inner loop 10000:
header = 3214, entry = (latch) * exit + tail * exit, tail = 252 at P(match) 28%.  Target band: entry 114 tail 252 (3 exits).  Lowering the entry needs P(head) about 40%.
Head and match tests that have no opcode prediction at estimate time, in combination.  python fl7e.py [label]: sweep or diff."""
import itertools, sys
import fl7lib as K

HF = {
    'eq': ('', '', 'buf[i] == key[0]'),
    'sub': ('', '', 'buf[i] - key[0] == 0'),
    'xor': ('', '', '!(buf[i] ^ key[0])'),
    'flag': ('\tint first;\n', '\t\tfirst = 0;\n\t\tif (buf[i] == key[0])\n\t\t\tfirst = 1;\n', 'first'),
    'flag2': ('\tint first;\n', '\t\tif (buf[i] == key[0])\n\t\t\tfirst = 1;\n\t\telse\n\t\t\tfirst = 0;\n', 'first'),
    'help': ('', '', 'sameChar(buf[i], key[0])'),
    'helpp': ('', '', 'startsAt(&buf[i], key)'),
}
PRE = {
    'help': "static int sameChar(unsigned char a, char b)\n{\n\tif (a == b)\n\t\treturn 1;\n\treturn 0;\n}\n\n",
    'helpp': "static int startsAt(unsigned char *p, const char *key)\n{\n\tif (*p == key[0])\n\t\treturn 1;\n\treturn 0;\n}\n\n",
}
SCAN = "\t\t\tp = &buf[i];\n\t\t\tfor (j = 0; j < len; j++)\n\t\t\t\tif (p[j] != key[j])\n\t\t\t\t\tj = len + 1;\n"
MATCHAT = "static int matchAt(unsigned char *p, const char *key, int len)\n{\n\tint j;\n\n\tfor (j = 0; j < len; j++)\n\t\tif (p[j] != key[j])\n\t\t\tj = len + 1;\n\tif (j == len)\n\t\treturn 1;\n\treturn 0;\n}\n\n"
MF = {
    'eq': (SCAN, 'j == len', ''),
    'sub': (SCAN, 'len - j == 0', ''),
    'xor': (SCAN, '!(j ^ len)', ''),
    'flag': (SCAN + "\t\t\tok = 0;\n\t\t\tif (j == len)\n\t\t\t\tok = 1;\n", 'ok', ''),
    'hm': ('', 'matchAt(&buf[i], key, len)', MATCHAT),
}
TL = {
    'q': "\t\t\t\tunsigned char *q = &buf[i + len];\n\n\t\t\t\tif (*q != 0)\n\t\t\t\t\treturn i + len;\n",
    'c': "\t\t\t\tif (buf[i + len] == 0)\n\t\t\t\t\tcontinue;\n\t\t\t\treturn i + len;\n",
    'sub': "\t\t\t\tif (buf[i + len] > 0)\n\t\t\t\t\treturn i + len;\n",
}
V = {}
for (hk, (hd, hp, hc)), (mk, (mb, mc, mp)), (tk, t) in itertools.product(HF.items(), MF.items(), TL.items()):
    decl = hd + ('\tint ok;\n' if mk == 'flag' else '')
    body = ("/* getters' own helper (not memFindStr) */\n" + PRE.get(hk, '') + mp + "static int findKey(unsigned char *buf, const char *key)\n{\n\tint i, j, len;\n\tunsigned char *p;\n" + decl +
            "\tlen = strlen(key);\n\tfor (i = 0; i < xb.iniSize - len; i++) {\n" + hp + "\t\tif (" + hc + ") {\n" + mb + "\t\t\tif (" + mc + ") {\n" + t + "\t\t\t}\n\t\t}\n\t}\n\treturn -1;\n}\n")
    V['%s,%s,%s' % (hk, mk, tk)] = K.fk(body)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        K.diff(V[sys.argv[1]])
    else:
        print(len(V))
        K.run(V, 'e', 24)
