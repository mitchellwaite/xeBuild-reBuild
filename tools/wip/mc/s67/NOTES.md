# s67: switch-edge probability levers; NO MATCH
Base s64/best_d (es2 156, R3 18). Short session.
## Idea 3 (predictors on case bodies) - negative, measured
Tiny test (6-case switch, -O3, -fdump-tree-profile_estimate-details): case labels with
`__attribute__((hot))` / `((cold))`, a case body calling __builtin_abort (noreturn) and one with
__builtin_unreachable: switch edges stay exactly even (14.3% each; unreachable/abort cases are just
dropped). gcc 6 combine_predictions_for_bb uses even probabilities for nedges != 2, so no label/call
predictor can give uneven jump-table edges. (predict.c fetch from gcc.gnu.org blocked by Anubis again.)
## Idea 1 (extra trace-end preds into case heads)
This is what the rok asm-goto fan (ork* multiplicities to c1/c8/c11/c12/i0/p0/c10/cdef/c3/hdd5/u2/s5/t4/t5)
already does (s54-s57, SA in s60-s65). rk.py region 3, ours vs M:
 ours pushes 129,116,107 (-1000408), 113 406, 119/108/120/121 405, 128 404, 1114 403, 132 209, 110 203
 M    pushes 129 910, 109 809, 107 809, 113 808, 110 808, 119 709, 108 709, 120 708, 121 707, 128 610, 116 609, 132 608
 In M keys strictly decrease in push order and head freqs are 7..10 (dispatch total ~90 vs ours ~48):
 the gap is overall dispatch flow (x2) plus a monotone per-case prio, not just tie order. Raising dispatch
 flow is only achieved by POST (s64), which breaks R2. No new lever found.
## Idea 2 (two-level dispatch) - not compiled; an if-guard before the switch only scales total flow, and
 peeling a case out of the switch changes the table (entry -> default), so it cannot keep one table.
Best unchanged: s62/best_b (es2 155), s64/best_d (es2 156/R3 18).
