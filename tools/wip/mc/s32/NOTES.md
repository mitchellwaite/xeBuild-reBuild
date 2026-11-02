# s32: loop-site content check + hdd4 placement scans (plain compile, no profile)

Result: NO MATCH. Best remains s29/best_g7b_dup.c (g7b): 7 true inversions, fncmp 27.
About 3700 real compiles. build/v/mc32 deleted at the end.

## A: the option-loop "RA flip" is not real for asm-goto loop sites
- cm.py: full listings via fncmp (FNCMP_CONTEXT=100000), multiset-of-lines diff vs the original.
  g7b differs by 1 line (an extra `mov [8+esp],ebx` hoist in the 288 region; it is already in g7b).
  sig:[hdd4] and keys:[hdd4] (and every loop site scanned, rA.jsonl) have the same 1-line
  multiset diff. So the +70..100 fncmp of loop sites (s31) is layout only (block order, plus a
  swapped test pair inside the loop at line ~199), not register allocation. No pins are needed.
- What loop sites really do: any loop site that gives a post-loop target P also reshuffles the
  case prefix (108/116 move: 129 107 109 110 113 116 119 108 121 120 128 132) and the tail.
  rL.jsonl (g7b_lab.c adds dead-end filler labels jn/nr/dc/rz + fail): filler-only gotos are inert
  (order identical); hdd4 + 1 filler puts 112 at the head (P too high), hdd4 + 2..4 fillers gives
  `49 112 103 115` with the case prefix disturbed, inv 32. rB.jsonl: hdd4 + case fillers, best 20+.
- search2.py (= s31 search.py scored 10*inv + fncmp/20, all loop sites): 2 seeds x 103 gens from
  g7b: stuck at 7.

## B: post-loop hdd4 sources (scanT.py, rT.jsonl; scanD.py, rD.jsonl)
- `{ AT(c9) clientWriteBlocks(..); JMP(hdd4,hdd5); }` (same at c11 / cdef / c10) gives the match
  prefix through `49 115 112 103`; the tail reorders (126 55 33 29 125 61 127 35 42 130 117 ..), inv 19.
  Adding hdd4 to existing JMPs (s4/s5/c8) gives 112 after 103 or before 49 (20-21).
- Pairwise on top of c9>[hdd4,hdd5] (248 designs: every voc F site x target, every rok target):
  best 17 (rok hdd5) / 18 (h4>u2). search2 from it (150 gens): 15.
- So the same pattern as s23/s31: placing 112 correctly costs the round-4 tail.

## Next
- The tail (55/126/125/61/33/29/67/127/117/130) is a round-4 tie/heap structure question; it needs
  hsim on the c9>[hdd4,hdd5] history (s18 hsim/analyze on build/v/mc32 slots) to find which blocks
  need f/P, not more blind search.
