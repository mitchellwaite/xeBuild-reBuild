"""lb6's loadBl written in loadBlFiles' loop: r is a real variable from the start, so its tests are threaded early.  Axes as gen_bd142, with forms of `goto chk`."""
import itertools, re, importlib.util, os
d = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('g140', os.path.join(d, 'gen_bd140.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
spec = importlib.util.spec_from_file_location('g133', os.path.join(d, 'gen_bd133.py'))
gi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gi)

BASE = 'build/bd/a5/lb6.c'


def ws(old):
    return r'[ \t]*' + r'\n[ \t]*'.join(re.escape(l) for l in old.split('\n'))


def PRE(b):
    b = b.replace('__asm__("" : "+a"(d));\n', '@PIN@\n')
    t = gi.inline(b, fail='none')
    t = re.sub(ws('goto fail;\n}\nappendAddonPatches'), 'r = -1;\nbreak;\n}\nappendAddonPatches', t, count=1)
    t = re.sub(ws('if (!e->offset)\ngoto fail;'), 'if (!e->offset)\nr = -1;', t, count=1)
    return t


def CASES(base):
    a = base.index('if (type == 5 || type == 17 || type == 11) {')
    b = base.index('case 6:', a)
    b = base.rindex('\n', 0, b) + 1
    out = []
    for s, ty, fl, gt, pin in itertools.product(g.SIGS, ('or',), g.FL, ('chk', 'r0', 'if'), (0, 1)):
        S = g.SIGS[s].replace('*pr', 'r')
        body = g.TY[ty].replace('@@', S)
        new = body + g.FL[fl] + '}\nbreak;\n'
        t = base[:a] + new + base[b:]
        t = t.replace('@PIN@', '__asm__("" : "+a"(d));' if pin else '')
        if gt == 'r0':
            t = re.sub(ws('break;\ngoto chk;'), 'break;\nr = 0;\ngoto chk;', t, count=1)
        elif gt == 'if':
            t = re.sub(ws('break;\ngoto chk;\n} else\nbreak;\n}'), 'break;\n} else\nbreak;\nr = 0;\n}', t, count=1)
        out.append(('%s %s %s %s pin%d' % (s, ty, fl, gt, pin), t))
    return out
