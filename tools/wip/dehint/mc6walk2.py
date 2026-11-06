"""mode_client attempt 6: walk from a base with the case-head feeds removed (mc6case_order's
strip), using count-neutral asm goto list edits and cheap new cp feeds (1-3 terms) into the
case heads, to find a cheaper set of hints that restores the reference's case order.

python tools/wip/dehint/mc6walk2.py BASE.c OUT_PREFIX [-j 6] [-steps 40] [-max COUNT]
Objective: (diff lines, case-order inversions, trick count), lowest first; a move is
taken only if it improves it and the count stays below -max (default 84)."""
import os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib, mc6case_order, mc6walk

REF_ORDER = [10, 12, 1, 3, 4, 5, 2, 8, 9, 11, 7]
HEADS = ['c1', 'c2', 'c3', 't4', 't5', 'c7', 'c8', 'c9', 'c10', 'c11', 'c12', 'cdef']
LOCS = {'fail': 'fail: __attribute__((cold));', 'dsp': 'dsp: cinfo = netGetInfo();'}
NEWF = re.compile(r' if \((__builtin_constant_p\(mode \+ 7\d{5}\)(?: && __builtin_constant_p\(mode \+ 7\d{5}\))*)\) goto (\w+);')
cnt = [0]


def inv(seq):
    pos = {v: i for i, v in enumerate(REF_ORDER)}
    s = [pos[x] for x in seq if x in pos]
    return sum(1 for i in range(len(s)) for j in range(i + 1, len(s)) if s[i] > s[j])


def feed(k, tgt):
    terms = []
    for _ in range(k):
        cnt[0] += 1
        terms.append('__builtin_constant_p(mode + %d)' % (700000 + cnt[0]))
    return ' if (%s) goto %s;' % (' && '.join(terms), tgt)


def moves(text):
    out = mc6walk.moves(text)
    for ln, anchor in LOCS.items():
        for h in HEADS:
            if not re.search(r'\b%s:|AT\(%s\)' % (h, h), text):
                continue
            for k in (1, 2, 3):
                i = text.index(anchor) + len(anchor)
                out.append(('F%s%d+%s' % (ln, k, h), text[:i] + feed(k, h) + text[i:]))
    for m in NEWF.finditer(text):
        out.append(('F-%s' % m.group(2), text[:m.start()] + text[m.end():]))
        terms = m.group(1).split(' && ')
        if len(terms) > 1:
            new = ' if (%s) goto %s;' % (' && '.join(terms[1:]), m.group(2))
            out.append(('Ft-%s' % m.group(2), text[:m.start()] + new + text[m.end():]))
    return out


def score(item):
    name, text = item
    s = mc1lib.score_text(text)
    c = mc1.count(text)['total']
    if 'compile' in s:
        return name, (99999, 99, c), text
    if s['identical']:
        return name, (0, 0, c), text
    ok, o, d = mc1lib.compile_src(text)
    seq = mc6case_order.order(o)
    mc1lib.cleanup(d)
    return name, (s['total'], inv(seq), c), text


def main():
    a = sys.argv[1:]
    base, pre = a[0], a[1]
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 6
    steps = int(a[a.index('-steps') + 1]) if '-steps' in a else 40
    mx = int(a[a.index('-max') + 1]) if '-max' in a else 84
    cur = mc1lib.read_src(base)
    _, s0, _ = score(('base', cur))
    print('base', s0, flush=True)
    path = []
    for st in range(steps):
        mv = moves(cur)
        with ThreadPoolExecutor(jobs) as ex:
            res = sorted((r for r in ex.map(score, mv) if r[1][2] < mx), key=lambda r: r[1])
        print('step', st, len(mv), 'top', [(r[0], r[1]) for r in res[:5]], flush=True)
        if not res or res[0][1] >= s0:
            print('stuck at', s0, path, flush=True)
            break
        cur, s0 = res[0][2], res[0][1]
        path.append(res[0][0])
        open('%s_%d.c' % (pre, st), 'w', newline='\n').write(cur)
        print('took', res[0][0], s0, flush=True)
        if s0[0] == 0:
            print('IDENTICAL', path, s0, flush=True)
            break


if __name__ == '__main__':
    main()
