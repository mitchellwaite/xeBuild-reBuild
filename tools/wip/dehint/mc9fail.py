"""mode_client attempt 9: fail's feeds in every order, each before or after the log call.

On the 4-line near miss (dtg2 feed gone) the last feed before fail's log gets the call
heuristic (71%) instead of 50%; this sweeps which feed sits there (count-neutral).

python tools/wip/dehint/mc9fail.py BASE.c [-j 6] [-o OUT.c] [-extra 'if (...) goto X;' ...]"""
import itertools, os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1lib

FEED = re.compile(r' ?if \(__builtin_constant_p\([^;]*\)\) goto \w+;')


def split(t):
    s = t.index('fail: __attribute__((cold));')
    e = t.index('\n', s)
    head = 'fail: __attribute__((cold));'
    feeds = [m.group(0).strip() for m in FEED.finditer(t[s:e])]
    k = t.index('ERROR: unable to connect', e)
    ls = t.rindex('\tlog_printf', 0, k)
    le = t.index('\n', k) + 1
    log = t[ls:le]
    r = t.index('\treturn 0;\n', le)
    for line in t[le:r].split('\n'):
        if line.strip():
            assert FEED.fullmatch(' ' + line.strip()), line
            feeds.append(line.strip())
    return t[:s], feeds, log, t[r:]


def render(pre, before, log, after, post):
    out = pre + 'fail: __attribute__((cold));' + ''.join(' ' + f for f in before) + '\n' + log
    for f in after:
        out += '\t' + f + '\n'
    return out + post


def main():
    a = sys.argv[1:]
    t = mc1lib.read_src(a[0])
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 6
    pre, feeds, log, post = split(t)
    extra = [a[i + 1] for i, x in enumerate(a) if x == '-extra']
    feeds = feeds + extra
    vs = {}
    for perm in itertools.permutations(range(len(feeds))):
        for cut in range(len(feeds) + 1):
            b = [feeds[i] for i in perm[:cut]]
            af = [feeds[i] for i in perm[cut:]]
            key = ' '.join(re.search(r'goto (\w+)', f).group(1) + str(i) for i, f in zip(perm, b + af))
            key = '%s | %s' % (' '.join(re.search(r'goto (\w+)', f).group(1) for f in b),
                               ' '.join(re.search(r'goto (\w+)', f).group(1) for f in af))
            txt = render(pre, b, log, af, post)
            vs.setdefault(txt, key + '  perm=' + ''.join(map(str, perm)) + ' cut=%d' % cut)
    items = list(vs.items())
    print(len(items), 'variants', file=sys.stderr)
    with ThreadPoolExecutor(jobs) as ex:
        res = list(ex.map(lambda v: (v[1], mc1lib.score_text(v[0]), v[0]), items))
    res.sort(key=lambda r: -1 if r[1].get('identical') else r[1].get('total', 99999))
    for n, s, txt in res[:25]:
        print(mc1lib.fmt(s)[:60], '::', n)
    if res and res[0][1].get('identical') and '-o' in a:
        open(a[a.index('-o') + 1], 'w', newline='\n').write(res[0][2])


if __name__ == '__main__':
    main()
