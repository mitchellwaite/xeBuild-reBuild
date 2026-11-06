"""mode_client attempt 16: t4 and/or t5 added to asm goto lists (one each, start of list) on
a BASE_k0, block count corrected (mc15k), scored, with the vrp1 frequencies of c2/t4/t5.

python tools/wip/dehint/mc16t45.py BASE_k0.c [-j 4] [-pre IDX,...]
  -pre: mc8comp edit indices applied first (on BASE)"""
import os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1lib, mc7j2l, mc8comp, mc12vrp, mc14filt, mc15k, mc16freq


def main():
    a = sys.argv[1:]
    t = mc1lib.read_src(a[0])
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    if '-pre' in a:
        for i in sorted((int(x) for x in a[a.index('-pre') + 1].split(',')), reverse=True):
            t = mc7j2l.apply(t, mc8comp.edits(t)[i][1])
    eds = mc8comp.edits(t)
    t4 = [(d, e) for d, e in eds if d.startswith('add t4>') and d.endswith('.s')]
    t5 = [(d, e) for d, e in eds if d.startswith('add t5>') and d.endswith('.s')]
    todo = [[x] for x in t4 + t5] + [[x, y] for x in t4 for y in t5]

    def one(combo):
        x = t
        for d, e in combo:
            ed = dict(mc8comp.edits(x)).get(d)
            if ed is None:
                return combo, None, None, None
            x = mc7j2l.apply(x, ed)
        try:
            k = 205 - mc14filt.c7x(mc12vrp.threads(x))
        except Exception:
            return combo, None, None, None
        y = mc15k.add(x, k) if 0 <= k <= 8 else None
        if y is None:
            return combo, k, None, None
        s = mc1lib.score_text(y, [])
        fr = {h[0]: f for _, f, h in mc16freq.freqs(y, 'vrp1', ['c2', 't4', 't5'])}
        return combo, k, s, fr
    with ThreadPoolExecutor(jobs) as ex:
        for combo, k, s, fr in ex.map(one, todo):
            name = ' + '.join(d for d, _ in combo)
            if s is None:
                print('skip', k, name, flush=True)
                continue
            dd = 0 if s.get('identical') else s.get('total', 99999)
            print(dd, 'k%s' % k, fr, name, flush=True)


if __name__ == '__main__':
    main()
