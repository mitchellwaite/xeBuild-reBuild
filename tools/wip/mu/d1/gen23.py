"""gen23.py: no XB_PATCHES: an array-of-names struct laid over xb.files by a cast, so xb.patches[n] stays an ARRAY_REF."""
import itertools
import os

import sw

HERE = os.path.dirname(os.path.abspath(__file__))
M = open(os.path.join(HERE, 'match.c'), newline='').read()
DEF = '#define XB_PATCHES\t\t/* xb.patches (xebuild.h) */\n'
OV = 'struct addonNames { char name[16][sizeof(struct fileent)]; };\n'
INC = '#include "smc.h"\n'
assert INC in M
NOP = M.replace(DEF, '').replace(INC, INC + OV)
SP = {
    'a': lambda k: '((struct addonNames *)&xb.files[XB_ADDONS])->name[%s]' % k,
    'b': lambda k: '((struct addonNames *)(xb.files + XB_ADDONS))->name[%s]' % k,
    'c': lambda k: '(*(struct addonNames *)&xb.files[XB_ADDONS]).name[%s]' % k,
    'd': lambda k: '(*(char (*)[16][sizeof(struct fileent)])&xb.files[XB_ADDONS])[%s]' % k,
    'e': lambda k: '(*(char (*)[35][sizeof(struct fileent)])xb.files)[XB_ADDONS + %s]' % k,
    'f': lambda k: '(*(char (*)[35][sizeof(struct fileent)])xb.files)[%s + XB_ADDONS]' % k,
}
vs = []
for (a, fa), (b, fb), (c, fc) in itertools.product(SP.items(), SP.items(), SP.items()):
    i0 = NOP.index('void parseAddonIdx')
    i1 = NOP.index('void getAddons')
    fn = NOP[i0:i1].replace('xb.patches[i]', fa('i')).replace('xb.patches[xb.numPatches]', fb('xb.numPatches'))
    t = NOP[:i0] + fn + NOP[i1:].replace('xb.patches[xb.numPatches]', fc('xb.numPatches'))
    vs.append(('%s%s%s' % (a, b, c), t))
sw.run(vs, '-O3', save='gen23', top=12)
