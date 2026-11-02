# s137 (attempt 118): NO MATCH. Floor stays 18 (s117/best.c = b18.c here).

## Block-set finding
best18's u2 hunk (`mov eax,[l]; jmp l`, mine 503-504) is NOT a misplaced block: ref has no such block at all
(ref 679 lines, mine 681). In gcc's asm it is `L535: mov eax,_cinfo; jmp L532` (L532 = the
`sendAvatarData(arg, cinfo->kernel)` call), never referenced in the text: it is the entry edge of the
lever `JMP(s4,c12)` (empty asm goto) in case 5 of the dispatch, which targets label `s4:` in case 4. The
edge needs cinfo reloaded, so gcc makes a separate edge block for it.
- Dropping `goto s4` (dead bcp goto, line 801): still 18, same diff (a1.c).
- Dropping s4 from the asm goto (`JMP(c12)` or none): 34. Retargeting it to each of the 29 other labels
  (v/j_*.c): best 32 (c3), t4 33.
- Moving the asm goto (v/k1..k5): k1/k3/k5 stay 18 but the dead block just moves (to 428 / 466); k1/k3 also
  turn the usage(5) hunk into a usage(3) one.
So best18's layout depends on an extra (dead-in-practice) asm-goto entry block that the ref doesn't have;
the lever set is fitted around it. A profile-free match needs a different way to supply that edge's
effect on bbro without a block that survives to the output (e.g. an edge whose target needs no reload).
## Usage(5) hunk
Ref 560-563 is the same usage(5) block as mine 542-545, diff just aligns it oddly; it's pure placement of a
noreturn block (as s136 says).
