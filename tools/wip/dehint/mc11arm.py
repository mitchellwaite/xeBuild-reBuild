"""mode_client attempt 11: a mode-chain arm removed and replaced by one k-term goto feed to
its case label (`if (cp && ...) goto c11;`) at every position of mode_client.

The arm `if (cp...) mode = 11; else` threads into case 11 through the switch; a direct goto
feed with fewer terms than the arm is a gain.  Plain -O3 scoring.

python tools/wip/dehint/mc11arm.py BASE.c -arm 11 -t c11[,L2] [-k 1,2,3] [-j 4] [-o DIR]"""
import os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib, mc7reloc

CP = r'__builtin_constant_p\(mode \+ \d+\)'


def drop_arm(t, arm):
    m = re.search(r'(?:else )?if \(' + CP + r'(?: && ' + CP + r')*\) mode = %d;(?: else)?' % arm, t)
    assert m, arm
    s = m.group(0)
    # keep the chain's else structure: drop "if (...) mode = N; else " or " else if (...) mode = N;"
    if s.startswith('else ') and s.endswith(' else'):
        rep = 'else'
    elif s.endswith(' else'):
        rep = ''
    else:
        rep = ''
    t2 = t[:m.start()] + rep + t[m.end():]
    t2 = t2.replace('else  switch', ' switch').replace('else switch', 'switch')
    return re.sub(r'mode = (\d+); switch', r'mode = \1; switch', t2)


def main():
    a = sys.argv[1:]
    t = mc1lib.read_src(a[0])
    arm = int(a[a.index('-arm') + 1])
    tg = a[a.index('-t') + 1].split(',')
    ks = [int(x) for x in (a[a.index('-k') + 1] if '-k' in a else '1').split(',')]
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    odir = a[a.index('-o') + 1] if '-o' in a else None
    b = drop_arm(t, arm)
    s0 = mc1lib.score_text(b, [])
    print('arm %d dropped: count %d, %s' % (arm, mc1.count(b)['total'], mc1lib.fmt(s0)[:80]), flush=True)
    todo = []
    for lab in tg:
        for p in mc7reloc.positions(b, 'mode_client'):
            for k in ks:
                cond = ' && '.join('__builtin_constant_p(mode + %d)' % (800000 + 10 * p + j) for j in range(k))
                todo.append(('%s@%d k%d' % (lab, p, k), b[:p] + ' if (%s) goto %s;' % (cond, lab) + b[p:], p))
    print(len(todo), 'variants', flush=True)
    with ThreadPoolExecutor(jobs) as ex:
        res = list(ex.map(lambda it: (it[0], mc1lib.score_text(it[1], []), it[1], it[2]), todo))
    rows = sorted((0 if s.get('identical') else s.get('total', 99999), n, x, p) for n, s, x, p in res)
    for d, n, x, p in rows[:15]:
        print(d, n, mc1.count(x)['total'], repr(b[max(0, p - 60):p]), flush=True)
    if odir:
        os.makedirs(odir, exist_ok=True)
        for d, n, x, p in rows[:5]:
            open(os.path.join(odir, 'arm%d_%s.c' % (arm, re.sub(r'\W+', '_', n))), 'w', newline='\n').write(x)


if __name__ == '__main__':
    main()
