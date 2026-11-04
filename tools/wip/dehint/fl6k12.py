"""fl6k12.py: a third loop exit that is live: the value test as two returns that ifcombine merges after the profile (`c > 0`, `c < 0`)."""
import itertools, sys
import fllib as L, fl6lib as F

S = F.drop(F.S0, ['KF'])
OLD = "\t\t\tif (j == len) {\n\t\t\t\tunsigned char *q = &buf[i + len];\n\n\t\t\t\tif (*q != 0)\n\t\t\t\t\treturn i + len;\n\t\t\t}\n"
assert S.count(OLD) == 1
Q = "unsigned char *q = &buf[i + len];\n\n\t\t\t\t"
T = {
    'gl': Q + "if (*(char *)q > 0)\n\t\t\t\t\treturn i + len;\n\t\t\t\tif (*(char *)q < 0)\n\t\t\t\t\treturn i + len;\n",
    'lg': Q + "if (*(char *)q < 0)\n\t\t\t\t\treturn i + len;\n\t\t\t\tif (*(char *)q > 0)\n\t\t\t\t\treturn i + len;\n",
    'cgl': "char c = buf[i + len];\n\n\t\t\t\tif (c > 0)\n\t\t\t\t\treturn i + len;\n\t\t\t\tif (c < 0)\n\t\t\t\t\treturn i + len;\n",
    'clg': "char c = buf[i + len];\n\n\t\t\t\tif (c < 0)\n\t\t\t\t\treturn i + len;\n\t\t\t\tif (c > 0)\n\t\t\t\t\treturn i + len;\n",
    'hi': Q + "if (*q >= 0x80)\n\t\t\t\t\treturn i + len;\n\t\t\t\tif (*q != 0)\n\t\t\t\t\treturn i + len;\n",
    'ge1': Q + "if (*q >= 0x20)\n\t\t\t\t\treturn i + len;\n\t\t\t\tif (*q != 0)\n\t\t\t\t\treturn i + len;\n",
}
V = {}
for k, t in T.items():
    V[k] = L.sub(S, OLD, '\t\t\tif (j == len) {\n\t\t\t\t' + t + '\t\t\t}\n')
print(len(V))
if __name__ == '__main__':
    F.run(V, 'k12', 8)
