"""fl8b.py: combinations of parseIni's local types (int/long in the same sign keeps behaviour), random sample.
  python fl8b.py N [drops;drops..]
Coalescing cares about type identity, so pairs may move where singles are transparent."""
import random, sys
import fl8lib as T

SIGNED = ['size', 'off', 'end', 'pos', 'len', 'nul', 'comma', 'n', 'i', 'nbl']
N = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
DROPS = (sys.argv[2] if len(sys.argv) > 2 else 'T1,T3;T1,T2,T3;T3;T1').split(';')
random.seed(int(sys.argv[3]) if len(sys.argv) > 3 else 8)
V = {}
while len(V) < N:
    d = random.choice(DROPS)
    a = []
    p = random.choice([.2, .4, .6, .8])
    for v in SIGNED:
        if random.random() < p:
            a.append('t.%s=long' % v)
    nc = random.choice(['uint32_t', 'uint32_t', 'unsigned', 'int', 'long'])
    if nc != 'uint32_t':
        a.append('t.noCrc=' + nc)
    lb = d + '|' + ','.join(a)
    V[lb] = T.state(lb)
rs = T.run(V, 'b', 15)
T.floors(rs)
