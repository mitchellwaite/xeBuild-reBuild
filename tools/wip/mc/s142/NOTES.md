# s142: bbro analysis of best16's residual (s141/best16.c, f2 16)

Files: dump.sh (bbro dump -> dd/NAME/), align.txt (s139/al.py P=s111/pf vs best16), srch.py (target +
singles/pairs), gr.py, beam.py (r4sim beam over key overrides), m.s/p.s (function asm, ours/profiled).

## A. What the 4 hunks really are (normalized log blocks are interchangeable)
Literal order of the standalone `log_printf(0,LC); jmp` blocks, profiled (= ref) vs best16:
  ref : LC157 | T(LC140..LC141) | LC156 LC155 | usage | T(LC142..LC143) | LC118 | LC117 ... LC147 | LC114 | clientPatches(NULL)
  ours: LC157 LC156 | T(LC140..LC141) | LC155 LC118 | usage | T(LC142..LC143) | LC117 ... LC147 | clientPatches(NULL) clientInfo(NULL) usage x3 | LC114
So three blocks are off, not two hdd blocks: hdd5 log LC156 (bb126) is one trace early, LC118
(clientEraseBlockI "outside system area", bb144) is before the LC142 trace instead of after it, and
LC114 (clientEraseBlockI einv, bb145) is at the end of the f0 tail instead of right after the LC147
block (trace 69..74). The minimal diff pairs them up as "394->461" and "554->536".

## B. bbro round 4 (best16 numbering; key = -freq, or -(1e6+100*prio+freq) with prio)
Pop order: ...127 152 126 105 49 121 144 108 55 143 62 33 29 69 128 150 35 42 53 145 79 81...
Target   : ...127 152 105 49 126 121 108 55 144 143 62 33 29 69 145 128 150 35 42 53 79 81...
Keys: 126 -4 changed to -1000104 (prio 1) by trace 30 (130/131 = case 8 clientReadBlocks; 131 is the
`__asm__ goto("" :::: S761)` lever from s139 -> edge 131->126 freq 1); 49 -7; 121 -4; 144 -3; 108 -3;
55 -2; 143 -2; 62 -2; 69 -1; 145/128/150/35/42/53 0 (ties).  In P both hdd logs are p3, LC140 trace p6.
r4sim: 126=-4 alone fixes LC156 (pops 49,126,121) but reshapes the fibheap so the f0 tail scrambles
(42 145 81 128 79 150 ...). 144 needs key in (-2 tie, after 55) and 145 needs to pop between 69 and 128
(-1 or prio) — both are tie-order dependent. Beam (5 deep, 40 wide, distinct orders) floor dist 2:
{126:-6,144:prio3} or {117:prio2,55:-3}; no override set reaches 0 within the sim (tail ties).

## C. Levers (t.sh NAME: f2 + clientEraseBlockI freqs + compiled r4 order)
- h2: case-8 lever `asm goto("" :::: S761)` -> `(S761, hdd4)`: 126 loses prio, pops 49,126,121 as in
  ref (exactly r4sim's 126=-4 prediction), f2 32 because the f0 tail reshuffles.
- clientEraseBlockI freqs (P: erase 5, success 4, failed 1, outside 2, invalid 1; best16: 4/2/2/3/0).
  e3 = drop the dead `if (bcp(block+9)) goto eout` after Success -> outside 2; y4 = + `JMP(efail)`
  (empty asm goto) in eout -> LC117 gets the eout->efail edge P has; z2 = + `esucc: __attribute__((hot))`
  -> success 3 / failed 2.  z2 = h2+e3+y4+hot = **front28.c, f2 28: every block up to ref line 535 is
  in ref order** (126 after LC141 trace, LC118 after LC143 trace, r4 pops ...69 as target).
- Remaining in z2: only the key-0 tail after trace 69..74: ours 42 128 81 146 79 151 35 53, ref
  146(LC114) 128 150 35 42 53 79 81 (LC114, clientPatches(NULL), clientInfo(NULL), usage x3, 79, 81).
  P has LC114 at f1/key -1; ours is cold (f0). Uncolding einv gives f4 (q1), removing the dead einv
  gotos f1 but re-breaks the front (q2 76); hot label on the outer then-arm inert (q3/q4).
  r4sim beam on z2 (target = z2 order with P's tail) floor dist 2: ties at key 0 depend on fibheap shape.
## Semantics
h2/y4: empty asm gotos fall through; e3 removes a dead bcp goto; hot label only changes estimates.
## Conclusion
NO MATCH. Best f2 still 16 (s141/best16.c); front28.c (f2 28) fixes all three misplaced log blocks
in the front and leaves only the f0 tail order (need LC114 at freq 1 / key -1 without moving the front).
