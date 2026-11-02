# s57: higher rok flow (WMAX 60) + p0/i0 -> hdd4/hdd5/u2/c12 seeds; NO MATCH

sa.py = s56/sa.py with total-weight cap from env WMAX (default 40). Runs (R3W=1, ~4200 real compiles, 4 workers
staggered 6 s): a (from s56 best, WMAX 60) never improved 199/R2 0; b (init2.json: i0 dropped, hdd4/hdd5 2, u2 1,
c12 2, t4/t5 6, _ft 8) -> es2 194 (R2 1); c/d from that (r2one.json) -> **best_c.json es2 189 (R1 2, R2 1, R3 25,
R4 119), ev 50**, best_d.json 194. Logs sa_[abcd].jsonl.

## Findings
- Raising rok flow (weights total 45-60) does lower R4 (131 -> 119) and R3 a little (26 -> 25), but every such state
  has R2 = 1: the extra rok flow pushes the reboot fail edge back over the s53 threshold. No R2 0 state below 199
  in 2100 c/d compiles (0 R2-0 states at all from r2one).
- SA settles on i0 high (7-9) and t5 9-11 rather than the hdd/u2/c12 seeds: head Cha section not fixed (task 2 open).
- Ideas 2 (round-2 trace-end fakes) and 4 (RX/k*l/eb bcp/T48) still untried; ev/fncmp/cm finalists not run (no
  candidate with R1..R3 near 0).
## Next
Combine the high-flow state (best_c.json) with a stronger tree-only reboot bcp boost (s53 lever) to bring R2 back
to 0, then continue R3/R4.
