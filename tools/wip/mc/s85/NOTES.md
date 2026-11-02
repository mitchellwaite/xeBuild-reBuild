# s85 (attempt 66): NO MATCH, best unchanged (s84/z3 = best_s84.c, 64/6/14)

About 57 real variants (r.sh: fncmp / sig2 / inv), plus round-4 what-if scripts wi*.py (r4sim based).

Findings
- Back group break, z3 vs v23: the keys of 29 (-2 -> -1) and 55 (ins by 49, -2 -> -3) change, so 55 pops right
  after -r (107) and inserts CU78/CU80 (key 0) early. Those two then pop ahead of 53/35/42 (fib-heap tie structure).
  The k55 second feed alone (d1) is enough to break the back. Dropping r5x alone from v23 (d2) keeps the back exact
  (inv 9).
- What-ifs on z3/v23 found no fix that reaches inv <= 2. Tried: key overrides of up to 4 R4 blocks (wi.py, wi4.py,
  40k samples), every insert order and 0/-1 key inside the 55 group (wi2.py), dummy insert/delete nodes (wi3.py),
  decrease-key on any block from any group (wi5.py), and CU78/80 moved into the R3 pushes (wi6.py). Best was 7.
- Structural Inv-late levers (erase function):
  - be1: range test before the -1 test (equivalent). Moves Inv late but changes code (fncmp 215).
  - be3: inverted -1 test. Worse.
  - be4: `goto einv` with einv at the end. No change.
  - c2-c5: asm-goto back edges to the -1 test. Loops; fncmp 281-356.

| var | base | change | fncmp | sig2 | inv |
|---|---|---|---|---|---|
| aw3/4/6/7 | z3 | wb3 3/4/6/7-conj | 64 | 6 | 14 |
| au1/au3 | z3 | u2 1/3-conj | 64/188 | 6/12 | 14/28 |
| ak4/akk | z3 | k55 2nd feed 4-conj / doubled | 64/130 | 6/12 | 14/22 |
| af1-af4 | z3 | fkbo label orders (i1 p1 / p1 dtg i1 / ndl dtg / dtg first) | 128,64,64,64 | 16,6,6,6 | 15,14,14,14 |
| aj1-aj5 | z3 | JMP order swaps (c3, s5, c8, c9) | 64 | 6 | 14 |
| aj6 | z3 | s4 JMP(i0,p0) | 132 | 16 | 18 |
| am1 | z3 | k55 feeds swapped | 64 | 6 | 14 |
| am2/am3 | z3 | 2nd feed char-style / removed | 86 | 12 | 15 |
| am4 | z3 | 2nd feed after k67 | 162 | 14 | 20 |
| ax1-ax3 | z3 | w5x position in -w test | 68,64,64 | 6 | 14 |
| ac1-ac3 | z3 | c12 JMP first / JMP(i0) / JMP(p0,i0) | 64/128/132 | 6/16/10 | 15/14/18 |
| be1/be3/be4 | z3 | erase restructure (above) | 215/148/64 | 15/14/6 | 21/29/14 |
| c2-c5 | z3 | JMP(eck) back edge from esucc/eout/eerase/efail | 288/356/281/344 | 24/25/18/29 | 25/34/22/27 |
| d1 | v23 | + k55 2nd feed | 72 | 8 | 16 |
| d2 | v23 | no r5x | 68 | 8 | 9 (back exact) |
| d3 | d1 | no r5x | 68 | 8 | 15 |
| d4w3/4 | d3 | wb3 3/4-conj | 64 | 6 | 14 |
| d2w3-5 | d2 | wb3 3/4/5-conj | 86 | 12 | 15 |
| d2u1/u3 | d2 | u2 1/3-conj | 68/128 | 8/12 | 9/22 |
| d2f1-f4 | d2 | fkbo orders | 68 | 8 | 16,9,9,9 |
| d2j1-j6 | d2 | JMP order swaps / s4 JMP(i0,p0) | 68 (j6 146) | 8 (20) | 9 (26) |

Conclusion: under bbro's fib-heap ties, the back group needs 55 to pop after 29/139/140, while the front needs
55 right after -r. No key-only or single-insert change satisfies both. The next idea needs a CFG change that
makes CU78/CU80 successors of a later trace than 55, or drops them from 55's insert list, without changing the
emitted code.
