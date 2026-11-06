# build de-tricking

Goal: `build/bd/reference.o` (copy of a matching build/obj/build.o) byte-identical from plain
`-O3`, with fewer hints.  52 tricks at the start of attempt 1.

## State after attempt 16

Attempt 16 landed nothing; src/build.c and build.sh are unchanged, so the count (16) and attempt 15's review table stand.  It checked every heuristic gcc 6 has against exp_devgl's dev test (none can be stacked: the 2% would need a call in the dev arm), took exp_t24's warning frequency apart factor by factor (the loop factor is fixed by the files[19] bound, and each test's missing predictor needs a call-free block or a call nobody would write), read pin_d's IRA pop order (the base's thread is popped before n and d), and found that exp_t10 only places CG's checkBl block (4 against 44).  Sweeps gen_bd270 (exp_t24 chain), gen_bd271 (pin_d address spellings), gen_bd272 (CG's own checkBl): none better than src.  See "## Attempt 16".

## State after attempt 15

**16 tricks** (17 before): `--param builtin-expect-probability=98`, 6 `__builtin_expect` (verbose, type == 10, `*pr != 0`, type != 24, isUpdateBl, devgl), 3 pins (e, d, size), the empty asm barrier, 2 hot and cold labels (t5le, none), 2 `__builtin_constant_p`, 1 dead test (`else if (type)`).  lab_badsize is gone: loadBl's case 23 tests `(e->size & ~3) != e->size`, which gets the opcode-nonequal heuristic that `e->size & 3` doesn't (gen_bd261; see "## Attempt 15").  New borderline shape, marked in src:

| Where | Shape | Why it's borderline |
|---|---|---|
| loadBl case 23 | `if ((e->size & ~3) != e->size)` | Live and not redundant, but loadConsoleBlFiles spells the same test `e->size & 3` (that one costs 6 lines in the other spelling), and this spelling is chosen for the predictor it gets |

The margins of exp_devgl (73% against 75.06%), exp_t24 (warning frequency 75 against 87) and exp_pr (`*pr`-true edge about 2%) are measured in "## Attempt 15"; no natural form reaches them.

## State after attempt 14

Attempt 14 landed nothing; src is unchanged, so the count (17) and the review tables below stand. It found that the `if (xb.type > BUILD_DEVGL16 && type == 14)` tail can't match: the reference's signature-failed path sends `xb.type <= 5` and `type != 14` to different places, and that form makes them one statement (see "## Attempt 14").

**Stuck** (judged after attempt 14; each has had its mechanism read from dumps and several attempts of natural forms):
- loadBl's tail, t5le and exp_pr: they set P(<=5) on vrp1's joiner copies (path counts in tree-ssa-threadupdate.c). Every form whose `<=5` exit goes straight to loadBl's return gets 0% on the SE copy (attempt 11), and the reference needs the `<=5` exit to be a statement of its own (attempt 14). vol_fail goes only with a near miss (drafts/build_loadBl_brktail_nearmiss.patch, 3 loose).
- The two `__builtin_constant_p`: their weight is tuned to the line (attempt 14's weight sweep: every other form is 26 loose and up).
- `else if (type)`, exp_t10, lab_badsize, pin_d: no natural form in 14 attempts; each comes down to one predictor or one IRA tie.
- exp_upd (isUpdateBl's own profile, attempt 8), exp_devgl (tree-sink's 75% rule), exp_verbose with pin_e (attempts 3, 5, 12, 13), pin_size (PRE names, attempt 7), exp_t24 (PRED_CALL on the block after `type == 25`), lab_none (two round-4 blocks, 5 attempts without movement).
- The `--param` stays while any expect does.

## State after attempt 13

Attempt 13 landed nothing; src is unchanged, so the count (17) and the review tables below stand. It read the Linux build's addUpdateBls, isUpdateBl, loadBlFiles tail, loadConsoleBlFiles, loadFileCrc, addBlsToImage and calcBlAreaSize for structure, and found nothing that the gcc 6 source doesn't already have (see "## Attempt 13" at the end).

## State after attempt 12

**17 tricks** (20 before): `--param builtin-expect-probability=98`, 6 `__builtin_expect` (verbose, type == 10, `*pr != 0`, type != 24, isUpdateBl, devgl), 3 pins (e, d, size), the empty asm barrier, 3 hot and cold labels (t5le, badsize, none), 2 `__builtin_constant_p`, 1 dead test (`else if (type)`). The two scan-bound expects and the next/buf pin are gone, and so is the findSmcConfig helper: the scan loops are written in extractSmcConfig as the Linux build has them (see "## Attempt 12"). The review tables below stand, except that findSmcConfig no longer exists. No new borderline shape.

## State after attempt 11

Attempt 11 landed nothing; src is unchanged, so the count (20) and the review tables below stand. It found why attempt 10's near miss has the SE copy's `ja` (the copies' `<=5` edge continues into loadBlFiles' shared `if (r)` join, which is drained to frequency 0) and that removing t5le alone needs the joiner's P(<=5) raised by a predictor (a call on the `>5` side does it; no natural one found). See "## Attempt 11" at the end.

## State after attempt 10

Attempt 10 landed nothing; src is unchanged, so the count (20) and the review tables below stand. It found which pass removes `fail:` without the asm (mergephi2, read from the 6.2.0 source) and a near miss that drops three of loadBl's tricks at once (vol_fail, lab_t5le, exp_pr: 3 loose, 11 strict lines, drafts/build_loadBl_brktail_nearmiss.patch). See "## Attempt 10" at the end.

## State after attempt 9

Attempt 9 landed nothing; src is unchanged, so the count (20) and the review tables below stand. It read loadBl's structure off the reference and the Linux build and measured three hint-free whole-function reconstructions: see "## Attempt 9" at the end. The best one is saved as drafts/build_loadBl_loop_reconstruction.patch (128 loose lines in loadBlFiles, no hints).

## State after attempt 8

Attempt 8 landed nothing; src is unchanged, so the count (20) and the review tables below stand. It did pin down why isUpdateBl needs its expect: see "## Attempt 8" at the end.

## State after attempt 7

**20 tricks:** `--param builtin-expect-probability=98`, 8 `__builtin_expect` (verbose, the two scan bounds, type == 10, `*pr != 0`, type != 24, isUpdateBl, devgl), 4 pins (e, next/buf, d, size), the empty asm barrier, 3 hot and cold labels (t5le, badsize, none), 2 `__builtin_constant_p`, 1 dead test (`else if (type)`). `no-early-inlining` is gone: see "## Attempt 7". The review table below stands, plus:

| Where | Shape | Why it's worth a look |
|---|---|---|
| `align16`, all 7 `(x + 15) & ~15` in build.c | A small static helper | Not redundant and reads naturally, so it isn't marked borderline. But it steers: patchBlsBlmod needs it at 3 or 4 of its sites to match. The other sites are free either way; they use it so the helper is the file's, not the function's |

## State after attempt 6

Attempt 6 landed nothing, so the count and the review table below stand. It did explain the type-11 copy, the constant_p entry and `else if (type)`: see "## Attempt 6" at the end.

## State after attempt 5

21 tricks, counting loadBl's dead `else if (type)` (attempt 5's report said 20, without it; README's rules count dead tests): `--param builtin-expect-probability=98`, 8 `__builtin_expect` (verbose, the two scan bounds, type == 10, `*pr != 0`, type != 24, isUpdateBl, the devgl test), 4 pins (e in loadFileCrc, next/buf in findSmcConfig, d in case 27, size in calcBlAreaSize), the empty
`__asm__ __volatile__("")` barrier at loadBl's `fail:`, 3 hot and cold labels (t5le, badsize, none), 2 `__builtin_constant_p`, 1 `no-early-inlining` (patchBlsBlmod). (After attempt 4: 25. After attempt 3: 26, with 10 expects. After attempt 2: 43, with 18 expects, 7 pins,
6 labels, 5 cb_hint and 3 no-early-inlining. After attempt 1: 50.)

Landed shapes to review:

| Where | Shape | Why it's borderline |
|---|---|---|
| patchCpuFan and its caller | The cpu fan section as a function, with `xb.cpuFan != 0xffffffff` tested in both | The repeat is redundant, folded after inlining, and only there for what it does to frequencies. It replaces no-early-inlining on patchSmcConfig and 4 cb_hint. The function alone is natural |
| loadBl case 24 (both arms), loadConsoleBlFiles case 24 | `if (loadBaseFile(..)) r = defaultBl60(e); else if (e->size != 0x60) r = defaultBl60(e);` | Two identical calls where `\|\|` would do; crossjump merging them is what orders the size store. All three now have the same form (attempt 4). The first arm can't use `\|\|` (243 lines), console's costs 2 lines |
| loadBl, signature passed | `else if (type)`, a test that can't be false there | Not new and not counted so far; plain `else` costs 54 loose lines. It's a dead test that steers threading, so it may deserve counting |

crcSame, blMagic and `goto toobig` are gone (attempt 5): checkBl has no borderline shape left.

Not borderline, but they steer, so check them: the struct copy in extractSmcConfig, `findSmcConfig` (gone in attempt 12), `int size` on extractSmcConfig and `int crc` on loadInputFile (comments in
the source say so). Both are compared as unsigned through the usual conversions, so behaviour is the same. `*pr = 0` in loadBl's
second case-24 arm is what `*pr = loadBl60(e)` did on success, so it's live and unchanged.

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

## Attempt 2

### Addons spelled through xb.addons (landed, no change to the trick count)

Every use past the end of `files` now says `xb.addons[n].name` (`&xb.addons[i]` in build.c): build, mode_build,
mode_update, options. No loop crosses from files into addons, so all of them converted, and each object is byte-identical;
full build SHA256 matches. xebuild.h's borderline sentence is gone. `bdaddons.py` was the sweep (its old strings are gone
from src now, so it only documents what ran). `(xb.addons + n)->name` costs 15 lines in parseAddonIdx at the
`xb.numPatches` site in mode_update, and `xb.addons + i` costs 2 lines in appendAddonPatches: use the index form.

### What landed (50 -> 43, all IDENTICAL, full build SHA256 matches)

1. **The two 0x60 copies, 4 tricks (gen_bd21 to gen_bd26).** Attempt 1 assumed points-to analysis; it isn't that. Reading sched2's dump
   (`-fdump-rtl-sched2-all`), the payload and core copies have `[0 S3392 A32]` on the rep_mov's memory, no MEM_EXPR, while the 0x60
   copy has `MEM[(char *)_190]`. flow_find_cross_jump calls merge_memattrs on every insn pair it matches, even if it then doesn't
   crossjump; with different SSA names the MEM_EXPR goes, and without one sched2 assumes a dependence on the size store. So the
   copy needs a partner with the same successor. loadBl's second arm already has one (the payload and core copies join at the same
   block), so only the first arm and the console copy lacked it. The fix is two copies: `if (load) copy; else if (size) copy;`.
   New helper `defaultBl60` holds the copy; the load tests are written where they're used. loadBl's first arm uses the two-call form
   and the second arm keeps `||` plus `*pr = 0`. Using the two-call form in both arms costs 250 lines, and without `*pr = 0` it's 100.
2. **`int size` on extractSmcConfig (noinline and `(void)&size`, gen_bd38).** The conversion in the bound tests gives forwprop a later SSA name,
   so `next <= size` falls out in both loops, split or not. `long` and `ssize_t` match too.
3. **`int crc` on loadInputFile (noclone, gen_bd42).** IDENTICAL with no attribute: with a uint32_t, ipa-cp clones for crc == 0
   (attempt 1's 21550 lines). `uint8_t *meta` -> `void *` doesn't help.
4. **exp_t2 came off free** after 1: the config and smc errors still tie at 107, and the order now comes out right. `greedy` is worth
   rerunning after every landing. lab_badsize also fell from 61 to 26.

### Costs now

Strict lines, removed alone: nei_blmod 2, lab_t5le 7, pin_type 11, cb1 12, pin_src 18, exp_pr 18, exp_upd 18, pin_i 22, pin_d 23, exp_400 25,
pin_e 26, lab_badsize 26, exp_t24 29, exp_210 43, lab_nf1 and lab_nf2 43 each, exp_devgl 43, nei_smc, cb2 and cb3 52 each, pin_size 82,
exp_verbose 83, lab_size 84, exp_200 97, exp_t10 116. Groups: lab_t5le+exp_pr 13, lab_badsize+lab_t5le+exp_pr 39, lab_none with its precheck 8.

### Near misses (not landed)

- **patchSmcConfig, 5 tricks, 8 loose (36 strict) lines:** drafts/build_patchSmcConfig_nearmiss.patch, gen_bd35. iniRangeOk written out in the
  cpu section lowers its log block to 298, under gpu's 348, which fixes the log order. But its success arm rises from 732 to 1029
  (it loses the helper's return prediction) and moves ahead of the temperature logs; it has to be at most gpu's 732. Writing out gpu
  instead (gen_bd33, gen_bd34) goes the wrong way. Seven spellings of the range test and flag (gen_bd36) all stay at 1029.
- **checkBl, 9 tricks:** drafts/build_checkBl_nearmiss.patch, gen_bd31 hg+all. Each arm but type 14 with its own crc log and `return -2` takes `bad`
  to 884, under its limit of 1000. A helper returning -3 (`return blTooBig(blsize, size)`, the local predictor can't see the constant)
  lifts the size error from 167 to 2071. It has to be in [1000, 2000): at 2071 it lands in bb-reorder's round 2 (threshold 20% of
  entry) and its block comes straight after the jump table. So 71 of frequency stands between this and the crc expects, cb5 and lab_size
  going. Seven copies of the log and an extra helper are a lot of shape, so this would land as borderline at best.
  `return -2` per arm with no `goto bad` at all loses c's PHI (default's c = 0 is then a constant): keep at least one goto.

### Mechanisms

- Crossjump's merge_memattrs drops MEM_EXPRs even when no crossjump happens, so a `S<big>` size with no expr in a sched2 dump marks a merge.
- bb-reorder's exec thresholds are 50%, 20%, 5% of the entry frequency: being a little over or under 2000 of 10000 decides the round.
- lab_none: r = 1 is 14 and the shrink-wrapped return 20, in the same round, and r = 1 has to come first. Six forms of case 24's
  failure (gen_bd27) don't move either value.

### Don't retry

- 0x60 copies: anything about points-to; it's the MEM_EXPR.
- pin_d by spelling the case 27 call (gen_bd40: locals, a fileent pointer, n; 23 at best).
- pin_src and pin_i by spelling the copy or its test (gen_bd41: 18 at best); i, j, found and buf types (gen_bd39).
- Types, all with no gain (gen_bd42, gen_bd43, gen_bd44): checkBl's params, m and blsize; calcBlAreaSize's locals and return; patched and iniRangeOk's
  params; loadBl's i, pr, type; loadConsoleBlFiles' r and type; loadFileCrc's crc, pad, verbose, size; patchBlsBlmod's cd, cbb, pt and size.
- isUpdateBl by switch, flag or ternary (gen_bd42 BDW=upd: 18 at best).

### What to try next

- Types and declarations were the best lever again (2 tricks and an uncounted statement from 2 words), but this attempt's sweep only changed one function
  at a time, with that function's hints all off. Worth trying with one hint off at a time, as a type can look worse with others in.
- checkBl: 71 of frequency on the size error (see near misses).
- patchSmcConfig: a written-out cpu section whose success arm stays at most 732.
- Look for other copies crossjump could explain: identical-looking blocks whose order or registers needed a hint.
- `--param` and the loadBl __builtin_constant_p entry stay last, as planned.

Tools added: `bdopt.py file.c fn regex..` (frequencies of matching blocks), `bdbbro.sh file.c fn` (bb-reorder's traces, rounds), `bdaddons.py`.
gen_bd22 to gen_bd26, gen_bd32 and gen_bd36-style chains take BASE from build/bd/gen_bdN_best.c, so they only rerun in order, and src has since moved on.

## Attempt 3

Re-measure first: no single removal or pair was free (nei_blmod 2, lab_t5le 7, pin_type 11, ...). The per-hint type sweep (gen_bd50, 1056 cases) found nothing either.
What moved everything is one idea: **a static function holding calls isn't early inlined, so at profile_estimate it's a call, and it comes back at ipa-inline.**

### What landed (43 -> 26, full build SHA256 matches at each step)

1. **cb5 (gen_bd61).** cb_hint worked as a call with side effects still there at profile_estimate (PRED_CALL on its edge, under no-early-inlining).
   A helper doing the arm's real work is the same call. A getter does nothing, as it's pure: gimple_has_side_effects is false. `blMagic(bl, &m)`, with an out parameter, works.
2. **7 crc expects (gen_bd62 to gen_bd67).** `crcSame(c, crc)` has no NONEQUAL prediction while it's a call. The failure log written in each arm (`return -2`) gets PRED_CALL and
   the negative return. Crossjump adds the arms' frequencies to `bad`, and it must stay under 1000: 878 + 101 = 979. Type 14 keeps `goto bad`, through crcSame (with `crc != c`: 1003).
3. **nei_smc and cb1 to cb4 (gen_bd60, gen_bd72 to gen_bd74).** The cpu fan section as `patchCpuFan`, with calls inside so it isn't early inlined. Its own -1 test is folded after
   ipa-inline under the caller's same test, and nothing rescales the blocks behind it, so its success arm falls from 693 to 355 and its logs to 216. A one-section helper really
   differs from the gpu section, which breaks attempt 2's tie. Plain stores: no setFan needed once nei_smc is gone.
4. **lab_nf1, lab_nf2 (gen_bd79).** The two scan loops as `findSmcConfig`, with the result through `uint32_t *pos`. Natural, and not borderline. Both labels were free after that.
   The form that returns from inside the loops doesn't match (120 lines); keep `found` and `*pos = i` at the end.
5. **exp_400, pin_src (gen_bd81, gen_bd82).** `*(struct smcConfigData *)e->data = *(const struct smcConfigData *)(buf + i);` in place of memcpy. Same bytes, no helper needed, no expect, no pin.
   Worth trying on any other pin next to a block copy.

### Costs now (strict, removed alone)

nei_blmod 2, lab_t5le 7, pin_type 11, exp_pr 18, exp_upd 18, pin_i 22, pin_d 23, pin_e 26, lab_badsize 26, exp_t24 29 (7 loose), exp_210 43 (11 loose), exp_devgl 43 (7 loose), pin_size 82, exp_verbose 83,
lab_size 84, exp_200 97, exp_t10 116, exp_t9 217, pin_m 242, vol_fail 296, lab_none 415, nei_chk 501, exp_27 510. `bdsubset.py` scores every subset per function; bdtricks' cb*, crc*, lab_nf*, exp_400, pin_src names no longer apply.

### Mechanisms

- **Early inliner:** a callee stays a call if growth > 14 or growth * (calls in it + 1) > 14, so a helper with two or three calls isn't early inlined, while a setter with none always is.
  Under no-early-inlining every helper is a call, but PRED_CALL needs side effects (gimple_has_side_effects): a pure helper only escapes the test's own opcode prediction.
- **A test folded after profile_estimate doesn't give its frequency back.** Blocks behind a repeated test stay scaled by its prediction (0.72 for != const). Only a late inline does this: FRE removes a repeat in one function before prediction.
- **bb-reorder's key** for a block after a trace's end is -(1000000 + 100 * edge frequency + block frequency), so the edge's frequency decides, not the block's. Temperature logs have edge 679, gpu's success arm 571; the cpu arm has to be below.
- **Crossjump sums frequencies before bb-reorder,** so per-arm copies count together against the epilogue copy's limit of 1000. A log helper called 7 times isn't inlined in cold arms: write the log in the arm.
- **nei_chk is two separate things.** In callers it only stops checkBl(.., 6, ..) from being inlined for its constant: writing `type` for the 6 in loadBl's case 6 removes all of the loadBlFiles cost (391 -> offsets only; VRP puts the 6 back). The rest is checkBl's frequencies: with early inlining crcSame and blMagic do nothing.
- **patchBlsBlmod's 2 lines:** spill stores follow partition order. pt's partition holds i_20, a low SSA name surviving from the third findFile's copy, where the reference has i_130, so pt sorts before cd (_68). Nothing here moved it.

### Near misses (not landed)

- **nei_chk, pin_type, lab_size (gen_bd75, gen_bd76, 34 loose lines; run gen_bd76 with build/bd/a3/base76.c, src plus `type` for the 6 in loadBl's case 6):** size test in checkBl, the rest in `blCheckType`, no attribute, no hot label, no type pin. It needs size in [1000, 2000) (400 now),
  bad under 1000 (1371 now), magic under 2000 (2101 now). With the hot label: size 19%, magic 1767, bad 1153, 36 loose. crcSame can't help without the attribute. An attribute on the inner function stops it being inlined at all (10891).

### Don't retry

- break -> return in loadBl, each one with each hint off (gen_bd53, 299 cases: no change at all).
- patchBlsBlmod: 1159 neutral shapes in triples (gen_bd54); forms of findFile (gen_bd55); findFile written out (gen_bd56); tail or walk as helpers (gen_bd77, gen_bd78).
- exp_verbose by forms of the verbose or equal test, gotos (gen_bd51). The goto predictor moves the bytes log from 1102 to 1609; it needs 2000.
- exp_upd by no `continue`, gotos, or nesting (gen_bd52, all 18). The rotation exit is whichever edge into the body is hottest: type == 23's 1816 against the bit test's 831; the first test always stays out of the bit test.
- Scan loop forms with an explicit next, while, for(;;), continue, in place (gen_bd59) or in findSmcConfig (gen_bd83); one helper per loop (gen_bd84: 122).
- patchSmcConfig: polarity (gen_bd71), goto around a section (gen_bd57: PRED_GOTO didn't change frequencies). Done anyway.
- pin_m by m's type, its use in the log, or the test's form (gen_bd69). `m &= 0x43` gets 13 lines but changes what the log prints.
- Separately written switch cases to thin default's share (gen_bd65: they don't merge to the same layout).
- exp_t24 by a helper for the room test or nesting (gen_bd85: 7 loose, same as without). exp_t9, exp_t10 by a shared update-fallback helper (gen_bd86: 248 and up).
- vol_fail by `if (pr)` (gen_bd87: 99 loose, 278 strict, against 75 and 296).

### What to try next

- The same helper lever on what's left: any hint about one section's frequencies (lab_badsize, exp_t10, exp_27's case 27, lab_none's case bodies, exp_devgl) as a static function with calls in it, tried alone and with a repeated test. Sweep helper boundaries, not spellings.
- Struct copies wherever a pin sits by a copy.
- nei_chk from the near miss above: size up, or the switch and bad down.
- `--param` and the constant_p entry stay last. 10 expects are left.

Tools added: `bdone.py` (one hint off, one edit; BDSLACK shows edits that don't beat it), `bdsubset.py`, `bddump.sh file.c fn pass,..` (t-* tree passes), gen_bd50 to gen_bd87. Heredocs do mangle `\\n` in generators: gen_bd68 was lost to it once; use the Write tool.

## Attempt 4

Tools: `bdrun.py gen.py [-f fn] [-n N] [-k label]` scores whole-source variants, strict and loose together (generators define `CASES(base)`, optional `PRE`, `BASE`); `bdfreq.py gen.py fn re1,re2 [-f fn]` adds the block frequencies
of matching lines to each row. gen_bd90 to gen_bd118. Beware: a difference in only `loadBlFiles:52 loadConsoleBlFiles:18 blmodMissing:2 buildFlash:16` is nothing but call displacements after checkBl's size moved, not a real difference.

### What moved the numbers

- **exp_27 was a dead test, not a frequency.** `__builtin_expect(type == 27, 1) &&` in case 27 cost 510 lines when only the expect went, because the `type == 27` test then got an opcode prediction. Taking the test out too is byte-identical (gen_bd94).
  **Whenever an expect sits on a test that's always true, remove the test, not just the expect.**
- **checkBl: test the type's range before the switch (gen_bd114, gen_bd115).** `if ((uint32_t)(type - 5) > 16) { c = 0; goto bad; }` and no `default:`. VRP removes the switch's own bound test, so it's the same one test in the object. A switch's edges are predicted evenly, so `default` was getting
  S/9 of the frequency, which is most of `bad`. With the range test, bad is 880 with plain `if (c != crc) goto bad` arms and no crcSame, and it needs under 1000.  `type < 5 || type > 21` is a different compare (616 lines).

- **loadBl case 24's second arm uses the two-call form too (gen_bd121),** byte-identical now (250 lines in attempt 2), so the arms no longer differ. A shape cleanup; the count doesn't change.
- Not landed, checkBl's range test: it isn't byte-identical yet (below), so src keeps crcSame and the seven logs.

### Near misses

Patches against this attempt's src: drafts/build_checkBl_nohints_nearmiss.patch, drafts/build_checkBl_rangetest_nearmiss.patch, drafts/build_loadBl_nobarrier_nearmiss.patch.

- **checkBl, no attribute, no helper, no hot label, no type pin, no crcSame, no blMagic (gen_bd115, `goto goto hot0 pin1`): 8 loose, 25 strict.** Only the m pin is left in it, and all that's wrong is the size error at 167: it needs an edge >= 1000 (epilogue copy) and < 2000 (round 2),
  and magic (2123) falls under 2000 as soon as it does. With the hot label: size 880, 6 loose. So the whole of checkBl comes down to P(size error) in [10%, 20%). The type pin goes free once no-early-inlining is off (gen_bd99).
- **checkBl with the range test and everything else kept, crcSame and the seven logs gone (gen_bd118, nei1 hot1 bm1 pt1 pm1): 0 loose, 7 strict, padding only.** The `xor eax,eax; jmp` block for c = 0 gets a `.p2align` because its frequency is 122 and compute_alignments' threshold is 1% of the maximum, 100.
  (`default:` in the switch isn't aligned: the bound test's edge from expand has a low frequency.) The test is 1.67% (call 29%, negative return 4%) of 7307. It needs under 100: forms of the range test and the m test change nothing (gen_bd119), and `type < 5 || type > 21` doesn't reduce to the same code. If this falls, it's worth landing even with no change to the count: it trades crcSame and seven copies of a log for one test.
  - `return -3` gets the negative return, 1.67%. With no constant reaching the return (`r = 0; if (blsize > size) { log; r = -3; } if (r) return r;`, gen_bd98): PRED_CALL alone, 29%, 2900. Adding the early return gives 20.71%, 2071, just as attempt 2 found (gen_bd117 `t3 crc=done mag=done ok=done`, but magic is 6414 there).
    A third predictor below 50% would do it. PRED_GOTO adds nothing here. `r`-style forms also put the size log's text before crc's unless the log stays after the switch.
  - A helper that isn't early inlined puts a call on the normal edge: 19.1% with the hot label (gen_bd101, m needs no pin there). But a helper holding the crc arms can't match: the reference's first arm has `cmp eax,[crc]` and the others `cmp [crc],eax`, which only happens when `c`'s SSA version is below `crc`'s,
    that is when the arms are in checkBl itself at into-SSA (crc is first used there). After inlining crc is the caller's low version and every arm canonicalizes to `crc != c`. So a split can't reach 0: gen_bd100, 101, 102, 114 split1.
- **loadBl, vol_fail (gen_bd107, `brk goto brk`): 1 loose, 7 strict.** case 23's log `*pr = -1; break;`, the signature tail `*pr = -1; break;`, case 2 `goto fail` with `fail: *pr = -1` after the return. Left: the reference's log jumps to case 2's `mov edi,-1` block, and the draft has its own `mov edi,-1`.
  `*pr` is a register by then, so `fail` is empty in GIMPLE, the -1 is a PHI argument on each edge, out-of-SSA appends it to the log block (one successor), and crossjump won't fold that into a split-edge block with a higher index. Something must keep `fail` non-empty until expand; that's what the asm does.
  case 23 moved after case 2 (gen_bd109) changes string order and doesn't fold it either. A clobber (scoped address-taken local) would do but there's no natural one here.
- **loadFileCrc, pin_e (gen_bd106, gen_bd111):** `e->size = pad && (size & 15) ? (size + 15) & ~15 : size;` fixes the registers (e esi, f ebx) with no pin, 2 loose, but it sinks the first store, and in loadCommonFile it swaps e the other way (28). Forms with both stores keep the swap (26).
  The ternary has one reference to e fewer, so it's IRA's priority order. A real use of e in the pad log goes the wrong way (gen_bd112).
- **lab_none: 4 loose, 8 strict with the plain `for`.** Order of two round-4 blocks: return [20] and r = 1 [14], r = 1 has to be first. Forms of case 24 (gen_bd104) and of defaultBl60 (gen_bd103) don't move either.
- **lab_t5le: 0 loose, 7 strict, alignment only.** With exp_pr too, 2 loose (`ja` for `jbe`); forms in gen_bd95.
- **lab_badsize: 6 loose.** Order of the appendAddonPatches block. Forms in gen_bd95; a shared loadPatchFile (gen_bd94) is much worse.

### Mechanisms

- **Predictors seen on checkBl's size test:** call 29%, early return 39%, together 20.7% by Dempster-Shafer; negative return gives 1.67% with the call. `-fdump-tree-profile_estimate` lists them per block (`bddump.sh file.c checkBl t-profile_estimate`).
- **A switch's outgoing edges are even.** combine_predictions_for_bb only predicts two-way branches, so adding or removing a distinct arm changes every arm's frequency. Separate identical cases thin default's share but don't merge back (gen_bd102 split1, split2).
- **calcBlAreaSize:** the `mov ebx,esi` before the 14 lookup is IRA's region split at the inlined findFile loop, and ebx holds the PRE'd `files[x].size` values. It's not a source variable.
- **loadXell as a shared helper is byte-identical** (gen_bd94 x25 in either or both functions), for whoever wants the two copies of case 25 merged. It doesn't remove a trick.

### Don't retry

- pin_size by temporaries for the file sizes, statement forms, a blFileSize helper, order or nesting of the build-type chain, declaration order (gen_bd105: 1280 cases; gen_bd110: all L40 or worse).
- pin_d by forms of the extract call, a fileent pointer, nesting the load fallbacks, or a helper (gen_bd113: 14 at best; helper 124).
- exp_t24 by the room test as its own `if` (gen_bd96: 7 at best, separate ifs 27), or a warning helper shared with addUpdateBls (gen_bd97: early inlined, 7, and it costs 6 in addUpdateBls). The expect keeps imgSize()'s call out of the block right after `type == 25`, so PRED_CALL misses that edge: the log is 153 with it, 75 without, and has to beat the block at 117.
- exp_devgl again: the `setne` has to stay above the test, and tree-sink needs the non-dev path at 75%; two `==` tests give 52%.
- checkBl by bad falling out of the switch to one log (gen_bd90): operand order and polarity of the crc test make no difference; same code.
- Separate identical switch cases; goto in the helper for magic failures (gen_bd102: no change at all).
- patchCpuFan's repeated test: it does pay. Without it, 52 lines in patchSmcConfig (40 loose); with the test only in the function, 91 (8 loose). gen_bd120's "IDENTICAL" for the caller-only form was an edit whose text didn't match; bdrun now labels those `(NO CHANGE)`. Check that label before believing an IDENTICAL.
- blMagic returning the value or gone (70 lines in checkBl), crcSame gone from type 14 only (64): both still pay while no-early-inlining stays (gen_bd121).
- A shared loadPatchFile for case 23 (gen_bd94): 219 lines in loadBlFiles, 118 in loadConsoleBlFiles.

### Costs now (strict, removed alone)

nei_blmod 2, lab_t5le 7, pin_type 11, exp_pr 18, exp_upd 18, pin_i 22, pin_d 23, pin_e 26, lab_badsize 26, exp_t24 29, exp_210 43, exp_devgl 43, pin_size 82, exp_verbose 83, lab_size 84, exp_200 97, exp_t10 116, exp_t9 217, pin_m 242, vol_fail 296, lab_none 415, nei_chk 501.
`--param`: 96 gives 46 lines (loadConsoleBlFiles, exp_t9), 97 gives 35 (loadBlFiles), 91 to 95 over 320 (extractSmcConfig, loadBlFiles), 90 adds loadFileCrc. So it's held by exp_t9, the loadBl expects, the two scan expects and exp_verbose.

### What to try next

- checkBl, P(size error) in [10%, 20%): any third predictor on `blsize > size`, or a form with call and early return (20.71%) whose magic stays low. That takes nei_chk, pin_type, lab_size, crcSame and blMagic together, and pin_m may follow (it isn't needed in the split forms).
- The default block under frequency 100 in the range-test form (see near misses).
- More always-true tests like case 27's: look at any expect whose test can't be false, or that a switch has already decided. exp_t24's `type != 24` is the one left, and it's there for its block, not its value.
- A statement that keeps loadBl's `fail` block non-empty until expand, with no code, in place of the asm (near miss above).
- `--param` and the constant_p entry stay last.

## Attempt 5

### What moved the numbers: an error variable (25 -> 20, full build SHA256 matches)

1. **checkBl, 4 tricks plus crcSame, blMagic and `goto toobig` (gen_bd130).** Very likely the author's own shape: `uint32_t blsize, c = 0; int m, r = 0;`, the arms only set `r`, and one block at the end logs by `r`, then `return r;`:
   `if (r) { if (r == -2) crc log; else if (r == -3) size log; else magic log; }`. Byte-identical with plain -O3 and no attribute, label, pin or helper, and the literal 6 stays in loadBl. 16 of 96 variants match, and only the outer `if (r)` matters
   (flat `if/else if` chain 15 lines, sequential ifs or a switch up to 167). `break` or `else` arms, `goto done` or nesting, `c = 0` in the declaration or the default are all equivalent. Behaviour: default still logs the crc message with c = 0, and m is bl[0], which nothing writes.
   Attempts 1 to 4's predictor arithmetic (P(size error) in [10%, 20%)) was beside the point: the logs aren't guarded by the size test when branches are estimated, so their frequencies come from jump threading the tests at the end. The crc, size, magic text order is just that chain's order.
2. **exp_t9 (gen_bd135).** loadConsoleBlFiles' update fallback: `if (r) { if (type == 9) {..} else if (type == 10) {..} } if (!r) r = checkBl(..);` in place of `if (r) break;`. Byte-identical with no expect.
3. **The r6 local (gen_bd150).** Case 6 is plain `if (!*pr) *pr = checkBl(.., 6, ..);`. No change to the count.

**The lesson for what's left: where a hint is about error-path frequencies, try setting a variable and testing it later, before any predictor work.**

### Near miss: loadBl with almost no hints

drafts/build_loadBl_errvar_nearmiss.patch (gen_bd137 to gen_bd146 take their BASE from build/bd/a5/lb*.c, each made by the one before with `-k`, so they only rerun in order). No constant_p, no expect on 10 or `*pr`, no t5le or badsize label: **32 loose lines in loadBlFiles** (83 strict), where taking only vol_fail off src costs 256. It keeps the d pin and the shared `fail` with its barrier (14 and 75 more loose without them). Landing it would remove 6 tricks. Its shape:
`*pr = checkBl(..); if (!*pr) { sig test; if (xb.type <= 5) break; if (type == 14) flash; }`, `goto chk` kept for CG (it's what makes CG's checkBl share CF's), signature as `if (!xb.pub1bl) .. else if (!verify) .. else if (type) ..` (the text order 0xcb8, 0xcf4, 0xd2c reads straight off this).
What's left in it:
- The type-11 test's copy: the reference has its own `pub1bl` test and no-key log for type 11, jumping straight to the loop's next iteration. The draft goes to the shared one. This is what the constant_p entry does. With t10, bad, cp and the `*pr` expect back on, it's all that differs with this signature form (`notel,nest,t10,bad,cp,pr`: 10 loose, 20 strict), but that keeps nearly all the tricks.
- appendAddonPatches' position (4 lines, the badsize label fixes it), the sig-failed flash copy's `imul` (the reference leaves `xb.files[i]` alone there, probably because that block has frequency 0), `jbe` for `ja` on the SE copy, a `mov edi,-1; jmp`.
- The loop form (r a real variable from the start, gen_bd133, gen_bd143) is further off: 90 at best with the pin on. The static function with `*pr` looks right: `*pr` stays memory until inlining, so its tests survive to be threaded late.
- Grid gen_bd146 (signature form, hint subsets, tail forms, 512 cases): only src's own hint set is identical, so nothing lands piecemeal from this base.

### Don't retry

- checkBl's range test and all P(size error) work: solved another way. The three checkBl near-miss patches are deleted.
- lab_none by console loop forms: an error variable for the -1, `for` conditions on r, int i, a pointer walk, `continue` (gen_bd136): 4 loose at best. r = 1 [14] against the return [20] don't move.
- exp_verbose: loadFileCrc's exits as an error variable. All 16 combinations are byte-identical to the plain form (gen_bd131: 18 loose, 83 strict), so r has no effect there. Logs per pad arm (gen_bd132: 68 and up), `&&` forms (gen_bd149: 18 at best).
- exp_t24: flags for the skip tests (gen_bd147: 380 and up), a redundant test on xb.type (gen_bd148: `xb.type <= 5` folds too early, 7; `!= RETAIL` 124). Plain, nested and `type != 24` are all 7.
- Case 6 falling into the shared case, or `type == 6 && !xb.cbb` in it (gen_bd145: 127 and up). It looked like the natural non-constant entry, but no.
- `xb.files[n].data` in place of the d local, without the pin: 14 loose (gen_bd150).

### Mechanisms

- tree_estimate_probability_bb's PRED_CALL only looks at a guarded block's own statements, and PRED_NEGATIVE_RETURN needs the constant to be a direct argument of the return block's PHI. A test that only sets a variable gets neither.
- predict.def at this tag: call 71, early return 61, const return 67, negative return 96, continue 50, goto 70. The C front end emits no goto predictor here: no GIMPLE_PREDICT in checkBl's cfg dump, and no goto heuristic in profile_estimate's. Earlier notes that credit it, for example the bytes log's 1609, should be read with that in mind.
- A loop's exit probability is shared out by exit count (predict_loops), so the scan loops' bound test, coming first, has the hotter exit and rotate_loop picks it. That's why exp_200 and exp_210 hold. I found no natural form.
- predict.c and predict.def were read from the official repo at releases/gcc-6.2.0, into build/bd/a5.

### Costs now (strict, removed alone)

nei_blmod 2, lab_t5le 7, exp_pr 18, exp_upd 18, pin_i 22, pin_d 23, pin_e 26, lab_badsize 26, exp_t24 29, exp_210 43, exp_devgl 43, pin_size 82, exp_verbose 83, exp_200 97, exp_t10 116, vol_fail 296, lab_none 333.

### What to try next

- loadBl's near miss: 6 tricks. It needs the type-11 copy to survive with no constant_p. Read vrp1 and dom2 on the patch, and look for what else could give the shared path a non-constant entry.
- The same lens on other objects: any counted hint about an error path in a function with several `return`s. image_read's last trick is worth a look.
- pin_size, exp_devgl and exp_upd haven't had the "what would he have written" look: each is one test in a function whose shape is otherwise guessed. checkBl's answer came from asking that, not from sweeping spellings.
- `--param` and the constant_p entry stay last. The param is now held by the loadBl expects, the scan bounds and exp_verbose.

## Attempt 6

No match; src is unchanged. All of this is on loadBl. Generators gen_bd160 to gen_bd168 build from src/build.c at 4bf4bde (attempt 5's source), so they only rerun against that text.

New tools: `bdpasses.py file.c fn regex [dir]` (count a pattern after each tree pass, which finds the pass that makes a copy), `bdtrack.py dir fn regex` (frequencies of those blocks per pass), `bdlabel.py gen.py "label" out.c` (write and score one case without running the whole generator; `bdrun -k` runs them all first). tree-ssa-threadbackward.c was read from the official repo at releases/gcc-6.2.0.

### What the type-11 copy really is

Attempt 5's note blamed block frequency. That was wrong for the copy itself: three separate things are tangled here.

1. **The copy is one FSM jump thread in dom3, and PHI argument order decides it.** The thread is `(24,25) (25,29) (29,137) (137,32) (32,124)`: from the constant 11 in the pub1bl block's PHI, through the no-key log and `xb.type`, to `type == 14`. fsm_find_control_statement_thread_paths walks the tail's `type` PHI in edge order and returns at once for a block it has already visited. So only the first argument naming the pub1bl block's PHI gets a try.
   - No-key edge first (`PHI <type_469(29), type_469(28), ..>`): the short path fits, 5 insns, and the copy appears.
   - Passed edge first (the near-miss signature form, `PHI <type_453(30), type_20(24), type_453(26), ..>`): that path goes through the verify call and is too long ("FSM did not thread around loop and would copy too many statements"), and the no-key edge is never tried.
   - Check it with `grep "FSM did not" *.dom3`, or look for the `(24, 25) .. (25, 29)` registration.
   - The earlier forms that lost the copy (`if (!xb.pub1bl) nokey; else if ...`) lost it this way, not through constant_p. With `if (xb.pub1bl) {..} else nokey` the copy is there with no constant_p at all.
2. **`else if (type)` sets a probability, and the dead test is what does it.** PRED_CALL only applies when the edge's destination holds a call. With a plain `else`, both arms hold log_printf calls, so the two predictions cancel: verify is 50/50 and the failed arm falls through (54 loose). The dead test leaves no call in the passed arm's first block, so only the failed arm is predicted against: 29/71, as the reference has it. The escape needs a conditional block in front of the log, or a passed log with a second predecessor.
   - Testing `*pr` later gets the 29/71 (`if (!v) {failed; *pr = -1;} if (!*pr) passed;`, gen_bd162 s1, s5). But threading then puts the passed log in a copy of the join, placed late, so its literal moves in .rdata and every later offset shifts (82 to 100 loose).
   - `else if (!*pr)` would behave like `type` but is just as dead, so it was not tried.
3. **constant_p now only places the type-11 block (26 loose: `dead src t1 bad0 cp0` in gen_bd161, drafts/build_loadBl_fsm_nearmiss.patch).** Removing it, the two constant_p and the t5le label (3 tricks), leaves that one block in the wrong place and nothing else. The test's block frequency is 0 after dom2's joiner threads. Its edge is 36 (`.305 * (N - C)`, with N the non-constant entry and C the constant 9, 10 and 14 entries), so 23's other edge is 43, under what I take to be round 3's exec threshold of 44 (5% of the entry's 882; worked out from the numbers, not read from a dump, while src's 46.5 passes). The trace stops at 23, block 24 gets priority -1003600 and is laid out too early. To land it needs:
   - 23->27 at 44 or more;
   - freq(24) from about 22 to 29, since it must sort after 29 [29] and tie with or beat 18 [22] (src has 22, of which constant_p's entry is the source).
   So the original probably had a real non-constant way into the shared checkBl that lasted until dom2 and then folded. I couldn't find one that's natural.

### Sweeps and results

- gen_bd160, gen_bd161: signature forms x tails x hints. The `dead` form is well ahead of everything else. `dead failx t1 bad0 cp1` (only the t5le label off) is 0 loose, 7 strict: padding before the no-key log. `dead fail t1 bad0 cp1` (t5le and the `*pr` expect off) is 2 loose, 13 strict: `ja` for `jbe` on the SE copy. `dead src t1 bad1 cp1` (badsize off) is 6 loose.
- gen_bd163: orders of the 5, 17, 11 test. The Linux build tests 17, 5, 11, but here 5, 17, 11 is best (26 against 28 and 30 loose, others costing more).
- gen_bd164: loadBlFiles written like loadConsoleBlFiles, switch in the loop and r a local. 164 loose at best, mostly layout; registers and code line up. This is still the shape I'd bet the author wrote, since the console function matches that way and tmp/xeBuild64 (v1.16) keeps r in a register tested after the switch.
- gen_bd165: console's fallback (`if (suGetCF(..)) *pr = 0;`, then `if (!*pr)`) with *pr: 115 loose at best, about the same with `seq`, `and` and `nest2`.
- gen_bd166: more fallbacks. c7 and c9 (no `goto chk`) are 33 loose, 192 strict, without constant_p. It's the most natural form short of the loop, and worth one more look.
- gen_bd167: 12 tail forms x `*pr` expect or not x hints: nothing beats the source's own tail; 0 loose, 7 strict at best, as above.
- gen_bd168: case 23 nesting, order and `% 4` (lab_badsize): 6 loose whatever the form, with and without the outer nest.
- t0 (no expect on type 10): adds `test edi,edi; je` after the CF and CG checkBl (4 loose), and block 24 goes to the end (key 0).

### Evidence from the Linux build (tmp/xeBuild64, older version, gcc 4.9)

Structure only: `r` in ecx with `test ecx,ecx` after the switch; the signature test order is 17, 5, 11; after setFlashBuild it reloads r and tests it; CF sets r13d to 9 before the SE test; CG goes to its own checkBl and on to the next iteration. Its strings run failed, passed, no-key, the order of `if (xb.pub1bl) { if (!v) failed else passed } else nokey`, which supports that form over the near miss's `if (!xb.pub1bl)`. The strings also appear once for the signature logs, so the code really is in one place.

### isUpdateBl, devgl, pin_size: looked at, nothing new

- isUpdateBl: the exported function's mask has bit 23 (0x3818600), addUpdateBls' copy doesn't (0x3018600) and tests 23 first. Only `type == 23`'s jump polarity differs (12 loose).
- devgl: `fuse` is `setne`, then `cmovbe` from the two-value test. Not retried; the don't-retry reasoning stands.
- pin_size: not retried; no new idea.

### Don't retry

- Getting the type-11 copy by frequency: it's the PHI order above.
- The `!xb.pub1bl` first signature forms (`c`, `d`, `e`): they lose the copy.
- `*pr` tested after the signature to replace `else if (type)` (s1 to s5): the passed log's literal moves.
- `goto sigdone` around the passed log (s6): 54 loose.
- Tail forms for t5le (gen_bd167) and case 23's forms for badsize (gen_bd168).

### What to try next

- A natural non-constant entry into the shared checkBl that dies at dom2. This is what's left between here and 3 tricks gone. Start from c7 and c9, and from whatever the near-miss patch's edge arithmetic says.
- The loop form (gen_bd164) with the mechanisms above in hand: read which blocks move, and why, rather than sweeping.
- `else if (type)`: anything that keeps the passed log's first block free of a call without a copy.
- FSM order may explain other "thread only happens with this shape" hints in other objects: check `FSM did not` in dom3 first.

## Attempt 7

Started on the small functions, as asked. One trick landed, patchBlsBlmod's, with a new lever. Generators gen_bd171 to gen_bd181. `bdhints.py` holds the remaining hints as named edits and prints their costs. gen_bd171 and gen_bd172 only rerun against src/build.c from before this attempt, as they look for the attribute; the rest run on this attempt's source.

### What moved the numbers: a small helper the early inliner takes (21 -> 20, full build SHA256 matches)

**patchBlsBlmod's no-early-inlining -> `align16` (gen_bd171, gen_bd172).** `static uint32_t align16(uint32_t v) { return (v + 15) & ~15; }`, used at all seven such expressions in build.c. Three attempts of sweeping neutral shapes had missed it.
- Why: the two spill stores follow partition order. Without the attribute, einline gives the third findFile's `i` a low freed name (i_20, seen from 027t.einline on), so pt's partition sorts before cd's. The freed names are the removed calls' `.MEM` names (the "missing" versions in a dump without `-vops` are often virtual operands, not holes). Another inlined call changes which copy gets them. With align16: cd partition 25, pt 29, cbb 34.
- gen_bd171: the sites that matter are patchBlsBlmod's. `bcd` or `abcd` are IDENTICAL, any smaller subset keeps the 2 lines. gen_bd172: the other three sites (loadFileCrc's two, patchBlsResign's one) make no difference, so all of them use it.
- **Lesson: when a hint is about SSA numbering, try a natural small helper, because it's a call until einline.** Spelling changes don't move these names, and a big helper isn't inlined early.

### Mechanisms found (no landing)

- **pin_size: it's operand order.** At forwprop4, `size_41 = size_254 + prephitmp_229` becomes `prephitmp_229 + size_254`, as the lower version goes first. So IRA's shuffle copy ties the sum to the prephitmp (r105 with r197), not to the running size, and they end up in different threads. In the JTAG arm the sum is `size_249 + prephitmp_287` because that arm's PRE names are new. PRE does this arm first and takes names off the free list (243, 242, .. 229); size_254 was made at dom2 and is high. In the source that matches, the asm isolates size from this. The mov is LRA's output reload for `size_226 = size_41 + _225` when the two sides have different registers (`add esi,..; mov ebx,esi`), not an out-of-SSA copy. To remove the pin, prephit's version has to be above the size PHI's, or the load must not go through PRE.
- **isUpdateBl: its own profile decides.** The exported function isn't early inlined into addUpdateBls (`_26 = isUpdateBl (type_24)` at profile_estimate), so the inlined copy keeps isUpdateBl's probabilities. The front end folds `a == x || a == y` pairs into one non-short-circuit test: `(23|15)`, `(16|9)`, `(10|24)`, then `25` alone. Each pair has only early return (39%), since `_5 != 0` gets no nonequal; a lone `==` gets both, 19.9%.
  - rotate_loop takes the hottest edge leaving the trace: 23's is 8725 * .39 = 3403 and the bit test's 5323 * .39 = 2076. So `type == 23` needs under 23.8%.
  - A lone 23 has 19.9%, but then it joins the bit test (mask 0x3818600 in the loop, L226). 23 only stays out of the bit test while it shares a test with the next type. That's the bind.
  - **`23, 10, 9, ..` (gen_bd173, gen_bd174, 48 orders, 4 loose in addUpdateBls) gets the rotation right** without an expect: `(23|10)` stays a real OR, expand splits it into two jumps and halves each edge. What's left is that 10 stays out of the mask (`cmp esi,0xa; je`, 0x3018200). The size change also moves buildFlash's call displacements and .rdata, which isn't a real difference.
  - `23 bac ere`-class ranges (`type == 23 || type == 15 || type == 16 || (type >= 9 && type <= 10) || type == 24 || type == 25`, 5 loose): the loop's mask takes 23 and the exported function loses `movzx eax,al`.
- **exp_devgl, exact condition.** Tree-sink moves `fuse` when the block's frequency is under 75% of its definition's. Two NONEQUAL tests give 50%, stale after ifcombine. A helper keeps it (gen_bd179: 7 loose at best, usually 9 to 13).
- **pin_e:** e and f are colored by thread frequency: e is pushed last and popped first, so it gets ebx. The pin adds e's frequency, which swaps the order. Without the verbose expect the frequencies change and it swaps by itself (exp_verbose + pin_e costs the same 18). So the pair falls together or not at all.
- **pin_i:** next (a50) is colorable early, so it's popped late, gets edx, and improve_allocation moves it to ebp by spilling e. Size has taken esi by then. Reaching next = esi needs next to be popped first, and it has too few conflicts for that.
- **pin_d:** the base (r535, thread 422) is popped before d (thread frequency higher), and gets eax. Its thread would have to outweigh d's.

### Near miss, not landed

`loadBl60` with `||` in loadBl's second case-24 arm only (`*pr = loadBl60(e)`, gen_bd178 `c or 2`) is IDENTICAL. The first arm and the console copy can't use it (90 and 6 loose), and one helper call beside two written-out copies is no more natural, so src keeps the three matching copies. `checkBlSig` in place of `else if (type)`: 128 loose.

### Don't retry

- pin_size by lookups through a helper, any subset of the 7 (gen_bd176, 127 cases: 40 at best).
- exp_upd: 23 tested in the loop before isUpdateBl (gen_bd175: 228 and up), parenthesized groupings (gen_bd180: parens mostly normalize, 12 at best), forms of isUpdateBl's return including bit tests (gen_bd181: 12 at best).
- exp_devgl through isDevGl, at the one site or all, 4 helper forms x 5 fuse forms (gen_bd179).
- loadFileCrc: logs per pad arm with align16 (gen_bd177: .rdata moves, 79 and up).
- Larger helpers in patchBlsBlmod (setBlSize, copyPatch, a file-entry lookup): not inlined early or cloned, 199 and up.

### Not tried this attempt

- exp_t24 and lab_none: no new idea, so per the brief no sweep. The scan bounds: no new form tried, only the mechanism above (attempt 5's) re-read. loadBl: attempt 6's leads stand.

### Costs now (strict and loose, removed alone)

lab_t5le 7/0, exp_pr 18/2, exp_upd 18/12, pin_i 22/22, pin_d 23/14, pin_e 26/26, lab_badsize 26/6, exp_t24 29/7, exp_210 43/11, exp_devgl 43/7, pin_size 82/40, exp_verbose 83/18, exp_200 97/29, exp_t10 116/46, vol_fail 296/126, lab_none 333/231. Sets: lab_t5le+exp_pr 13/2, exp_200+exp_210 239/189 (111 loose in extractSmcConfig itself).

### What to try next

- exp_upd: the `(23|x)` OR that stays a real OR is the right lead. Find why 15 joins the mask from `(23|15)` but 10 doesn't from `(23|10)`, reading reassoc1 (optimize_range_tests) on both, and look for an order where the OR survives until expand and x still ends up in the mask.
- The same lever elsewhere: other small helpers the author is likely to have had, wherever a pin or hint comes down to SSA or partition order. image_read's and other objects' notes may have similar cases.
- pin_size: anything that keeps this arm's size load out of PRE, or changes PRE's order so this arm gets new names.

## Attempt 8

No match; src is unchanged. Generators gen_bd190 to gen_bd196 run on src/build.c as of f302f7d. tree-ssa-reassoc.c was read from the official repo at releases/gcc-6.2.0 (into build/bd/a8, not kept in tools).

### isUpdateBl: why only `(23|15)` works, and why it then needs the expect

Read from reassoc1 (`bddump.sh file.c addUpdateBls t-reassoc1`) on `23, 15, ..` and `23, 10, ..` with no expect.

- The front end pairs the chain into `(23|15) (16|9) (10|24) 25`, one block each. The first block dominates addUpdateBls' body, so **FRE reuses its compares for the body's own `type == X` tests** (`if (_105 != 0)` for `type == 23`). A compare with two uses stays in place: reassoc's inter-bb range test (maybe_optimize_range_tests) leaves it out of the merge. Compares in later blocks don't dominate the body and aren't reused.
- 15 is the only update type the body never tests with `==`. So in `(23|15)`, 15 joins the bit test and 23 stays out, which is the reference's `cmp 23; je` and mask 0x3018600. gen_bd196 checks it: with the expect kept on `(23|X)`, X = 15 is IDENTICAL and 9, 10, 16, 24, 25 cost 127 to 280 lines.
- But then the first block is `_105 | 0`, a single jump with isUpdateBl's own probability: early return only, 39% (the `_5 != 0` test on a bool gets no opcode heuristic, and isUpdateBl isn't early inlined, so its profile is what's inlined at IPA). rotate_loop needs that edge under 23.8%.
- `23, 10, ..` gets the rotation right only because 10 is reused too, so the OR stays two jumps and expand halves the edge. That always leaves a `cmp 10` the reference doesn't have.
- So the reference shape needs a first block `(23|15)` with less than 23.8%, and no form of isUpdateBl itself can give that: it has no calls, no loop, and only the early-return predictor reaches that edge (gen_bd181 covered its return forms). Perhaps the original really had a likely/unlikely there; this attempt found nothing natural that replaces it.
- The test written in addUpdateBls' loop instead (a macro or copy, isUpdateBl plain; gen_bd190, 720 orders x `||`/`&&` forms): 54 loose at best, and 23 joins the mask in every form starting `23, 15` (212 and up). In the loop the test is negated (`continue` unless it's an update type), so the pairs are `type != 23 & type != 15` (cunrolli dump); the body's `type == 23` isn't the same expression, nothing is reused, and 23 merges.

### Other sweeps, all no better than src

- gen_bd191, the helper lever on pin_d: a natural `takeData(e, &xb.kv)` (and `takeFile`) for the nine "free, take over data and size, clear the source" moves in loadBl and loadConsoleBlFiles, by group, two statement orders, pin on or off. The pin still costs 14 loose in every form; with the pin on, loadBl's three netfile moves through the helper are 2 strict lines off, the console's cost 3 loose and move .rdata, the fileent moves 84 and up, the smcConfig moves 182 and up.
- gen_bd192, exp_devgl: fuse as int, unsigned, BOOL, _Bool, uint8_t, char, uint32_t x `!= 0`, `!!`, `? 1 : 0`, plain. 7 loose at best (the same as src without the expect); the narrow types cost 12.
- gen_bd193, `else if (type)`: plain else 54 loose; the failed arm going straight to `fail` (the same behaviour, as the tail would break with -1 or goto fail) 89; returning from it 50; positive polarity 61.
- gen_bd194, lab_none: loadConsoleBlFiles' precheck as a plain early return (`if (nFiles <= 1) return 0;`, three spellings) 231 loose: the early-return predictor makes the guard hotter. The plain `for` with no precheck stays the best at 4 loose, 8 strict.
- gen_bd195, pin_size: calcBlAreaSize's two round-ups through an `alignUp(v, a)` helper (two forms, with or without the `size & 0x3fff` guard). The helper is free (IDENTICAL with the pin) but the pin still costs 40 loose: those sites are after the arm, so they don't change PRE's names there. Dropping the guard costs 103.

### Don't retry

- exp_upd by any order, grouping, form of isUpdateBl's return, or the test written in the loop: the partner must be 15, and then the first block's 39% is fixed by isUpdateBl's own profile.
- pin_d by a take-over-data helper (gen_bd191).
- exp_devgl by fuse's type (gen_bd192).
- `else if (type)` by sending the failed arm to `fail` or returning (gen_bd193).
- lab_none by an explicit early return (gen_bd194).
- pin_size by helpers after the arm (gen_bd195).

### What to try next

- exp_upd only falls if something lowers the `(23|15)` edge in isUpdateBl's own profile, or if isUpdateBl is early inlined into addUpdateBls with the loop's predictors and 23's compare still reused. Neither looked natural here; treat it as parked.
- loadBl's group (2 constant_p, t5le, exp_pr, exp_t10, badsize, vol_fail, pin_d, `else if (type)`: 9 of the 20) is still where most of the count is, and attempt 6's leads stand. Note that `if (*pr) goto fail;` in the `xb.type <= 5` tail does nothing to behaviour (*pr is 0 or already -1 there): it's only there for the shared -1 block. A natural form of the tail without it would have to give the same block in another way.
- The scan bounds, exp_verbose with pin_e, exp_t24 and lab_badsize had no new idea this attempt.

## Attempt 9

No match; src is unchanged. Goal was loadBl from a fresh question about structure. Generators gen_bd200 to gen_bd205 build from src/build.c as of f302f7d (gen_bd200's text replaces loadBl and loadBlFiles whole, so it reruns as long as those two keep their first and last lines). New tools: `bdanchors.py file.c fn` (block order of fn against the reference, read off calls, .rdata offsets and rets; a moved block shows as a -/+ pair) and `bdrdata.py file.c` (which .rdata strings moved). Best whole-function reconstruction: drafts/build_loadBl_loop_reconstruction.patch (apply with `git apply -p0`).

### What the reference and the Linux build say about the structure

Read from the reference's loadBlFiles (objdump, IDA's build/decomp_22.txt) and tmp/xeBuild64's (build/x64.dis, the function at 405280; strings found by address):
- **The arms only set r, and r is tested once after the switch.** Both builds keep r in one register (edi, ecx), every load result goes through it, and every failure reaches one `could not read` log. In Linux the test is literally after the switch (405355 `test ecx,ecx`), as loadConsoleBlFiles has it.
- **One shared `r = -1` site for the SMC, patch-size and signature failures**, in both builds: Windows 33d4 (`mov edi,-1` falling into the log), Linux 4059e2. loadConsoleBlFiles, written with plain `r = -1;` per arm and matching, has a separate `mov edx,-1; jmp` after each failure in the reference. So the original loadBl really had one -1 site (src's `goto fail`), not `r = -1` per arm; the asm barrier's job (keeping that block) is real, only its means is a hint.
- **After a signature failure the code still reaches the tail:** `xb.type <= 5` goes to the shared -1, otherwise `type == 14` is tested and setFlashBuild can run (with `xb.files[i].data`, frequency 0) before the log. In Linux both outcomes do the same, so the tail isn't guarded by r. That matches `if (xb.type > BUILD_DEVGL16 && type == 14)` or src's tail; nothing tells them apart.
- CF success and the load-success type-9 path share the SE test; CG has its own checkBl(10). The type-11 test is a copy only in the Windows build (gcc 6 threading); Linux sends 17, 5 and 11 to one pub1bl block.
- .rdata order is not source order: the strings run sig block, 1, 22, 25, 27, reading.., 3, 23, 4, default, log. It's the bb chain order at expand, after threading; every reconstruction below kept it (`bdrdata.py`: 0 strings moved), and the `.rdata differs` they report is the jump table.

### Three reconstructions, no hints at all (loose lines in loadBlFiles)

| | Shape | Best | Generator |
|---|---|---|---|
| A | The switch written in loadBlFiles' loop, r a local, `r = -1` where it fails (as loadConsoleBlFiles and the Linux build) | **128** (con2 fallback, `!xb.pub1bl` signature form, 5,17,11, int r) | gen_bd200 (288 cases) |
| B | src's `static void loadBl(e, i, &r)` with every loadBl hint off | 183 | gen_bd201 |
| B2 | A's arms in `loadBl(e, i, &r)`, through `*pr` or a local stored at the end | 225 and up | gen_bd204 (144) |
| C | A's switch in `static int loadBl(e, i)`, r returned | 225 and up | gen_bd202 (72) |

For comparison, src with its 9 loadBl hints is 0, and attempt 5's near miss (6 of them off) is 32. In A: the fallback form `con2` (`if (r) {9: CF; else 10: CG}` then `if (r) break;`) beats console's `if (!r) {...}` and the `&&` forms; signature `!xb.pub1bl` first beats the Linux string order's form by 50 (attempt 6's PHI-order rule doesn't carry over to the loop); tail form, guard form and case 23's form make no difference; int r beats uint32_t by 17.

What A gets wrong (`bdanchors.py`): only two blocks move (case 2's smc fallback, case 27's config.bin chain), the type-11 copy is missing, and the rest is attempt 1 to 6's known small things (the d registers, a 0x60 copy's `mov edi,eax`, the -1 placements, `jbe`/`ja`).

### Mechanisms

- **The none test's probability is why loadBl is a helper.** In src the guarded block is the call `loadBl(e, i, &r)` at profile_estimate (the helper has calls, so it isn't early inlined), so PRED_CALL gives `strnicmp != 0` 29%: switch 6160, each case arm 513. With the switch written in the loop (A), the guarded block holds no call: 50%, switch 7163, arms 597, and that is what moves cases 2 and 27. loadConsoleBlFiles gets 50% too, and matches, so the two loops were not written alike. A call at the head of A's guarded block (`GetTickCount()` as a probe) doesn't rescue A (170): the arms differ in more than frequency.
- **A helper that returns r (C) puts return predictors on its arms:** the -1 and 1 PHI arguments of `return r` get the negative and const return predictions, so failure paths go cold and appendAddonPatches, checkBl and the signature log move to the front. src's `*pr` stores get no such prediction, so the original's r went through a pointer (or memory), as src has it.
- **Why src keeps a `fail:` block only with the barrier** (from memory of tree-cfgcleanup.c's remove_forwarder_block and cfgcleanup.c's try_crossjump_to_edge, not checked against the 6.2.0 source): an empty `fail` forwarder survives tree cfg cleanup only while one of its predecessors also reaches its successor directly (the smc test does, before threading); after the caller's `if (r)` is threaded it can go, and then the patch-size log's -1 is appended to the log block, which crossjump can only share if that block (the lower index) is wholly matched. That is attempt 4's observation, now with the reason.
- The scan loops: the found test in the loop condition (`for (..; i + N <= size && (found = ..) != 1; ..);`), `while` forms and a separate `found = ..; if (found == 1) break;` all compile to the same code as src's form, with or without the expects (gen_bd205, 200 cases). `if (found != 1)` for the second loop costs 80.

### Don't retry

- The loop form (A) with hints added back: d pin 14 lines, type-10 expect 2, badsize label worse, a `fail:` label inside the switch (with or without the barrier) 64 to 85 worse (gen_bd203).
- A helper returning r, with any call form or the none test inside it (gen_bd202).
- A's arms moved into the `*pr` helper (gen_bd204).
- Scan loop forms with found in the condition (gen_bd205).

### What to try next

- loadBl: B is right at the loop level and A is closer in the arms. The arm in the helper has to keep A's threading, which happens after inlining in A and partly before it in B. Compare A and B's vrp1 and dom2 dumps on the 5..21 arm (`bdpasses.py`), rather than sweeping B's spellings again; the first pass where they part is the lead.
- The shared -1 needs a block that survives until expand. The cfgcleanup reading above says one way: a `fail` whose every predecessor keeps a second edge to the same successor. Not tried.
- The scan bounds, exp_verbose with pin_e, exp_t24, lab_badsize: no new idea beyond the loop forms above.

## Attempt 10

No match; src is unchanged. Generators gen_bd210 to gen_bd213 run on src/build.c as of 2f2be6f (gen_bd211 to gen_bd213 build on gen_bd210's `b f brk`, through its `mk`). tree-cfgcleanup.c, cfgcleanup.c and bb-reorder.c were read from the official repo at releases/gcc-6.2.0 (into build/bd/a10, not kept; bb-reorder.c turned out not to be needed, and cfgrtl.c's fixup_reorder_chain was not fetched).

### Which pass removes `fail:` without the asm (checked against dumps and source)

- With the asm off, `fail` survives every cleanup_tree_cfg up to fre3: two of its predecessors (the smc test and the t5le `*pr` test) also reach the `if (r)` join directly with another value of r, so remove_forwarder_block refuses it (its phi_alternatives_equal check), as attempt 9 guessed.
- But **mergephi2 (pass_merge_phi, 095t) removes it.** `fail` has a virtual PHI (`.MEM_230 = PHI <.MEM_213(25), .MEM_250(83), .MEM_267(102)>`, seen with `-fdump-tree-fre3-vops`): its three predecessors come with different memory states. pass_merge_phi takes any forwarder *with* PHIs (tree_forwarder_block_p(bb, true)), and remove_forwarder_block_with_phi doesn't refuse on differing arguments: it splits those edges into new forwarders. So the -1 moves to the split smc and t5le edges (new, high-index blocks) and onto the size log's own edge. phitrack (largest PHI's -1 arguments per pass): `ccp2 4294967295(106)`, then `mergephi2 4294967295(83) (112) (113)`.
- So attempt 9's lead, "a `fail` whose every predecessor also has a direct edge to the same successor", doesn't help: that only stops remove_forwarder_block, and mergephi doesn't care. To survive with no asm, `fail` must have no PHI at mergephi2 and mergephi3 (104t), i.e. one predecessor (or all with the same memory state), or hold a real statement until expand.
- Even with one predecessor, a source `fail` block goes later: once vrp1/dom2 thread `if (r)` it forwards straight to the could-not-read log, which its predecessor doesn't reach directly, so cleanup removes it and moves its label into the log (gen_bd212: `goto <bb 109> (fail)` where 109 is the log).
- **Crossjump's rule** (cfgcleanup.c, checked): with a 1-insn match (`mov edi,-1` is under min-crossjump-insns, 5) try_crossjump_to_edge only goes ahead when the 'from' block is wholly matched. Against the fallthru predecessor 'from' is the non-fallthru one; otherwise it's the lower-indexed one (try_crossjump_bb only pairs e with a higher-index e2, and identical insns keep dir_both, so no swap). The size log's block is lower (expand order follows source order, which .rdata pins) and isn't wholly matched, so its -1 can't join the split-edge -1 blocks. This is attempt 4's observation with the reason read from source.

### Near miss: no asm, no t5le label, no `*pr` expect (gen_bd210 `b f brk`, 3 loose, 11 strict)

drafts/build_loadBl_brktail_nearmiss.patch (`git apply -p0`; the patch leaves the old comments as they are). Three edits, all natural and with the same behaviour:
- the size log sets `*pr = -1; break;` itself, in place of `goto fail`;
- the `xb.type <= BUILD_DEVGL16` tail is a plain `if (xb.type <= BUILD_DEVGL16) break;` (`*pr` is already 0 or -1 there, as attempt 8 noted);
- `fail:` keeps case 2's goto only, with no asm. (`fail` then has one predecessor, no virtual PHI.)
What's left, both in loadBlFiles:
1. The size log has its own `mov edi,-1` and jumps to the log; the reference jumps to the shared -1 block (the crossjump rule above).
2. The CG/SE checkBl copy at 388a: `ja 358e; jmp 2f30` for `jbe 2f30; jmp 358e`. Its `xb.type <= 5` jump has REG_BR_PROB 10000 on gtu in the bbro dump, where src's hot label gives 9869 on leu (the other two `xb.type` tests are 0 here against 9869 and 1090 in src, but come out the same). It's the edge drained by dom2's threads again, which is what t5le was for.
Tried on this base, none better: the t5le hot label back on the plain break (10000 lines: a hot label on a break heats everything), `return` for either break, `type != 14` exits, `xb.type > 5 && type == 14`, type tested first (66 and up), the size test inverted or with `else` (same 11), the asm put back (58), case 2's -1 written in place (`{ *pr = -1; break; }` or `if (!e->offset) *pr = -1;`: 240), case 2 moved ahead of other cases (47 and up, gen_bd211), `fail:` placed inside the switch before case 23 or others (11 at best, gen_bd212).
With all of loadBl's other hints off as well (t10, badsize, pin_d, the constant_p entry, `else if (type)`), this base is 109 loose (218 strict), better than attempt 9's A (128) and B (183). No single hint or pair goes free on it (lab_badsize+pin_d is the cheapest pair, 23 loose).

### Don't retry

- Keeping `fail` by giving every predecessor a direct edge to the join: mergephi merges it anyway.
- `fail:` label position in the source: it doesn't set the block's fate or index (gen_bd212).
- Case 2 moved within the switch (gen_bd211), or its -1 written in place.
- Hot labels on a `break`.
- Tail forms on the near-miss base (gen_bd213, q3/q5 in build/bd/a10): 11 at best.

### Not done

- The A/B pass diff (goal 2): with the near-miss base at 109 loose with every loadBl hint off, it now beats A, so the premise ("A is closer in the arms") changed; not run.
- Goal 3 (exp_verbose with pin_e, exp_t24, lab_badsize): no new idea.

### What to try next

- The near miss's size log: its -1 has to end up in a block that's wholly matched and lower in index than the others, or in one GIMPLE block with the smc -1 that holds a statement until expand. The reference's -1 block (33d4) has the smc test, the size log (30a4 jmp) and the sigfail copy (37d0 jbe) as predecessors, so the original kept one block somehow.
- The near miss's SE copy: anything that raises the `xb.type <= 5` probability on the CG/SE checkBl path without a label; check REG_BR_PROB in `bdbbro.sh` (build/bd/bbro_loadBlFiles.txt) on the compares with `xb+8` and 5.

## Attempt 11

No match; src is unchanged.  Goal: close attempt 10's near miss (`b f brk`, drafts/build_loadBl_brktail_nearmiss.patch). Generators gen_bd220 to gen_bd225 run on src/build.c as of 350598e (gen_bd220, 221 and 225 build on gen_bd210's `mk`). tree-ssa-threadupdate.c was read from the official repo at releases/gcc-6.2.0 (into build/bd/a11, not kept). Scratch tools in build/bd/a11 (not kept in tools): `trk.py dumpdir fn regex` (per tree pass, the blocks whose `if` matches regex, with frequency and successor probabilities; how the numbers below were read), `pp.sh` (all tree dumps of a file, then trk).

### (b) The SE copy's `ja`: why the copies get P(<=5) = 0 (checked against dumps and source)

- At profile_estimate (loadBl, `bddump.sh f loadBl t-profile_estimate`) the near miss's `xb.type <= 5` gets only the early-return heuristic: 39% (`<=5` is a plain `break`, i.e. the return block). src's hot label makes it 85%. Without the label but with src's `if (*pr) goto fail` arm (t5le alone off) it's 50%: no heuristic at all.
- vrp1 threads every way into that test (joiner threads `(pred, X) (X, join) joiner; (join, next) normal`, X the test, join loadBl's return = loadBlFiles' `if (r)`), so X is copied for the r = 0 paths (freq 157) and the sig-failed path (29). For a joiner copy, ssa_fix_duplicate_block_edges (tree-ssa-threadupdate.c) sets P(on-path) = path_out / path_in, where path_out is the minimum count along the rest of the path. In the near miss the copy of the join (the path's second block) gets frequency 0 (`trk.py`: copies `bb136[157] _438 <= 5 -> 135 (0%) | 24 [100%]`, and bb135, the join's copy, `freq 0`), so the `<=5` edge of every copy is 0% and stays so to RTL (REG_BR_PROB 10000 on gtu / 0 on leu for all six `xb.type` compares). Why the join's count is 0 at that point: the same pass's FSM threads into the join (`(x, join) nocopy`, about 30 of them, all loadBl's other exits) are done before the joiner threads, and they take the join's flow; I didn't follow those updates line by line, so that part is inferred. In src the `<=5` arm is the t5le block (the `*pr` test), its own block, so the path doesn't continue through the drained join.
- So the near miss's tail can't get `jbe` by spelling the `xb.type` test: any form whose `<=5` edge goes straight to the join gets 0%. It needs a block of its own in the `<=5` arm that the threads go through, which is what src's `if (*pr) goto fail` is.

### t5le alone (exp_pr and the asm kept): what it needs

- src minus the label is 0 loose, 7 strict: the SE copy is `jbe` (its P(<=5) is 57.96%), only the last no-key log loses its `.p2align`. compute_alignments aligns that block (freq 17, no fallthru) only by "freq > 10 x prev": prev is fixup_reorder_chain's `jmp` block after the SE copy (freq 4), whose frequency is 4 x P(>5). It needs frequency <= 1, so P(<=5) >= 62.5% on the SE copy (src: 98.69%).
- Measured (diagnostics, not shapes): with an expect on the test, P(copy) follows the base probability (55% -> 36%, 65% -> 50%, 75% -> 67%, 85% -> 86%, but that run also moved the `*pr` expect, as both use the param). With a call on the `>5` side (a dummy `setFlashBuild(0)` in front of `if (type == 14)`), PRED_CALL makes the joiner 71% and the SE copy 82%: enough. So a guarded call right at the `>5` edge would land t5le.
- No natural shape found that does it (gen_bd222, gen_bd224): `< BUILD_DEVKIT`, `*pr == -1`, every if/else arrangement of the kit and `*pr` arms (0/7 at best, `jbe` but no alignment); a `seFlashBuild(i, type)` helper holding `if (type == 14) setFlashBuild(..)` (two calls, so not early inlined: 74 loose, the helper's own profile moves much more than this edge).
- The kit arm first, `if (xb.type > BUILD_DEVGL16) { if (type == 14) set..; break; } if (__builtin_expect(*pr != 0, 0)) goto fail; break;` (gen_bd223 `brk exp`, gen_bd224 g1/g4/g6..g8): 4 loose, 19 strict in loadBlFiles (the rest is call displacements): the alignment and SE copy come out right, but the sig-failed setFlashBuild copy reads `xb.files[i].data` through the IV (`mov eax,[ebx]`) where the reference recomputes it (`imul eax,[esp+0x2c],0x42c`). In src that copy is made by vrp1/dom2 on the loop's exit path before ivopts (`i_373 = PHI <i_402>`, loop-closed), so ivopts leaves it; in this form it's still the in-loop block at ivopts and is copied later. `xb.type > 5 && type == 14` (`and exp`): 2 loose, 18 strict, but its sig-failed `type != 14` path goes to `fail` where the reference sets its own -1. `type == 14` first (3 forms): 43 loose.

### (a) The size log's own -1: what I checked

- At jump2 (the only crossjump pass here; `-fdump-rtl-all`) the -1 blocks are: bb34 (sig-failed arm), bb104 (the size log, -1 last), bb129 (sig-failed copy's split edge), bb130 (`fail`, case 2's split edge), and jump2 does `Cross jumping from bb 129 to bb 130; 1 common insns`. bb104 against bb130 is refused: bb130 falls into the log block, so bb104 is 'from' and not wholly matched (attempt 10's rule).
- The reverse direction (S into L's tail, which would give the reference's `jmp 33d4`) needs L to be the fallthru predecessor of the log at jump2, i.e. the size log right before the could-not-read log in the insn chain. The .rdata order (size 0xeb0, then 27's config.bin strings, the default case's, the log's 0xf28) is expand order, so case 27 and default are expanded between them: not possible with this string order.
- So the reference's size log was never holding a -1 of its own: its edge's -1 was in a block that existed at expand (src's `fail`, kept by the asm), or on a critical edge. Case 23 through a read helper returning -1 (`loadPatchFile`, three forms, gen_bd225): 62 loose and up.

### Don't retry

- Spellings of the near miss's `xb.type <= 5` test or arm with a plain `break` (gen_bd220: `< BUILD_DEVKIT`, `!(> 5)`, `- 1 < 5`, switch on xb.type both ways, `return`, `|| type != 14`, nesting, xb.type read into a local before checkBl): 3 loose at best, the join is drained whatever the spelling.
- A setFlashBuild helper for the kit arm (gen_bd221, gen_bd222 h1/h2): 43 to 74 loose.
- Case 23 through a read helper (gen_bd225).
- If/else arrangements of the kit and `*pr` arms on src without t5le (gen_bd224): 0/7 at best.

### What to try next

- t5le alone: a real call (with side effects) at the start of the `>5` side. Nothing natural is there in the reference (the `>5` copies go straight to `cmp esi,0xe`), so the call would have to fold away later, e.g. a call that's only removed after profile_estimate. Worth one look at what the author might have called there (a kit-only log under a verbose flag would change behaviour).
- The kit-arm-first form (4 loose): the sig-failed setFlashBuild copy has to be made before ivopts, on the exit path, as in src.
- (a) stays tied to keeping a `fail` block until expand; attempts 9 to 11 found no natural statement for it.

## Attempt 12

Goal: leave loadBl alone and reconstruct the author's structure for the other functions' tricks.  **One landing, 20 -> 17**: the scan loops (2 expects and the next/buf pin).  Generators gen_bd230 to gen_bd237 run on src/build.c as of b1ed804 (gen_bd230 to 232 and 237 replace loadFileCrc's verbose block, gen_bd233 to 235 replace findSmcConfig and its call, gen_bd236 the fuse block; 233 to 235 need findSmcConfig, so they only rerun against the old source).  Scratch in build/bd/a12 (not kept).

### extractSmcConfig: the Linux build's scan loops (landed, IDENTICAL, full build SHA256 matches)

Reading: tmp/xeBuild64's scan (404839..4048a2, build/x64.dis) tests the bound, then `found != 1`, calls smcConfigOk, and on a hit (`cmp eax,1; je`) jumps back to the bound test **without advancing i**; on a miss it advances i and loops.  That is a loop whose condition holds both tests and whose body only moves i on a miss, i.e.

```
i = 0;
found = 0;
while (i + 0x200 <= size && found != 1) {
	found = smcConfigOk(buf + i);
	if (found != 1)
		i += 0x200;
}
if (!found) { i = 0; /* the same with 0x210 */ }
if (!found)
	goto notfound;
```
gcc 6 threads the hit's re-test straight to the found block, which is the reference's fallthrough out of the loop; gcc 4.9 left it.  Written in extractSmcConfig itself this is IDENTICAL with plain flags (the param still on for the rest), with no expect, no pin and no findSmcConfig.  Behaviour is the same as the old for/break loops: found is the last result, i stays on a hit and ends past the bound on a miss.

- In findSmcConfig (gen_bd233, gen_bd234: loop forms, condition orders, i's type, const buf, declaration orders) the layout comes out right too (27 loose, 48 strict), but buf and next swap registers (edi/esi) in every form: the pin's job.  Inlined by hand (gen_bd235) it is IDENTICAL, all three init placements and both `while` spellings; `!found` as an early `return 2` with the log in place costs 591 (it moves .rdata).
- `found` initialized at the top as `while (found != 1 && i + 0x200 <= size)` (bound second) is 59 and up: keep the bound first, as Linux has it.
- Mechanism (profile_estimate read with `bddump.sh src/build.c extractSmcConfig t-profile_estimate`; the threading step inferred, not traced): both loop tests get PRED_LOOP_EXIT (first match, 4.5% each, two exits), and the inner `if (found != 1)` gets no prediction (50%).  The hit path goes back through the header, so after threading its exit edge carries about half the body's frequency, far above the bound exit's 4.5%, and bb-reorder makes it the fallthrough.  In the old for/break form the hit exit had 4.5% of a smaller block, below the bound exit, which is what the expects reversed.
- **Lesson: a loop shape the Linux build shows (an extra jump back to a re-test) can be read as source structure even when gcc 6 threads it away.**  Worth checking the Linux build for every loop that still needs a hint.

### loadFileCrc (exp_verbose + pin_e): structure read, no landing

- Reference, IDA and Linux (402900, which has the same five parameters) agree on src's structure: `e->size = size; if (pad && (size & 15)) e->size = align16(size); if (verbose) { if (size != e->size) pad log; else bytes log; }`.  Nothing in either build suggests another form.
- With both hints off only the bytes log's block is placed late (18 loose); the registers are already right.  Its block frequency is 1102 because the non-pad path reaches it only by a jump thread (vrp/dom: size == e->size is known there), and the threaded flow (about 2950) never gets added to the log's frequency (`bdcheck.sh`: the inner test 2834 > its predecessor 1968 after threading; stale).  Round 2 needs 2000: at P(!=) = 72% that needs P(verbose) >= 91%, which no natural test of an int parameter gets (compare with 0: no opcode heuristic).
- gen_bd230 (compare opcodes x arm order x `verbose`, `!= 0`, `> 0`): `e->size > size` with `verbose > 0` gets the layout right (6 lines) but `jae`/`jg` for `je`/`jne`, so the source had `!=` and a plain test.  `>` with plain verbose: 1968, 32 short of round 2.
- gen_bd231, gen_bd232: forms that give the non-pad path its own edge to the bytes log before profile_estimate.  `goto alloc` after the pad log (drafts/build_loadFileCrc_goto_nearmiss.patch, `git apply -p0`): layout right, 38 lines of name/size registers.  IRA (`-fdump-rtl-ira`, checked): name (r99) and crc (r103) are both colorable with equal conflicts and are pushed by frequency; name must beat crc to get edi (then crc goes to memory and size takes ebp).  The goto form's pad log is 504 (PRED_CALL now lands on it, as its other arm has no call), so name's frequency is too low.  Two bytes logs (dup, dup2) aren't tail-merged (79 loose, .rdata moves).
- gen_bd237: crc tail forms (early return, `r`, `c != crc`, `crc == c` return) on both bases: no change, or worse.
- Don't retry: compare spellings or verbose spellings (opcode must stay je/jne), the crc tail, two bytes logs.  What's left would need the pad log hot and the bytes log reached without a thread, at once.

### buildFlash's devgl expect: no landing

- gen_bd236: ten fuse forms (dev types as the skip case: `&&` chain, nested, if/else, ternary, `||` value, switch, switch in the non-JTAG arm, negated test, bitwise or of the two tests): 7 loose at best (the negated test, same as src without the expect).  The reference speculates the glitch2mfg load and setne on every non-JTAG path and merges by cmovbe; the switch forms don't get if-converted.  The tree-sink rule (attempt 7) stands.

### Not reached

exp_t24 (IDA shows the same `if (type == 25) { if (offset < imgSize()) warn; else adding log }` as src; only the warning's cold block order differs), lab_none, pin_size and lab_badsize (loadBl, left alone as asked) got no new structure reading beyond that.  The Linux build's patchSmcConfig (404250) has both fan sections inline with one `cpuFan != -1` test each and the gpu warning placed before the cpu one, as in Windows; I found nothing there that suggests a replacement for patchCpuFan.

### Costs now (strict and loose, removed alone)

lab_t5le 7/0, exp_pr 18/2, exp_upd 18/12, pin_d 23/14, pin_e 26/26, lab_badsize 26/6, exp_t24 29/7, exp_devgl 43/7, pin_size 82/40, exp_verbose 83/18, exp_t10 116/46, vol_fail 296/126, lab_none 333/231.  `bdhints.py` no longer has exp_200, exp_210 and pin_i.

### What to try next

- The Linux build lens on the other loops with hints: loadConsoleBlFiles' loop (lab_none), addUpdateBls' loop (exp_upd), and loadBlFiles' (loadBl's group).  Look for jumps back to a loop test that gcc 6 would thread.
- The param is now held by the loadBl expects, exp_verbose, exp_t24, exp_upd and exp_devgl; re-measure which values still match after each landing.
- loadFileCrc: a form whose bytes log is reached directly from the non-pad path and whose pad log keeps both arms' calls (so no PRED_CALL on it).  The two-copy form wasn't tail-merged; a shape that merges might do.

## Attempt 13

No match; src is unchanged.  Goal: attempt 12's lever (loop structure read off tmp/xeBuild64, build/x64.dis) on every function that still has a hint.  Generators gen_bd240 (isUpdateBl forms) and gen_bd241 (loadFileCrc with a padded-size local) run on src/build.c as of f735084.  Linux strings were found by file offset + 0x400000 (static ELF) and grepped as `mov esi,0x...` in x64.dis.

### Structure readings (Linux, gcc 4.9)

- **isUpdateBl (407840) is a real function** in Linux too: `(t - 23) <= 2 ? 1 : ((t - 15) <= 1 | (t - 9) <= 1)`, i.e. reassoc's ranges [23,25], [15,16], [9,10].  **addUpdateBls (407870) inlines it:** `cmp 23; sete r14b; je body`, then [24,25], [9,10], and [15,16] last, on the way back to the latch; the body's `type == 23` is `test r14b` (the compare reused, as attempt 8 found for gcc 6).  The loop is `if (!isUpdateBl) continue;` with no re-test, the none test is `continue`, and the body tests 9, 23, 25, 16, 10, 24 in src's order.  Nothing here differs from src; the block order doesn't pin the source order of the chain (it depends on where 4.9's reassoc puts merged ranges, not checked).
- **loadBlFiles (405280):** r (ecx) is tested once after the switch (405355) and the loop reloads nFiles only on paths with a call.  Case 23: `if (r) -> log`, size log `jmp 4059e2`, appendAddonPatches -> latch.  **The one -1 block (4059e2 `mov ecx,-1; jmp log`) is reached from the size log, case 2's `!e->offset` (falls into it) and the signature-failed tail**, as attempt 9 said.  Signature-failed: log, then `xb.type <= 5 -> -1 block`, `type != 14 -> -1 block`, else `ecx = -1`, setFlashBuild, the r test.  The passed, no-key and non-signature types go to 405a73: `xb.type <= 5 -> latch`, `type != 14 -> latch`, else `r = 0`, setFlashBuild, the r test.  That reads as `if (xb.type > BUILD_DEVGL16 && type == 14) setFlashBuild(..);` with r tested after the switch, which attempt 11 already measured (`and exp`, 2 loose, 18 strict, with the `*pr` expect still on).  CG (405ded) goes from its checkBl straight to the latch; CF success sets r13d = 9 and goes to the SE test.  No new loop shape: the loop has no jump back to its test that gcc 6 could have threaded away.
- **loadConsoleBlFiles (405e70):** the same loop as loadBlFiles (precheck `nFiles <= 1 -> return 0`, switch, r tested after), so nothing new for lab_none; the precheck is the loop header copy any `for` gives.
- **loadFileCrc (402900):** the pad path keeps the dead `size == e->size` compare (as the Windows reference does, 2a7) and the non-pad path goes straight to the bytes log, which is a thread in both compilers.  So the source compares `size != e->size` inside `if (verbose)`, as src has it; no goto or second log.
- **addBlsToImage (4071f0..):** `if (xb.type == RETAIL && (23 || 25)) .. else if (xb.type > 5) { if (23 || 25) .. } else if (type == 25 && offset < imgSize())`, as src without the `type != 24`.  Nothing for exp_t24.
- **calcBlAreaSize (around 409700):** every findFile lookup is inlined and the arms are scattered by threading; I couldn't read a source form from it for pin_size.

### Measured

- gen_bd240, isUpdateBl's return written as ranges (`>= && <=`, `(uint32_t)(t - a) <= n`) or `==` groups in all 6 orders of the three Linux ranges, a switch, and `if (type == 23) return 1;` first: no expect in any.  Best 12 loose (`15 16 23 24 25 9 10` as `==`, the same as src without the expect); the range and switch forms change isUpdateBl itself (19 to 22 lines, the reference is one bit test with 23 in it) and cost 164 and up in addUpdateBls.  einline still refuses isUpdateBl ("growth 10 exceeds --param early-inlining-insns divided by number of calls", read from `bddump.sh .. t-einline`), so the loop's predictors never reach the first test.  The reason the message says "divided by number of calls" for a callee with no calls wasn't checked: the official repo's ipa-inline.c was behind a bot wall when fetched.
- gen_bd241, loadFileCrc with `len` for the padded size (set in two statements, a ternary, or stored late), compared as `size != len`, `size != e->size` or `len != size`, logged as `len` or `align16(size)`, allocated by `len` or `e->size`; no expect, no pin: 88 loose at best (18 for src without them); it also changes loadCommonFile (28) and moves .rdata.

### Don't retry

- exp_upd from isUpdateBl's return forms or the Linux ranges (gen_bd240); the Linux loop shape is src's.
- loadFileCrc with a local for the padded size (gen_bd241).
- Reading the Linux build for loadBl's tail, lab_none, exp_t24 or pin_size: done here, nothing beyond attempts 9 to 11.

### What to try next

- The Linux lens is used up for build: every loop with a hint has src's shape there.  What's left are frequency and register questions inside shapes that both builds agree on.
- exp_upd: only an isUpdateBl small enough for einline (growth under 7 with that check) that still compiles to the reference's one bit test would bring the loop's predictors in; the forms tried here all grew or changed the bit test.
- loadBl: Linux's tail supports `if (xb.type > BUILD_DEVGL16 && type == 14)`; attempt 11's `and exp` (2 loose) is the base, and what's left there is the sig-failed `type != 14` path going to `fail` where the reference has its own -1.

## Attempt 14

No match; src is unchanged.  Goal: one try at loadBl's tail from the `and` form, then a mechanism hunt on the cheapest trick.  Generators gen_bd250 to gen_bd254 run on src/build.c as of eb75581.  Scratch in build/bd/a14_* (not kept).

### The `and` tail can't match: the reference's two sig-failed exits differ (read from the reference's objdump)

The reference's signature-failed path (loadBlFiles 37b5..3808):
```
37c9  cmp xb.type,5 ; jbe 33d4          <=5: to the shared -1 block (33d4 mov edi,-1, falling into the log at 33d9)
37d6  cmp esi,0xe ; mov edi,-1 ; jne 33d9   !=14: straight to the log, -1 already set in this block
37e4  imul .. ; setFlashBuild ; jmp 33d9
```
So `<=5` and `type != 14` are different statements in the source: `<=5` reaches a -1 site of its own (src's `if (*pr) goto fail`), while `!= 14` and the setFlashBuild path share the -1 the failed arm set.  In every `and` form both exits are the same statement after the kit test (`if (*pr) goto fail;` or the plain `break`), so they reach the same place: `and exp` sends `!= 14` to fail (`jne 564`, the 2 loose lines), and `and` with a plain break sends both to the log with the -1 in the failed arm's block (`mov edi,-1` before the log call).  The Linux build (both exits to its -1 block) is consistent with either source, because gcc 4.9 crossjumps a split edge's `mov ecx,-1; jmp log` into that block; Windows tells them apart.  Attempt 13's reading of the Linux tail is therefore not evidence for `and`.

Measured (gen_bd250, gen_bd251; loose/strict lines in loadBlFiles):
- What the `and` form allows: `and exp` with the asm kept removes t5le only (2/18), the same as t5le alone off src (0/7 is better).  `and` with a plain break and the size log's own `*pr = -1; break;` removes t5le, exp_pr and the barrier (5/17, with or without the asm, since fail then has case 2 only), but attempt 10's `brk` near miss removes the same three for 3/11.  So the `and` form opens nothing new.
- `nest` (`if (xb.type > 5) { if (type == 14) set; break; }`) is the same as `and` with a plain break (5/17) or 4 to 7 loose with the `*pr` test.
- The `<=5` exit written in the failed arm, `log; if (xb.type <= BUILD_DEVGL16) goto fail; *pr = -1;` (before or after the store), with the tail as a plain `and`: the two exits now come out right (`jbe` to fail, `mov edi,-1; jmp` for `!=14`), but the sig-failed setFlashBuild copy moves to the end and reads `xb.files[i].data` through the IV (`mov eax,[ebx]`, attempt 11's ivopts problem) and the SE copy is `ja`: 24 loose at best (`a1 src g v`), 27 with the plain tail.

### Mechanism hunt: lab_t5le (the cheapest, 0 loose / 7 strict), and two side looks

- t5le's 7 lines are one `.p2align` on the type-11 copy's no-key log (freq 17), which compute_alignments gives when its frequency is over 10x its layout predecessor's (fixup_reorder_chain's jmp block after the SE copy, freq 4 = freq(SE copy) x P(>5)).  Attempt 11 attacked P(>5).  This attempt tried the other two factors:
  - freq(SE copy), through the SE test's form (gen_bd252: nested, split, a local, `memcmp`, `strncmp`, swapped byte order): nested and local forms compile to the same code (still 0/7); swapping the bytes changes the code (4 loose); `memcmp` and `strncmp` change it far more (500 and up).  The `== 'S'`, `== 'E'` tests each get the nonequal heuristic, whatever the nesting.
  - freq(no-key log), which the `__builtin_constant_p` entry's weight sets (gen_bd253: int or pointer compares, bare constant_p, one of the two, `||`): only src's form matches; every other form is 26 loose and up, with or without t5le.  So the label can't be moved onto that hint either.
- loadBl's signature test as a switch, the way verifyBlSigs writes it (`case 5: case 11: case 17:`, gen_bd254, 4 case orders x `else if (type)` or `else` x hint subsets): 167 loose and up.  The switch changes the code (it's no longer three compares), so it isn't the source.
- lab_badsize, read from profile_estimate: the size log gets 61% without the label (both arms hold calls, so PRED_CALL cancels, and the appendAddonPatches arm has the early-return heuristic), 89.9% with it; appendAddonPatches' block is 123 against 32.  No natural predictor raises the log's side (its first block always holds the log call); not swept again.
- pin_d, read from the objdump: in the reference the base (`imul edx,edx,0x42c`) takes the register of the reloaded nFlashFiles at the join after the load fallbacks, and d gets eax; without the pin base gets eax and d edx.  loadConsoleBlFiles' case 27 has another shape (no fallbacks) and matches plainly.  Nothing new to sweep beyond gen_bd113.
- exp_t24: a `pure` imgSize() would also keep PRED_CALL off the block after `type == 25` (gimple_has_side_effects is false for a pure call; inferred, not built), but that's an attribute in a shared header whose only job here is steering, so it wasn't tried.

### Don't retry

- Any `if (xb.type > BUILD_DEVGL16 && type == 14)` or nested kit-first tail (gen_bd250): the `<=5` and `!=14` exits must be different statements.
- The `<=5` exit as a goto in the failed arm (gen_bd251).
- Forms of the SE test (gen_bd252) and weights of the constant_p entry (gen_bd253) for t5le.
- A switch for the signature types (gen_bd254).

### What to try next

Nothing with real odds.  The only open lead is attempt 10's near miss (3 tricks for 3 loose lines), which needs a `fail` block that survives to expand with no asm (mergephi2) and a `<=5` arm block that vrp1's joiner threads go through (tree-ssa-threadupdate.c's path counts); attempts 10, 11 and 14 found no natural statement for either.  I'd park build at 17.

## Attempt 15

Goal: the tricks with the least mechanism work (exp_t24, exp_devgl, lab_badsize) first.  Generators from gen_bd260.  Scratch in build/bd/a15 (not kept).

### Costs re-measured (src as of 4c988f7c)

Singles unchanged from attempt 12's table: lab_t5le 7/0, exp_pr 18/2, exp_upd 18/12, pin_d 23/14, pin_e 26/26, lab_badsize 26/6, exp_t24 29/7, exp_devgl 43/7, pin_size 82/40, exp_verbose 83/18, exp_t10 116/46, vol_fail 296/126, lab_none 333/231.  All 78 pairs: none cheaper together than its parts, except the known exp_verbose+pin_e (18 loose, as exp_verbose alone) and lab_t5le+exp_pr (13/2).

### The exact margins of the three least-worked tricks (read from profile_estimate, sink and bbro dumps)

- **exp_devgl: 73.0% against 75.06%.**  Without the expect, buildFlash's dev test `(xb.type - 4) <= 1` gets only the opcode-positive heuristic (`x <= 1` predicted false, hitrate 73).  sink splits the critical non-dev edge (bb4, freq 603) and select_best_block sinks `_64 = _63 != 0` and the cast there because 603 < 826 x 0.75 = 619.5 (sink-frequency-threshold 75; the load has a vuse, so 82 for it, and it stays).  So the non-dev side needs 75.06% where the natural one has 73%: one more predictor in that direction of any strength would do, and none exists in that code (no call, return or loop in either arm).  The dev types written as two `==` tests are worse (48% / 52%), a switch 50%, a range written the other way folds to the same `> 1` test (73%).  Noted for later: sink also refuses when the value reaches its PHI on two edges (find_bb_for_arg returns NULL), but every form that would do that is merged into one range test by fold or ifcombine before sink.
- **exp_t24: the warning block needs frequency >= 87, it has 75.**  addBlsToImage's entry frequency is 431, so bb-reorder's round 2 needs 20% of it, 86.2; the warning (bbro block 40) at 75 falls to round 3 and is laid out after the seReplacesCf findFile(14) found-exit block (80, freq 117, round 2), which is the whole 7-line difference.  With the expect it's 153 (round 2, before 80).  The type == 25 edge gets nonequal (28%) plus PRED_CALL (the next block holds imgSize(): 29%), 13.7% of 1881 = 258, and the warning 29% of that; it needs 16% (or the `xb.type > 5` test, 50% with no heuristic, at 58% for the <=5 side).  The expect works by putting a call-free block between `type == 25` and imgSize().
- **lab_badsize: appendAddonPatches' block needs frequency < 44 in loadBlFiles, it has 76** (round 4 starts below 5% of the entry, 882).  In loadBl's own profile case 23 is 833 -> retail test 62.2% (nonequal, call and early return) -> `*pr` test 61% (early return) -> size test, whose good arm gets 39% (both arms hold calls, so PRED_CALL cancels; the good arm's break is an early return).  It would need about 22.6%: 39% -> 22.6% takes a predictor of about 69% on its own, or two of 60%.  The label gives 89.9% for the log.

### What landed: lab_badsize by the spelling of the size test (17 -> 16, IDENTICAL, full build SHA256 matches)

gen_bd261: `if ((e->size & ~3) != e->size)` in loadBl's case 23, no label.  A compare of two non-constants gets the opcode-nonequal heuristic (72% for `!=`), which `x & 3` (a compare with 0) doesn't; with the good arm's early return (61%) that's about 80% for the log, so appendAddonPatches' block falls under round 4's threshold.  fold leaves the form alone until after profile_estimate, and every spelling of it compiles to the same `test al,3`: `(x & ~3) != x`, `x != (x & ~3)`, `x / 4 * 4 != x`, `(x >> 2 << 2) != x`, `& ~3u`, `& 0xfffffffc` are all IDENTICAL; `x % 4` is the old 6 loose.  gen_bd262: the same spelling in loadConsoleBlFiles' case 23 costs 6 loose there, and in appendAddonPatches' addon test (`== a->size`) 60, so only loadBl uses it; that inconsistency is why src marks it "Borderline, for review".

**Lever for the rest: a test's spelling picks its opcode heuristic.**  `==`/`!=` between two non-constants, or against a non-zero constant, gets nonequal (72%); `<`/`<=`/`>`/`>=` against 0, 1 or -1 gets positive (73%); anything compared with 0 (including a bare value or `x & c`) gets nothing.  Worth checking on every remaining expect and label whose margin is one predictor.

### The spelling lever on the rest (gen_bd263 to gen_bd266), and other sweeps: nothing more lands

- gen_bd260, exp_t24: the room test out of the xb.type chain, as addUpdateBls has it (`if (type == 25 && e->offset < imgSize())` after the chain; the same behaviour, as the chain's other arms already skip 23 and 25), with four chain forms and three room forms: 63 loose at best.  vrp1 then doesn't thread the kit path's not-23/25 edge past the type-25 test (the reference does), so the chain really is an `else if` chain.
- gen_bd263, exp_pr: `*pr` is 0 or -1 at the tail, so `*pr == -1` (nonequal) or `(int)*pr < 0` (positive) can stand for `*pr != 0`.  With the t5le label kept: 0 loose, 9 strict (both), against 2/18 for the plain `!= 0`; the 9 are a `.p2align` on the type-11 block (compute_alignments, `-fdump-rtl-alignments` via bddump.sh: its layout predecessor, the sig-failed setFlashBuild copy, falls from 4 to 0).  Why: the sig-failed joiner copy of the `xb.type <= 5` test gets P(<=5) = path_out / path_in, and path_out is capped by the `*pr`-true edge's count, so that edge must carry less than the sig-failed path's own flow (about 2% of the test's count); natural heuristics give 28% at best (37.8% with the break's early return).  Without the label every spelling is 2 loose (the SE copy's `ja`).
- gen_bd264, exp_devgl: the dev override as a second top-level statement (`fuse = 1; if (!JTAG) fuse = g != 0; if (dev) fuse = 1;`, five forms of the first part, either order): 7 loose, as src without the expect.  vrp1 threads the JTAG path past the dev test before sink, so the def block and its critical PHI edge are the same as before.
- gen_bd265: attempt 10's brktail near miss (no asm, no t5le, no `*pr` expect) on the new case 23: 9 loose at best (`brk brk bar0`), worse than its old 3 with the badsize label, and `*pr == -1` tails don't help it (0/9 needs the label and asm).
- gen_bd266, lab_none: the console precheck spelled `<= 1`, `< 2`, signed forms, `== 1`, negated, as `goto none` or `return 0`, no cold label: 229 loose at best.
- gen_bd267, exp_verbose with pin_e: compare spellings with 0 (`size - e->size`, `^`, `- != 0`) fold back to `!=` (18 loose, as before); `e->size > size` or `size < e->size` with `verbose > 0` is 8 lines with or without the pin (`ja`/`jg` for `jne`/`je`, attempt 12's finding), so the source had `!=` and a plain test.

### Don't retry

- exp_t24 by a separate room test after the chain (gen_bd260), or by any spelling of `type == 25` (fold makes them all `==`, nonequal) or of the room test (`<` between non-constants has no heuristic).
- exp_devgl by the dev override as its own statement (gen_bd264), or by spellings of the dev test: all fold to `(t - 4) <= 1` (73%), `& ~1 == 4` would be nonequal 72%, two `==` 52%, a switch 50%; it needs 75.06%.
- exp_pr by `*pr == -1` or `(int)*pr < 0` (gen_bd263): the `*pr`-true edge must carry about 2%.
- The `(size & ~3) != size` spelling in loadConsoleBlFiles or appendAddonPatches (gen_bd262).
- lab_none by the precheck's spelling (gen_bd266).
- exp_verbose by spelling the size compare against 0 (gen_bd267).

### Costs now (strict/loose, removed alone; 16 tricks)

lab_t5le 7/0, exp_pr 18/2, exp_upd 18/12, pin_d 23/14, pin_e 26/26, exp_t24 29/7, exp_devgl 43/7, pin_size 82/40, exp_verbose 83/18, exp_t10 116/46, vol_fail 296/126, lab_none 333/231.  No pair is cheaper than its parts beyond the known exp_verbose+pin_e (18 loose) and lab_t5le+exp_pr (13/2).

### What to try next

- The opcode-heuristic lever (a spelling that makes the test a compare of two non-constants, or against 0/1/-1) on other objects' hints: it's cheap to sweep and it moved a 29-point gap here.  In build, every remaining expect and label has been checked against it.
- exp_devgl is the closest margin left (73% against 75.06%): any second predictor on the dev test in the non-dev direction would land it, if one turns up that the author could have written.
- exp_t24 needs a call-free block between `type == 25` and imgSize() that folds after profile_estimate, or 16% on the type == 25 edge.

## Attempt 16

Goal: the cheapest tricks first (exp_devgl's 2%, exp_t24's block frequency), stacking predictors rather than spelling one test, then IRA-side ideas for the pins.  Generators from gen_bd270.  Scratch in build/bd/a16 (not kept).

### Costs re-measured (src as of e76f027f)

Unchanged from attempt 15: lab_t5le 7/0, exp_pr 18/2, exp_upd 18/12, pin_d 23/14, pin_e 26/26, exp_t24 29/7, exp_devgl 43/7, pin_size 82/40, exp_verbose 83/18, exp_t10 116/46, vol_fail 296/126, lab_none 333/231.

### exp_devgl: the predictors that could reach the dev test (read from profile_estimate, `bddump.sh build/bd/a16/nodev.c buildFlash t-profile_estimate`)

- At profile_estimate buildFlash's start is bb2 (1148: `xb.type != 2`, nonequal 72%) -> bb3 (826: load, `_64 = _63 != 0`, `fuse_65 = (int) _64`, `_67 = t - 4; if (_67 <= 1)`, positive 27/73) -> bb4 (empty dev arm) -> bb5 (`fuse_9 = PHI <1(2), fuse_65(3), 1(4)>`).  The 3->5 edge is critical; sink splits it and moves the cast and the compare there.
- Every heuristic gcc 6 has for a two-way test, checked against that shape: opcode (one per test, 73% is the best a range test gets; `== 4 || == 5` 52%, a switch 50%), PRED_CALL (needs a call with side effects in a block the test dominates and that doesn't post-dominate it: neither arm has one, and bb5 post-dominates), early return / return-value predictors (no return there; a helper returning fuse gets none either, as return_prediction skips the constants 0 and 1), loop predictors (no loop), pointer (xb.type is an int), continue/goto (C front end: continue only).  So there is no second predictor to stack: the 2% can only come from a call in the dev arm, which nobody would write.
- sink's other refusals (single def, no side effects, `find_bb_for_arg` NULL when the value reaches the PHI on two edges, `commondom == frombb` when a use other than the PHI sits in bb3) all need fuse_65 to be used twice or reach the join twice; any natural form that does (a second override statement, `|=`) is merged back by ccp's bit tracking (`fuse | 1` with fuse in {0,1}) or by vrp1's JTAG thread before sink (gen_bd264).
- Verdict: stuck, not swept again.  Don't retry exp_devgl without a new kind of predictor.

### exp_t24: where the warning's 75 comes from, factor by factor (profile_estimate of build/bd/a16/not24.c)

- The round-2 threshold is 20% of the entry (431 at bbro), so the warning needs warning/entry >= 0.2; it has 0.174 and needs x1.16.
- warning/entry = (outer loop factor) x (path probability).  The loop factor is "guessed loop iterations" (94.7% on the latch, about 19 trips): estimated_stmt_executions from the `xb.files[i]` accesses, i.e. the files[19] bound, so it's fixed by the layout (files[20] or [21] change every xb offset; checked: nothing is IDENTICAL).  Written as pointer arithmetic it falls back to the 91% loop-exit predictor (fewer trips), the wrong way.
- The path: retail-skip join 3762 -> `xb.type > 5` (no heuristic, 50%) -> 1881 -> `type == 25` (nonequal 28% with PRED_CALL 29% from imgSize() in the next block: 13.7%) -> 258 -> room test (`<` between non-constants: none; PRED_CALL against the warning's log: 29%) -> 75.
- Every factor checked for a natural predictor: the `> 5` test would need PRED_CALL in the kit arm's first block (it starts with the 23/25 test); `type == 25` loses its PRED_CALL only with a call-free block in front of imgSize() (the expect's job; a real test there would stay in the code); the warning loses its PRED_CALL only if its block had a second predecessor or started with a test.  None exists.
- gen_bd270: the kit arm as `else if (xb.type > BUILD_DEVGL16 && (type == 23 || type == 25))`, the same shape as the retail arm, with the room test still in the chain (3 kit forms x 2 retail forms x 3 room forms): 27 loose at best (`and r p`); the kit path's not-23/25 flow is threaded past the type-25 test, but the retail path's copy of that test moves too.  Not close.
- Diagnostic only: `__builtin_expect(xb.seReplacesCf, 0|1)` (to move the competing findFile(14) exit block, 117) or a call in that arm: 99, 7 and 60 loose.  The competing block isn't the lever.

### pin_d through IRA (read from `-fdump-rtl-ira` of build/bd/a16/nopind.c, pin off)

- Case 27's tail is `r534 = r125 * 0x42c` (r125 = pretmp_80, the PRE'd nFlashFiles, 5 defs, one per fallback), `r535 = r534 + xb`, `d (r263) = [r535 + 0x422bc]`, size `r493 = [r535 + 0x422c0]`.  Shuffle copies cp3 (r534-r125) and cp4 (r535-r534) tie the base to n, but the pop order is r535 (base, eax: nothing assigned yet to prefer), r125 (edx, it conflicts with eax users elsewhere), r534 (eax, follows r535), then d (edx).  The reference is consistent with r125 popped first (edx), the base following it by the copies (`imul edx,edx`), and d taking eax.  The pin gets there by giving d eax outright.
- So removing it needs n's thread to outweigh the base's, or d's to outweigh the base's (d has one def and two uses in the same blocks as the base's three refs, so it can't by itself).
- gen_bd271: address spellings, `xb.files + xb.nFlashFiles` and `(xb.files + n)->` at the loadBaseFile calls, in the fallback arm and at the d/size reads (16 cases, pin off): every form that keeps `&xb.files[n]` in the fallback is the old 14 loose (GIMPLE normalizes the rest to the same ARRAY_REF); the pointer-plus fallback is 127.  Don't retry.

### exp_t10: what it places (bbro traces, `bdbbro.sh`, src against exp_t10 off)

- The only moved block is CG's checkBl copy (bbro block 14): 4 with the expect, 44 without, which lifts it into round 3 and lays it out before the passed log's setFlashBuild.  Round 4 orders by edge as well as block frequency (66 [23] comes before 51 [31]), so it needs roughly 22 or less: a factor of two on top of nonequal+call (13.7%) and the break's early return (61% to the goto).
- gen_bd272: the CG arm calling checkBl itself (`if (suGetCG(..)) *pr = checkBl(e->data, e->size, type|10, e->crc); break;`, or with `if (!suGetCG) break;` first), with and without the expect, which is the same behaviour (for type 10 everything after chk: is a no-op).  All 8 cases are the same 45 loose (85 strict with the displaced callers): the CG checkBl block lands in the right place, but the could-not-read log moves ahead of the patch code and CF/CG's checkBl argument setup crossjumps further than the reference's.  The expect makes no difference in that form, so the order of block 14 is no longer the issue there; what's left is the shared tail.  Not landed, and probably not the source: the reference's CG copy sets `[esp+8] = 10` and jumps into the CF/chk checkBl's shared argument setup, i.e. one checkBl call reached by `goto chk` with the 10 threaded in; two calls crossjump deeper than that.  Also on src, exp_t10 off: the CG arm falling through to chk with no goto (`c7`) 52 loose in loadBlFiles (it moves .rdata), the same with the expect kept 116, `if (suGetCG(..)) goto chk; break;` 46 (as plain).

### exp_upd: einline's refusal re-read

- `bddump.sh build/bd/a16/noupd.c addUpdateBls i-einline` (no expect): "growth 10 exceeds --param early-inlining-insns divided by number of calls", body size 13 as four OR blocks.  The second einline test fires, so something counts as a call in a callee that has none in the dump; the official ipa-inline.c is still behind the bot wall (fetched again this attempt), so the reason stays unchecked.  Nothing swept.

### Don't retry (attempt 16)

- exp_devgl by any shape that keeps the setne in the non-JTAG block without a call in the dev arm: no gcc 6 heuristic is left to stack (see above).
- exp_t24 by the kit arm as `xb.type > BUILD_DEVGL16 && (type == 23 || type == 25)` in the chain (gen_bd270), by the files bound (layout), or by moving the seReplacesCf block.
- pin_d by address spellings (gen_bd271).
- exp_t10 by CG calling checkBl itself (gen_bd272) or falling through to chk.

### Costs now (strict/loose, removed alone; 16 tricks, unchanged)

lab_t5le 7/0, exp_pr 18/2, exp_upd 18/12, pin_d 23/14, pin_e 26/26, exp_t24 29/7, exp_devgl 43/7, pin_size 82/40, exp_verbose 83/18, exp_t10 116/46, vol_fail 296/126, lab_none 333/231.

### What to try next

- Every expect and label left in build is now accounted for as "a predictor gcc 6 doesn't have in natural code" (exp_devgl, exp_t24, exp_t10, exp_pr, exp_verbose, exp_upd, t5le, none) or an IRA/PRE tie (the pins).  The one lead with something left to read: exp_upd's einline refusal ("divided by number of calls" for a callee with no calls).  If the official ipa-inline.c at releases/gcc-6.2.0 can be read, find what num_calls counts; an isUpdateBl that einline takes brings addUpdateBls' loop predictors to the `(23|15)` test.
- Otherwise park build at 16, as attempt 14 suggested at 17.
