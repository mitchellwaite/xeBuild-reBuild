"""Attempt 4: for each removal R (optricks), rewrite the two rev feeds' dead arms with
control-flow statements only (return / goto dz1 / goto dz2, no new builtins) and score.
python tools/wip/dehint/opret4b.py [R..]"""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib, optricks, opret4

C, E0 = opret4.C, opret4.E0
F1, F2 = opret4.F1, opret4.F2
I1 = 'if (%s) goto dz1;' % E0(2)
I2 = 'if (%s) goto dz2;' % E0(16)
ST = ['', 'return;', 'goto dz1;', 'goto dz2;']


def f1s():
    out = {}
    for a, b in itertools.product(ST, ST):
        if b == 'goto dz1;' or a in ('return;', 'goto dz1;', 'goto dz2;') and a == b:
            pass
        body = ' '.join(x for x in (a, I1, b) if x)
        out['1[%s|%s]' % (a, b)] = 'if (%s) { %s }' % (C(1), body)
    return out


def f2s():
    out = {}
    for a, b in itertools.product(ST, ST):
        body = ' '.join(x for x in (a, I2, b) if x)
        out['2[%s|%s]' % (a, b)] = 'if (%s) { %s }' % (E0(15), body)
    return out


def main():
    rs = sys.argv[1:] or ['', 'mG_cygnos', 'mG_smcne', 'mG_nosec', 'mG_nandmu', 'G_exp', 'bx_z', 'N_exp', 'm_N']
    base = optricks.base()
    jobs = []
    for r in rs:
        b0, got = optricks.apply(base, [r] if r else [])
        for n1, v1 in f1s().items():
            for n2, v2 in f2s().items():
                t = b0.replace(F1, v1).replace(F2, v2)
                jobs.append(('%s %s %s' % (r or '-', n1, n2), t))
    with ThreadPoolExecutor(max(2, (os.cpu_count() or 4) - 1)) as p:
        res = list(p.map(lambda j: (j[0], optlib.score_text(j[1])), jobs))
    res.sort(key=lambda x: x[1].get('total', 10 ** 9))
    for n, r in res[:int(os.environ.get('TOP', '30'))]:
        print('%-60s %s' % (n, optlib.fmt(r)))


if __name__ == '__main__':
    main()
