# s117 (attempt 98): NO MATCH. New overall best: best.c (= best18.c) f2 18, all three blocks (141/139/145) right.
(previous overall best s102/best.c 24; s116/best.c 27.)

Path (on s116's b0.c, comb.py names; climb.sh/pairs.sh cost f2 + 10*blocks wrong):
- The c1 levers n00_t4/s06_s4 are NOT needed: r1 = singles on n07_c11 n25_s5 -> n26_c10 (JMP(c10) right
  after AT(c10), self-edge) gives 26 with all three right. Their reload blocks were intrinsic: every
  never-taken edge into t4/s4 from a block without cinfo in eax gets a `mov eax,[_cinfo]; jmp` block
  (tried edges after dsp, before netDumpNand, from t5/s5, "a"/"r" inputs on the asm goto: all worse).
- p1 pairs (top 40 distinct singles): + n19_dsp (JMP(dsp) after AT(s5)) + n31_i1 (JMP(i1) after AT(cdef)) -> 25.
- r3: + s07_c2 (c2 added to case 1's 2nd asm goto) -> 19 (fixes the 5/3 tail mostly).
- 19 had an extra `call _netDisconnect` (bbro duplicated ndl into the reboot-only path);
  `{ netReboot(reboot); JMP(fail); }` in dtg fixes it -> 18 (best18.c). `ndl: JMP(u2); netDisconnect();` also 18.
- k/ (b0 = best18): r1, r2 (u2/rok targets), p1 pairs: floor 18, nothing lower. Leave-one-out of each lever: all worse.
  ndl dead-conjunct lengths (g/), dtg/rok/ndl/u2 asm gotos (h/, m/), arg-parse asm gotos / label orders (c/, n/): none below 18.
Remaining diff of best.c (18 lines):
  1. u2 `call client_usage(2,0)` block placed 1 block early (ref 429) and the `[8+esp]=ebx` log block swapped (424 vs 465).
  2. reload `mov eax,[_cinfo]; jmp` (ref 502) = s5's JMP(s4,c12) edge into s4 (s4 is load-bearing: removing it -> 134).
  3. one client_usage(5, argv[i]) shared block (L608: -e/-c/-ip) placed after L407 instead of last.
~5000 variants compiled. Semantics: only empty never-taken asm gotos to existing labels (incl. a self-edge)
plus the existing dead __builtin_constant_p entries. Equivalent to src/mode_client.c.
