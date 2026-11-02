# s107 (attempt 88): NO MATCH. Best stays s102/best.c (f2 24).

Key finding: hand-inlining clientEraseBlockI into case 10 (mk.py -> h0.c; labels renamed *_i, function
removed) is codegen-neutral: f2 24 and the same round-4 order as best. Its labels (eerase_i, ecmp_i,
enet_i, esucc_i, efail_i, eout_i, einv_i) are now main-local, so main code can jump to them.
Semantics: same statements, run once in the same place; the only edits are dead gotos.

Variants (all from h0/h1; ev.sh = run.sh + srch.dist; ~300 hand/grid + ~1270 climb evals):
- g/c*, g2: dead cp `goto eout_i` from 19 main sites x 1-5 conjuncts x esucc->eout on/off: 139's freq goes
  3->11 (key -11), and it pops right after 105/49 (f2 34, d4). Conjunct count and site make no
  difference (the feed is quantized).
- g/b*, g/a*: a real zero-byte edge (JMP(eout_i), alone or added to existing asm-goto lists): f2 108-239,
  because `block` becomes live (and uninitialized) from the source block, which upsets RA. b15 (efail->eout
  inside the callee) costs 39. An edge from a round<=3 block (104/141/48/46/5) into 139, which the m.py
  target needs, therefore always costs this RA damage, so (a) is not reachable for free.
- g3/g5: feeds to the other callee labels. einv_i: neutral (24/32, same order). efail_i: 139 drops to key -2
  and comes AFTER 55 (108 55 139, as the target wants), but 138 (now 137) drops to -1 and lands after 62,
  and 81/140 move (f2 40, d5). eerase/enet: 136 takes over (f2 98). Pairs of feeds: nothing better.
- g6: feeds into c10 / ecmp_i (top of the 134 trace): with the c10 feed from site 13, 134-135 become a
  round-3 trace (134 [13] 135 [13]), so 139 is pushed in round 3, but at key -6, 134 leaves the round-4
  list, and f2 is 82-104.
- cl.py climbs (conjunct add/del, cost f2+2d), 4x~320: from ef.c (efail feed) to 44-48; from iv.c (einv feed) 38.
Conclusion: a round-3 push of 139 needs either a real edge (RA damage from `block`) or a 134 trace that is
hot enough for round 3 (then 134 leaves the round-4 list, which contradicts the target). The efail feed
newly gives 55-before-139 ordering, but at the cost of 138's key and of 81/140.
