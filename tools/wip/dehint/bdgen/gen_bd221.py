"""Attempt 11: the near miss's tail through a small helper that isn't early inlined (two calls), so at profile_estimate the
`xb.type > 5` edge leads to a call: PRED_CALL against it, DS with early return gives P(<=5) about 61% (39% now)."""
import os, sys, importlib.util
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun
d = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('g220', os.path.join(d, 'gen_bd220.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
PRE = g.PRE
BRK = g.BRK
SET = g.SET
HEAD = '/* load the input file e (xb.files[i]) by its type */\nstatic void loadBl('

HELPERS = {
    'h1': ('static void seFlashBuild(uint32_t i, int type)\n{\n	if (type == 14)\n		' + SET + '}\n\n',
           '		if (xb.type > BUILD_DEVGL16)\n			seFlashBuild(i, type);\n		break;\n'),
    'h2': ('static void seFlashBuild(uint32_t i, int type)\n{\n	if (type == 14)\n		' + SET + '}\n\n',
           '		if (xb.type <= BUILD_DEVGL16)\n			break;\n		seFlashBuild(i, type);\n		break;\n'),
    'h3': ('static void seFlashBuild(const uint8_t *se)\n{\n	setFlashBuild(getBeU16(se + 2));\n}\n\n',
           '		if (xb.type <= BUILD_DEVGL16)\n			break;\n		if (type == 14)\n			seFlashBuild(xb.files[i].data);\n		break;\n'),
    'h4': ('static void seFlashBuild(struct fileent *e, int type)\n{\n	if (type == 14)\n		setFlashBuild(getBeU16(e->data + 2));\n}\n\n',
           '		if (xb.type > BUILD_DEVGL16)\n			seFlashBuild(&xb.files[i], type);\n		break;\n'),
    'h5': ('static void kitFlashBuild(uint32_t i, int type)\n{\n	if (xb.type > BUILD_DEVGL16 && type == 14)\n		' + SET + '}\n\n',
           '		kitFlashBuild(i, type);\n		break;\n'),
}


def mk(t, k):
    h, tail = HELPERS[k]
    t = bdrun.sub(t, BRK, tail, 1)
    return bdrun.sub(t, HEAD, h + HEAD, 1)


def CASES(base):
    return [(k, lambda b, k=k: mk(b, k)) for k in HELPERS]


FOCUS = ['_loadBlFiles']
