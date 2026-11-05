"""loadBl, vol_fail off: case 23 after case 2, so crossjump can share the -1 of case 2's failure (the fully matched block has to have the lower index)."""
import itertools, importlib.util, os
spec = importlib.util.spec_from_file_location('g107', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_bd107.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
C23, C2, T, END, LOG = g.C23, g.C2, g.T, g.END, g.LOG
EXP = '__builtin_expect(*pr != 0, 0)'
B23 = '''	case 23:
		if (xb.type == BUILD_RETAIL)
			break;
		*pr = loadBinFile(e);
		if (*pr)
			break;
		if (e->size & 3) {
		badsize: __attribute__((hot));
''' + C23 + '''		}
		appendAddonPatches(e);
		break;
'''
DEF = '	default:\n		log_printf(1, "####### unhandled bl load'


def body(lab, tail):
    s = B23.replace('		badsize: __attribute__((hot));\n', '') if not lab else B23
    return s.replace(C23, LOG + tail)


def CASES(base):
    assert B23 in base
    out = []
    F2 = {
        'lab': '		if (!e->offset) {\n		fail:\n			*pr = -1;\n		}\n		break;\n',
        'brk': '		if (!e->offset)\n			*pr = -1;\n		break;\n',
        'goto': C2,
    }
    FT = {'brk': '			if (%s)\n				*pr = -1;\n			break;\n' % EXP, 'goto': T}
    F23 = {'brk': '			*pr = -1;\n			break;\n', 'ret': '			*pr = -1;\n			return;\n', 'goto': '			goto fail;\n'}
    EE = {'none': '	return;\n}\n', 'fail': '	return;\nfail:\n	*pr = -1;\n}\n'}
    for (a, va), (b, vb), (c, vc), (en, ve), lab, pos in itertools.product(F23.items(), F2.items(), FT.items(), EE.items(), (0, 1), ('after2', 'afterdef')):
        labs = (b == 'lab') + (en != 'none')
        uses = (a == 'goto') + (b == 'goto') + (c == 'goto')
        if labs != (1 if uses else 0) and not (b == 'lab' and uses == 0 and False):
            continue
        t = base.replace(B23, '')
        if pos == 'after2':
            t = t.replace(DEF, body(lab, va) + DEF)
        else:
            k = t.index(DEF)
            k2 = t.index('		break;\n	}\n	return;\n', k)
            t = t[:k2] + '		break;\n' + body(lab, va) + t[k2 + len('		break;\n'):]
        t = t.replace(C2, vb).replace(T, vc).replace(END, ve)
        out.append(('%s %s %s %s lab%d %s' % (a, b, c, en, lab, pos), t))
    return out
