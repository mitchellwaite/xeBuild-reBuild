# s121 (attempt 102): NO MATCH. Floor stays 18 (b0.c = s117/best.c).

Structure (dir 1): best18 (s118/dd/mc.bbro) and profiled (s111/pf/mc.bbro) bbro both duplicate exactly
two blocks (a 3474/3475-insn trace head copy and one ~120-insn tail block); no extra bb-reorder copies in
either. The profiled CFG has ~20 fewer blocks (empty forwarders absent: 143 vs 165 bbs before dup), so
the round-4 set difference is in forwarder/jump blocks, not in copy_bb decisions.
Issue 1 (ref asm 290-305, 421-469): ref stores [8+esp]=ebx once before the nandSize compare; the
outside-area and invalid logs (421/425) need no store; the "Failed to erase" copy that re-stores ebx
is the post-neteraseblock path and sits in the second group (465) after usage(2). Ours has the same
blocks, ordered usage(2) first and fail-log in the first group: ordering, not RA.
Variants (~135, all equivalent: only never-taken asm-goto / __builtin_constant_p edges or asm volatile(""))
- v/ (gen.py, 34): dead gotos between clientEraseBlockI labels (einv/eout/esucc/eerase/efail) from 5
  sites + asm volatile("") at 9 spots. 12 x 18 all byte-identical to b0; g_eo_efail2 20 (fail log
  becomes fall-through after the erase call), others 21-112.
- v2/ (gen2.py, 23): reverse / drop each label of each switch-region asm goto. 7 x 18; rm1_8
  (JMP(s4,c12) -> JMP(s4)) is a different 18: cinfo reload moves and the tail usage block becomes
  usage(3) instead of usage(5). del_11/del_22 19.
- v3/ (55): gen.py + gen2.py on rm1_8: best 18 (17 of them), none lower.
- v4/ (~28): gen2 on g_eo_efail2 and del_11: >=19.
Conclusion: clientEraseBlockI edge levers and switch asm-goto label sets are exhausted around best18.
