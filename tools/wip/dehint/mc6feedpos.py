"""mode_client attempt 6: replace a k-term cp feed by a shorter feed (1..K terms) into the
same target from another place in mode_client: a feed sends 1/2^k of its block's flow, so
a colder source with fewer terms can add the same frequency.

python tools/wip/dehint/mc6feedpos.py FEED_RX TARGET [-k 2] [-j 5] [-base FILE]
  FEED_RX: regex for the feed statement to remove (once) from the base
  Tries the shorter feed after every `;` / label colon of mode_client's body (positions
  that don't compile are skipped).  Prints the best results; IDENTICAL ones -> HIT."""
import os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib


def positions(text):
    s = text.index('int mode_client(')
    s = text.index('{', s) + 1
    e = text.index('\nconst char mc_rdpad')
    out = []
    for m in re.finditer(r';|(?<![:\w])\w+:(?!:)', text[s:e]):
        out.append(s + m.end())
    return out


def main():
    a = sys.argv[1:]
    rx, tgt = a[0], a[1]
    K = int(a[a.index('-k') + 1]) if '-k' in a else 2
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 5
    base = mc1lib.read_src(a[a.index('-base') + 1] if '-base' in a else mc1.BASE)
    t, n = re.subn(rx, '', base, count=1)
    assert n == 1, 'feed not found'
    c0 = mc1.count(t)['total']
    todo = []
    for p in positions(t):
        for k in range(1, K + 1):
            f = ' if (%s) goto %s;' % (' && '.join('__builtin_constant_p(mode + %d)' % (790000 + 10 * p + j)
                                                     for j in range(k)), tgt)
            todo.append(('@%d k%d %r' % (p, k, t[max(0, p - 30):p].replace('\n', ' ')), t[:p] + f + t[p:]))
    print(len(todo), 'variants, count', c0, '+ k', flush=True)

    def one(it):
        s = mc1lib.score_text(it[1])
        return it[0], s

    res = []
    with ThreadPoolExecutor(jobs) as ex:
        for name, s in ex.map(one, todo):
            if 'compile' in s:
                continue
            if s['identical']:
                print('HIT', name, flush=True)
                res.append((0, name))
            else:
                res.append((s['total'], name))
    res.sort()
    for d, nme in res[:15]:
        print('  ', d, nme)


if __name__ == '__main__':
    main()
