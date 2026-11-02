# s112 (attempt 93): NO MATCH. Best stays s102/best.c (f2 24).

Goal: reproduce the profiled build's round-4 priority ladder (s111) without the profile.
Tools: run.sh (f2 + round-4 pop order with each block's last (prio,freq) key, via keys.py),
gen*.py (variant generators), w1.py (r4sim what-ifs). b0.c = copy of s102/best.c. log.txt has all runs.

Why best has no ladder (analysis):
- gcc 6 sets even probabilities on every >2-successor block without a profile (combine_predictions_for_bb
  returns early for nedges != 2), and expand_case keeps those per-edge. So every switch edge out of dsp
  (freq 46) is ~46/13 = 3.5. Case labels per edge, grouping, or a dead extra case can't make them
  unequal. Priority is the max EDGE_FREQUENCY over preds that are trace ends (or DFS back edges), so
  only the switch block (and case blocks that end traces through the JMP() inter-case edges) give
  priority. Feeds from the rk/fkbo asm-goto weight tables add frequency, not priority, because those
  blocks are mid-trace.
- So the "dilution" in best is not the issue (freq is already about prio+1..+4). The issue is that all
  switch edges are equal and the absolute scale is too small (prio 3-5) to give a 10-step ladder.
Variants (54 real, all f2 >= 24):
- p_/m_*: +-1 rk weight per case target (18): f2 24 (most, keys unchanged: rk is ~20 freq / 52 units,
  so one unit is < 1) or 46-56.
- f_*: drop one case label from the fkbo asm goto (5): 38-50 (f_c10 = 38: 129 before 134).
- d_*: +-1 `asm goto dsp` back edges in c1/c3/c9 (6): 24, keys unchanged (no effect on dsp's freq).
- g1..g12: dead k-conjunct cp `goto dsp` at the loop head to scale up dsp (12): 142-204. The extra edge
  restructures earlier passes; even k=12 (no freq change) is 166. Scaling dsp's freq this way is not
  viable.
- q_*: fkbo fa slot retargeted to a case (weight table on the hot path, 12): 56-134. Raises case freqs
  and pushes 141 into round 4 at f9, but no priority ladder (q_lad: prios collapse to 2).
r4sim (w1.py on best's dump): pushing 141 into round 4 with any key in (2..3, 5..10) x 134/126 overrides
gives dist >= 7 (tail reshuffle), vs base 3. Same as s111.
Conclusion: a per-case priority ladder isn't reachable without a profile: switch edges are equal by
construction, and the levers that add per-case weight (rk/fkbo tables) add frequency, not priority.
The only ways to change priority are dsp's total frequency (uniform for all cases; the dead-goto way
breaks the code) and the JMP() inter-case edges (already used). Floor 24 stands.
Semantics: variants only change targets of never-taken empty asm-goto labels, add or remove empty
asm gotos, or add dead __builtin_constant_p gotos. Equivalent to src/mode_client.c.
