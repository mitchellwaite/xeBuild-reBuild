# attempt 15, probe only (never a candidate): random dead arms, to see whether any count and shape of names freed at VRP1 leaves writeFsTable clean on a14.
# Arms: chain, nested if, two sequential dead tests, writes to z or blk. IWB= other base.
import os, random
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_a14.c')
SEED = int(os.environ.get('IWS', '1501'))
N = int(os.environ.get('IWN', '3000'))
r = random.Random(SEED)
POS = ['	buf = malloc(0x4000);\n', '	log_printf(1, "offset 0x%x len 0x4000', '	if (!xb.bigBlock)\n		goto small;\n']
CONDS = ['(off & 0x3fff) > 0x3fff', '(blk & 0xff) > 0xff', '(off >> 14) > 0x3ffff', '(off & 1) > 1', '(off >> 30) > 3', '(off & 0x1ffff) > 0x1ffff']
OPS = ['z += %d;', 'z ^= %d;', 'z <<= %d;', 'z -= %d;', 'z |= %d;', 'z >>= %d;', 'z *= %d;', 'z &= %d;', 'z += off + %d;', 'z ^= blk + %d;', 'y = z + %d;', 'z = y ^ %d;']
def chain(k):
    return ' '.join(r.choice(OPS) % r.choice([1, 3, 5, 7, 9, 11, 13]) for _ in range(k))
def arm():
    k = r.randint(1, 24)
    tgt = r.choice(['off', 'off', 'blk', 'i'])
    b = 'uint32_t z = %s, y = 1; %s' % (tgt, chain(k))
    if r.random() < .25:
        b += ' if (%s) { %s }' % (r.choice(CONDS), chain(r.randint(1, 8)))
    return '	if (%s) {\n		%s\n		%s = z + y;\n	}\n' % (r.choice(CONDS), b, tgt)
A = []
for n in range(N):
    ps = r.choice(POS)
    a = arm()
    if r.random() < .3:
        a += arm()
    A.append(('r%d_%d' % (SEED, n), [(ps, a + ps)]))
AXES = [A]
FLAGS = []
