"""Attempt 11: tail forms on attempt 10's near miss (gen_bd210 `b f brk`) for the SE copy's `ja` (it needs P(xb.type <= 5) > 50%).

vrp1's joiner threads go (pred, xb.type test) joiner; (<=5 edge, if (r)) normal, and each one subtracts its share from
the joiner's <=5 edge count (tree-ssa-threadupdate.c compute_path_counts / update_profile), so later copies get 0%.
Axes here: how xb.type is tested in the tail."""
import os, sys, importlib.util
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun
d = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('g210', os.path.join(d, 'gen_bd210.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

SET = g.SET
BRK = g.TAILS['brk']


def PRE(t):
    return g.mk(t, 'b', 'f', 'brk')


TAILS = {
    'brk': BRK,
    'lt6': BRK.replace('xb.type <= BUILD_DEVGL16', 'xb.type < BUILD_DEVKIT'),
    'sw': '		switch (xb.type) {\n		case BUILD_RETAIL: case BUILD_JTAG: case BUILD_GLITCH: case BUILD_DEVGL: case BUILD_DEVGL16:\n'
          '			break;\n		default:\n			if (type == 14)\n				' + SET + '		}\n		break;\n',
    'sw2': '		switch (xb.type) {\n		case BUILD_DEVKIT: case BUILD_DEVKIT16: case BUILD_TESTKIT: case BUILD_TESTKIT16:\n'
           '			if (type == 14)\n				' + SET + '			break;\n		}\n		break;\n',
    'elif': None,  # else if (type == 14 && xb.type > 5) after the signature block
    'gtnest': '		if (xb.type > BUILD_DEVGL16)\n			if (type == 14)\n				' + SET + '		break;\n',
    'ret': '		if (xb.type <= BUILD_DEVGL16)\n			return;\n		if (type == 14)\n			' + SET + '		break;\n',
    'rng': BRK.replace('xb.type <= BUILD_DEVGL16', 'xb.type - 1 < BUILD_DEVGL16'),
    'nk': BRK.replace('xb.type <= BUILD_DEVGL16', '!(xb.type > BUILD_DEVGL16)'),
    'ne14': '		if (xb.type <= BUILD_DEVGL16 || type != 14)\n			break;\n		' + SET + '		break;\n',
    'loc': None,  # kit = xb.type > 5 read before checkBl
}

SIG_END = '				log_printf(1, "loaded %s, could not check signature rsa key not present!\\n", e->name);\n		}\n'


def mk(t, k):
    if k == 'elif':
        t = bdrun.sub(t, SIG_END + BRK, SIG_END[:-4] + '		} else if (type == 14 && xb.type > BUILD_DEVGL16)\n			' + SET + '		break;\n', 1)
        return t
    if k == 'loc':
        t = bdrun.sub(t, BRK, '		if (!kit)\n			break;\n		if (type == 14)\n			' + SET + '		break;\n', 1)
        t = bdrun.sub(t, '	chk:\n		*pr = checkBl(', '	chk:\n		kit = xb.type > BUILD_DEVGL16;\n		*pr = checkBl(', 1)
        t = bdrun.sub(t, 'static void loadBl(struct fileent *e, uint32_t i, uint32_t *pr)\n{\n	int type;\n',
                      'static void loadBl(struct fileent *e, uint32_t i, uint32_t *pr)\n{\n	int type, kit;\n', 1)
        return t
    return bdrun.sub(t, BRK, TAILS[k], 1)


def CASES(base):
    return [(k, lambda b, k=k: mk(b, k)) for k in TAILS]


FOCUS = ['_loadBlFiles']
