"""mode_client attempt 12: every single trick removal (feeds, JMP statements, cold labels,
__builtin_unreachable calls, if (0) blocks) on a base, with vrp1's thread order and the score.
Shows which removals shift the block count (the switch-thread hash order, mc12vrp).

python tools/wip/dehint/mc12rm.py BASE.c [-j 4] [-o DIR]"""
import os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1lib, mc12vrp, mc12filt

PATS = [
    ('feed', r' ?if \(__builtin_constant_p\([^()]*\)\) goto \w+;', ''),
    ('jmp', r' ?JMP\([^)]*\);', ''),
    ('cold', r'(\w+): __attribute__\(\(cold\)\);', r'\1:;'),
    ('unr', r'__builtin_unreachable\(\);', ';'),
    ('if0', r'if \(0\) \{ \w+: __builtin_unreachable\(\); \} ?', ''),
]


def variants(t):
    s0 = t.index('static void clientEraseBlockI(')
    out = []
    for kind, rx, rep in PATS:
        for m in re.finditer(rx, t):
            if m.start() < s0:
                continue
            new = re.sub(rx, rep, m.group(0))
            out.append(('%s@%d %s' % (kind, m.start(), m.group(0).strip()[:50]), t[:m.start()] + new + t[m.end():]))
    return out


def main():
    a = sys.argv[1:]
    t = mc1lib.read_src(a[0])
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    odir = a[a.index('-o') + 1] if '-o' in a else None
    vs = variants(t)
    print(len(vs), 'removals', flush=True)

    def one(it):
        try:
            th = mc12vrp.threads(it[1])
        except Exception:
            th = []
        return it[0], th, mc1lib.score_text(it[1], []), it[1]
    with ThreadPoolExecutor(jobs) as ex:
        res = list(ex.map(one, vs))
    rows = sorted(((0 if s.get('identical') else s.get('total', 99999)), k, th, x) for k, th, s, x in res)
    for d, k, th, x in rows:
        print(d, 'GOOD' if th and mc12filt.good(th) else 'bad ', ','.join(z for _, _, z in th), k, flush=True)
    if odir:
        os.makedirs(odir, exist_ok=True)
        for n, (d, k, th, x) in enumerate(rows[:3]):
            open(os.path.join(odir, 'rm_%d_%d.c' % (n, d)), 'w', newline='\n').write(x)


if __name__ == '__main__':
    main()
