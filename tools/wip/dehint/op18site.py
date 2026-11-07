#!/usr/bin/env python3
"""Attempt 18: which button sites call parseButtonX (its own split header now that the part
call takes the constant `def`: called twice, fnsplit may split it at the call as it does
parseButton) crossed with trick removals.

python tools/wip/dehint/op18site.py [-r rm1,rm2+rm3,..] [assign ..]
  assign: three letters for xellbutton, xellbutton2, dualboot: X = parseButtonX, P = parseButton
  (default: every assignment); -r: removals from op13.RM ('-' = none)"""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib
import op13

SRC = optlib.read_src(optlib.SRC)
SITES = (('xb.xellButton = parseButtonX(getIniValue("xellbutton"));', 'xb.xellButton = %s(getIniValue("xellbutton"));'),
         ('xb.xellAltButton = parseButton(getIniValue("xellbutton2"));', 'xb.xellAltButton = %s(getIniValue("xellbutton2"));'),
         ('xb.dualButton = parseButton(getIniValue("dualboot"));', 'xb.dualButton = %s(getIniValue("dualboot"));'))
for a, _ in SITES:
    assert a in SRC, a


def build(assign, rms):
    t = SRC
    for (old, new), c in zip(SITES, assign):
        t = t.replace(old, new % ('parseButtonX' if c == 'X' else 'parseButton'), 1)
    if rms != '-':
        for n in rms.split('+'):
            for old, new in op13.RM[n]:
                if old not in t:
                    return None
                t = t.replace(old, new, 1)
    return t


def run(c):
    a, r = c
    t = build(a, r)
    if t is None:
        return c, {'compile': 'edit missing'}
    return c, optlib.score_text(t)


def main():
    a = sys.argv[1:]
    rms = ['-']
    if '-r' in a:
        i = a.index('-r'); rms = a[i + 1].split(','); del a[i:i + 2]
    assigns = a or [''.join(p) for p in itertools.product('XP', repeat=3)]
    combos = [(x, r) for x in assigns for r in rms]
    with ThreadPoolExecutor(6) as ex:
        for (x, r), res in ex.map(run, combos):
            print('%s %-10s %s' % (x, r, optlib.fmt(res)[:200]), flush=True)


if __name__ == '__main__':
    main()
