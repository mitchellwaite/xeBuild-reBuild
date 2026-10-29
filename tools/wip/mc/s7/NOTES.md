# mode_client, 7th session (2026-10-28): loop-exit hypothesis checked against predict.c, NO MATCH

## predict.c (gcc-6.2.0, official gcc.gnu.org git, read via the built-in browser; curl hits the Anubis bot page)
`predict_loops`, PRED_LOOP_EXIT:
    probability = (REG_BR_PROB_BASE - hitrate(LOOP_EXIT)) / n_exits;
    if (probability < HITRATE (2)) probability = HITRATE (2);
So 2% is a FLOOR: more exits can only raise the probability towards 11%, never below 2%.
The s6 hypothesis (more distinct exits -> exit prob < 2%) is refuted.
Only PRED_LOOP_ITERATIONS (constant niter, 1/niter, max-predicted-iterations=100 -> >=1%)
or a first-match predictor ranked above LOOP_EXIT (BUILTIN_EXPECT = 50% with our param)
can override it; neither is available without changing code.

## Empirical (-fdump-tree-profile_estimate-details on the draft)
Latch bb 104: "first match 98.0%, loop exit heuristics: 98.0%" (DS would be 95.2%).
The other ~19 loop-exit predictions sit on noreturn (client_usage) blocks and are ignored.

## spec1.py (10 variants, `python tools/wip/mc/s7/batch.py tools/wip/mc/s7/spec1.py`)
| variant | f | pre | keys |
|---|---|---|---|
| g_e_p / g_ee_p (E(argc<1) guard) | 228 | 1 | u2 gone |
| g_*_d (same + E(!(mode&&arg))) | 164-312 | 3 | av/xb -4 but Bl -3 |
| g_lt_p (argc<1 && !promptEnter) | 104 | 3 | u2 0 |
| loopE / loopNE (expect on loop test) | ~800 | 0 | loop goes 50% |
Every E(!(mode&&arg)) dispatch also makes Block -3 (> 2), so even an ideal u2 ~3 would not
give the original order with that dispatch: the window is closed from the Block side too.

## Next angle
Not the loop exit.  Need a d (dispatch freq) in ~70-87 with the hot layout intact, from a
source predictor combination not tried yet, or accept 15/16 (park mode_client in asm).
