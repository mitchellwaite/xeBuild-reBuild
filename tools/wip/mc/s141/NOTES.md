# s141: profile-free mode_client, from s139 best17 (f2 17)

## B. Case-5 cinfo reload: FIXED -> best16.c (f2 16, 4 hunks)
Cause (tree-optimized dump, dd/): at t5 cinfo is a PRE value (prephitmp, from the load before the
switch), but label s5 has many fake preds (rk dispatcher ork7/8, c3/c9 JMPs, the bcp goto). So the
"a"(cinfo) input of the asm goto inside s5 has no available value and gets a fresh load.
Fix: move that asm goto ahead of label s5, into the t5 then-arm, so only the t5 edge runs it:
  { __asm__ goto ("" :: "a"(cinfo) :: s4, c12); AT(s5)JMP(dsp);  { sendCompatData(arg); } }
Its input is now the value the test loaded, so the reload is gone. Semantics: the empty asm goto
falls through, as before. Splitting labels as (s4)+(c12) gives the same result (c3); other splits,
merges or orders give 34/44. "X"/extra "i"(0) inputs and a plain asm in front change nothing (17).
baseC.c = baseA.c with this change; baseC + p17 = best16.c.

## A. Search on baseC + p17 (gen.py/climb.py; the bsingles mode was added)
- Singles 6338: none below 16 (1947 inert at 16; best non-inert is 17).
- Pairs over the top 100 non-inert (noninC.json): floor 16.
- SA x4 (600 iterations; pool 1500 for seed 1, 4377 for seeds 2-4): all end at p17, 16/4.
Not done: srch.py r4sim targeting of the two blocks.
Left: the two hdd `log_printf(0,..); jmp` blocks. Ref asm lines 461 and 536; ours land at 394 and 554.
