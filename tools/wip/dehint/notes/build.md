# build de-tricking

Goal: `build/bd/reference.o` (copy of a matching build/obj/build.o) byte-identical from plain
`-O3`, with fewer hints.  52 tricks at the start of attempt 1.

## State after attempt 3

26 tricks: `--param builtin-expect-probability=98`, 10 `__builtin_expect`, 6 pins, the empty
`__asm__ __volatile__("")` barrier at loadBl's `fail:`, 4 hot and cold labels, no `cb_hint()`,
2 `__builtin_constant_p`, 2 `no-early-inlining` (checkBl, patchBlsBlmod). (After attempt 2: 43, with 18 expects, 7 pins,
6 labels, 5 cb_hint and 3 no-early-inlining. After attempt 1: 50.)

Landed shapes to review:

| Where | Shape | Why it's borderline |
|---|---|---|
| patchCpuFan and its caller | The cpu fan section as a function, with `xb.cpuFan != 0xffffffff` tested in both | The repeat is redundant, folded after inlining, and only there for what it does to frequencies. It replaces no-early-inlining on patchSmcConfig and 4 cb_hint. The function alone is natural |
| checkBl, blMagic | `blMagic(bl, &m)` where `m = bl[0]` would do | An out parameter so the call has side effects, for PRED_CALL. It replaces cb_hint |
| checkBl, 7 arms | `if (!crcSame(c, crc)) { log; return -2; }`, the same log 7 times, with `goto bad` kept for type 14 and default | crcSame only hides the compare from the predictor while no-early-inlining holds. It replaces 7 expects |
| checkBl | `goto toobig`, with the size error's text after the crc error's | Text order only, for .rdata. Plain `if (blsize <= size) { ... }` nesting matches too |
| loadBl case 24 (first arm), loadConsoleBlFiles case 24 | `if (loadBaseFile(..)) r = defaultBl60(e); else if (e->size != 0x60) r = defaultBl60(e);` | Two identical calls where `\|\|` would do; crossjump merging them is what orders the size store. The second arm of loadBl's case 24 uses `\|\|`, so the two arms differ for no visible reason |

Not borderline, but they steer, so check them: the struct copy in extractSmcConfig, `findSmcConfig`, `int size` on extractSmcConfig and `int crc` on loadInputFile (comments in
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
