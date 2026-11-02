# s80 (attempt 61)

Base: best_s80.c = copy of s79/best_s79.c. Re-measured with s79/m.sh: fncmp 196, sig2 12 (unchanged).

## Semantics check of best_s80.c vs src/mode_client.c (diff reviewed by hand)
- All added `__builtin_constant_p(...)` conditions are on non-constant `i`/`mode`, so they fold
  to 0: every guarded `goto`/`mode = 7/11/9` is dead (bcp-dead).
- `JMP(...)` / `__asm__ goto("" :::: L)` and the rk*/fa* asm-goto fans are empty asm: fall through
  at run time (zero-byte hints); labels added (lu1, k55l, k61l, k67l, dsp, t4, t5, s4, w5x, ...) are labels only.
- `-r`/`-w`/`-e` branches wrapped as `} else { L: if (...) {` with the three closers `} } }` after the
  final `client_usage(1, argv[i])`: else-grouping intact.
- `-ip`'s second arg: `k = i+2; b = argv[k]; if (!b || k == argc || *b == '-')` vs original
  `i+2 == argc || !b || ...`: argv[argc] is NULL, no side effects, same result.
- `-w`: `({asm goto w5x; 0;})` conjunct is 0 at run time; `if (mode) { w5x: client_usage(5,..) }` same.
- hdd4/hdd5 cold labels, `JMP` inside cases, extra `asm goto dsp` before `break`: hints only.
- clientEraseBlockI added as a static copy with labels (eerase/esucc/efail/eout/einv) and JUMP(efail): same behaviour.
Conclusion: semantics-preserving.

## Work
Only the baseline confirmation and the check above were done this attempt; no new variants
improved on (196, 12). Remaining order diffs are unchanged from s79/NOTES.md (Info0 vs -ip,
CU before -r, Ferase after -w, -e group fibheap tie order).
