# s134 (attempt 115): NO MATCH. Plain best stays s132/best34.c (f2 34); overall floor s117/best.c (18).

## 1. r4sim on best34 (dd/b34/mc.bbro; tag.py maps asm lines to bbro blocks via gcc -dA)
Window heads, best34: 49 103 112 115 55 126 61 130 125 29 67 127 77 117 33 42 35 53 79
Target (ref):         49 112 115 103 55 126 125 61 33 29 67 127 130 117 35 42 53 77 79
(103 u2 f4; 112/115 reboot logs f2; 126 eout; 125 efail(ebx log); 130 Info(NULL); 117 Patches(NULL);
 127 einv; 33 usage4 ecx; 29 usage3 ecx; 35/42 usage5; 53/77 usage3; 79 usage5.)
- Exhaustive singles/pairs (keys -8..0, window blocks), triples (13 blocks, keys -4..0, 37765 sims), and
  SA (window and all blocks, full-order metric, arbitrary many overrides): 0 exact hits, floor distance 4.
- u2 at 0/-1/-2: arm 55 (inserted at key -2 when 49 is processed) pops between 112 and 115; target needs
  112,115,103 all before 55 which only happens via fib-heap tie history with u2 at -4 or logs < -2.
  The prefix alone (..61) is reachable only with 112/115 more negative than -2 (e.g. 112:-6 115:-4);
  the 61..117 segment alone is never exact. Keys can't produce the target: needs different block/insert set.
- rs.py / rs2.py / rsa.py = searches.
## 2. Automated lever generator (gen.py, climb.py)
Edits: k-lever A `(t && !k)` / C `(k || t)` on every if condition and every sub-term (51 conds, 200 edits);
hot/cold label on every statement (122 stmts, 244); dead `if (k) goto` and empty asm goto from every statement
to 31 cold targets + rok/fail (7432 singles total). Cost f2*100 + diff hunks (r4sim block ids aren't stable
across variants, so hunks used as tie-break).
- Singles 7432: none < 34; 1867 inert (34). Best non-inert 36.
- Greedy: no improving step. Pairs over the 100 best distinct non-inert singles (4950): floor 34.
- SA 4 chains x 450 over 4000 singles: all end at 34 (base).
- ~13.8k real compiles in total (v/g_*.res, cache.jsonl).
- Hot label on the reboot logs (raise to f3 for the prefix solution): 42/43, moves another log instead.
## 3. Semantics
All edits: k = __builtin_constant_p(runtime) = 0, so `t&&!k`==t, `k||t`==t (same evaluation order);
labels/hot/cold no-ops; `if (k) goto` dead; empty asm goto falls through. Equivalent to src/mode_client.c.
## Conclusion
Exhausted for this family: the window order is not reachable by key changes (r4sim proof-by-search) and
the generated lever space has no improvement over best34.
