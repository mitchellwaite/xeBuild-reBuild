# s123 (attempt 104): NO MATCH. Floor stays f2 18 (b18.c = s117/best.c).

Tools (all in s123): dump.sh SRC DIR (cprop_hardreg-blocks + bbro dumps), fdo2.sh (profiled build -> pf/),
cfg.py (trace-time CFG: freq/preds/succs/insns/lines/trace), map.py (best18 <-> profiled block map via
source-line alignment + symbols; map_b18.txt / map_b18_pairs.txt), ord.py/fin.py (round-4 traces and final
layout in common numbering), rm.py (r4sim with blocks removed), pfsim.py, mv81.py, keys.py, d127.py, ev4.py
(variant -> layout distance vs profiled, in profiled numbering, + count of unmapped extra blocks).

## 1. Block map (trace-time CFG, after bbro's cfg cleanup)
best18 157 live blocks, profiled 140. 139 mapped. 18 best18 blocks have no profiled counterpart; 1 profiled
block (108, the dispatch tablejump) maps to our 112 by hand.

| ours | freq | trace | source construct |
|---|---|---|---|
| 45 | 63 | T10 r2 | -I arm: split of the `if` (mapped approx, prof 45 f73) |
| 57 | 0 | T41 r4 (mid) | -r test: `asm goto(r5x,r3x)` block splits the condition |
| 66 | 1 | T44 r4 (mid) | -w test: `asm goto(w5x)` conjunct |
| 105 | 0 | T36 r4 head | rok rk network / u2 dead edge (`__builtin_constant_p ... goto` residue, no succ) |
| 106 | 0 | T36 r4 | dead block from the `mode = 7/11/9` constant_p chain (no preds) |
| 112 | 45 | T14 r2 | dsp dispatch tablejump (= prof 108) |
| 114 | 3 | T25 r4 (mid) | case 1 `asm goto(dsp)` x3 after netDumpNand |
| 117 | 6 | T26 r4 head | case 3 block-start `JMP(hdd4,s5,hdd5)` |
| 124,125 | 8,4 | T28 r4 (mid) | case 5 `AT(s5)JMP(dsp); { JMP(s4,c12); ...` |
| 127 | 1 | T46 r4 head | `mov eax,[_cinfo]; jmp` reload for the s5->s4 edge (issue 2) |
| 134 | 4 | T30 r4 head | case 8 `JMP(p1,cdef)` after clientReadBlocks |
| 136 | 8 | T33 r4 head | case 9 block-start `JMP(s5)` |
| 138,156 | 1,2 | T33 r4 (mid) | case 9 trailing `asm goto(dsp)` x3 |
| 140 | 62 | T15 r2 head | case 10 self-loop `JMP(c10)` |
| 150 | 7 | T24 r4 (mid) | case 12 `({JMP(p0);0;})` conjunct |
| 154 | 4 | T35 r4 head | default block-start `JMP(i1)` |
| 157 | 13 | T25 r4 (mid) | break/merge forwarder after case 1 |
(ours 142 = prof 125, the cinfo->nandSize test, is real; map.py pairs it wrongly with 127.)

## 2. r4sim
- rm.py: each extra removed (mid-trace: drop visit/ins; head: rename to its trace successor), all 1159
  singles/pairs/triples of 19 candidates: no hit. 15 singles are inert; 124, 127, 134, 136 make it worse.
  All extras at once: worse (s119-want dist 8, prof dist 13 vs base 1/5).
- pfsim.py: the profiled event stream with best18's keys gives a much worse order: the keys, not the block
  set, decide it.
- The real target (fin.py: final layouts in common numbering) is not s119's "want" (152 after 79).
  best18 vs prof differ only in: ...54 [108 146 145] 55..61 [129 122] 62... vs ...54 [129 122 108] 55..61
  [146 145] 62..., and usage(5) bb81 after bb79 at the tail. (129/122 = hdd5/hdd4 logs, 108 = u2,
  146/145 = erase logs.)
- keys.py: in prof 108/129/122 come into round 4 with priority keys (-1000205/-1000304/-1000303) from
  round 3, because the rok dispatch block (prof 102 = ours 104) has direct JUMP edges to u2/hdd4/hdd5 and
  p0/i0 (131/152 inserted 'next' there too). 49 has priority (-1000607) because prof's 48 ends its r3 trace:
  96 (-keys arm) has freq 9 < round-3 exec_th 10 (ours 18, so 48 96 form one trace). 145 gets a key change
  from prof's outside-area log (efail edge). Also prof's g55 inserts 79 at bb56 and 81 at bb60 (the
  `if (mode)` test); ours inserts 81,79 both at bb56 (the r5x,r3x asm goto). Moving only that insertion
  (mv81.py) just swaps 79/81 (dist 5).

## 3. Real variants (~350, all compiled with f2; all edits never-taken asm goto labels or dead
## __builtin_constant_p conjuncts, so equivalent to src/mode_client.c)
- v/ (36): -r asm goto forms on b18, s122 m_c9/m_s5c, s121 rm1_8. r1/r4/r5/r9 are equivalent 18s;
  r9 (`i + 1 == argc || ({asm goto(r3x)}) || !a || *a == '-'`, r5x edge dropped) reproduces prof's g55
  insertion order (79 at 56, 81 at 60) but the tail block becomes usage(3) instead of usage(5). r2/r3/r8/r10 20.
- w/ (123): retarget each rkE ork slot to p0/i0/u2/hdd4/hdd5/c11: slots 14-51 (2nd/3rd rok asm gotos) are
  byte-identical (their edges are gone before bbro); slots 11-13: u2 44, hdd4/5 48, p0/i0 86.
- x/ (68), y2/ (7): 2-3 of those targets together, repurposing slots 0-10, adding labels to the first rok
  asm goto (max 30 operands, so no dilution possible): 44-102. One label = 1/26 of rok freq 20 -> priority
  and freq too big (u2 jumps to asm 393).
- k/ (51), k2/ (48): lower -keys arm (96) freq below exec_th: dead cp conjuncts (`&& !cp`, `!cp &&`,
  `({if (cp) goto L; 1;})`, body gotos): 96 keeps freq 18 (merged block keeps the pre-split freq), 18 or
  90-182; never-taken asm goto at arm start/end to 16 labels: 50/50 split, but the body still has freq 18
  (freq not recomputed), best 18 (identical), else 22-73.
- f/ (12): c3b (`clientKeys(); } asm goto(dsp, hdd4, s5, hdd5)`) removes forwarder 117 byte-identically
  (also on r9); c3a 34; folding cdef's JMP(i1) into its trailing asm goto 142.
Conclusion: the remaining diff needs prof's round-3 priority structure (rok edges with edge freq 2-3 to
u2/hdd4/hdd5, 48 ending its trace). Without a profile, asm-goto edges from rok carry 1/26 of its freq at
best, and the -keys arm frequency can't be lowered (dead conjuncts/asm-goto splits keep freq 18).
Forwarder removal is inert or worse, both in the model and in real builds.
