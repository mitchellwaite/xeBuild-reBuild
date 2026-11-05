"""loadBl's shared -1 block without the asm barrier (attempt 10).

Without the asm, `fail:` is an empty block with a virtual PHI (its three predecessors have different memory states), so
mergephi2 (pass_merge_phi, tree-cfgcleanup.c) takes it as a forwarder with PHIs and merges it, splitting the smc and t5le
edges, whose arguments differ.  Axes: where the -1 sites go (end-of-function orders, size log at the end, per-site stores),
the t5le tail's form, and whether the t5le label and *pr expect stay."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun

LOG = 'log_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);\n'
SIZE_SRC = ('		if (e->size & 3) {\n		badsize: __attribute__((hot));\n			' + LOG + '			goto fail;\n		}\n')
END_SRC = '	return;\n	/* one -1 block'
TAIL_SRC = ('		if (xb.type <= BUILD_DEVGL16) {\n		t5le: __attribute__((hot));\n			if (__builtin_expect(*pr != 0, 0))\n'
            '				goto fail;\n			break;\n		}\n		if (type == 14)\n			setFlashBuild(getBeU16(xb.files[i].data + 2));\n		break;\n')
SET = 'setFlashBuild(getBeU16(xb.files[i].data + 2));\n'

SIZE = {
    'g': SIZE_SRC,  # goto fail (src)
    'b': '		if (e->size & 3) {\n		badsize: __attribute__((hot));\n			' + LOG + '			*pr = -1;\n			break;\n		}\n',
    'e': '		if (e->size & 3)\n			goto badsize;\n',  # log at the end
}
ENDS = {
    'f': '',  # fail: *pr = -1 (src without the asm)
    'bf': 'badsize:\n	LOG	*pr = -1;\n	return;\n',  # badsize block, then fail
    'bff': 'badsize:\n	LOG',  # badsize falls into fail
}
ENDS_AFTER = {
    'fb': '	return;\nbadsize:\n	LOG	*pr = -1;\n',
}
TAILS = {
    'src': TAIL_SRC,
    'pl': TAIL_SRC.replace('__builtin_expect(*pr != 0, 0)', '*pr != 0'),
    'nl': TAIL_SRC.replace('		t5le: __attribute__((hot));\n', ''),
    'nlpl': TAIL_SRC.replace('		t5le: __attribute__((hot));\n', '').replace('__builtin_expect(*pr != 0, 0)', '*pr != 0'),
    'brk': '		if (xb.type <= BUILD_DEVGL16)\n			break;\n		if (type == 14)\n			' + SET + '		break;\n',
    'and': '		if (xb.type > BUILD_DEVGL16 && type == 14)\n			' + SET + '		break;\n',
}


def mk(t, size, end, tail):
    t = bdhints.off(t, 'vol_fail')
    t = bdrun.sub(t, SIZE_SRC, SIZE[size], 1)
    t = bdrun.sub(t, TAIL_SRC, TAILS[tail], 1)
    if end in ENDS:
        t = bdrun.sub(t, END_SRC, '	return;\n' + ENDS[end].replace('LOG', LOG) + '	/* one -1 block', 1)
    else:
        t = bdrun.sub(t, '	*pr = -1;\n}\n\nint loadBlFiles', '	*pr = -1;\n' + ENDS_AFTER[end].replace('LOG', LOG) + '}\n\nint loadBlFiles', 1)
    return t


def CASES(base):
    out = []
    for size, end, tail in itertools.product(SIZE, list(ENDS) + list(ENDS_AFTER), TAILS):
        if size == 'e' and end == 'f':
            continue
        if size != 'e' and end != 'f':
            continue
        out.append(('%s %s %s' % (size, end, tail), lambda b, s=size, e=end, tl=tail: mk(b, s, e, tl)))
    return out


FOCUS = ['_loadBlFiles']
