# s79 (attempt 60): hand fixes of the round-4 order (from best_s77.c)

Tools: m.sh SRC (fncmp, sig2 count, bbro order), mk.py (exact-once replace), bc.py (bcp chain),
vars.sh (kk = round-4 keys). Measures are (fncmp, sig2 +/- lines).

| variant | change | fncmp | sig2 | effect |
|---|---|---|---|---|
| best_s77 | base | 196 | 14 | ReadBl BinPatch(-1000403) WriteBl(-1000309) Patches(c7,-1000305) |
| a1/a2 | more conjuncts on `mode = 9` thread | 232 | 18 | switch->c9 edge 4, WriteBl (f9) jumps to round 3 |
| b1-b3 | a1 + drop goto c9 feeds | 216-264 | 16-26 | c9 freq stays >=6 (dsp loop back-edges) |
| c5/c6 | `if(bcp^k) mode = 11;` after mode=9 | 214 | 14 | BinPatch edge 3 but mode=7 thread dies (only the last two threads work): c7 edge 4 |
| g*/h* | mode=11 thread before 7 / between 7 and 9 | 196/214 | 14 | same problem |
| i6 | `mode = 7; else if (bcp^6) mode = 11; else if (... ) mode = 9` (else chain: all three thread) | 212 | 14 | WriteBl 309, c7 305, BinPatch 303 |
| **j1** | i6 + fail-feed `if (bcp^4) goto c11;` | **196** | **12** | BinPatch f6 -> -1000306: ReadBl WriteBl BinPatch Patches = original. WriteBl diff fixed |
| k1-k4 | j1 minus i1 in fkbo fan (+ replacement c8/c11/c2) | 224-232 | 18-28 | Info0 loses prio but round-4 tail reshuffles |
| l1/l2 | JMP(efail) from eout/einv | 198 | 12 | no order change |
| m2-m5 | fail-feed goto c10 | 198-312 | 14-29 | Ferase still f1 |

Remaining (j1): Info0 fkbo-prioritised before -ip; a CU before -r; Ferase after -w;
-e group (orig: -w CU CU -e Invalid Patches Info CU..). Original needs Ferase f>=2 and
LC117/Patches/Info at f0 popped after -e; round-4 equal-key pops follow fibheap
structure (e.g. 80,68,78 pushed 78,80,68), so they need measured experiments.
Semantics: all j1 deltas over best_s77 are bcp-guarded (`mode = 11`, `goto c11`) = dead.

gr3.py 2 x ~22 min from j1.c (q1/q2.log.gz): no gain, plateau (12, 196). Best: best_s79.c (= j1.c).
Next: Ferase freq / -e group via measured fibheap tie experiments; port the else-chain
mode=11 + feed c11 fix onto best_s78.c (its order is further off: Keys/hdd5 in round 3).
