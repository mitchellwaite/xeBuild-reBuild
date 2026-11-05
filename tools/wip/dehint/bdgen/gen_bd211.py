"""From gen_bd210's `b f brk` (no asm, no t5le label, no *pr expect; size log sets -1 and breaks; 11 strict lines): case 2's
position in the switch and its -1 form.

Crossjump (cfgcleanup.c try_crossjump_bb / try_crossjump_to_edge) with a 1-insn match only proceeds when the 'from'
block, the lower-indexed of the two (or the non-fallthru one against a fallthru pred), is wholly matched.  The smc -1
block is wholly `mov edi,-1`, the size log's is not, so the smc block must come before the size log in block order."""
import itertools, os, sys, importlib.util
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun
d = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('g210', os.path.join(d, 'gen_bd210.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

C2_START = '	case 2:\n'
C2_END = '		if (!e->offset)\n			goto fail;\n		break;\n'
FAIL_END = ('	return;\n	/* one -1 block for the patch size, SMC and (xb.type <= BUILD_DEVGL16) signature\n'
            '	   failures: the asm keeps it a block of its own (else the -1 is appended\n'
            '	   to the size log, which crossjump can\'t then share) */\nfail:\n	*pr = -1;\n}\n')
FORMS = {
    'goto': C2_END,
    'blk': '		if (!e->offset) {\n			*pr = -1;\n			break;\n		}\n		break;\n',
    'set': '		if (!e->offset)\n			*pr = -1;\n		break;\n',
}
BEFORE = {
    'src': None,
    'b23': '	case 23:\n',
    'b4': '	case 4:\n',
    'b3': '	case 3:\n',
    'b25': '	case 25:\n',
    'b1': '	case 1:\n',
    'b24': '	case 24:\n',
    'b6': '	case 6:\n',
}


def mk(base, form, where):
    t = g.mk(base, 'b', 'f', 'brk')
    s = t.index('static void loadBl(')
    i = t.index(C2_START, s)
    j = t.index('	default:\n', i)
    c2 = t[i:j]
    assert C2_END in c2
    c2 = c2.replace(C2_END, FORMS[form])
    t = t[:i] + t[j:]
    k = t.index(BEFORE[where] if where != 'src' else '	default:\n', s)
    t = t[:k] + c2 + t[k:]
    if form != 'goto':
        t = bdrun.sub(t, FAIL_END, '}\n', 1)
    return t


def CASES(base):
    return [('%s %s' % (f, w), lambda b, f=f, w=w: mk(b, f, w)) for f, w in itertools.product(FORMS, BEFORE)]


FOCUS = ['_loadBlFiles']
