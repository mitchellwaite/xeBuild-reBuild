# s51: event-score search (plain compile goal)

Result: NO MATCH. Best unchanged: s47/H5c2.c (ev 5 / m.py 6 / fncmp 34 / cm (0,6)).

Tools: es.py (fine event score vs s18 MATCH slot build/mcmatch/slotm: per-round edit distance of the flattened
event/group-token sequence, weights R1 8, R2 4, R3 2, R4 1; anonymous blocks >=1000 renamed by first appearance so
bb-index offsets don't count; match vs itself = 0). `python es.py FILE.c TAG` or `python es.py SLOTDIR`.
sa.py (s50 lever genome hill-climb, cost es + W*ev; env G, W), lv.py (copy of s50/lv.py with BASE = H5c2).
Logs sa_a1.jsonl (W=3, from H5c2), sa_b1.jsonl (W=1, from T48 s/300 + rok c12,i0): ~1150 compiles.

## Findings
- H5c2 es = 348 (R1 2, R2 33, R3 53, R4 94). T48 s/300 + rok(c12,i0): es 377-516, worse in R3/R4, same R1/R2.
- No lv lever lowers R2 below 33 (734/1152 compiles exactly 33; all others worse). Both climbs return to H5c2.
- The first real divergence is ROUND 2, not round 3: the match's R2 trace (after vX51) inserts
  131 118 115 112 121 120 116 132 (all :n) in one go; H5c2 inserts only 132 there and 116/120/121 later from
  the iX55 trace. Round 3 differences (pushes of 115/112/131/118, re-keys c112..c132) follow from that:
  those blocks are already in the heap in the match. So round-3 levers fight a symptom.
- R1 only differs by one cX37 position (likely offset/canon noise).

## Next
- Find what makes the match's R2 trace reach the case blocks 131/118/115/112/121/120 (switch/jump-table
  successors of the trace end block vX51): edge probabilities out of that block in the profiled cfg vs plain.
  Levers: probability on that dispatch edge (expect on the switch value / case-order), not rok/T48.
