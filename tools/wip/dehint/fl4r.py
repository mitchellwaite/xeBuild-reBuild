"""fl4r.py <tests> [extra]: from fl4f's base with <tests>, one more dead test before each statement of parseIni's bl..[security] code.
With a second argument 'pair N seed': N random pairs of extra tests."""
import random, re, sys
import fllib as L, fl4lib as F, fl4g as G

CONDS = ['off < -1', 'pos < 0', 'size < 0', 'buf == NULL']
ARMS = ['*buf = 0']


def sites(s):
    a = s.index('sprintf(label, "[%sbl%s]"')
    b = s.index('log_printf(1, "------ ini parsing completed')
    out = []
    k = a
    while True:
        k = s.find('\n', k)
        if k < 0 or k >= b:
            break
        k += 1
        ln = s[k:s.find('\n', k)]
        m = re.match(r'(\t+)(\w.*)$', ln)
        if not m:
            continue
        t = m.group(2)
        if t.startswith(('else', 'case', 'free(buf)', 'return')):
            continue
        # after an `if (...)` without a brace or `else` the next line is its body
        prev = s[s.rfind('\n', 0, k - 1) + 1:k - 1].strip()
        if prev.endswith(')') and prev.startswith(('if', 'for', 'else if')) or prev == 'else':
            continue
        if prev.endswith(';') and prev.startswith('} else') :
            continue
        out.append((k, m.group(1)))
    return out


def ins(s, k, ind, cond, arm):
    return s[:k] + '%sif (%s) {\n%s\t%s;\n%s}\n' % (ind, cond, ind, arm, ind) + s[k:]


if __name__ == '__main__':
    tl = sys.argv[1]
    base = G.mk(F.st(tl))
    ss = sites(base)
    print(len(ss), 'sites')
    V = {}
    if len(sys.argv) > 2:
        N, seed = int(sys.argv[3]), int(sys.argv[4])
        rng = random.Random(seed)
        while len(V) < N:
            ps = sorted(rng.sample(range(len(ss)), 2), reverse=True)
            cs = [rng.choice(CONDS[:3]) for _ in ps]
            s = base
            for p, c in zip(ps, cs):
                s = ins(s, ss[p][0], ss[p][1], c, ARMS[0])
            V['%s@%d %s@%d' % (cs[0], ps[0], cs[1], ps[1])] = s
    else:
        for i, (k, ind) in enumerate(ss):
            for c in CONDS:
                V['%d %s' % (i, c)] = ins(base, k, ind, c, ARMS[0])
    print(len(V))
    F.run(V, 'r', show=20)
