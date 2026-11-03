"""gen22.py: no XB_PATCHES.  The reference keeps `base + index` as one address so PRE only moves index*0x42c: try ARRAY_REF spellings with the index inside a real array."""
import itertools
import os

import sw

HERE = os.path.dirname(os.path.abspath(__file__))
M = open(os.path.join(HERE, 'match.c'), newline='').read()
DEF = '#define XB_PATCHES\t\t/* xb.patches (xebuild.h) */\n'
NOP = M.replace(DEF, '')
S = 'sizeof(struct fileent)'
SP = {
    'ptr': lambda k: '(xb.files + %s + XB_ADDONS)->name' % k,
    'pname': lambda k: '(&xb.files[XB_ADDONS] + %s)->name' % k,
    'idx': lambda k: '&xb.files[XB_ADDONS].name[%s * %s]' % (k, S),
    'idx2': lambda k: '&xb.files[XB_ADDONS].name[%s * 0x42c]' % k,
    'idx3': lambda k: 'xb.files[XB_ADDONS].name + %s * %s' % (k, S),
    'idx4': lambda k: '&xb.files[0].name[(%s + XB_ADDONS) * %s]' % (k, S),
    'idx5': lambda k: '&((char *)xb.files)[(%s + XB_ADDONS) * %s]' % (k, S),
    'idx6': lambda k: '&((char *)&xb.files[XB_ADDONS])[%s * %s]' % (k, S),
    'name': lambda k: 'xb.files[XB_ADDONS + %s].name' % k,
}
i0 = NOP.index('void parseAddonIdx')
i1 = NOP.index('void getAddons')
vs = []
for (a, fa), (b, fb), (c, fc) in itertools.product(SP.items(), SP.items(), SP.items()):
    fn = NOP[i0:i1].replace('xb.patches[i]', fa('i')).replace('xb.patches[xb.numPatches]', fb('xb.numPatches'))
    t = NOP[:i0] + fn + NOP[i1:].replace('xb.patches[xb.numPatches]', fc('xb.numPatches'))
    vs.append(('%s__%s__%s' % (a, b, c), t))
print(len(vs))
sw.run(vs, '-O3', save='gen22', top=20)
