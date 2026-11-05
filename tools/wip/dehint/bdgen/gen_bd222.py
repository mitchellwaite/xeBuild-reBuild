"""Attempt 11: t5le alone off (src keeps the `*pr` expect and the asm).  Only the alignment of the last no-key log differs:
it needs the SE copy's jmp block at frequency <= 1, i.e. P(xb.type <= 5) >= 62.5% on that copy (57.96% now, 98.69% with
the label; the joiner `xb.type <= 5` itself is 50% at profile_estimate, 85% with the label).  Axes: shapes that put a
predictor on the joiner's edges."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun

SET = 'setFlashBuild(getBeU16(xb.files[i].data + 2));\n'
TAIL = ('		if (xb.type <= BUILD_DEVGL16) {\n		t5le: __attribute__((hot));\n			if (__builtin_expect(*pr != 0, 0))\n'
        '				goto fail;\n			break;\n		}\n		if (type == 14)\n			' + SET + '		break;\n')
NOLAB = TAIL.replace('		t5le: __attribute__((hot));\n', '')
HEAD = '/* load the input file e (xb.files[i]) by its type */\nstatic void loadBl('
H1 = 'static void seFlashBuild(uint32_t i, int type)\n{\n	if (type == 14)\n		' + SET + '}\n\n'
H2 = 'static void seFlashBuild(struct fileent *e, int type)\n{\n	if (type == 14)\n		setFlashBuild(getBeU16(e->data + 2));\n}\n\n'

FORMS = {
    'nolab': (None, NOLAB),
    'h1': (H1, NOLAB.replace('		if (type == 14)\n			' + SET, '		seFlashBuild(i, type);\n')),
    'h2': (H2, NOLAB.replace('		if (type == 14)\n			' + SET, '		seFlashBuild(&xb.files[i], type);\n')),
    'pr1': (None, NOLAB.replace('__builtin_expect(*pr != 0, 0)', '__builtin_expect(*pr == (uint32_t)-1, 0)')),
    'gt': (None, '		if (xb.type > BUILD_DEVGL16) {\n			if (type == 14)\n				' + SET + '			break;\n		}\n'
           '		if (__builtin_expect(*pr != 0, 0))\n			goto fail;\n		break;\n'),
    'lt6': (None, NOLAB.replace('xb.type <= BUILD_DEVGL16', 'xb.type < BUILD_DEVKIT')),
}


def mk(t, k):
    h, tail = FORMS[k]
    t = bdrun.sub(t, TAIL, tail, 1)
    if h:
        t = bdrun.sub(t, HEAD, h + HEAD, 1)
    return t


def CASES(base):
    return [(k, lambda b, k=k: mk(b, k)) for k in FORMS]


FOCUS = ['_loadBlFiles']
