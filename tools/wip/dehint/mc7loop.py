"""mode_client attempt 7: greedy loop over mc7comp's removals.  For the current state, each
removal (mc7comp.REMOVALS, in order) is tried alone and with every single free list edit
(mc7comp.edits); the first IDENTICAL one is taken, its state written, and the loop starts
over.  Ends when a full pass finds nothing.

python tools/wip/dehint/mc7loop.py BASE.c OUTDIR [-j 4] [-names a,b,...]
States: OUTDIR/state_<n>_<count>.c; log on stdout."""
import os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib, mc7comp, mc7j2l


def try_removal(cur, name, jobs):
    t = cur
    for rx, rep in mc7comp.REMOVALS[name]:
        t, n = re.subn(rx, rep, t, count=1)
        if n != 1:
            return None, 'n/a'
    todo = [('alone', t)] + [(k, mc7j2l.apply(t, ed)) for k, ed in mc7comp.edits(t)]
    best = None
    with ThreadPoolExecutor(jobs) as ex:
        # in chunks, so a hit stops the search early
        for i in range(0, len(todo), 64):
            chunk = todo[i:i + 64]
            res = list(ex.map(lambda it: (it[0], mc1lib.score_text(it[1]), it[1]), chunk))
            for k, s, txt in res:
                if 'compile' in s:
                    continue
                if s['identical']:
                    return txt, k
                if best is None or s['total'] < best[0]:
                    best = (s['total'], k)
    return None, best


def main():
    a = sys.argv[1:]
    cur = mc1lib.read_src(a[0])
    odir = a[1]
    os.makedirs(odir, exist_ok=True)
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    names = a[a.index('-names') + 1].split(',') if '-names' in a else [n for n in mc7comp.REMOVALS if n != 'none']
    step = 0
    print('start', mc1.count(cur)['total'], flush=True)
    found = True
    while found:
        found = False
        for nm in names:
            txt, info = try_removal(cur, nm, jobs)
            if txt:
                step += 1
                c = mc1.count(txt)['total']
                p = os.path.join(odir, 'state_%d_%d.c' % (step, c))
                open(p, 'w', newline='\n').write(txt)
                print('TAKE', nm, info, 'count', c, p, flush=True)
                cur = txt
                found = True
                break
            print('  no', nm, info, flush=True)
    print('final', mc1.count(cur)['total'], flush=True)


if __name__ == '__main__':
    main()
