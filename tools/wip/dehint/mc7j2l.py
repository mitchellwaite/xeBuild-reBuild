"""mode_client attempt 7: an asm goto statement removed and its labels moved into other asm
goto label lists (labels in a list are not counted; the statement is).  Each label goes to
another list of the same function (at its start or end) or is dropped.

python tools/wip/dehint/mc7j2l.py [-base FILE] [-j 4] [-only IDX,...] [-nodrop]
Prints the statements (index, labels); then per statement the IDENTICAL hits and the best
misses.  -o DIR writes each hit as DIR/j2l_<idx>_<n>.c"""
import itertools, os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib


def fn_ranges(t):
    out = []
    for nm, hd in (('cebi', 'static void clientEraseBlockI('), ('mc', 'int mode_client(')):
        s = t.index(hd)
        e = t.index('\n}\n', s)
        out.append((nm, s, e))
    return out


def stmts(t):
    """[(fn, stmt_start, stmt_end, lab_start, lab_end, labels, removable)]"""
    res = []
    rng = fn_ranges(t)
    for m in re.finditer(r'\bJMP\(([^)]*)\);', t):
        if t[m.start() - 8:m.start()].endswith('define '):
            continue
        fn = [n for n, s, e in rng if s < m.start() < e]
        if not fn:
            continue
        res.append((fn[0], m.start(), m.end(), m.start(1), m.end(1),
                    [x.strip() for x in m.group(1).split(',')], True))
    for m in re.finditer(r'__asm__ goto \(', t):
        # find the matching ')' and the last ':' before it
        k, d = m.end(), 1
        while d:
            d += {'(': 1, ')': -1}.get(t[k], 0)
            k += 1
        body_end = k - 1
        c = t.rindex(':', m.end(), body_end) + 1
        fn = [n for n, s, e in rng if s < m.start() < e]
        if not fn:
            continue
        labs = [x.strip() for x in t[c:body_end].split(',')]
        ls = c + len(t[c:body_end]) - len(t[c:body_end].lstrip())
        se = t.index(';', body_end) + 1
        rem = '"i"(107)' in t[m.start():body_end]
        res.append((fn[0], m.start(), se, ls, body_end, labs, rem))
    return sorted(res, key=lambda r: r[1])


def apply(t, edits):
    for s, e, txt in sorted(edits, key=lambda x: -x[0]):
        t = t[:s] + txt + t[e:]
    return t


def main():
    a = sys.argv[1:]
    base = mc1lib.read_src(a[a.index('-base') + 1] if '-base' in a else mc1.BASE)
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    only = [int(x) for x in a[a.index('-only') + 1].split(',')] if '-only' in a else None
    odir = a[a.index('-o') + 1] if '-o' in a else None
    st = stmts(base)
    for i, s in enumerate(st):
        print(i, s[0], s[5], 'removable' if s[6] else '', flush=True)
    for i, s in enumerate(st):
        if not s[6] or (only and i not in only):
            continue
        others = [(j, o) for j, o in enumerate(st) if j != i and o[0] == s[0]]
        # each label: drop, or (list j, start|end)
        choices = ([None] if '-nodrop' not in a else []) + [(j, w) for j, _ in others for w in ('s', 'e')]
        todo = []
        for combo in itertools.product(choices, repeat=len(s[5])):
            if len(s[5]) > 2 and sum(c is not None for c in combo) < len(combo) - 1:
                continue
            ed = [(s[1], s[2], '')]
            add = {}
            for lab, c in zip(s[5], combo):
                if c is not None:
                    add.setdefault(c, []).append(lab)
            for (j, w), labs in add.items():
                o = st[j]
                if w == 's':
                    ed.append((o[3], o[3], ', '.join(labs) + ', '))
                else:
                    ed.append((o[4], o[4], ', ' + ', '.join(labs)))
            todo.append((combo, apply(base, ed)))

        def one(it):
            return it[0], mc1lib.score_text(it[1]), it[1]

        res = []
        with ThreadPoolExecutor(jobs) as ex:
            for combo, sc, txt in ex.map(one, todo):
                if 'compile' in sc:
                    res.append((99999, combo, None))
                    continue
                res.append((0 if sc['identical'] else sc['total'], combo, txt))
        res.sort(key=lambda r: r[0])
        nh = 0
        for d, combo, txt in res:
            if d == 0:
                nh += 1
                print('HIT', i, s[5], combo, 'count', mc1.count(txt)['total'], flush=True)
                if odir:
                    open(os.path.join(odir, 'j2l_%d_%d.c' % (i, nh)), 'w', newline='\n').write(txt)
        print('stmt', i, s[5], len(todo), 'variants, hits', nh, 'best',
              [(d, c) for d, c, _ in res[:4]], flush=True)


if __name__ == '__main__':
    main()
