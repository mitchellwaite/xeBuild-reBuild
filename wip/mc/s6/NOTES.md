# mode_client, 6th session (2026-10-28): frequency-budget analysis, ~110 variants, NO MATCH

Tools (run from repo root): `python wip/mc/s6/batch.py wip/mc/s6/specN.py` builds each
(old,new) replacement variant of the draft, prints fncmp lines (f, draft=56), mcvar inv/pre and
round-4 heap keys of u2=usage(2), av/xb=HDD errors, Bl/Fa=erase Block/Failed, -r.
`keys.py V.c` prints all round-4 trace starts with keys; `tr.py V.c` rounds 1-3 traces.
(g.py/sw.py: single-variant helpers; their output paths are wip/mc/s6/v_*.c.)

## What the original needs (keys = -freq; round 4 extracts the smallest key)
Original round-4 order: -ip(7) av xb u2 -r(2) Bl Fa -w ...  -> av,xb >= u2 >= 2 and Bl <= 2.
Draft: u2 4, av/xb 2, Bl 1.  Loop-internal keys (-ip 7, -r 2, usage3/4/5 0-1) never move.

Budget (draft): entry 214 = 10000 x loop-exit 2%; u2 = 214 x 2% = 4.28 (all of it from the
threaded entry edge; post-loop noreturn edge = 0).  Post-loop 196 splits at the folded
`(mode==0)|(arg==0)` test by the call heuristic 71/29 -> switch side 58, dispatch 56, case 4.3,
HDD 2, Block 1.  Measured: HDD ~ d/26, Block ~ 0.026 d (d = dispatch).
- HDD >= 4 needs d >= ~91; Block <= 2 needs d <= ~94 (narrow window) ...
- ... but the hot layout (reboot side reached by fallthrough, traces 98/99 then 100/101 in
  round 1) needs the reboot side >= 107 (round-1 threshold = 214/2), i.e. switch side <= ~89.
  Every variant with P(switch) >= 50% flips the layout (f >= 108).
- So with u2 = 4 there is no consistent P; u2 must drop to ~3 *and* d rise to ~70-87.
  Available probabilities are only 0 (noreturn/cold), 2 (loop exit), 29/71 (call), 50 (E with
  param 50): no knob gives u2 ~3 or switch ~40-45%.

## Results (all f != 0)
| spec | variants | best |
|---|---|---|
| (s6 singles) guard `if (argc<1) client_usage(2,NULL)` before loop (guard1-4) | 4 | u2 -> 0 (pre=2), only content diff = i=0 store sched; order then wrong (u2 too cold), f 254 |
| post-loop E() forms b1-b5, swapped branches s0-s3 | 9 | E(!(mode&&arg)): pre=4 (-ip av xb u2 exact, keys 4/4/4) but layout flips, Bl -3, f 116 |
| spec1: 12 conditions (E on mode/arg parts, ==NULL, <=0) | 12 | none keep layout with d raised |
| spec2: 4 conds x 9 mods (rok/fail cold removed, E(netConnect), cold u2) | 36 | e_n1 pre=4 inv 17 f 172 |
| spec3: 3 guards x 4 conds x 3 u2 forms | 36 | nothing new |
Earlier this session also confirmed IDA/Ghidra structure = draft (5th session note); orig
entry `jle` goes straight to usage(2), same CFG as ours.

## Next angle
Something that makes the loop-exit probability itself smaller than 2% (n_exits in
predict_loops: 1500/n with n=7 here?) without changing code -- e.g. more distinct exit edges at
profile time that later merge (tail-merge/crossjump).  That lowers u2 quadratically (10000 p^2)
but HDD only linearly, while loop-internal keys stay; combined with E(!(mode&&arg))-like
d this could open a window.  Needs predict.c (gcc.gnu.org git was bot-blocked this session).
