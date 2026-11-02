# s132 (attempt 113): NO MATCH. New plain-compile best f2 34 (was 42); floor stays s117/best.c 18.

Tools: gk.py BASE OUT off:form... (k-lever on the if at line offset `off` from the arg-loop `for`;
A=(c)&&!k, B=!k&&(c), C=k||(c); KV=name env for the k variable), gg.sh NAME BASE SPEC... (gk + f2 + dump + fq),
sw.py (disjunct permutations; only perm 102 is safe), gen.py/vars.sh/fq.py from s131. res.txt = ~500 measured.

## best34.c (= c0 + EK + EK2 + MK + K7 + `-bp` usage(4) test `(j == argc || !b || *b == '-') && !k`)
Equivalent to src: both k's are __builtin_constant_p of runtime values -> 0; every `&& !k` / `else if (!k)` is a no-op.
Synergy only: 18A alone 58, EK+18A 64, K7+18A 58, EK+K7 (s131) ~44, all three 34.
Remaining diff (asm 420-560): u2 (f4) placed first instead of after the two cold logs; one cold log (ebx) and
usage(4)/usage(3)/usage(0) blocks still shuffled.

## Measured, no gain
- k-lever A/B/C on all 22 arg-loop ifs: from c0 (66), from s131 f_FI 48 (66; 18A -> 44), from b44 (63), b34 (63),
  b18 (36, with KV=kk since b18 has a block-local k): all >= base.
- 32-combo grid {EK, K7, K12, reboot&&!k, 18A}: best 34.
- u2 is binary under every k/cp form: 4 or 0 (`reboot && !k`, `!k && reboot`, `!(k||!reboot)` -> 0 -> 38;
  cp(reboot/mode/ip/arg) inert). Asm-goto feeds from loop logs: f2 only from the -noenter log (76), others 0 (38-102).
- Splitting the 18A condition per disjunct: `*b=='-' && !k` or `(j==argc||!b) && !k` = 34, others 44-72.
- NO_MODE_ARG/netConnect/loop-condition k forms: 34-180. KU/FP/FI/P12/K12/PL/CT on b34: 34-228.
- Disjunct swaps on b34: >= 36.
## Conclusion
k-lever on the -bp usage(4) test is a new cheap improvement for the plain compile (42 -> 34), but u2 can't be
set to 2 locally and the cold usage tie order still differs; nothing beats b18's 18.
