"""etog.py BASE.json : toggle E() (50% expect) on each option test of the loop chain, on top of
the edit set BASE; prints score/order per toggle (and pairs with env PAIRS=1)."""
import json, os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voc, ev
OPTS = ['-noenter", 8', '-reboot", 7', '-bp", 3', '-rb", 3', '-wb", 3', '-eb", 3', '-s", 2', '-keys", 5', '-ip", 3',
        '-r", 2', '-w", 2', '-e", 2', '-c", 2', '-i", 2', '-p", 2', '-v", 2']


def toggle(text, opt):
    a = '!strnicmp(argv[i], "%s)' % opt
    e = 'E(%s)' % a
    if e in text: return text.replace(e, a, 1)
    assert a in text, opt
    return text.replace(a, e, 1)


def edtext(edits, togs):
    t = voc.make(edits)
    for o in togs: t = toggle(t, o)
    return t


if __name__ == '__main__':
    base = json.load(open(sys.argv[1])) if os.path.exists(sys.argv[1]) else json.loads(sys.argv[1])
    combos = [(o,) for o in OPTS]
    if os.environ.get('PAIRS'): combos = list(itertools.combinations(OPTS, 2))
    for c in combos:
        r = ev.ev(edtext(base, c), 'etog')
        if r is None: print(c, 'ERR'); continue
        print(r['score'], r.get('fncmp'), c, ' '.join(map(str, r['o'][12:])), flush=True)
