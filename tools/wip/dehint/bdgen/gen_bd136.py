"""loadConsoleBlFiles' loop in error-variable forms, the cold label and precheck gone: the return 0 has to sort after r = 1, so the loop's exits have to change."""
import itertools, re

PRECHECK = '''	/* the cold label gives the shrink-wrapped return 0 frequency 0, so
	   bb-reorder lays it out last */
	if ((uint32_t)xb.nFiles <= 1)
		goto none;
'''
TAIL = '''		if (r) {
			log_printf(0, "\\n\\n**** could not read %s (%i) ****\\n\\n", e->name, r);
			return -1;
		}
	}
	return 0;
none: __attribute__((cold));
	return 0;
}
'''
HEAD = '''int loadConsoleBlFiles(void)
{
	struct fileent *e;
	uint32_t i;
	uint32_t r;

'''
LOG = 'log_printf(0, "\\n\\n**** could not read %s (%i) ****\\n\\n", e->name, r);\n'


def forms():
    yield 'plain', HEAD, 'for (i = 1; i < (uint32_t)xb.nFiles; i++) {\n\t\te = &xb.files[i];\n\t\tr = 0;\n', '\t\tif (r) {\n\t\t\t' + LOG + '\t\t\treturn -1;\n\t\t}\n\t}\n\treturn 0;\n}\n'
    H2 = HEAD.replace('uint32_t r;\n', 'uint32_t r;\n\tint ret = 0;\n')
    yield 'ret', H2, 'for (i = 1; i < (uint32_t)xb.nFiles; i++) {\n\t\te = &xb.files[i];\n\t\tr = 0;\n', '\t\tif (r) {\n\t\t\t' + LOG + '\t\t\tret = -1;\n\t\t\tbreak;\n\t\t}\n\t}\n\treturn ret;\n}\n'
    yield 'ret2', H2, 'for (i = 1; !ret && i < (uint32_t)xb.nFiles; i++) {\n\t\te = &xb.files[i];\n\t\tr = 0;\n', '\t\tif (r) {\n\t\t\t' + LOG + '\t\t\tret = -1;\n\t\t}\n\t}\n\treturn ret;\n}\n'
    yield 'ret3', H2, 'for (i = 1; i < (uint32_t)xb.nFiles && !ret; i++) {\n\t\te = &xb.files[i];\n\t\tr = 0;\n', '\t\tif (r) {\n\t\t\t' + LOG + '\t\t\tret = -1;\n\t\t}\n\t}\n\treturn ret;\n}\n'
    H3 = HEAD.replace('uint32_t r;\n', 'uint32_t r = 0;\n')
    yield 'r1', H3, 'for (i = 1; i < (uint32_t)xb.nFiles && !r; i++) {\n\t\te = &xb.files[i];\n', '\t\tif (r)\n\t\t\t' + LOG + '\t}\n\treturn r ? -1 : 0;\n}\n'
    yield 'r2', H3, 'for (i = 1; !r && i < (uint32_t)xb.nFiles; i++) {\n\t\te = &xb.files[i];\n', '\t\tif (r)\n\t\t\t' + LOG + '\t}\n\treturn r ? -1 : 0;\n}\n'
    H4 = HEAD.replace('\tuint32_t i;\n', '\tint i;\n')
    yield 'inti', H4, 'for (i = 1; i < xb.nFiles; i++) {\n\t\te = &xb.files[i];\n\t\tr = 0;\n', '\t\tif (r) {\n\t\t\t' + LOG + '\t\t\treturn -1;\n\t\t}\n\t}\n\treturn 0;\n}\n'
    yield 'wh', HEAD, 'i = 1;\n\twhile (i < (uint32_t)xb.nFiles) {\n\t\te = &xb.files[i];\n\t\tr = 0;\n', '\t\tif (r) {\n\t\t\t' + LOG + '\t\t\treturn -1;\n\t\t}\n\t\ti++;\n\t}\n\treturn 0;\n}\n'
    yield 'ptr', HEAD, 'for (i = 1, e = &xb.files[1]; i < (uint32_t)xb.nFiles; i++, e++) {\n\t\tr = 0;\n', '\t\tif (r) {\n\t\t\t' + LOG + '\t\t\treturn -1;\n\t\t}\n\t}\n\treturn 0;\n}\n'
    yield 'cont', HEAD, 'for (i = 1; i < (uint32_t)xb.nFiles; i++) {\n\t\te = &xb.files[i];\n\t\tr = 0;\n', '\t\tif (!r)\n\t\t\tcontinue;\n\t\t' + LOG + '\t\treturn -1;\n\t}\n\treturn 0;\n}\n'


def CASES(base):
    a = base.index(HEAD)
    b = base.index('/* the header bytes freeboot/xell read')
    f = base[a:b]
    i = f.index('\t\tif (strnicmp(e->name, "none", 4) || e->crc) {')
    j = f.index(TAIL)
    mid = f[i:j]
    out = []
    for name, h, lp, tl in forms():
        s = h + '\t' + lp + mid + tl + '\n'
        out.append((name, base[:a] + s + base[b:]))
    return out
