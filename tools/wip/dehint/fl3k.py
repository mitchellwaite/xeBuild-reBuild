"""fl3k.py: no pin.  findKey tails that read xb.iniBuf (what `buf != xb.iniBuf` did, without a test), x iniU32Invalid shapes."""
import itertools, sys
import fllib as L

L.FLAGS[:] = ['-O3']
B = L.base()
PIN = '\t__asm__("" :: "b"(val));\n'
B = L.sub(B, PIN, '')
UNR = '''				unsigned char *q = &buf[i + len];

				if (q == 0)
					__builtin_unreachable();
				if (*q != 0)
					return i + len;
'''
R = '\t\t\t\tif (*q != 0)\n\t\t\t\t\treturn i + len;\n'
Q = '\t\t\t\tunsigned char *q = &buf[i + len];\n\n'
TAILS = {
 'ne': Q + '\t\t\t\tif (buf != xb.iniBuf)\n\t\t\t\t\treturn -1;\n' + R,
 'ne2': Q + '\t\t\t\tif (xb.iniBuf != buf)\n\t\t\t\t\treturn -1;\n' + R,
 'eq': Q + '\t\t\t\tif (buf == xb.iniBuf) {\n\t' + R.replace('\n\t\t\t\t\t', '\n\t\t\t\t\t\t') + '\t\t\t\t}\n',
 'g': '\t\t\t\tunsigned char *q = &xb.iniBuf[i + len];\n\n' + R,
 'g2': '\t\t\t\tif (xb.iniBuf[i + len] != 0)\n\t\t\t\t\treturn i + len;\n',
 'gn': '\t\t\t\tunsigned char *q = &xb.iniBuf[i + len];\n\n\t\t\t\tif (buf == NULL)\n\t\t\t\t\treturn -1;\n' + R,
 'gn2': '\t\t\t\tif (xb.iniBuf == NULL)\n\t\t\t\t\treturn -1;\n\t\t\t\tif (xb.iniBuf[i + len] != 0)\n\t\t\t\t\treturn i + len;\n',
 'gl': '\t\t\t\tunsigned char *b = xb.iniBuf;\n\n\t\t\t\tif (b == NULL)\n\t\t\t\t\treturn -1;\n\t\t\t\tif (b[i + len] != 0)\n\t\t\t\t\treturn i + len;\n',
 'gq': Q + '\t\t\t\tif (q == xb.iniBuf)\n\t\t\t\t\treturn -1;\n' + R,
 'gr': Q + '\t\t\t\tif (buf != xb.iniBuf || *q == 0)\n\t\t\t\t\tcontinue;\n\t\t\t\treturn i + len;\n',
 'ga': Q + '\t\t\t\tif (buf == xb.iniBuf && *q != 0)\n\t\t\t\t\treturn i + len;\n',
}
U = '''	val = (char *)&xb.iniBuf[off];
	if (val[0] == '0' && myatol(val[1]) == 'x') {
		if (validateString(val + 2) == 0)
			return val;
		return NULL;
	}
	if (validateString(val) != 0)
		return NULL;
	return val;
'''
US = {
 'o': U,
 'el': U.replace("		return NULL;\n	}\n	if (validateString(val) != 0)", "		return NULL;\n	} else if (validateString(val) != 0)"),
 'eq': U.replace('	if (validateString(val) != 0)\n		return NULL;\n	return val;\n', '	if (validateString(val) == 0)\n		return val;\n	return NULL;\n'),
 'nest': U.replace("if (val[0] == '0' && myatol(val[1]) == 'x') {", "if (val[0] == '0') {\n\t\tif (myatol(val[1]) == 'x') {").replace("		return NULL;\n	}\n	if (validate", "		return NULL;\n		}\n	}\n	if (validate"),
 'ptr': U.replace('val[0]', '*val'),
 'c': U.replace("	if (val[0] == '0' && myatol(val[1]) == 'x') {\n		if (validateString(val + 2) == 0)\n			return val;\n		return NULL;\n	}\n	if (validateString(val) != 0)", "	if (val[0] == '0' && myatol(val[1]) == 'x')\n		off = validateString(val + 2);\n	else\n		off = validateString(val);\n	if (off != 0)"),
 'p2': U.replace('	if (validateString(val) != 0)', '	else if (validateString(val) != 0)').replace('		return NULL;\n	}\n	else', '		return NULL;\n	} else'),
 'ret': "	val = (char *)&xb.iniBuf[off];\n	if (val[0] == '0' && myatol(val[1]) == 'x')\n		return validateString(val + 2) == 0 ? val : NULL;\n	return validateString(val) == 0 ? val : NULL;\n",
 'ret2': "	val = (char *)&xb.iniBuf[off];\n	if (val[0] == '0' && myatol(val[1]) == 'x') {\n		if (validateString(val + 2) != 0)\n			return NULL;\n		return val;\n	}\n	if (validateString(val) != 0)\n		return NULL;\n	return val;\n",
 'ret3': "	val = (char *)&xb.iniBuf[off];\n	if (val[0] != '0' || myatol(val[1]) != 'x') {\n		if (validateString(val) != 0)\n			return NULL;\n		return val;\n	}\n	if (validateString(val + 2) == 0)\n		return val;\n	return NULL;\n",
}
V = {}
for t, u in itertools.product(TAILS, US):
    s = L.sub(B, UNR, TAILS[t])
    s = L.sub(s, U, US[u])
    V[t + '_' + u] = s
print(len(V))
rs = L.sweep(V, prefix='k3', show=45, workers=2)
