"""g1.py: spell the addon name so xb.numPatches stays an int ARRAY_REF index over xb.files until laddress:
the 19 entries go in a constant part, not in the index.  See NOTES.md."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mu

R = open(os.path.join(HERE, 'ref.c'), newline='').read()
DEF = '#define XB_PATCHES\t\t/* xb.patches (xebuild.h) */\n'
assert DEF in R
NOP = R.replace(DEF, '')
Z = 'XB_ADDONS * sizeof(struct fileent)'
PLAIN = lambda k: '(xb.files + %s + XB_ADDONS)->name' % k
SP = {
    'idx': lambda k: '&xb.files[%s].name[%s]' % (k, Z),
    'plus': lambda k: '(xb.files[%s].name + %s)' % (k, Z),
    'cplus': lambda k: '((char *)&xb.files[%s] + %s)' % (k, Z),
    'splus': lambda k: '(&xb.files[%s] + XB_ADDONS)->name' % k,
    'sidx': lambda k: '(&xb.files[%s])[XB_ADDONS].name' % k,
    'cidx': lambda k: '&((char *)&xb.files[%s])[%s]' % (k, Z),
    'iplus': lambda k: 'xb.files[XB_ADDONS + %s].name' % k,
}
for n, f in SP.items():
    # parseAddonIdx's two sites: the variant; mode_update's: the -a sites as they were
    i0 = NOP.index('void parseAddonIdx')
    i1 = NOP.index('void getAddons')
    fn = NOP[i0:i1].replace('xb.patches[i]', f('i')).replace('xb.patches[xb.numPatches]', f('xb.numPatches'))
    t = NOP[:i0] + fn + NOP[i1:].replace('xb.patches[xb.numPatches]', PLAIN('xb.numPatches'))
    o, err = mu.compile_text(t, 'g1_' + n)
    if not o:
        print(n, 'ERR', err[:300])
        continue
    sc = mu.score(o)
    print(n, mu.total(sc), sc, 'ALLSEC' if all(mu.sec_cmp(o).values()) else '')
    with open(os.path.join(mu.OUT, 'g1_' + n, 'v.c'), 'w', newline='\n') as w:
        w.write(t)
