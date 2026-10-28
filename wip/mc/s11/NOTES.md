# mode_client, 11th session (2026-10-28): source-structure probes, NO MATCH (still 15/16)

## Setup gotcha
Prep MUST run with `EXTRA='--param builtin-expect-probability=50'` exported, otherwise the
.gcno CFG differs and every profile compile ICEs (`create_edge, cgraph.c:850`):
`EXTRA='--param builtin-expect-probability=50' python wip/mcfdo.py "$(cygpath -w "$PWD")\build\mcX" SRC.c`

## Tools
- run.py = s10 run.py + env: MCD (build dir, default mcsp), FAKE (erase leaf bbs for the
  fake-exit overrides, default "5 6 7 8"), ERASE (tree edges for e2 e3 e4).
- search11.py = search10.py with SLOG (log name in s11/) and START (start design) env.
- mk.py OUT.c BODY.txt: sp.c with clientEraseBlock replaced by BODY.txt.

## Variants (best.json from s10 remapped)
| variant | GIMPLE effect | result |
|---|---|---|
| vA: `if (!netConnect) goto fail;` before the switch | identical CFG to sp.c | no change |
| vC: clientEraseBlock with early returns | identical CFG | no change |
| vB (eraseB.txt): erase chain with inverted tests `==-1 / >= / !net` | errors become bb 3/5/7, leaves 3 5 7 8 | e4 51: 32/12 (same as sp); e4 49/55: 36/11 |
| vD: second `({asm("");0;})` after `!arg` | folded away, same CFG | no change |
vB + search11 (hill-climb): see searchB.out / searchB.log.best.
Reproduce vB: prep build/mcvB from vB.c, then
`FAKE="3 5 7 8" MCD=mcvB ERASE="2>3 4>5 6>7" python wip/mc/s11/run.py a wip/mc/s11/bB.json`.

## Conclusion
The erase-chain shape only flips which side of each test is the fallthrough; the s10 cap
(dispatch entry 104 must pop after -eb/-s 44/38 in round 2 -> cases <= ~7) is in mode_client
and untouched. Equivalent C rewrites of the post-loop/dispatch code canonicalise to the same
GIMPLE. Next angle: a hint that really adds a block between trace end 99 and 104 (e.g. a
volatile asm with an output used by the switch, or a cold-label block), then rerun the
s10 simulators on its bbro dump.

searchB (vB, 480 compiles, seed 11): no improvement, best stays fncmp 32 / inv 12 (= s10 best).
Total this session: ~495 compiles.
