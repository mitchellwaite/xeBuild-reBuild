# s104 (attempt 85): NO MATCH. Best stays s102/best.c (f2 24). New second family: c_w2f3.c (f2 34).

Model work (mandatory part):
- r4sim (s86/r4sim.py) reproduces the round-4 pop order exactly for s102 best and g4 dumps (o_dmp_*.txt).
- Target round-4 pop order (from the ref layout): T in srch.py =
  best's order with 141 (BinPatch) after 131, 139 (Blk) after 55 (-r), 145 (i0) after 127 (p0).
- g4 = best + only 141's key change (-10 -> -6, pushed into round 4); that one extra round-4 heap node
  reshuffles ties (fib-heap shape), nothing else in the event stream changes.
- srch.py: sim with key overrides + dummy (zero-byte) heap insertions at any event; beam.py/beam2/beam3.py
  beam search, kd.py/kd2.py exhaustive key grid + 1/2 dummies.
  * From g4: 2 dummies reach dist 1 but only at round-3 positions inside the rejected-push sequence
    (pre idx 175 = between get/push 129, idx 203-206) - no trace is built there, so not realizable.
    Realizable positions (after round-3 trace visits + any round-4 group) + keys: min dist 2 (beam2_g4.log).
  * From c_w2f3: keys of {139,29,33,55} x 2 dummies (kd2_w2f3.log): no exact hit; min 1.
    Permuting the round-3 tail push order + keys: min 3. Keys alone (6 blocks, -4..0): min 2.
  => Within key changes + <=2 zero-byte insertions the target is unreachable from either state; the
     remaining Blk/55 order needs 139 key >= 55 key (Blk freq 2 or -r freq 3) AND a different heap shape.
- Realized zero-byte blocks (asm goto to `z: __builtin_unreachable();`, a*.c, b*.c) are not freq-neutral:
  the extra asm-goto target steals edge freq (e.g. 104->142 priority 5->4), and the z block gets
  key -1000100 / -1; none below 44.

Real variants (~165, res*.txt not kept; see *.d/*.mine): 
- c_wXfY.c / e_ / r_ / g_ / j_: wb3 loop-head feed (593) conjuncts X + new wb4 feed (label on L634
  client_usage(4)) with Y conjuncts. w2f3, w2f4, w4f2, w4f3, w4f4 -> f2 34 from g4 (56) AND from best
  (e_*, 141 also moves to round 4): BinPatch and i0 placed RIGHT; remaining 34 = usage 3/4 (29/33) promoted
  (keys -2/-3) plus Blk/Fer before -r. With 29/33 back at -1 (w5+), shape reverts to g4 (56).
- d*.c (esucc/eout/eerase bcp-goto conjuncts on c_w2f3): inert (34) except removing eerase goto (58).
- h*/k*: k55l (-r) feed conj -/+ : inert or worse; k3_j_w5f3 gets 108 139 55 138 62 33 29 69 but breaks p0/i0 (42).
- m*: wb4 feed inside the -wb branch: inert.
Semantics: all levers are dead __builtin_constant_p gotos, labels, or empty asm gotos (fallthrough) /
unreachable labels after return - equivalent to src/mode_client.c.
Tools: gen.py (line-local substitutions), mk1.sh/mk2.sh (feed grids), run.sh/par.sh (f2 + r4 order, 4-way), bi.sh (fixed: no longer deletes mc.bbro on rerun).
