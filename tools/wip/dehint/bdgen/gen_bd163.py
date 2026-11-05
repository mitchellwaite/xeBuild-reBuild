"""Order and form of the type test around the signature check (the Linux build tests 17, 5, 11).  No constant_p."""
import importlib.util, itertools, os
d = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('g161', os.path.join(d, 'gen_bd161.py'))
g1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g1)
g = g1.g
OLD = 'if (type == 5 || type == 17 || type == 11) {'
FORMS = {'%d,%d,%d' % p: 'if (type == %d || type == %d || type == %d) {' % p for p in itertools.permutations((5, 17, 11))}
FORMS['paren1'] = 'if ((type == 17 || type == 5) || type == 11) {'


def CASES(base):
    out = []
    for fm, tl, sg, t10, bad, in itertools.product(FORMS, ('src', 'failx', 'fail', 'failh', 'and', 'brk'), ('dead',), (0, 1), (0, 1)):
        def mk(b, fm=fm, tl=tl, sg=sg, t10=t10, bad=bad):
            t = g.with_arm(b, g.arm(sg, tl, 0, t10).replace(OLD, FORMS[fm]))
            t = g.nocp(t)
            return g.nobad(t) if bad else t
        out.append(('%s %s %s t%d bad%d' % (fm, tl, sg, t10, bad), mk))
    return out


FOCUS = ['_loadBlFiles']
