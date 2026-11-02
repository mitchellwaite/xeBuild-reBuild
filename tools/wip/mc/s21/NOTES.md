# mode_client s21: calibrated injection table + hsim-scored subset solve (2026-10-29) -- NO MATCH

Profile build stays. No src/ or build.sh change. Work dir build/v/mc21 (scratch).

## Tools
- `table.py OUT.json [BASE.json]`: measures every single s19 injection (t,s,w) on top of a base
  (8 threads, ~75 s for 384 jobs, ~3 min with chain sources): per-block fq delta, inv, missing.
  `meas()` now scores inv + 5 per NEED block absent from the round-4 order (s20's realize and
  my first loop runs accepted injections that silently dropped 112/115 -- "inv 16" was bogus).
- `solve.py TABLE DESIGN`: additive-model anneal of subsets toward s20 design1 (L1). Predicted
  L1 12, measured 20 (inv 29): deltas are far from additive.
- `loop.py ROUNDS [start]`: closed loop: table on current base, anneal subsets (<= ADD) scored by
  hsim.inv on the BASE's real history with f = basefq + sum deltas (P tied to f where P==f;
  this replaces the design-distance objective and builds realizability in), measure TOPK, accept
  best measured, re-table. hsim now agrees with measurement (19 == 19) once missing blocks count.
- `srcx.py`: adds chain sources `s<t>` (goto placed before post-loop call t, to a later target);
  env CVAR (default `arg`; `mode` is constant there so bcp folds early -> a real edge).
- `meas.py INJ DESIGN`: one measurement with distance.
- `inv19.json`: best honest result [(44,rok,pp),(50,rok,q)], inv 19 (plain 23).

## Results
- Best honest: inv 19 (clientPatches(arg) and clientInfo(arg) raised). Loop then finds no
  measured or hsim-predicted improvement (ADD up to 8, 60k anneal iters, TOPK 20).
- Why (table t0.json): no injection can raise 55, 61, 67, 103, 112, 115 within the order:
  103/55/61 only ever drop; injections targeting the HDD logs (40/42) raise 112/115 by
  1..73 depending on weight/source but always pull the block out of round 4 (an earlier
  trace takes it via the new edge) -> missing. design1 needs exactly those raised (+2..+4).
- Chain sources (cold block -> next cold block, to build 103->112->115 traces): 590/700 have
  no effect at all (cold source freq * 50% rounds to 0), the rest drop blocks from round 4.

## Next ideas
- The vocabulary is the bottleneck, not the solver: need a way to raise a cold block's f
  by 2..4 WITHOUT a new incoming edge (an edge always lets trace growth claim the block).
  Candidates: raise the block's existing predecessor test probability instead (expect on the
  existing sendAvatarData/sendCompatData result test with a bcp-dependent value, e.g.
  `__builtin_expect(r, bcp(x)?1:0)` -- check whether expect with a non-constant folded later
  keeps a probability), or inject frequency into the predecessor (send call blocks 39/41 = 112/115's
  only preds) and let the 50% split carry it: rows (39,*) currently only lower 112 by 1 --
  investigate why (label before the send call creates a new merge block?).
- Fix analyze.spmap so a block with an extra dead pred is still identified (check whether the
  "missing" 112 is really placed earlier or merely renamed: look at fdo.s order directly).
- Re-anneal design (fanneal DIST) on the inv-19 history, restricted to blocks the table can move.
