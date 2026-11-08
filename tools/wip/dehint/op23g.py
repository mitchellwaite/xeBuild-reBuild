#!/usr/bin/env python3
"""Attempt 23: the rev feeds (dz1/dz2's dead feeds) as structures x test forms.

python tools/wip/dehint/op23g.py [-m] [-max N] [-show] STRUCT[:f1,f2,..] ..
  STRUCT names a template in S (tests {t1}..{tk}); forms per test from FORMS (default: all
  combinations of FORMS_DEFAULT, k tests).  Prints score, dz counts and the tricks the feed
  costs (cp tests + expects).  -max N: only report scores <= N.  -c C: only costs < C (default 7).  -f a,b: forms.  -show: print the feed text."""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib
import op23

NUM = [1, 2, 15, 16, 17, 18]
FORMS = {'p': '{x}', 'lt': '{x} < 0', 'eq': '{x} == 5', 'gt': '{x} > 0', 'ne': '{x} != 5',
         'e': '__builtin_expect({x}, 0)', 'e1': '__builtin_expect({x}, 1)', 'n': '!{x}'}
FORMS_DEFAULT = ['p', 'lt', 'eq', 'gt', 'e']
I = '\t\t\t'
# templates: the current one, dz2's test split between both dummies (noreturn on both of its
# edges cancels, so it needs no expect), and the dz2 feed first
S = {
    'cur': I + 'if ({t1}) {{ if ({t2}) goto dz1; return; }}\n' + I + 'if ({t3}) {{ if ({t4}) goto dz2; }}\n',
    'dd1': I + 'if ({t1}) {{ if ({t2}) goto dz1; return; }}\n' + I + 'if ({t3}) {{ if ({t4}) goto dz1; goto dz2; }}\n',
    'dd2': I + 'if ({t1}) {{ if ({t2}) goto dz1; return; }}\n' + I + 'if ({t3}) {{ if ({t4}) goto dz2; goto dz1; }}\n',
    'rv1': I + 'if ({t1}) {{ if ({t2}) goto dz1; goto dz2; }}\n' + I + 'if ({t3}) {{ if ({t4}) goto dz1; return; }}\n',
    'rv2': I + 'if ({t1}) {{ if ({t2}) goto dz2; goto dz1; }}\n' + I + 'if ({t3}) {{ if ({t4}) goto dz1; return; }}\n',
    # three tests: one split test under two natural ones
    'tri1': I + 'if ({t1}) {{ if ({t2}) {{ if ({t3}) goto dz1; goto dz2; }} }}\n',
    'tri2': I + 'if ({t1}) {{ if ({t2}) {{ if ({t3}) goto dz2; goto dz1; }} }}\n',
    # four tests: two natural, a split, one more natural level
    'q1': I + 'if ({t1}) {{ if ({t2}) {{ if ({t3}) {{ if ({t4}) goto dz1; goto dz2; }} }} }}\n',
    'q2': I + 'if ({t1}) {{ if ({t2}) {{ if ({t3}) {{ if ({t4}) goto dz2; goto dz1; }} }} }}\n',
    # a split test with a natural test on one arm
    'sp1': I + 'if ({t1}) {{ if ({t2}) {{ if ({t3}) goto dz1; goto dz2; }} goto dz1; }}\n',
    'sp2': I + 'if ({t1}) {{ if ({t2}) {{ if ({t3}) goto dz2; goto dz1; }} goto dz1; }}\n',
    'sp3': I + 'if ({t1}) {{ if ({t2}) goto dz1; if ({t3}) goto dz1; goto dz2; }}\n',
    'sp4': I + 'if ({t1}) {{ if ({t2}) goto dz1; if ({t3}) goto dz2; goto dz1; }}\n',
    # attempt 23's first match (dd2 with B plain: B's edge to dz1 is noreturn 0%) reduced
    'ar': I + 'if ({t1}) return;\n' + I + 'if ({t2}) {{ if ({t3}) goto dz2; goto dz1; }}\n',
    'ar1': I + 'if ({t1}) return;\n' + I + 'if ({t2}) {{ if ({t3}) goto dz1; goto dz2; }}\n',
    'ae': I + 'if ({t1}) {{ if ({t2}) {{ if ({t3}) goto dz2; goto dz1; }} }}\n',
    'ae1': I + 'if ({t1}) {{ if ({t2}) {{ if ({t3}) goto dz1; goto dz2; }} }}\n',
    'a2': I + 'if ({t1}) {{ if ({t2}) goto dz2; goto dz1; }}\n',
    'a21': I + 'if ({t1}) {{ if ({t2}) goto dz1; goto dz2; }}\n',
    'ab': I + 'if ({t1}) {{ if ({t2}) goto dz1; return; }}\n' + I + 'if ({t3}) {{ if ({t4}) goto dz2; goto dz1; }}\n',
    # the dz1 feed with its return, then a split feed
    'r3a': I + 'if ({t1}) {{ if ({t2}) goto dz1; return; }}\n' + I + 'if ({t3}) {{ if ({t4}) {{ if ({t5}) goto dz1; goto dz2; }} }}\n',
    'r3b': I + 'if ({t1}) {{ if ({t2}) goto dz1; return; }}\n' + I + 'if ({t3}) {{ if ({t4}) {{ if ({t5}) goto dz2; goto dz1; }} }}\n',
}


def text(st, forms):
    k = S[st].count('{t')
    assert len(forms) == k, (st, forms)
    d = {}
    for i, f in enumerate(forms):
        d['t%d' % (i + 1)] = FORMS[f].format(x=op23.X(NUM[i]))
    return S[st].format(**d)


def cost(forms):
    return len(forms) + sum(1 for f in forms if f in ('e', 'e1'))


def run(st, forms, m):
    t = op23.SRC.replace(op23.FEED, text(st, forms), 1)
    r = optlib.score_text(t, optlib.P83)
    mm = op23.metric(t, optlib.P83) if m else ''
    return st, forms, r, mm


def main():
    a = sys.argv[1:]
    m = '-m' in a
    if m:
        a.remove('-m')
    show = '-show' in a
    if show:
        a.remove('-show')
    mx = None
    if '-max' in a:
        i = a.index('-max'); mx = int(a[i + 1]); del a[i:i + 2]
    cmax = 7
    if '-c' in a:
        i = a.index('-c'); cmax = int(a[i + 1]); del a[i:i + 2]
    fd = FORMS_DEFAULT
    if '-f' in a:
        i = a.index('-f'); fd = a[i + 1].split(','); del a[i:i + 2]
    jobs = []
    for spec in a:
        st, _, fs = spec.partition(':')
        k = S[st].count('{t')
        if fs:
            jobs.append((st, fs.split(',')))
        else:
            for c in itertools.product(fd, repeat=k):
                if cost(c) < cmax:
                    jobs.append((st, list(c)))
    with ThreadPoolExecutor(6) as ex:
        for st, forms, r, mm in ex.map(lambda j: run(j[0], j[1], m), jobs):
            sc = 0 if r.get('identical') else r.get('total', 99999)
            if mx is not None and sc > mx:
                continue
            print('%-5s %-20s cost %d  %s %s' % (st, ','.join(forms), cost(forms), optlib.fmt(r).split(' {')[0], mm), flush=True)
            if show:
                print(text(st, forms))


if __name__ == '__main__':
    main()
