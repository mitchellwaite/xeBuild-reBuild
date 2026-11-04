"""flxb.py: iniBoolInvalid without the pin, grid over val type/local forms and test shapes."""
import itertools
import fllib as L

L.FLAGS[:] = ['-O3']
B = L.base()
SIG = 'char *iniBoolInvalid(const char *key)'
a = B.index(SIG)
b = B.index('unsigned int getIniU32(')
VT = {'c': ('char *val;', '(char *)', ''), 'cc': ('const char *val;', '(const char *)', '(char *)'), 'u': ('unsigned char *val;', '', '(char *)'), 'v': ('void *val;', '', '(char *)')}
GET = {
 'g': '\tif (xb.iniSize == 0)\n\t\treturn NULL;\n\toff = FIND;\n\tif (off == -1)\n\t\treturn NULL;\n\tval = %s&xb.iniBuf[off];\n',
 'lt': '\tif (xb.iniSize == 0)\n\t\treturn NULL;\n\toff = FIND;\n\tif (off < 0)\n\t\treturn NULL;\n\tval = %s&xb.iniBuf[off];\n',
 'n': '\tif (xb.iniSize == 0)\n\t\treturn NULL;\n\toff = FIND;\n\tif (off != -1) {\n\t\tval = %s&xb.iniBuf[off];\n',
 'p': '\tif (xb.iniSize == 0)\n\t\treturn NULL;\n\toff = FIND;\n\tif (off == -1)\n\t\treturn NULL;\n\tval = %sxb.iniBuf + off;\n',
 'nn': '\tif (xb.iniSize != 0) {\n\toff = FIND;\n\tif (off != -1) {\n\t\tval = %s&xb.iniBuf[off];\n',
}
TEST = {
 'o': 'if (strnicmp(%(v)sval, "true", 4) == 0)\n\t\treturn NULL;\n\tif (strnicmp(%(v)sval, "false", 5) != 0)\n\t\treturn %(r)sval;\n\treturn NULL;\n',
 'e': 'if (strnicmp(%(v)sval, "true", 4) == 0)\n\t\treturn NULL;\n\telse if (strnicmp(%(v)sval, "false", 5) == 0)\n\t\treturn NULL;\n\telse\n\t\treturn %(r)sval;\n',
 'n': 'if (strnicmp(%(v)sval, "true", 4) != 0) {\n\t\tif (strnicmp(%(v)sval, "false", 5) != 0)\n\t\t\treturn %(r)sval;\n\t}\n\treturn NULL;\n',
 'n2': 'if (strnicmp(%(v)sval, "true", 4) == 0)\n\t\treturn NULL;\n\tif (strnicmp(%(v)sval, "false", 5) == 0)\n\t\treturn NULL;\n\treturn %(r)sval;\n',
 'rt': 'ret = %(r)sval;\n\tif (strnicmp(%(v)sval, "true", 4) == 0)\n\t\tret = NULL;\n\telse if (strnicmp(%(v)sval, "false", 5) == 0)\n\t\tret = NULL;\n\treturn ret;\n',
 'ptr': 'if (strnicmp(%(v)sval, "true", 4) != 0 && strnicmp(%(v)sval, "false", 5) != 0)\n\t\treturn %(r)sval;\n\treturn NULL;\n',
}
V = {}
for vt, g, t in itertools.product(VT, GET, TEST):
    d, cast, use = VT[vt]
    r = {'c': '', 'cc': '(char *)', 'u': '(char *)', 'v': ''}[vt]
    v = {'c': '', 'cc': '', 'u': '(char *)', 'v': ''}[vt]
    body = SIG + '\n{\n\tint off;\n\t' + d + '\n'
    if t == 'rt':
        body += '\tchar *ret;\n'
    gt = GET[g] % cast
    body += gt + '\t' + TEST[t] % {'v': v, 'r': r}
    close = {'n': '\t}\n\treturn NULL;\n', 'nn': '\t}\n\t}\n\treturn NULL;\n'}.get(g, '')
    body += close + '}\n'
    V['%s_%s_%s' % (vt, g, t)] = B[:a] + body + B[b:]
print(len(V))
L.sweep(V, prefix='b', show=20)
