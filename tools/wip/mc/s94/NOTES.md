# s94 (attempt 75): NO MATCH. ~330 variants (log.txt, q.log, r.log, s.log; scripts v1-v5.sh + ccs sweeps).
New inv best: best_s94.c (= n2 = q_1_1) fncmp 42 / sig2 10 / inv 6.
- n1 = b08 + dead `if (__builtin_constant_p(block+5)) goto einv;` at end of eout (before JUMP(efail)) in
  clientEraseBlockI: 42/10/7; Blk moves up to Fer (order -r Fer Blk CU29 CU33 -w). Conjunct count/order/
  position inside eout inert; JUMP(efail) can be dropped (v31 same). goto at eout start / esucc target: worse.
- n2 = n1 + cc chain 1 +1 conjunct: CU33 before CU29 -> inv 6. ccs sweeps on n1 (q) and n2 (r): plateau 42/6.
- x1 = n2 + e6's `asm goto einv` at start of esucc: 36/10/8 (Blk Fer fixed, Info/Inv swapped back); ccs on x1 (s): best 34/18, 36/8.
- -w levers on n1 (w5x disjunct positions/removal, extra edges to w5x/wb3, cold w5x/wb3): all inert; hot k61l very bad.
- efail/esucc edges to eout/einv (v45-v50): worse or inert.
Remaining on n2: Fer before Blk, -w after CU33/CU29. On x1: -w and Info/Inv.
