"""mode_client attempt 7: subsets (size 1..K) of the 1-term feeds of mode_client removed,
each with/without the latch-flip toggle (mc7rev: `x = argv[++i]`) and with/without hc4
added to case 5's JMP(s4, c12) (the free list edit that compensated the c9 removal).

python tools/wip/dehint/mc7sub.py [-base FILE] [-k 3] [-j 4] [-o DIR]"""
import itertools, os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib, mc7rev

FEED = r' ?if \(__builtin_constant_p\((?:mode|i) \+ \d+\)\) goto \w+;'
ROK = 'JMP(s4, c12)'


def main():
    a = sys.argv[1:]
    base = mc1lib.read_src(a[a.index('-base') + 1] if '-base' in a else 'build/mc/w7/base63.c')
    K = int(a[a.index('-k') + 1]) if '-k' in a else 3
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    odir = a[a.index('-o') + 1] if '-o' in a else None
    s0 = base.index('int mode_client(')
    feeds = [(m.start() + s0, m.end() + s0, m.group(0).strip()) for m in re.finditer(FEED, base[s0:])]
    todo = []
    for k in range(1, K + 1):
        for sub in itertools.combinations(range(len(feeds)), k):
            t = base
            for i in sorted(sub, reverse=True):
                t = t[:feeds[i][0]] + t[feeds[i][1]:]
            for rv in (0, 1):
                for h in (0, 1):
                    x = mc7rev.rev(t) if rv else t
                    if h:
                        if ROK not in x:
                            continue
                        x = x.replace(ROK, 'JMP(s4, c12, hc4)')
                    nm = '+'.join(re.search(r'goto (\w+)', feeds[i][2]).group(1) + '@%d' % i for i in sub)
                    todo.append(('%s rev%d hc4%d' % (nm, rv, h), x))
    print(len(feeds), 'feeds', len(todo), 'variants', flush=True)
    res = []
    with ThreadPoolExecutor(jobs) as ex:
        for k, s, txt in ex.map(lambda it: (it[0], mc1lib.score_text(it[1]), it[1]), todo):
            if 'compile' in s:
                continue
            d = 0 if s['identical'] else s['total']
            if d == 0:
                print('HIT', k, mc1.count(txt)['total'], flush=True)
                if odir:
                    open(os.path.join(odir, 'sub_%s.c' % re.sub(r'\W', '_', k)), 'w', newline='\n').write(txt)
            res.append((d, k))
    res.sort()
    for d, k in res[:30]:
        print('  ', d, k)


if __name__ == '__main__':
    main()
