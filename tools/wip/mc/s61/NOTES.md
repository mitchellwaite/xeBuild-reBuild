# s61: R3 case-head key analysis + PD (pre-dispatch diversion) lever + SA; NO MATCH

## Tools
- raw.py SLOT|m: es2 canonical B id -> raw (spmap) id. rk.py SLOT|m R: one round's events with fibheap keys.
- fq.py SLOT DETAILS: block freq + per-pred edge freq for mapped case-group blocks (compgotos-blocks-details dump).
- exp.py TAG MOD.py: s60 text(best169) through mod(s), es2 + fq table (details compile into slot_TAG/det).
- sa.py: s60 SA + PD lever (ordered [[label,depth]] tree-only bcp gotos after the switch-path netGetInfo).
- M details: rerun the fdo second compile from build/obj/mode_client.fdo/-.gcda with
  -fdump-rtl-compgotos-blocks-details (bb numbering == build/mcmatch/slotm).

## B58-B84 map (R3, canonical -> raw source id; key = -(1e6 + 100*prio + freq), prio = max edge freq from a trace end)
B58 131 clientInfo, B59 118 clientPatches, B60 115 s5 sendCompat, B61 112 s4 sendAvatar, B62 121 c10, B63 120 c9,
B64 107 c1, B65 116 c7 test, B66 132 cdef, B69 108 c2, B70 109 c3, B71 110 t4, B72 113 t5, B74 119 c8, B75 128 c11,
B76 129 c12 test, B80 117 (M) / 130 (T), B81 130 / 1121, B82 114 / 117, B83 94 / 1104, B84 49.
M R3 keys (prio/freq): c12 9/10, c3 8/9, c1 8/9, t5 8/8, t4 8/8, c8 7/9, c2 7/9, c9 7/8, c10 7/7, c11 6/10,
c7 6/9, cdef 6/8, s5 3/4, s4 3/3, 103 2/5. Ours (f169): every dispatch head prio 4, freqs 9..4.
M edge source: dispatch bb108 edges c12 9, c3/c1/t5/t4 8, c8/c2/c9/c10 7, c11/c7 6, cdef 1; BUILD_FDO asm goto
bb102 edges c11 4, c7 3, cdef 6, s5 3, s4 3, c8/c2 2, others 1.
Ours: plain switch gives EVEN dispatch edges (4 each, gcc 6 has no switch predictor); rok chunks (bb103/bb109)
add 1..4. So the R3 heap order (and the B60-B76 permutation, the 132/131/118 fallthroughs = those heads being
visited instead of pushed, and the 83/80-82 insert differences) all come from flat dispatch probabilities.
- Dead extra case values (case 13 -> scope/asm forwarder -> c12) are NOT pruned (even with
  `if (mode==13) __builtin_unreachable()`): jump table grows, fncmp 196. Dead end.
- PD lever: depth-1 diversion takes ~50% of dispatch flow (c12 +21); deeper depths give ~F/2^d. Ordering by
  freq at uniform prio is the only reachable route.

## SA (4 x 5400 s, ~6560 evals each; a R3W=1, b R3W=2, c PPD=0.6, d R3W=3/T0=6/PDP=1)
| file | es2 (R1,R2,R3,R4) | ev | fncmp | cm |
|---|---|---|---|---|
| fin0.c/json (b) | 159 (2,0,20,103) | 61 | 160 | (14,24) |
| fin1.c/json (a) | 161 (2,0,19,107) | 50 | 178 | (14,22) |
| fin2.c/json (min ev, R2 0) | 175 (2,0,21,117) | 43 | 142 | (14,22) |
New es2 best 159 (was 169); R3 25 -> 19/20. Still far from MATCH (no objcmp). c/d did not improve.
## Next
The flat dispatch is the structural blocker: the match's dispatch edges are 9..1 per case, ours even.
Only uniform-prio + freq ordering is reachable; a freq-target designer (desired freq per head from M's
key order, solved with PD depths) would beat blind SA. best_[abc]61.json kept.
