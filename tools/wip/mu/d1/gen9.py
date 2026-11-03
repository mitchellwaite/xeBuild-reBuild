"""gen9.py: no dummy block.  The heap model says block 105 (updateNand's netUnmount block) only has to leave the 9 tie with 44/43: key 8.
That needs all of updateNand scaled by .85-.96: a dead `pret` test (PRED_POINTER/early return at profile_estimate, folded after inlining).
Axes: where the pret test goes x reboot form x writeImage error form x -ip form."""
import itertools

import axes as a
import sw

vs = []
for (tk, tv), (rk, rv), (ek, ev), (ik, iv) in itertools.product(a.TOP.items(), a.REB.items(), a.ERRS.items(), a.IPS.items()):
    vs.append(('%s_%s_%s_%s' % (tk, rk, ek, ik), a.build(tv, rv, ev, iv)))
print(len(vs))
sw.run(vs, '-O3', save='gen9', top=30)
