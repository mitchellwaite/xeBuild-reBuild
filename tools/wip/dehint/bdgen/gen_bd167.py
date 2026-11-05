"""The tail of the case 5 arm (xb.type test, *pr, setFlashBuild) without the t5le label: forms that may predict xb.type <= 5 as strongly."""
import importlib.util, itertools, os
d = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('g161', os.path.join(d, 'gen_bd161.py'))
g1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g1)
g = g1.g
SET = 'setFlashBuild(getBeU16(xb.files[i].data + 2));\n'
X = '__builtin_expect(*pr != 0, 0)'
T = {
    't1': 'if (xb.type > BUILD_DEVGL16) {\nif (type == 14)\n' + SET + 'break;\n}\nif (PR)\ngoto fail;\n',
    't2': 'if (xb.type > BUILD_DEVGL16) {\nif (type == 14)\n' + SET + '} else if (PR)\ngoto fail;\n',
    't3': 'if (xb.type <= BUILD_DEVGL16) {\nif (PR)\ngoto fail;\n} else if (type == 14)\n' + SET,
    't4': 'if (xb.type > BUILD_DEVGL16 && type == 14)\n' + SET + 'else if (xb.type <= BUILD_DEVGL16 && PR)\ngoto fail;\n',
    't5': 'if (xb.type > BUILD_DEVGL16 && type == 14)\n' + SET + 'if (xb.type <= BUILD_DEVGL16 && PR)\ngoto fail;\n',
    't6': 'if (xb.type <= BUILD_DEVGL16 && PR)\ngoto fail;\nif (xb.type > BUILD_DEVGL16 && type == 14)\n' + SET,
    't7': 'if (PR && xb.type <= BUILD_DEVGL16)\ngoto fail;\nif (xb.type > BUILD_DEVGL16 && type == 14)\n' + SET,
    't8': 'if (PR && xb.type <= BUILD_DEVGL16)\ngoto fail;\nif (xb.type <= BUILD_DEVGL16)\nbreak;\nif (type == 14)\n' + SET,
    't9': 'if (xb.type <= BUILD_DEVGL16) {\nif (PR)\ngoto fail;\nbreak;\n}\nif (type != 14)\nbreak;\n' + SET,
    't10': 'if (xb.type > BUILD_DEVGL16) {\nif (type != 14)\nbreak;\n' + SET + 'break;\n}\nif (PR)\ngoto fail;\n',
    't11': 'if (xb.type <= BUILD_DEVGL16) {\nif (!(PR))\nbreak;\ngoto fail;\n}\nif (type == 14)\n' + SET,
    't12': 'if (xb.type <= BUILD_DEVGL16) {\nif (!(PR))\nbreak;\n} else {\nif (type == 14)\n' + SET + 'break;\n}\ngoto fail;\n',
}
PRS = {'x': X, 'p': '*pr'}
g.TAILS.update({k + pk: v.replace('PR', pv) for k, v in T.items() for pk, pv in PRS.items()})


def CASES(base):
    out = []
    for tl, t10, bad, cp, sg in itertools.product([k + p for k in T for p in PRS], (0, 1), (0, 1), (0, 1), ('dead', 'a')):
        def mk(b, tl=tl, t10=t10, bad=bad, cp=cp, sg=sg):
            t = g.with_arm(b, g.arm(sg, tl, 0, t10))
            if not cp:
                t = g.nocp(t)
            return g.nobad(t) if bad else t
        out.append(('%s %s t%d bad%d cp%d' % (sg, tl, t10, bad, cp), mk))
    return out


FOCUS = ['_loadBlFiles']
