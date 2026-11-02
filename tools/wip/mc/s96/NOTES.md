# s96 (attempt 77): NO MATCH. ~260 measured variants (log.txt; v1-v5.sh, ccs sweeps p14.log on a14, pk4.log on k4).
Best unchanged at 26/6/5; best_s96.c = b01 = d01 minus the JMP(i0) in s4 (identical score, one hint fewer).
- Round-4 keys are tiny ints (-freq), so Blk(140)/CU108/-r order is a pure fib-heap tie: d01 140,108 at -3, 55 at -2;
  k4 has all three at -3 and still extracts 140,108,55. r4sim on k4: 140=-2 puts it after 62 (139/62 tie wins);
  wd.py dummy pushes/inserts on k4 bottom out at 4 (same as s95).
- Blk freq 2 via any dead edge into efail before the range test (a08/a11/a14/a16/a19): order CU108 -r Blk -w (Blk
  right place) but Fer drops to freq 0 and zero group scrambles (46/10/22); ccs on a14 best inv 15.
- Edge into eout before the tests (a06/a10/a15/a17), removing eerase->einv (c02): Blk freq 4 (36/8/10).
- Conjunct count / (char*) form of esucc->eout goto: Blk 2, zero group broken (a01-a04, 42-50/10/18).
- Inert (26/5): JUMP(efail,esucc), extra einv edges (c03-c07), JMP(i0) removal/dup (b01,b05), JUMP(i0) dup (b04).
- Harmful: dropping einv/i0/p0 cold labels (c01, b03, b06), dropping JMP(p0) in c12 (b02).
Next idea untried: make Fer keep freq 2 while Blk gets freq 2 from an efail edge (e.g. second efail edge from
the success path), then fix the Fer/Blk tie and zero group.
