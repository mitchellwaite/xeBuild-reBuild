"""mode_client attempt 8: greedy loop over mc8comp's removals (mc7loop with cebi labels/lists
in the edit set).  Each removal alone and with every single free list edit; with -two N,
removals whose best single miss is <= N lines also get pairs of edits from the best 60.
The first IDENTICAL one is taken (count must drop) and the loop starts over.

python tools/wip/dehint/mc8loop.py BASE.c OUTDIR [-j 4] [-names a,b] [-two N]"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib, mc8comp


def main():
    a = sys.argv[1:]
    cur = mc1lib.read_src(a[0])
    odir = a[1]
    os.makedirs(odir, exist_ok=True)
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    two = int(a[a.index('-two') + 1]) if '-two' in a else 0
    names = a[a.index('-names') + 1].split(',') if '-names' in a else [n for n in mc8comp.REMOVALS if n != 'none']
    c0 = mc1.count(cur)['total']
    print('start', c0, flush=True)
    step = 0
    found = True
    while found:
        found = False
        for nm in names:
            t = mc8comp.remove(cur, nm)
            if t is None:
                print('  n/a', nm, flush=True)
                continue
            if mc1.count(t)['total'] >= mc1.count(cur)['total']:
                print('  not counted', nm, flush=True)
                continue
            hits, res = mc8comp.run(t, jobs)
            if not hits and two and res and res[0][0] <= two:
                hits, res = mc8comp.run(t, jobs, two=60)
            if hits:
                k, txt = hits[0]
                step += 1
                c = mc1.count(txt)['total']
                p = os.path.join(odir, 'state_%d_%d.c' % (step, c))
                open(p, 'w', newline='\n').write(txt)
                print('TAKE', nm, k, 'count', c, p, flush=True)
                cur = txt
                found = True
                break
            print('  no', nm, res[:3], flush=True)
    print('final', mc1.count(cur)['total'], flush=True)


if __name__ == '__main__':
    main()
