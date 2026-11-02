# s59: second reboot-fail diversion levers + R4 levers; NO MATCH (run cut short, ~390 SA compiles)

sa.py = s57 SA + post-text levers: rf/rft (bcp on the reboot fail edge -> ndl/dtg/rbn), d2/d2t/d2p (second bcp
diversion before/inside `if (reboot)` to ndl/rbn/u2/case labels/fail), rp (bcp after rok netGetInfo -> ndl),
rE (expect on reboot netConnect), E2 (round-2 trace-end fakes after netDisconnect to case labels), rx126/rx117
(JUMP->JMP), ebm (drop eb bcp lines), kl (drop k67l bcp). Logs sa_[abcd].jsonl.

## Findings
- Single-lever scans on s57 best_c: rf (any target) and d2 to ndl/rbn/case labels all wreck R2 (7..28); rE 1/2 R2 7;
  d2 to u2/fail, rx126, rx117, kl: no effect; ebm 2 +2 es2. No single lever gives R2 0 on best_c.
- SA worker a (from best_c, R3W=1) found **best179.json: es2 179 (R1 2, R2 0, R3 27, R4 109), ev 58** -- new R2-0
  best (s56 was 199). Levers in it: E2 {i0:1}, ebm 2, kl 1, rx126 1, cap 26, npre 0 (see json).
- c (FIX head weights) best R2-0 227; b/d (from s56, E2-only for d) no improvement in the short time.
- Workers were stopped early by the caller's hand-back request; ev/fncmp/cm/objcmp finalists not run.
## Next
Continue SA from best179.json (R3W=1) for the full length; then fncmp/cm finalists.
