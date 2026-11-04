"""keyssubset.py [fn..]: per-function all-subsets search of src/keys.c's hints.

Each site is a literal (old, new) replacement.  Prints every subset that keeps the
whole object byte-identical, and the closest misses (by the function's own diff).
Param 'p:<n>' axes: python keyssubset.py kv --param 40,50,60,70
"""
import itertools, sys
from multiprocessing.pool import ThreadPool
import keyslib as K

SITES = {
    'fc': [
        ('pure', 'uint32_t getBeU32(const uint8_t *p) __attribute__((pure));\n', ''),
        ('off', '__builtin_expect(off >= 0x4000, 0)', 'off >= 0x4000'),
    ],
    'kv': [
        ('size', '__builtin_expect(kv->size != 0x4000, 1)', 'kv->size != 0x4000'),
        ('z16', '__builtin_expect(!checkZeros(buf, 16), 0)', '!checkZeros(buf, 16)'),
        ('z88', '__builtin_expect(checkZeros(buf + 56, 88), 0)', 'checkZeros(buf + 56, 88)'),
        ('alt', '__builtin_expect(!alt, 0)', '!alt'),
        ('failed', 'failed: __attribute__((hot));\n', '\n'),
        ('hashOk', 'hashOk: __attribute__((hot));\n', '\n'),
        ('zerosOk', 'zerosOk: __attribute__((hot));\n', '\n'),
    ],
    'dae': [
        ('size', '__builtin_expect(size, 1)', 'size'),
        ('D', "__builtin_expect(buf[off] == 'D', 1)", "buf[off] == 'D'"),
        ('A', "__builtin_expect(buf[off + 1] == 'A', 0)", "buf[off + 1] == 'A'"),
        ('E', "__builtin_expect(buf[off + 2] == 'E', 0)", "buf[off + 2] == 'E'"),
        ('P', "__builtin_expect(buf[off + 3] == 'P', 0)", "buf[off + 3] == 'P'"),
        ('ok', 'ok: __attribute__((cold));\n', '\n'),
        ('pin1', '__asm__("" : "+b"(off));\n', '\n'),
        ('pin2', '__asm__("" :: "d"(off));\n', '\n'),
    ],
}
FN = {'fc': '_fcrtEncrypt', 'kv': '_kvPrepare', 'dae': '_daeEncrypt'}


def run(which, base, minsize=1, maxsize=None):
    sites = SITES[which]
    subsets = []
    for n in range(minsize, (maxsize or len(sites)) + 1):
        subsets += list(itertools.combinations(sites, n))

    def one(a):
        i, sub = a
        s = base
        for name, old, new in sub:
            assert old in s, old
            s = s.replace(old, new)
        o = K.compile(s, tag='ss_%s_%d' % (which, i))
        d = K.fndiff(o) if o else {'fail': 999}
        return [x[0] for x in sub], K.same(o), d
    with ThreadPool(4) as p:
        res = p.map(one, list(enumerate(subsets)))
    matches = [r for r in res if r[1]]
    print(which, 'subsets', len(res), 'matches', len(matches))
    for r in sorted(matches, key=lambda r: -len(r[0])):
        print('  MATCH', r[0])
    near = sorted((r for r in res if not r[1]), key=lambda r: sum(r[2].values()))[:12]
    for r in near:
        print('  near', sum(r[2].values()), r[0], r[2])
    return res


if __name__ == '__main__':
    base = K.base()
    for w in sys.argv[1:] or ['fc', 'kv', 'dae']:
        run(w, base)
