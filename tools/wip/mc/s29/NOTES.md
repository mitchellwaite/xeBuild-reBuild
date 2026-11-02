# s29: match-history features in hsim + realizing X2/T48/RX in the PLAIN compile

Result: NO MATCH. Best real plain compile still g7b (best_g7b_dup.c): 7 true inversions, fncmp 27.
Tools = s28 copies (paths -> build/v/mc29, deleted at the end; `mkdir -p build/v/mc29` and rebuild
slots with `python m.py SRC TAG` / `sh tools/wip/mc/s18/match/repro.sh` + copy build/mcmatch/slotm
to build/v/mc29/slot_match).

g7b's 7 inversions: 112 too late (5: after 103 126 55 125 61), 126/55 (1), 77/53 (1).
(k94 placement is NOT a diff in g7b; fncmp shows only those hunks + one scheduling hunk.)

## (1) hsim models
- ed4.py (on the s18 MATCH history; log ed4.log): revert match features to the g7b form one subset at
  a time + f search.  A = 112 as round-3 priority push and B = 115 the same are ESSENTIAL (revert
  either -> >= 9); C (103 prio) and E (130 inserted at rok) are free (CE still 0); D (117 at rok) 3,
  F (125 rekey @126) 2, G (130 rekey @117) 3, H (49 priority) 3 alone.
- ed2/ed3/ed5/sa.py on the g7b history: pushing 112/115 (+117/103) in round 3 with priority keys,
  49 priority, RX re-keys, SA over f and P: best 8 (ed5.log, sa_ab*/sa_abrx*).  The tail becomes
  nearly perfect, but the extra round-4 heap nodes reshuffle the P4/f4 case-prefix ties
  (prefix depends on the NUMBER of nodes, not where the pushes happen; dummy nodes don't fix it).
- psa.py / sa.py on REAL X2 histories (see 2): with 49 priority (H) + RX the tail is perfect;
  only the case prefix (ties) and 112's trace absorption remain:
  * r1 (rok X2 = match list): sa_r1h best 16, all from the prefix (108/116 too early: f7 vs 110/113 f4).
  * c_all (X2 + RX + T48 realized): with case f/P free -> 0 (sa_call_*): history admits a match
    but needs distinct case P levels like the match profile.
  * dfull (X2 + h4t/h5t labels + RX + T48): psa best 5 = only 112 missing (110's trace absorbs
    112 once 110's freq rises); everything else orderable with case f in 4..10, P129 9-10, P132 3.

## (2) plain-compile levers (all real compiles, des.py harness)
- X2 at rok (`JMP(...)` instead of the empty `JUMP(...)`; s28's "rok JUMP +s4 no-op" was because
  JUMP expands to nothing): reproduces the match's round-3 structure (1102 inserts 117/130/112/115,
  re-keys 103) with P2 for the targets.  Labels `h4t:`/`h5t:` on the case 4/5 hwFlags tests are
  harmless (g7b still 7/27) and let X2 raise 110/113.
- T48 realized: label k48l before the -keys test (else-if chain wrapped in `else { ... }`),
  toggles -wb/-eb E() off, and `if ((char *)__builtin_constant_p(i + 10) == (char *)1) goto k48l;`
  at the start of the -s body -> f48 12, rekeys 94 P9/f9 and 49 P3/f3 (inj48b.jsonl; loop-top
  injections are far too hot, f48 in the thousands).  Round-3 threshold: 48 at 9 is not a trace
  start, 94 at 11 is still followed, 8 is not.
  Problem: 94 (P9) then pops before 129 (P4) and before all cases; 49 P3 pops before 132 (P2).
- RX126 (last `JUMP(efail)` -> JMP, inlined copy) / RX117 (`JUMP(i0)` -> JMP) work (125 P2).
- A single-target first JMP level (e.g. `JMP(c12); JMP(...)`) makes rok's trace absorb the target
  (129 disappears); chained JMP levels give geometric shares, too coarse for the 3-4 integer f
  levels the prefix needs (rok freq 41, dispatch gives every case P4/f4).
- Searches: rokscan (all 1-2 extra rok targets on g7b): best 18; rsa.py (rok JMP lists + E toggles
  + RX, 4x~1000 compiles): stuck at 7; dsa.py (chained rok/X1-site JMPs, rx, t48; 9 runs, ~5300
  compiles, from empty and from the full X2 list): best 23-24.

## Next ideas
- The tie-free route needs distinct case priorities: source of 3-4 graded P/f levels for case
  heads besides rok (e.g. several asm-goto sites on paths with different frequencies, each giving
  one level), plus P129 > P94 (or T48 with f94 < case keys) and P132 >= P49.
- Keep 110's trace off 112 when h4t raises 110 (raise hdd4 arm 1113 without raising 112).
