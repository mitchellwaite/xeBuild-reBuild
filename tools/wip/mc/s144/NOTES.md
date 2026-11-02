# s144: fibheap-shape analysis of the round-4 f0 tail (front28 / c1), profile-free mode_client

Files: shape.py (dummy push / drop / swap edits in rounds 2-3), shape2.py (move a round-4 insert to
another trace group + dummy entries, singles/pairs/SA), shape3.py (permute inserts inside one group),
shape4.py (shape2 moves only), shape5.py (shape2 with env targets TT/TP), dv.py (dummy-absorption test),
mk.py (source variants), t.sh NAME (f2 + simulated r4 order), run.sh DIR (climb singles/pairs/SA),
fb/ f28/ c1/ (gen.py/climb.py ports, base.c = fb.c / front28.c / c1.c).

## 1. Model validation (MANDATORY step 1)
s86/r4sim.py already replays rounds 1-3 event by event on tools/wip/fibsim.py, which is GCC 6.2's
fibonacci_heap (insert into root list after root, extract_min with consolidate, replace_key =
decrease or delete+insert, delete_node). Checked: simulated round-4 order == real "Getting bb" order,
**exactly**, for s143/dd/front28, s143/dd/c1 and s142/dd/best16 (all blocks). So tie order is fully
modelled; no change to the model was needed (no need to read fibonacci_heap.h).

## 2. Shape search (step 2), target tail after 143: 62 33 29 69 146 128 151 35 42 53 79 81
Facts from the dumps (bbro numbers): 146 (LC114 einv) is inserted by the first r4 trace 139
(clientEraseBlockI entry); 128 (case-7 p0 clientPatches(NULL)) and 151 (case-12 i0 clientInfo(NULL)) by
trace 148 (case 12 dispatch; 128 via the `({JMP(p0); 0;})` edge); 79/81 (-c usage 3/5, crossjumped
with -r's r3x/r5x) by trace 55 in asm-goto label order (r5x first -> 81 before 79).
- Keys only (s143): floor 6. Permuting inserts inside groups (shape3, 1-2 groups, 146 key -1/0): floor 6.
- Dummy pushes/drops/swaps in rounds 2-3 (shape.py): c1 floor 9, front28 floor 4.
- Moving inserts between groups, no extra entries (shape4): floor 4 both.
- With extra heap entries (shape2/SA): **0 reachable**. Minimal c1 recipe (dv.py):
  (a) 128 inserted by trace 108 (u2 usage) or 121 (hdd4 log) instead of 148;
  (b) 81 inserted after 79 in trace 55 (= label order r3x, r5x);
  (c) one extra key-0 entry created by trace 143 (efail log) that stays in the heap until it is
      absorbed by trace 79/42/53 (a single-block usage trace) - no source form found: those blocks
      are already in the heap when 143 runs, so a re-insert only changes a key, not the shape.
## Source translation
- (b) `asm goto("" :::: r3x, r5x)` swaps 79/81 exactly as modelled (f_bac / front28_b).
- (a) dropping `|| ({JMP(p0); 0;})` from case 12 (a0): front28 28 -> 20; with (b): **fb.c f2 18**
  (front28 + b + a0). Residual: LC117/LC118 (143/144) swap (pop at the -2 tie) and the f0 tail
  149 146 79 128 81 42 53 35 vs target 146 128 149 35 42 53 79 81. Re-adding the p0 edge elsewhere
  (u2 before/after usage, hdd4 arm, -w arm, swapped c12 operand) 18..165, never better.
- shape5 on fb (TP "144 143", TT tail): 0 needs dummy at 108 + 128 from trace 62 + 146 key -1 (c1's
  einv freq 1, which on its own costs the front: c1+b+a0 = 78).
## 3. gen/climb
gen.py/climb.py (s141 port) on fb.c (6334 singles): stopped after ~1550 singles, none below 18.
front28 base: ~370 singles, none below 28. c1 base (76) dropped in favour of fb. Pairs/SA not reached.
Resume: `NJ=4 sh run.sh fb` (the cache in fb/v is reused).
## Conclusion
NO MATCH. Best f2 still 16 (s141/best16.c). New fb.c (front28 + r3x/r5x swap + no c12 JMP(p0)) is 18:
it gets parts (a)+(b) of the modelled recipe. Part (c), one more key-0 heap entry created during the
efail trace and kept until the usage traces run, has no source form found, and the 143/144 tie flips.
## Semantics
b swaps the labels of an empty asm goto (falls through); a0 removes an empty asm goto from the c12
condition (it never jumps). Both equivalent to src/mode_client.c.
