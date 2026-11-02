# s78 (attempt 59): flag sweep + short climb

## Flag sweep (fncmp / sig2), extra flags on top of the plain compile
| flags | fx.c | best_s77.c |
|---|---|---|
| baseline | 98 / 24 | 196 / 14 |
| --param align-loop-iterations=100 | 98 / 24 | 196 / 14 |
| -O2 | 99 / 24 | 197 / 14 |
| builtin-expect-probability=40 | 614 / 62 | 728 / 54 |
| builtin-expect-probability=65 | 324 / 50 | 302 / 32 |
| drop -fno-ipa-profile | 98 / 24 | 196 / 14 |
None helps; keep the s77 flags.

## Climb
gr3.py 560 s each: from best_s77.c no gain (14,196); from fx.c -> best_s78.c (sig2 24, fncmp 86).
Only bcp-chain edits (compile-time dead), so semantics as fx.c. Order-diff fixes (WriteBl/Info0
priority, CU2, Ferase, -e group) not attempted this round. Logs: g*.log.gz/g*.out.gz.
