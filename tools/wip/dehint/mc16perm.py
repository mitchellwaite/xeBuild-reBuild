"""mode_client attempt 16: every order of case 3's list (labels given) on a BASE_k0, block count
corrected, scored, with the case keys (mc12keys) of the best.

python tools/wip/dehint/mc16perm.py BASE_k0.c t4,t5,hdd4,hdd5,c3 [-j 4]"""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1lib, mc12vrp, mc14filt, mc15k
from mc16l6 import OLD


def main():
    a = sys.argv[1:]
    t = mc1lib.read_src(a[0])
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    labs = a[1].split(',')
    old = OLD if OLD in t else None
    if old is None:
        import re
        old = re.search(r'JMP\((?:\w+, )*c3(?:, \w+)*\);', t).group(0)

    def one(p):
        x = t.replace(old, 'JMP(%s);' % ', '.join(p), 1)
        k = 205 - mc14filt.c7x(mc12vrp.threads(x))
        y = mc15k.add(x, k) if 0 <= k <= 8 else None
        if y is None:
            return p, k, None
        return p, k, mc1lib.score_text(y, [])
    with ThreadPoolExecutor(jobs) as ex:
        for p, k, s in ex.map(one, list(itertools.permutations(labs))):
            if s is None:
                print('skip', k, ','.join(p), flush=True)
                continue
            print(0 if s.get('identical') else s.get('total'), 'k%s' % k, ','.join(p), flush=True)


if __name__ == '__main__':
    main()
