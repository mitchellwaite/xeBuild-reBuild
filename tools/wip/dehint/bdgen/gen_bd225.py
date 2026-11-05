"""Attempt 11, the near miss's size log (gen_bd210 `b f brk`): case 23 through a read helper that checks the size and
returns -1, so the -1 is a return value (PHI in the helper) instead of a store in the size log's block."""
import os, sys, importlib.util
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun
d = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('g210', os.path.join(d, 'gen_bd210.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

LOG = g.LOG
C23 = ('		*pr = loadBinFile(e);\n		if (*pr)\n			break;\n		if (e->size & 3) {\n		badsize: __attribute__((hot));\n			' + LOG +
       '			*pr = -1;\n			break;\n		}\n		appendAddonPatches(e);\n		break;\n')
HEAD = '/* load the input file e (xb.files[i]) by its type */\nstatic void loadBl('
HELP = {
    'r': ('static int loadPatchFile(struct fileent *e)\n{\n	int r;\n\n	r = loadBinFile(e);\n	if (r)\n		return r;\n	if (e->size & 3) {\n		' + LOG +
          '		return -1;\n	}\n	appendAddonPatches(e);\n	return 0;\n}\n\n', '		*pr = loadPatchFile(e);\n		break;\n'),
    'r2': ('static int loadPatchFile(struct fileent *e)\n{\n	int r;\n\n	r = loadBinFile(e);\n	if (!r && (e->size & 3)) {\n		' + LOG +
           '		r = -1;\n	}\n	return r;\n}\n\n', '		*pr = loadPatchFile(e);\n		if (!*pr)\n			appendAddonPatches(e);\n		break;\n'),
    'r3': ('static int loadPatchFile(struct fileent *e)\n{\n	if (loadBinFile(e))\n		return 1;\n	if (e->size & 3) {\n		' + LOG +
           '		return -1;\n	}\n	return 0;\n}\n\n', '		*pr = loadPatchFile(e);\n		if (!*pr)\n			appendAddonPatches(e);\n		break;\n'),
}


def mk(t, k, base):
    if base == 'nm':
        t = g.mk(t, 'b', 'f', 'brk')
        old = C23
    else:
        old = C23.replace('			*pr = -1;\n			break;\n', '			goto fail;\n')
    h, body = HELP[k]
    t = bdrun.sub(t, old, body, 1)
    return bdrun.sub(t, HEAD, h + HEAD, 1)


def CASES(base):
    return [('%s %s' % (k, b), lambda t, k=k, b=b: mk(t, k, b)) for k in HELP for b in ('nm', 'src')]


FOCUS = ['_loadBlFiles']
