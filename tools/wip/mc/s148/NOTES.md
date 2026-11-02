# s148: alternative-solution enumeration + dummy levers + t6 climb (profile-free mode_client)

Base s146/t6.c (f2 16; r4 tail 150 147 79 128 81 42 53 35, target 147 128 150 35 42 53 79 81).
Tools: alt.py DUMP K (r4sim enumeration of up to K changes: dummy heap entries key 0/-1/-2 inserted
by any trace at any op position, key overrides -2/-1/+1 on 150 147 79 128 81 42 53 35 144 145 75,
removal of any existing ins/chg op), alt3.py (triples over the 228 non-redundant changes whose single
score <= 9), alt3b.py (every 3rd change on top of each best pair), dz.py (JMP(dz) sweep), t.sh, run.sh.

## 1. Model enumeration on t6's dump (535 changes)
- singles: floor 7. pairs (143k): floor 2, only {dummy key -2 by trace 144 (line ~699, -c `if (mode)`),
  dummy key 0 by trace 69 (c12 `arg == dummy`, line 785)} -> tail 147 79 150 35 42 53 128 81
  (79/128 swapped). triples (filtered, ~2M) and pair+any-third: floor 2. No solution reaches 0 with
  <= 3 changes of these kinds; nothing removes the need to move 128 relative to 79.
## 2. Levers
- dz.py: dead `if (0) { dz: [cold]; asm volatile(""); }` before mode_client's `return 0` + JMP(dz)
  before each of 94 statements (cold and plain): floor 17; the dz block pops early in round 4
  (position ~10, before 127) as its own trace, tail unchanged (renumbered only).
- manual (m0-m7): JMP(dz) in i0 arm (m1/m3) 29, tail 150 147 42 53 35 75 128 79 dz 81; i1 arm 87/35;
  plus JMP(dy) at line 700 (model's key -2 dummy) 82-102. alt.py on m1: singles floor 8.
  The model's trace-144/69 dummies are not realisable: asm-goto edges either fold, pop early, or
  change the inserting block's freqs and wreck the front.
## 3. Climb (s146/e gen/climb, base c/base.c = t6 + kk in clientEraseBlockI, inert 16/5)
6324 singles, top-100 non-inert pairs (4950), SA x2 (600 it): floor (16,5), nothing better.
All jobs stopped.
## Result
NO MATCH. Best f2 16 (s141/best16.c, s146/t6.c). Semantics: JMP = empty asm goto falling through,
dead if(0) blocks and dead kk reads; all variants equivalent to src/mode_client.c.
