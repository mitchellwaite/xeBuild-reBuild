# s115 (attempt 96): NO MATCH. Best still s102/best.c (f2 24; b0.c is a copy).

Systematic real-edge (empty asm goto) search on best.c. Tools: gen.py (family v), gen2.py (family w),
comb.py (apply any set of v/w edits: `python comb.py out.c s07_i0 n00_t4 ...`), run.sh DIR (f2 of
DIR/*.c, 4 parallel -> DIR/res.txt), scan.sh (flags which of 141/139/145 are placed right).
Targets throughout: c1 c2 c3 c7 c8 c9 c10 c11 c12 cdef hdd4 hdd5 i0 i1 p0 p1 s4 s5 t4 t5 dsp dtg ndl fail.

- v (464): append one target to each of the 21 existing asm-goto label lists in the function
  (r5x/r3x, w5x, rkv0, fkbo, the JMPs in c3/s5/c8/c9/c12, the dsp gotos). Floor 24 (130 neutral),
  39 compile errors. No stray jmp possible, but nothing moves 141/139/145.
- w (768): new JMP(t) before each `break;` in the switch and right after each AT() label (32 spots).
  Floor 24 (202 neutral).
- p (703): all pairs of the 38 singles scoring 25..34. Floor 24 (only neutral pairs).
- q (1192): n00_t4 (JMP(t4) at the end of case 1) + every valid single. Floor 25 (= base back + reload).
Total about 3100 real variants. scan.sh over all: no variant places 141 or 139 correctly. Only
145 clientInfo(NULL) ever gets fixed: JMP(t4)/JMP(t5)/JMP(s4) at the end of case 1/2 (n00/n02,
f2 27/28) and s07..s13 + i0 (f2 30). It always costs a cinfo reload (`mov eax,[l]` before the t4
test, the path skips dsp) and swaps the order inside the tail's `5` block (546-549 vs 553-556).
Adding the label to case 1's existing dsp gotos (s04..s06) instead is neutral (24), so the fix needs
a new edge.
Conclusion: single and pair zero-byte real edges into existing labels don't reach 141's round-4
placement or the 55-over-139 key order. The a_c6_c11 effect (141 right) needs a new case-6 block,
which this search space doesn't contain without a stray jmp.
Semantics: only never-taken empty asm gotos added (labels already exist, all in scope; the compile
errors were rejected). Equivalent to src/mode_client.c.
