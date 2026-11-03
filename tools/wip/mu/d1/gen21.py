"""gen21.py: no XB_PATCHES: separate spellings for the test and copy sites of parseAddonIdx (mode_update's own sites use `ptr`, which already match)."""
import itertools
import os

import sw

HERE = os.path.dirname(os.path.abspath(__file__))
M = open(os.path.join(HERE, 'match.c'), newline='').read()
DEF = '#define XB_PATCHES\t\t/* xb.patches (xebuild.h) */\n'
NOP = M.replace(DEF, '')
SP = {
    'name': lambda k: 'xb.files[XB_ADDONS + %s].name' % k,
    'name2': lambda k: 'xb.files[%s + XB_ADDONS].name' % k,
    'ptr': lambda k: '(xb.files + %s + XB_ADDONS)->name' % k,
    'ptr2': lambda k: '(xb.files + XB_ADDONS + %s)->name' % k,
    'cast': lambda k: '(char *)&xb.files[XB_ADDONS + %s]' % k,
    'cast2': lambda k: '(char *)(xb.files + XB_ADDONS + %s)' % k,
    'mac': lambda k: '((char (*)[sizeof(struct fileent)])(xb.files + XB_ADDONS))[%s]' % k,
    'mac2': lambda k: '((char (*)[sizeof(struct fileent)])&xb.files[XB_ADDONS])[%s]' % k,
    'mac3': lambda k: '((char (*)[sizeof(struct fileent)])xb.files)[XB_ADDONS + %s]' % k,
    'mac4': lambda k: '((char (*)[sizeof(struct fileent)])xb.files)[%s + XB_ADDONS]' % k,
    'addr': lambda k: '((char *)xb.files + (XB_ADDONS + %s) * sizeof(struct fileent))' % k,
    'addr2': lambda k: '((char *)(xb.files + XB_ADDONS) + %s * sizeof(struct fileent))' % k,
    'addr3': lambda k: '(%s * sizeof(struct fileent) + (char *)(xb.files + XB_ADDONS))' % k,
    'pname': lambda k: '(&xb.files[XB_ADDONS] + %s)->name' % k,
    'pn2': lambda k: '(&xb.files[XB_ADDONS])[%s].name' % k,
}
i0 = NOP.index('void parseAddonIdx')
i1 = NOP.index('void getAddons')
vs = []
for (a, fa), (b, fb) in itertools.product(SP.items(), SP.items()):
    fn = NOP[i0:i1].replace('xb.patches[i]', fa('i')).replace('xb.patches[xb.numPatches]', fb('xb.numPatches'))
    t = NOP[:i0] + fn + NOP[i1:].replace('xb.patches[xb.numPatches]', SP['ptr']('xb.numPatches'))
    vs.append(('%s__%s' % (a, b), t))
print(len(vs))
sw.run(vs, '-O3', save='gen21', top=20)
