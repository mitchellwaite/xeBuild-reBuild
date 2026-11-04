"""keysdaeone.py W H B L E [pins]: print the daeEncrypt diff for one keysdaegrid combination,
with branch targets blanked so only real instruction differences show."""
import difflib, re, sys
import keyslib as K, keysdaegrid as G
from keysfn import replace_fn
a = sys.argv[1:]
pins = 'pins' in a
s = replace_fn(K.base(), 'daeEncrypt', G.text(a[0], a[1], a[2], a[3], pins, a[4]))
open(K.OUT + '/daeone.c', 'w', newline='\n').write(s)
o = K.compile(s, tag='daeone')
print(K.same(o), K.fndiff(o))


def norm(L):
    return [re.sub(r'\.-?[0-9a-f]+$', '.L', x) for x in L if 'DISP32' not in x and 'dir32' not in x]


for ln in difflib.unified_diff(norm(K.dis(K.REF)['_daeEncrypt']), norm(K.dis(o)['_daeEncrypt']), lineterm='', n=1):
    print(ln)
