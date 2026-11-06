"""mode_client attempt 14: a k = 0 base with every combination of the duplicated-noreturn
block shapes (help split 1 or 2, oneArg / wbArgs / -c / -e / -r / -w / -ip splits), scored,
grouped by the number of blocks they add.  Shows whether which shapes give the k matters.

python tools/wip/dehint/mc14shapes.py BASE_k0.c [-k 3] [-j 4] [-o DIR]"""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1lib, mc14rmk as R

Q = R.Q
RA = ('\t\t\tif (i + 1 == argc || !a || *a == ' + Q + ')\n\t\t\t\t{ r3x: client_usage(3, argv[i]); }',
      '\t\t\tif (i + 1 == argc || !a)\n\t\t\t\t{ r3x: client_usage(3, argv[i]); }\n\t\t\tif (*a == ' + Q + ')\n\t\t\t\tclient_usage(3, argv[i]);')
WA_OLD = '\t\t\tif (i + 1 == argc || !a || *a == ' + Q + ')\n\t\t\t\tclient_usage(3, argv[i]);'
WA = (WA_OLD, '\t\t\tif (i + 1 == argc || !a)\n\t\t\t\tclient_usage(3, argv[i]);\n\t\t\tif (*a == ' + Q + ')\n\t\t\t\tclient_usage(3, argv[i]);')
# (name, blocks, edits); help variants are exclusive
SHAPES = [('h1', 1, [(R.H, R.H1)]), ('h2', 2, [(R.H, R.H2)]), ('one', 1, [R.ONE]), ('wb', 1, [R.WB]),
          ('c', 1, [R.CSPL]), ('e', 1, [R.ESPL]), ('r', 1, [RA]), ('w', 1, [WA])]


def apply(t, combo):
    for _, _, eds in combo:
        for old, new in eds:
            if old not in t:
                return None
            t = t.replace(old, new, 1)
    return t


def main():
    a = sys.argv[1:]
    t = mc1lib.read_src(a[0])
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    want = [int(x) for x in a[a.index('-k') + 1].split(',')] if '-k' in a else None
    odir = a[a.index('-o') + 1] if '-o' in a else None
    todo = []
    for n in range(1, 5):
        for c in itertools.combinations(SHAPES, n):
            if sum(1 for s in c if s[0].startswith('h')) > 1:
                continue
            k = sum(s[1] for s in c)
            if want and k not in want:
                continue
            todo.append((k, '+'.join(s[0] for s in c), c))

    def one(it):
        k, nm, c = it
        x = apply(t, c)
        if x is None:
            return k, nm, None, None
        return k, nm, mc1lib.score_text(x, []), x
    with ThreadPoolExecutor(jobs) as ex:
        for k, nm, s, x in ex.map(one, todo):
            if s is None:
                print(k, nm, 'missing', flush=True)
                continue
            d = 0 if s.get('identical') else s.get('total', 99999)
            print(d, 'k%d' % k, nm, flush=True)
            if d == 0 and odir:
                os.makedirs(odir, exist_ok=True)
                open(os.path.join(odir, 'hit_%s.c' % nm), 'w', newline='\n').write(x)


if __name__ == '__main__':
    main()
