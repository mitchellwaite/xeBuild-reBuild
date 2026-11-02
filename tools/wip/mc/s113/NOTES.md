# s113 (attempt 94): NO MATCH. Best is still s102/best.c (f2 24; b0.c is a copy).

Tools: gen.py (variants: c11=N conjuncts, j:POS:LBL empty asm goto), run.sh (f2 + round-4 keys),
kc.py / kd.py / kv.py / kh.py (r4sim searches on a dump), sa.py (real SA over every dead-cp chain's
conjunct count plus optional empty asm gotos), sa1..4.log + sa*/best_*.c, log.txt.

Main finding: the premise "best has no ladder" doesn't hold up. r4sim on best's dump: best's round-4
order already matches the profiled order for the whole front (142 113 116 119 122 134 115 129 131 ...
126 147 105 49 125 121). The f2 of 24 is exactly three misplaced blocks (asm diff, b0.d):
141 clientBinPatch (built in round 3, but the original builds it in round 4 between 131 and 126),
139 log_printf (pops before 108/55) and 145 clientInfo(NULL) (in the tail).
So a key ladder isn't needed. Hill-climbing key overrides on the case blocks never gets below
r4sim dist 3 (= base).
- Fail->c11 dead-cp conjunct count 4 (k4.c) or 5 pushes 141 into round 4 with key (3,6)/(3,5), at
  exactly the right front position. But the extra round-4 heap node reshuffles the fib-heap tail:
  f2 56 (r4sim dist 7). Same with JMP(c11) at p1/c8/c2 (b_*). An extra case-6 block (a_c6_c11) gets
  f2 31: 141 is correct, but it adds a jmp block, and 139 plus the client_usage blocks are still off.
- r4sim on k4 with abstract edits (extra round-3 pushes of blocks that round 4 visits, key overrides;
  extras penalised): floor dist 1 with 2 edits; 139 always pops before 55 (139 is inserted at -3 by
  134's trace, 55 at -2 by 49's). Moving that key breaks something else.
- Real variants: about 45 hand-made (k*, a_*, b_*) and about 1800 SA evals (4 chains, from k4). Floor
  26 (c7-target asm goto at i1); k4-family 56. Never <= 24.
- Renumbering the constants in the dead-cp conjuncts (same counts) changes f2 (52 vs 56), so the
  constant values themselves are a noise source.
Semantics: variants only change conjunct counts of never-true __builtin_constant_p gotos or add
empty asm gotos (never taken). Equivalent to src/mode_client.c.
