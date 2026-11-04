"""fl10f.py [label]: iniBoolInvalid's own shape on the skipNul base (fl10e), where only its r149 is off by a usage of about 8.  Post-loop blocks set ebx's starting usage."""
import itertools, sys, re
import fllib as L, fl10lib as F, fl10a as A, fl10e as E

BASE = E.form('q1', 'p', 'bk', 0)
OLD = BASE[BASE.index('char *iniBoolInvalid(const char *key)'):BASE.index('unsigned int getIniU32(const char *key')]

HEADS = {
    'early': ("\tif (xb.iniSize == 0)\n\t\treturn NULL;\n\toff = FIND;\n\tif (off == -1)\n\t\treturn NULL;\n\tval = (char *)&xb.iniBuf[off];\n", ''),
    'nest': ("\tif (xb.iniSize != 0) {\n\t\toff = FIND;\n\t\tif (off != -1) {\n\t\t\tval = (char *)&xb.iniBuf[off];\n", "\t\t}\n\t}\n"),
    'nest2': ("\tif (xb.iniSize == 0)\n\t\treturn NULL;\n\toff = FIND;\n\tif (off != -1) {\n\t\tval = (char *)&xb.iniBuf[off];\n", "\t}\n"),
}
BODIES = {
    's': "if (strnicmp(val, \"true\", 4) == 0)\n\treturn NULL;\nif (strnicmp(val, \"false\", 5) != 0)\n\treturn val;\nreturn NULL;\n",
    'r': "if (strnicmp(val, \"true\", 4) == 0)\n\treturn NULL;\nif (strnicmp(val, \"false\", 5) == 0)\n\treturn NULL;\nreturn val;\n",
    'a': "if (strnicmp(val, \"true\", 4) != 0 && strnicmp(val, \"false\", 5) != 0)\n\treturn val;\nreturn NULL;\n",
    'o': "if (strnicmp(val, \"true\", 4) == 0 || strnicmp(val, \"false\", 5) == 0)\n\treturn NULL;\nreturn val;\n",
    'n': "if (strnicmp(val, \"true\", 4) != 0) {\n\tif (strnicmp(val, \"false\", 5) != 0)\n\t\treturn val;\n}\nreturn NULL;\n",
    'e': "if (strnicmp(val, \"true\", 4) == 0)\n\treturn NULL;\nelse if (strnicmp(val, \"false\", 5) == 0)\n\treturn NULL;\nelse\n\treturn val;\n",
    't': "if (strnicmp(val, \"true\", 4) == 0)\n\treturn NULL;\nreturn strnicmp(val, \"false\", 5) != 0 ? val : NULL;\n",
    'v0': "if (strnicmp(val, \"true\", 4) != 0 && strnicmp(val, \"false\", 5) != 0)\n\tret = val;\nreturn ret;\n",
    'v1': "if (strnicmp(val, \"true\", 4) != 0)\n\tif (strnicmp(val, \"false\", 5) != 0)\n\t\tret = val;\nreturn ret;\n",
    'c': "cmp = strnicmp(val, \"true\", 4);\nif (cmp == 0)\n\treturn NULL;\ncmp = strnicmp(val, \"false\", 5);\nif (cmp != 0)\n\treturn val;\nreturn NULL;\n",
    'f': "if (strnicmp(val, \"false\", 5) == 0)\n\treturn NULL;\nif (strnicmp(val, \"true\", 4) != 0)\n\treturn val;\nreturn NULL;\n",
    'vb': "if (getBoolWord(val) < 0)\n\treturn val;\nreturn NULL;\n",
}
HELPER = "static int getBoolWord(const char *val)\n{\n\tif (strnicmp(val, \"true\", 4) == 0)\n\t\treturn 1;\n\tif (strnicmp(val, \"false\", 5) == 0)\n\t\treturn 0;\n\treturn -1;\n}\n"


def ind(t, n):
    return ''.join('\t' * n + l for l in t.splitlines(True))


def mk(hk, bk):
    h, t = HEADS[hk]
    n = 1 if hk == 'early' else (3 if hk == 'nest' else 2)
    decl = "\tint off;\n\tchar *val;\n"
    if bk in ('v0', 'v1'):
        decl += "\tchar *ret = NULL;\n"
    if bk == 'c':
        decl += "\tint cmp;\n"
    tail = '' if hk == 'early' else "\treturn NULL;\n"
    new = "char *iniBoolInvalid(const char *key)\n{\n" + decl + h + ind(BODIES[bk], n) + t + tail + "}\n"
    if bk == 'vb':
        new = HELPER + new
    if bk in ('v0', 'v1') and hk != 'early':
        new = new.replace("return NULL;\n}", "return ret;\n}")
    return L.sub(BASE, OLD, new)


V = {'%s,%s' % (h, b): mk(h, b) for h, b in itertools.product(HEADS, BODIES)}

if __name__ == '__main__':
    if len(sys.argv) > 1:
        F.diff(V[sys.argv[1]])
    else:
        F.run(V, 'f', show=40)
