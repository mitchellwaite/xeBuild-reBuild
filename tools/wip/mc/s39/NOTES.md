# s39: option-loop usage(3)/(4)/(5) source shapes (plain compile, no profile)

Result: NO MATCH. Best unchanged: s35 H5b.c 5 inv / fncmp 40 / cm (0,8). ~1400 compiles. build/v/mc39 deleted.
Tools copied from s38 (mc38 -> mc39). run.py F.c... = cm + inv (absolute paths handled). m.py gained NONR=1
(drops `noreturn` from the client_usage prototype before compiling).

## Shapes tried (on H5b; mk.py, mk2.py regenerate them)
| shape | cm | inv |
|---|---|---|
| H5b base | (0,8) | 5 |
| all loop usage(3) -> goto one shared call, in loop end (V3_in) / after loop (V3_out) | (110,20) | 18+4 miss |
| same for usage(4)/(5) | (39..,14) | worse |
| pair-share usage(3) site k -> k+1 (Q0-3 / R0-3: -bp,-wb,-eb,-ip) | (13..31, 10..16) | 11-22 |
| pair-share among -r/-w/-e/-c (Q4-6, R4-6) | (0,8) | 5 (already crossjumped; no-op) |
| client_usage noreturn+cold | (0,8) | 5 (no-op) |
| client_usage without noreturn (N0) | (0,6) | 5, fncmp 120, same case/tail order |
| J1 without noreturn | (0,4) | 7 |
So the original has separate usage(3) calls for -bp/-wb/-eb/-ip (sharing them changes content); the
-r/-w/-e/-c ones already merge. No content-neutral shape removes 53/77/79 as cold succs of the loop.

## NONR base
Removing noreturn (local discovery still makes it noreturn later) gives a different bbro history with
same content metric (actually block-metric 6 vs 8). Full one-step table on st_H5b with NONR=1
(tabN.jsonl, 1348 cands): floor still 5 (best fncmp 68). Not a new route.

## Next
- Untried: usage calls via a static noinline wrapper / function pointer, __builtin_unreachable after
  calls, flag+break sinking with argv index kept in a separate var; NONR combined with gs2 beam / rel hsim.
