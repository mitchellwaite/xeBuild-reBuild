# s62: TH lever (jump-threading assignments make switch dispatch edges uneven); NO MATCH

## Lever
`if (__builtin_constant_p(mode+X) && ...depth...) mode = V;` placed directly before `switch (mode)`.
vrp1/dom thread the then-arm straight to case V; update_bb_profile_for_threading lowers ONLY the
V dispatch edge (others renormalised up); fab later folds bcp to 0 and the arm vanishes (no code).
So unlike PD (which lowers the whole dispatch block), TH gives per-case uneven dispatch probabilities,
the thing s61 said gcc 6 can't do. Verified: depth 1 on c11 removes its whole dispatch edge (111:4 -> gone).
Deeper depth = smaller cut (F/2^d, clamped). Integer freqs are tiny (dispatch edges 4), so granularity is coarse.

## Runs (sa.py = s61 SA + TH; R3W=2; 4 x 3600 s, ~5200 evals each)
| file | es2 (R1,R2,R3,R4) | ev |
|---|---|---|
| best_a.json/.c (from fin0) | 156 (2,0,19,102) | 61 |
| best_b.json/.c (from fin0) | 155 (2,0,21,97) | 60 |
| best_c.json (designed init des.json) | 160 (2,0,20,104) | 59 |
| ev_d.json/.c (from fin2, min ev) | 193 (2,0,27,123) | 39 |
New es2 best 155 (was 159), new ev best 39 (was 43). R3 barely moves (19-21): reductions alone can't
reach M's 9..6 ordering above s5/s4 (prio 3) because our dispatch edges start at only 4.

## Next
- Combine TH with raising dispatch-block freq first (so edges ~9 then cut down to M's 9/8/7/6/1 profile);
  a designer on fq.py output per TH depth (measure edge cut per (case,depth), then solve) instead of SA.
- TH with a threading value that hits a case via a *different* path (e.g. mode=V set in a rok chunk) to
  add, not only subtract.
