# s65: R3 c11 hand probes + annealed-R2 POST SA; NO MATCH
## Hand probes (hv.py, variants of s64/best_d, es2 156 = R1 2/R2 0/R3 18/R4 104, fncmp 158)
- PD c11 removed / depth 8 / 9, TH c11 dropped, rok w c11 1 or 2: no change at all (identical es2/fncmp).
- w c11 4: es2 183 (R3 26); w c11 0: 163 (R3 20); c11 out of rok order: 233 (R2 1); X c11 removed: 214;
  w0+X2: 183 (fncmp 152, lowest seen here but R4 127).
=> the c11 visit is not removable through PD/rok/TH c11 levers without hurting; removing c11 flow hurts R3.
## SA (sa.py = s64 sa + R2 penalty annealed 2 -> 400 per R2 event, b2_ tracks best R2-0 es2; 4 x 3600 s, ~5150 evals each)
- p1/p2 (best_d, POST 1-2), p3 (best_b, POST 2): never below R2 40; best es2 ~464 (R2 40). POST at depth <=2
  cannot be compensated by the existing levers - R2 is structurally broken by the halved post-loop region.
- f4 (free, R3W 3, best_d): no improvement (156).
## Next ideas
- POST is a dead end with current levers; a compensating lever must ADD flow to the non-dispatch post-loop
  blocks (e.g. dead bcp gotos from the dispatch region into the NO_MODE_ARG side's blocks) - untested.
- The 1114/109 push difference still unexplained; try rk.py on best_d with w0x2 variant (fncmp 152).
