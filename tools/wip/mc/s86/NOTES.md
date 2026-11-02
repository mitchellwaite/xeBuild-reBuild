# s86 (attempt 67): NO MATCH, best unchanged (s84/z3 = best_s84.c, 64/6/14)

42 compiled variants (v01-v42, vb.py + b1-b6.txt, results in log.txt) plus r4sim what-ifs (w1-w8.py).

Tools
- r4sim.py fix: an `ins` of a block already in the heap now does replace_key when the key differs (real
  bb-reorder behaviour). Earlier what-ifs (s85 wi*.py) skipped it. Replay of z3/d2 still exact.
- w1.py: drop 78/80 from 55's inserts, insert from group G. w3/w4: random insert moves + key overrides.
  w5: single extra insert of block b from group G. w8: move inserts between groups.
- z3L.c / d2L.c: labels `cu3l`/`cu5l` on -c's usage(3)/(5) calls (= blocks 78/80); labels alone change nothing.

Findings
- Even with 78/80 never inserted, z3's back group is inv 7 (74 and 140 tie order). The what-if that reaches inv 2
  needs 78/80 inserted by the -w trace (61) instead of -r (55), plus 61 key -1: not realizable, -r's usage
  edges go to 78/80 (same emitted block).
- Single extra early insert of 78/80 (asm-goto edge from an earlier trace) best sim inv 8 (from 142 = case 12).
- Real asm-goto edges perturb freqs much more than the sim assumes:
  - into k67l (-e test) from wb3/wb4/u2: loop entry, fncmp 511-1018.
  - to cu3l/cu5l from c12's JMP: Pat127 freq 2, fncmp 135-179. cold label on cu3l: no change.
  - from fkbo fan (replacing fa20 / fa0): fncmp 194-307 (fan edges carry freq 2). fkbo asm is at 30 operands.
  - from rok fan, cdef, hdd5 log: fncmp 67-137, inv 15. From hdd4 log: 135. From u2/wb3: 361-392.

| var | base | change | fncmp | sig2 | inv |
|---|---|---|---|---|---|
| v01/v02/v03 | z3 | JMP(k67l) in wb3 / usage4 / u2 | 516/511/1018 | 36/36/102 | - |
| v04-v06 | d2 | same | 551/521/1008 | 37/34/102 | - |
| v07/v15 | z3L/z3LC | labels only (plain / cold) | 64 | 6 | 14 |
| v08-v12 | z3L | c12 JMP + cu3l/cu5l (orders, both) | 162-179 | 12-16 | 30-33 |
| v13/v14/v20 | d2L(C) | c12 JMP + cu3l | 135-137 | 16 | 29-30 |
| v16-v18 | z3LC | c12 JMP + cold cu3l/cu5l | 177-179 | 14-16 | 30-32 |
| v19 | z3LC | separate JMP(cu3l) at c12 | 149 | 12 | 17 |
| v21/v23/v24/v31 | z3L | fkbo fan slot -> cu3l/cu5l | 307/307/305/194 | 26/26/26/16 | 27-32 |
| v22/v33 | z3L | asm operand overflow | err | | |
| v25/v26/v32 | z3L | rok fan + cu3l | 87/87/137 | 10/10/8 | 24/23/15 |
| v27/v30 | z3L | hdd4 JMP(cu3l/cu5l) | 135 | 14 | 21 |
| v28/v29 | z3L | hdd5 JMP(cu3l/cu5l) | 67 | 8 | 15 |
| v34/v35 | d2L | hdd5 JMP | 161 | 18/22 | 26/31 |
| v36-v38 | z3L/d2L | u2 JMP(cu3l/cu5l) | 368-392 | 32-38 | 37-39 |
| v39 | z3L | cdef JMP(cu3l) | 137 | 8 | 15 |
| v40-v42 | z3L/d2L | wb3 JMP(cu3l/cu5l) | 361/361/180 | 32/32/20 | - |

Conclusion: plan item 1 (move the 78/80 insert away from 55) is not realizable: 55's edges to 78/80 are part of
the emitted code, and any added edge that inserts them earlier shifts frequencies (asm goto edges split evenly)
far more than the target needs. Sim-level, no single early insert beats inv 8. Remaining unexplored: levers that
change fib-heap root structure without new edges (e.g. extra zero-freq blocks that are popped/consolidated
early, from code that already exists in the original), or matching the original's profile-shaped freqs directly.
