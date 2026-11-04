"""python tools/wip/dehint/iw20climb.py <base.c> <out_prefix> [first] [last] [threads] [rounds]: hill climb over the single options of gen_iw<first..last> (each option applied alone when all its
search strings are in the current text). Options that add a hint (asm, __builtin, attribute, hot/cold labels) are skipped; dead tests aren't detectable, so read the result. Each round runs every applicable
option, then applies the best improver (by total lines, then fewer functions off) and repeats. Writes <out_prefix>_<lines>.c per accepted step, <out_prefix>_0.c on a match, and logs labels to <out_prefix>.log."""
import hashlib, importlib.util, os, re, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib
here = os.path.dirname(os.path.abspath(__file__))
BAD = re.compile(r'__asm__|asm\s*\(|__builtin|__attribute__|\bhot\b|\bcold\b|unreachable|no-|partial\s*(>|<=|>=|<)|\bif \(left')


def moves(first, last):
    ms = []
    seen = set()
    for n in range(last, first - 1, -1):
        p = os.path.join(here, 'gen_iw%d.py' % n)
        if not os.path.exists(p):
            continue
        try:
            sp = importlib.util.spec_from_file_location('g', p)
            m = importlib.util.module_from_spec(sp)
            sp.loader.exec_module(m)
            axes = m.AXES
        except BaseException:
            continue
        for ax in axes:
            try:
                for o in ax:
                    if not o[1]:
                        continue
                    k = repr(o[1])
                    new = ''.join(b for a, b in o[1])
                    old = ''.join(a for a, b in o[1])
                    # a move that adds an `if` is usually a dead test; they've been the bulk of the old generators
                    if k in seen or BAD.search(new) or new.count('if (') > old.count('if (') or new.count('? ') > old.count('? ') + 1:
                        continue
                    seen.add(k)
                    ms.append((n, o[0], o[1]))
            except Exception:
                pass
    return ms


def apply(t, ed):
    for a, b in ed:
        if a not in t:
            return None
        t = t.replace(a, b)
    return t


def main():
    a = sys.argv[1:]
    base, pre = a[0], a[1]
    first = int(a[2]) if len(a) > 2 else 100
    last = int(a[3]) if len(a) > 3 else 400
    th = int(a[4]) if len(a) > 4 else 4
    rounds = int(a[5]) if len(a) > 5 else 8
    text = open(base, newline='').read().replace('\r\n', '\n')
    ms = moves(first, last)
    log = open(pre + '.log', 'a', newline='\n')
    ex = ThreadPoolExecutor(th)
    score = lambda t: iwlib.score_text(t, [])
    cur = score(text)
    log.write('start %s, %d moves\n' % (iwlib.fmt(cur)[:150], len(ms)))
    log.flush()
    seen = {hashlib.md5(text.encode()).hexdigest()}
    for rd in range(rounds):
        jobs = []
        for n, lab, ed in ms:
            t = apply(text, ed)
            if t is None or t == text:
                continue
            h = hashlib.md5(t.encode()).hexdigest()
            if h in seen:
                continue
            seen.add(h)
            jobs.append((n, lab, t))
        res = []
        allf = open('%s_r%d.txt' % (pre, rd), 'w', newline='\n')
        for j, r in ex.map(lambda j: (j, score(j[2])), jobs):
            if 'compile' in r:
                continue
            res.append((r.get('total', 0), len(r.get('per', {})), j[0], j[1], j[2], r))
            allf.write('%d gen%d %s %s\n' % (r.get('total', 0), j[0], j[1], r.get('per', {})))
            allf.flush()
            if r.get('total', 1) == 0:
                open(pre + '_0_%d.c' % j[0], 'w', newline='\n').write(j[2])
        allf.close()
        res.sort(key=lambda x: x[:2])
        log.write('round %d: %d jobs; top %s\n' % (rd, len(jobs), [(x[0], x[2], x[3]) for x in res[:8]]))
        log.flush()
        if not res:
            break
        b = res[0]
        if b[0] == 0:
            open(pre + '_0.c', 'w', newline='\n').write(b[4])
            log.write('ZERO gen%d %s\n' % (b[2], b[3]))
            log.flush()
            break
        if (b[0], b[1]) >= (cur.get('total', 1 << 30), len(cur.get('per', {}))):
            break
        text = b[4]
        cur = b[5]
        open('%s_%d.c' % (pre, b[0]), 'w', newline='\n').write(text)
        log.write('accept %d gen%d %s %s\n' % (b[0], b[2], b[3], iwlib.fmt(b[5])[:150]))
        log.flush()
        # greedy: the other improvers of this round, each kept if it still improves
        for x in res[1:40]:
            if x[0] >= res[0][0] + 60:
                break
            ed = next((m[2] for m in ms if m[0] == x[2] and m[1] == x[3]), None)
            t2 = apply(text, ed) if ed else None
            if t2 is None or t2 == text:
                continue
            r2 = score(t2)
            if 'compile' not in r2 and (r2.get('total', 0), len(r2.get('per', {}))) < (cur['total'], len(cur['per'])):
                text = t2
                cur = r2
                open('%s_%d.c' % (pre, r2['total']), 'w', newline='\n').write(text)
                log.write('greedy %d gen%d %s %s\n' % (r2['total'], x[2], x[3], iwlib.fmt(r2)[:150]))
                log.flush()
                if r2['total'] == 0:
                    open(pre + '_0.c', 'w', newline='\n').write(text)
                    log.write('ZERO\n')
                    log.close()
                    return
    log.write('done\n')
    log.close()


main()
