# s26 -- mode_client profile-free (continuation of s25)

## Setup
- Copied the s25 tools (voc/ev/m/pot/ga/ga2/hsim users, objcmp, tweak, hq, heapdump, ...) here,
  with paths retargeted to build/v/mc26 (create that dir before use: `mkdir -p build/v/mc26`).
- Deleted build/v/mc25 (694 MB). build/v/mc26 was deleted at the end too.
- Re-checked g7b.json: score (true inversions) 7, fncmp 27. Reproduces.

## Tries
- ga2.py POT2=1 POP=30, seed 2601, from g7b.json, 400 generations (3200 compiles):
  no improvement over init (obj 7070.27 = pot 7, score 7). Log: gp26a.log, population gp26a.pop.json.
  So even a long potential search started from g7b stays at the s25 plateau.

## Result: NO MATCH. Best still s25 g7b (best_g7b_dup.c copied here): 7 inversions, fncmp 27.

## Next ideas (still open, not tried this session)
1. Run ga2 from other seeds or populations (s25 gp*.pop.json, the p34 family) instead of g7b. From g7b
   the potential landscape is flat.
2. Event-neutral realizer: add f deltas only through bcp injections inside clientEraseBlockI and
   check them in hsim before compiling.
3. Control when 55 pops (f126 vs f55 tie) to move 77/79's heap insertion.
4. New JMP sites inside clientEraseBlockI and at the c7/c12 `arg == dummy` tests.
