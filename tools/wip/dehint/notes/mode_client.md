# mode_client de-tricking

Goal: `build/mc/reference.o` (copy of a matching build/obj/mode_client.o) byte-identical with
fewer hints.  141 tricks at the start of attempt 1 (README.md's list: `--param
builtin-expect-probability=50`, 89 `__builtin_constant_p` feeds, 19 asm goto, 10 pins, 7
hot/cold labels, 6 expects, 3 `if (0)`, 3 `__builtin_unreachable`, 2 literal-order asm "i",
clientEraseBlockI inlined by hand).

## State after attempt 1

**105 tricks** by README's categories (141 before): 33 `__builtin_constant_p` and 3 asm goto
statements gone, no new hint, no borderline shape.  Whole object IDENTICAL BYTES, full build
SHA256 10dac648...1971c, progress 617/617.  build.sh unchanged (the param is still needed).

Remaining, by category:

| Category | Before | Now | Where |
|---|---|---|---|
| `--param builtin-expect-probability=50` | 1 | 1 | build.sh (plain -O3: 736 lines) |
| `__builtin_constant_p` | 89 | 56 | 2 in clientEraseBlockI (dy feed and back edge), `kk` (memset size / `if (!kk)`), u2 at the loop head, the 3-term `(char *)` k61l feed in `-s`, -r's k61l, after the loop (dtg), rok's ndl, dsp's t4 (4), the mode=7/11/9 chain (6+6+5), ndl tail s5 (4) and u2 (1), fail's 10 feeds (4+3+4+1+4+1+1+1+1) |
| asm goto statements (JMP / `__asm__ goto`) | 19 | 16 | rok list now 9 labels (was 26), fkbo list 27 (was 30), c3's JMP(hdd4,hdd5) (s5 gone) |
| pins | 10 | 10 | bp `"a"(i + 1)`, two `"=D"/"D"` blocks + `"r"(count)` in clientBinPatch, `-i`/`-p` `"d"(i + 1)`, `"a"(i)` in the `-r` head asm goto, `"a"(cinfo)` in case 5, fkbo `"X"`, rok `"m"` |
| cold labels | 7 | 7 | efc, einv, ac, rok, hc4, hdd5_c, fail |
| expects | 6 | 6 | E on -bp/-wb/-eb and reboot (+ the macro) |
| `if (0)` / unreachable | 3 / 3 | 3 / 3 | dy, dv, dz |
| literal-order asm "i" | 2 | 2 | clientInfo, clientWriteBlocks |
| hand-inlined clientEraseBlockI | 1 | 1 | |

Also removed, not in README's counts: clientEraseBlockI's `efcl: asm volatile("" : : "i"(64))`,
clientEraseBlock's unused `kk`/`AT(efail)`, rok's dead trampoline sub-block (rk14-rk51), every
trampoline that no list reaches (rk/ork, fa/ofa), and the unused plain labels (eerase, esucc,
eout, lu1, wb3, k55l, k67l, w5x, dvb, fkbo, S761, p0, p0c, i0, i0_c, c8, c8t, c9t).
Labels nothing jumps to never mattered.

## Attempt 1

Tools (tools/wip/dehint/):
- `mc1lib.py <file.c> [-np] [-v [fn]]`: compile as build.sh does (`#line 1 "mode_client.c"`, `-O3
  --param builtin-expect-probability=50`) and compare with build/mc/reference.o (whole file
  bytes, else .text disassembly per function, .rdata/.data/.bss and relocs).  ~0.7 s a compile.
- `mc1.py list|singles|greedy|pairs|climb|show|count`: cuts the source (MCBASE=<file>, default
  src/mode_client.c) into a template of slots.  Manual slots (pins, literal asms, dead blocks,
  the kk construct, the mode chain), automatic ones: every cp feed `if (cp && ...) goto L;` as a
  list of terms (drop terms or all), every asm goto label list (drop labels), cold labels
  (drop, or keep as a plain label), expects.  Post edits: `inline` (call clientEraseBlock),
  `rok_all`, `fk_all`, `-np`; groups (G_dy, G_dz, G_dv, G_efail, G_kk, G_dpin, G_hdd, G_dsp,
  G_cebi, G_E) remove a dead block with every edge into it.  `climb`: greedy, then singles and
  pairs (of edits within `-m` lines) on top, take a pair, repeat.  MCCHAIN=lists makes the
  mode=7/11/9 arms term lists.  Slot names carry a running index, so names differ between
  bases; states (build/mc/*.json) belong to the base they were made on.
- `mc1clean.py in.c out.c`: drops dead trampolines and unused plain labels one at a time,
  keeping each that stays IDENTICAL.

Runs (states and logs in build/mc/, not tracked):
1. singles on the start: 47 of ~210 edits IDENTICAL alone.  Free: clientEraseBlock's kk and
   AT(efail), efcl, rk_dead1, s5 in c3's JMP, rk0-rk13 alone, and any single term of the
   feeds u2(750), ndl(5562..), dtg(7351..), dtg(5569..), ndl(7368..), dtg(6949..).
2. greedy (free edits first, then by single diff): 138 -> 123 in my count (build/mc/g1.json).
3. pairs on g1 (69 near misses, diff <= 60, 2338 pairs): only `j_dsp_36` (default's `"i"(109)`
   asm goto) with one cp term dropped from the dtg/ndl chains.
4. climb -m 24: round 1 took that pair, greedy went on (j_i1, rk1/8/13, dv list's dsp, c7, c8,
   cdef, fa0, fa1, dtg, c3, the `-s` cdef feed, more chain terms) to 109; round 2 took
   `cp_c9_7-ALL + j_c11_27-c11` (dsp's whole c9 feed with c8t's JMP(c11)) and reached 103;
   round 3 no pair.  pairs -m 80 on that state (61 near, 1793 pairs): none.
5. mc1clean on it, then a new base (build/mc/c2.c) with the mode chain arms as term lists:
   one more term (arm 9's first) -> 102.  pairs -m 30 (30 near, 434 pairs): none.
6. Hand tidy (braces and blank lines around removed labels): still IDENTICAL BYTES; full build
   matches.

### What each remaining hint is needed for (singles on the final state)

Diff = differing disassembly lines; sizes from build/mc/singles2.json (final state).
- Near misses (<= 30 lines), all bb-reorder ties between two adjacent cold tail blocks or a
  swapped pair of `client_usage(5, ...)` / log blocks, or the literals' .rdata order:
  ci_lit 4 (clientInfo's .rdata), each wb_lit operand 6-14, the whole fail feed to t5 8,
  E(reboot) 10 (two usage tails swap), bp_rcount 12 (clientBinPatch reload thread), c3 feed
  terms 18, hdd4 in c3's JMP 18, bp_D either block 20, dsp's t4... c9 feed 22, mode chain arm
  11 terms 24, arm 9 terms 28, fail's ndl(205562) feed whole 24, bp_pin 30.
- 35-60: `-p`/`-i` `"d"` pins 35/41 (both 52), rok list's c12 and rk6 44, every fa2-fa20 edge
  44 (each edge into fkN counts; the 19 of them set its frequency), case 5's c12 50,
  hc4 cold 56, JMP(dz) 60.
- 78-150: the `-r` head `if (!kk)` block 78 (G_kk 78), JMP(c10) 92, JMP(dy) 122, rok's dv
  edge 136, the dy feed 144.
- 170+: everything else, up to 736 (-np).  Large ones: E on -bp/-wb 457-597, rok cold 422,
  fail's t5 feed terms 394, cp_dtg_4 (after the loop) 392, fkbo's "X" asm 358, inline 265.
- Compile-only dependencies: dy/dv/dz blocks need their edges gone first; `kk` is used by the
  memset and `if (!kk)`; fail's label is jumped to.

### Mechanisms observed

- Feed chains are not all-or-nothing.  `cp(a) && cp(b) && ...` chains could often lose terms
  one at a time, but which terms can go depends on how many have gone elsewhere: at the start
  any single term of six chains was free, at the end dropping one term of fail's t5 feed costs
  394 lines while dropping the whole feed costs 8.  The removals interact through counts
  (SSA names, blocks, edges into a target), not through the term's constant.
- Pairs work as compensation: removing the default case's `"i"(109)` asm goto alone moved two
  tail blocks (8 lines), and dropping any one cp term in the dtg/ndl/dtg chains put them back.
  Same for the c9 feed + JMP(c11).  So many 8-line near misses are tie flips of a single heap
  key, fixable by another single change of the same weight.
- Edge multiplicity matters: rok's list keeps c12 directly and also rk6 -> ork6 -> c12, and c3
  only through rk10 -> ork10 (the direct c3 went).  The 19 fa edges into fkN each count.
- Unused labels, dead trampolines (labels no list names), and scope braces without
  declarations never changed a byte.

### Don't retry

- Any single removal or single term drop on the final state (all tested, table above);
  pairs within 80 lines on the 103 state, within 30 on the 102 state.
- `-np` (736), all four E's with -np (609), inline clientEraseBlock (265, also with all of
  clientEraseBlockI's hints gone: 265), rok_all (328), dropping the whole fkbo construct.
- Removing a dead `if (0)` block together with its edges (G_dy 225, G_dv 203, G_dz 60 at the
  first greedy state).

### Ideas for attempt 2

- Triples / climb with a wider pair window on the 8-30 line near misses: they are tie flips, so
  two or three paired removals may cancel (e.g. E(reboot) 10 + a term drop; ci_lit 4 is only
  clientInfo's literal order, try the success-first shape with another join).
- Replace the fa2-fa20 edge bundle (19 edges into fkN) by something with the same frequency
  effect: a cp chain feeding fkN, or a loop-free natural construct.
- The literal-order asms (ci_lit 4, wb_lit 6-14) are small and local: try nested/success-first
  shapes and result-variable joins in clientInfo and clientWriteBlocks (options' lever).
- clientBinPatch's pins (bp_D 20, bp_rcount 12): try local types/scoped temporaries for count
  and start (keys' and sendAvatarData's levers) rather than asm.
- Model-based (tools/wip/mc/s86/r4sim.py) recomputation of which heap keys the remaining feeds
  set, then search for natural code that yields the same keys.
