"""flpe.py: flash='else' (closed before [security]) over the other axes."""
import itertools
import fllib as L, flpi as P

V = {}
for k in itertools.product(['else'], ['cur', 'nest', 'early', 'after'], ['goto', 'nest', 'inline'], ['asm', 'plain', 'nest'], ['else']):
    for dn, d in dict(a=('off1', 'off2'), b=(), c=P.ALLDEAD).items():
        V['_'.join(k) + '_' + dn] = P.gen(*k, dead=d)
L.sweep(V, prefix='pe', show=30)
