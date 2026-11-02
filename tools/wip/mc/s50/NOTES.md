# s50: round-3 lever compiles on H5c2 (plain compile goal)

Result: NO MATCH. Best unchanged: s47/H5c2.c (ev 5 / m.py 6 / fncmp 34 / cm (0,6)).

Tools: h.py (ev score + fncmp + round-3 feature score r3s vs s18 match: v94 in R3 +3, missing c112/c115/c103/c132,
missing p115/p112/p131/p118, 53 pushed before 42/35; H5c2 = 13, match = 0), lv.py (lever genome -> text:
rok JUMP->real JMP target lists, second JUMP->JMP, JUMP(i0)->JMP, E() drops on -bp/-wb/-eb/-e/-c, T48 =
k48l label before the -keys test (else-wrap) + bcp goto from 10 sites with 1-3 bcp terms, two extra bcp gotos
to existing labels), sa.py (mutation search; env W = score weight, G = start genome). Logs: sa_a*.jsonl, sa_b*.jsonl.

## Findings (~6500 real compiles, 8 runs x ~560 s)
- Every lever that changes round 3 at all costs >= +9 ev: best per r3s (min ev score):
  r3s 12 -> 16, 11 -> 14, 10 -> 28, 8 -> 28 (k48b.c: T48 at -keys body, fncmp 228, cm (0,16)), 7 -> 51, 6 -> 59, 5 -> 126.
- r3s 0 never reached. rok real JMP lists reproduce the match's R3 g1102 re-keys of 112/115/132 partially
  (e.g. rok c12,hdd5,c7,hdd4 + T48 keysb: c115 c112 in R3) but always also break the prefix/case order.
- T48 at -s (N=300, rok c12,i0) gives the match's 1048 shape exactly (i94:n i49:n c94 c49) but ev 41.
- Most extra bcp gotos to existing labels are no-ops (folded before bbro).
- Task 4 (53/42 swap) not attempted: no content-safe source swap identified.

## Next
- Combine the exact-1048 lever (t48 s/300 + rok) with prefix-repair levers; score with evdiff by round, not r3s.
