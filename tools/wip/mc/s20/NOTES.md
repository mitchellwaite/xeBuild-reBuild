# mode_client s20: design-driven profile-free pass (2026-10-29) -- NO MATCH

Setup: `python tools/wip/mc/s19/mkslot.py src/mode_client.c build/v/mc20/slot_plain`;
analyze reproduces plain inv 23 (all case heads f4/P4, tail f0..2).

## Tools
- `fanneal.py SLOT EVALS SEED`: f-only anneal on the plain history (P as
  measured; env FMAX, PTIE=1 ties P to f where measured P==f, DIST=1 adds
  L1 distance from measured f, START=json, T0).
- `realize.py DESIGN.json STEPS [start.json|-] [WSET]`: greedy over s19
  search.make() injections, objective L1(fq - design) + 3*inv, measured by
  mkslot + s18 analyze (~0.5 s per eval, 94 tgt/src pairs x 4 weights).
- `inv0_a.json` (first inv-0 design, far from plain), `design1.json`
  (inv-0 design at L1 28 from plain).

## Results
- hsim on the plain history admits inv 0 with f alone, unconstrained.
  Closest found (design1, L1 28): cases unchanged (all 4), raise only
  103 +2, 112 +4, 115 +4, 55 +3, 126 +4, 61 +3, 125 +3, 33 +2, 29 +1, 67 +2
  (49 stays 7). Local DIST anneal from the plain point stalls at inv 3.
- Caveat: hsim keeps the plain insertion history fixed and ignores flow
  constraints (55/61/67 halving chain, 112/115 need send calls 39/41 raised).
- realize.py greedy: 3 steps, inv 23 -> 16, but distance to design never
  falls (27-29): single injections add the wrong quanta (and step 0 dropped
  block 125 from the order, which the objective tolerated). Stalled.
  fncmp not attempted (no candidate near inv 0).

## Next ideas
- Realize per block with calibrated injections: first measure, for each
  target block alone, the f delta each (src, weight) gives (table), then
  solve the design as a small integer program instead of greedy.
- Penalize missing blocks (analyze NEED) in realize's objective.
- Re-slot after each realized batch and re-anneal design on the new history
  (START from previous design) -- the plan's iterate loop, not done here.
- Add flow constraints (chain_ok-like) to fanneal so designs are realizable.
