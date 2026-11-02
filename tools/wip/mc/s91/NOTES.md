# s91 (attempt 72): NO MATCH. New best: best_s91.c (= g2.c = g_27_-2.c) fncmp 42 / sig2 10 / inv 6
(previous: c38 42/8/9, v06 36/10/18). ~900 compiles (log.txt: 466 lines; hc1?/hc2?/hc3?.log: 435 climb steps).

## r4sim what-ifs (step 1)
- r4sim.py (s86 version) replays c38 (b38) and a01, g_27_-2 round 4 exactly.
- c38 round-4 order 107 29 139 138 55 33 61 68 ..., target 107 55 139 138 61 33 29 68 ... (tmap.py).
  Keys: 29 -2, 33 -1, 107 -3 (round-3 pushes); 55 -2 (ins by 49), 139/138 -2 (ins by 134), 61 -1 (by 55), 68 -1 (by 61).
- Key-only (ws.py, single/pair): best inv 8. 29 must be key -1 (wb3 freq 1) for 29 after 33.
- Push-order/insert what-ifs (wm.py, wr2.py random search, wp.py exhaustive single/pair):
  * on c38: best single = push 53 (ip3 CU, key 0) during round 3 among the priority pushes/48 trace -> inv 5.
    Not realizable: 53 has freq 0 so it can't get a priority key, and it is already in the heap
    (inserted by round-2 trace 38), so an extra edge doesn't re-insert it.
  * on a01 (29 at -1): push-53-earlier -> inv 4; 3-edit combos reach 2 (138 inserted first in 134's trace,
    80 inserted before 78 by 55's trace, push 53 early); 5 edits reach 0.
  * on g2: extra early insert of 55 (-r test) by trace 123 (t5) or 115 (c2) -> 4; + 139 earlier -> 3.
    A real asm-goto edge to k55l from t5/c2 (e01-e05) enters the loop: fncmp ~1190.
- Dummy zero-key node what-ifs (wd.py): best 6; not an obvious source construct.

## Levers that worked (step 2/3)
- a01: wb3 feed 2->3 conjuncts makes 29 freq 1 (key -1), as the sim needs (alone 60/12/15).
- r2_*: dead `({asm goto("" :::: r5x); 0;})` as FIRST disjunct of -r's usage(3) test puts 80 before 78
  in 55's insert order (CU c3/c5 order now right); on c38 alone 92/8/8.
- g1 = a01 + r2 + fail c11 chain 4->3 terms: -r now first of the -2 group (52/12/9).
- g2 = g1 + fail `ndl` (7368) chain 6->4 terms: 42/10/6. Order: 108 -r Fer Blk CU33 CU29 -w -e Inv Pat CU35 CU42 CU53 Info CU79 CU81 -c.
  Remaining: Blk/Fer swap, -w must precede CU33/CU29, Info position, plus 2 code diffs from it.
## Measured and plateaued
- cc.py: +-1/+-2 conjuncts on each of 30 constant_p chains (ccs.sh) on c38 (k_*), a01 (m_*), g1 (g_*), g2 (h_*): 432 variants.
  c38 best inv 9; g2 best still 42/6 (52 variants tie 6).
- fail-line order climbs, inv first (hc.py ... 1): c38 (hc11-13) 42/9, g1 (hc21-23) 52/9, g2 (hc31-33) 42/6.
- r5x positions r1/r3 (2nd/3rd disjunct): inert.
Tools: ws.py (keys), wm.py/wr2.py/wp.py (moves, extra inserts, random/exhaustive; target via tmap), wd.py (dummy nodes),
cc.py/ccs.sh (conjunct-count sweep), ms.sh (measure existing .c).
Semantics: best_s91.c differs from c38 only by dead constant_p conjunct counts and a dead asm goto that never jumps.
