"""Attempt 11: if/else spellings of the tail with no t5le label, the `*pr` expect and asm kept (src otherwise).
gen_bd223's `brk exp` (kit arm first, break in it) is 4 loose; `and exp` 2 loose but its sig-failed type != 14 path goes to
`fail`.  These are the explicit else forms."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun

SET = 'setFlashBuild(getBeU16(xb.files[i].data + 2));\n'
TAIL = ('		if (xb.type <= BUILD_DEVGL16) {\n		t5le: __attribute__((hot));\n			if (__builtin_expect(*pr != 0, 0))\n'
        '				goto fail;\n			break;\n		}\n		if (type == 14)\n			' + SET + '		break;\n')
PR = '__builtin_expect(*pr != 0, 0)'
FORMS = {
    'g1': '		if (xb.type > BUILD_DEVGL16) {\n			if (type == 14)\n				' + SET + '		} else if (' + PR + ')\n			goto fail;\n		break;\n',
    'g2': '		if (xb.type <= BUILD_DEVGL16) {\n			if (' + PR + ')\n				goto fail;\n		} else if (type == 14)\n			' + SET + '		break;\n',
    'g3': '		if (xb.type <= BUILD_DEVGL16) {\n			if (' + PR + ')\n				goto fail;\n			break;\n		} else if (type == 14)\n			' + SET + '		break;\n',
    'g4': '		if (xb.type > BUILD_DEVGL16) {\n			if (type == 14)\n				' + SET + '		} else {\n			if (' + PR + ')\n				goto fail;\n		}\n		break;\n',
    'g5': '		if (xb.type <= BUILD_DEVGL16) {\n			if (' + PR + ')\n				goto fail;\n		} else {\n			if (type == 14)\n				' + SET + '		}\n		break;\n',
    'g6': '		if (xb.type > BUILD_DEVGL16) {\n			if (type == 14)\n				' + SET + '			break;\n		}\n		if (' + PR + ')\n			goto fail;\n		break;\n',
    'g7': '		if (xb.type > BUILD_DEVGL16) {\n			if (type == 14)\n				' + SET + '			return;\n		}\n		if (' + PR + ')\n			goto fail;\n		break;\n',
    'g8': '		if (xb.type > BUILD_DEVGL16) {\n			if (type == 14)\n				' + SET + '			break;\n		}\n		if (' + PR + ')\n			goto fail;\n		return;\n',
}


def CASES(base):
    out = []
    for k, f in FORMS.items():
        out.append((k, lambda b, f=f: bdrun.sub(b, TAIL, f, 1)))
        out.append((k + ' plain', lambda b, f=f: bdrun.sub(b, TAIL, f.replace(PR, '*pr'), 1)))
    return out


FOCUS = ['_loadBlFiles']
