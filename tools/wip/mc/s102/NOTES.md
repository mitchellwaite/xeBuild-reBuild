# s102 (attempt 83): NO MATCH. New best best.c (= e_12.c) f2 24 (b0 26).

Fix: -r cmp/mov sched swap solved by adding a labelled usage(3) target to the r5x asm goto:
  if (({__asm__ goto("" :::: r5x, r3x); 0;}) || i + 1 == argc || !a || *a == '-')
      { r3x: client_usage(3, argv[i]); }
(semantics unchanged: empty asm always falls through; label is only a target). Moving the r5x asm
goto later in the || chain also fixes the swap but swaps the usage 3/5 cold blocks (28).
Applied to all s99/s100/s101 .c (rr/, rr.log): b0 family -> 24, y36 -> 30; nothing else below 30.

Remaining diffs in best.c (24): BinPatch bb141 (freq 10, round-3 trace) right after netReboot (10);
Blk LC118 printf (f3, T37r4) before u2 instead of after -r log/LC117 (8); i0 clientInfo(NULL)
(f0, T50r4) after 3 usage blocks instead of directly after p0 (6).
- c11 fail feed 4/5 conjuncts drops BinPatch to f6/f5 round 4 and places it right (after WriteBlocks)
  but reshuffles round-4 heap (g4.c 56; climb from g4 only reached 30).
- i0 levers (JMP(i0) from p0/p1/i1/c8/hdd, c12/c7 asm gotos, dead cp gotos to i0): all inert or worse.
- Blk levers (eout JMP efail/esucc/eerase, feed conjunct changes): none below 24.
- c11 JMP/asm-goto/cold variants (v1.txt): all worse or inert.
- cl.py: f2 climb over p.out asm-volatile + bcp-conj add/del levers, 3x500 (cl_1..3.log): best.c plateau 24.
~1900 variants measured. Tools: sw.py (substitution sweeps, '@@' sep, ' ;; ' multi), bi.sh (bbro bbinfo), cl.py.
