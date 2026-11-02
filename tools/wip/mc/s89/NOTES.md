# s89 (attempt 70): NO MATCH. Best unchanged: s88/v06.c 36/10/18

~1450 variants measured (log.txt for hand ones; hl*/hc*/cd*.log for climbs, each line = one compile).
New tools: lp.py/el.sh (permute an asm-goto label list), hl.py (climb a label list, per-seed tag),
dc.py/cd.py (set / coordinate-descend the number of `asm goto(dsp)` per dispatch case).

| what | base | result |
|---|---|---|
| fkbo label list (first 9 labels) climbs hl61/62/63 | v06/v04/v10 | plateau 36/18, 42/6, 38/13; rev = 62, any swap of p1..cdef usually worse |
| rok rkv0 list rev / first-11 rev / climb hl83 | v06, c38 | 37 / 36 / 42 - list order nearly inert |
| dsp counts per case, coord descent cd1-5 | v06/v04/v10/b22/c38 | no improvement anywhere |
| c3 JMP list perms/subsets (c1-c10) | v06 | 36 or worse (c4 = drop hdd5: 46, inv 10) |
| JMP(c3)/JMP(t4) after netDumpNand (c11-16) | v06 | 67-94 |
| more dead edges into c3: ork9/10 -> c3 (c22), ork12/13 (c37), c38 = c22 minus ork17 | v06 | **42/8/9: clientKeys block now right after netDumpNand (front fixed)** but back cold traces reorder (-r/Block swap, -w trace, Ferase/Patches/Info) |
| one extra c3 edge (c21,c31,c35,c36) | v06 | 37 (threshold needs 2) |
| same c3 edges on v04/v10 (c41-46) | | 66/62, or no effect |
| fail-line climbs hc71 (b22), hc81/92 (c38), hc91 (c38, inv-first) | | climbs only reach 36 by undoing the Keys fix; with Keys fixed best stays 42/9 |

Finding: Keys position (call;jmp near sendCompatData in v06) is a round-4 trace order tie; >=2 extra dead
edges into c3 fix it, but the same shift reorders the freq 0-2 back traces (heap insertion order).
Keys-right and back-right look coupled through heap insertion order; next: r4sim what-if with c38's order to find
an edge that restores the back order (-r before Block, -w before CU group) without touching c3.
