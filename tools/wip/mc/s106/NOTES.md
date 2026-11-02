# s106 (attempt 87): NO MATCH. Best stays s102/best.c (f2 24). New basin: 55 before 139 realized (f2 26).

Model broadening (m.py, unrestricted; m2.py, restricted to realizable edits): beam over edits of the
round-3 tail and round-4 groups of the parsed bbro event stream (simulated with s104/srch.sim):
swp/mvp (round-3 push order), i2p (round-4 start pushed in round 3 instead), mvi (move/rekey a round-4
insertion to any group position), rkp (round-3 push key), dum (zero-byte dummy inserts), depth 3-5.
- From best: dist 1 (only 141) with 2 edits: 139 pushed in round 3 (key -3, between 33 and 53) + 55 key -3.
  The 139 edit cannot be realized: 139 (eout printf) lives in the inlined clientEraseBlockI, so all its
  predecessors are in trace 134-137 (round 4); no mode_client edge can reach it. one.py: no key/insert
  combination inside the 134 group alone helps.
- From w (c_w2f3) and g4: depth 3 min dist 2.
55 vs 139 (what decides them): both enter round 4 as "possible start of this round" with key -freq
(139 from 135 in trace 134 at -3; 55 from 49 at -2). Ties go to the one inserted first (139).
Realization found:
- 55 freq 3: k55l feed in -ip down to one conjunct (v/a1.c, f2 24, order unchanged since 139 ties first).
- 139 freq 2: remove the esucc `goto eout` dead cp goto (2/3 conjuncts act the same).
- v/e0_b3.c = w.c - wb3 feed + k55l 1 conj + esucc->eout removed: 108 55 139 62 33 138 69 29 ... (f2 34),
  first variant with 55 before 139. Rest wrong: 138 after 62/33, 29 after 69, 79/81 early.
- -w (62) freq levers: -s k61l feed off or to k67l puts 62 at -1 but also raises 79/81 (-e usage) to -1 (56).
- kg.py key grid on e0_b3 (6 blocks, -4..0): min dist 2. m2 beam from e0_b3 depth 4/5: min dist 1, never 0.
- cl.py climbs (dead-cp conjunct add/del, cost f2+2*dist, 3x400) from e0_b3 all reach the same plateau
  v/h1.c (= c/clb_1.c) f2 26: 33 108 55 138 139 62 29 69 81 79 ...; cl2.py pure-f2 climbs from h1 (2x300): 26.
  m.py from h1 depth 4: min dist 1.
Real variants: ~100 hand (v/*.c) + ~1800 climb evals. Semantics: every edit only adds/removes conjuncts
of dead __builtin_constant_p gotos or removes one (esucc->eout); equivalent to src/mode_client.c.
Conclusion: the model now covers earlier-round push order, insertion moves and 3+ dummies; within it the
target needs at least one round-3 push of a clientEraseBlockI block or a 2nd tie change that no source
lever reaches. 55-before-139 can be realized but costs 2 in f2 vs best (26 vs 24).
