"""fl3a.py: findKey's unreachable and iniBoolInvalid's pin, plain-C forms (grid)."""
import itertools
import fllib as L

L.FLAGS[:] = ['-O3']
B = L.base()
UNR = '''				if (q == 0)
					__builtin_unreachable();
				if (*q != 0)
					return i + len;
'''
PIN = '\t__asm__("" :: "b"(val));\n'
FK = {
 'keep': UNR,
 'and': '\t\t\t\tif (q && *q)\n\t\t\t\t\treturn i + len;\n',
 'and2': '\t\t\t\tif (q != NULL && *q != 0)\n\t\t\t\t\treturn i + len;\n',
 'nest': '\t\t\t\tif (q != NULL) {\n\t\t\t\t\tif (*q != 0)\n\t\t\t\t\t\treturn i + len;\n\t\t\t\t}\n',
 'ret': '\t\t\t\tif (q == NULL)\n\t\t\t\t\treturn -1;\n\t\t\t\tif (*q != 0)\n\t\t\t\t\treturn i + len;\n',
 'cont': '\t\t\t\tif (q == NULL)\n\t\t\t\t\tcontinue;\n\t\t\t\tif (*q != 0)\n\t\t\t\t\treturn i + len;\n',
 'brk': '\t\t\t\tif (q == NULL)\n\t\t\t\t\tbreak;\n\t\t\t\tif (*q != 0)\n\t\t\t\t\treturn i + len;\n',
 'stor': '\t\t\t\tif (q == NULL)\n\t\t\t\t\tlen = 0;\n\t\t\t\tif (*q != 0)\n\t\t\t\t\treturn i + len;\n',
 'endl': '\t\t\t\tif (q == NULL)\n\t\t\t\t\ti = xb.iniSize;\n\t\t\t\telse if (*q != 0)\n\t\t\t\t\treturn i + len;\n',
 'rel': '\t\t\t\tif (q < buf)\n\t\t\t\t\treturn -1;\n\t\t\t\tif (*q != 0)\n\t\t\t\t\treturn i + len;\n',
 'neg': '\t\t\t\tif (i + len < 0)\n\t\t\t\t\treturn -1;\n\t\t\t\tif (*q != 0)\n\t\t\t\t\treturn i + len;\n',
 'none': '\t\t\t\tif (*q != 0)\n\t\t\t\t\treturn i + len;\n',
 'pq': '\t\t\t\tif (p && *q)\n\t\t\t\t\treturn i + len;\n',
 'bq': '\t\t\t\tif (buf && *q)\n\t\t\t\t\treturn i + len;\n',
}
PN = {
 'keep': PIN,
 'none': '',
 'tv': '\tif (val == NULL)\n\t\treturn NULL;\n',
 'tv2': '\tif (val != NULL) {\n\t\tif (strnicmp(val, "true", 4) == 0)\n\t\t\treturn NULL;\n\t\tif (strnicmp(val, "false", 5) != 0)\n\t\t\treturn val;\n\t}\n\treturn NULL;\n#if 0\n',
 'tv3': '\tif (val == NULL)\n\t\treturn val;\n',
 'tv4': '\tif (!val)\n\t\toff = 0;\n',
 'tv5': '\tif (val == NULL)\n\t\tval = "";\n',
}
s0 = L.sub(B, '\tif (strnicmp(val, "false", 5) != 0)\n\t\treturn val;\n\treturn NULL;\n}\nunsigned', '\tif (strnicmp(val, "false", 5) != 0)\n\t\treturn val;\n\treturn NULL;\n#ENDIF\n}\nunsigned')
V = {}
for f, pn in itertools.product(FK, PN):
    s = L.sub(s0, UNR, FK[f])
    s = L.sub(s, PIN, PN[pn])
    s = s.replace('#ENDIF\n', '#endif\n' if pn == 'tv2' else '')
    if f in ('neg',) :
        pass
    V[f + '_' + pn] = s
print(len(V))
rs = L.sweep(V, prefix='a3', show=40)
