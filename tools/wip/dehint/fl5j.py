"""fl5j.py <width> <depth> <start label>..: beam search over fl5h states (fl5f axes; fl5c axes; extras | tests), at most 3 of the 4 tests.
Different objects with the same score are kept apart by a hash, so transparent moves don't fill the beam.  Logs to a5/j.txt."""
import hashlib, sys, os, threading
from concurrent.futures import ThreadPoolExecutor
import fllib as L, fl5lib as F, fl5f as X, fl5c as C, fl5h as H

TN = ['raw', 'off3', 'off4', 'x']
_loc = threading.local()
_cnt = [0]
_lock = threading.Lock()
LOG = os.path.join(F.A5, 'j.txt')


def ev(lb):
    if not hasattr(_loc, 'id'):
        with _lock:
            _cnt[0] += 1
            _loc.id = _cnt[0]
    try:
        s = H.gen(*H.parse(lb))
    except (ValueError, AttributeError, AssertionError):
        return None
    o = L.compile(s, None, 'a5j_%d' % _loc.id)
    if o is None:
        return None
    sc = L.score(o)
    n = F.nscore(o, sc)
    d = hashlib.md5(L.sections(o)['.text']).hexdigest()
    return n, d, lb


def neigh(lb):
    fc, cc, ex, t = H.parse(lb)
    out = []
    for a in X.AX:
        for v in X.AX[a]:
            f2 = dict(fc)
            if f2.get(a) == v:
                del f2[a]
            else:
                f2[a] = v
            out.append(H.lab(f2, cc, ex, t))
    for a in C.ORDER:
        for v in C.AX[a]:
            c2 = dict(cc)
            if c2.get(a) == v:
                del c2[a]
            else:
                c2[a] = v
            out.append(H.lab(fc, c2, ex, t))
    for e in H.EXTRA:
        e2 = [x for x in ex if x != e] if e in ex else ex + [e]
        out.append(H.lab(fc, cc, e2, t))
    for x in TN:
        t2 = tuple(y for y in TN if (y in t) != (y == x))
        if len(t2) < 4:
            out.append(H.lab(fc, cc, ex, t2))
    return out


if __name__ == '__main__':
    W, D = int(sys.argv[1]), int(sys.argv[2])
    seen = {}
    frontier = sys.argv[3:]
    done = set()
    with ThreadPoolExecutor(4) as ex:
        for lb, r in zip(frontier, ex.map(ev, frontier)):
            seen[lb] = r
        for depth in range(D):
            todo = []
            for lb in frontier:
                if lb in done:
                    continue
                done.add(lb)
                todo += [n for n in neigh(lb) if n not in seen]
            todo = list(dict.fromkeys(todo))
            print('depth', depth, 'evaluating', len(todo), flush=True)
            for lb, r in zip(todo, ex.map(ev, todo)):
                seen[lb] = r
            byhash = {}
            for lb, r in seen.items():
                if r is None:
                    continue
                k = r[1]
                # fewer tests and axes first among equals
                rank = (r[0], lb.count(',') + lb.count('=') + lb.count('+'))
                if k not in byhash or rank < byhash[k][0]:
                    byhash[k] = (rank, lb)
            best = sorted(byhash.values())[:W]
            frontier = [b[1] for b in best]
            with open(LOG, 'a', newline='\n') as f:
                f.write('depth %d\n' % depth)
                for b in best:
                    f.write('%s\t%s\n' % (b[0][0], b[1]))
            print([(b[0][0], b[1]) for b in best[:8]], flush=True)
            ms = [lb for lb, r in seen.items() if r and r[0] == 0]
            if ms:
                print('MATCH', ms[:20], flush=True)
                break
