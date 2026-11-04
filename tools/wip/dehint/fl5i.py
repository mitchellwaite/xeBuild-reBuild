"""fl5i.py <fl5f label> [conds]: one more dead test before each statement of parseIni's code from the bl section on, at an fl5f state."""
import re, sys
import fllib as L, fl5lib as F, fl5f as X, fl5g as G

CONDS = ['off < -1', 'off < 0', 'pos < 0', 'size < 0']
ARMS = ['*buf = 0', '*buf = 0;\n@\tbuf[size] = 0']


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
        prev = s[s.rfind('\n', 0, k - 1) + 1:k - 1].strip()
        if prev.endswith(')') and prev.startswith(('if', 'for', 'else if')) or prev == 'else':
            continue
        out.append((k, m.group(1)))
    return out


def ins(s, k, ind, cond, arm):
    return s[:k] + '%sif (%s) {\n%s\t%s;\n%s}\n' % (ind, cond, ind, arm.replace('@', ind), ind) + s[k:]


if __name__ == '__main__':
    base = X.gen(*G.parse(sys.argv[1]))
    ss = sites(base)
    V = {}
    for i, (k, ind) in enumerate(ss):
        for c in CONDS:
            for j, a in enumerate(ARMS):
                V['%d %s %d' % (i, c, j)] = ins(base, k, ind, c, a)
    print(len(ss), len(V))
    F.run(V, 'i', show=14)
