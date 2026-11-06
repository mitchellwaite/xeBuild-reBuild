"""mode_client attempt 14: every single trick removal (mc12rm's list) combined with k extra
vrp1 blocks from natural duplicated noreturn calls (an `||` test split into separate ifs
calling the same client_usage; PRE's tail merge folds the copies back, so they are live at
vrp1 and gone by RTL).  k = 0..4.

python tools/wip/dehint/mc14rmk.py BASE.c [-j 4] [-o DIR] [-k 0,1,2,3,4] [-only SUBSTR]"""
import os, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1lib, mc12vrp, mc12filt, mc12rm

U = '\t\t\tclient_usage(0, NULL);\n'
H = ('\t\tif (!strnicmp(argv[i], "help", 2) || !strnicmp(argv[i], "-?", 2) || !strnicmp(argv[i], "/?", 2))\n' + U)
H1 = ('\t\tif (!strnicmp(argv[i], "help", 2))\n' + U +
      '\t\tif (!strnicmp(argv[i], "-?", 2) || !strnicmp(argv[i], "/?", 2))\n' + U)
H2 = ('\t\tif (!strnicmp(argv[i], "help", 2))\n' + U + '\t\tif (!strnicmp(argv[i], "-?", 2))\n' + U +
      '\t\tif (!strnicmp(argv[i], "/?", 2))\n' + U)
Q = "'-'"
ONE = ('\tif (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == ' + Q + ')\n\t\tclient_usage(3, argv[i]);\n\tif (mode)\n\t\tclient_usage(5, argv[i]);\n\t*pi = i + 1;',
       '\tif (!argv[i + 1] || i + 1 == argc)\n\t\tclient_usage(3, argv[i]);\n\tif (*argv[i + 1] == ' + Q + ')\n\t\tclient_usage(3, argv[i]);\n\tif (mode)\n\t\tclient_usage(5, argv[i]);\n\t*pi = i + 1;')
WB = ('\tif (!b || j == argc || *b == ' + Q + ')\n\t\tclient_usage(4, argv[i]);',
      '\tif (!b || j == argc)\n\t\tclient_usage(4, argv[i]);\n\tif (*b == ' + Q + ')\n\t\tclient_usage(4, argv[i]);')


ARM = '\t\t} else if (!strnicmp(argv[i], "-c", 2)) {\n'
TST = '\t\t\tif (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == ' + Q + ')\n\t\t\t\tclient_usage(3, argv[i]);\n'
SPL = ('\t\t\tif (!argv[i + 1] || i + 1 == argc)\n\t\t\t\tclient_usage(3, argv[i]);\n'
       '\t\t\tif (*argv[i + 1] == ' + Q + ')\n\t\t\t\tclient_usage(3, argv[i]);\n')
CSPL = (ARM + TST, ARM + SPL)     # the -c arm
ESPL = (TST, SPL)                 # first such test: the -e arm


def add(t, k):
    """t with k extra vrp1 blocks (None if a shape is missing)."""
    steps = {0: [], 1: [(H, H1)], 2: [(H, H2)], 3: [(H, H2), ONE], 4: [(H, H2), ONE, WB],
             5: [(H, H2), ONE, WB, CSPL], 6: [(H, H2), ONE, WB, CSPL, ESPL]}[k]
    for old, new in steps:
        if old not in t:
            return None
        t = t.replace(old, new, 1)
    return t


def main():
    a = sys.argv[1:]
    t = mc1lib.read_src(a[0])
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    odir = a[a.index('-o') + 1] if '-o' in a else None
    ks = [int(x) for x in a[a.index('-k') + 1].split(',')] if '-k' in a else [0, 1, 2, 3, 4]
    only = a[a.index('-only') + 1] if '-only' in a else None
    vs = [v for v in mc12rm.variants(t) if not only or only in v[0]]
    jobsl = [(name, k, add(x, k)) for name, x in vs for k in ks]
    print(len(jobsl), 'variants', flush=True)

    def one(it):
        name, k, x = it
        if x is None:
            return name, k, None, None, None
        try:
            th = mc12vrp.threads(x)
        except Exception:
            th = []
        return name, k, th, mc1lib.score_text(x, []), x
    if odir:
        os.makedirs(odir, exist_ok=True)
    with ThreadPoolExecutor(jobs) as ex:
        for name, k, th, s, x in ex.map(one, jobsl):
            if s is None:
                print('missing', k, name, flush=True)
                continue
            d = 0 if s.get('identical') else s.get('total', 99999)
            print(d, k, 'GOOD' if th and mc12filt.good(th) else 'bad ', ','.join(z for _, _, z in th), name, flush=True)
            if d == 0 and odir:
                open(os.path.join(odir, 'hit_%d_%s.c' % (k, name.split()[0].replace('@', '_'))), 'w', newline='\n').write(x)


if __name__ == '__main__':
    main()
