# s90 (attempt 71): NO MATCH. Best unchanged: s88/v06.c 36/10/18 (c38 42/8/9)

~270 variants (log.txt; sweeps sw.sh -> swa.txt, swb.txt, swv.txt), all single rok-fan (ork_i) retargets:
| sweep | base | n | result |
|---|---|---|---|
| each rkE ork (11-21,43-51) -> each case c1,c12,s5,c8,c10,cdef,t4,t5,c3 | c38 | 180 | 159 unchanged 42/8/9; ->c10 (and a few cdef) 38/12/18 (undo Keys fix); ->t5 42/10/19; 3 at 66 |
| each non-rkE ork -> rkE | c38 | 32 | 30 unchanged; ork9/ork10 -> rkE back to v06 (36/10/18) |
| rkE ork -> c3/t4/c8 | v06 | 57 | 36 or 37 |
Finding: single fan-edge retargets are inert for the back cold-trace order (-r/Blk, -w, Fer); the
fan edge counts only matter for the c3 threshold. Back order needs a lever outside the rok fan
(insert order of freq 0-2 traces), not more dead edges. r4sim what-ifs not redone this round.
