# s52: why the round-2 trace stops (plain compile) and a lever for it

Result: NO MATCH. Best overall unchanged: s47/H5c2.c (ev 5 / fncmp 34 / es 348 = R1 2, R2 33, R3 53, R4 94).
New best R2: c_t2A.c (= lp4.mk(9,21,0,'tail',2,'A')): es 368 (R1 2, **R2 26**, R3 56, R4 136), ev 52, fncmp 228
(instruction multiset unchanged, +114/-114 lines: layout only).

## Root cause (task 1)
- The match's vX51 pushes come from the BUILD_FDO `__asm__ goto("" :::: i1,p1,hdd5,hdd4,c10,c9,c1,c7,cdef)` before
  netGetInfo (match bb106 = asm goto, 107 = switch range check, 108 = tablejump; trace 105 106 107 108 [87..86]).
  H5c2 has that JUMP disabled (106 = range check, 107 = tablejump; trace stops at 107).
- Plain compile with that asm goto (JMP): asm goto with >2 succs gets even probs (1/10) at tree level;
  bbro needs prob >= 20% (round 2) AND edge freq >= exec_th = 217*0.2 ~ 44. Trace stops at the asm block.
- Fake extra labels don't work naively: (a) labels in the fallthru bb make expand_asm_stmt emit a fallthru_label,
  the block is split and find_many_sub_basic_blocks leaves >2-succ edges at probability 0 (cfgbuild.c
  compute_outgoing_frequencies: "rely on BBs with more than two successors to have sane probabilities");
  (b) bcp-guarded fake blocks are folded at fab1 (tree) -> same as (a); (c) asm operand limit 30.
- Working construct (ck3.py/lp4.py): fake labels fa_k each `goto ofa_k` out of a `struct {}` scope (asm "X"(&var) keeps
  the vars), so try-finally lowering gives one clobber-only copy per destination: distinct, non-forwarder tree blocks
  that expand to nothing; RTL cfgcleanup forwards them into the fallthrough and redirect_edge_succ_nodup SUMS the probs.
  Fallthrough share (1+K)/(10+K), K<=21 -> .71; still < .76 needed at freq 58, so add a frequency boost:
  bcp backedge `if (bcp(mode+91)&&bcp(mode+92)) goto fkbo;` before `if (E(reboot))` with fkbo at the asm block
  (header 'A'): loop exists only at tree level (stale freq after fab). Then the R2 37-group matches the match's
  insertion sequence (131 118 115 112 121 120 107 116 132, vX vX, 108 ...).
- Boosts entering via netConnect / forward bcp from the NO_MODE_ARG block wreck R1 (then-branch loses freq,
  round-1 trace 101/102 drops below 108 = round-1 exec_th).
- Remaining R2 diff: fail-path trace X40 (H5c2 143 [101], match 139 [73]) comes first in round 2; plus i109/iX54:t naming.

## Search
- grid.py/lp*.py/fl.py ~120 variants; sa2.py (s51 lv levers on the construct) 2 x 540 s, ~2200 compiles
  (sa_s52a1.jsonl, sa_s52a2.jsonl): best es 350 (R2 26, R3 49, R4 132) ev 60; nothing beats H5c2 on es+ev.

## Next
- Lower the fail-path freq below the 105 trace (or raise 105 without touching R1) to fix R2 order.
- Then R3/R4 with lv levers on c_t2A base (sa2.py, BASEV env).
