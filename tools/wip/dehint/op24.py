#!/usr/bin/env python3
"""Attempt 24: the rev feeds' last two expects (e2, e3) without dead code.

python tools/wip/dehint/op24.py [-m] [-e] [-show] [-o out.c] [-v fn] variant ..
  a variant names an entry of V: (feed text, tail text) replacing the two feed lines and the
  dummies' labels at the end of applyIniOptions in src/options.c (attempt 23's landed shape).
  -m  op23's counts from the optimized dump (dz = the unreachable blocks, rev, ret, ..)
  -e  op23's profile_estimate predictions of the feed tests (and parseButtonX's power)"""
import os, re, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib
import op23

SRC = open(optlib.SRC).read()


def X(n):
    return '__builtin_constant_p(xb.blSuffix[1] + %d)' % n


I = '\t\t\t'
FEED = (I + 'if (%s) { if (%s) goto dz1; return; }\n' % (X(1), X(2)) +
        I + 'if (__builtin_expect(%s, 0)) { if (__builtin_expect(%s, 0)) goto dz2; goto dz1; }\n' % (X(15), X(16)))
assert FEED in SRC, 'feed'
TAIL = 'dz1:\n\t__builtin_unreachable();\ndz2:\n\t__builtin_unreachable();\n}\n'
assert TAIL in SRC, 'tail'
T12 = 'dz1:\n\t__builtin_unreachable();\ndz2:\n\t__builtin_unreachable();\n}\n'
T21 = 'dz2:\n\t__builtin_unreachable();\ndz1:\n\t__builtin_unreachable();\n}\n'
T2 = 'dz2:\n\t__builtin_unreachable();\n}\n'
T1 = 'dz1:\n\t__builtin_unreachable();\n}\n'

V = {}


def fx(s):
    return s.format(**{'n%d' % i: X(i) for i in range(1, 40)})


def add(name, feed, tail=T12):
    V[name] = (fx(feed), tail)


E = '__builtin_expect({n}, 0)'
B1 = I + 'if ({n1}) {{ if ({n2}) goto dz1; return; }}\n'
B1g = I + 'if ({n1} > 0) {{ if ({n2}) goto dz1; return; }}\n'
add('base', B1 + I + 'if (__builtin_expect({n15}, 0)) {{ if (__builtin_expect({n16}, 0)) goto dz2; goto dz1; }}\n')
# no expects, both labels at the end (attempt 23's candidate without its sprintf)
add('ne', B1g + I + 'if ({n15} < 0) {{ if ({n16} < 0) goto dz2; goto dz1; }}\n', T21)
# PRED_GOTO: dz1 inline (no goto on its arm), so only dz2's arm carries the goto prediction
for a, af in (('p', '{n1}'), ('gt', '{n1} > 0'), ('ne5', '{n1} != 5')):
    for c, cf in (('p', '{n15}'), ('lt', '{n15} < 0'), ('eq', '{n15} == 5'), ('gt', '{n15} > 0'), ('ne5', '{n15} != 5')):
        for d, df in (('p', '{n16}'), ('lt', '{n16} < 0'), ('eq', '{n16} == 5'), ('gt', '{n16} > 0'), ('ne5', '{n16} != 5')):
            hd = I + 'if (%s) {{ if ({n2}) goto dz1; return; }}\n' % af
            # dz1's label inline after dz2's goto; dz2 alone at the end
            add('gi:%s,%s,%s' % (a, c, d), hd + I + 'if (%s) {{ if (%s) goto dz2;\ndz1:\n\t\t\t\t__builtin_unreachable(); }}\n' % (cf, df), T2)
            # inverted: dz1 inline on the then arm, dz2 by goto
            add('gv:%s,%s,%s' % (a, c, d), hd + I + 'if (%s) {{ if (%s) {{\ndz1:\n\t\t\t\t__builtin_unreachable(); }} goto dz2; }}\n' % (cf, df), T2)


# the whole rev stretch (live code + feeds), replaced at once: the feeds ahead of the live
# sprintf, so the live call sits on the edge out of the feed tests
STRETCH0 = SRC[SRC.index('\tif (!xb.blSuffix[0]) {\n'):SRC.index('\treturn;\n\t/* the dummy heap')]
SP = '\t\t\tsprintf(xb.blSuffix, "_%s", s);\n'


def stretch(name, body, tail=T12):
    body = re.sub(r'\{n(\d+)\}', lambda m: X(int(m.group(1))), body).replace('{{', '{').replace('}}', '}')
    V[name] = ('STRETCH' + body, tail)


H = '\tif (!xb.blSuffix[0]) {\n\t\ts = getIniValue("rev");\n\t\tif (s) {\n'
Z = '\t\t}\n\t}\n'
for c, cf in (('p', '{n15}'), ('lt', '{n15} < 0'), ('gt', '{n15} > 0'), ('e', E.format(n='{n15}'))):
    for d, df in (('p', '{n16}'), ('lt', '{n16} < 0'), ('e', E.format(n='{n16}'))):
        # B1 then the split feed, then the live sprintf (C's false edge -> the call block)
        stretch('pre:%s,%s' % (c, d), H + B1 + I + 'if (%s) {{ if (%s) goto dz2; goto dz1; }}\n' % (cf, df) + SP + Z)
        # the split feed alone first, B1 after the sprintf
        stretch('mid:%s,%s' % (c, d), H + I + 'if (%s) {{ if (%s) goto dz2; goto dz1; }}\n' % (cf, df) + SP + B1 + Z)
        # live code as early returns (the feeds after the sprintf)
        stretch('er:%s,%s' % (c, d), '\tif (xb.blSuffix[0])\n\t\treturn;\n\ts = getIniValue("rev");\n\tif (!s)\n\t\treturn;\n'
                + SP[2:] + B1[2:] + '\tif (%s) {{ if (%s) goto dz2; goto dz1; }}\n' % (cf, df))


# asm goto label lists: a block with more than two successors gets even probabilities in
# gcc 6 (no noreturn), so a two-label asm goto feeds both dummies a third of its block each.
# extra edits, applied after the feed: name -> [(old, new)]
AG1 = '\t\t\t\t\t__asm__ goto ("" :::: dz1);\n'
AG2 = '\t\t\t\t__asm__ goto ("" :::: dz2);\n'
assert AG1 in SRC and AG2 in SRC
XE = {}
for k1, l1 in (('1', 'dz1'), ('12', 'dz1, dz2'), ('21', 'dz2, dz1')):
    for k2, l2 in (('2', 'dz2'), ('12', 'dz1, dz2'), ('21', 'dz2, dz1')):
        if k1 == '1' and k2 == '2':
            continue
        for fk, ft in (('nf', ''), ('base', None)):
            nm = 'ag:%s,%s,%s' % (k1, k2, fk)
            V[nm] = (ft if ft is not None else V['base'][0], T12)
            XE[nm] = [(AG1, AG1.replace('dz1', l1)), (AG2, AG2.replace('dz2', l2))]


def build(name):
    feed, tail = V[name]
    if feed.startswith('STRETCH'):
        t = SRC.replace(STRETCH0, feed[7:], 1)
    else:
        t = SRC.replace(FEED, feed, 1)
    t = t.replace(TAIL, tail, 1)
    for old, new in XE.get(name, []):
        assert old in t
        t = t.replace(old, new, 1)
    return t


def main():
    a = sys.argv[1:]
    flags = optlib.P83
    m = e = show = False
    out = vf = None
    for f in ('-m', '-e', '-show'):
        if f in a:
            a.remove(f)
    m, e, show = '-m' in sys.argv, '-e' in sys.argv, '-show' in sys.argv
    if '-np' in a:
        a.remove('-np'); flags = []
    if '-o' in a:
        i = a.index('-o'); out = a[i + 1]; del a[i:i + 2]
    if '-v' in a:
        i = a.index('-v'); vf = a[i + 1]; del a[i:i + 2]
    names = []
    for n in a:
        if n.endswith('*'):
            names += [k for k in V if k.startswith(n[:-1])]
        else:
            names.append(n)

    def one(n):
        t = build(n)
        return n, optlib.score_text(t, flags), (op23.metric(t, flags) if m else ''), (op23.preds(t, flags) if e else '')
    if vf:
        for n in names:
            optlib.vdiff(build(n), flags, vf)
    else:
        with ThreadPoolExecutor(6) as ex:
            for n, r, mm, ee in ex.map(one, names):
                print('%-20s %s %s' % (n, optlib.fmt(r), mm), flush=True)
                if ee:
                    print(ee)
                if show:
                    print(V[n][0])
    if out:
        with open(out, 'w', newline='\n') as f:
            f.write(build(names[-1]))


if __name__ == '__main__':
    main()
