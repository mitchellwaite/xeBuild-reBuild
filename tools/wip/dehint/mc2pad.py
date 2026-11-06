"""mode_client attempt 2: remove a cp chain (or other hint) and pad another cp chain with
fewer extra terms, i.e. look for net reductions where only the count of terms matters.

python tools/wip/dehint/mc2pad.py -r KEY[,KEY..] [-k MAXK] [-j N] [-2]
KEY: mc1 edit keys (m2_singles.json); each base gets k = 1..MAXK extra terms on every
chain (-2: also on every pair of chains, k1 + k2 <= MAXK).  Only variants with a net
reduction are scored.  Hits -> build/mc/m2pad_hits.json."""
import itertools, json, os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib

HITS = os.path.join(mc1lib.BUILD, 'm2pad_hits.json')
CHAIN = re.compile(r'if \(([^;{}]*__builtin_constant_p\((\w+) \+ \d+\)[^;{}]*)\) (goto \w+|mode = \d+);')


def chains(text):
    out = []
    for m in CHAIN.finditer(text):
        out.append((m.end(1), m.group(2), text[:m.start()].count('\n') + 1, m.group(3)))
    return out


def pad(text, ks):
    """ks: {chain index: k}; insert k terms at the end of each chain's condition"""
    cs = chains(text)
    seq = [900000]
    for idx in sorted(ks, key=lambda i: -cs[i][0]):
        pos, var = cs[idx][0], cs[idx][1]
        add = ''
        for _ in range(ks[idx]):
            seq[0] += 1
            add += ' && __builtin_constant_p(%s + %d)' % (var, seq[0])
        text = text[:pos] + add + text[pos:]
    return text


def main():
    a = sys.argv[1:]
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    maxk = int(a[a.index('-k') + 1]) if '-k' in a else 3
    keys = a[a.index('-r') + 1].split(',')
    t = mc1.build_template(mc1lib.read_src(mc1.BASE))
    es = {e[0]: e for e in mc1.edits(t)}
    n0 = mc1.count(mc1lib.read_src(mc1.BASE))['total']
    todo = []
    for key in keys:
        st = mc1.merge(({}, {}, []), es[key][1:])
        base = mc1.render(t, *st)
        gain = n0 - mc1.count(base)['total']
        cs = chains(base)
        specs = [{i: k} for i in range(len(cs)) for k in range(1, min(maxk, gain - 1) + 1)]
        if '-2' in a:
            for i, j in itertools.combinations(range(len(cs)), 2):
                for k1 in range(1, maxk):
                    for k2 in range(1, maxk - k1 + 1):
                        if k1 + k2 < gain:
                            specs.append({i: k1, j: k2})
        for sp in specs:
            name = key + ' + ' + ' '.join('L%d%s+%d' % (cs[i][2], cs[i][3].split()[-1], k) for i, k in sp.items())
            todo.append((name, pad(base, sp)))
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
    for d, k in sorted(best)[:20]:
        print(d, k)


if __name__ == '__main__':
    main()
