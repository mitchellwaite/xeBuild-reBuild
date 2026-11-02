# s88 (attempt 69): NO MATCH. New best 36 (v06.c), -bp regalloc diff FIXED

~530 variants measured: v01-v11 hand (rv.sh, log.txt), 16 single-line perms (en.sh: lines 667/739/799, all no-op),
3 fail-line climbs on v04 (hc11-13.log, 210), 2 on v06 (hd21-22, 120), 3 on v10 (he31-33, 180). hc.py now takes a per-seed tag (parallel-safe).

| var | base | change | fncmp/sig2/inv |
|---|---|---|---|
| v01-v03 | e01 | -bp pins "r"->"d" | 188/15/29 |
| v05 | e01 | drop first -bp pin | 68 (no change) |
| **v04** | e01 | first -bp pin `__asm__("" :: "r"((unsigned)(i + 1) * 4))` -> `__asm__("" :: "a"(i + 1))` | **42/8/6**: the 24-line "-ip" (actually -bp arm) eax/edx swap is gone |
| v07-v09 | e01 | other pin combos with "a" | 42 |
| **v06** | e02 | same "a" pin | **36/10/18** (best) |
| v10 | z3 | same | 38/6/14 |
| v11 | h1 | same | 92 |
| climbs | v04/v06/v10 | fail-line perm | plateaus 36/18, 38/14, 42/6-7; no lower |

Remaining (v06): back-of-function cold block order only (usage(3)/(5) pairs, a log_printf(ebx) block, call/jmp pair
near sendcompatdata). v04/v10 share the misplaced `log_printf(...,ebx)` block (moves ~35 lines later).
Lines 667/739/799 goto order: no effect. Next: other dead-goto kinds (asm goto chains on dsp/rok lines; pf.py only
handles `if (...)` statements) on v06/v10; try the "a" pin with other e01-class fail perms.
