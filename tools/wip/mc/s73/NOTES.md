# s73: hand-targeted levers on best82; NO MATCH (fncmp 82 -> 76)
- f.sh SRC.c: plain-flags fncmp count, diff in SRC.d (FNCMP_CONTEXT=2000 for full listing).
- Diff item 1 (test/je swap) FIXED by -wb second-arg check operand order:
  `{ int k = i + 2; b = argv[k]; if (!b || k == argc || *b == '-') client_usage(4, argv[i]); }`
  (only `!b` first gives 80; the k temp in a block gives 76). best76.c / best76.patch (vs s71/best82.c).
- perm.py: all operand permutations of every argv `if (A||B||C)` check: no further gain.
- Epilogue after netDisconnect (original duplicates add esp,92..ret there): tried goto ret single exit,
  asm goto before return, empty asm after netDisconnect, asm goto ndl edge: 76/76/76/84, no gain.
- Case 3 JMP(hdd5,s5) removal/swap: 76/100, no gain.
- sa.py = s71 SA with the -wb lever fixed on; 3 x 2400 s from best_s71w2.json: no fncmp gain (76).
- Remaining: cold error-block order, epilogue copy, rok X-operand leas (lea edx/ecx [56/59+esp]), base/index swap.
