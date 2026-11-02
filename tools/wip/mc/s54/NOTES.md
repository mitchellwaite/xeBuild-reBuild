# s54: rok dispatch enabled (R2 kept at 0); round-3 case-key order still open

Result: NO MATCH. New best by es2: **c_s54.c** = c_r10 + full rok asm goto (16 labels, extra fakes p0 x1, c3 x2)
+ tree-only fkbo boost from the then-branch (replaces the latch) + 3 `goto ndl` diversions before dtg:
**es2 239 (R1 2, R2 0, R3 40, R4 143)**, ev 76, fncmp 236. (c_r10: es2 300, R3 56.) Best by ev is still s47/H5c2.c.

## Findings
- label -> spot (lab.py): c12 129, c11 128, p0 117, i0 130, c9 120, hdd4 112, hdd5 115, c2 108, c1 107, c10 121,
  u2 103, cdef 132, c8 119, c7 116, c3 109, s5 114; case-4/5 hwFlags tests are 113/110 (labels t4/t5 in lev.py).
- bb_to_key = -(1e6 + 100*prio + freq): prio = max edge freq from a trace-end pred, freq = block freq. Match R3 order
  comes from R2 tablejump prios 9..6 (profile). Plain: every tablejump edge has the same prio (4), so order = block freq.
- Why rok JMP broke R2: rok edges enter the fkbo boost loop body -> irreducible, so no loop scaling, and the trace stops
  before the tablejump. Fix: drop the latch and use a tree-only `if (bcp(mode+91..94)) goto fkbo;` in the
  NO_MODE then-branch (cur.py base()). The R2 tail then needs join*P(reboot) < 42.5 (exec_th = 217*200/1000 = 43, rounded):
  3 `if (bcp) goto ndl;` before dtg (base2()) keep join at 85.
- Exact rok edge freqs (cdef 6, hdd4/hdd5 3, u2 2, p0/i0/s5 0) can't be had with one asm (30-operand limit):
  you need >=21 extra fakes but only 14 fit. Leftover R3 diff: cB80/cB81 (p0/i0 get Cha'd).
- For the R3 order, t4/t5 would need freq above c8/c2/c9/c10/c11/c7/cdef, but those already get +2 from the fkbo edges.
  Boosts from fail (lev.py B) plus exit diversions (X) raise join over the threshold above, so R2 goes to 1. Not solved.

## Tools
rkgen.py (rok/fkbo fake constructs), cur.py (bases), lev.py (all levers: w, fk, B, X, npre, dd, dt), sa.py/sa2.py (SA,
logs sa*_s54*.jsonl), fq.py (compgotos dump with freq/edge probs + call map), r3.py (raw round events with spot
names, match | ours), bmap.py, lab.py, t1-t8.py (scans).
## Next
Get per-case freq ordering within prio 4 without raising join: e.g. lower the fkbo per-target share (more fkbo fakes via
a second chained asm that keeps the trace), or lower the dtg flow so case boosts fit under join <= 86.
