# s84 (attempt 65): front fixed on x4/z3, back group broken again

Step 0 (semantics): s83's -r `({__asm__ goto("" :::: r5x); 0;})` emits no instructions and never jumps at runtime,
so the condition is unchanged; r5x: sits inside the existing `if (mode)` around the same client_usage(5) call. So
behaviour is preserved, the same pattern as w5x. z3 drops r5x entirely anyway.

Results (r.sh: fncmp / sig2 / inv; base h1 = 64/8/7). Levers are mk.py replacements in b1..b8.sh.
- v18/v23 (esucc bcp feed 2-conj / removed): Fer freq 3->2 -> front `CU29 Blk Fer -r CU33 -w -e` (Blk Fer now in
  the right relative order), back still exact. 64/8/8.
- w12 = v23 + wb3 feed 5-conj: CU29 freq 2->1 -> front `Blk Fer -r CU29 CU33 -w -e`, back broken (CU53 first). 80/12/14.
- **x4 = w12 + second k55 feed `if (bcp(i+35)&&bcp(i+36)&&bcp(i+37)) goto k55l;`**: -r freq 3, -w 2 ->
  front `-r Blk -w Fer CU33 CU29 -e` (target `-r Blk Fer -w CU33 CU29 -e`, 1 swap). Back
  `Inv 81 53 35 42 Pat Info 79 -c` vs target `Inv Pat Info 35 42 53 79 81 -c`. 70/6/15.
- **z3 = x4 without the r5x asm goto: 64/6/14 = best_s84.c** (best sig2 so far; back still off).
- ws3.py (random what-if: move a block's R4 ins event to another group with a key) on x4/z3: inv 1-2 reachable only by
  inserting Inv (einv, 140/141) late (from the -e or CU29/CU33 group) plus Fer key -1. No source lever found for
  that: Inv is a successor of the erase trace (135) which pops first in R4. einv cold off, JMP(einv) from
  eout/eerase/esucc, bcp gotos to einv/eout, __builtin_expect on erase tests: all worse (y1-y7, q3-q8).
- s83 back levers retried on x4 (z1-z8): fkbo i1,p1 / p1,dtg,i1, c12 JMP variants, r5x moves: none restores the back.

| var | base | change | fncmp | sig2 | inv |
|---|---|---|---|---|---|
| v01 | h1 | r5x after argc | 68 | 8 | 8 |
| v02 | h1 | r5x after !a | 68 | 8 | 8 |
| v03 | h1 | w5x first | 68 | 8 | 7 |
| v04 | h1 | w5x after !a | 64 | 8 | 7 |
| v06 | h1 | k55 1-conj | 222 | 14 | 25 |
| v07 | h1 | k55 4-conj | 64 | 8 | 7 |
| v08 | h1 | k67 2-conj | 64 | 8 | 7 |
| v09 | h1 | k67 4-conj | 64 | 8 | 7 |
| v10 | h1 | k61 2-conj | 150 | 12 | 20 |
| v11 | h1 | k61 4-conj | 64 | 8 | 7 |
| v12 | h1 | wb3 5-conj | 80 | 12 | 15 |
| v13 | h1 | u2 1-conj | 64 | 8 | 7 |
| v14 | h1 | u2 3-conj | 138 | 14 | 25 |
| v15 | h1 | k55 feed x2 | 64 | 8 | 7 |
| v16 | h1 | k67 feed x2 | 64 | 8 | 7 |
| v17 | h1 | eout no JUMP(efail) | 64 | 8 | 7 |
| v18 | h1 | esucc 2-conj | 64 | 8 | 8 |
| v19 | h1 | eout cold | 148 | 20 | 33 |
| v20 | h1 | einv not cold | 274 | 20 | 26 |
| v21 | h1 | eout JUMP(efail,einv) | 64 | 8 | 7 |
| v22 | h1 | eout JUMP first | 64 | 8 | 7 |
| v23 | h1 | no esucc feed | 64 | 8 | 8 |
| v24 | h1 | eout JUMP(einv) | 64 | 8 | 7 |
| v25 | h1 | eout JUMP(esucc) | 64 | 8 | 7 |
| v26 | h1 | esucc goto eout | 70 | 10 | 16 |
| w01-w16 | v23 | v01-v16 levers on v23 | 64-150 | 6-18 | 8-24 (w12 80/12/14 front closer) |
| x1-x3 | w12 | wb3 3/4-conj, none | 80 | 12 | 14 |
| x4 | w12 | 2nd k55 feed 3-conj | 70 | 6 | 15 |
| x5 | w12 | 2nd k55 feed 2-conj | 170 | 14 | 21 |
| x6-x8 | w12 | 2nd k61 feed 3/2/1-conj | 320-360 | 24-28 | 29-32 |
| x9 | w12 | einv JMP(eout) | 129 | 15 | 19 |
| y1-y5 | x4 | eout JUMP(efail,einv)/(einv,efail)/none, einv not cold, eout JMP(einv) | 70-284 | 6-22 | 15-24 |
| y6/y7 | x4 | JMP(einv) in eerase / esucc | 93/78 | 10/6 | 30/18 |
| z1 | x4 | fkbo i1,p1 | 138 | 16 | 16 |
| z2 | x4 | r5x after argc | 64 | 6 | 14 |
| z3 | x4 | no r5x | 64 | 6 | 14 |
| z4-z6 | x4 | c12 JMP none / first / +JMP(i0) | 70-138 | 6-16 | 15-16 |
| z7 | x4 | fkbo p1,dtg,i1 | 70 | 6 | 15 |
| z8 | x4 | JMP(r5x) from -w | 288 | 12 | 19 |
| q3/q4 | z3 | expect on erase range / block!=-1 | 148/288 | 14/24 | 29 |
| q6-q8 | z3 | esucc 3-conj bcp goto efail/einv/eout | 72/72/148 | 6/6/14 | 17/17/29 |

Next: on z3, fix the back group (Pat/Info before 35/42/53, 81 last) with insert-order levers (s83 style), or find a
lever that inserts Inv late. ws3.py NAME ITER blocks SEED MAXMOVES does the what-ifs (ids per variant, see tmap).
