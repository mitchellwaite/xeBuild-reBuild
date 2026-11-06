"""mode_client attempt 15: each register/memory pin removed (alone and the two -i/-p "d"
pins together) x k = 0..6 extra vrp1 blocks (mc14rmk.add), with the thread targets.
BASE must be a k = 0 text.

python tools/wip/dehint/mc15pins.py BASE_k0.c [-j 2] [-o DIR]"""
import os, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1lib, mc12vrp, mc14rmk

D = ' || ({ __asm__ ("" :: "d"(i + 1)); 0; })'
PINS = [
    ('bp_a', [('\t__asm__("" :: "a"(i + 1));\n', '')]),
    ('i_d', [(D, '')]),
    ('p_d', [(D, '')]),        # second occurrence, handled below
    ('ip_d', [(D, ''), (D, '')]),
    ('r_a', [('__asm__ goto ("" :: "a"(i) :: rk6, r5x, r3x)', '__asm__ goto ("" :::: rk6, r5x, r3x)')]),
    ('rko_m', [('{ __asm__ ("" :: "m"(rko)); goto rkn2; }', '{ goto rkn2; }')]),
    ('fkv_X', [('__asm__ ("" :: "X"(&fkv)); ', '')]),
]


def variants(t):
    out = []
    for name, eds in PINS:
        x = t
        if name == 'p_d':
            i = x.index(D, x.index(D) + 1)
            x = x[:i] + x[i + len(D):]
        else:
            for o, n in eds:
                if o not in x:
                    x = None
                    break
                x = x.replace(o, n, 1)
        if x is not None:
            out.append((name, x))
    return out


def main():
    a = sys.argv[1:]
    t = mc1lib.read_src(a[0])
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 2
    odir = a[a.index('-o') + 1] if '-o' in a else None
    todo = [(n, k, mc14rmk.add(x, k)) for n, x in variants(t) for k in range(7)]

    def one(it):
        n, k, y = it
        if y is None:
            return n, k, None, None, y
        try:
            th = ','.join(z for _, _, z in mc12vrp.threads(y))
        except Exception:
            th = '?'
        return n, k, th, mc1lib.score_text(y, []), y
    with ThreadPoolExecutor(jobs) as ex:
        for n, k, th, s, y in ex.map(one, todo):
            if s is None:
                print('missing', n, k, flush=True)
                continue
            d = 0 if s.get('identical') else s.get('total', 99999)
            print(d, n, 'k%d' % k, th, flush=True)
            if d == 0 and odir:
                os.makedirs(odir, exist_ok=True)
                open(os.path.join(odir, 'hit_%s_%d.c' % (n, k)), 'w', newline='\n').write(y)


if __name__ == '__main__':
    main()
