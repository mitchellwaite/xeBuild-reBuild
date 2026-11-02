# s31: site table + graded-level design attempt (plain compile, no profile)

Result: NO MATCH. Best remains s29/best_g7b_dup.c (g7b): 7 true inversions, fncmp 27.
About 1300 real compiles. Build dir build/v/mc31 was deleted at the end.

## Step 1: site tables (sites.json, sites_loop.json; step1.py, step1b.py, probe.py)
- Post-loop sites (voc.SITES): g7b plus one JMP to cdef (block 132; c11 for the cdef sites, einv/eout in eb).
  None of them is a round-3 trace end. They only add frequency to the target (132 f6 -> 7/8/9).
  The P of 132 stays 2. Sites that keep contents and order: c1> c2> c3> c8> c9> c11> h4> h5> s4<> s5<>
  p0> p1> i0> eerase<> einv> enet<.
  - f deltas from c9>: 1 target +3, 2 targets +2 each, 3 targets +2, 4 targets +1.
  - Label -> block: c1 107, c2 108, c3 x1, c7 116, c8 119, c10 121, c11 128, c12 129/130.
  - hdd4 -> 112, hdd5 -> 115, p0 -> 117, i0 -> 130 and u2 -> 103 get P2.
- rok with a short target list is not a trace end. Its trace absorbs a target, and case P stays at
  the dispatch's 4. Case f stays below the round-3 threshold only with about 7+ targets, so rok gives P <= ~5.
- Option-loop sites (loopsites.py) are real trace ends only without T48:
  - sig ("reboot has already...") and keys (mode=3 arm end) give P9 with 1 target and P6 with 2 (edge 18/(n+1)).
  - wb gives P89; eb (mode=10) gives f only.
  - Every loop site raises fncmp by about 70-100 (option-loop RA change, s12).
  - With T48 (des.build t48=1) sig/keys no longer give P.

## Step 2: solve + hsim (hs.py, hsa.py)
- The match history shows graded P works (s29 sa_call: 0). On the g7b history graded case levels (f or P)
  do not help: hsim gives 34, because the tail reshuffles. On the c_all history the best is 47.
- Available P levels for cases: dispatch 4, rok <= 5, loop sites 9/6/4.5 only without T48.
  So the s29 design (P129 11, 107 9, 110 8, ... with T48) is not realizable with these levers. I wrote no ILP:
  the site table shows the level set is too small.
- hsa.py (f-only SA on the eb:hdd4 history): floor 15 hsim (incl. the x1 miss penalty).

## Step 3: real compiles (d31.py rounds r1-r5, search.py)
- r2/r3: c_all plus sig/keys graded targets, best 53/208. r4: loop-site x hdd4 table.
  **eb:hdd4** (`{ mode = 10; JMP(hdd4); }`) gives the exact prefix through `49 115 112 103`. The tail
  scrambles (inv 28, fncmp 95).
- search.py (real-compile local search over rok/loop/F/rx/t48, score fncmp+8*inv):
  - seed 1 from g7b, 480 compiles: stays at 7/27.
  - seed 2 from eb:hdd4, 640 compiles: best inv 10 / fncmp 78 (115/117/130 missing).

## Step 4: 110 + s4 sibling (r5.txt/r5.log)
- eb:h4t,s4; keys/sig h4t,s4; eb:hdd4 plus r/e/v:s4 or h4t,s4: raising 110 still makes it jump to the head (s23).
  s4 targets were inert (r/e/v:s4 gave the same order as eb:hdd4). Best 28.

## Next
- A non-loop trace-end source with frequency 10-20 (P levels 5-9) that keeps contents, or a fix for the
  loop-site RA change (pins as in s15/s16), would make the loop-site P levels usable.
