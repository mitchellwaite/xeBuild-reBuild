"""loadBl with vol_fail off: the `fail` label inside the arm of case 2 or of the signature tail, or case 23's log after the store."""
import itertools
import importlib.util, os
spec = importlib.util.spec_from_file_location('g107', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_bd107.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
C23, C2, T, END, LOG = g.C23, g.C2, g.T, g.END, g.LOG
EXP = '__builtin_expect(*pr != 0, 0)'


def CASES(base):
    out = []
    F23 = {
        'goto': C23,
        'brk': LOG + '			*pr = -1;\n			break;\n',
        'ret': LOG + '			*pr = -1;\n			return;\n',
        'first': '			*pr = -1;\n' + LOG + '			break;\n',
    }
    F2 = {
        'goto': C2,
        'brk': '		if (!e->offset)\n			*pr = -1;\n		break;\n',
        'lab': '		if (!e->offset) {\n		fail:\n			*pr = -1;\n		}\n		break;\n',
    }
    FT = {
        'goto': T,
        'brk': '			if (%s)\n				*pr = -1;\n			break;\n' % EXP,
        'lab': '			if (%s) {\n			fail:\n				*pr = -1;\n			}\n			break;\n' % EXP,
    }
    EE = {'none': '	return;\n}\n', 'fail': '	return;\nfail:\n	*pr = -1;\n}\n', 'if0': '	if (0) {\nfail:\n		*pr = -1;\n	}\n}\n'}
    for (a, va), (b, vb), (c, vc), (en, ve) in itertools.product(F23.items(), F2.items(), FT.items(), EE.items()):
        labs = (b == 'lab') + (c == 'lab') + (en != 'none')
        uses = (a == 'goto') + (b == 'goto') + (c == 'goto')
        if labs != (1 if uses else 0):
            continue
        t = base.replace(C23, va).replace(C2, vb).replace(T, vc).replace(END, ve)
        out.append(('%s %s %s %s' % (a, b, c, en), t))
    return out
