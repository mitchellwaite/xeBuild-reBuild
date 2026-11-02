# s38: race-free re-verification + J1 case-head analysis (plain compile, no profile)

Result: NO MATCH. Best unchanged: s35 H5b.c (st_H5b.json) 5 inv / fncmp 40 / cm (0,8).
~7100 real compiles, all with race-free tags (tt.tid()). build/v/mc38 deleted.
Tools copied from s37 (mc37 -> mc38). Note: cm.py needs ABSOLUTE paths (relative -> silent (0,0)).

## 1. Serial re-verification (ver.py)
| file | inv | fncmp | cm |
|---|---|---|---|
| H5b.c (s35) | 5 | 40 | (0,8) |
| J1.c (s37) | 7 | 38 | (0,6) |
| S5.c (s34) | 5 | 37 | (1,8) |
| best_g7b_dup.c (s29) | 7 | 27 | (1,8) |
All claims hold; the race did not corrupt the recorded bests.

## 2. Race-free re-runs
- tabJ1.jsonl: full one-step table on J1 (1348 XT=1 cands). 700 neutral; nothing < 7. No candidate
  moves 113 ahead of 108 without breaking the tail (best such: 26).
- js1.jsonl: eb JMP(p1,X)/(X,p1) and J1 + one more loop-site JMP (358): nothing < 7.
- gH5b.log: gs2 beam from H5b, XT=1, 2 rounds, beam 3 (1348 + 4042): floor 5 confirmed
  (`!rok:b p1` 5/76 is the best neighbour). So earlier "floor 5" conclusions were not race artefacts.

## 3. Why J1 loses 113 (hd2.py diff of H5b vs J1 histories)
The eb JMP(p1) makes block 118 (clientPatches(arg)) a cold successor of trace 1038 in round 1
(`ins next 118 -7`, pushed into the round-4 start heap). In H5b, 118 is only inserted during 119's
round-4 trace (P1 key). hsim (dx2.py): moving 118 back to 119's trace on the J1 history gives
exactly H5b (5); removing it gives 19. The single extra root 118 is BOTH the tail fix (55, 53) and
the case-head break (113 behind 128): same fibheap consolidation change.
- dx.py / dx3.py: dummy extra roots (any group of rounds 1-4, keys -9..0, P keys, 1-3 copies), alone
  or with any single f delta +-2: nothing below 7 on J1, nothing below 5 on H5b. Parity/root-count
  levers cannot separate the two effects.
- rel.py / rel2.py (relocate one block's insertion event to another group): on J1, 53 inserted in
  round 4 during case 119/120/121 -> 3 (case heads fixed: `129 107 110 113 108 ...`), +29/33/35/42
  relocations -> 2, +77@55 or 126@120 -> 1. On H5b the s36 result again (77/79 @61 -> 2).
  None realizable: 53 (usage:3:dx) keeps its round-1 cold insertion from the option loop; an added
  edge cannot remove an insertion, only add one (and duplicate inserts are no-ops).

## Next
- The remaining routes all need a CFG where 53 (or 77/79) is NOT a cold successor of the option-loop
  trace 1038, i.e. a different crossjump/duplication of the usage(3) calls. That changes content.
- Profile splice remains the only matching build.
Files: ver.py, tabJ.py/tabJ1.jsonl, an.py, js.py/js1.jsonl, gH5b.log, hd2.py, dx.py, dx2.py, dx3.py,
rel.py, rel2.py.
