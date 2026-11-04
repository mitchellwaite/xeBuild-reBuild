"""fl5a.py [n] [seed]: section helpers in combination: each of bl raw flash sec is none, whole, loop or entry, with forms; plus cbb.
No dead tests in parseIni.  Singles exhaustively, then a random sample of combinations."""
import itertools, random, sys
import fl5lib as F

SECS = ['bl', 'raw', 'flash', 'sec']
FORMS = ['', 'f', 't', 'ft', 'u', 'fu', '1', '1f', '1t', 'b', 'bf', 'bt', '1b', '1bf']


def lab(h):
    return ','.join('%s:%s' % kv for kv in sorted(h.items()))


V = {}


def add(h, t=()):
    l = lab(h) + '|' + '+'.join(t)
    if l not in V:
        try:
            V[l] = F.gen(t, True, h)
        except Exception as e:
            sys.stderr.write('%s: %r\n' % (l, e))


for sec in SECS:
    for kind in ('', 'L', 'B'):
        for form in FORMS:
            add({sec + kind: form})
add({'cbb': ''})
n = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
r = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
while len(V) < n:
    h = {}
    k = r.choice((2, 2, 3, 4))
    for sec in r.sample(SECS, k):
        h[sec + r.choice(('', 'L', 'B'))] = r.choice(FORMS)
    if r.random() < .2:
        h['cbb'] = ''
    add(h)
print(len(V))
F.run(V, 'a', show=25)
