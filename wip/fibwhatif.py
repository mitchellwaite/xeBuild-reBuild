"""What-if replay of bb-reorder's STC heap (wip/fibsim.py), event-driven.

python wip/fibwhatif.py <mode_update bbro dump>
Rounds 1-3 replay exactly; in round 4 each extraction replays that trace's
own events (its visits and inserts), so a changed key moves the trace's
insertions with it (fibsim's non-strict run keeps them at the dump's time,
which finds false solutions). sim(groups(ev), {bb: key}) gives the order;
the main tries every 1-3 key change of +-1/2 for the original's
devkit/WARNING/no-HDD order (that subsequence only: compare the whole
round-4 order too, minus connected traces; none of these keeps it).
"""
import sys, itertools, collections
sys.path.insert(0, 'wip')
import fibsim

def groups(ev):
    """rounds: list of (pre_events, {bb: events after 'get bb'}) ; round 1 pre includes entry."""
    rounds = []
    cur = None; key = None
    for e in ev:
        if e[0] == 'round':
            cur = {'pre': [], 'g': {}, 'order': []}; rounds.append(cur); key = None
        elif e[0] == 'get':
            key = e[1]; cur['g'][key] = []; cur['order'].append(key)
        else:
            (cur['pre'] if key is None else cur['g'][key]).append(e)
    return rounds

def sim(rounds, keys, rnd_from=4):
    heap = fibsim.Heap(); new = None
    loc = {2: (heap, heap.insert(0, 2))}
    order = []
    def apply(e):
        nonlocal heap, new
        if e[0] == 'visit':
            if e[1] in loc:
                h, n = loc.pop(e[1]); h.delete_node(n)
        elif e[0] == 'ins':
            k = keys.get(e[2], e[3]) if -100 < e[3] <= 0 else e[3]
            h = heap if e[1] == 'this' else new
            if e[2] in loc:  # already queued (possible in what-if): keep
                return
            loc[e[2]] = (h, h.insert(k, e[2]))
        elif e[0] == 'push':
            k = keys.get(e[1], e[2])
            loc[e[1]] = (new, new.insert(k, e[1]))
        elif e[0] == 'chg':
            if e[1] in loc:
                h, n = loc[e[1]]; loc[e[1]] = (h, h.replace_key(n, e[2]))
    for ri, r in enumerate(rounds, 1):
        if new is not None:
            heap = new
        new = fibsim.Heap()
        for e in r['pre']: apply(e)
        if ri < rnd_from:
            # replay exactly
            for b in r['order']:
                z = heap.extract_min(); loc.pop(z.data, None)
                order.append(z.data)
                for e in r['g'][b]: apply(e)
        else:
            while heap.min is not None:
                z = heap.extract_min(); b = z.data; loc.pop(b, None)
                order.append(b)
                for e in r['g'].get(b, []): apply(e)
    return order

if __name__ == '__main__':
    ev = fibsim.parse(sys.argv[1])
    R = groups(ev)
    o = sim(R, {})
    real = [e[1] for e in ev if e[0] == 'get']
    print('sim==real', o == real)
    want = [46, 90, 122, 118, 94]
    keyed = collections.OrderedDict()
    for r in R[2:]:
        for e in r['pre'] + [x for g in r['g'].values() for x in g]:
            if e[0] == 'ins' and -100 < e[3] < 0: keyed[e[2]] = e[3]
            if e[0] == 'push' and -100 < e[2] <= 0: keyed[e[1]] = e[2]
    cand = [b for b in keyed if keyed[b] >= -9]
    print(dict((b, keyed[b]) for b in cand))
    n = 0
    for rr in (1, 2, 3):
        for nodes in itertools.combinations(cand, rr):
            for ds in itertools.product([-2, -1, 1, 2], repeat=rr):
                k = {b: min(0, keyed[b] + d) for b, d in zip(nodes, ds)}
                o = sim(R, k)
                if [b for b in o if b in want] == want:
                    n += 1
                    if n < 60: print('OK', k)
    print('total', n)
