"""keyskvone.py s f q h z v a: print the kvPrepare diff for one keyskvgrid combination."""
import difflib, sys
import keyslib as K, keyskvgrid as G
from keysfn import replace_fn
o = K.compile(replace_fn(K.base(), 'kvPrepare', G.text(*sys.argv[1:8])), tag='kvone')
print(K.same(o), K.fndiff(o))
for ln in difflib.unified_diff(K.dis(K.REF)['_kvPrepare'], K.dis(o)['_kvPrepare'], lineterm='', n=int(sys.argv[8]) if len(sys.argv)>8 else 1):
    print(ln)
