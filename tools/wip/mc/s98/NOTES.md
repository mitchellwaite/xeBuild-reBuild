# s98 (attempt 79): NO MATCH. ~320 measured variants (log.txt; c2.log = ccs on k2h).
Best unchanged: best_s96.c (= b0.c) fncmp 26 / sig2 6 / inv 5 (invd.py: Blk before CU108 -r = 2, Info after wb5/eb5/ip3 = 3).
Tools: g1.sh (efail/esucc loop shapes on J1), g2.py (self-loop wrap/after/before on 11 statements),
g3.sh (JMP(i0) real edges), g4.py (efail loop on asm split part, +/- top goto), g5.py (k61l chain 1-5 on H1/J1/m02n),
gen1.py top/er/ou gotos on m02n (n2_*), invd.py (named inversion order), sw.py/sw2.py (r4sim insert-order what-ifs).
Findings:
- Self-loops on argv-loop statements (-r/-w/-e/-ip printf, mode=1/2) and on "erasing"/Success/Inv: inert.
- Blk self-loop (wrap or before) on H1 gives exactly b0's order (26): loop on eout = Blk 3.
- efail loop: Fer 4 (with top goto efail), 22 (loop before printf, no top goto), 3 (empty loop after printf), 1 (loop
  after printf, no top goto = m02n: Blk 3, Fer 1 after CU33). asm("") split parts merge into the Fer block: no new values.
- Observed (Blk,Fer) pairs only: (3,2 b0 order), (2,3), (2,2 -> -r Fer -w Blk or -r Fer Blk with -w 1), (2,4), (3,1), (4,1).
  Never Blk 2 + Fer 2 with Blk before Fer.
- k61l chain: -w freq is binary (0 extra conj -> 2, >=1 -> 1) on H1/J1/m02n.
- JMP(i0) real edges from any block raise Info freq to 1-2 (worse); JMP(i0) in p0 / before clientPatches(arg) inert.
- r4sim (sw.py): on H1 the order among key-0/-2 ties is fibheap-shape driven; deleting 146 before 142's inserts gives 3,
  but 146's push cannot be removed realistically (nopush 16). Edge-order perms of 134/55 give >=10.
- ccs on k2h: no change below 42 / inv 6.
Next: needs a heap-shape lever (an extra round-4 insert/delete of a dummy block between 134 and 142 processing)
that is byte-neutral; loops and cp gotos only move integer freqs, which are exhausted around Blk/Fer.
