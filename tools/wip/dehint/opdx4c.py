"""Attempt 4: dx replaced by one asm goto (no feed) placed before any statement line of
applyIniOptions, to dz1, dz2 or a new dz3 (+ unreachable after dz2).  Base build/op/nodx.c.
python tools/wip/dehint/opdx4c.py [base.c] [-k]"""
import os, re, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib, opdx4

AG = '__asm__ goto ("" :::: %s);'


def variants(base, labels=('dz1', 'dz2', 'dz3')):
    i = base.find('void applyIniOptions(void)\n{')
    j = base.find('\treturn;\n', i)
    lines = base[i:j].split('\n')
    out = {}
    for k, l in enumerate(lines):
        if k < 4 or not l.strip() or l.strip().startswith(('/*', '*', '}', '{', 'else')) or l.rstrip().endswith('*/'):
            continue
        prev = lines[k - 1].rstrip()
        # only at statement starts: previous line ends a statement or opens a block
        if not (prev.endswith(';') or prev.endswith('{') or prev.endswith('}') or prev.endswith('*/')):
            continue
        ind = l[:len(l) - len(l.lstrip('\t'))]
        for lab in labels:
            nl = lines[:k] + [ind + AG % lab] + lines[k:]
            t = base[:i] + '\n'.join(nl) + base[j:]
            if lab == 'dz3':
                t = opdx4.DZ3['dz3_last'](t)
            out['%03d:%s' % (k, lab)] = (t, l.strip()[:50])
    return out


def main():
    a = [x for x in sys.argv[1:] if not x.startswith('-')]
    base = optlib.read_src(a[0] if a else os.path.join(optlib.BUILD, 'nodx.c'))
    vs = variants(base)
    with ThreadPoolExecutor(max(2, (os.cpu_count() or 4) - 1)) as p:
        rs = list(p.map(lambda kv: (kv[0], kv[1][1], optlib.score_text(kv[1][0])), vs.items()))
    rs.sort(key=lambda x: x[2].get('total', 10 ** 9))
    for n, l, r in rs[:int(os.environ.get('TOP', '30'))]:
        print('%-10s %-50s %s' % (n, l, optlib.fmt(r)))
    if '-k' in sys.argv:
        for n, l, r in rs[:3]:
            open(os.path.join(optlib.BUILD, 'dx4c_%s.c' % n.replace(':', '_')), 'w', newline='\n').write(vs[n][0])


if __name__ == '__main__':
    main()
