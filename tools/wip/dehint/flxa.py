"""flxa.py: helper shapes: memFindChar, memFindStr's result handling, against several dead states;
findKey with a result variable."""
import itertools, os, sys
import fllib as L, flx as X, flx3 as A

MC = '''int memFindChar(unsigned char *buf, char c, int size)
{
	int i;

	for (i = 0; i < size; i++)
		if (buf[i] == c)
			return i;
	return -1;
}
'''
MCS = {
 'cur': MC,
 'ret_brk': 'int memFindChar(unsigned char *buf, char c, int size)\n{\n\tint i, ret = -1;\n\n\tfor (i = 0; i < size; i++)\n\t\tif (buf[i] == c) {\n\t\t\tret = i;\n\t\t\tbreak;\n\t\t}\n\treturn ret;\n}\n',
 'ret_set': 'int memFindChar(unsigned char *buf, char c, int size)\n{\n\tint i, ret = -1;\n\n\tfor (i = 0; i < size; i++)\n\t\tif (buf[i] == c) {\n\t\t\tret = i;\n\t\t\ti = size;\n\t\t}\n\treturn ret;\n}\n',
 'ret_set2': 'int memFindChar(unsigned char *buf, char c, int size)\n{\n\tint i, ret;\n\n\tret = -1;\n\tfor (i = 0; i < size; i++) {\n\t\tif (buf[i] == c) {\n\t\t\tret = i;\n\t\t\ti = size + 1;\n\t\t}\n\t}\n\treturn ret;\n}\n',
 'j': 'int memFindChar(unsigned char *buf, char c, int size)\n{\n\tint i;\n\n\tfor (i = 0; i < size; i++)\n\t\tif (buf[i] == c)\n\t\t\tbreak;\n\tif (i < size)\n\t\treturn i;\n\treturn -1;\n}\n',
 'j2': 'int memFindChar(unsigned char *buf, char c, int size)\n{\n\tint i;\n\n\tfor (i = 0; i < size; i++)\n\t\tif (buf[i] == c)\n\t\t\tbreak;\n\tif (i == size)\n\t\treturn -1;\n\treturn i;\n}\n',
 'while': 'int memFindChar(unsigned char *buf, char c, int size)\n{\n\tint i = 0;\n\n\twhile (i < size) {\n\t\tif (buf[i] == c)\n\t\t\treturn i;\n\t\ti++;\n\t}\n\treturn -1;\n}\n',
 'ptr': 'int memFindChar(unsigned char *buf, char c, int size)\n{\n\tint i;\n\tchar *p = (char *)buf;\n\n\tfor (i = 0; i < size; i++)\n\t\tif (p[i] == c)\n\t\t\treturn i;\n\treturn -1;\n}\n',
 'rev': 'int memFindChar(unsigned char *buf, char c, int size)\n{\n\tint i;\n\n\tfor (i = 0; i < size; i++)\n\t\tif (c == buf[i])\n\t\t\treturn i;\n\treturn -1;\n}\n',
 'cast': 'int memFindChar(unsigned char *buf, char c, int size)\n{\n\tint i;\n\n\tfor (i = 0; i < size; i++)\n\t\tif ((char)buf[i] == c)\n\t\t\treturn i;\n\treturn -1;\n}\n',
}
STATES = {
 'A': ((), 'asm'),
 'S': (('comma', 'i', 'off3', 'off4', 'off5', 't', 'len'), 'nest'),
 'Z': (tuple(X.ALLDEAD), 'nest'),
 'N': (('i', 'off3', 'off5', 't'), 'nest'),
 'T': (('t', 'len'), 'asm'),
 'Y': (('comma', 'i', 'off3', 'off4', 'off5', 't', 'len'), 'asm'),
}
V = {}
for st, (d, fl) in STATES.items():
    base = X.gen(d, fl)
    for m, t in MCS.items():
        V[st + '_' + m] = L.sub(base, MC, t)
rs = L.sweep(V, prefix='mc', show=60)
