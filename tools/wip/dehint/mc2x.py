"""mode_client attempt 2: natural micro-edits (term orders of the parser's argument tests)
alone and combined with mc1 hint removals.

python tools/wip/dehint/mc2x.py list
python tools/wip/dehint/mc2x.py run [-r REMOVALS] [-n 1|2] [-j N]
REMOVALS: comma-separated mc1 edit keys (as in build/mc/m2_singles.json), each tried with
every natural edit (and with pairs of natural edits when -n 2); 'none' = no removal.
Hits are printed and appended to build/mc/m2x_hits.json."""
import itertools, json, os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib

HITS = os.path.join(mc1lib.BUILD, 'm2x_hits.json')


def term_perms(cond):
    """term orders that keep each null test before its dereference"""
    terms = cond.split(' || ')
    def safe(p):
        for k, x in enumerate(p):
            if x.startswith('*'):
                null = '!' + x[1:].split(' ')[0]
                if null in p and p.index(null) > k:
                    return False
        return True
    return [' || '.join(p) for p in itertools.permutations(terms) if list(p) != terms and safe(p)]


def natural_edits(text):
    """[(name, start, end, replacement)] on text positions"""
    out = []
    for m in re.finditer(r'if \(((?:[^()]|\([^()]*\))*? \|\| (?:[^()]|\([^()]*\))*?)\)', text):
        cond = m.group(1)
        if '__asm__' in cond or 'strnicmp' in cond or '== \'-\'' not in cond:
            continue
        line = text[:m.start()].count('\n') + 1
        for k, alt in enumerate(term_perms(cond)):
            out.append(('L%d_p%d' % (line, k), m.start(1), m.end(1), alt))
    return out


def apply(text, eds):
    for _, s, e, r in sorted(eds, key=lambda x: -x[1]):
        text = text[:s] + r + text[e:]
    return text


def main():
    a = sys.argv[1:]
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    n = int(a[a.index('-n') + 1]) if '-n' in a else 1
    rem = a[a.index('-r') + 1].split(',') if '-r' in a else ['none']
    t = mc1.build_template(mc1lib.read_src(mc1.BASE))
    es = {e[0]: e for e in mc1.edits(t)}
    if a[0] == 'list':
        for x in natural_edits(mc1lib.read_src(mc1.BASE)):
            print(x[0], x[3])
        return
    todo = []
    for r in rem:
        st = ({}, {}, []) if r == 'none' else mc1.merge(({}, {}, []), es[r][1:])
        base = mc1.render(t, *st)
        nat = natural_edits(base)
        for c in itertools.combinations(nat, n):
            if len({x[1] for x in c}) < n:
                continue
            todo.append(('%s + %s' % (r, ' + '.join(x[0] for x in c)), apply(base, c)))
    print(len(todo), 'variants', flush=True)
    hits = json.load(open(HITS)) if os.path.exists(HITS) else {}
    best = []
    def one(v):
        s = mc1lib.score_text(v[1])
        return v[0], s, mc1.count(v[1])['total']
    with ThreadPoolExecutor(jobs) as ex:
        for k, s, c in ex.map(one, todo):
            if s.get('identical'):
                print('HIT', k, c, flush=True)
                hits[k] = c
                json.dump(hits, open(HITS, 'w'), indent=1)
            elif 'total' in s:
                best.append((s['total'], k))
    for d, k in sorted(best)[:15]:
        print(d, k)


if __name__ == '__main__':
    main()
