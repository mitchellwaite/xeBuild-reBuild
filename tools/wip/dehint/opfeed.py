"""opfeed.py SITE [forms]: replace one dead-feed site in src/options.c by nested
__builtin_constant_p/__builtin_expect forms (oprev.FORMS) and score each with optlib.
Sites: z (parseButtonX's goto z arms), dx (parseButtonX's power-arm feed)."""
import os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib, oprev

SITES = {
    'z': ('		if (__builtin_constant_p(xb.xellButton + 1)) { if (__builtin_constant_p(xb.xellButton + 2)) goto z; if (__builtin_constant_p(xb.xellButton + 3)) goto z; }\n',
          '__builtin_constant_p(xb.xellButton + %d)', 'z', 1),
    'dx': ('		if (__builtin_expect(__builtin_constant_p(xb.xellButton + 5), 1)) goto dx;\n',
           '__builtin_constant_p(xb.xellButton + %d)', 'dx', 5),
}


def render(form, cp, lab, base):
    conds = []
    for i, c in enumerate(oprev.FORMS[form]):
        c = c.replace('__builtin_constant_p(xb.blSuffix[1] + %d)', cp)
        conds.append(c % (base + i))
    return '\t\t' + oprev.nest(conds, lab) + '\n'


if __name__ == '__main__':
    site = sys.argv[1]
    old, cp, lab, base = SITES[site]
    forms = sys.argv[2].split(',') if len(sys.argv) > 2 else list(oprev.FORMS)
    t0 = optlib.read_src(optlib.SRC)
    assert old in t0

    def one(f):
        return f, optlib.score_text(t0.replace(old, render(f, cp, lab, base)))
    with ThreadPoolExecutor(6) as p:
        rs = list(p.map(one, forms))
    rs.sort(key=lambda x: x[1].get('total', 10 ** 9))
    for f, r in rs:
        print('%-8s %s' % (f, optlib.fmt(r)))
