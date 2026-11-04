"""fl6k8.py: matchAt (fl6k7 h2) base; iniU32Invalid's body in natural forms, for movsx key[0]'s register."""
import itertools, sys
import fllib as L, fl6lib as F, fl6k7 as K

BASE = K.V['h2,q,bk']
OLD = BASE[BASE.index("char *iniU32Invalid(const char *key)"):BASE.index("/* load and pre-parse options.ini")]
HEADS = {
    'plain': "char *iniU32Invalid(const char *key)\n{\n\tint off;\n\tchar *val;\n\tif (xb.iniSize == 0)\n\t\treturn NULL;\n\toff = FIND;\n\tif (off == -1)\n\t\treturn NULL;\n\tval = (char *)&xb.iniBuf[off];\n",
    'noval': None,
}
HX = {
    'and': "\tif (val[0] == '0' && myatol(val[1]) == 'x') {\n@@\t}\n",
    'nest': "\tif (val[0] == '0') {\n\t\tif (myatol(val[1]) == 'x') {\n@@\t\t}\n\t}\n",
}
IN = {
    'eq': "\t\tif (validateString(val + 2) == 0)\n\t\t\treturn val;\n\t\treturn NULL;\n",
    'ne': "\t\tif (validateString(val + 2) != 0)\n\t\t\treturn NULL;\n\t\treturn val;\n",
    'ifelse': "\t\tif (validateString(val + 2) == 0)\n\t\t\treturn val;\n\t\telse\n\t\t\treturn NULL;\n",
    'ifelse2': "\t\tif (validateString(val + 2) != 0)\n\t\t\treturn NULL;\n\t\telse\n\t\t\treturn val;\n",
    'bang': "\t\tif (!validateString(val + 2))\n\t\t\treturn val;\n\t\treturn NULL;\n",
    'tern': "\t\treturn validateString(val + 2) ? NULL : val;\n",
    'tern2': "\t\treturn validateString(val + 2) == 0 ? val : NULL;\n",
    'ret': "\t\tif (validateString(val + 2) != 0)\n\t\t\tval = NULL;\n\t\treturn val;\n",
}
END = {
    'ne': "\tif (validateString(val) != 0)\n\t\treturn NULL;\n\treturn val;\n",
    'eq': "\tif (validateString(val) == 0)\n\t\treturn val;\n\treturn NULL;\n",
    'tern': "\treturn validateString(val) ? NULL : val;\n",
    'ret': "\tif (validateString(val) != 0)\n\t\tval = NULL;\n\treturn val;\n",
    'else': None,
}
V = {}
for hx, i_, e in itertools.product(HX, IN, END):
    body = HX[hx].replace('@@', IN[i_])
    if e == 'else':
        body = body.rstrip('\n') + ' else ' + '{\n\t\tif (validateString(val) != 0)\n\t\t\treturn NULL;\n\t\treturn val;\n\t}\n'
        body += '\treturn NULL;\n'
    else:
        body += END[e]
    src = HEADS['plain'] + body + "}\n\n"
    V['%s,%s,%s' % (hx, i_, e)] = BASE.replace(OLD, src)
print(len(V))
if __name__ == '__main__':
    F.run(V, 'k8', 25)
