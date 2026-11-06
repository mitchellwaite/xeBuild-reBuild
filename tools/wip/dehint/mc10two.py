"""mode_client attempt 10: a near miss + one named AT edit, then every count-neutral repair.

python tools/wip/dehint/mc10two.py BASE.c 'add hdd5>8.s'|none [-r at,lists,reloc,less,perm,retarget] [-j 2] [-o DIR]"""
import os, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1lib, mc7j2l, mc9rep, mc10edits

GENS = dict(mc9rep.GENS)
GENS['at'] = lambda t: [v for _, v in mc10edits.variants(t)]


def main():
    a = sys.argv[1:]
    t = mc1lib.read_src(a[0])
    key = a[1]
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 2
    odir = a[a.index('-o') + 1] if '-o' in a else None
    reps = (a[a.index('-r') + 1] if '-r' in a else 'at,less,perm,lists,retarget,reloc').split(',')
    if key != 'none':
        t = mc7j2l.apply(t, dict(mc10edits.edits_at(t))[key])
    print(a[0], key, mc1lib.fmt(mc1lib.score_text(t, []))[:40], flush=True)
    for r in reps:
        cands = GENS[r](t)
        with ThreadPoolExecutor(jobs) as ex:
            ss = list(ex.map(lambda x: mc1lib.score_text(x, []), cands))
        res = sorted((0 if s.get('identical') else s.get('total', 99999), n) for n, s in enumerate(ss))
        print(r, len(cands), 'best', [d for d, n in res[:8]], flush=True)
        if res and res[0][0] == 0:
            if odir:
                os.makedirs(odir, exist_ok=True)
                open(os.path.join(odir, 'h_%s.c' % r), 'w', newline='\n').write(cands[res[0][1]])
            print('HIT', r, flush=True)
            break


if __name__ == '__main__':
    main()
