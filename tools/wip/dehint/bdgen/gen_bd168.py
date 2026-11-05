"""lab_badsize: case 23 nested the way the author tends to nest, with the arm otherwise as in src."""
import itertools
LOG = 'log_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);\n'
OLD_START = '\tcase 23:\n'
OLD_END = '\tcase 27:\n'
SIZE = {
    'if': 'if (e->size & 3) {\n' + LOG + 'goto fail;\n}\nappendAddonPatches(e);\n',
    'else': 'if (e->size & 3) {\n' + LOG + 'goto fail;\n} else\nappendAddonPatches(e);\n',
    'not': 'if (!(e->size & 3)) {\nappendAddonPatches(e);\nbreak;\n}\n' + LOG + 'goto fail;\n',
    'notelse': 'if (!(e->size & 3))\nappendAddonPatches(e);\nelse {\n' + LOG + 'goto fail;\n}\n',
    'eq': 'if ((e->size & 3) == 0)\nappendAddonPatches(e);\nelse {\n' + LOG + 'goto fail;\n}\n',
    'rem': 'if (e->size % 4) {\n' + LOG + 'goto fail;\n}\nappendAddonPatches(e);\n',
}
OUTER = {
    'brk': 'if (xb.type == BUILD_RETAIL)\nbreak;\n*pr = loadBinFile(e);\nif (*pr)\nbreak;\nSIZE',
    'nest1': 'if (xb.type == BUILD_RETAIL)\nbreak;\n*pr = loadBinFile(e);\nif (!*pr) {\nSIZE}\n',
    'nest2': 'if (xb.type != BUILD_RETAIL) {\n*pr = loadBinFile(e);\nif (!*pr) {\nSIZE}\n}\n',
    'nest3': 'if (xb.type != BUILD_RETAIL) {\n*pr = loadBinFile(e);\nif (*pr)\nbreak;\nSIZE}\n',
}


def CASES(base):
    i = base.index(OLD_START, base.index('static void loadBl('))
    j = base.index(OLD_END, i)
    out = []
    for o, s in itertools.product(OUTER, SIZE):
        out.append(('%s %s' % (o, s), base[:i] + OLD_START + OUTER[o].replace('SIZE', SIZE[s]) + 'break;\n' + base[j:]))
    return out


FOCUS = ['_loadBlFiles']
