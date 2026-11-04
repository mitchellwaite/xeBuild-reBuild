"""fl7b.py: the outer loop's test as a comparison with 0.  tree_predict_by_opcode gives `x > 0` PRED_TREE_OPCODE_POSITIVE, which combines with
the loop exit heuristic, so the exit's probability falls about as far as a third exit makes it fall.  Count-down and remaining forms, tails, matchAt on or off."""
import itertools, sys
import fl7lib as K

CM = {'bk': 'buf[i] == key[0]', 'kb': 'key[0] == buf[i]'}
SCAN = "\t\t\tp = &buf[i];\n\t\t\tfor (j = 0; j < len; j++)\n\t\t\t\tif (p[j] != key[j])\n\t\t\t\t\tj = len + 1;\n"
TL = {
    'q': "\t\t\tif (j == len) {\n\t\t\t\tunsigned char *q = &buf[i + len];\n\n\t\t\t\tif (*q != 0)\n\t\t\t\t\treturn i + len;\n\t\t\t}\n",
    'n': "\t\t\tif (j == len) {\n\t\t\t\tif (buf[i + len] != 0)\n\t\t\t\t\treturn i + len;\n\t\t\t}\n",
    'a': "\t\t\tif (j == len && buf[i + len] != 0)\n\t\t\t\treturn i + len;\n",
    'c': "\t\t\tif (j == len) {\n\t\t\t\tif (buf[i + len] == 0)\n\t\t\t\t\tcontinue;\n\t\t\t\treturn i + len;\n\t\t\t}\n",
}
LP = {
    'a': ('', '', "for (i = 0; xb.iniSize - len - i > 0; i++)"),
    'b': ('', '', "for (i = 0; xb.iniSize - i - len > 0; i++)"),
    'g': ('', '', "for (i = 0; xb.iniSize - (i + len) > 0; i++)"),
    'c': ('\tint left;\n', '', "for (i = 0, left = xb.iniSize - len; left > 0; i++, left--)"),
    'c2': ('\tint left;\n', '\tleft = xb.iniSize - len;\n', "for (i = 0; left > 0; i++, left--)"),
    'd': ('\tint left;\n', '\tleft = xb.iniSize - len;\n', "for (i = 0; left - i > 0; i++)"),
    'e': ('\tint left;\n', '\tleft = xb.iniSize - len;\n', "for (i = 0; left > 0; left--, i++)"),
    'f': ('\tint left;\n', '', "for (i = 0; (left = xb.iniSize - len - i) > 0; i++)"),
    'h': ('\tint left;\n', '', "for (i = 0; (left = xb.iniSize - i) > len; i++)"),
    'w': ('', '', "for (i = 0; 0 < xb.iniSize - len - i; i++)"),
}
V = {}
for (lk, (dc, pre, lp)), (ck, c), (tk, t) in itertools.product(LP.items(), CM.items(), TL.items()):
    V['%s,%s,%s' % (lk, ck, tk)] = K.fk("/* getters' own helper (not memFindStr) */\nstatic int findKey(unsigned char *buf, const char *key)\n{\n\tint i, j, len;\n\tunsigned char *p;\n" + dc + "\tlen = strlen(key);\n" + pre +
                                         "\t" + lp + " {\n\t\tif (" + c + ") {\n" + SCAN + t + "\t\t}\n\t}\n\treturn -1;\n}\n")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        K.diff(V[sys.argv[1]])
    else:
        print(len(V))
        K.run(V, 'b', 30)
