# attempt 3: on the near file IWB (a1, c3 gone, no asm in imgAdd's dead tests; one compare off): every form of the dead tests left in imgAdd.
import os
BASE = os.environ.get('IWB', 'build/iw/a3/v2.c')
A2 = '		if (x > first + 0x4000)\n			blocks += 2;\n'
C4 = '		if ((len & 0x3fff) > 0x3fff)\n			blocks++;\n'
A5 = '			if (x > first + 0x4000)\n				blocks += 2;\n'
A6 = '		if (x + 0x4000 < first)\n			blocks++;\n'
def v(old, ind, conds, bodies):
    r = []
    for ci, c in enumerate(conds):
        for bi, b in enumerate(bodies):
            r.append(('%s%d%d' % (old[1], ci, bi), [(old[0], ind + 'if (' + c + ')\n' + ind + '	' + b + ';\n')]))
    return r
C_HI = ['x > first + 0x4000', 'first + 0x4000 < x']
C_LO = ['x + 0x4000 < first', 'first > x + 0x4000']
AXES = [
 v((A2, 'a'), '		', C_HI + C_LO, ['blocks += 2', 'blocks++']),
 v((C4, 'c'), '		', ['(len & 0x3fff) > 0x3fff'], ['blocks++', 'blocks += 2', 'start++']),
 v((A5, 'f'), '			', C_HI + C_LO, ['blocks++', 'blocks += 2', 'start++']),
 v((A6, 's'), '		', C_LO + C_HI, ['blocks++', 'blocks += 2', 'start++']),
]
