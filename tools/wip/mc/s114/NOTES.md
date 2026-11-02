# s114 (attempt 95): NO MATCH. Best still s102/best.c (f2 24; b0.c here is a copy).

Tools: pert.py/runp.sh (randomise every __builtin_constant_p(var + K) constant), g6.py/rv.sh (case-6
dead-cp gotos), sa.py (SA: conj counts + "collision" move = a chain's first constant set equal to
another chain's + case-6 empty asm goto label), sa1..4.log.

1. Constant values are NOT a tie-break lever. 200 random renumberings of all dead-cp constants in
   best.c: all f2 24. 60 of k4.c: all 56. 60 of a_c6_c11.c: all 31. The s113 56->52 observation
   must come from a collision: when two dead conjuncts get the same expression (mode + K), FRE/PRE
   value-number them as one, which changes the CFG structure (shared/threaded tests), not
   tie-breaks. (sa.py's a + 50000*i scheme can collide across chains.) So no dump bisection needed.
2. Case 6 with a dead-cp goto (1..6 conj) to c11/c12/c9/c10/... on best and on k4 (108 variants):
   best-family floor 24 (c11/c12 no change), k4-family floor 42/56. A dead-cp goto is folded before
   bbro and does not reproduce a_c6_c11's effect (141 in r4); only a real (asm goto) edge does, and
   that always leaves a jmp block (fallthrough to the switch end isn't next).
3. SA with conj counts + collisions + case-6 asm-goto label, 4 chains x 400 (1600 evals) from
   a_c6_c11 (x2), best, best+c11=4: floor 24 (only best-like configs), a_c6_c11 chains never below 31.
Semantics: only never-true __builtin_constant_p conjuncts and never-taken empty asm gotos changed.
