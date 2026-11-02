# s83 (attempt 64): back f0 group fixed by heap-structure levers

Base best60.c (s82). **best_s83.c (= h1.c): fncmp 64, sig2 8, inversions 7 (inv.py metric; best60 = 19 on the
same metric)**. Back group after -e is now exactly the original's: Inv Pat Info CU35 CU42 CU53 CU78 CU80 -c.
Remaining order diffs are front only: ours `u2 Fer Blk CU29 -r CU33 -w -e`, target `u2 -r Blk Fer -w CU33 CU29 -e`.
Diff vs best60 (all zero-byte asm goto / label / list order, braces intact):
1. fkbo asm goto list `i1, p1, ...` -> `p1, i1, ...` (b1: back group becomes Info Inv Pat 35 42 53 80 78 -c).
2. -r: `if (({__asm__ goto("" :::: r5x); 0;}) || i + 1 == argc || ...)` + `if (mode) { r5x: client_usage(5, argv[i]); }`
   (d1): the -r trace now inserts CU80 before CU78 -> 78 80 order right. The label did NOT stop the CU merge.
3. c12: `if (arg == dummy || ({JMP(p0); 0;}))` (h1): c12's trace inserts Info then Pat (JMP before the test = e5 inserts
   Pat first; inside i1 = bad).

## Finding: no prio route
bb_to_key gives priority only if edge_freq > priority(0): a zero-frequency edge from a trace end never prioritises,
so the "key -1000000 via 0-freq asm goto" idea of s82 is impossible. Also a JMP inside the loop body (a1-a4) is a
loop exit: fncmp 330. Instead the back group is fixed by *insertion order* (heap structure), found with:
- mv.py DUMP blocks: what-if moving ins events of blocks to other groups/round-3 pushes.
- perm.py x NAME: permute the round-4 initial ins events (+ 78/80 swap); showed back group exact needs
  Info-first initial inserts with Pat right after, and 80 inserted before 78 in the -r group.
- perm2.py, ksr.py/ksr2.py (key grid searches on variant NAME), osrch2.py (osrch on variant ids via tmap), ev.py x NAME
  (compact heap event trace), inv.py NAME, r.sh now prints inv= and logs to log.txt.
Front: key-only grid on i4 history can't get below 5 inversions; moving front keys (k55 3-conj int: i5) re-breaks the
back group (consolidation shape changes). osrch2 3x12000 on i4: best 4 inv (not 0).

| var | base | change | fncmp | sig2 | inv |
|---|---|---|---|---|---|
| a1 | | | 330 | 32 | 43 |
| a2 | | | 330 | 32 | 43 |
| a3 | | | 330 | 32 | 43 |
| v8 | | | 68 | 10 | 16 |
| b1 | | | 80 | 10 | 11 |
| b2 | | | 60 | 10 | 19 |
| b3 | | | 160 | 20 | 26 |
| b4 | | | 160 | 20 | 26 |
| b5 | | | 96 | 12 | 15 |
| b6 | | | 9999 | 0 | inv? |
| b7 | | | 9999 | 0 | inv? |
| b8 | | | 60 | 10 | 19 |
| b9 | | | 60 | 10 | 19 |
| b10 | | | 60 | 10 | 19 |
| c1 | | | 80 | 10 | 11 |
| c2 | | | 80 | 10 | 11 |
| c3 | | | 80 | 10 | 11 |
| c4 | | | 80 | 10 | 11 |
| c5 | | | 80 | 10 | 11 |
| c6 | | | 80 | 10 | 11 |
| d1 | | | 76 | 10 | 10 |
| d2 | | | 80 | 10 | 11 |
| d3 | | | 76 | 10 | 10 |
| e1 | | | 294 | 20 | 33 |
| e2 | | | 282 | 22 | 23 |
| e3 | | | 302 | 22 | 44 |
| e4 | | | 94 | 14 | 15 |
| e5 | | | 64 | 10 | 8 |
| f1 | | | 302 | 22 | 44 |
| f2 | | | 140 | 18 | 24 |
| f3 | | | 140 | 18 | 25 |
| f4 | | | 64 | 10 | 8 |
| f5 | | | 90 | 12 | 15 |
| g1 | | | 90 | 12 | 16 |
| g2 | | | 274 | 18 | 34 |
| g3 | | | 64 | 10 | 20 |
| g4 | | | 76 | 10 | 10 |
| h1 | | | 64 | 8 | 7 |
| h2 | | | 64 | 10 | 8 |
| h3 | | | 134 | 18 | 23 |
| i1 | | | 72 | 8 | 16 |
| i2 | | | 100 | 12 | 29 |
| i3 | | | 100 | 12 | 29 |
| i4 | | | 64 | 8 | 7 |
| i5 | | | 100 | 12 | 29 |
| j1 | | | 64 | 8 | 8 |
| j2 | | | 64 | 8 | 7 |
| j3 | | | 72 | 6 | 12 |
| j4 | | | 64 | 8 | 7 |
| j5 | | | 64 | 8 | 7 |
| k1 | | | 80 | 12 | 15 |
| k2 | | | 80 | 12 | 15 |
| k3 | | | 80 | 12 | 15 |
| k4 | | | 64 | 8 | 8 |

Changes: a1-a3 JMP(i0|p0|p0,i0) after `mode = 4;` (loop body); v8 = s82 v8; b1 fkbo p1,i1; b2 JMP(cdef,p1); b3/b4
s4 JMP(i0,p0)/(p0,i0); b5 s4 JMP(p0); b6/b7 extra fkbo labels (error: label in list twice); b8 ndl feed p0->i0;
b9 JMP(c12,s4); b10 c9 JMP(hdd5,hdd4); c1-c6 further fkbo list perms (only p1-before-i1 matters); d1-d3 r5x asm goto
before/after argc test / standalone; e1-e5 JMP(p0) in c3 list front/back, i1 after/before call, c12 head; f1 JMP(p0)
before case-12 break; f2/f3 c12 JMP(i0,p0)/(p0,i0); f4 e5 minus s4 JMP(i0) (same); f5 e5 + fkbo i1,p1; g1-g4 JMP(p0) in
c3 / after clientKeys / c3 only / c10; h1-h3 JMP(p0) inside c12 condition (|| after, || before, && after);
i1-i5 v8 front levers on h1 (all / no esucc / u2+k55 / u2 1-conj / k55 3-conj int); j1 no esucc feed; j2 lu1 feed;
j3 k61l feed (sig2 6, fncmp 72); j4 k55 3-conj char; j5 no k55 feed (dead on h1); k1-k3 wb3 feed off/3/4-conj;
k4 esucc 2-conj.

Next: front only. Need -r to pop right after u2 (before Fer/Blk), Fer after Blk, CU29 after CU33, without
changing the round-4 consolidation shape that now gives the back group. Search insert-order levers (like 2./3.) for
the front with perm.py-style what-ifs on h1's history before trying freq levers.
