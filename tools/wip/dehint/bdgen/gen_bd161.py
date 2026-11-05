"""gen_bd160's signature forms and the source's tail, without constant_p; hints as axes.  -k a label, then look at build/bd/gen_bd161_best.c."""
import importlib.util, itertools, os
d = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('g160', os.path.join(d, 'gen_bd160.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

TAILS = dict(g.TAILS)
TAILS['fail'] = 'if (xb.type <= BUILD_DEVGL16) {\nif (*pr)\ngoto fail;\nbreak;\n}\nif (type == 14)\nsetFlashBuild(getBeU16(xb.files[i].data + 2));\n'
TAILS['failx'] = 'if (xb.type <= BUILD_DEVGL16) {\nif (__builtin_expect(*pr != 0, 0))\ngoto fail;\nbreak;\n}\nif (type == 14)\nsetFlashBuild(getBeU16(xb.files[i].data + 2));\n'
TAILS['failh'] = 'if (xb.type <= BUILD_DEVGL16) {\nt5le: __attribute__((hot));\nif (*pr)\ngoto fail;\nbreak;\n}\nif (type == 14)\nsetFlashBuild(getBeU16(xb.files[i].data + 2));\n'
TAILS['src'] = 'if (xb.type <= BUILD_DEVGL16) {\nt5le: __attribute__((hot));\nif (__builtin_expect(*pr != 0, 0))\ngoto fail;\nbreak;\n}\nif (type == 14)\nsetFlashBuild(getBeU16(xb.files[i].data + 2));\n'
g.TAILS.update(TAILS)


def CASES(base):
    out = []
    for sg, tl, t10, bad, cp in itertools.product(g.SIGS, TAILS, (0, 1), (0, 1), (0, 1)):
        def mk(b, sg=sg, tl=tl, t10=t10, bad=bad, cp=cp):
            t = g.with_arm(b, g.arm(sg, tl, 0, t10))
            if not cp:
                t = g.nocp(t)
            return g.nobad(t) if bad else t
        out.append(('%s %s t%d bad%d cp%d' % (sg, tl, t10, bad, cp), mk))
    return out


FOCUS = ['_loadBlFiles']
