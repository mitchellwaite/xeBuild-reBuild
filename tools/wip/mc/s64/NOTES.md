# s64: dispatch-raising levers + SA; NO MATCH

## Probes (m1.py, q.py = s62 text + mod, es2 + fq table; base s62/best_b, dispatch bb111 freq 46, edges 4)
Label `dsp:` right before `switch (mode)` (after the TH chain), dead bcp gotos into it from:
- `-v` arm in the option loop: no effect (arm freq ~0). Using `mode` there after `mode = 7` is a REAL goto
  (bcp(7+k) folds to 1) - use non-constant vars (argc, i).
- pre-loop (before `for`): mode == 0 there, so vrp/dom thread the goto straight to cdef; dispatch stays 46.
- loop top (i bcp): depth 3 only -> dispatch 82 (edges 7) but R1 10/R2 55 and fncmp +80 (loop exit changes
  loop estimates); depth >=4 no freq change but fncmp still +26 (content change).
- backedge after the switch: no freq change at any depth (es2 224-250, content changes).
- loop-top goto to a label before `if (NO_MODE_ARG...)` (scale whole post-loop region): bogus case-head
  freqs (c12 29..42 via threading), es2 >= 244.
- POST (before `if (NO_MODE_ARG...)`, argc bcp): WORKS: depth 1 dispatch 112 (edges 9!), d2 75 (6), d3 53 (4),
  d>=4 ~no change. But it steals (1-2^-d) of every other post-loop block: d1 es2 794, d2 532, d3 299 (R2 broken).
## SA (sa.py = s62 + POST/LT levers, 4 x 4800 s, ~6900 evals each)
| run | start | best es2 (R1,R2,R3,R4) | ev | fncmp |
|---|---|---|---|---|
| a free+LT | best_b | 155 (no gain) | | |
| b POST 2-3 forced | best_b | never R2 0 (1303 cost, es2 245) | | |
| c POST 3-4 | best_b | best_c 160 (2,0,22,100) POST 4 | 57 | 172 |
| d free R3W=3 | best_a | best_d 156 (2,0,18,104) | 57 | 158 |
No es2 improvement (155 still best); best_d has lowest R3 so far (18).
## Read of R3 tokens (s61/rk.py q0 3 vs m 3)
es2 tokens carry no keys: R3 diff is which heads are VISITED vs pushed (ours visit 128 c11 freq 37 - stale
tree freq from fail/PD gotos - and 132), 1114 pushed instead of 109, and 1103's insert list. So equalising
prio alone is not enough; c11's inflated freq (fail `goto c11`, PD c11) makes it a trace continuation.
## Next
- Make POST usable: compensate the stolen post-loop flow (e.g. a second POST-like goto from the dispatch
  region back into the NO_MODE_ARG side is impossible w/o loops; instead re-tune rok/E2 at scale 1/2 with a
  dedicated SA that only allows POST 1-2 and a softer R2 penalty).
- Remove the c11 visit: drop/reduce fail `goto c11` and PD c11 depth so c11 head freq ~ dispatch share.
