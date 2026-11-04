"""fl4j.py N seed: random combinations of fl4d's natural helpers at fl4f's base."""
import random, sys
import fl4lib as F, fl4d as D, fl4f as B
N, seed = int(sys.argv[1]), int(sys.argv[2])
rng = random.Random(seed)
V = {}
tries = 0
ORD = [a for a in D.ORDER if a != 'w']
while len(V) < N and tries < N * 20:
    tries += 1
    c = {}
    for a in ORD:
        if rng.random() < 0.35:
            c[a] = rng.choice(list(D.AX[a]))
    l = D.lab(c)
    if l not in V:
        V[l] = D.gen(c, B.BASE)
print(len(V))
F.run(V, 'j', show=25)
