# s81 (attempt 62): hand levers on the four round-4 order diffs

Base best_s80.c (fncmp 196, sig2 12). New best: **best_s81.c (= n1.c): fncmp 68, sig2 8**, semantics-preserving
(diff vs best_s80: bcp-dead gotos on non-constant i/mode/block, braced cold labels, label-only, empty asm JMP).
Tools: r.sh NAME BASE old new ... (mk.py + fncmp + sig2 + tail order with freqs), tail.py,
r4sim.py (round-4 replay on tools/wip/fibsim.py with per-block key overrides; reproduces gcc exactly),
srch.py / sa.py (what-if key searches against the target order).
NOTE: dd.sh in s77/s79 swaps LC114/LC117: LC117 = "Failed to erase" (Ferase), LC114 = "Invalid arguments". Fixed in tail.py.

Target round-4 tail (original): inv -ip hdd5 hdd4 CU107(u2) -r Blk Fer -w CU33 CU29 -e Inv Pat0 Info0 CU35 CU42 CU53 CU78 CU80 -c
(Info/Patches cold calls in the original are the NULL ones: clientInfo(NULL)/clientPatches(NULL); hot ones take arg.)

| var | base | change | fncmp | sig2 | effect |
|---|---|---|---|---|---|
| **diff 1: Info0 prio / hot-cold sense** |||||
| a1 | s80 | cold label i1 -> i0 | 228 | 18 | Info leaves tail, -e group shuffles |
| a2 | s80 | a1 + drop i1 from fkbo | 224 | 24 | Info f0 but -r/Blk swap |
| a3 | s80 | a1 + fkbo i1->i0 | 208 | 14 | Info143 still prio |
| a4 | s80 | drop i1 from fkbo only | 232 | 28 | (= s79 k1) |
| a5 | s80 | a1 + s4 JMP(i1)->JMP(i0) | 216 | 14 | |
| **a6** | s80 | a1+a3+a5 | **192** | 12 | hot Info(arg)/cold Info(NULL) sense now right (fixes the je/jne diff) |
| a7 | s80 | a1 + fkbo i1->c12 | 252 | 28 | |
| b1-b10 | a6 | fkbo i0 -> fa21/c12/c2/c11/c8/hdd4/u2/c3/t4/efail | 112-246 | 18-28 | b7 (u2) fncmp 112 but u2 gets fkbo prio before -ip; efail not in scope |
| j_*_1..4 | g6,h4,i3 | fkbo i0 -> none/c12/i1/hdd5 | 90-148 | 10-28 | **j_i3_3 (i1) removes Info prio, hot order intact: 96/10** ; c12 reshuffles hot part |
| **diff 2: CU(2,NULL)=u2 (bb107) before -r** |||||
| c1-c7 | a6 | goto u2 feeds in fail block / chain lengths | 192/222 | 12/24 | fail is cold: no freq change; removing feed (c4) worse |
| d1,d9 | a6 | loop-head u2 feed 1 conjunct | 146 | 18 | u2 f4 (too high) |
| d2-d7 | a6 | extra/changed feeds (post-loop, ==3 forms) | 192 | 12 | no freq change (saturated) |
| d8 | a6 | feed `bcp(i+320)&&bcp(i+321)` (int form) | 146 | 18 | u2 f3, but before hdd4 (tie -3) |
| d10/d11/d12 | a6 | 2 feeds / `||` / 2x2-conj | 98/144/220 | 14/18/12 | u2 f5/f8/f2 |
| e1-e5 | d8 | raise hdd4 (post-loop goto, JMP dup, i0 fan) | 82-170 | 12-22 | **e4: JMP(hdd5,s5,hdd4) in c3 -> hdd4 f5, u2 after both: 82/12** |
| f1-f6 | e4 | hdd5 vs hdd4 order | 82-154 | 12-20 | **f5: JMP(hdd4,s5,hdd5) -> hdd5 hdd4 u2 order = original** |
| **diff 3: Ferase before -w** |||||
| g1-g3 | f5 | goto efail before eerase (1-3 conj) | 148 | 18 | Fer stays 1, -r/-w reshuffle |
| g4/g5 | f5 | JMP(efail) from eout / at eerase | 84/151 | 12/18 | |
| **g6** | f5 | esucc: `if (bcp(block+7)) goto efail;` | **70** | 10 | Fer f2, pops before -w (diff 3 fixed) |
| h1/h3 | g6 | cold einv (Inv f0) [+cold p0] | 144/104 | 18/14 | Fer jumps to f3 |
| h4-h7 | h3 | drop / weaken esucc feed (0,2,3,4 conj) | 100/100/84/84 | 14/14/12/12 | h4: Fer f2 + Inv/Pat f0 |
| k3/k4/n2 | j_i3_3/m1 | feeds into eout (Blk) | 76-148 | 10-14 | Blk f3 but Fer drops to 1 |
| **diff 4: -e group / fibheap ties** |||||
| h2 | g6 | cold p0 | 128 | 14 | Pat f0, after -e |
| i1-i5 | h4 | k67l feeds (1..3 conj, int form) | 156-284 | 18-34 | **i3 (3 conj) -e f1, pops right after CU29/CU33** |
| k1,k2,k5,k6,k7 | j_i3_3 | k55l/k67l/k61l feed edits | 96-148 | 10-16 | mostly saturated; k7 (no k67l feed) -e back to f0 |
| l1-l4 | j_i3_3 | drop k61l feeds | 86-112 | 14-20 | -w f1 |
| m1-m4 | l2 | label wb3 on -wb usage3 + feed (2/3/1 conj) | 68-86 | 10-14 | **m1: CU29 f2; after -e: Inv Info Pat 35 42 53 80 78 -c (near target)** |
| **n1** | m1 | re-add k61l feed after k55l feed | **68** | **8** | -w f2 again |
| n3-n5,o1-o5 | m1/n1 | k55l strength, wb4 label feed, wb3 feed forms/places | 68-96 | 8-12 | freq 1<->2 cliff only |

Current (n1) tail: inv -ip hdd5 hdd4 CU107 CU29 Blk Fer -r -w CU33 -e Inv Info Pat CU80 CU78 CU35 CU42 CU53 -c
Remaining: CU29 must be f1 but pop after CU33 (f1 ties); -r before Blk/Fer; Pat before Info; CU35/42/53 before 78/80.
r4sim key searches (sa.py on m1/j_i3_3 dumps) never reach 0 inversions with <=10 key overrides: with these heap
histories the f0 group order cannot be reached by key changes alone; the round-3 push order (53 42 35 pushed in that
order) and round-4 insert timing would have to change. Next: use r4sim to search over *insertion order* (round-3 trace
order of 33/29/35/42/53 pushes) and then find levers for that.
