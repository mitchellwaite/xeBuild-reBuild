# s70: diagnose/repair the asm-goto loop R2 break; NO MATCH
Base s64/best_d (es2 156). Probes: `python ../s64/q.py TAG ../s64/best_d.json m_X.py` (env vars pick the variant);
`python kv.py TAG` prints the round-2 heap keys (block freqs) of the switch trace for comparison with `m`.

## R2 diagnosis (s69/m_e, tail asm goto at case 12 -> `dsp:` before switch)
- The R2 break is not the rok block itself: the `dsp:` label splits the block before the switch into its own
  2-pred block, whose fallthrough edge (freq 37) is below the round-2 threshold, so the main trace stops there and
  everything after (switch, rok/netGetInfo trace) moves to round 3.
- Moving `dsp:` up to `cinfo = netGetInfo();` after fkbo (or to fkbo itself) keeps the trace: R2 0-2 (m_p.py gi/fk 233, R2 1).
- Remaining R2 1: the cycle is entered by DFS from rok's asm goto (c10 first), so the dispatch->case edge is
  EDGE_DFS_BACK and that case gets the back-edge priority key (-1000403). Fix: list `dsp` FIRST in rok's asm goto
  (m_v.py TA=r) -> DFS enters at dsp, R2 0 for every single tail edge.
  Best: tail edge at case 10 + r -> **es2 149 (R1 2, R2 0, R3 18, R4 97)**, ev 58, but fncmp 270.
- Why tail loops don't raise dispatch: case blocks also have rok/fkbo preds, so dsp never dominates them; the
  cycle is irreducible and predict.c drops DFS-back edge flow. Natural loops need the latch in a new block before the
  case's AT label (head position): those raise case freqs to ~10 (M 8-10) but the extra head blocks cost R2 22-30
  (m_v TPOS=head, m_b, m_a). Bcp-guarded head gotos (m_b) don't vanish cleanly either (R2 30).
- Back edge to a header before NO_MODE_ARG (natural, m_t.py): es2 460-1120.

## SA (sa.py = s62 PD/TH + LP tail-loop lever with dsp-at-netGetInfo + rok-dsp-first)
4 workers x 4000 s (~5900 compiles each), from s64/best_d (w1,w2) and s62/best_b (w3,w4) with LP {10:1}.
Best: best_es2.json / best145.c = **es2 145 (R1 2, R2 0, R3 18, R4 93)**, ev 54, LP {10:1, 3:2, 1:1}; but
fncmp 271 (base 158): the loop changes register allocation, so the es2 gain does not reach the bytes.
R3 stayed at 18: this lever does not change the dispatch flow, so it can't fix R3.
sa_s70w*.jsonl.gz are the logs.

## Conclusion / next
- The R2 break is understood and fixed (dsp placement + DFS entry order), but loops that keep R2 0 are irreducible
  and add no flow. Natural loops (head latch blocks) add the right flow (~10/case) but add blocks.
- Next idea: natural head latch blocks that later passes remove before bbro while the estimated freqs stay. Needs
  a guard that folds after profile_estimate but before RTL (the m_b bcp guard left jump-threaded copies). Another
  option: drop the rok/fkbo edges into one case so a tail latch is natural.
