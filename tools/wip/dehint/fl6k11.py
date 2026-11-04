"""fl6k11.py: matchAt base; the getters' lookup: an iniVal helper (all subsets of getters), and forms of iniU32Invalid's head."""
import itertools, sys
import fllib as L, fl6lib as F, fl6k10 as K

BASE = K.V['10,t,q,buf']
A = BASE.index('char *iniU32Invalid(const char *key)')
HDR = "\tint off;\n\tchar *val;\n\tif (xb.iniSize == 0)\n\t\treturn NULL;\n\toff = FIND;\n\tif (off == -1)\n\t\treturn NULL;\n\tval = (char *)&xb.iniBuf[off];\n"
U = BASE[A:]
assert HDR in U
U32H = {
    'nest': None,
    'and': "\tint off = -1;\n\tchar *val;\n\tif (xb.iniSize != 0)\n\t\toff = FIND;\n\tif (off == -1)\n\t\treturn NULL;\n\tval = (char *)&xb.iniBuf[off];\n",
    'or': "\tint off;\n\tchar *val;\n\tif (xb.iniSize == 0 || (off = FIND) == -1)\n\t\treturn NULL;\n\tval = (char *)&xb.iniBuf[off];\n",
    'neg': "\tint off;\n\tchar *val;\n\tif (xb.iniSize == 0)\n\t\treturn NULL;\n\toff = FIND;\n\tif (off < 0)\n\t\treturn NULL;\n\tval = (char *)&xb.iniBuf[off];\n",
    'ptr': "\tint off;\n\tchar *val = NULL;\n\tif (xb.iniSize == 0)\n\t\treturn val;\n\toff = FIND;\n\tif (off == -1)\n\t\treturn val;\n\tval = (char *)&xb.iniBuf[off];\n",
    'tern': "\tint off;\n\tchar *val;\n\toff = xb.iniSize ? FIND : -1;\n\tif (off == -1)\n\t\treturn NULL;\n\tval = (char *)&xb.iniBuf[off];\n",
    'val': "\tchar *val;\n\tint off;\n\tif (xb.iniSize != 0) {\n\t\toff = FIND;\n\t\tif (off != -1)\n\t\t\tgoto have;\n\t}\n\treturn NULL;\nhave:\n\tval = (char *)&xb.iniBuf[off];\n",
}
V = {}
for k, h in U32H.items():
    if h is None:
        continue
    V['u32h=' + k] = BASE[:A] + U.replace(HDR, h)
# iniVal helper, used by a subset
HELP = ("/* the value for key in the loaded ini, or NULL */\nstatic char *iniVal(const char *key)\n{\n\tint off;\n\n\tif (xb.iniSize == 0)\n\t\treturn NULL;\n"
        "\toff = FIND;\n\tif (off == -1)\n\t\treturn NULL;\n\treturn (char *)&xb.iniBuf[off];\n}\n\n")
G = {
    'b': ("long getIniBool(const char *key, int def)\n{\n\tint off;\n\tchar *val;\n\tif (xb.iniSize == 0)\n\t\treturn def;\n\toff = FIND;\n\tif (off == -1)\n\t\treturn def;\n\tval = (char *)&xb.iniBuf[off];\n",
          "long getIniBool(const char *key, int def)\n{\n\tchar *val = iniVal(key);\n\n\tif (val == NULL)\n\t\treturn def;\n"),
    'B': ("char *iniBoolInvalid(const char *key)\n{\n\tint off;\n\tchar *val;\n\tif (xb.iniSize == 0)\n\t\treturn NULL;\n\toff = FIND;\n\tif (off == -1)\n\t\treturn NULL;\n\tval = (char *)&xb.iniBuf[off];\n",
          "char *iniBoolInvalid(const char *key)\n{\n\tchar *val = iniVal(key);\n\n\tif (val == NULL)\n\t\treturn NULL;\n"),
    'u': ("unsigned int getIniU32(const char *key, unsigned int def)\n{\n\tint off;\n\tif (xb.iniSize == 0)\n\t\treturn def;\n\toff = FIND;\n\tif (off == -1)\n\t\treturn def;\n\treturn myatou32((char *)&xb.iniBuf[off], def);\n",
          "unsigned int getIniU32(const char *key, unsigned int def)\n{\n\tchar *val = iniVal(key);\n\n\tif (val == NULL)\n\t\treturn def;\n\treturn myatou32(val, def);\n"),
    'U': ("char *iniU32Invalid(const char *key)\n{\n\tint off;\n\tchar *val;\n\tif (xb.iniSize == 0)\n\t\treturn NULL;\n\toff = FIND;\n\tif (off == -1)\n\t\treturn NULL;\n\tval = (char *)&xb.iniBuf[off];\n",
          "char *iniU32Invalid(const char *key)\n{\n\tchar *val = iniVal(key);\n\n\tif (val == NULL)\n\t\treturn NULL;\n"),
}
for r in range(1, 5):
    for sub in itertools.combinations('bBuU', r):
        s = BASE
        for c in sub:
            s = L.sub(s, G[c][0], G[c][1])
        d = "#define FIND findKey(xb.iniBuf, key)\n"
        s = L.sub(s, d, d + HELP)
        V['iniVal=' + ''.join(sub)] = s
print(len(V))
if __name__ == '__main__':
    F.run(V, 'k11', 24)
