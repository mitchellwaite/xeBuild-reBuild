# s92 (attempt 73): NO MATCH. ~150 variants (log.txt).
Best fncmp: best_s92.c (= e6.c) 36/10/8 = g2 + dead `__asm__ goto ("" :::: einv);` at start of esucc in clientEraseBlockI.
  Fixes Blk/Fer swap (order: -r Blk Fer CU33 CU29 -w -e Info Pat ... Inv). Remaining: -w before CU33/29, Inv/Info placement.
p_0_-2 (cc sweep on e6, chain 0 -2) fncmp 34 but inv 18 (CU29 jumps early).
- v01-v05: constant_p goto k55l from case 2/5: loop entry wrecks freqs (fncmp ~960) even as dead constant_p edge.
- fkbo label adjacent swaps (f0-f7), rk list swaps (r0-r9): inert or worse.
- w1-w3 (w5x disjunct position): inert. e1/e11/e12 (edge to einv at eerase): -w moves before Blk/CU33 (wanted) but CU81/Inv jump, inv 18.
- e2/e4/e8/e10/x2-x6: worse. ccs sweep on e6 (ccs_p.txt, 109 variants): best inv 8.
Next idea: combine e11's -w move with something that keeps CU81/Inv late.
