# s147: goal 1 probes (move case-7 p0 block off the dispatch trace), profile-free mode_client

Base s146/t6.c (f2 16). t.sh NAME = f2 + simulated r4 tail (copy of s146/t.sh). All variants edit
only the case-7 p0 arm / the u2 arm of t6 (JMP = empty asm goto falling through; `if (0)` blocks
reached only by goto; semantics unchanged: p0 still calls clientPatches(NULL) then falls to dtg).

| file | change | f2 | tail |
|---|---|---|---|
| v1 | p0: JMP(u2) then label p0x + call; u2: JMP(p0x) | 108 | front broken |
| v2 | p0: JMP(hdd4) before call | 92 | front broken |
| v3 | p0: JMP(u2) before call | 16 | = t6 (asm edge folded) |
| v4 | v1 with cold label on p0x | 162 | |
| v5 | p0: JMP(hdd4); u2: JMP(p0x) | 156 | |
| w1 | case 7 p0 = `goto p0`; body moved to `if (0)` block after u2 | 16 | same order, block renumbered 109 |
| w2 | w1 + JMP(p0) after client_usage in u2 | 16 | same |
| w3 | w1 without cold label | 76 | |
| w4 | w1 + JMP(p0) before client_usage | 163 | |

Insight: wherever the clientPatches(NULL) block sits in source, `goto` is threaded so it is still a
direct successor of the case-7 dispatch block, which pops before traces 108/121; extra asm-goto
edges from u2/hdd4 either fold away (no change) or perturb the front heavily (asm goto splits u2 /
hdd4 blocks and changes their freqs). Goal (iii) not reached. Goals 2/3 (alt enum on t6, fixed
s146/e climb from t6) not run this session.

NO MATCH, best f2 still 16 (s141/best16.c, s146/t6.c).
