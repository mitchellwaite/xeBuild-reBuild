# s28: bbro event-history edits for mode_client (continuation of s27)

Result: NO MATCH. Best still s27 g7b (best_g7b_dup.c, g7b.json): 7 true inversions, fncmp 27.
Scratch dir build/v/mc28 (deleted). Tools = s27 copies with paths -> mc28, plus evedit.py.

## s18 MATCH history vs g7b (evdiff g7b match; slot from s18/match/repro.sh build/mcmatch/slotm)
- Round 4 pop order/inserts of the tail are almost the same; the decisive difference is EARLIER:
  in the match, 112 (avatar), 115 (compat), 103, 117, 130 are already round-4 heap entries at round
  start (pushed in round 3: 1102=rok's visit inserts 117/130/114 and re-keys 112/115/103/132 with
  priority keys P=3/3/2), and dispatch (1105/1106) inserts 115/112 directly in round 2.
  In g7b, 115 is inserted ('this') by x1=1109 and 112 by 110 inside round 4 with plain -f keys.
- Match also has c125 on 126's visit and c130 on 117's visit (RX126/RX117 gotos + profile).
- So the known-good history differs in which round/popper introduces 112/115 and their priority
  keys, i.e. structural (rok as head of a dispatch reaching s4/s5) + profile priorities.

## evedit.py (hsim with event edits + fany f-search, 3 restarts)
- Edits: move X in {112,115,126,77,79,53,55,61,125} to a round-3 push after any round-3 group,
  or to a round-4 'this' insert by any round-4 popper (single edit). 362 edits run (log evedit1.log,
  search stopped before the last blocks).
- Best 6 (e.g. 77 inserted by 112's pop; 77 pushed in round 3 after 110/113 with f115 7 f112 7
  f103 6 f125 4). Pushing 112 as round-3 push with key -1 gets worse (12-22): without priority keys
  the match's round-3 placement doesn't help. No single edit reaches 0.
- Real compile: adding s4 to the rok JUMP list (or dropping c3 from it) is a no-op (inv 8 measured
  order, fncmp 27): rok's JUMP doesn't influence the round-3 pushes in the plain compile.

## Next ideas
- Pair edits (push 112+115 in round 3 WITH priority keys P, as in the match) in hsim; needs
  modelling 'push' with -(1e6+100P+f) keys. Then find a plain-compile source of priority keys
  for 112/115 (in the match they come from profile edge probabilities through rok).
