"""keysdae.py: daeEncrypt variants from text edits of the base draft (KEYSBASE).

Axes (each a list of (name, old, new) applied literally): off's initial value,
pins, expects, the cold label.  Prints the best combinations by the function's diff.
Run with a spec: python keysdae.py init,pin1,pin2,size,D,A,E,P,ok  (axes to toggle)."""
import itertools, sys
from multiprocessing.pool import ThreadPool
import keyslib as K

T = {
    'init': ('uint32_t off = 0;\n', 'uint32_t off;\n'),
    'pin1': ('__asm__("" : "+b"(off));\n', '\n'),
    'pin2': ('__asm__("" :: "d"(off));\n', '\n'),
    'size': ('__builtin_expect(size, 1)', 'size'),
    'D': ("__builtin_expect(buf[off] == 'D', 1)", "buf[off] == 'D'"),
    'A': ("__builtin_expect(buf[off + 1] == 'A', 0)", "buf[off + 1] == 'A'"),
    'E': ("__builtin_expect(buf[off + 2] == 'E', 0)", "buf[off + 2] == 'E'"),
    'P': ("__builtin_expect(buf[off + 3] == 'P', 0)", "buf[off + 3] == 'P'"),
    'ok': ('ok: __attribute__((cold));\n', '\n'),
}


def run(base, axes, fixed=(), top=25):
    for f in fixed:
        assert T[f][0] in base, f
        base = base.replace(*T[f])
    subs = []
    for n in range(len(axes) + 1):
        subs += itertools.combinations(axes, n)
    slots = [[] for _ in range(4)]
    for i, j in enumerate(subs):
        slots[i % 4].append((i % 4, j))

    def work(sl):
        out = []
        for slot, sub in sl:
            s = base
            for a in sub:
                s = s.replace(*T[a])
            o = K.compile(s, tag='dg%d' % slot)
            out.append((sub, K.same(o), K.fndiff(o) if o else {'fail': 9999}))
        return out
    with ThreadPool(4) as p:
        res = sum(p.map(work, slots), [])
    res.sort(key=lambda r: (sum(r[2].values()), -len(r[0])))
    for r in res[:top]:
        print('MATCH' if r[1] else '     ', sum(r[2].values()), r[0])
    return res


if __name__ == '__main__':
    axes = sys.argv[1].split(',')
    fixed = sys.argv[2].split(',') if len(sys.argv) > 2 else []
    run(K.base(), axes, fixed)
