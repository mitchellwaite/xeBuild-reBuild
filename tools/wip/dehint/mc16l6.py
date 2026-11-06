"""mode_client attempt 16: case 3's list (`JMP(hdd4, hdd5, c3, dv)`, whose edges are gone by
RTL but feed profile_estimate) set to every subset of LABELS (in that order), block count
corrected (mc15k), scored, with the vrp1 frequencies of c2/t4/t5.

python tools/wip/dehint/mc16l6.py BASE_k0.c [-j 4] [-l t4,t5,c9,hdd4,hdd5,c3,dv] [-need hdd4,...]"""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1lib, mc12vrp, mc14filt, mc15k, mc16freq

OLD = 'JMP(hdd4, hdd5, c3, dv);'


def main():
    a = sys.argv[1:]
    t = mc1lib.read_src(a[0])
    assert OLD in t
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    labs = a[a.index('-l') + 1].split(',') if '-l' in a else ['t4', 't5', 'c9', 'hdd4', 'hdd5', 'c3', 'dv']
    need = a[a.index('-need') + 1].split(',') if '-need' in a else []
    todo = []
    for n in range(1, len(labs) + 1):
        for sub in itertools.combinations(labs, n):
            if all(x in sub for x in need):
                todo.append(sub)

    def one(sub):
        x = t.replace(OLD, 'JMP(%s);' % ', '.join(sub), 1)
        try:
            k = 205 - mc14filt.c7x(mc12vrp.threads(x))
        except Exception:
            return sub, None, None, None
        y = mc15k.add(x, k) if 0 <= k <= 8 else None
        if y is None:
            return sub, k, None, None
        s = mc1lib.score_text(y, [])
        fr = {h[0]: f for _, f, h in mc16freq.freqs(y, 'vrp1', ['c2', 't4', 't5'])}
        return sub, k, s, fr
    with ThreadPoolExecutor(jobs) as ex:
        for sub, k, s, fr in ex.map(one, todo):
            name = ','.join(sub)
            if s is None:
                print('skip', k, name, flush=True)
                continue
            dd = 0 if s.get('identical') else s.get('total', 99999)
            print(dd, 'k%s' % k, fr, name, flush=True)


if __name__ == '__main__':
    main()
