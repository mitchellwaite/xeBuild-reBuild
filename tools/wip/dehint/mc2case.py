"""mode_client attempt 2: move one case of the mode switch (case order is the author's free
choice), alone and on top of mc1 hint removals.

python tools/wip/dehint/mc2case.py -r KEY[,KEY..] [-j N]    KEY 'none' = no removal
Hits -> build/mc/m2case_hits.json."""
import json, os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib

HITS = os.path.join(mc1lib.BUILD, 'm2case_hits.json')


def cases(text):
    """(start, end, [case texts]) of the mode switch body"""
    s = text.index('switch (mode) {') + len('switch (mode) {')
    e = text.index('\n\t\t\t}\n\t\t} else\n\t\t\tgoto fail;', s)
    body = text[s:e]
    parts = re.split(r'(?=\n\t\t\t(?:case \d+|default):)', body)
    assert parts[0] == '', repr(parts[0][:40])
    return s, e, parts[1:]


def moves(text):
    s, e, parts = cases(text)
    out = []
    n = len(parts)
    for i in range(n):
        for j in range(n):
            if i == j or j == i + 1:
                continue
            p = list(parts)
            x = p.pop(i)
            p.insert(j if j < i else j - 1, x)
            lab = lambda q: re.match(r'\n\t\t\t(case \d+|default)', q).group(1).replace('case ', 'c')
            out.append(('%s->before_%s' % (lab(x), lab(parts[j]) if j < n else 'end'), text[:s] + ''.join(p) + text[e:]))
    return out


def main():
    a = sys.argv[1:]
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    keys = a[a.index('-r') + 1].split(',') if '-r' in a else ['none']
    t = mc1.build_template(mc1lib.read_src(mc1.BASE))
    es = {e[0]: e for e in mc1.edits(t)}
    todo = []
    for key in keys:
        st = ({}, {}, []) if key == 'none' else mc1.merge(({}, {}, []), es[key][1:])
        base = mc1.render(t, *st)
        for nm, v in moves(base):
            todo.append((key + ' + ' + nm, v))
    print(len(todo), 'variants', flush=True)
    hits = json.load(open(HITS)) if os.path.exists(HITS) else {}
    best = []

    def one(v):
        return v[0], mc1lib.score_text(v[1]), mc1.count(v[1])['total']
    with ThreadPoolExecutor(jobs) as ex:
        for k, s, c in ex.map(one, todo):
            if s.get('identical'):
                print('HIT', k, c, flush=True)
                hits[k] = c
                json.dump(hits, open(HITS, 'w'), indent=1)
            elif 'total' in s:
                best.append((s['total'], k))
    for d, k in sorted(best)[:25]:
        print(d, k)


if __name__ == '__main__':
    main()
