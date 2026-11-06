"""mode_client attempt 7: the latch-compare flip toggle.  Attempt 3's `x = argv[i + 1];
i++;` spelling (all arms) set PRE's latch-phi name; reverting it to `x = argv[++i];` flips
the compare back on bases where a removal flipped it.  Cross the toggle (all arms, or one)
with every near miss of a singles file (mc1 edits on the base).

python tools/wip/dehint/mc7rev.py BASE.c SINGLES.json [-m 80] [-j 4]"""
import json, os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib

PAT = re.compile(r'(\w+) = argv\[i \+ 1\];\n(\t+)i\+\+;')


def rev(t):
    return PAT.sub(lambda m: '%s = argv[++i];' % m.group(1), t)


def main():
    a = sys.argv[1:]
    base = mc1lib.read_src(a[0])
    sj = json.load(open(a[1]))
    md = int(a[a.index('-m') + 1]) if '-m' in a else 80
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    t = mc1.build_template(base)
    c0 = mc1.count(base)['total']
    todo = []
    for k, r in sj.items():
        m = re.match(r'(\d+)', r['r'])
        if r['ok'] or not m or int(m.group(1)) > md or r['count'] >= c0 or k.startswith(('G_', '-np')):
            continue
        txt = mc1.render(t, r['state'], r['drops'], r.get('post', []))
        todo.append((k, rev(txt)))
    print(len(todo), 'near misses x revert', flush=True)
    res = []
    with ThreadPoolExecutor(jobs) as ex:
        for k, s, txt in ex.map(lambda it: (it[0], mc1lib.score_text(it[1]), it[1]), todo):
            if 'compile' in s:
                continue
            d = 0 if s['identical'] else s['total']
            if d == 0:
                print('HIT', k, mc1.count(txt)['total'], flush=True)
            res.append((d, k))
    res.sort()
    print(res[:20])


if __name__ == '__main__':
    main()
