"""fl6k4.py: findKey's tail written with j where it's equal to len (DOM/VRP copy it in after inlining)."""
import itertools, sys
import fllib as L, fl6lib as F

S = F.drop(F.S0, ['KF'])
OLD = "\t\t\tif (j == len) {\n\t\t\t\tunsigned char *q = &buf[i + len];\n\n\t\t\t\tif (*q != 0)\n\t\t\t\t\treturn i + len;\n\t\t\t}\n"
assert S.count(OLD) == 1
A = ['i + len', 'i + j', 'j + i', 'len + i']
TL = {
    'q': "unsigned char *q = &buf[@1];\n\n\t\t\t\tif (*q != 0)\n\t\t\t\t\treturn @2;\n",
    'n': "if (buf[@1] != 0)\n\t\t\t\t\treturn @2;\n",
    'c': "if (buf[@1] == 0)\n\t\t\t\t\tcontinue;\n\t\t\t\treturn @2;\n",
    'pl': "if (p[len] != 0)\n\t\t\t\t\treturn @2;\n",
    'pj': "if (p[j] != 0)\n\t\t\t\t\treturn @2;\n",
    'cpj': "if (p[j] == 0)\n\t\t\t\t\tcontinue;\n\t\t\t\treturn @2;\n",
    'qp': "unsigned char *q = &p[j];\n\n\t\t\t\tif (*q != 0)\n\t\t\t\t\treturn @2;\n",
    'qd': "if (*(p + j) != 0)\n\t\t\t\t\treturn @2;\n",
    'off': "int off = @1;\n\n\t\t\t\tif (buf[off] != 0)\n\t\t\t\t\treturn off;\n",
}
HD = {'eq': 'j == len', 'le': 'j <= len'}
CM = ['buf[i] == key[0]', 'key[0] == buf[i]']
V = {}
for tk, a1, a2, hk, c in itertools.product(TL, A, A, HD, CM):
    t = TL[tk]
    if '@1' not in t and a1 != A[0]:
        continue
    if '@2' not in t and a2 != A[0]:
        continue
    t = t.replace('@1', a1).replace('@2', a2)
    s = L.sub(S, OLD, '\t\t\tif (%s) {\n\t\t\t\t%s\t\t\t}\n' % (HD[hk], t))
    s = L.sub(s, 'if (buf[i] == key[0])', 'if (%s)' % c)
    V['%s,%s,%s,%s,%s' % (tk, a1.replace(' ', ''), a2.replace(' ', ''), hk, c[:3])] = s
print(len(V))
if __name__ == '__main__':
    F.run(V, 'k4', 20)
