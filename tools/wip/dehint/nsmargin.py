"""python tools/wip/dehint/nsmargin.py <gen dir or files...>: return-0 block's align margin per source: branch - 4*fallthru (must be > 0)."""
import concurrent.futures as cf, glob, importlib.util, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nsret0


def margin(src):
    try:
        order, info, t = nsret0.run(src, [])
    except Exception as e:
        return src, None, str(e)[:100]
    best = max(order, key=lambda n: len(info[n][1]))
    fq = {n: info[n][0] or 0 for n in order}
    br = fa = 0.0
    parts = []
    for p, pc, fl in info[best][1]:
        if p == 'ENTRY':
            continue
        v = fq[int(p)] * float(pc) / 100
        if 'FALLTHRU,' in fl or fl.startswith('FALLTHRU'):
            fa += v
        else:
            br += v
        parts.append('%s:%d*%s' % (p, fq[int(p)], pc))
    return src, br - 4 * fa, 'b=%d f=%d %s' % (br, fa, ' '.join(parts))


def main():
    files = []
    for a in sys.argv[1:]:
        files += sorted(glob.glob(os.path.join(a, 'v*.c')), key=lambda x: int(re.search(r'v(\d+)', os.path.basename(x)).group(1))) if os.path.isdir(a) else [a]
    with cf.ThreadPoolExecutor(os.cpu_count() or 4) as ex:
        for s, m, d in ex.map(margin, files):
            print(os.path.basename(s), None if m is None else int(m), d)


if __name__ == '__main__':
    main()
