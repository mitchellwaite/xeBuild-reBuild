# mode_client, 8th session (2026-10-28): systematic predictor search, NO MATCH (still 15/16)

Tools: `batch.py SPEC` (s7 runner writing here), `pe.sh VARIANT.c` (profile_estimate
predictions for the post-loop blocks), `flags.py [SRC]` (param/flag sweep).
76 experiments (spec1-7 + 19 flag sets).

## Predictors found (profile_estimate-details)
- combined `!(mode && arg)` (ifcombined `mode==0 | arg==0`): only PRED_CALL, 71% to the
  reboot side -> dispatch share 0.29 (d=56).  `mode>0`, `mode<=0` etc. change nothing
  because the test is a BIT_IOR of bools.
- splitting the test (`!mode || ({__asm__("");0;}) || !arg`, keeps one test each in asm):
  mode test: `==0` none (50%), `<=0`/`<1` OPCODE_POSITIVE 73%; arg test: TREE_POINTER 15% +
  CALL 71% -> DS 30.2% to the reboot side.  E() on either gives exactly 50%.
- HDD bit tests: CALL 71/29 cancel -> 50%.  `== 0x20`, `>>5 &1`, `>= 0x20` fold to `!= 0`
  before the estimate; `(int)(.. & 0x20) > 0` OPCODE_POSITIVE favours the success arm;
  inverted (`(int)(~flags & 0x20) > 0`) makes the error arm 73% -> it becomes the in-trace
  arm (key None).  Forward user gotos get no PRED_GOTO here; only source block order changes
  (error arm becomes fallthrough).  `__attribute__((cold))` on sendAvatarData/sendCompatData:
  same (error arm in-trace).
- switch: predict.c (6.2.0) `combine_predictions_for_bb`: nedges != 2 -> set_even_probabilities,
  plain 1/nedges, no unlikely-edge exclusion (that is gcc 7).  13 edges -> 1/13 each.

## Results
| spec | variants | best | note |
|---|---|---|---|
| 1 | mode/arg opcode forms, netConnect `>0`/`==1`/`>=1` | base (f56) | combined test unaffected; `>0` changes code |
| 2 | split post-loop test (asm stmt) | sx_le av-4 Bl-3 inv18 | dispatch 0.51 flips hot layout (f110) |
| 3 | split + E()/pointer forms, 15 | le_neg = sx_le | E -> 50% tie also flips hot layout |
| 4 | cold callees | - | HDD error arm goes in-trace |
| 5 | goto'd success arms (+split) | - | same |
| 6 | HDD test opcode forms | - | folded or wrong direction |
| 7 | inverted HDD test (+split) | - | error arm in-trace |
| flags | expect 45-60, hot-bb-frequency-fraction, predictable-branch-outcome, -O2, no-thread-jumps, no-dom | base | -O2 f123; no-dom u2 0 |

## Why the window is empty (with the guessed profile)
- HDD error <= d/26: switch edges are exactly 1/13 (predict.c), and an error arm above 50%
  of its case becomes the case's in-trace arm (spec4/5/7), so <= half.
- u2 = 10000 p^2 = 4.28 (entry->exit path threaded by tree DOM; p = 2% floor).
- HDD >= u2 needs d >= 111 (dispatch share >= ~0.57); the hot layout needs the reboot side
  > 50% at the (last) arg test, i.e. share < 0.5 (combined) or < 0.73*0.5 (split).
- Block/HDD is 0.68 independent of d.
So no combination of guessed predictors gives the original order; the remaining levers are
(a) fewer switch edges (merged case labels; but a 2-label edge records no case value, so DOM
cannot re-split it and code would differ), (b) a crafted profile (memory note says the
switch path <= 1/3 argument blocks it), or (c) park mode_client in asm.
