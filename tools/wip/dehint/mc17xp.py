#!/usr/bin/env python3
"""mode_client attempt 17: a measuring device, not a candidate.  A two-connect variant of
mc17.py with the connects given explicit odds through `__builtin_expect` and `--param
builtin-expect-probability=N`: the switch path's N% likely to succeed and, with -both, the
reboot path's N% likely to fail.  It showed what the reference's layout needs before any
source had it (N = 76..85 with -both: the layout through -ip and the case order).

python tools/wip/dehint/mc17xp.py [-both] [-l] [-d] VARIANT N [N ..]
  -l  print the layout diff, -d write dumps to build/mc/w17/d_xp_N"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc17
import mc17lib as L
import mc17sw

a = sys.argv[1:]
both = '-both' in a
show = '-l' in a
dump = '-d' in a
a = [x for x in a if x not in ('-both', '-l', '-d')]
t = mc17.text_of(a[0])
C = 'netConnect(ip)'
i = t.index(C)
j = t.index(C, i + 1)
sw_first = 'switch (mode)' in t[i:j]            # which of the two is the switch path's


def rep(t, pos, exp):
    return t[:pos] + '__builtin_expect(netConnect(ip) != 0, %d)' % exp + t[pos + len(C):]


if both:
    t = rep(t, j, 0 if sw_first else 1)
    t = rep(t, i, 1 if sw_first else 0)
else:
    t = rep(t, i if sw_first else j, 1)
t = t.replace('!__builtin_expect(netConnect(ip) != 0, 1)', '__builtin_expect(netConnect(ip) == 0, 0)')
t = t.replace('!__builtin_expect(netConnect(ip) != 0, 0)', '__builtin_expect(netConnect(ip) == 0, 1)')
for n in a[1:]:
    ex = ['--param', 'builtin-expect-probability=%s' % n]
    if dump:
        print(L.dump(t, 'xp_%s' % n, extra=ex))
    ok, o, d = L.compile_src(t, extra=ex)
    if not ok:
        print(o)
        continue
    idn, tot, per, notes = L.report(o)
    names = [x[0] for x in L.chunks(o)]
    pre = 0
    for x, y in zip(mc17sw.REFC, names):
        if x != y:
            break
        pre += 1
    if show:
        L.laydiff(o)
    print(n, tot, 'moved=%d' % L.laydiff(o, show=False), 'pre=%d' % pre,
          'cas=%s' % ('C' if mc17sw.caseorder(names) == mc17sw.REFCASE else '-'))
    L.cleanup(d)
