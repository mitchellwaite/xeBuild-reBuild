# mode_client s23 (profile-free) -- NO MATCH

Profile build stays. No src/ or build.sh change. Scratch: build/v/mc23 (ref19 = inv-19 slot).
Base for everything: s21 inv19.json [(44,rok,pp),(50,rok,q)], inv 19.

## Tools (all use s19 search.make + s21 table.meas, NEED-missing penalty 5 each)
- `ext.py BASE [WSET]`: adds non-call targets to search.TGT: 58=h4 / 59=h5 (label before the
  case 4/5 `if (cinfo->hwFlags` test = blocks 110/113), 60=t7 / 61=t12 (before `if (arg == dummy)`
  of case 7/12 = 116/129); measures singles.
- `table2.py`, `loop2.py`: s21 table/loop with ext's targets (loop2 = s21 loop.py, imports ext).
- `try.py INJ-JSON TAG`: one measurement (inv, order, all fq).
- `where.py INJ TAG`: final .s sequence of log strings / calls (where a block really lands).
- `lab.py INJ TAG SPEC..` / `scanlab.py BASE TAG`: label attribute levers without new edges:
  `{ l: __attribute__((hot|cold)); stmt }` at hdd4/hdd5/s4/s5/reb/u2, case heads c1..c12/cdef,
  option then-branches o<name>, and RAW 'ent'/'ent2' (an `if (argc <= 0)` guard before the loop).
- `fanneal2.py SLOT TABLE EVALS SEED`: s20 fanneal restricted to blocks the table moves (env
  EXTRA adds blocks, ONLY=1 uses EXTRA only), flow rule 112 <= f110/2, 115 <= f113/2, L1 cost.

## Findings
1. Why (39,*) lowers 112: 39/41 (send calls) are NOT preds of 112/115. 112/115's only pred is
   the hwFlags test 110/113 (f4, 50/50 split -> 2/2). Injecting into the send block raises 111
   (unmapped) and the label/join makes the 110 split lean to 111 (-1 on 112; same as s4:hot).
   Fix: target the test itself (h4/h5). (58,fail,pp): 110 +5, 112 +3 and 112 moves before 103
   (wanted) -- but 110/113 then jump the round-4 head (inv 38-47). Every lever that makes 112
   >= its sibling 111 (hdd4:hot, s4:cold, 40/42 injections) lets the 110 trace claim 112 ->
   missing. So 112 can only rise as f110/2: needs f110 >= 8 to beat 103 (f4).
2. "Missing" is real, not an analyze.spmap bug: where.py on (40,rok,b) shows the
   "cannot send avatar" log placed in the hot case-4 trace where sendAvatarData was, and the
   send call moved to the tail. s21's numbers stand.
3. 103 = usage(2) reached from the entry (argc<=0 threaded edge 2->103); u2:cold, reb:cold,
   case-head labels have no effect (switch: nedges != 2 => predictions ignored; E() is
   first-match so labels on E-tests/reboot do nothing). 'after' injections drop 103 to 0
   (break the 2->103 threading). ent2 (`if (argc<=0) client_usage(2,NULL)` + cold) -> 103=0.
   No lever found that gives 103 = 2..3.
4. Head realization: design from fanneal2 on ref19 (129 7,107 7,109 6,110 6,113 6,108 5)
   realized exactly by rok-pp duplicates (d3: each (t,rok,pp) = +1, duplicates add) -- head
   order perfect, but tail scrambles (inv 31: 115/112 swap, 29/33/61/125/126 reshuffled by the
   new insertion history). Re-anneal on d3's slot wants 55/61/125/126 +1..+2 (inv 10 in sim),
   which no lever provides; head+112/115 only: sim inv 20-22.
5. 'fail' source saturates: several fail injections share its small frequency (each +5 alone,
   +3 together). 'top' (loop) sources into h4/hdd4 wreck the order (39-56).
6. Option-chain labels: cold label on a then-branch raises the following tests (oip:cold 55 +5,
   or:cold 61/67 +1) but always pulls the raised block out of round 4 (trace claim), E() tests
   ignore labels; hot labels only lower. loop2 (278 rows incl. ext targets, ADD 6, TOPK 12):
   no measured improvement on inv 19.

## Conclusion / next ideas
The binding constraint is structural: a cold block can only rise while staying <= its
sibling at the same 2-way test, so raising 112/115/55/61 requires raising their test blocks,
which are themselves ordered heads/loop blocks. Frequency nudging around inv 19 is exhausted.
- Search 2-level designs explicitly: raise test AND sibling together (e.g. h4 + 39 injections
  so 111 = 112 tie, check tie-break direction in bbro better_edge_p) -- not tried.
- A source with large frequency budget that does not perturb the tail history (entry-level
  source before the loop needs a bcp variable that is not folded at once; all locals are
  constant there -- maybe a volatile-free global read).
- Structural source changes (s22 idea): merge/hoist the hwFlags test, change which blocks exist.
