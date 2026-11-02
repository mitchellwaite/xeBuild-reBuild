# s116 (attempt 97): NO MATCH. First variant with 141, 139 and 145 all placed right: best.c (f2 27).

base b0.c = s113/a_c6_c11.c (case-6 asm goto c11, 141 right, f2 31). comb.py = s115's, reading this b0.c.
- y/ (gen.py): c11 dead-entry conjuncts 4/5/6 x 145 fixes (n00/n02 t4/t5/s4, s07..s13 i0).
  The conjunct count does nothing. n00_t4 makes 141+145 right (f2 40); i0 sites break things (93).
- q/ (gq.py): n00_t4 + every single v/w edit (1192 compiled). s06_s4 -> f2 28, 141+145 right.
  n25_c1 -> 141+139 right (46).
- climb.sh ROUND EDITS: singles on top, cost f2 + 10*(blocks wrong) -> rN/cost.txt.
  r1 (n00_t4 s06_s4): n25_s5 = all three right, f2 28. r2: + n07_c11 removes the stray case-6 jmp -> 27.
  r3/r4: no single improves on 27 (the floor is wide, mostly neutral edits).
best.c = b0 + n00_t4 s06_s4 n07_c11 n25_s5. What's left in its diff (27 lines):
  1. cinfo reload `mov eax,[l]` before the t4 test (351) and again in the moved `call l(2,0)` block (path skips dsp).
  2. n25_s5 (JMP(s5) after AT(c9)) moves the `[esp]=2,[4+esp]=0; call` block 9 lines early (420 vs 429)
     and pulls `[8+esp]=ebx` from 465 up to 424.
  3. Tail `5`/`3` block order swapped (535-559): same as in every 145 fix.
Next: pairs over best.c targeting 1-3; register pin / edge placement after the cinfo load; another site
for the 139 lever that doesn't move the call-2 block.
Semantics: only never-taken empty asm gotos to existing labels plus the dead __builtin_constant_p entry. Equivalent.
