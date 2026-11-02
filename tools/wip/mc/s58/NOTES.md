# s58: tree-only bcp depth (dd/dt/npre) + pinned head weights; NO MATCH (cut short)

sa.py = s57/sa.py plus mutations of dd/dt (bcp depth 1..8) and npre (0..14). The FIX env pins weights
(task 2, e.g. FIX=i0=0,p0=0,hdd4=2,hdd5=2,u2=2,c12=3). The run was stopped early by the caller: about 260 SA
compiles over 4 workers (a/b from s57 best_c, c pinned, d from s56 best). Logs are in sa_s58[abcd].jsonl, best_c.json.

## Findings
- On best_c, dt 3/6 makes things worse (es2 358/419, R2 24/33). npre had no effect at dt 1, so deeper dtg is the
  wrong lever for the reboot edge.
- Pinned head weights (c): best es2 209 (R2 1, R3 34). No R2-0 state.
- The best R2-0 state is still s56 c_s56.c es2 199 / ev 57.
- Not done: task 3 (round-2 trace-end fakes), task 4 (RX/k*l/eb bcp/T48), task 5 finalists.
## Next
Try a second, independent bcp diversion target (not a deeper dtg). Then run the SA for the full planned length.
