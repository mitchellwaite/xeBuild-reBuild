"""Attempt 5: op5's helper flow forms (one helper FN) x every single optricks removal.
python tools/wip/dehint/op5x.py FN [removal names..]  -> build/op/op5x_FN.txt (sorted)
A line is IDENTICAL-worthy only when the total trick count goes down."""
import os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib, optricks, op5


def main():
    a = sys.argv[1:]
    fn = a.pop(0)
    b0 = optricks.base()
    rems = a or [n for n in optricks.active(b0) if n != 'part']
    cur_n = op5.ntricks(fn, *op5.CUR[fn])
    fs = [f for f in op5.forms(fn) if 'return 1;' not in f[1:3] and (fn != 'N' or f[0] in (None, 'keep'))]
    jobs = []
    for r in rems:
        b, got = optricks.apply(b0, [r])
        if not got:
            continue
        for f in fs:
            if f == op5.CUR[fn]:
                continue
            n = op5.ntricks(fn, *f)
            # removal r inside the same helper is already covered by the forms
            if r.startswith(fn + '_') or (fn == 'ib' and r.startswith('ib_')):
                continue
            if n > cur_n:
                continue
            jobs.append(((r, f), n, op5.replace_fn(b, fn, op5.body(*f)), r))
    print(len(jobs), 'jobs', flush=True)
    out = os.path.join(optlib.BUILD, 'op5x_%s.txt' % fn)

    def one(j):
        return j[0], j[1], optlib.score_text(j[2], optricks.flags_for([j[3]]))
    with ThreadPoolExecutor(4) as p:
        res = list(p.map(one, jobs))
    res.sort(key=lambda x: x[2].get('total', 10 ** 9))
    with open(out, 'w', newline='\n') as f:
        for k, n, r in res:
            f.write('%-80s n=%d %s\n' % (repr(k), n, optlib.fmt(r)))
    for k, n, r in res[:30]:
        print('%-80s n=%d %s' % (repr(k), n, optlib.fmt(r)))


if __name__ == '__main__':
    main()
