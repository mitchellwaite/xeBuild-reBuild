# s47: the exact 77/79 mechanism (plain compile, no profile)

Result: NO MATCH. New best clean content: H5c2.c (= s42/H5b.c + zero-byte asm-goto edge in the -w arm,
`mk.py H5b.c H5c2.c c2`): m.py 6 inv (same order as H5b) / fncmp 34 / cm (0,6)  (H5b: 6 / 40 / (0,8)).
Best order: Uc1.c (= s44/U.c + asm goto `c1` in -w arm): m.py 3 inv, true (ev WANT) order only 2 inv
(55 vs 126/125, the two reboot log_printf blocks), tail 35 42 53 77 79 exact; but fncmp 50 / cm (10,6)
(the -r arm RA flip of U).

## Task 1: U vs P in bbro (exact)
- 77 / 79 = the shared crossjumped tails client_usage(3, argv[i]) / client_usage(5, argv[i]) (eax group;
  original labels .L_408ca9 / .L_408cbc, jumped to by ALL four len-2 arms -r/-w/-e/-c, see rawref.py).
- Both are key-0 singleton traces in round 4; order = fibheap tie order of the key-0 nodes 35/42/53/77/79.
- P (-r tails eax, in 77/79's pred set: 77 <- 56,57,58, 79 <- 59): pushed during the -r trace (group 55,
  after ins 61 key -2) as 77 then 79 -> pops 35 42 79 77 53.
- U (-r tails become edx group, not preds): first pushes come from the -w trace (group 61, after
  ins 67 key -1): 77 from 62, 79 from 65 -> 35 42 53 79 77.
- hsim what-ifs (wi2/wi3.py on slot_tP): the target 35 42 53 77 79 needs the push of 79 BEFORE 77,
  both inside the -w group after its 67 ins, and NO -r pushes. Any -r push (any position, any order)
  gives at best 35 42 77 79 53 (wi3 55 55). Moving 53/42/35 pushes (wi5) or adding a dummy key-0
  node (wi6) never gives the tail without breaking others (>=12 inv).

## Task 2: levers
- Zero-byte `__asm__ goto("" :::: w5x)` in the -w arm with `w5x:` on its client_usage(5) call:
  position c1 (before `i + 1 == argc`) pushes 79 first -> on U: tail exact (Uc1). Positions c2/mid/c3/c4
  after the first usage(3) jump don't. `top`/`pre` (before a = argv) wreck the order (41-43 inv).
- On H5b/P the edge is order-neutral (the -r trace pushes first) but c2 improves content (fncmp 34, cm 0,6).
- RA pins restoring the -r arm (eax=i, edx=i+1) on Uc1 ("d"(i+1), "a"(i), both): -r tails rejoin 77/79,
  back to 6 inv / cm (0,8). Confirms s43's coupling with the exact reason: the original's -r arm DOES jump
  to the shared tails, so in the plain heap model the -r trace's pushes always come first.
- So a plain match needs the -r trace's pushes to be ineffective (77/79 already queued in round 4 before
  the -r trace, inserted 79 first) or a different heap shape; round-3 pushes (wi4) shift other blocks.

## Next
- Find an existing earlier round-4 trace (before group 55, after 53/42/35 are in the heap) that can carry
  zero-byte asm-goto edges to w5x-style labels on the shared tails, 79's label first (wi3-style sim first:
  add ('ins','this',79,0),('ins','this',77,0) to each round-4 group before 55 and check the tail).
- Task 3 (ebl/k*l/beam) not reached.

Tools: wi.py..wi6.py (hsim what-ifs), mk.py (asm-goto variants), rawref.py (raw original/gcc listings
with labels), lev.py/lev2.py (lever scans). Scratch build/v/mc47 deleted.
