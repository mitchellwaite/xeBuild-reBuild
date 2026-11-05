"""From gen_bd210's `b f brk`: case 2's `goto fail` target placed inside the switch, before the size log.

The smc -1 block then keeps a low block index (a source block with one predecessor has no virtual PHI, so mergephi
leaves it, and cleanup_tree_cfg's remove_forwarder_block refuses it because the smc test also reaches the join with
another value).  At jump2, crossjump's 1-insn match needs the lower-indexed block wholly matched: that is now the
`mov edi,-1` block, so it can be redirected into the size log's tail, as the reference has it."""
import itertools, os, sys, importlib.util
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun
d = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('g210', os.path.join(d, 'gen_bd210.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

FAIL_END = ('	return;\n	/* one -1 block for the patch size, SMC and (xb.type <= BUILD_DEVGL16) signature\n'
            '	   failures: the asm keeps it a block of its own (else the -1 is appended\n'
            '	   to the size log, which crossjump can\'t then share) */\nfail:\n	*pr = -1;\n}\n')
FAIL = '	fail:\n		*pr = -1;\n		break;\n'
WHERE = {
    'b23': '	case 23:\n',
    'b4': '	case 4:\n',
    'b3': '	case 3:\n',
    'b25': '	case 25:\n',
    'b22': '	case 22:\n',
    'b1': '	case 1:\n',
    'b24': '	case 24:\n',
    'b6': '	case 6:\n		if (!xb.cbb)',
    'b27': '	case 27:\n',
    'b2': '	case 2:\n		*pr = loadBaseFile',
}
TAILS = ['brk', 'and', 'src', 'nlpl']


def mk(base, where, tail, size):
    t = g.mk(base, size, 'f', tail)
    t = bdrun.sub(t, FAIL_END, '}\n', 1)
    i = t.index('static void loadBl(')
    k = t.index(WHERE[where], i)
    return t[:k] + FAIL + t[k:]


def CASES(base):
    return [('%s %s %s' % (w, tl, s), lambda b, w=w, tl=tl, s=s: mk(b, w, tl, s))
            for w, tl, s in itertools.product(WHERE, TAILS, ('b', 'g'))]


FOCUS = ['_loadBlFiles']
