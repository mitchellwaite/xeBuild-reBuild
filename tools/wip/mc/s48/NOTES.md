# s48: what-if sims on H5c2 for 77/79 and 126/125/55 (plain compile, no profile)

Result: NO MATCH. Best unchanged: s47/H5c2.c (m.py 6 inv, ev true-order 5-6, fncmp 34, cm (0,6));
best order still s47/Uc1.c (ev 2, cm (10,6)). Only 1 real compile (H5c2 slot); rest is hsim on its history.

## Task 1 (77/79 from an earlier round-4 trace): impossible in the heap model
- wi7.py: move both 77/79 ins (either order, any positions) into EVERY round-4 group before 55
  (129..125): always 77/79 pop BEFORE 35/42/53 (14-28 inv). 35/42/53 are round-3 pushes; anything queued
  in round 4 before 55 lands ahead of them after consolidation.
- wi8.py: 77 and 79 independently at any (group,pos) among groups 49..67: the tail 35 42 53 77 79 appears
  ONLY with both in group 61 (after pos 2 = after 67's ins), confirming s47.
- wi9.py: keep the -r pushes, add a dummy node (key 0..-3) inserted anywhere in groups 49..67 and optionally
  deleted (visited) later: never the tail (best 35 42 77 79 53). So heap-shape tricks do not neutralise the
  -r pushes.
- -fdump-rtl-all-details: crossjumping only happens in 266r.jump2 (none at/after bbro), so the -r arm tails
  are preds of the shared 77/79 at bbro whenever the original eax pairing holds (s44/s46). With the -r
  trace (55) running before 61, its pushes always come first -> the original order is not reachable from
  this event history by insertion/heap tricks alone.

## Task 2 (55 vs 126/125)
- fs.py / fa.py / fa2.py: freq (key) overrides 0..6 on all round-4 named blocks (exhaustive on
  55,126,125,61,33,29,67; hill climb on 19 blocks), with and without 77/79 moved to 61: min true inv 5
  (as is) / 2 (moved) -- 126 125 always before 55. wi10.py: relocating 55's or 126's ins to every
  (group,pos): no change (best 5 / 2). Not a key or insertion problem in this history (matches s42).
- Not done: ebl/k*l/bcp lever beams (need a structural change first; the sims show no key/insert target).

## Next
- The remaining two inversions need a different round-3/round-4 history (pre events, number of traces
  extracted between) -- e.g. sim edits on R[2] (round 3) pushes/extractions together with the 61 move,
  or check whether the original was not a plain heap order at all (profile-only).
Tools: wi7-wi10.py, fs.py, fa.py, fa2.py (all take a mkslot slot dir; make one with s42/m.py SRC TAG).
Scratch build/v/mc42, build/v/mc48a deleted.
