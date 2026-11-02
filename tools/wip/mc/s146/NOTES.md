# s146: tie fix + model-designed efail dummy (part c), profile-free mode_client

Base fb.c = s144/fb.c (f2 18). Tools: t.sh NAME (f2 + simulated r4 order), mke.py BASE (c3-style
dead `ex` block variants), enum1-4.py (r4sim enumerations), tie.py, run.sh DIR (s144 climb), fb/ e/.

## 1. Tie 143/144 (LC117/LC118) - FIXED: t6.c, f2 16 (ties s141/best16)
tie.py: in fb, trace 139 inserts 146(einv) 144(eout) 143(efail), both -2. The tie flips only by
inserting efail before eout (keys unchanged) or by changing keys. Source: `JMP(efail);` before
`if (block < cinfo->nandSize ...)` in clientEraseBlockI plus a cold label on efail
(`AT(efail) { efc: __attribute__((cold)); }`). Now efail enters at key 0 and is boosted by eout's
trace end (chg -1000100), so it pops right after eout: front is in ref order, only the f0 tail
differs (t6 tail 150 147 79 128 81 42 53 35 vs target 147 128 150 35 42 53 79 81).
Without the cold label (t1/t2/t3) 29-40.

## 2. Model for the extra entry (part c)
- enum2 on fb: 0 needs ALL of: LC114 (146) key -1, 128 (case-7 p0) first inserted by trace 108 (u2)
  or 121 (hdd4), and a dummy inserted by the efail trace at key 0 (absorber irrelevant: an
  unabsorbed dummy popping after the tail also scores 0). With 128 left in trace 127 (its natural
  case-7 dispatch) and <=2 dummies (enum3): floor 3 on fb, 2 on t4/t6.
- 128 is the untaken arm of the case-7 dispatch block 127, which pops before 108/121, so its first
  insertion is always by 127; an added edge from u2/hdd4 can only re-key it (and a key decrease is
  a priority boost that pops it at once). Adding JMP(p0) in u2 (t6u 16 unchanged, t6v 163).
  => the modelled exact recipe is not reachable with the natural CFG; part (c) alone cannot finish.
- enum2b on t6 shape with 128 from 108/121 forced: nothing <= 2.
## 3. c3 variants on t6 (mke.py)
- asm-volatile body (e1-e4, e8: hot/cold/none, JMP before/after log): the dead block (149) IS
  inserted by the efail trace at key 0 (model's shape), but 75 now pops early and 149 lands between
  79 and 42: f2 53. enum4 on that dump (128 move, LC114 key, absorber): floor 5.
- empty / goto bodies (e5 `;`, e6 goto einv, e7 goto efail): block folded away, = t6 (16).
## 4. Climbs (s144 gen/climb, -O3 flags of s101/f2.sh)
- fb: 6334 singles, 100-top pairs (4950), SA x2 (600 it): floor 18, nothing better.
- e (t6e2 + kk in clientEraseBlockI so gen can edit it; gen.py ce range fixed to
  clientEraseBlockI - the s144 port pointed it at the unused public clientEraseBlock): base 53;
  6324 singles floor 17 (dead kk feeds 603/607/608/618 -> usage lines 677/685/692/700 pull the
  dummy out; residual = the same tail hunks as t6), pairs floor 17, SA 27/28. Nothing <= 16.
## Semantics
JMP(...) is an empty asm goto that falls through; label attributes and `if (0)` dead blocks do not
change behaviour; `int kk = __builtin_constant_p(block)` is only read in dead conditions.
## Result
NO MATCH. Best f2 16: s141/best16.c and new s146/t6.c (front fully in ref order; residual is only
the f0 tail ordering, which the model says needs 128 inserted before the case-7 trace).
