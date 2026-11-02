# s55: chained rok asm with exact edge weights (idea 1); NO MATCH

Best by es2: **c_s55.c** = lev.text({'w':W}) with rkgen cap=30 (16 reals + 19 fakes -> 2 chained asm gotos),
W = {cdef 6, hdd4 3, hdd5 3, u2 2, c3 2, p0 2, c11 1}: **es2 230 (R1 2, R2 1, R3 34, R4 142)**, ev 78, fncmp 239.
(s54 c_s54.c: es2 239, R2 0, R3 40.) Best ev still s47/H5c2.c.

## Findings
- The 30-operand limit is not a blocker: rkgen.rok already chains chunks (cap). Exact s54 weights {cdef6,hdd4 3,hdd5 3,u2 2}
  fit in one asm (30 ops) -> R3 33 but R4 162 (es2 244). Splitting the same set across chunks (cap 16/8) changes
  R2/R3 (chunk boundaries alter probabilities: each chained asm splits flow evenly over its labels + fallthrough).
- Two-chunk variants mostly cost R2 = 1 (join over the 43 threshold); greedy on weights reached es2 230 but never R2 0
  with R3 < 40. Ideas 2 (distinct prios) and 3 (join budget) not explored this session.

## Tools
s1.py (cap/weight variants), hc.py (greedy +-1 on rok weights, fixed cap; log hc.jsonl).
## Next
Combine hc weights with base2 npre (more ndl diversions) to pull R2 back to 0; try per-chunk label grouping (order arg)
so the chunk carrying t4/t5-related targets gets a smaller fan-out.
