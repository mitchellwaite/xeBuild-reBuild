# s66: 1114/109 push, post-loop compensation lever, source-structure check; NO MATCH
Base: s64/best_d (es2 156 = R1 2/R2 0/R3 18/R4 104, fncmp 158). Tools: cp.py (best_d + POST + compensation
gotos), tm.py (text substitutions on best_d + rk.py R3 dump), th.py (drop each TH/PD entry), x3.py (c3 knobs).
## 1. 1114/109 wrong push (rk.py region 3)
- canonical 109 = clientKeys (case 3). In ours case 3's head is the `JMP(hdd5,s5)` asm-goto block (copy id 1114,
  key -1000403) and clientKeys falls through at freq 1; in M 109 itself is the case head (key -1000809).
- Fix: move the JMP after the call (`{ clientKeys(); JMP(hdd5,s5); }`, o_k2.c) or drop it (o_k1.c): 109 is pushed
  directly, but R3 stays 18 (k2) / 22 (k1) and R4 rises 104 -> 120/124 (es2 172/184). The wrong push is cosmetic
  for R3; R3 is the even dispatch keys (-1000408..403 ours vs -1000910..610 in M).
- No TH/PD entry or c3 X/w/TH knob removes 1114 (all no-ops or worse).
## 2. Compensation lever for POST (dead i/argc-bcp gotos from loop top / pre-loop into post-loop labels
   cpnm (then-branch of NO_MODE_ARG), cprb (reboot test), cpnc (else netConnect), dtg, ndl; depths 1-6, combos)
- POST 2 alone: es2 567 (R2 40). Every single or combined compensation goto made it worse (es2 686..965,
  R2 59..92, R1 also up to 14-30). Dead loop gotos add new merge blocks rather than restoring the halved
  post-loop frequencies. Lever is negative; POST stays a dead end.
## 3. Source structure
- Linux xeBuild64 (v1.16) has no network client modes: no cross-check possible for mode_client.
- M's uneven dispatch probabilities (9..1) on a jump-table switch cannot come from gcc 6 plain compile source:
  switch edges get even probs without profile, gcc 6 has no if-chain->switch conversion, and a
  `__builtin_expect` on the switch value lifts only one edge. Case order/shared bodies don't change edge probs.
  This is strong evidence the original was built with -fprofile-use, so a plain-compile match needs a
  lever that produces per-edge uneven switch probabilities (none found in 66 attempts).
## 4. SA: not run (no lever moved R3 below 18).
