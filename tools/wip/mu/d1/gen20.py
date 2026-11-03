"""gen20.py: on match.c, drop XB_PATCHES (the last listed trick): spell the patch names over xb.files instead of the union view; also updateNand with an int return."""
import os

import sw

HERE = os.path.dirname(os.path.abspath(__file__))
M = open(os.path.join(HERE, 'match.c'), newline='').read()
DEF = '#define XB_PATCHES\t\t/* xb.patches (xebuild.h) */\n'
assert DEF in M
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
}
vs = []
for n, f in SP.items():
    t = NOP.replace('xb.patches[i]', f('i')).replace('xb.patches[xb.numPatches]', f('xb.numPatches'))
    vs.append((n, t))
sw.run(vs, '-O3', save='gen20')
