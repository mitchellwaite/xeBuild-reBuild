# s69: weighted asm-goto loop levers; NO MATCH
Base s64/best_d (es2 156, R2 0, R3 18). Probes: `python ../s64/q.py TAG ../s64/best_d.json m_X.py` (lp2.py mkw = per-case multiplicity).

| probe | loop edges | es2 (R1,R2,R3,R4) |
|---|---|---|
| a | default x2 | 401 (2,24,64,161) |
| b | case1 + default | 438 (2,24,81,164) |
| c | case1 x2 + case2 | 466 (2,25,81,188) |
| d | default x3 | 419 (2,24,64,179) |
| e | one asm goto at case-12 tail (before break) | 415 (2,25,62,175) |

Finding: any real loop back to the switch, from heads or tails, at any multiplicity, gives R2 24-25 (the rok-block
bb-reorder move noted in s68). R2 is not tuned by edge count or position, so an SA over loop weights would start
at a floor of about 400 against the 155 best. SA was not run. Bests are unchanged (s62/best_b 155, s64/best_d 156).
Next idea: repair R2 directly (rok order/weights, or put an ecx pin on the dispatch) while keeping one loop edge.
