# s118 (attempt 99): NO MATCH. Floor stays 18 (s117/best.c = b0.c here).

Semantics check of s117/best.c vs src/mode_client.c: equivalent. `{ netReboot(reboot); JMP(fail); }`
is an empty asm goto that never jumps, so control falls through to `ndl: netDisconnect();` exactly as
the original (`if (reboot) netReboot(reboot); netDisconnect(); return 0;`). All other additions are
never-taken empty asm gotos and __builtin_constant_p dead gotos; the u2/dtg/ndl dead entries fold to 0.

Variants (gen.py BASE VARFILE, '~~'-separated old/new pairs; pair.py = all pairs of a list; run.sh -P8):
- v1/v2 (55 singles): issue 2 (s4 edge moved to t5 / dsp / as "a"(cinfo) input / t4 target / order),
  issue 3 (r5x/r3x order, drop/extend w5x, cold attrs on r3x/r5x/w5x, extra edges into w5x/r5x/r3x),
  issue 1 (u2 dead feeds removed/lengthened, u2 cold, edges into u2 from parse/log blocks).
  Neutral (18, different asm): a4 (s4 moved onto the AT(s5) asm goto -> reload block moves next to
  the [8+esp]=ebx log block, still present), c1 (r3x,r5x order -> L407 usage(3) takes the early slot
  instead of L609 usage(5): the slot after the c11 log block (L541) goes to the first label of that
  asm goto). Everything else worse.
- v3 (93): an extra label first/middle/last in the r5x,r3x asm goto: all >= 39.
- p2 (1197 pairs of 52 singles): floor 18.
bbro (dd/mc.bbro): L609 = pre-bbro bb152, a round-4 key-0 trace start queued from trace 23 (bb149);
key-0 ties are taken in heap order, so it lands before patches(NULL)/info(NULL) (bb35/42); the ref
has it after L407.
~1345 variants compiled.
