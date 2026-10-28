"""Write a .gcda that reproduces gcc's guessed profile (for -fbranch-probabilities).

python re/gcda.py <x.gcno> <x.c.042t.profile_estimate> <out.gcda>
                   [fn:src>dst=prob ... | @file] [--only=fn,fn] [--src=file.c]
                   [--threshold=N]

The .gcno (and the dump, with -fdump-tree-profile_estimate-blocks-details)
come from one compile with the object's flags plus -fprofile-arcs
-ftest-coverage, with the same aux name as the profile build (both `-o -`).
gcno blocks are mapped onto the dump's (branch_prob splits blocks after
calls and compacts the numbers), two-way probabilities are recomputed
exactly from the dump's predictor lines (gcc 6's DS / first-match combine),
flows are solved from the entry, and counts scaled so that gcc's count-based
hot test agrees with the guessed one (cold iff freq < entry freq / 1000,
integer division). A static function's entry count is its call sites' (an
inlined called-once body keeps its own counts). An override `fn:src>dst=prob`
(dump bb numbers) sets one edge probability in % (the other edges of src keep
their ratios). --src names the C file when the gcno's (a #line name) isn't
one. --only writes counts for those functions only (the rest stay
guessed). build.sh builds mode_update with it (wip/mufdo.sh is the
experiment driver). --consistent writes exactly conserved integer counts
(needed when overrides make zero flows); --mult=fn:K scales fn's counts.
"""
import re, struct, sys

ON_TREE, FAKE = 1, 2
T_FUNCTION, T_BLOCKS, T_ARCS, T_LINES = 0x01000000, 0x01410000, 0x01430000, 0x01450000
T_COUNTER_ARCS, T_PROGRAM_SUMMARY = 0x01a10000, 0xa3000000
THRESHOLD = 1 << 14          # hot_bb_threshold, in counts (counts * 10000 must not overflow)


def read_gcno(path):
    d = open(path, 'rb').read()
    w = struct.unpack('<%dI' % (len(d) // 4), d)
    version, stamp = w[1], w[2]
    fns, i = [], 3
    while i < len(w):
        tag, n = w[i], w[i + 1]
        rec = w[i + 2:i + 2 + n]
        i += 2 + n
        if tag == T_FUNCTION:
            ln = rec[3]
            name = struct.pack('<%dI' % ln, *rec[4:4 + ln]).rstrip(b'\0').decode()
            ls = rec[4 + ln]
            src = struct.pack('<%dI' % ls, *rec[5 + ln:5 + ln + ls]).rstrip(b'\0').decode()
            fns.append({'ident': rec[0], 'lck': rec[1], 'cck': rec[2], 'name': name, 'src': src,
                        'arcs': []})
        elif tag == T_ARCS:
            src = rec[0]
            for k in range(1, len(rec), 2):
                fns[-1]['arcs'].append((src, rec[k], rec[k + 1]))
    return version, stamp, fns


# gcc 6 predict.def, in enum order; True = PRED_FLAG_FIRST_MATCH
PREDICTORS = [('combined', 0), ('DS theory', 0), ('first match', 0), ('no prediction', 0),
              ('unconditional jump', 1), ('loop iterations', 1), ('compare and swap', 1),
              ('__builtin_expect', 1), ('guessed loop iterations', 1), ('continue', 0),
              ('noreturn call', 1), ('cold function call', 1), ('loop branch', 1), ('loop exit', 1),
              ('pointer', 0), ('pointer (on trees)', 0), ('opcode values positive', 0),
              ('opcode values nonequal', 0), ('fp_opcode', 0),
              ('opcode values positive (on trees)', 0), ('opcode values nonequal (on trees)', 0),
              ('fp_opcode (on trees)', 0), ('call', 0), ('early return (on trees)', 0), ('goto', 0),
              ('const return', 0), ('negative return', 0), ('null return', 0),
              ('guess loop iv compare', 0), ('loop iv compare', 1), ('hot label', 0),
              ('cold label', 1)]
PRED_IDX = {n: i for i, (n, f) in enumerate(PREDICTORS)}
HIT = {'continue': 5000, 'loop branch': 8600, 'loop exit': 9100, 'pointer (on trees)': 8500,
       'opcode values positive (on trees)': 7300, 'opcode values nonequal (on trees)': 7200,
       'fp_opcode (on trees)': 9000, 'call': 7100, 'early return (on trees)': 6100, 'goto': 7000,
       'const return': 6700, 'negative return': 9600, 'null return': 9000, 'hot label': 8500,
       'noreturn call': 9996, 'cold function call': 9996, 'cold label': 9996,
       'guess loop iv compare': 9996, 'loop iv compare': 9996, 'unconditional jump': 10000}
# computed ones: loop iterations (10000 + n/2) / n, loop exit max(900 / exits, 200)
LOOPISH = {(10000 + n // 2) // n for n in range(1, 10001)} | {max(900 // k, 200) for k in range(1, 100)}
LOOPISH = sorted(LOOPISH | {10000 - p for p in LOOPISH})


def exact(name, v):
    """The probability (out of 10000) that gcc printed as v% with %.1f."""
    cands = [HIT[name], 10000 - HIT[name]] if name in HIT else []
    if name in ('loop exit', 'loop iterations', 'guessed loop iterations'):
        cands += LOOPISH
    ok = [c for c in cands if abs(c / 100 - v) <= 0.0501]
    # __builtin_expect: the param's value, printed exactly (1% steps)
    return min(ok, key=lambda c: abs(c / 100 - v)) if ok else round(v * 100)


def combine(preds):
    """gcc 6 combine_predictions_for_bb for two edges; preds = [(name, prob of edge 0)]."""
    best_p, best, comb = 5000, len(PREDICTORS), 5000
    for i, (name, p) in enumerate(preds):
        k = PRED_IDX[name]
        # shortcut: ignores gcc's veto when one predictor appears twice in opposite
        # directions (only matters if that predictor is first-match)
        if best > k:
            best_p, best = p, k
        d = comb * p + (10000 - comb) * (10000 - p)
        comb = 5000 if d == 0 else int(comb * p * 10000 / d + 0.5)
    if best < len(PREDICTORS) and PREDICTORS[best][1]:
        return best_p
    return comb


def read_dump(path):
    """{function: {bb: (freq, {dst: prob%})}} from the last listing of each function;
    two-way probabilities are recomputed exactly from the predictions. Also
    {function: {bb: [called names]}}."""
    out, fn, bb, calls = {}, None, None, {}
    preds, cur = {}, None
    for l in open(path):
        m = re.match(r';; Function (\S+)', l)
        if m:
            if fn in out:
                fix(out[fn], preds.get(fn, {}))
            fn = m.group(1)
            out[fn], calls[fn], bb = {}, {}, None
            preds.setdefault(fn, {})
            continue
        m = re.match(r'Predictions for bb (\d+)', l)
        if m:
            cur = preds[fn].setdefault(int(m.group(1)), [])
            del cur[:]
            continue
        m = re.match(r'  (.+) heuristics( \(ignored\))?: ([\d.]+)%', l)
        if m and cur is not None:
            if m.group(1) not in ('DS theory', 'first match', 'combined', 'no prediction'):
                cur.append((m.group(1), exact(m.group(1), float(m.group(3)))))
            continue
        cur = None
        m = re.match(r';;\s+basic block (\d+), loop depth \d+, count \d+, freq (\d+)', l)
        if m and fn:
            bb = int(m.group(1))
            out[fn][bb] = (int(m.group(2)), {})
            calls[fn][bb] = []
            continue
        if fn and bb is not None and not l.startswith(';;'):
            calls[fn].setdefault(bb, []).extend(re.findall(r'(?<![\w.])(\w+) \(', l))
        m = re.match(r';;\s+(?:succ:)?\s+(\w+) \[([\d.]+)%\]', l)
        if m and fn and bb is not None and ('succ:' in l or out[fn][bb][1]):
            dst = {'EXIT': 1}.get(m.group(1)) or int(m.group(1))
            out[fn][bb][1][dst] = float(m.group(2))
    if fn in out:
        fix(out[fn], preds.get(fn, {}))
    return out, calls


def fix(blocks, preds):
    """Replace the printed (0.1%) probabilities by gcc's exact ones."""
    for bb, (freq, succ) in blocks.items():
        ds = list(succ)
        if len(ds) == 2:
            p = combine(preds.get(bb, []))
            succ[ds[0]], succ[ds[1]] = p / 100, (10000 - p) / 100
        elif ds:
            for d in ds:
                succ[d] = (10000 + len(ds) // 2) // len(ds) / 100
            if len(ds) == 1:
                succ[ds[0]] = 100.0


def solve(arcs, probs, fakeov=None):
    """Flows (entry = 1) for the non-fake arcs; probs {(src, dst): p}.
    fakeov {gcno block: percent} also routes that share of a call block's
    flow through its fake arc to EXIT (gcc derives the fake arc's count from
    the block's others, so the block keeps its count and only its successors
    see less)."""
    succ = {}
    for s, d, f in arcs:
        if not f & FAKE or (fakeov and s in fakeov and d == 1):
            succ.setdefault(s, []).append(d)
    x = {0: 1.0}
    for _ in range(200000):
        nx = {0: 1.0}
        for s, ds in succ.items():
            tot = sum(probs[(s, d)] for d in ds) or 1
            for d in ds:
                nx[d] = nx.get(d, 0) + x.get(s, 0) * probs[(s, d)] / tot
        if all(abs(nx.get(k, 0) - x.get(k, 0)) < 1e-14 for k in set(nx) | set(x)):
            break
        x = nx
    flow = {}
    for s, ds in succ.items():
        tot = sum(probs[(s, d)] for d in ds) or 1
        for d in ds:
            flow[(s, d)] = x.get(s, 0) * probs[(s, d)] / tot
    return x, flow


def mapping(arcs, est):
    """gcno block -> dump block. branch_prob splits blocks after calls (the
    first part gets a fake edge to EXIT) and the gcno numbers are compacted,
    so walk both graphs from the entry, following those split chains."""
    succ, preds, fake = {}, {}, set()
    for s, d, f in arcs:
        if f & FAKE:
            fake.add(s)
        else:
            succ.setdefault(s, []).append(d)
            preds[d] = preds.get(d, 0) + 1
    m, todo = {0: 0, 1: 1}, [(2, 2)]
    while todo:
        g, t = todo.pop()
        while True:
            if g in m:
                assert m[g] == t, (g, m[g], t)
                break
            m[g] = t
            ds = succ.get(g, [])
            tds = list(est[t][1])
            if g in fake and len(ds) == 1 and preds[ds[0]] == 1 and ds[0] not in m and ds[0] != 1 \
                    and not (len(tds) == 1 and tds[0] == 1):
                g = ds[0]       # second half of a split block
                continue
            assert len(ds) == len(tds), (g, ds, t, tds)
            todo += [(a, b) for a, b in zip(ds, tds) if a != 1]
            break
    return m


def flows(fn, est, over):
    arcs = fn['arcs']
    m = mapping(arcs, est)
    probs = {}
    for s, d, f in arcs:
        if f & FAKE:
            continue
        t = m[s]
        if s == 0:
            probs[(s, d)] = 100.0
        elif m.get(d) == t:
            probs[(s, d)] = 100.0       # split chain
        else:
            probs[(s, d)] = est[t][1][m[d]]
    fn['map'] = m
    # `fn:bb>1=P` on a block with a fake arc to EXIT (a call that may not
    # return): P% of its flow leaves by that arc, the real successors share
    # the rest in their ratios
    fakeov = {}
    for (ts, td), p in list(over.items()):
        if td == 1 and not any(m[k[0]] == ts and m[k[1]] == 1 for k in probs):
            for s, d, f in arcs:
                if f & FAKE and d == 1 and m.get(s) == ts:
                    fakeov[s] = p
            del over[(ts, td)]
    for s, p in fakeov.items():
        for k in [k for k in probs if k[0] == s]:
            probs[k] *= (100 - p) / 100
        probs[(s, 1)] = p
    groups = {}
    for (ts, td), p in over.items():
        s, d = [k for k in probs if m[k[0]] == ts and m[k[1]] == td and ts != td][0]
        groups.setdefault(s, {})[d] = p
    for s, ds in groups.items():
        rest = sum(v for (a, b), v in probs.items() if a == s and b not in ds)
        left = 100 - sum(ds.values())
        for k in [k for k in probs if k[0] == s and k[1] not in ds]:
            probs[k] = probs[k] * left / rest if rest else left
        for d, p in ds.items():
            probs[(s, d)] = p
    x, flow = solve(arcs, probs, fakeov)
    real = {s for s, d, f in arcs if not f & FAKE}
    for s, d, f in arcs:
        if f & FAKE and s not in real:
            flow[(s, d)] = x.get(s, 0)      # noreturn call: leaves by its fake edge
    return flow, x


def hot_scale(x):
    """Counts per unit flow so that count >= THRESHOLD matches the guessed test
    (cold iff freq < entry freq / 1000, integer division); None when that
    test is 0 (every block hot, see min_flow)."""
    xmax = max(x.values())
    m = round(x[0] * 10000 / xmax) // 1000
    return THRESHOLD / ((m - 0.5) * xmax / 10000) if m else None


CONSISTENT = False
MULT = {}
ENTRY = {}
RUNS = 1


def integer_flow(arcs, f):
    """Integer arc counts that conserve flow exactly (--consistent): zero-flow
    arcs stay 0, the others are rounded except on a max-flow spanning tree
    (plus a virtual EXIT->ENTRY arc), whose arcs absorb the rounding. Plain
    per-arc rounding can leave a zero-flow arc gcc solves at -1."""
    pos = [(s, d) for s, d, fl in arcs if f.get((s, d), 0) > 1e-9]
    parent = {}

    def find(a):
        while parent.setdefault(a, a) != a:
            a = parent[a]
        return a
    tree = {(1, 0)}
    parent[find(1)] = find(0)
    for k in sorted(pos, key=lambda k: -f[k]):
        a, b = find(k[0]), find(k[1])
        if a != b:
            parent[a] = b
            tree.add(k)
    c = {(s, d): (round(f[(s, d)]) if (s, d) in pos else 0) for s, d, fl in arcs}
    c[(1, 0)] = 0
    # solve the tree arcs by peeling leaves (conservation: in == out at every block)
    unknown = set(tree)
    while unknown:
        for v in {x for k in unknown for x in k}:
            inc = [k for k in unknown if v in k]
            if len(inc) == 1:
                k = inc[0]
                unknown.discard(k)
                e = sum(n for a, n in c.items() if a[1] == v and a not in unknown and a != k) - \
                    sum(n for a, n in c.items() if a[0] == v and a not in unknown and a != k)
                c[k] = e if k[0] == v else -e
                break
        else:
            raise SystemExit('integer_flow: tree solve stuck')
    del c[(1, 0)]
    assert all(v >= 0 for v in c.values()), [k for k, v in c.items() if v < 0]
    return c


def map_bb(fns, name, bb):
    """A gcno block of function `name` that is (part of) dump block bb."""
    m = [f for f in fns if f['name'] == name][0]['map']
    return min(g for g, t in m.items() if t == bb)


def main():
    gcno, dump, out = sys.argv[1:4]
    over, only, srcfile = {}, None, None
    args = []
    for a in sys.argv[4:]:
        # @file: overrides one per line (# comments)
        args += [l.split('#')[0].strip() for l in open(a[1:])] if a.startswith('@') else [a]
    for a in filter(None, args):
        if a.startswith('--only='):
            only = a[7:].split(',')
            continue
        if a.startswith('--mult='):
            # --mult=fn:K: a static function's counts K times its call
            # sites' (a called-once body is inlined with its own counts)
            f, k = a[7:].split(':')
            MULT[f] = float(k)
            continue
        if a.startswith('--entry='):
            # --entry=fn:caller:bb: fn's entry count is caller's dump block bb's
            # count (gcc 6 inlines a global callee with its own counts, unscaled)
            f, cf, bb = a[8:].split(':')
            ENTRY[f] = (cf, int(bb))
            continue
        if a.startswith('--runs='):
            # the summary's run count: 0 makes no block probably-never-executed
            # (count * fraction >= runs), so count-0 blocks key -freq in bb-reorder
            global RUNS
            RUNS = int(a[7:])
            continue
        if a == '--consistent':
            global CONSISTENT
            CONSISTENT = True
            continue
        if a.startswith('--src='):
            srcfile = a[6:]
            continue
        if a.startswith('--threshold='):
            # a smaller hot threshold when every block must be hot and the
            # smallest flow is tiny (counts * 10000 must still fit 64 bits)
            global THRESHOLD
            THRESHOLD = int(a[12:])
            continue
        m = re.match(r'(\w+):(\d+)>(\d+)=([\d.]+)$', a)
        over.setdefault(m.group(1), {})[(int(m.group(2)), int(m.group(3)))] = float(m.group(4))
    version, stamp, fns = read_gcno(gcno)
    if only:
        fns = [f for f in fns if f['name'] in only]
    est, calls = read_dump(dump)
    # a static function's entry count must be its call sites' (an inlined
    # called-once body keeps its own counts); the rest get the hot-test scale
    text = open(srcfile or fns[0]['src']).read()
    static = {f['name'] for f in fns
              if re.search(r'^static\b[^;{]*\b%s\s*\(' % f['name'], text, re.M)}
    fl = {fn['name']: flows(fn, est[fn['name']], over.get(fn['name'], {})) for fn in fns}
    sites = {n: [(f, map_bb(fns, f, bb)) for f in calls if f in fl
                 for bb, cs in calls[f].items() if n in cs]
             for n in static}
    for f, (cf, bb) in ENTRY.items():
        static.add(f)
        sites[f] = [(cf, map_bb(fns, cf, bb))]

    def min_flow(name):
        """Smallest flow (entry = 1) in name and the static functions inlined into it."""
        x = fl[name][1]
        v = min(f for f in x.values() if f > 0)
        for c in static:
            for f, g in sites[c]:
                if f == name:
                    v = min(v, x[g] * min_flow(c))
        return v

    scale = {}
    while len(scale) < len(fns):
        for fn in fns:
            name = fn['name']
            if name in scale:
                continue
            if name in static and sites[name]:
                if any(f not in scale for f, g in sites[name]):
                    continue
                scale[name] = sum(fl[f][1][g] * scale[f] for f, g in sites[name]) * MULT.get(name, 1)
            else:
                scale[name] = (hot_scale(fl[name][1]) or THRESHOLD / min_flow(name)) * MULT.get(name, 1)
    words, allc = [], []
    for fn in fns:
        c = {k: round(v * scale[fn['name']]) for k, v in fl[fn['name']][0].items()}
        if CONSISTENT:
            c = integer_flow(fn['arcs'], {k: v * scale[fn['name']] for k, v in fl[fn['name']][0].items()})
        ctr = [c.get((s, d), 0) for s, d, f in fn['arcs'] if not f & ON_TREE]
        allc += ctr
        words += [T_FUNCTION, 3, fn['ident'], fn['lck'], fn['cck'], T_COUNTER_ARCS, 2 * len(ctr)]
        for v in ctr:
            words += [v & 0xffffffff, v >> 32]
    # program summary: RUNS runs, one histogram bucket whose min is the hot threshold
    tot, mx = sum(allc), max(allc)
    lo = lambda v: [v & 0xffffffff, v >> 32]
    bucket = 0
    while (1 << (bucket // 4 + 1)) <= THRESHOLD:   # any bucket at or above it works
        bucket += 4
    bv = [0] * 8
    bv[bucket // 32] |= 1 << (bucket % 32)
    summ = [0, len(allc), RUNS] + lo(tot) + lo(mx) + lo(mx) + bv + [len(allc)] + lo(THRESHOLD) + lo(tot)
    # read_counts_file gives each counter record the summary read before it
    words = [T_PROGRAM_SUMMARY, len(summ)] + summ + words
    open(out, 'wb').write(struct.pack('<3I', 0x67636461, version, stamp) + struct.pack('<%dI' % len(words), *words))
    print('%d functions, %d counters' % (len(fns), len(allc)))


if __name__ == '__main__':
    main()
