# s145: source forms for the extra efail heap entry (part (c) of s144's recipe)
Base fb.c = s144/fb.c (f2 18). mk.py writes variants that add an empty asm goto at the end of
clientEraseBlockI's efail block (JMP(ex)) to a new label; t.sh NAME = f2 + simulated r4 order.
- c1 (ex = einv) / c2 (JMP(einv)): f2 86; einv edge moves 79/75 ahead of the front.
- c3 (`if (0) { ex: asm volatile(""); }` at end of fn) = c4 (`return; ex: ...`): f2 29. A new block
  (147) does get pushed by the efail trace, and 128 now lands before 79, but it is popped between 79
  and 81 instead of being absorbed by a usage trace.
- c5 (dead "Success!" copy at ex): did not compile (string escaping in mk.py).
Limit: efail lives in the inlined static clientEraseBlockI, so it cannot get an edge to a
mode_client usage call site; the extra entry has to be a block inside that function.
Not done: the 143/144 tie fix and resuming the gen/climb (`NJ=4 sh ../s144/run.sh fb`).
NO MATCH; best is still s141/best16.c (16), fb.c 18.
