"""mode_client attempt 7: the dead blocks dz / dv (`if (0) { L: __builtin_unreachable(); }`)
removed and their edges pointed at another label: the other dead block, or a natural block
that ends in a noreturn call (u2, r3x, r5x) or returns.

python tools/wip/dehint/mc7dead.py [-base FILE]"""
import os, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib

DZ = 'if (0) { dz: __builtin_unreachable(); }'
DV = 'if (0) { dv: __builtin_unreachable(); }'
TG_DZ = ['dv', 'u2', 'r3x', 'r5x', 'fail', 'dtg', 'ndl', 'efail_none']
TG_DV = ['dz', 'u2', 'r3x', 'r5x', 'fail', 'dtg', 'ndl']


def variants(t):
    out = {}
    for g in TG_DZ:
        if g == 'efail_none':
            continue
        s = t.replace(DZ, '').replace('JMP(dz);', 'JMP(%s);' % g)
        out['dz->' + g] = s
        # also as a label of the -e arm's statement removed (edge dropped) + other block
    for g in TG_DV:
        s = t.replace(DV, '').replace('__asm__ goto ("" :::: dv, ', '__asm__ goto ("" :::: %s, ' % g)
        out['dv->' + g] = s
    # both into one block
    s = t.replace(DZ, '').replace('JMP(dz);', 'JMP(dv);')
    out['dz->dv'] = s
    s = t.replace(DV, '').replace('__asm__ goto ("" :::: dv, ', '__asm__ goto ("" :::: dz, ')
    out['dv->dz'] = s
    # the dead block written once, both labels on it
    s = t.replace(DZ, '').replace(DV, 'if (0) { dv: dz: __builtin_unreachable(); }')
    out['dvdz_one'] = s
    return out


def main():
    a = sys.argv[1:]
    t = mc1lib.read_src(a[a.index('-base') + 1] if '-base' in a else mc1.BASE)
    vs = variants(t)
    with ThreadPoolExecutor(4) as ex:
        for k, s in zip(vs, ex.map(mc1lib.score_text, vs.values())):
            print(k, mc1.count(vs[k])['total'], mc1lib.fmt(s)[:120], flush=True)


if __name__ == '__main__':
    main()
