"""mode_client attempt 9: a new plain label in the source plus that label added to one
asm goto list (start or end), or a new 1-term feed to it.

The 4-line near miss (drafts/mode_client_a8_near4.c) swaps c9/c11 because fail's last
feed (now c11's) gets the call heuristic (71%: its else block, the log, is dominated and
calls log_printf).  A second predecessor of the log block undoes the dominance.

python tools/wip/dehint/mc9flog.py BASE.c [-at REGEX] [-lab NAME] [-feeds] [-j 4]
  -at: regex whose match start is where `NAME: ` goes (default: fail's log_printf)"""
import os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1lib, mc7j2l


def variants(t, lab, at):
    m = re.search(at, t)
    assert m, at
    t = t[:m.start()] + lab + ': ' + t[m.start():]
    out = [('label-only', t)]
    for j, o in enumerate(mc7j2l.stmts(t)):
        if o[0] != 'mc':
            continue
        out.append(('%d.s %s' % (j, o[5][:3]), mc7j2l.apply(t, [(o[3], o[3], lab + ', ')])))
        out.append(('%d.e %s' % (j, o[5][:3]), mc7j2l.apply(t, [(o[4], o[4], ', ' + lab)])))
    return out


def main():
    a = sys.argv[1:]
    base = mc1lib.read_src(a[0])
    lab = a[a.index('-lab') + 1] if '-lab' in a else 'flog'
    at = a[a.index('-at') + 1] if '-at' in a else r'log_printf\(0, "\\n\\n\*\*\*\*\* ERROR: unable to connect'
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    vs = variants(base, lab, at)
    with ThreadPoolExecutor(jobs) as ex:
        res = list(ex.map(lambda v: (v[0], mc1lib.score_text(v[1]), v[1]), vs))
    for n, s, t in sorted(res, key=lambda r: r[1].get('total', 99999) if not r[1].get('identical') else -1):
        print(n, mc1lib.fmt(s))
        if s.get('identical') and '-o' in a:
            open(a[a.index('-o') + 1], 'w', newline='\n').write(t)


if __name__ == '__main__':
    main()
