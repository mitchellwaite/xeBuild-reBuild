# s53: round 2 fixed (fail-path order); rounds 3-4 unchanged

Result: NO MATCH. New best by event score: **c_r10.c** (= s52/c_t2A + one line):
es 308 (R1 2, R2 12, R3 58, R4 128), **es2 300 (R1 2, R2 0, R3 56, R4 172)**, ev 56, fncmp 222.
Best by ev is still s47/H5c2.c (ev 5 / fncmp 34 / es 348 / es2 488).

## Task 1: fail path below the 105 trace (done)
- Round-2 start order uses the key of the edge from a trace end (priority*100000 + freq), so raising 105's
  block freq via tree-only edges does not help (edge 100->105 stays 58); the fail edge 102->143 must drop below 58.
- Lever: in the NO_MODE_ARG then-branch, before `if (reboot) {`, a tree-only bcp goto to a label put on
  `if (E(reboot)) netReboot` (after the switch):
  `if (__builtin_constant_p(mode + 93)) goto dtg;` ... `dtg: if (E(reboot))`.
  Diverts stale tree freq away from the reboot netConnect: 103 20 / 143 51 (< 105's 58); R1 untouched.
  Same with target netDisconnect (nd_r11, R2 es 11/es2 7) or E(bcp). Before the NO_MODE test or into netConnect
  (nc2) it wrecks R1. v1-v4.py hold the scan (t.py applies substitutions to c_t2A, prints R1 keys + R2 first traces).
- es2.py: es with all block ids canonicalized by first appearance over the whole history; removes the 109 vs
  anonymous-id naming noise (c_r10 R2 = 0). R4 counts rise under es2 (renaming cascades); compare es2 to es2 only.
  dd.py/dd2.py print per-round diffs.

## Task 2: R3/R4 hill-climb on c_r10 (sa3.py, cost es2 + W*ev)
- 3 runs x 1500 s (~4600 compiles, sa_s53a{1,2,3}.jsonl): best es2 289 (R4 161) with t48 levers, ev 52;
  **R3 never moves (56)** with any lv lever. Full rok JMP (all 16 labels) -> es2 443 (R2 29).
- R3 diff: match's first R3 trace is the reboot success block (102) whose BUILD_FDO rok dispatch inserts
  117/130/114 and re-keys 112/115/103/132; then case blocks pushed with priorities 9..2. Plain rok asm goto gives
  even probs. Next: per-case fake-label weighting on the rok dispatch (several clobber-only fakes per case label,
  as in s52's fallthrough construct but targeting the case labels) to reproduce those priorities.

## Task 3
No candidate matched fncmp; cm/objcmp not run (nothing to verify).
