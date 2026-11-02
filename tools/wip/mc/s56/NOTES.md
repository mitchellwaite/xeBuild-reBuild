# s56: rok fakes to case-4/5 test blocks (t4/t5) + joint SA; NO MATCH

Best by es2: **c_s56.c** (state best.json) = c_r10 levers + chained rok asm (sa.py rok2, which also accepts fake
targets t4/t5 = case-4/5 hwFlags test blocks 113/110):
w {t4 4, t5 4, _ft 5, c12 1, i0 1, c8 2, s5 1, c1 1}, cap 29, X {c2 1, c7 4, c11 3, c3 1}, custom chunk order:
**es2 199 (R1 2, R2 0, R3 26, R4 131)**, ev 57, fncmp 211 (es2/fncmp via es2.run fncmp=True; tools/re/fncmp.py on a
wip path fails to find xebuild.h). Previous: s55 230 (R2 1), s54 239. Best ev still s47/H5c2.

## Findings (~6500 real compiles, 4 race-free SA workers, logs sa_s56*.jsonl, old/)
- Idea 1 (s55 weights + npre/order, R2 hard-constrained): from the s55 R2=1 point the SA never reached R2 0 (1150
  compiles); R2=0 side from s54 weights stalls at 239. Weight sets with R2 0 exist only near small rok totals.
- Idea 3 key lever: t4/t5 were never rok targets. Fakes to t4/t5 raise 113/110 above the other case heads within prio 4
  without raising join: {p0 1,c3 2,t4 4,t5 4} alone gives es2 226 / R3 26. All good states use t4/t5 4.
- R3 remaining: case-head freqs only take ~3 integer levels (4/6/7; rok flow is small), so graded match keys 910..205
  collapse into ties; the head Cha section (match pushes 112/115/103/132; ours 117/130 = p0/i0 rok targets) differs.
- hsim.load writes bbro_mc.txt into build/mcmatch/slotm at es2 import: start parallel workers staggered (>=5 s).
- Idea 2 (fake edges from round-2 trace ends to case heads for distinct prios) and idea 4 (R4 levers) NOT tried.
## Next
Raise rok flow (more scale -> more freq levels) e.g. place rok on a hotter path or feed it from the boosted loop; then
idea 2 for prios; then R4.
