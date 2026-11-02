# s95 (attempt 76): NO MATCH. ~600 measured variants (log.txt; v1-v9.sh, ccs sweeps c/e/f/m/p.log, hc7.log).
New best: best_s95.c (= d01) fncmp 26 / sig2 6 / inv 5 (was n2 42/10/6). Diff vs n2 = two dead gotos:
- b06 = n2 + `if (__builtin_constant_p(i + 5555)) goto k61l;` after -r's log_printf: -w (blk 62) freq 1->2, so it
  now precedes CU33/CU29 (sub-problem A solved). Same effect: a09/a12 (asm goto k61l, worse fncmp), a13/b05
  (`&& !cp` on -r test). But zero group scrambles (CU81 first; fib-heap structure) -> 42/10/18.
- d01 = b06 + `if (__builtin_constant_p(block+9)) goto eout;` at end of esucc: Blk freq 2->3; zero group back in
  target order. Order now: Blk CU108 -r Fer -w CU33 CU29 -e Inv Pat CU35 CU42 CU53 Info CU79 CU81.
  Remaining inv 5: Blk(140, key -3, ins by 135 myatoh32 trace) before CU108/-r, and Info(146) after CU53.
- r4sim on n2: -w alone needs key -2 (done). On d01: key-only (<=3 overrides) best 4; wp/wr2 insert what-ifs
  again only reach <5 via an extra early insert of 55 (-r test) from 123/135/143/105 = edges into the loop
  (g01-g03: cp goto k55l from after the loop -> fncmp 850+).
- k4 = d01 + cc chain 4 (-ip goto k55l) -1: -r freq 3, still 26/5 (Blk CU108 -r). k1 = + chain 2 -1 (u2):
  CU108 -r Blk Fer -w CU33 CU29 correct but CU108 above hdd5/hdd4 and -c/zero group off (148/16);
  m_6_2 (k1 + k61l chain +2) 138/8/8.
- Inert/worse: E()/expect/cold/hot on -r/-w tests (a01-a06), JMP(i0)/cp goto i0 for Info (h*, b06h*),
  -c usage cold/asm (c1-c4), eout edge variants (d11-d16, j*), esucc->efail (j01: Fer 3, 122/8).
- ccs on b06, b01 (x1+lever), d01, k1, m_6_2 and fail-line hc on d01 (hc7): plateau 26/5.
Next: from d01 need Blk tie-broken after CU108/-r (fib-heap tie) and Info earlier; try k4/k1-type freq shifts
with compensations for CU108-vs-hdd (CU108 key -4 ties hdd5/hdd4).
