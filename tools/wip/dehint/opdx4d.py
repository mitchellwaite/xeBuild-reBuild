"""Attempt 4: dz3 (asm goto from the xellbutton log block, label + unreachable after dz2) with a
cheap feed (1-2 builtins) at any statement line of applyIniOptions.  Base build/op/nodx.c.
python tools/wip/dehint/opdx4d.py [asmpos]"""
import os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib, opdx4

C = '__builtin_constant_p(xb.blSuffix[1] + %d)'
FEEDS = {
    'c': 'if (%s) goto dz3;' % (C % 31),
    'e0': 'if (__builtin_expect(%s, 0)) goto dz3;' % (C % 31),
    'e1': 'if (__builtin_expect(%s, 1)) goto dz3;' % (C % 31),
    'cc': 'if (%s) { if (%s) goto dz3; }' % (C % 31, C % 32),
}


def variants(base, asmpos):
    t0 = opdx4.DZ3['dz3_last'](opdx4.ins(base, asmpos, 'dz3'))
    i = t0.find('void applyIniOptions(void)\n{')
    j = t0.find('\treturn;\n', i)
    lines = t0[i:j].split('\n')
    out = {}
    for k, l in enumerate(lines):
        if k < 4 or not l.strip() or l.strip().startswith(('/*', '*', '}', '{', 'else')) or l.rstrip().endswith('*/'):
            continue
        prev = lines[k - 1].rstrip()
        if not (prev.endswith(';') or prev.endswith('{') or prev.endswith('}') or prev.endswith('*/')):
            continue
        ind = l[:len(l) - len(l.lstrip('\t'))]
        for fn, f in FEEDS.items():
            nl = lines[:k] + [ind + f] + lines[k:]
            out['%03d:%s' % (k, fn)] = (t0[:i] + '\n'.join(nl) + t0[j:], l.strip()[:50])
    return out


def main():
    a = sys.argv[1:]
    base = optlib.read_src(os.path.join(optlib.BUILD, 'nodx.c'))
    vs = variants(base, a[0] if a else 'log_pre')
    with ThreadPoolExecutor(max(2, (os.cpu_count() or 4) - 1)) as p:
        rs = list(p.map(lambda kv: (kv[0], kv[1][1], optlib.score_text(kv[1][0])), vs.items()))
    rs.sort(key=lambda x: x[2].get('total', 10 ** 9))
    for n, l, r in rs[:int(os.environ.get('TOP', '30'))]:
        print('%-10s %-50s %s' % (n, l, optlib.fmt(r)))


if __name__ == '__main__':
    main()
