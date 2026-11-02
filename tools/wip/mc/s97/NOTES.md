# s97 (attempt 78): NO MATCH. ~300 measured variants (log.txt; v1.sh, gen1.py g_/h_/j_ sweeps, ccs q.log on H1, gen2.py k_).
Best unchanged: best_s96.c (= b0.c here) 26/6/5.
- a00 = b0 + dead `cp(block+79)&&cp(block+80) goto efail` before the range test (s96 a14): Blk 2 in place, but
  Fer (LC117) rises to 3 and moves early; Success block (LC116) appears at freq 1 after -w; zero group scrambled.
- gen1.py: dead goto {efail,esucc,eout,einv,eerase} x 1/2 conjuncts at top/eerase/esucc(before/after)/eout/efail,
  on b0 (g_) and a00 (h_). Fer back to 2 only via an esucc SELF-LOOP (h_su_esucc_1 = H1.c, 42/10/18):
  CU108 -r Fer -w Blk ..., zero group starts CU81 and ends Inv.
- ccs on H1 (q.log, 118): nothing below 26; q_8_2 (k61l chain +2) gives CU108 -r Fer Blk CU33 CU29 -w:1 with the
  zero group right (42/10/6) but -w drops to 1.
- efail SELF-LOOP on H1 (j_fa_efail_1 / k_efail_*, any conjunct count 1-8): 30/8/11, CU108 -r Blk -w (Blk right),
  Fer at 4 early, zero group Info Pat CU35 CU42 CU53 Inv CU79 CU81. efail->einv edge: Fer 3 before -r (122/8/8).
  Conjunct counts in self-loops are inert (loop heuristics, not cp branch probs).
- kk.py (r4sim key overrides, single+pairs) on H1 bottoms at 5; wd.py on H1: only dummy-block inserts (key -3 at
  block 142 extraction, or a round-3 tail push) reach 3, none realisable byte-neutrally.
Next: lower Fer from 4 to 2 while keeping the efail self-loop (e.g. loop on a split sub-block of efail, or move the
esucc loop to esucc->efail with Success freq) and check Blk/Fer tie order; zero group then needs Inv/Info swap.
