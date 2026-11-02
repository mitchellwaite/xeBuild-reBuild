# s27 -- mode_client profile-free (continuation of s26)

Result: NO MATCH. Best still g7b (best_g7b_dup.c, g7b.json): 7 true inversions, fncmp 27.
Scratch dir build/v/mc27 (deleted at the end; `mkdir -p build/v/mc27` before using the tools).

## New tools
- voc.py: new RAW sites (JMP inserted as a bare statement, no braces): `c6<` (case 6 before break),
  `c7t<`/`c12t<` (before the `arg == dummy` tests), `eneg<` `elt<` `enet<` (before the three ifs
  in clientEraseBlock[I]).
- evdiff.py A B: diff of two slots' bbro histories with keys stripped (per popped block event groups)
  + measured f/P deltas.  nev==0 => "event-neutral": hsim on A's history predicts B exactly
  (checked: !fail:pp hdd4 -> f112 7, hsim 21 == real 21).
- injscan.py BASE.json TAG OUT.jsonl: every single bcp injection / raw eb site on top of BASE, with
  evdiff vs TAG (inj27.jsonl = on g7b).
- nsearch.py: event-neutral realizer: combos (K<=3) of neutral levers, deltas summed, hsim-scored.
- fany.py TAG: coordinate descent over ANY f of the 19 tail blocks (0..8) on TAG's history.
- fdum.py TAG: same plus dummy heap nodes (tree-shape lever) after any pop.

## Tries / results
1. (idea 2, new jump sites) tweak.py K<=2 on g7b over the 6 new sites (572 compiles): best 7
   (c7t< some targets, elt<, enet< are no-ops at 7; elt<[eerase] 8; c6/c12t scramble to 10-35).
   K=1 tweak over all sites (incl. new) on v1.json (962 compiles): best 16.
2. (idea 3, event-neutral realizer) injscan on g7b (313 compiles): ~100 injections are
   event-neutral (nev 0) -- all !after/!fail/!ebtop ones; !rok ones are not (nev 6).  Their
   deltas are coarse: f112 1->7/16/29/33/52/74, f115 4->5/8/17.., f103 4->0, f126 2->3 (!ebtop:b/q
   eout, neutral, still 7), f125 1->2, f127 0->1/2.  nsearch (43 distinct levers, K<=3): best 7.
3. (idea 1, when 55 pops / heap shape) heapdump: 55 pops after 126 (both -2; 126 inserted
   during 121, 55 during 49), 77/79 enter at 55's pop and end above 53 in the tree.  KEY RESULT:
   fany.py on g7b's history: no f assignment of the tail blocks gets below 6 (best 6:
   49 5,112 3,103 3,125 2,67 2); fdum.py (f + dummy heap nodes, 25 restarts x 400 steps): 7.
   p34-family history (p34x variant): fany best 7.  So on these histories neither f, nor 55's pop
   time (f55 is in the search), nor extra heap nodes can reach 0: the HISTORY (which blocks a
   trace inserts / claims) must change, not just keys.
4. (idea 4) ga2.py POT2 from s25 populations (gp4/gp5/gs1-3/gp1 top-6 each + p34, seedpop.jsonl),
   ~19 min: best pot 2.2 (score 24, p34 family again) -- same plateau. Log ga27a.log.

## Next ideas
- Target history, not keys: find what event change makes the target order feasible.  Extend hsim
  to edit events (move 77/79 inserts to another popper, drop 112's claim of x, let 112's trace
  end earlier) and search for the MINIMAL event edit that gives 0 with fany; then look for a
  source lever producing exactly that event change.
- Finer injection weights (3-4 chained bcps) only matter after a feasible history exists.
