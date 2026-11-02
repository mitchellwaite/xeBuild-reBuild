# s100 (attempt 81): NO MATCH. ~850 measured variants (log.txt, climb3_*.log). Best unchanged: b0.c (= s96/best_s96.c) 26/6/5.

Tools: ev.sh NAME (fncmp, inv, hot = diff of r1-3 block list vs b0 from hs.py), sub.py MASK (b0 + subset of rdbest's
7 asm insertions), pos.py (asm at every ; { } of given lines), climb3.py BASE SEED N (lexicographic (fncmp,inv) climb
over p.out asm levers).
- All 127 subsets of rdbest's insertions on b0 (s_*.c): none below 26 (s_8 28, s_64 32). Single bits: 1,4,8,16,32
  keep r1-3 identical (hot=0) yet fncmp 82-158: round-4 trace extraction itself reshuffles (T26/T27 swap etc.).
  inv 3 needs bit 2 (asm after `goto dtg;` line 725, or anywhere on line 723/724): it splits the reboot-test block
  (hot 1:138:L726 -> 1:142:L725). s_42 (bits 2,8,32) = CU110 Blk -r Fer -w ... Pat Info, inv 3, fncmp 153.
- pos.py around lines 723-734 on s_40: inv 3 only from lines 723/724 positions (always hot=2); others inv 15/18.
- climb3 from s_42 (300): best 64/9 by random-walking many levers; from b0 (400): 238 evals sideways at 26/5, none lower.
Conclusion: the inv-3 shape requires the line-724 block split; no zero-byte lever found that gives it with hot=0.
