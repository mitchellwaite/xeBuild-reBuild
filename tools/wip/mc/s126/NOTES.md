# s126 (attempt 107): NO MATCH. Floor stays f2 18 (s117/best.c).

Tools: gen0.py (= s125 gen.py on b18.c), run0.sh, batch.sh LIST (4-parallel run + round-3/4 traces),
climb.py TAG ROUNDS EDITS... (greedy climb over JMP(...)+label additions and predictor feeds/hot labels).
base.c = s125 kf_7 rebuilt by gen0: Hs Lk Ls2 R=krb E=kky,4 E=ks2,3,30 E=krb,1,60 E=ks2,1,40 (f2 144).
res.txt has ~950 measured variants. All edits are dead constant_p gotos, labels, hot labels or extra
asm-goto labels (empty template, never jumps): equivalent to src/mode_client.c.

## Results
- kky feed length 5/6/8/10: saturates, 48 stays f13 (144). Stronger krb feed: 46 f10, worse (150).
- Hk (hot -keys arm, 93/7): 48->49 drops to ~1 but 96 joins 48's r3 trace (old equilibrium) -> 160.
- Li + kipt feed (-ip test dominance-off): 49 f7 as in prof, prio 7, f2 120 (best of kf_7 family);
  Li+Hk 100. Prof round 3 kept, but 49's trace lands right after 141 (prof: after 136).
- Adding a label to any existing JMP(...) on the Li base: JMP(x,c1) best, 96; the climb from there
  falls into the 48+96 merged-trace equilibrium and ends at 18.
- Climbs from b18 (no edit < 18) and from r_2_1 (K=kky,1 gives 18 = b18 equilibrium, then plateau).
Conclusion: every path that keeps prof's round 3 stays >= 96; everything better collapses to b18's
equilibrium at 18. The prof round-4 priorities of the switch-case blocks remain unreachable: the
predictor levers only move the front blocks (48/49/46), not the case arms' trace-end priorities.
