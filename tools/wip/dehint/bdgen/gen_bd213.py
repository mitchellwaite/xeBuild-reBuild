"""From gen_bd210's `b f brk` (3 loose, 11 strict): tail and size-log forms that might fix its two differences, the SE copy's
`ja` for `jbe` and the size log's own `mov edi,-1`.  `lab` keeps the t5le hot label on the plain break (one trick back)."""
import itertools, os, sys, importlib.util
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun
d = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('g210', os.path.join(d, 'gen_bd210.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

SET = g.SET
LOG = g.LOG
g.TAILS.update({
    'lab': '		if (xb.type <= BUILD_DEVGL16) {\n		t5le: __attribute__((hot));\n			break;\n		}\n		if (type == 14)\n			' + SET + '		break;\n',
    'gt': '		if (xb.type > BUILD_DEVGL16) {\n			if (type == 14)\n				' + SET + '		}\n		break;\n',
    'ne': '		if (xb.type <= BUILD_DEVGL16 || type != 14)\n			break;\n		' + SET + '		break;\n',
    'ne2': '		if (xb.type > BUILD_DEVGL16 && type == 14)\n			' + SET + '		break;\n',
})
g.SIZE.update({
    'b2': '		if (e->size & 3) {\n		badsize: __attribute__((hot));\n			' + LOG + '			*pr = -1;\n		} else\n			appendAddonPatches(e);\n		break;\n',
    'b3': '		if (!(e->size & 3)) {\n			appendAddonPatches(e);\n			break;\n		}\n		badsize: __attribute__((hot));\n		' + LOG + '		*pr = -1;\n		break;\n',
})
APP = '		appendAddonPatches(e);\n		break;\n	case 27:'


def mk(base, size, tail):
    t = g.mk(base, size if size in ('b', 'g') else 'g', 'f', tail)
    if size not in ('b', 'g'):
        t = bdrun.sub(t, g.SIZE['g'] + APP, g.SIZE[size] + '	case 27:', 1)
    return t


def CASES(base):
    return [('%s %s' % (s, tl), lambda b, s=s, tl=tl: mk(b, s, tl))
            for s, tl in itertools.product(('b', 'b2', 'b3'), ('brk', 'lab', 'gt', 'ne', 'ne2'))]


FOCUS = ['_loadBlFiles']
