# s49: H5c2 vs s18 profiled MATCH bbro history (plain compile goal)

Result: NO MATCH. Best unchanged: s47/H5c2.c (m.py 6, ev 5, fncmp 34, cm (0,6)); best order s47/Uc1.c.
Only compiles: s18/match/repro.sh (fncmp 0, round4 inv=1) and H5c2 slot (m.py 6). No lever compiles done.

Tools (take slot dirs; H5c2 slot via `s42/m.py s47/H5c2.c TAG`, match slot = build/mcmatch/slotm after repro.sh):
- hist.py SLOT: per-round/group event dump (v=visit, p=push, iN:t/n=insert, cN=chg).
- cross.py A B: sim A's history with B's keys, single/pair/triple key transplants.
- graft.py A B: round-wise history mixes (useless: unnamed block numbers shift by 1, mixes are junk).
- needk.py A B: on B history, revert B keys to A keys greedily; lists keys B needs.
- pscan.py A: P (trace-end priority) x f scan for 55/126/125/61 on A history.

## Findings (task 1)
- R4 events for 126/125/55/61/77/79 are IDENTICAL in both: 126,125,127 inserted in g121, 55 in g49,
  61/77/79 in g55 (the -r trace), 67 in g61. So s48's "77/79 must be inserted only by 61" is a property
  of H5c2's keys, not of the target: the MATCH also inserts 77/79 from the -r trace (g55).
- The real difference is ROUND 3:
  match: R3 trace 1102 visits only itself, inserts 117 130 114 and stops with chg on 112 115 103 132; trace
  1048 stops with chg on 94 49. Then EVERY round-4 seed is pushed in R3 (109 107 113 110 119 108 120 121 128
  116 132 115 112 103 ... 131 118 29 33 42 35 53) -- note 53 pushed LAST (after 42 35), 94 not visited in R3.
  H5c2: R3 1048 trace visits 94 (v94) and inserts 49; 115/112/131/118 are not pushed in R3; push order
  ... 103 29 33 53 42 35 (53 before 42/35) -> this is the 35 42 79 77 53 vs 35 42 53 77 79 tail.
- Keys: on H5c2 history no key/P transplant (singles..triples of all 22 differing blocks; P 0..2 x f 1..4 on
  55/126/125/61) gets below m-inv 10 (sim) -- history-bound, confirming s48.
- On the MATCH history, needk.py: 55's key is NOT needed (f=2 like plain is fine), but trace-end priority keys
  are: 125 (P=1, f=1) essential (else +2 = 126/125 vs 55), 49 P=6, 112 P=3, 132 P=6, plus the high R3/R4
  keys of 107..129. P>0 = bb_to_key priority from an edge out of a trace end with EDGE_FREQUENCY>=1, which
  plain estimated frequencies give (P=0 everywhere in H5c2).
- So the target needs (a) round 3 to stop at 112/115/103/132 and 94/49 (thresholds) so they are pushed,
  with 53 pushed after 35/42, and (b) a nonzero trace-end edge frequency into 125.

## Next
- Lever compiles: make 94 fail the R3 threshold (bcp-goto cold edge into 94 / trace-end lever T48) so 1048
  stops before 94; get an RX goto (s18/s29) from a trace end into 125 to give P>0; reorder R3 53 vs 42/35
  insertion (53 inserted in R2 g1038 before 42) -- swap their source order. cm + evdiff each.
- Not proven unreachable.
