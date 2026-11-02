# s139 (attempt 120): block-free base vEa (s138/vEa.c, f2 35) vs profiled bbro

Files: dump.sh (bbro/profile_estimate dumps -> dd/NAME), al.py (emitted-order alignment of
s111/pf/bbinfo.txt vs dd/vEa/bbinfo.txt -> align.txt), al2.py (map P->V by block signature, map.json),
keys.py (round-4 keys P vs V, keys.txt), srch.py (r4sim key search on vEa), baseA.c (vEa + kk vars,
f2 35), gen.py/climb.py/nonin.py (s136 ports on baseA).

## A. Block-by-block (align.txt has every block: bb, trace/round, freq, both sides)
- Rounds 1-2 (P 2-51 / V 2-51): identical block set and order, same traces. Freqs equal in the
  arg loop; differ after it: P14/15/16 175/109/110 vs V 127/138/71, P17 73/51, P46-51 (T10/T12)
  73/60/87x4 vs 63/44/58/58/47/45 -- V splits P's T12 (netConnect..cinfo) into T12+T14 and adds
  V52 (T15r2 f62, a forwarder).
- Round 3: P has 5 traces (58 netGetInfo f37, 60 f15, 62 f13, 63 usage f12, 59 netReboot T15r2 f61);
  V has 6 (59, 62, 64/65, 66, 67) and builds V96 (= P94, f18 vs P f9) in round 3; P builds it in r4.
  Threshold is entry*5% = 10 in both; P94 at f9 falls below it.
- Round 4: V has 19 extra forwarder blocks (60,61,63,69,72-75,77,81,82,86,87,89-94,96 new-numbering);
  P's ~41 r4 traces map 1:1 to V heads (V heads are often an empty forwarder before P's block:
  P111->V117/118 clientKeys, P123->V132/135 clientWriteBlocks, P136->V152/153 LC157).
- Round-4 keys (keys.txt; p=priority=pred-edge freq, f=bb freq), P vs V, in P pop order:
  P133 p9/f10 vs V147 p5/f7; P94 p9/f9 vs V96 (r3); P109/111 p8/f9, P112/115 p8/f8 vs V p4/f6 x4;
  P110/122 p7/f9, P123 p7/f8 vs V p4/f5, p4/f4, p4/f4; P124 p7/f7 vs V139 p31/f6 (myatoh32 entry,
  pushed early with prio 31 -> popped FIRST in V); P132 p6/f10, P118 p6/f9, P136 p6/f8, P49 p6/f7
  vs V p3/f9, p3/f8, p2/f4, f7 (no prio); P117 p3/f4, P114 p3/f3, P104 p2/f5 vs V f2,f2,f3;
  tail P f1-f3 vs V f0-f3 (P131/P119 f1 vs V f0).
- Emitted-order differences that survive forwarder removal: clientWriteBlocks (P74, own trace after
  ReadBlocks) sits inside V's BinPatch trace T33; LC156/LC155 logs (P84/85 before usage P86) placed
  after the -x/... strnicmp chain in V; LC118/LC117 logs (P93/95) moved; clientPatches P111/112 and
  usage P117/118 order.

## B. r4sim on vEa (srch.py, keys.py)
- vEa replay exact. LCS distance to the mapped P pop order: base 11.
- Any-key SA (single/pair/SA over all r4 blocks, 6x4000): floor 6 with 3 overrides
  {144:p2/f10, 132:p3/f13, 108:f2}; remaining misses: V139 still first (its p31 push in round 3 is
  outside the sim's r4 overrides' reach), V96 not in r4, 81/79 order, forwarders 128/105 interleave.
- Transplanting ALL of P's keys onto vEa's events: front matches (147 113 117 120 123 _ 116 132 139 146
  134 152 49) except 96 (r3) and a tie swap 116/131 (equal p7/f9, heap shape); the f0-f3 tail is
  scrambled (128,105 forwarders + V's insertion structure). So targets are: (1) P94/V96 freq <= 9,
  (2) V139 must not get the prio-31 edge (it must arrive as p7), (3) switch-case ladder p9..p6 instead
  of flat p4/p3, (4) ~19 forwarders gone. (3) is the same ladder s111/s124 showed heuristics can't make.

## C. gen/climb on baseA (vEa + kk, f2 35)
- Singles 6340: floor 25 (asm goto 787->755/761 = feed into hdd4/hdd5 logs; 631..801->735).
- Pairs over 100 non-inert (4950): **17/5 hunks** (new overall best, block-free):
  best17.c = p17.json [("f",773,761,"a"), ("f",755,761,"k")]: empty asm goto to hdd5 (S761) before
  case-12's `JMP(c11); break;` plus dead `if (kk) goto S761;` before the hdd4 log.
- SA 600 iters from p17 over 4000 singles: stays 17.
- Residual of best17 (diff v/best17.ref v/best17.mine): extra `mov eax,[cinfo]` in case 5 (the "a"(cinfo)
  reload, ref 361) + two `log_printf(0,..); jmp` hdd log blocks misplaced (ref 461 and 536 -> 395 and 555).
## Semantics
kk = __builtin_constant_p(runtime) = 0, `if (kk) goto` dead; empty asm goto falls through; "a"(cinfo)
input on the empty asm goto only reads a value. Equivalent to src/mode_client.c.
## Conclusion
NO MATCH; best f2 17 (block-free, best17.c), beats b18. Next: climb from best17 (singles on top of p17),
and remove the case-5 cinfo reload line.
