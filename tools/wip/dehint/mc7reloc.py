"""mode_client attempt 7: generic relocation.  Remove one or more constructs (regexes, each
once) from the base and insert ONE statement built from a template at every position
(after each `;` / label colon) of a function; report IDENTICAL hits.

python tools/wip/dehint/mc7reloc.py -rm RX [-rm RX ...] -ins TEMPLATE [-k 1,2] [-fn NAME]
       [-var mode] [-base FILE] [-j 4] [-o OUT.c]
  TEMPLATE: the statement, `{cp}` is replaced by k terms `__builtin_constant_p(VAR + N)`
            joined with ` && ` (e.g. 'if ({cp}) goto ndl;' or 'if ({cp}) mode = 7;')
  -fn: mode_client (default) or clientEraseBlockI (positions inside that body)
  -o:  write the hit nearest the first removed construct to OUT.c"""
import os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib

ENDS = {'mode_client': '\nconst char mc_rdpad', 'clientEraseBlockI': '\n}\n'}


def positions(text, fn):
    s = text.index(('int ' if fn == 'mode_client' else 'static void ') + fn + '(')
    s = text.index('{', s) + 1
    e = text.index(ENDS[fn], s)
    return [s + m.end() for m in re.finditer(r';|(?<![:\w])\w+:(?!:)', text[s:e])]


def args(a, k, d=None, many=False):
    if many:
        return [a[i + 1] for i, x in enumerate(a) if x == k]
    return a[a.index(k) + 1] if k in a else d


def main():
    a = sys.argv[1:]
    rms = args(a, '-rm', many=True)
    tpl = args(a, '-ins')
    ks = [int(x) for x in args(a, '-k', '1').split(',')]
    fn = args(a, '-fn', 'mode_client')
    var = args(a, '-var', 'mode' if fn == 'mode_client' else 'block')
    jobs = int(args(a, '-j', '4'))
    out = args(a, '-o')
    t = mc1lib.read_src(args(a, '-base', mc1.BASE))
    near = None
    for rx in rms:
        m = re.search(rx, t)
        assert m, 'not found: ' + rx
        if near is None:
            near = m.start()
        t = t[:m.start()] + t[m.end():]
    near = near or 0
    c0 = mc1.count(t)['total']
    todo = []
    for p in positions(t, fn):
        for k in ks:
            cp = ' && '.join('__builtin_constant_p(%s + %d)' % (var, 700000 + 10 * p + j) for j in range(k))
            st = ' ' + tpl.replace('{cp}', cp)
            todo.append((p, k, t[:p] + st + t[p:]))
    print(len(todo), 'variants; count without insert', c0, flush=True)

    def one(it):
        return it[0], it[1], mc1lib.score_text(it[2]), it[2]

    res = []
    with ThreadPoolExecutor(jobs) as ex:
        for p, k, s, txt in ex.map(one, todo):
            if 'compile' in s:
                continue
            ctx = t[max(0, p - 40):p].replace('\n', ' ')
            if s['identical']:
                print('HIT @%d k%d count %d %r' % (p, k, mc1.count(txt)['total'], ctx), flush=True)
                res.append((0, abs(p - near), p, k, txt))
            else:
                res.append((s['total'], abs(p - near), p, k, None))
    res.sort(key=lambda r: r[:2])
    for d, _, p, k, _ in res[:12]:
        print('  ', d, '@%d k%d' % (p, k), repr(t[max(0, p - 40):p].replace('\n', ' ')))
    hits = [r for r in res if r[0] == 0]
    if hits and out:
        open(out, 'w', newline='\n').write(hits[0][4])
        print('wrote', out, 'count', mc1.count(hits[0][4])['total'])


if __name__ == '__main__':
    main()
