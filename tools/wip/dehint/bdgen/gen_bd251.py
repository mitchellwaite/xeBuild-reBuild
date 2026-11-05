"""Attempt 14: the reference's signature-failed path sends `xb.type <= 5` to the shared -1 block (37d0 jbe 33d4) but
`type != 14` straight to the log with the -1 already set (37d9), so the two exits are different statements.  Try the
<=5 exit in the failed arm itself (`if (xb.type <= BUILD_DEVGL16) goto fail;`), crossed with tail forms, the size
log's -1, and the barrier.  Runs on src/build.c as of eb75581."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun

LOG = 'log_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);\n'
SIZE_SRC = ('		if (e->size & 3) {\n		badsize: __attribute__((hot));\n			' + LOG + '			goto fail;\n		}\n')
TAIL_SRC = ('		if (xb.type <= BUILD_DEVGL16) {\n		t5le: __attribute__((hot));\n			if (__builtin_expect(*pr != 0, 0))\n'
            '				goto fail;\n			break;\n		}\n		if (type == 14)\n			setFlashBuild(getBeU16(xb.files[i].data + 2));\n		break;\n')
SET = 'setFlashBuild(getBeU16(xb.files[i].data + 2));\n'
ARM_SRC = ('					log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);\n'
           '					*pr = -1;\n')
GT = '					if (xb.type <= BUILD_DEVGL16)\n						goto fail;\n'
ARM = {
    'a0': ARM_SRC,
    'a1': ARM_SRC.replace('					*pr = -1;\n', GT + '					*pr = -1;\n'),
    'a2': ARM_SRC + GT,
}
TAILS = {
    'src': TAIL_SRC,
    'nl': TAIL_SRC.replace('		t5le: __attribute__((hot));\n', ''),
    'nlpl': TAIL_SRC.replace('		t5le: __attribute__((hot));\n', '').replace('__builtin_expect(*pr != 0, 0)', '*pr'),
    'and': '		if (xb.type > BUILD_DEVGL16 && type == 14)\n			' + SET + '		break;\n',
    'brk': '		if (xb.type <= BUILD_DEVGL16)\n			break;\n		if (type == 14)\n			' + SET + '		break;\n',
    'nest': '		if (xb.type > BUILD_DEVGL16) {\n			if (type == 14)\n				' + SET + '		}\n		break;\n',
}
SIZE = {
    'g': SIZE_SRC,
    'b': '		if (e->size & 3) {\n		badsize: __attribute__((hot));\n			' + LOG + '			*pr = -1;\n			break;\n		}\n',
}


def mk(t, arm, tail, size, vol):
    t = bdrun.sub(t, ARM_SRC, ARM[arm], 1)
    t = bdrun.sub(t, TAIL_SRC, TAILS[tail], 1)
    t = bdrun.sub(t, SIZE_SRC, SIZE[size], 1)
    if vol == 'nv':
        t = bdhints.off(t, 'vol_fail')
    return t


def CASES(base):
    out = []
    for arm, tail, size, vol in itertools.product(ARM, TAILS, SIZE, ('v', 'nv')):
        out.append(('%s %s %s %s' % (arm, tail, size, vol), lambda b, a=arm, tl=tail, s=size, v=vol: mk(b, a, tl, s, v)))
    return out


FOCUS = ['_loadBlFiles']
