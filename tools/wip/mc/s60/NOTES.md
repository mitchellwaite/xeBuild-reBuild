# s60: full-length SA from s59 best179; NO MATCH

sa.py = copy of s59/sa.py (logs here). Round 1 (4 x 5400 s, ~7900 iters each): a/b R3W=1 from best179, c R3W=3,
d R3W=1 from s59/init_s56.json. Round 2 (e/f/g/h from best169: R3W 1/2, FIX t4,_ft,c12,c8 pinned, T0=2) was
stopped early on hand-back.

## Results
- **best169.json / f169.c: es2 169 (R1 2, R2 0, R3 25, R4 103), ev 54, fncmp 177, cm (15, 24)** (from c, R3W=3).
- a best 175 (R3 25), b 178, d (s56 seed) 187. Max-ev R2-0 state bestev.json/fev.c: ev 105 but es2 250, fncmp 178.
- SA plateaued: 28k R2-0 evaluations, no state below 169.
## dd2 R3 diff (f169)
Within the B60..B76 group the block order differs (T: 69,64,74,65,... vs M: 70,64,72,71,74,69,...), and
iB83/cB80-82 are hoisted in T (M keeps cB83/84 after GB47); B66/B58/B59 are v (fallthrough) in T vs p in M.
Suggests a lever on the case-group order of the B60-B76 targets and on B83 placement; not implemented.
## Next
Add a lever permuting the B60-B76 targets (and B83 position) then resume SA from best169.json.
