"""fl6k3.py: findKey's `j == len` written so that it only becomes == after inlining (VRP folds j <= len at the loop exit), tails, compare."""
import itertools, sys
import fllib as L, fl6lib as F

S = F.drop(F.S0, ['KF'])
OLD = "\t\t\tif (j == len) {\n\t\t\t\tunsigned char *q = &buf[i + len];\n\n\t\t\t\tif (*q != 0)\n\t\t\t\t\treturn i + len;\n\t\t\t}\n"
assert S.count(OLD) == 1
HD = {
    'le': ('if (j <= len)', 0), 'lt1': ('if (j < len + 1)', 0), 'ngt': ('if (!(j > len))', 0), 'sub': ('if (j - len == 0)', 0),
    'nsub': ('if (!(j - len))', 0), 'eq': ('if (j == len)', 0), 'ge': ('if (len >= j)', 0), 'neq': ('if (len == j)', 0),
    'gtc': ('if (j > len)\n\t\t\t\tcontinue;\n', 1), 'nec': ('if (j != len)\n\t\t\t\tcontinue;\n', 1),
}
TL = {
    'q': "unsigned char *q = &buf[i + len];\n\n\t\t\t\tif (*q != 0)\n\t\t\t\t\treturn i + len;\n",
    'n': "if (buf[i + len] != 0)\n\t\t\t\t\treturn i + len;\n",
    'p': "if (p[len] != 0)\n\t\t\t\t\treturn i + len;\n",
    'c': "if (buf[i + len] == 0)\n\t\t\t\t\tcontinue;\n\t\t\t\treturn i + len;\n",
    'cp': "if (p[len] == 0)\n\t\t\t\t\tcontinue;\n\t\t\t\treturn i + len;\n",
    'cq': "unsigned char *q = &buf[i + len];\n\n\t\t\t\tif (*q == 0)\n\t\t\t\t\tcontinue;\n\t\t\t\treturn i + len;\n",
}
MM = {'len1': 'j = len + 1;', 'len': 'j = len;', 'brk': 'break;', 'len2': 'j = len + 2;', 'big': 'j = 0x7ffffffe;'}
CM = ['buf[i] == key[0]', 'key[0] == buf[i]']
V = {}
for (hk, (h, f)), (tk, t), mk, c in itertools.product(HD.items(), TL.items(), ['len1', 'brk', 'len2'], CM):
    if mk == 'brk' and hk in ('le', 'ngt', 'lt1', 'gtc', 'ge'):
        pass
    if f:
        body = '\t\t\t' + h + '\t\t\t{\n\t\t\t\t' + t + '\t\t\t}\n'
    else:
        body = '\t\t\t' + h + ' {\n\t\t\t\t' + t + '\t\t\t}\n'
    s = L.sub(S, OLD, body)
    s = L.sub(s, 'if (buf[i] == key[0])', 'if (%s)' % c)
    if mk != 'len1':
        s = L.sub(s, "\t\t\t\tif (p[j] != key[j])\n\t\t\t\t\tj = len + 1;\n", "\t\t\t\tif (p[j] != key[j])\n\t\t\t\t\t%s\n" % MM[mk])
    V['%s,%s,%s,%s' % (hk, tk, mk, c[:3])] = s
print(len(V))
if __name__ == '__main__':
    F.run(V, 'k3', 16)
