# build de-tricking

Goal: `build/bd/reference.o` (copy of a matching build/obj/build.o) byte-identical from plain
`-O3`, with fewer hints.  52 tricks at the start of attempt 1.

## State after attempt 1

50 tricks: `--param builtin-expect-probability=98`, 19 `__builtin_expect`, 9 pins, the empty
`__asm__ __volatile__("")` barrier at loadBl's `fail:` (README's list counts barriers; the earlier
count of 52 had missed it), 6 hot and cold labels, 5 `cb_hint()` calls, 2 `__builtin_constant_p`,
3 `no-early-inlining`, 2 inlining attributes (`noclone` on loadInputFile, `noinline` on
extractSmcConfig), 2 `__builtin_assume_aligned`.

Landed shapes to review:

| Where | Shape | Why it's borderline |
|---|---|---|
| xebuild.h | `struct fileent files[XB_ADDONS]; struct fileent addons[16];` | The addons are still spelled `files + XB_ADDONS` (mode_build, mode_update, options), past the declared bound. One view for every object, not a per-file one, and all objects are byte-identical; any of 19, 20, 21 matches |
| checkBl | `goto toobig`, with the size error's text after the crc error's | Text order only, for .rdata. Plain `if (blsize <= size) { ... }` nesting matches too |

## Attempt 1

Tools (tools/wip/dehint/):
- `bdlib.py <file.c> [-v [fn]] [-L] [-np|-p N]`: IDENTICAL or per-function lines against build/bd/reference.o
  (make it with `cp build/obj/build.o build/bd/reference.o` after a matching build). `-L` or BDLOOSE=1 ignores
  jump targets and padding, to read what's really different. A compile takes about 1 s.
- `bdtricks.py singles|pairs|greedy|show` (every trick as a named edit; BDBASE, BDFLAGS), `bdc.py a,b c,d` (score
  sets), `bdshow.sh a,b [fn]` (diff with those off), `bdcheck.sh file.c fn` (block frequencies from the
  .optimized dump), `bdsweep.py bdgen/gen_bdN.py [-n TOP] [-k label]` (cross products of edits).
- `bdgen/gen_bd*.py`: this attempt's sweeps. Write them with the Write tool; heredocs mangle `\n`.

### What landed (52 -> 49, all IDENTICAL, full build SHA256 matches)

1. **Literal-order asm in checkBl.** The .rdata order crc, size, magic is the text order: put the size error's
   block after the crc one's (`goto toobig`, or nest the rest in `if (blsize <= size)`). No effect on code.
2. **always_inline on loadConsoleBl.** The switch written in loadConsoleBlFiles' loop, `r = 0` first. Hand
   inlining is source shape, and it's what always_inline did at early inlining. Side effect: exp_t2 went from
   405 lines to 8, and exp_t9 and lab_none are cheaper too.
3. **XB_FILES_BOUND.** Every object is byte-identical with `files[19]`, `[20]` or `[21]`, so there's no reason
   for a per-file view: xebuild.h now declares `files[XB_ADDONS]` and `addons[16]`. Build needs 19 to 21:
   18 and 22 cost 10 lines in verifyBlSigs, 24 costs 122. (NOTES.md line 446 and README still mention the macro.)

### Cost of each remaining trick alone

Lines: strict, then loose (BDLOOSE, ignoring targets and padding).

| trick | strict | loose | functions |
|---|---|---|---|
| pin_p60 | 2 | 2 | loadBlFiles |
| pin_p | 2 | 2 | loadConsoleBlFiles |
| nei_blmod | 2 | 2 | patchBlsBlmod |
| addr_size (`(void)&size`, not counted) | 4 | 4 | extractSmcConfig |
| lab_t5le | 7 | 0 | loadBlFiles |
| noinline | 8 | 8 | extractSmcConfig |
| exp_t2 | 8 | 4 | loadConsoleBlFiles |
| pin_type | 11 | 5 | checkBl |
| cb1 | 12 | 4 | patchSmcConfig |
| pin_src | 18 | 18 | extractSmcConfig |
| exp_pr | 18 | 2 | loadBlFiles |
| exp_upd | 18 | 12 | addUpdateBls |
| pin_i | 22 | 22 | extractSmcConfig |
| pin_d | 23 | 14 | loadBlFiles |
| exp_400 | 25 | 5 | extractSmcConfig |
| pin_e | 26 | 26 | loadFileCrc |
| exp_t24 | 29 | 7 | addBlsToImage |
| exp_210 | 43 | 11 | extractSmcConfig |
| lab_nf1, lab_nf2 | 43 each | 22 each | extractSmcConfig (108 together) |
| exp_devgl | 43 | 7 | buildFlash |
| nei_smc, cb2, cb3 | 52 each | 40 each | patchSmcConfig |
| lab_badsize | 61 | 32 | loadBlFiles |
| aa_p | 62 | 38 | loadConsoleBlFiles |
| pin_size | 82 | 40 | calcBlAreaSize |
| exp_verbose | 83 | 18 | loadFileCrc |
| lab_size | 84 | 15 | checkBl |
| exp_200 | 97 | 29 | extractSmcConfig |
| exp_t10 | 116 | 46 | loadBlFiles |
| vol_fail | 145 | 75 | loadBlFiles |
| crc5..crc13 | 152 each | 96 each | checkBl (any one alone is the same as all 7) |
| cb5 | 158 | 100 | checkBl |
| exp_t9 | 217 | 85 | loadConsoleBlFiles |
| cb4 | 230 | 120 | patchSmcConfig |
| pin_m | 242 | 140 | checkBl |
| aa_60 | 251 | 68 | loadBlFiles |
| lab_none | 350 | 267 | loadConsoleBlFiles (see below: 8 with the precheck gone too) |
| exp_27 | 470 | 211 | loadBlFiles |
| nei_chk | 487 | 257 | checkBl, loadBlFiles |
| noclone | 21550 | 20698 | everything (ipa-cp clones) |

All 820 pairs of the cheap ones (before landings 2 and 3): none IDENTICAL (build/bd/pairs.txt isn't kept).
Useful groups, by the numbers:
- **The two 0x60 copies, 4 tricks for 4 lines:** pin_p+aa_p and pin_p60+aa_60 each cost the same 2 lines as the pin alone.
- **patchSmcConfig, 5 tricks for 40 loose lines:** nei_smc+cb1..4 off only swaps two cold traces.
- **checkBl, 9 tricks for 15 loose lines:** cb5, lab_size and the 7 crc expects off together.
- **loadFileCrc, 2 tricks:** exp_verbose+pin_e costs 18, the same as exp_verbose alone.
- **loadBl, 2 tricks:** lab_t5le+exp_pr, 13 strict and 2 loose.
- **loadConsoleBlFiles, 2 tricks:** lab_none with the `nFiles <= 1` precheck gone too: 8 strict, 4 loose.

### Mechanisms

- **The 0x60 copies (pin_p, pin_p60).** The store `e->size = 0x60` must stay before the rep movs setup. sched2 only
  does that with a dependence. e is `&xb.files[i]` (points to xb) and p is malloc's (points to a heap var), so PTA says
  they don't alias. With a pin, p points anywhere, but then it needs assume_aligned too, as malloc's alignment is gone.
  gen_bd9: plain, sizeof, `e->size` as the length, memmove, struct copy, src and size locals and pointer types all keep
  the 2 lines. The original knows the alignment, so its p is probably still malloc's, which suggests e isn't known to
  point to xb there (a param or a loaded pointer has the escaped solution, which includes an escaped heap var).
- **checkBl.** Layout needs size error >= 10% of entry (epilogue copy) and bad < 10%. `return -3` gets
  PRED_NEGATIVE_RETURN (2%), plus PRED_CALL, so 1.7% naturally; hot label and cb_hint make it 19.1%. bad is 9.87% with the
  expects, 14.66% without; most of it is the default case. A `static int crcSame()` helper instead of the expects
  (no NONEQUAL prediction while it's still a call, under no-early-inlining) gives 11.44%, not enough (gen_bd20).
  A flag `r = -3; ... if (r) return r` escapes the return prediction but gives 29%: too hot, size moves to a register and
  the literal goes first (gen_bd7). Magic stays at 8.5% there, and it needs >= 10% too.
- **nei_chk.** Without it the frame of loadBlFiles grows from 0x3c to 0x4c and registers change. Not looked at further.
- **pin_type.** type is loaded late (find_moveable_pseudos, probably) unless something uses it before the first call.
- **patchSmcConfig.** With everything off, the iniRangeOk log blocks for cpu and gpu tie at the same frequency, and
  cpu comes first; the reference has gpu first. Keeping only cb3 (with nei_smc) gives cpu 348, gpu 495 and fixes the log
  blocks, but the two success arms are then swapped (4 loose lines), and .rdata offsets shift. Natural arms can't break
  the tie, because each section starts from a join at 100% (gen_bd12: nested, reversed and early-exit forms, all 40).
- **noinline on extractSmcConfig.** Without it fnsplit accepts a split at the first scan loop ("Split before loop,
  accepting despite low frequencies"), and re-inlining makes size's SSA name low, so forwprop writes `size >= next`
  (cmp ebp,esi) where the reference has `next <= size` (cmp esi,ebp). (void)&size does nothing then. gen_bd11.
- **exp_verbose.** The "bytes" log needs freq >= 2000 for bb-reorder's second round. verbose != 0 gets no opcode
  prediction (compare with 0), so it's 50%, and the arm 28% of that: 1102. It needs P(verbose) >= 93%: `> 0` (64%) isn't enough.
- **exp_devgl.** Without the expect, tree-sink moves the setne into the non-dev path (it only leaves a statement in place
  if the target has >= 75% of the frequency, and non-dev is about 50%). No spelling of the test got there (gen_bd2, gen_bd2b: flags,
  ranges, ternaries, gotos all give 43). The goto predictor didn't help.
- **exp_t2.** The config and smc errors tie at 107 and later blocks win ties, so smc comes first. Moving smc's text
  earlier would break .rdata order. gen_bd14 (order of `r = -1`, shared fail block, break forms) all give 8.
- **lab_none.** With the precheck gone (plain `for`), the return is block 62 [20] and `r = 1` is block 22 [15], in the
  same round; it needs r = 1 first. Forms of the case 24 test don't change it (gen_bd16).
- **nei_blmod.** Early inlining of findFile swaps two spills (pt before cbb), 2 lines. Decl order, scopes, a separate
  `dst` for `cbb = cd`, polarity: none helps (gen_bd8, 8b, 8c).
- **exp_upd.** Only layout of the first test; the bit test and 23's compare are right. gen_bd1 and gen_bd4 stay at 18.
- **XB bound.** Address spelling (`xb.files + i`) in the loops and helpers didn't replace the bound (gen_bd17), and it
  isn't needed now.

### Don't retry

- exp_upd by `||` orders, a separate `if (type == 23)` (304 lines) or switch (346).
- exp_devgl by spelling of the dev test.
- exp_t24 by nesting or a local for imgSize (gen_bd3: 29 at best).
- exp_400+pin_src by spelling of the room test or src/dst locals (gen_bd13, 105 variants, 18 at best).
- exp_t9, exp_t10 by nesting, switch or order of the 9 and 10 tests (gen_bd18: l0 46, c0 85 loose).
- lab_t5le+exp_pr by polarity or merged conditions (gen_bd10, gen_bd10b; 13 and 7 at best).

### What to try next

- Other things like XB_FILES_BOUND: declarations that were kept per file or per hint but may not be needed. Check
  everything against all objects (`tools/wip/dehint/bdallobjs.sh`'s method; it still takes -DXB_FILES_BOUND as written: compile each src/*.c, cmp to build/obj).
- More hand inlining: what the attributes do early can often be written out. nei_smc delays iniRangeOk, nei_chk
  delays raiseKernel; a hand-written copy in one of the two fan sections would make the sections differ for real, and
  could break patchSmcConfig's tie (5 tricks).
- The 0x60 copies (4 tricks): find what could make e opaque to PTA in both functions, or a real reason for p's.
- checkBl: bad has to lose about 150 more after the crcSame shape, or the default arm's share has to fall (fewer
  switch edges to it, or a shared case). 9 tricks at stake.
- `--param` and the loadBl __builtin_constant_p entry stay last, as planned.
