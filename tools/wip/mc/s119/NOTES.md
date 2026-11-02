# s119 (attempt 100): NO MATCH. Floor stays 18 (b0.c = s118/b0.c = s117/best.c).

About 300 real variants compiled (run.sh = s118's; results in v*/res.txt). All edits are
never-taken empty asm gotos or __builtin_constant_p dead gotos, so all are equivalent to the original.
- v1/v2 (135): dead bcp feeds to r5x/r3x/u2 placed mid-loop (after each option's assignment),
  1-6 terms, the plain and (char*)==1 forms. They fold before bbro: output identical to b0 or worse
  (the statement's shape matters, the target doesn't). Only feeds at the loop top survive.
- v3/t (51): loop-top feeds (before wb3, between, after u2) to r5x/r3x/w5x/lu1/u2, 1-3 terms, plus
  retargeting the u2 feed: best 18 (= b0), the rest 34-112.
- v4 (16): issue 2, the JMP(s4) edge from other blocks (hdd4/hdd5/c1/c2/c3/c8/c9/c10/c11/c12/cdef/p1/i1),
  "r"(cinfo) input, split JMP(s4);JMP(c12): b9 (split) is neutral 18 (the reload moves into the
  [8+esp]=ebx log slot and usage(3) takes L609's early slot, like s118 a4/c1); b10 = b0; b16 is 19.
- v5 (17): adding/removing E() on every option test: E on -c/-e is a no-op; the rest 22-536.
- v6 (64): the loop-top feeds and v4 on bases b9/b16/c1: floor 18.
r4sim model of issue 3 (w2.py/w3.py/w4.py on s118/dd/mc.bbro):
- Moving bb152's insertion to any other group/position (key -2..1) always changes the order of
  other blocks. Only placements inside 149's group keep them, and those leave 152 where it is
  (or put it last if key 1).
- No single key override of any node, key -8..3, gives the ref order. The only pair hits are 152 and 75 both
  key 1 (or 152 and 83 both key 1): 152 and the strnicmp trace head bb75 (queued from 69's group) must pop after
  every key-0 tie. bb_to_key without a profile can't give a positive key (BB_FREQ_MAX needs a cold
  partition or an unlikely-executed function). Moving both insertions together doesn't hit either.
  So the ref's round 4 probably differs structurally (the tie order comes from a different heap shape),
  not from a single 152 edit.
