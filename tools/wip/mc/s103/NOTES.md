# s103 (attempt 84): NO MATCH. Best stays s102/best.c (f2 24).

Sweeps (sw.py now skips conflicting substitutions instead of aborting):
- v1.txt (23): c11 fail feed 3->4 conjuncts + one other fail-feed conjunct +1/-1. Best 50 (c3 feed +1), 52 (c9 -1, s4 -1); rest 56-68.
- v2.txt (89): the 23 single feed tweaks alone on best.c (13 inert at 24, others 46+), plus c11=4 with
  the 3 best v1 tweaks paired with every other tweak: none below 46.
Conclusion: fail-feed conjunct counts cannot both demote clientBinPatch to round 4 and preserve the
round-4 heap order; the r4sim-guided model work (exact fibheap insertion order) was not done here.
