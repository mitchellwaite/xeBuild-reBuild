# s101 (attempt 82): NO MATCH. ~4000 measured variants (climb4_*/climb5_*/climb6_*/sx_*/sw_*/rd_* logs, sub_f2.log, sw15.log, ps_f2.log). Best by fncmp unchanged: b0.c (= s96/best_s96.c) 26.

Key finding 1 (metric): fncmp.py's difflib diff overstates mismatches when blocks move. f2.sh (fncmp2.py dumps
normalized ref/mine; count = GNU `diff --minimal`) gives the true edit size: b0 26, s_42 33 (fncmp said 153),
v08 35. Old fncmp-ranked results (s99/s100) should be re-read with f2.sh. climb6.py / sx.py use f2.sh.
Key finding 2 (s_42's "hot change"): the line-725 empty asm blocks jump threading of the argc<=0 path
(original and b0: `jle` -> client_usage(2)); s_42 instead jumps to the reboot test via an extra
`xor ebp; [44]=0; xor edi; [40]=0; jmp` PHI-copy block (5 extra lines, reboot block freq 138->142).
Explicit thread `for (i = 0; i < argc || ({ if (!i) goto u2; 0; }); i++)` (w15; equivalent: loop exit with
i==0 iff argc<=0, mode=0/reboot=0 -> u2) or `if (i == 0) goto u2;` after the loop restores the jle and
makes the line-725 asm irrelevant. Best of that family: y36.c (w15 + rdbest bits 4,32) f2 32, plateau
(single-lever sweep + 2 climbs). Residual vs original there: BinPatch block after netReboot (10, also in b0),
u2+printf moved early (10), -r cmp/mov sched (2, also b0), 3-line usage block (6, also b0).
- climb4 (hot,inv,fncmp) from s_42 found fncmp 43 = s_42 + one asm after `a = argv[i + 1];` (-w); x.s
  differs from s_42 only by a cmp/mov swap -> purely a difflib artifact.
- Single sweeps with f2 on b0, s_42, w15, y36: nothing below 26/33/32/32. All 127 rdbest subsets: min 26 (s_8);
  with w15: min 32. pos.py positions at 721-736/794-800: 33/48/50 only.
- w01-w08: other zero-byte forms at line 725 (asm with inputs, asm goto, dead bcp gotos): 33 or 50.
