# s30: mode_client profile-free, short pass

Result: NO MATCH. Best remains s29/best_g7b_dup.c (g7b): 7 true inversions (m.py inv 8), fncmp 27.

- Set up s30 (m.py copied from s29, build dir build/v/mc30, removed at end). Re-measured:
  g7b inv 8 / fncmp 27; s29 c_all.c (X2+RX+T48 realized) inv 74 / fncmp 308 (as s29: needs graded case P levels).
- scan.py: add a second plain JMP site right after the netConnect JUMP list in g7b, random 1-5 targets
  from {i1,p1,hdd5,hdd4,c10,c9,c1,c7,cdef,s4,s5,c3,c2,c8} (40 compiles): best inv 42 (c8 alone; s4+c7+cdef).
  Every extra goto site at the dispatch head absorbs/re-keys whole case groups; it does not give
  graded levels. Graded levels must come from sites on paths of DIFFERENT frequency (not the hot
  netConnect path), as s29 Next ideas say. Not attempted: per-site frequency table + ILP, 110+s4 sibling pair.
