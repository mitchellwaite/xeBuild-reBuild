"""mode_client attempt 16: mc16l6's case 3 list subsets crossed with t4 / t5 added to the
start of rok's list (rko asm goto: dv, c12, s5, c9, ...), count corrected, scored, with the
vrp1 frequencies of c2/t4/t5.

python tools/wip/dehint/mc16l6r.py BASE_k0.c [-j 4] [-need hdd4,hdd5]"""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1lib, mc12vrp, mc14filt, mc15k, mc16freq
from mc16l6 import OLD

RKO = '__asm__ goto ("" :::: dv, c12,'


def main():
    a = sys.argv[1:]
    t = mc1lib.read_src(a[0])
    assert OLD in t and RKO in t
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    need = a[a.index('-need') + 1].split(',') if '-need' in a else []
    labs = ['t4', 't5', 'c9', 'hdd4', 'hdd5', 'c3', 'dv']
    subs = [s for n in range(1, 8) for s in itertools.combinations(labs, n) if all(x in s for x in need)]
    todo = [(s, r) for s in subs for r in ((), ('t4',), ('t5',), ('t4', 't5'))]

    def one(it):
        sub, r = it
        x = t.replace(OLD, 'JMP(%s);' % ', '.join(sub), 1)
        if r:
            x = x.replace(RKO, '__asm__ goto ("" :::: %s, dv, c12,' % ', '.join(r), 1)
        try:
            k = 205 - mc14filt.c7x(mc12vrp.threads(x))
        except Exception:
            return it, None, None, None
        y = mc15k.add(x, k) if 0 <= k <= 8 else None
        if y is None:
            return it, k, None, None
        s = mc1lib.score_text(y, [])
        fr = {h[0]: f for _, f, h in mc16freq.freqs(y, 'vrp1', ['c2', 't4', 't5'])}
        return it, k, s, fr
    with ThreadPoolExecutor(jobs) as ex:
        for (sub, r), k, s, fr in ex.map(one, todo):
            name = 'l6=%s rko+=%s' % (','.join(sub), ','.join(r) or '-')
            if s is None:
                print('skip', k, name, flush=True)
                continue
            print(0 if s.get('identical') else s.get('total'), 'k%s' % k, fr, name, flush=True)


if __name__ == '__main__':
    main()
