"""Attempt 11, family 4d: gen_nr105 with got instead of size in the helper's store, and `size = got` forms: another got ref at the store's freq."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_nr105 as g

STORES = {'got': '*len = got;', 'sizegot': 'size = got;\n\t\t*len = size;', 'gotnl': '*len = (int)got;'}


def variants():
    for an, tl, ck in itertools.product(g.ARMS, g.TAILS, ('ifnot2', 'ret')):
        s0 = g.mk(an, 'not', 'afternl', tl, ck)
        for sn, st in STORES.items():
            yield '|'.join((an, tl, ck, sn)), s0.replace('*len = size;', st)
