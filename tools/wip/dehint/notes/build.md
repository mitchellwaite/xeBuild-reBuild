# build de-tricking

Goal: `build/bd/reference.o` (copy of a matching build/obj/build.o) byte-identical from plain
`-O3`, with fewer hints.  52 tricks at the start of attempt 1.

## State after attempt 31

Attempt 31 landed nothing; src/build.c and build.sh are unchanged, so the count (12) and the review tables stand.  It took attempt 30's vol_fail near miss (the size log's own -1, 1 loose / 7 strict) through both routes attempt 30 named, and closed them.  (a) Block order can't help: crossjump tries each pred against the log's fallthru predecessor first, so every wholly matched -1 block merges into the fallthru one before the size log could be the 'to' side, and the split -1 blocks always take the fallthru place (rtl_split_edge puts them before the log and force_nonfallthru()s the old one; a diagnostic with case 23 last still has its own -1).  (b) A split needs the size path's last block to end in a test that is gone from the final code, and only a dead test does that.  Case 23's spellings (own -1, return, nested, good path first, `e->size & 3`) and case 2's `{ fail: }` block don't move the line (gen_bd430).  See "## Attempt 31".

## State after attempt 30

Attempt 30 landed nothing; src/build.c and build.sh are unchanged, so the count (12) and the review tables stand.  It rebuilt loadBl from scratch with all seven of its hints off together and scored the forms hint-free: result through `*pr` or a returned / stored local, fallback, fail's position, the signature block's form, position (after the switch: 220 and up) and a helper for it, case order, case 6 falling into the 5..21 arm.  The best hint-free forms are 67 to 89 loose against src minus hints' 165, but that is attempts 25/26's and9 + c2 reshaping; none removes a hint once the others go back (a returned local leaves 8 loose with every hint, no key first 10), and `else if (type)` is the largest single item hint-free (the verify test is 50/50 by PRED_CALL on both arms and bb-reorder's tie takes the failed log).  New near miss: **on and9 + c2 + case 6 first the barrier costs 1 loose / 7 strict** (drafts/build_loadBl_c6_nobarrier_nearmiss.patch): only the size log's own -1, which jump2 can't crossjump with the shared -1 block because the size log's block is lower in the chain and not wholly matched.  The pins didn't move (pin_d is 14 on every case order).  Sweeps gen_bd410 to gen_bd423.  See "## Attempt 30".

## State after attempt 29

Attempt 29 landed nothing; src/build.c and build.sh are unchanged, so the count (12) and the review tables stand.  It tested attempt 28's route for exp_t10: take PRED_TREE_EARLY_RETURN off the CG failure and the other types' `else break`.  predict.c skips that predictor only for an edge that reaches the return block through a non-empty block laid out right before it (fail holds that place now).  A diagnostic with a new asm block there confirms attempt 28's arithmetic exactly: block 116 drops to 94 (CG failure only), 90 (else only), and under 88 with both (no copy of 117; drafts/build_loadBl_t10_noearly_diag.patch, diagnostic only).  No natural form gets there.  Joining the failures at checkBl's result test moves the whole tail (159 loose and up, gen_bd400).  Using the existing barrier as that block breaks its -1 block (88 and up, gen_bd402).  The fallback's failures can't be the last code in loadBl.  So exp_t10 stays, and t5le with it.  Sweeps gen_bd400 to gen_bd402.  See "## Attempt 29".

## State after attempt 28

Attempt 28 landed nothing; src/build.c and build.sh are unchanged, so the count (12) and the review tables stand.  It took attempt 27's exp_t10 near miss apart: the copied block 116 is vrp1's shared thread copy of chk for the type-9 non-SE and CG edges, **116 = 0.2576 x (load-ok + CFok) + CGok = 66.2 + 5.5 + 27** (threshold 88), and a diagnostic word compare for the SE test (SE 28% instead of 7.8%) removes the copy and leaves only that compare (5 loose, every other function matching), with **lab_t5le then free** and exp_pr one line (drafts/build_loadBl_t10_u16_diag.patch).  But every factor is fixed by gcc 6's heuristics in this structure (nonequal on the SE and type tests, no predictor on the load test, early returns on CG's breaks; CG's own checkBl crossjumps with case 6, 83 loose; the log inside loadBl, 95), and threading conserves flow, so repeated tests can't drain it.  Sweeps gen_bd390 to gen_bd394; new tools bddup.py and bdblocks.py.  See "## Attempt 28".

## State after attempt 27

Attempt 27 landed nothing; src/build.c and build.sh are unchanged, so the count (12) and the review tables stand.  New: exp_t10 is two bbro effects, read from the dumps: the CG flow that vrp1 threads into chk with type 10 known cools the shared copy's type-11 block (22 -> 18, it loses a round-4 tie and moves), and it pushes the merged checkBl call block over the duplication threshold (99 against 88, so bbro copies the `if (r)` test into it).  The first is fixed by the __builtin_constant_p entry's weight (`.. && __builtin_constant_p(type) == 1`), which on src leaves only the copy: **2 loose / 53 strict** (drafts/build_loadBl_t10_weight_nearmiss.patch; the expect moved to the CG success test is IDENTICAL, so the hint is about CG's success flow).  exp_pr through the return predictor (PRED_NEGATIVE_RETURN, 4%) is closed: it also flips the size and smc tests.  On the c2 base exp_pr costs two alignments, not one.  Sweeps gen_bd380 to gen_bd384.  See "## Attempt 27".

## State after attempt 26

Attempt 26 landed nothing; src/build.c and build.sh are unchanged, so the count (12) and the review tables stand.  It read why the barrier works on the and9 base: the asm keeps `fail` through mergephi2/3, and PRE's tail merge then joins the smc and signature-copy forwarders into a PHI block in front of it, which together give the reference's single -1 block (33d4).  Without the asm no shape keeps a block there: mergephi removes it if it has a PHI, cleanup if it hasn't (no -1 source also reaches the log with another r), and crossjump can't merge the size log's -1 (its block is always the lower one).  New: fail placed at the end of case 2 (`if (e->offset) break; fail: *pr = -1; break;`, so the smc test falls into it) is IDENTICAL with the barrier and drops the barrier's cost from 60 to 9 loose on and9 (t5le is then free; drafts/build_loadBl_c2_fail.patch), and on it exp_pr costs only one alignment (14 strict, 0 loose).  Sweeps gen_bd370 to gen_bd374.  See "## Attempt 26".

## State after attempt 25

Attempt 25 landed nothing; src/build.c and build.sh are unchanged, so the count (12) and the review tables stand.  It tried attempt 24's lever (an extra predecessor at profile_estimate that vrp1 threads away) on exp_devgl, lab_none and loadBl's tail.  exp_devgl: bb3 (def + dev test) has only the entry's JTAG test before it, so no thread through it can know devgl, and sink's 3->5 edge is always critical.  lab_none: r = 1 can't pass the not-entered return without the glitch test reaching 34% (has 29%, PRED_CALL), and its trace-priority route is shut.  New: the and9 family of the update fallback (`if (type == 9 && CF) ; else if (type == 10 && CG) goto chk; else break;` and spellings, gen_bd360 to gen_bd362) is IDENTICAL with the expect and 28 loose without it (src 46), halves vol_fail (60 against 126) and widens the param window to p = 94 to 98; but exp_t10's measured window is <= 6% on the CG edge against the natural 19.9%, so the expect stays (drafts/build_loadBl_and9_fallback.patch).  See "## Attempt 25".

## State after attempt 24

**12 tricks** (13 before): `--param builtin-expect-probability=98`, 3 `__builtin_expect` (type == 10, `*pr != 0`, devgl), 2 pins (d, size), the empty asm barrier, 2 hot and cold labels (t5le, none), 2 `__builtin_constant_p`, 1 dead test (`else if (type)`).  exp_t24 is gone: addBlsToImage's kit test sits in the else-if chain like the retail one (`else if (xb.type > BUILD_DEVGL16 && (type == 25 || type == 23))`, attempt 16's gen_bd270 shape), so the kit path's other types pass through the xell room test at profile_estimate and the warning gets the frequency it needs; with 25 first, vrp1's first assert on the kit-false edge is `type != 25`, so the threader takes that path past the room test afterwards (with 23 first it can't: 63 loose).  IDENTICAL BYTES, full build SHA256 matches.  addBlsToImage is now param-independent; the object still matches at p = 96, 98, 99 only (loadBlFiles), so the param stays at 98.  See "## Attempt 24".  New borderline shape, marked in src:

| Where | Shape | Why it's borderline |
|---|---|---|
| addBlsToImage's skip tests | `(type == 25 \|\| type == 23)` in both the retail and the kit test | Live and not redundant, but the order is chosen for what gcc does with it: vrp1's threader only sees the first leaf's `!=` assert on the kit test's false edge |

## State after attempt 23

**13 tricks** (14 before): `--param builtin-expect-probability=98`, 4 `__builtin_expect` (type == 10, `*pr != 0`, type != 24, devgl), 2 pins (d, size), the empty asm barrier, 2 hot and cold labels (t5le, none), 2 `__builtin_constant_p`, 1 dead test (`else if (type)`).  exp_upd is gone: isUpdateBl tests 23 and 15 as ifs of their own before the `||` group (gen_bd341, gen_bd342), so the lone `type == 23` gets nonequal + early return (19.9%, inside attempt 22's <= 28% window) at profile_estimate, and ifcombine pairs the two lone tests into the same `(23|15)` OR after inlining, whose `type == 23` the loop body reuses.  IDENTICAL BYTES, full build SHA256 matches.  addUpdateBls is now param-independent; the object still matches at p = 96, 98, 99 only (loadBl's expects), so the param stays at 98.  See "## Attempt 23".  New borderline shape, marked in src:

| Where | Shape | Why it's borderline |
|---|---|---|
| isUpdateBl | `if (type == 23) return 1; if (type == 15) return 1; return type == 16 \|\| ..;` | Live and not redundant, but splits the devkit CF (15) from its CG (16) and is chosen for what gcc does with it: the lone tests get a predictor the folded `\|\|` pair doesn't, and ifcombine re-pairs them |

## State after attempt 22

Attempt 22 landed nothing; src/build.c and build.sh are unchanged, so the count (14) and the review tables stand.  It tried attempt 20's lever on exp_t24, exp_devgl, exp_upd and lab_none and found no thread-made path in any of them: the blocks the hints fix all exist at profile_estimate, and the missing piece is a predictor.  New: the real windows, measured by varying `builtin-expect-probability` with each function's single expect (tools/wip/dehint/bdpwin.py): exp_t24's middle block needs >= 77% (the warning must beat the seReplacesCf exit block's 117, not reach 87: x1.57 from the natural 75); exp_devgl 75% (attempt 15's margin, confirmed); exp_upd P23 <= 28% (not 23.8%): exactly the nonequal heuristic, which the `(23|15)` OR of bools doesn't get.  lab_none: the case-24 `||` form raises r = 1 from 14 to 18 of the 21 needed and moves the size store (gen_bd331, 6/10).  See "## Attempt 22".

## State after attempt 21

Attempt 21 landed nothing; src/build.c and build.sh are unchanged, so the count (14) and the review tables stand.  It tried attempt 20's lever (repeat the deciding test so the path exists at profile_estimate) on loadBl's tail and found it doesn't carry over: the tail's paths are split by the caller's `if (r)` after inlining, so a `*pr` re-test inside loadBl only makes new tests with their own wrong probabilities (gen_bd320; diagnostics gen_bd321 show they'd need about 2% and over 50%).  Also measured: attempt 11's kit-first tail (4 loose) is a code-size coincidence (the alignments dump is the same as src minus t5le) plus a PHI-order effect that sends dom2's FSM thread past setFlashBuild (gen_bd322); the could-not-read log inside loadBl (gen_bd323, 95 loose), a plain else with either verify polarity (gen_bd324, 50 and up: bb-reorder's 50/50 tie or .rdata), the SE path with its own checkBl (gen_bd325, 40).  See "## Attempt 21".

## State after attempt 20

**14 tricks** (16 before): `--param builtin-expect-probability=98`, 5 `__builtin_expect` (type == 10, `*pr != 0`, type != 24, isUpdateBl, devgl), 2 pins (d, size), the empty asm barrier, 2 hot and cold labels (t5le, none), 2 `__builtin_constant_p`, 1 dead test (`else if (type)`).  loadFileCrc's exp_verbose and pin_e are gone: the log choice repeats the pad test, `if (pad && (size & 15) && size != e->size) pad log; else bytes log;` inside `if (verbose)` (gen_bd315, gen_bd316), which gives the non-pad path its own edge to the bytes log at profile_estimate (bytes log 3220, round 2) instead of a later thread (1102).  IDENTICAL BYTES, full build SHA256 matches.  pin_size (gen_bd310 to gen_bd312, whole-function forms) and pin_d (gen_bd317, lifetime and scope) didn't move.  See "## Attempt 20".  New borderline shape, marked in src:

| Where | Shape | Why it's borderline |
|---|---|---|
| loadFileCrc's verbose block | `if (pad && (size & 15) && size != e->size)` picks the pad log | The pad condition is computed twice (once for the store, once for the log), and `size != e->size` can't be false once it holds.  Live, reads naturally; chosen because the repeat creates the non-pad path before branch prediction |

## State after attempt 19

Attempt 19 landed nothing; src/build.c and build.sh are unchanged, so the count (16) and attempt 15's review table stand.  It followed attempt 18's lead, t5le through S / Xc, and closed it: at profile_estimate S / Xc = Psig x Pk x Pf, and in natural code each factor takes only fixed values (Psig 64%: fold packs at most two of the 5/17/11 compares into one 50% block, the third gets nonequal; Pk 85%: the pointer heuristic; Pf 29% or 50%: the verify must stay a zero test, so only PRED_CALL moves it), giving 15.8% (src) or 27.2% (plain else, which moves the failed log) where t5le needs 21.6% with the failed log still under bb-reorder's last-round threshold.  The SE copy's frequency (t5le's other factor) can't be lowered either: threading re-splits the `type == 9` test from its total, so the SE block stays 6 even with the CF path at 2% (diagnostic).  Sweeps gen_bd300 (diagnostics) and gen_bd301 (failed-arm spellings): nothing better than src.  See "## Attempt 19".

## State after attempt 18

Attempt 18 landed nothing; src/build.c and build.sh are unchanged, so the count (16) and attempt 15's review table stand.  New: all 220 triples of hints are additive; t5le and exp_pr have a closed form from vrp1's joiner counts (the SE copy's P(<=5) = Xc p (1 - q) / (Xc - S), the signature-failed copy's = Xc p q / S, checked to the digit against the dumps), which says t5le needs p >= 54% or the signature-failed share S / Xc >= 21.6% (15.6%), and exp_pr needs p q <= 3.7%; and defaultBl60 is late inlined (not early, as attempt 17 had it), so lab_none's r = 1 comes from its own profile and can at best tie.  Sweeps gen_bd290 to gen_bd294 (lone `type == 23`, stacked `*pr` tests, a result test for `else if (type)`, defaultBl60 forms, signature-block forms): none better than src.  See "## Attempt 18".

## State after attempt 17

Attempt 17 landed nothing; src/build.c and build.sh are unchanged, so the count (16) and attempt 15's review table stand.  It settled exp_upd's einline refusal: fnsplit has already split isUpdateBl (isUpdateBl.part.N holds the tail tests), and that call is the "number of calls" (growth 10 x 2 > 14).  Early inlining (forced, or naturally with a `uint32_t` return) gets the head right but costs 177 strict with or without the expect, because the inlined pairs lose isUpdateBl's early-return 39% and the bit test goes to 50%; so the lead is dead.  Sweeps gen_bd280 to gen_bd284 (isUpdateBl bodies, types, range-folded pair orders; defaultBl60 forms for lab_none; calcBlAreaSize locals for pin_size): none better than src.  See "## Attempt 17".

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

## Attempt 17

Goal: settle exp_upd's einline refusal by experiment, then the cheapest others.  Generators from gen_bd280.  Scratch in build/bd/a17 (not kept; `sx.py` there is bdlib with extra gcc flags).  `bdrun.py` now takes `BDEXTRA="flags"` for diagnostic runs (never for a landing).

### exp_upd: why einline refuses isUpdateBl (settled by experiment, dumps only)

- **fnsplit has already split isUpdateBl when einline looks at it.**  Early local passes run callees first, and pass_split_functions runs after einline in each function's early pipeline, so by the time addUpdateBls is early-inlined, isUpdateBl is `header + call isUpdateBl.part.3 (type)` (`bddump.sh build/bd/a17/noupd.c isUpdateBl t-fnsplit`: "Split point at BB 4 .. New best split point", BB4 being the `(10|24)` block, split size 7; the header keeps `(23|15)` and `(16|9)`).  That call is the one call einline counts.
- Measured with `--param early-inlining-insns=N` (diagnostic): N <= 9 "growth 10 exceeds --param early-inlining-insns"; 10..19 "... divided by number of calls"; 20 and up inlined.  So the rule is growth * (n + 1) > N with n = 1.  Toy files (build/bd/a17/t/t1..t6.c) agree: a call-free 7-test `||` chain gets n = 1 (split), a callee with two real calls n = 2, and a 4-test chain (growth 5) or a static callee called once (fnsplit: "not called directly or called once") is inlined.  So attempt 3's "growth * (calls in it + 1)" is right, but the calls include fnsplit's part call.
- isUpdateBl must stay global: the exe is stripped, nothing calls 0x42c600, and the offline copy exists, which only an externally visible function gives.  `static` would let einline take it (not split) but delete the offline body.  Its position is fixed by -fno-toplevel-reorder.
- **Inlining it early doesn't make the expect redundant, and doesn't match.**  With `-fno-partial-inlining` (or early-inlining-insns=20; both diagnostic) isUpdateBl is early inlined and the head comes out right (`cmp 23; je`, mask 0x3018600: FRE still reuses the pair's `type == 23`), but addUpdateBls is 177 strict / 100 loose, *with or without the expect*.  Read from the .optimized and bbro dumps (build/bd/a17/opt_src.txt, opt_np.txt): the merged bit test (the `(16|9)` pair's block after reassoc) is 39% to the body in src, from isUpdateBl's own early-return predictor, and 50% once inlined early, because an inlined pair's true edge goes to an `iftmp = 1` block (no return, no call, `_5 != 0` gets no opcode heuristic).  At 39% bb-reorder ends trace 1 at the bit test (6 -> 45, the latch, wins) and rotates loop 4-45; at 50% the trace runs on into the body (6 -> 47) and the whole loop is laid out rotated from the 16/24 block.  So the late inline's early-return 39% is needed on the bit test, and the expect (or something like it) on the first pair; early inlining loses the first and doesn't help the second.
- gen_bd280 (isUpdateBl forms that can't be split: `|` with or without parens, `r |=` statements, a flag, separate `if .. return 1`, switch, in 5 orders, no expect): `|` forms are early inlined, isUpdateBl itself matches, but 23 joins the loop's mask (one statement chain, no reusable compare): 214 loose and up.  `if` forms 78 and up, switch 281.  Only the `||` chain in src's or the 15-first order is the old 12 loose.
- gen_bd282 (isUpdateBl's parameter type x return type x addUpdateBls' `type` local, no expect, 80 cases): int, long, uint32_t parameters are the old 12 loose; narrow parameter types 226.  **A `uint32_t` (or `_Bool`, `uint8_t`) return is early inlined naturally**: fnsplit refuses it ("incoming frequency is too large" at both points, so its pairs don't get the int return's early-return 39%), einline takes it (n = 0), and addUpdateBls is the same 177/102 as the forced runs above.  So a natural early-inlined isUpdateBl exists, and it confirms the 50% problem rather than escaping it.
- gen_bd284 (late inlining kept; a first pair of adjacent constants, which fold makes a range test `(unsigned)(type - c) <= 1` with the opcode-positive heuristic, 27% x early return = 19.1%; 6 first pairs x 120 orders of the rest): best 12 loose, the same 12 as src without the expect (`15 16 23 ..`).  Read from isUpdateBl's profile_estimate: fold pairs the range with the *next* test as well, so `15 || 16 || 23` is one block `range | (type == 23)` with early return only (39%), and the later adjacent pairs become the 19.1% ranges.  A pair holding 23's compare (needed for FRE's reuse) is always an OR of two bools with no opcode heuristic, and 23 paired with 24 becomes a range with no `type == 23` to reuse.
- Verdict: exp_upd's lead is dead.  Early inlining, by any route, gives 50% where 39% is needed; late inlining fixes 39% but leaves the first pair at 39% where < 23.8% is needed (attempt 8), and no predictor is left for it in isUpdateBl's own body.

### lab_none and pin_size: two quick new axes, nothing

- gen_bd281, lab_none: with the precheck and label gone, the plain `for` is the old 4 loose / 8 strict, and the two swapped blocks are both round-4 traces with no priority (bbro keys -20 for the not-entered `return 0`, -14 for the inlined defaultBl60's `r = 1`), so whichever has the higher frequency goes first.  defaultBl60 is early inlined into every caller (no profile of its own), so its form (positive test, result variable, `!= NULL`, 6 forms) gives the same GIMPLE after inlining: all IDENTICAL with the label, all 4/8 without.  The 14 is the inlined malloc-null test's pointer heuristic, and the 20 the header copy's 5.3% (files[19] loop bound); neither has a natural lever left.
- gen_bd283, pin_size: x's type (findFile returns int), x scoped per arm, xs scoped in its block, size's type (36 cases, pin off): uint32_t/unsigned x is the old 40 loose in every scope; int x 78, int size 135.  Scoping doesn't move PRE's names.

### Don't retry (attempt 17)

- exp_upd through early inlining, by any route (`static`, which also deletes the offline copy the exe has; a non-int return; forms fnsplit can't split; the param or -fno-partial-inlining as diagnostics): the inlined pairs lose the early return, the bit test goes to 50% and the loop is laid out rotated (177 strict).  The lead from attempts 13 and 16 is closed.
- exp_upd by isUpdateBl's parameter, return or local types (gen_bd282), by `|`, `|=`, flag, `if`-chain or switch bodies (gen_bd280), or by range-folded first pairs in any order (gen_bd284).
- lab_none by defaultBl60's form (gen_bd281): it's early inlined everywhere, so every form is the same GIMPLE.
- pin_size by scoped or retyped locals (gen_bd283).

### Costs now (strict/loose, removed alone; 16 tricks, unchanged)

lab_t5le 7/0, exp_pr 18/2, exp_upd 18/12, pin_d 23/14, pin_e 26/26, exp_t24 29/7, exp_devgl 43/7, pin_size 82/40, exp_verbose 83/18, exp_t10 116/46, vol_fail 296/126, lab_none 333/231.

### What to try next

- Nothing in build has real odds left by the methods used so far: every expect and label is a missing gcc 6 predictor in natural code, and the pins are IRA/PRE ties (attempts 14 to 17).  Park build at 16.
- The one question not asked by experiment: could addUpdateBls' body (not isUpdateBl) be laid out right at the early-inlined probabilities, now that a natural early-inlined isUpdateBl exists (the `uint32_t` return, gen_bd282)?  Its diff is pure layout (the 16/24 block placed before the latch).  Probably not: the bit test's 50% is set on the pairs' edges at profile_estimate, whose true successor is the inlined `iftmp` join (no statements a predictor reads), so nothing in the body reaches it; and at 50/50 bb-reorder's better_edge_p (from memory, not checked against the 6.2.0 source) falls back to the destination's frequency, lower is better, and then block order, and both favour the body (47 [7941]) over the header-latch (45 [8725]).  If someone checks, read bb-reorder.c's better_edge_p and find_traces_1_round from the official repo first, then run body forms with `BDEXTRA=-fno-partial-inlining`.
- The bdrun `BDEXTRA` variable is for such diagnostics only.

## Attempt 18

Goal: the tricks closest to matching (t5le, exp_pr, lab_none, exp_upd from the body side), with borderline but natural shapes considered more readily.  Generators from gen_bd290.  Scratch in build/bd/a18 (not kept; `triples.py` there scores every k-subset of bdhints).

### Costs re-measured (src as of 8b56de61)

Singles unchanged: lab_t5le 7/0, exp_pr 18/2, exp_upd 18/12, pin_d 23/14, pin_e 26/26, exp_t24 29/7, exp_devgl 43/7, pin_size 82/40, exp_verbose 83/18, exp_t10 116/46, vol_fail 296/126, lab_none 333/231.  **All 220 triples** (new): each is the sum of its parts; the cheapest are exp_pr+lab_t5le+x (9 loose and up).  No triple opens anything a pair didn't.

### exp_upd: a lone `type == 23` first block (gen_bd290, three hand runs)

- fold_truth_andor only makes `a || b` into `a | b` when both are simple compares, so a parenthesized group of three or more (`type == 23 || (type == 15 || type == 16 || type == 9) || ..`) keeps `type == 23` as a block of its own, which would get nonequal + early return (19.9%, under the 23.8% rotate_loop needs).  A group of two is a range test (simple) and merges back: `23 || (15 || 16)` is one block `(type == 23) | range` at 39%, the old 12 loose.
- But a lone `if (type == 23)` is a GIMPLE_COND with no SSA bool, so nothing in addUpdateBls' body can reuse it, and reassoc merges 23 into the mask (0x3818600): 226 to 267 loose for three groupings.  This is attempt 8's rule from the other side: 23 must sit in a pair, as an SSA bool, and then it's 39%.  The full sweep wasn't run; gen_bd290 is kept for the record.

### t5le and exp_pr: the joiner arithmetic, closed form (read from vrp1 and profile_estimate dumps, `build/bd/a18/vrp1_not5.txt`)

- t5le's 7 lines, exactly (`-fdump-rtl-alignments` of src with the label off): the no-key log copy (final bb 112, freq 17) is aligned only when its layout predecessor, fixup_reorder_chain's jmp block after the SE copy (bb 111), has freq <= 1 (`17 > 10 x prev`).  bb 111 is EDGE_FREQUENCY(SE copy -> setFlashBuild) = 4 x 42.04% = 1.68 -> 2.  So t5le needs P(<=5) on the SE copy > 62.5% (has 57.96%), or the SE copy's freq 3 (has 4: SE block 6 -> checkBl's 61% -> 3.66), or the no-key log >= 21.
- vrp1 makes two joiner copies of the `xb.type <= 5` test X: one for the signature-failed edge (S = 29 at vrp1, `*pr` = -1, threads through T = `if (*pr)` to fail) and one for the four `*pr` = 0 edges (157).  With Xc = S + 157 = 186, base p = P(X <= 5) and q = P(T -> fail), tree-ssa-threadupdate.c's path counts give (sig copy first, then the other, checked against both dumps to the digit):
  - sig copy: P(<=5) = Xc p q / S = 6.41 p q (src: 0.85 x 0.02 -> 6.41%, final bb 102's 641);
  - other copy (it becomes the SE copy): P(<=5) = Xc p (1 - q) / (Xc - S) (label off: 186 x 0.5 x 0.98 / 157 = 58.0%; label on: 98.7%, the 9869 in the dump).
- So t5le needs p (1 - q) >= 0.528, i.e. p >= 54% with q = 2%; at p = 50% (no heuristic: X's arms hold no call and neither goes straight to the return block) no q helps.  exp_pr needs the sig copy's P(<=5) <= about 24% (so its setFlashBuild copy keeps freq >= 3 and the type-11 block after it isn't aligned): p q <= 3.7%.  Natural spellings give q = 28% at best (37.8% with the break's early return).
- The other lever in the formula is S / Xc (15.6%): with q = 2% and p = 50%, S / Xc >= 21.6% lands t5le.  S is the verify-failed share: (5|17) 50%, 11 28%, pub1bl 85%, verify-failed 29% (PRED_CALL on the failed log; the dead `else if (type)` keeps PRED_CALL off the passed arm).  Diagnostic (a dead `if (type)` before the failed log, so 50%: build/bd/a18/diag_s.py): S doubles, the signature-failed log becomes hot and moves (72 loose with t5le off, 48 with t5le and exp_pr off).  So S has a window; not pursued further.
- Why X gets no heuristic, read from predict.c's early-return rule (tree_estimate_probability_bb, from memory, consistent with every number above): an edge is predicted not taken when its destination is the return block (and isn't next_bb), or when its destination's single successor is.  X's arms are T and the type == 14 test, neither of which is; T's break edge is, which is why q is pushed up to 61% (not down).

### Sweeps (gen_bd291 to gen_bd293)

- gen_bd291, exp_pr: two or three redundant tests of `*pr` chained (`(int)*pr < 0`, `*pr == -1`, `*pr != 0`, nested or `&&`; they thread away, *pr being known on each path).  `&&` folds back to one test; nested ones do stack at profile_estimate (36.6% x 37.8% = 13.8% for `< 0` then `== -1`) but every two-test form is the old 0/9 with the label and 2/13 without; three nested tests break `fail` (44 loose).  13.8% is far from 2%, and the shape is code nobody writes.  Don't retry.
- gen_bd292, `else if (type)`: the passed log guarded by a result test instead (`if (!*pr)` after the verify, a local `ok`, the passed arm first, `else if (!*pr)`), with t5le and the `*pr` expect on or off: 56 loose at best (`else if (!*pr)`, which is as dead as `else if (type)`, since `*pr` is 0 there); the live forms 82 and up.  Don't retry.
- gen_bd293, lab_none: **defaultBl60 is not early inlined** (attempt 17 said it was): loadConsoleBlFiles calls `defaultBl60.isra.0` at profile_estimate and IPA inlines it late, so r = 1's frequency is defaultBl60's own NULL probability (pointer 15% with the early return's 39%: 10.1%) x the two call sites (136): 14 against the not-entered return's 20.  Even without the early return it would be 15% -> 20, a tie.  Seven defaultBl60 forms (positive test, result variable both ways, else, `return e->data == NULL`, `!e->data`) x case 24 with two calls or `||` x precheck kept or not: the first four are the same CFG (IDENTICAL with the label, 4/8 without), the return-value forms 280 and up.  defaultBl60 is shared with loadBl, so its profile also moves loadBlFiles (a diagnostic expect on its NULL test costs loadBlFiles 26 to 300).  Don't retry lab_none through defaultBl60.
- gen_bd294, t5le through S: the signature block's natural variants with t5le off (6 orders of `type == 5 || 17 || 11`, pub1bl test either polarity, verify test either polarity, `else if (type)` or plain else; 48 cases).  Only src's form is the old 0/7; other type orders change the compare order (4 loose, and the alignment is still missing), the negated pub1bl test moves .rdata (50 and up), a plain else 50 and up.  None moves S into the window.  Don't retry.

### exp_upd from the body side (target 4): looked at, not swept

- The natural early-inlined isUpdateBl (`uint32_t` return, attempt 17) is 177 strict / 102 loose with or without the expect; its diff (`build/bd/a18/ei.c`) is four chunks moved (the 16/24 tail, the imgCfOffset block, the epilogue, `cmp esi,eax` for `cmp eax,esi`), not one placement, so no single body form would close it.  better_edge_p wasn't read.  With late inlining, rotate_loop (bb-reorder.c, from memory) picks the hottest edge leaving the loop's trace: the 23 test's edge to the body (P23 x 8725) must lose to the bit test's (8551 x 50% x 39%), i.e. P23 < 16.3% on the trace's frequencies (attempt 8's 23.8% was measured on another base); the expect gives 2%, a lone `==` would give 19.9%, and the pair gives 39%.

### Don't retry (attempt 18)

- Triples of hints off (all 220 are additive).
- exp_upd by a lone `type == 23` first block (gen_bd290's idea): 23 then merges into the mask.
- exp_pr by stacked redundant `*pr` tests (gen_bd291).
- `else if (type)` by a result test after the verify (gen_bd292).
- lab_none through defaultBl60's form or NULL probability (gen_bd293): it's late inlined and shared with loadBl.
- t5le through the signature block's forms (gen_bd294), or by raising the verify-failed share with a dead test (diag_s: the failed log moves).

### Costs now (strict/loose, removed alone; 16 tricks, unchanged)

lab_t5le 7/0, exp_pr 18/2, exp_upd 18/12, pin_d 23/14, pin_e 26/26, exp_t24 29/7, exp_devgl 43/7, pin_size 82/40, exp_verbose 83/18, exp_t10 116/46, vol_fail 296/126, lab_none 333/231 (4/8 with the precheck gone too).

### What to try next

- t5le has a closed form now: the SE copy's P(<=5) = Xc p (1 - q) / (Xc - S).  The only term not yet moved by a natural shape is S / Xc (needs 15.6% -> 21.6% with nothing else hot enough to move).  A natural way to make the verify-failed path somewhat likelier (not 50%), or the non-signature flow into the tail somewhat smaller, is the one untested lever; check any candidate first with `bddump.sh f loadBlFiles alignments` (bb 111's freq must be <= 1) before scoring.
- The same formula says exp_pr needs p q <= 3.7%; with p near 50% that's q <= 7%, far below any natural predictor.  exp_pr only goes with a different tail.
- Otherwise build stays parked at 16, as attempts 14 to 17 said.

## Attempt 19

Goal: attempt 18's main lead, t5le through S / Xc (the signature-failed share of the flow into the `xb.type <= 5` test X), then any trick with an untested idea.  Generators from gen_bd300.  Scratch in build/bd/a19 (not kept; `meas.py` there prints loadBl's profile_estimate frequencies of the three signature logs and X, the last alignment lines of loadBlFiles, and the bdrun score for each file given).

### t5le through S / Xc: the signature block's factors only take a few values (read from loadBl's profile_estimate)

- S / Xc = Psig x Pk x Pf at profile_estimate (every flow out of checkBl's success reaches X, so the ratio is the product along the failed path): Psig = 64% (`type == 5 || type == 17` is folded into one `_66 | _67` block with no heuristic, 50%, then `type == 11` nonequal, 28%), Pk = 85% (pointer; both arms' first blocks hold a call, so PRED_CALL cancels), Pf = 29% (PRED_CALL on the failed log only, because `else if (type)` keeps the call out of the passed arm's first block).  0.64 x 0.85 x 0.29 = 15.8% (attempt 18's 15.6% at vrp1).  t5le needs 21.6%.
- What each factor can be in natural code, and why:
  - Pf: the verify result must stay a zero test (the reference has `test eax,eax`; `!= 1` or `<= 0` change the compare), so no opcode heuristic applies.  Only PRED_CALL moves it: 29% (call in the failed arm only, src), 50% (calls in both, i.e. a plain else, or in neither) or 71%.
  - Psig: fold_truth_andor packs at most two leaves into a non-IF OR (simple_operand_p_2 refuses a TRUTH_OR operand), so any order or grouping of the three `==` is a 50% pair and a 28% single (64%), or three singles (62.7%), or one block with `|` written out (50%).
  - Pk: the pointer heuristic, 85%, unless one arm's first block loses its call (69.8% or 93.3%), which needs a test in front of that arm's call.
- So the natural products are 15.8% (src) and 27.2% (plain else, Pf 50%).  The window is narrower than 21.6% and up: measured with meas.py, raising S also moves the failed log and its copies (plain else with t5le off: 80 loose; `!= 1`, Pf 51.2%, diagnostic only: 76 loose, bb 111 still 4; a dead `if (type)` in front of the failed log, Pf 50%: 72 loose).  Rough bound from bb-reorder: the failed log is 29 at bbro, and round 4 starts at 5% of the entry (44); S >= 40.2 for t5le and S < 44 for the failed log to stay in round 4 would leave Pf in 40% to 44%, which no combination of the heuristics above gives (call against failure with early return for it would be 39.0%, nonequal with call 51.2%).
- gen_bd300 (diagnostics, not shapes: `!= 1`, dead `if (type)` wrappers in front of the failed log, the no-key log or the verify): none gets bb 111 to 1 without moving other blocks; the cheapest is the no-key wrapper (8 loose, .rdata moves).

### t5le through the SE copy's own frequency (the other factor in bb 111 = freq(SE copy) x P(>5))

- bb 111 is 2 because the SE copy is 4 (the SE block, 6, x checkBl's 61% = 3.66).  An SE block of 5 would make the copy 3 and bb 111 1, i.e. t5le with no change to P(<=5).
- The SE block's 6 is bb8 x 28% x 28% x 28% in loadBl's profile, where bb8 is the join of `*pr == 0` after loadInputFile (50%, no heuristic) and CF success (61%).  Threading recomputes the split of the `type == 9` test from its total, so taking the CF path's flow away is not enough: diagnostic `__builtin_expect(!suGetCF(..), 1)` (CF success 2%): the type-9 join goes 78 -> 72, the SE block stays 6, bb 111 stays 2 (0/7, as src without the label).  It would take bb8 about 15% lower, i.e. loadInputFile's success under 43%, and nothing natural predicts against it (both arms start with a `type == 9` test).
- Diagnostic `__builtin_expect(e->data[0] == 'S', 0)`: the SE copy goes to 0 and the alignment comes back on another block (14 loose).
- gen_bd301 (natural spellings of the failed arm that leave the profile as it is: `*pr = -1` before the log, the verify result in a local `ok` declared in the block or at the top; t5le on or off): all IDENTICAL with the label, all the old 0/7 without.  As expected from the above: nothing here touches Psig, Pk or Pf.

### exp_t24: what a redundant middle test would need (worked out, not swept)

- The expect works by putting a call-free block between `type == 25` and the imgSize() block, so `type == 25` keeps only nonequal (28%).  Attempt 15 put the need at 16% on that edge, so a middle block that folds after profile_estimate would need P(true) >= 57%; its true edge leads to the imgSize() call (PRED_CALL, 29%), so its own heuristic must be >= 76.4% (DS with 29%).  Only the pointer heuristic (85%) is that strong, so it would take a pointer test that VRP later proves non-null (`e` itself, `e->name`), which nobody writes.  The tests that are really redundant there (`xb.type != BUILD_RETAIL`, `xb.type <= BUILD_DEVGL16`) are compares with 0 or 5: no heuristic, 29% with the call, which makes the warning colder, not hotter.

### Don't retry (attempt 19)

- t5le through the signature block (Psig, Pk, Pf): natural code gives S / Xc = 15.8% (src) or 27.2% (plain else) and nothing between; the verify test must stay a zero test (no opcode heuristic), the 5/17/11 test is always a 50% pair and a 28% single, and Pk is the pointer heuristic.
- t5le through the SE block's frequency: threading re-splits the `type == 9` test from its total, so even the CF path at 2% leaves the SE block at 6.
- Spellings of the failed arm or a local for the verify result (gen_bd301): same profile, same code.
- exp_t24 by a redundant test between `type == 25` and the room test: it needs a >= 76% heuristic of its own against the call (only a pointer test of a known non-null pointer).

### Costs now (strict/loose, removed alone; 16 tricks, unchanged)

lab_t5le 7/0, exp_pr 18/2, exp_upd 18/12, pin_d 23/14, pin_e 26/26, exp_t24 29/7, exp_devgl 43/7, pin_size 82/40, exp_verbose 83/18, exp_t10 116/46, vol_fail 296/126, lab_none 333/231 (not re-measured: src/build.c is the same as attempt 18's, 9210177c).

### What to try next

- Attempt 18's closed form is now closed on all three of its inputs for natural code: S / Xc (this attempt), p (no heuristic reaches X's arms; attempt 11) and q (attempt 18).  t5le's other two conditions are set by blocks other tricks already pin: the SE copy's frequency (threading keeps the SE block at 6) and the type-11 no-key log's 17 (the constant_p weight, attempt 14).  So t5le only goes with a different tail or a different constant_p entry, i.e. with the source of loadBl's whole tail, not one test.
- The only multi-trick lead left is still attempt 10's near miss (vol_fail, t5le and exp_pr for 3 loose with the old badsize label, 9 loose on the current case 23).  Its two open questions are the same as attempt 11's: a `fail` block that lives to expand without the asm, and a `<=5` arm block that vrp1's joiner threads pass through.
- Otherwise build stays parked at 16.

## Attempt 20

Goal: the functions that got the least work lately: calcBlAreaSize's pin_size by whole-function forms (image_read's lever), then loadFileCrc's exp_verbose + pin_e by structure, then pin_d.  Generators from gen_bd310.  Scratch in build/bd/a20 (not kept).  New tool: `bdorder.py gen.py [regex]` prints, per case, calcBlAreaSize's statement before each setPatchSlot in the .optimized dump (or the lines matching regex) with the score.

### pin_size: whole-function forms (gen_bd310 to gen_bd312, pin off)

- gen_bd310 (144 cases): kit lookups as a `for (t = 12; t <= 14; t++)` loop (with and without x, `< 15`), a loop over a `static const` table, index locals per bootloader (`cb`, `cd`, `ce`, `cf`) summed at the end in three ways, size locals summed at the end, the sum as one expression, each arm returning through an `alignBlArea` helper, a `?:` return; x as uint32_t or int.  Best is src's own form (40 loose / 82 strict); the running `cb`/`cd` form is the same code, everything else 129 loose and up (loops 238 and up: cunroll doesn't give the straight-line lookups back).
- gen_bd311 (80 cases): the other arms' forms (retail head as one expression, offset first, a loop; xell block with `xs = 0x40000` first, a pointer, the arms written out, an offset local; JTAG lookups inline): all 40 at best; most are the same GIMPLE.
- gen_bd312 (16 cases): setPatchSlot / imgCfSize shared by kit and retail (104 and up), each arm as a static helper called once (134 and up).
- Read from the dumps (`bdpasses.py`, PRE details): reassoc1 is what first writes the kit sum as `_40 + size_254` (rank: the load ranks above the PHI in the same block); PRE then replaces `_40` by prephitmp_229 and fold orders by version.  PRE's insert walk does the kit arm first and pops the free list (243, 242, 237, 236, 229, ...: dom2's retail-arm copies that reassoc1 and dce freed), so the kit names are always below the size PHI's (254); the JTAG arm comes last and gets fresh names (284 to 287), which is why its sum is `size_249 + prephitmp_287`.  `bdorder.py gen_bd311.py`: no arm form flips the kit sum (prephitmp 134 to 243 against size 249 to 255).
- But the operand order isn't the whole story: diagnostic `"+r"(size)` in place of `"+b"` (order fixed by the asm, no register) fixes the JTAG arm and the early files[0].size load but ties the kit sum to the prephitmp (`add ebx,eax` with size in eax): 9 loose.  So the reference needs size's PHI in its own allocno with ebx, which is IRA's region choice at the 14 loop (attempt 4), not only the version order.
- Nothing in gen_bd310 to gen_bd312 gets under src's 40 loose; pin_size stays.

### loadFileCrc (exp_verbose + pin_e): structural forms (gen_bd313 to gen_bd315)

- gen_bd313 (64 cases), the logs as a `logReading` helper (verbose outside or inside, if/else or early return, padded size as `e->size`, `align16(size)` or read from e): 67 loose in loadFileCrc at best, and .rdata moves (the helper stays a call in some callers).
- gen_bd314 (16 cases), attempt 12's goto form with the pad arm nested or `&&`, the pad log's third argument, `size == 0`, `c != crc`: all the old 38 (name and size swapped: IRA pushes name before crc, as its frequency fell with the pad log's).
- **gen_bd315: IDENTICAL BYTES with both hints off** (`vfirst`): the pad test repeated inside `if (verbose)` to pick the log,
  ```
  if (verbose) {
  	if (!pad || !(size & 15))
  		bytes log;
  	else {
  		if (size != e->size) pad log; else bytes log;
  	}
  }
  ```
  Either polarity of the inner compare matches.  The forms that give each pad arm its own verbose test and bytes log (non-pad arm first, 104; pad arm first, attempt 12's dup, 79 and .rdata) don't.
- **gen_bd316, landed (16 -> 14, IDENTICAL BYTES, full build SHA256 matches):** `plain pos_and int`,
  ```
  if (verbose) {
  	if (pad && (size & 15) && size != e->size)
  		pad log;
  	else
  		bytes log;
  }
  ```
  `neg_nest`, `neg_chain` and `pos_nest` (the same test with nested if/else) also match; the compact `&&` form is in src.  The padded arm without the compare (`ponly`, 67) doesn't, so the dead `size != e->size` stays (the reference has its compare at 2a7).  A `padded` flag for the pad condition (int or BOOL, before or after the first store) makes loadFileCrc.constprop clones: 10000+.
  - Borderline (marked in src): the pad condition is computed twice, and `size != e->size` can't be false once it holds.  It's live code that reads naturally ("log the pad if we padded"), like patchCpuFan's repeated test.
  - Mechanism (checked in the bbro dump, `bddump.sh src/build.c loadFileCrc bbro`): the re-test gives the non-pad path its own edges to the bytes log at profile_estimate (pad false 50%, `size & 15` false 50%, then nonequal 28% on the rest), so the log gets about 0.82 of the verbose arm: bb 12 [3220], round 2 (needs 2000), against 1102 in the old form, where only a later thread separated the path.  The pad log is 716.  The registers (name edi, size ebp, e esi, f ebx) then come out as the reference has them with no pin, as they did in the old form with both hints off.  The earlier forms gave the non-pad path its own route by a goto (pad log 504: name below crc) or by a second verbose test per arm (dup: .rdata order).
- **Lesson: when a hint is about a path that only a later thread separates, test the condition that decides the path again where it's needed, so the path exists at profile_estimate.**  Attempt 12's search was for forms that reach the log "directly"; the re-test does it without a goto or a second log.
- gen_bd313 to gen_bd316 replace the old loadFileCrc text, so they only rerun against src as of a0108d6d (before this landing).

### pin_d: lifetime and scope (gen_bd317, pin off, on the landed src)

- d in its block, assigned in the test, absent (loadConsoleBlFiles' spelling), an early `break`, a file-entry pointer for the tail (with and without the break), `void *` and `const` d, the size in a block local inside `if (d)`: all the old 14 loose / 23 strict (GIMPLE is the same ARRAY_REF loads).  The size in a local read next to d (either order) is 143.  Nothing moves IRA's pop order (attempt 16: the base's thread is popped before n's).

### Don't retry (attempt 20)

- pin_size by whole-function forms: loops over types or a table (cunroll doesn't give the straight-line lookups back), index or size locals summed at the end, one-expression sums, per-arm returns or helpers, a shared setPatchSlot tail (gen_bd310, gen_bd312); by the other arms' forms (gen_bd311: none flips the kit sum's operand order, and the order alone isn't enough, see the `"+r"` diagnostic).
- loadFileCrc: done.  The `logReading` helper (gen_bd313) and attempt 12's goto form with spellings (gen_bd314) are worse than the landed form anyway.
- pin_d by d's or the size's lifetime and scope (gen_bd317), on top of attempts 4, 5 and 16.

### Costs now (strict/loose, removed alone; 14 tricks)

lab_t5le 7/0, exp_pr 18/2, exp_upd 18/12, pin_d 23/14, exp_t24 29/7, exp_devgl 43/7, pin_size 82/40, exp_t10 116/46, vol_fail 296/126, lab_none 333/231 (`bdhints.py` on the landed src).  The two `__builtin_constant_p`, the dead `else if (type)` and the `--param` aren't in bdhints.

### What to try next

- **The re-test lever on the other frequency hints.**  Where an expect or label exists because a path is only split by a later thread (vrp1/dom), a natural re-test of the deciding condition at the point of use creates that path before profile_estimate.  loadBl's tail (t5le, exp_pr: vrp1 joiner copies of the `xb.type <= 5` test) is the obvious candidate, as is exp_t10; the brief kept this attempt off loadBl, so it's untried there.
- pin_size: the kit sum needs its own allocno in ebx (IRA's region split at the 14 loop); whole-function forms don't move it.  If anything, look for a form that changes the 14 loop's region (its frequency or pressure), not the sum's spelling.
- pin_d stays an IRA pop-order tie.

## Attempt 21

Goal: attempt 20's lever (test the deciding condition again where a path uses it, so the path exists at profile_estimate rather than being made by a later thread) on loadBl's tail (t5le, exp_pr, the barrier), then exp_t10 and the rest.  Generators gen_bd320 to gen_bd325, all on src as of c7114455.  Scratch in build/bd/a21 (not kept; `trk.py dumpdir fn regex [passregex]` there prints, per tree pass, fn's blocks whose statements match regex with frequency and successor probabilities, from the last body in each dump).

### The tail split by `*pr` (gen_bd320, gen_bd321)

- gen_bd320 (132 cases): tail forms that give the signature-failed (`*pr` = -1) and `*pr` = 0 paths their own `xb.type <= 5` test before profile_estimate: `*pr` first with the `<=5` test in each arm (`prfirst`, `prfirst2`), `*pr && <=5` / `<=5 && *pr` as the fail exit plus a second `<=5` test, the `<=5` test twice, the kit test in an else, the whole tail per `*pr` arm (`pr_split`); `*pr` spelled `!= 0`, bare or `== -1`; its expect on or off; the size log through `goto fail` (src) or attempt 10's own `*pr = -1; break;` with the barrier off.  Best: src's own form (0/7 with the expect, 2/13 without, t5le off in both).  `prfirst` with the expect is 2/18, the same bytes as src with exp_pr off; without the expect 48 loose.  Every two-test form is 72 loose and up, `pr_split` 68 (it loses the type-11 copy); with the size log's own -1 everything is 92 and up (the `*pr` test then still reaches `fail`, so fail keeps three predecessors).
- Read from profile_estimate (`prfirst`): the split works as intended, each `<=5` test gets its own probability: the `*pr` = 0 one is 39% (its `<=5` arm is the `break`, the early-return heuristic), the sig-failed one 50% (fail holds a store, no heuristic), and the outer `*pr` test 50% without its expect.
- gen_bd321 (diagnostics, expects on each arm's test): with the outer `*pr` expect and `__builtin_expect(<=5, 1)` on the `*pr` = 0 arm, 0/9 (the type-11 block's `.p2align`, exp_pr's old 9 lines: the sig-failed setFlashBuild copy has frequency 1 where src has 4); the sig-failed arm's probability makes no difference (0/9 for 2%, 50% and 98%).  Without the outer expect every case is 48 loose and up.  So the split needs three probabilities that no natural form gives: the outer `*pr` test about 2%, the `*pr` = 0 test's `<=5` side well over 50% (its natural best is 50%, and 39% when that side is the break), and enough sig-failed flow through the shared `type == 14` block.
- Why the sig-failed setFlashBuild copy needs that flow: at vrp1 the `type == 14` block keeps its profile_estimate count (src 28 = X's `>5` 15% of 186, with t5le; 93 at 50%), and the copies dom2 makes for the sig path are limited by it.

### attempt 11's kit-first tail (4 loose) is not closer: a code-size coincidence plus a PHI-order effect

- Rerun on the current src (gen_bd223, gen_bd322: kit arm spelled 11 ways, the `*pr` arm 3 ways): every `if (xb.type > BUILD_DEVGL16) {..}` form is the same 4/19 in loadBlFiles with the expect (6/23 without), plus call displacements in later functions (44 total); `!(xb.type > 5)` folds back to src's `<= 5` (0/7).  Only the condition's orientation matters.
- The alignments dump (`bddump.sh f loadBlFiles alignments`) is identical for src minus t5le and the kit form: bb 111 (the jmp after the SE copy) freq 2, bb 112 (the type-11 no-key log) freq 17 and not aligned in either.  So the kit form doesn't fix t5le's alignment; its code is shorter (the IV read), which happens to move the padding.  Don't count it as t5le gone.
- Why its sig-failed setFlashBuild copy reads through the IV (checked in vrp1, sra and dom2 dumps): vrp1's threads are the same in both forms (only the `*pr` block's number differs), but the join after the tail gets its predecessors in a different order: `r_371 = PHI <.., r_476(set), r_476(type14), ..>` in src, `<.., r_476(type14), r_476(set), ..>` in the kit form.  dom2's FSM backward walk takes the first argument (attempt 6's rule), so in src it threads the sig path `(20,23) (23,24) (24,104)` through setFlashBuild (both blocks copied before ivopts, the copy recomputes `xb.files[i].data` from i), and in the kit form `(20,23) (23,104)` through the false edge (only the type == 14 test copied; setFlashBuild is copied by dom3, after ivopts).  So the `<= 5` orientation is required.

### What the joiner formula leaves for t5le in the `<= 5` orientation (worked out, partly measured)

- With the src structure, attempt 18's formula P(SE copy, <=5) = Xc p (1 - q) / (Xc - S) needs p (1 - q) >= 52.8% at S / Xc = 15.6%.  q can only go towards 0 (the expect gives 2%), so p >= 53% to 54%: X needs a predictor of any strength towards its `<=5` side.  None applies (checked against the predictor list again): neither arm's first block holds a call (PRED_CALL), neither is the return block or a single-successor block before it (early return), `xb.type <= 5` is a compare with 5 (no opcode heuristic, and `< 6` folds to it), there is no loop (continue, loop predictors), and the C front end only emits a predictor for `continue` (no PRED_GOTO: CG's `goto chk` gets plain 61% from the break's early return).
- Giving the SE path its own `<=5` test (its own checkBl, then `if (xb.type > 5) set; break;`) would combine the early return (39%) and PRED_CALL on the set side (71%) by DS: 61.0%, still under 62.6%.  Built anyway (gen_bd325: three spellings, checkBl's type 14 or `type`, t5le / exp_pr on or off): 40 loose in loadBlFiles plus displacements in every case, the hints make no difference; the second checkBl and setFlashBuild calls change the code before the profile matters.  Don't retry.
- The other two factors of bb 111 (the jmp after the SE copy, freq 2, must be <= 1 for the no-key log's `.p2align`): the SE copy's 4 (SE block 6 x checkBl's 61%; the SE block is 9.9 at profile_estimate, attempt 19's re-split rule keeps it 6) and the no-key log's 17 (the constant_p weight).  Nothing new.

### The "could not read" log in loadBl (gen_bd323, 48 cases)

- Idea: the `if (r)` that vrp1 threads is the caller's, and its join is drained by ~30 FSM threads before the joiner copies (attempt 11); with the log in loadBl after the switch (`if (*pr) log;`, fail: logging itself, `goto out` back to the test, the switch jumping over fail:, an early-return spelling; the caller only `if (r) return -1;`) the test exists at loadBl's profile_estimate.  Best 95 loose in loadBlFiles plus displacements (`over`, any hints); with t5le, exp_pr and the barrier off 113.  The log's PRED_CALL and the new join reshape the whole profile.  Don't retry.

### `else if (type)` with a plain else, revisited for t5le (gen_bd324, 24 cases)

- A plain else raises S / Xc to 27.2% (Pf 50%), which by the formula is enough for t5le even with q = 2% (P = 67%), and it would remove the dead test too.  Measured: plain else with t5le and exp_pr off is 56 loose (128 strict); with exp_pr kept 56/128; t5le kept 54 plus displacements.  What's left is the verify's layout: at 50/50 bb-reorder's better_edge_p falls through to the failed log (the next block in order), where the reference falls through to the passed log; and with exp_pr off the SE copy's `ja`.
- The passed arm first (`if (cbVerifySig(..)) passed; else {failed}`, either spelling of the test) wins the tie but moves .rdata (the passed string before the failed one; the reference's order is no-key, failed, passed): 50 loose at best.  `*pr = -1` before or after the failed log: no change.  So the tie can't be broken in natural code; the dead test's 29% stays.  Don't retry plain-else forms (attempts 5, 6, 18, 19 and this one).

### exp_t10: what the CG flow is made of (profile_estimate of src with the expect off)

- CG's checkBl copy is CG's flow at loadBl's profile_estimate: `*pr` after loadInputFile 50% (zero test, no heuristic) x `type == 9` false 86.3% x `type == 10` 19.9% x suGetCG success 61% = 43.6 (44 at bbro; it needs about 22).  The 19.9% is nonequal (28%) + PRED_CALL against the CG block (29%) + the early return on the `else break` (which pushes it up: without it 13.7%); the 61% is the failure break's early return.  Without both early returns the copy would be about 25, so both breaks would have to reach something other than the return, which in this function only the caller's log does (and moving the log in is gen_bd323's 95).  The CG checkBl copy is a joiner copy whose count is its full incoming edge, so threading doesn't help or hurt here: the factor has to be at profile_estimate.  Not swept.

### Don't retry (attempt 21)

- The tail split by `*pr` before the `<=5` test, or the `<=5` test repeated per exit (gen_bd320): each split test then needs its own unnatural probability (gen_bd321: outer `*pr` about 2%, the `*pr` = 0 test's `<=5` side over 50%).
- The kit-first orientation (`xb.type > BUILD_DEVGL16` first) in any spelling (gen_bd322): the join's PHI order sends dom2's FSM thread past setFlashBuild; and its 4 loose were a code-size coincidence, not t5le.
- The could-not-read log inside loadBl (gen_bd323).
- The SE path with its own checkBl and kit test (gen_bd325).
- Plain else for the passed log, either polarity (gen_bd324).
- Diagnostic expects can't be stacked to reach t5le's p >= 54% without a hint, so don't sweep spellings of `xb.type <= 5`.

### Costs now (strict/loose, removed alone; 14 tricks, unchanged)

lab_t5le 7/0, exp_pr 18/2, exp_upd 18/12, pin_d 23/14, exp_t24 29/7, exp_devgl 43/7, pin_size 82/40, exp_t10 116/46, vol_fail 296/126, lab_none 333/231 (`bdhints.py`, re-measured on c7114455).

### What to try next

- Attempt 20's lever fits a hint whose path is merged in the source and split by a thread *inside the same function before profile_estimate matters*.  loadBl's tail paths are split by the caller's `if (r)` after inlining, so a re-test inside loadBl creates new tests with their own (wrong) probabilities instead of giving the threaded path its flow (gen_bd320, gen_bd321).  The lever doesn't carry over to t5le, exp_pr or exp_t10.
- t5le now has every input of its formula checked against natural code (attempts 11, 14, 18, 19, 21): it needs one predictor towards X's `<=5` side, and the tail has none to offer.  exp_pr needs q <= 4.4% with the label (q is a `*pr` zero test: no heuristic, and the break's early return pushes it the wrong way).  exp_t10 needs both of CG's breaks to stop being early returns.
- Otherwise build stays parked at 14.

## Attempt 22

Goal: attempt 20's lever (repeat the deciding test, or test it where the value is used, so the path exists at profile_estimate) on the four frequency hints outside loadBl: exp_t24, exp_devgl, exp_upd, lab_none; pins only with a new idea.  Generators gen_bd330, gen_bd331, on src as of c941f014.  Scratch in build/bd/a22 (not kept).  New tool `bdpwin.py [file.c] [p,p,..]`: scores a source at several `builtin-expect-probability` values and prints addBlsToImage, buildFlash, addUpdateBls and loadConsoleBlFiles strict/loose.  That isolates each target because each of those functions holds exactly one of the expects; other functions' changes only show up as call displacements.

### The real windows, measured with the param (new: the earlier margins were derived from dumps)

`bdpwin.py` on src, p = 50 to 99 (function loose/strict):

| p | addBlsToImage (exp_t24) | buildFlash (exp_devgl) | addUpdateBls (exp_upd) |
|---|---|---|---|
| 50 to 65 | 7/29 | 7/43 (12/600 at 50) | 12/18 |
| 70 | 7/29 | 27/63 | 12/18 |
| 72 | 7/29 | 27/63 | **0/0** |
| 75 | 7/29 | 20/20, call displacements only: **matches** | 0/0 |
| 77 | **0/0** | displacements | 0/0 |
| 90 and up | 0/0 | 0/0 | 0/0 |

- **exp_t24 needs more than attempt 15 said.**  The expect's block probability q has to be >= 77% (75% fails).  The warning's frequency is 1881 x 28% (nonequal only: the call-free middle block sits in front of imgSize()) x q x 29% = 152.7 q, so the window starts between 114.5 and 117.6.  The warning has to beat the seReplacesCf findFile(14) exit block (117) in bb-reorder's heap, not just reach round 2 (87).  From the natural 75 that's x1.57, not x1.16.  Attempt 19's middle-test bound gets worse with it: a call-free middle block now needs P >= 89% of its own against the imgSize() call (pointer 85% gives 69.8% combined; nonequal 72%, e.g. the redundant `xb.type != BUILD_RETAIL`, gives 51.2%, warning 78.  BUILD_RETAIL is 1, so that test does get nonequal, unlike what attempt 19 assumed).
- **exp_devgl: attempt 15's margin stands.**  p 75 already matches (buildFlash differs only in call displacements caused by other functions' expects), p 72 doesn't, which fits sink's 75.06% rule; the natural test has 73%.
- **exp_upd's window is P23 <= 28% (p 72 matches, 70 doesn't), not 23.8% (attempt 8) or 16.3% (attempt 18).**  28% is exactly the nonequal heuristic alone.  Natural forms give 39% (the `(23|15)` pair: an OR of two bools, no opcode heuristic, early return only) or 19.9% (a lone `==`, which then merges 23 into the mask).  So the pair needs one more predictor with P <= 39% of its own on top of the early return (DS(39%, x) <= 28.5% needs x <= 39%), and isUpdateBl has no call, loop or non-0/1 return to supply one.
- gen_bd330 (diagnostic: the expect moved from the first pair to the second, third or fourth test of isUpdateBl, as `, 1`): the third and fourth are the old 12/18; the second pair is 100/177 at every p from 52 to 90, i.e. a structural change (the expect splits the pair that reassoc merges into the mask), not a probability window.  So "raise the mask block's probability instead of lowering P23" can't be measured this way; it would need a TAKEN predictor (only `!=`, or `>`/`>=` against 0/1/-1, give one), which an "is one of" chain doesn't have.

### exp_t24: what would give x1.57, and why the code doesn't have it (read from profile_estimate of src with the expect off)

- Path at profile_estimate: bb 36 `xb.type > 5` (50%, no heuristic: neither arm's first block holds a call) -> bb 39 `type == 25` 13.7% (nonequal 28% with PRED_CALL 29% from imgSize() in bb 40) -> bb 40 room test 29% (PRED_CALL from the warning's log) -> bb 41 warning 75.
- Either of two single changes would be enough: bb 39 losing PRED_CALL (28%: warning 153, the reference's own number with the expect), or bb 40 losing it (50%: 129).  PRED_CALL (tree_estimate_probability_bb) needs the edge's destination to be dominated by the test and to contain a call.  So bb 40 or bb 41 would need a second predecessor at profile_estimate, or the room test's false side would need a call block of its own.  The room block is only reachable from the `type == 25` test and the warning only from the room test; every reordering tried (retail or kit arm nested, the type test outside, the room test after the chain: gen_bd96, gen_bd147, gen_bd260, gen_bd270) keeps both with one predecessor.  The room test's false edge goes to the shared "adding" join (it's threaded to the adding log only later, which is what IDA shows), so it can't hold a call without a second adding log.
- Is the warning's path made by threading (the brief's question)?  No: the warning block is never copied.  Threading only removes the retail-not-23/25 flow from bb 36 and bb 39 (vrp1 knows `xb.type == 1` there), and the warning keeps its profile_estimate frequency to the end.  So attempt 20's lever has nothing to act on here: the path already exists at prediction, and it's the predictors on it that are fixed.
- `e->offset != 0xffffffff &&` in front of the room test would make a call-free middle block (nonequal 72%), but nothing proves it, so it stays in the code, and it skips imgSize() for unplaced entries.  Not a candidate.

### exp_devgl: nothing new

- The window is the old 73% against 75%.  The devgl value is used only at the top (the cmovbe) and by `if (fuse)` far below, after many calls; testing it at the use would reload xb.type there.  The later `else if (xb.type == BUILD_DEVGL || ..)` patch arm comes after calls too.  No predictor is reachable (attempt 16's list).  Not swept.

### lab_none: the call sites' flow (gen_bd331, 9 cases)

- Read from profile_estimate and bbro of src with precheck and label gone: case 24 is 716 (1 of the switch's 10 targets), `!xb.glitch2mfg` sends 29% on to the loadBaseFile block (PRED_CALL), loadBaseFile's test 29% to the first defaultBl60 call (PRED_CALL; the else side has no call), the size test 51.2% (nonequal with PRED_CALL): sites 60 + 76 = 136, r = 1 (bbro bb 53) 136 x 10.1% = 14.  The not-entered return (bb 62) is 20 and was queued in round 1, so bb 53 needs 21 or more (about 205 at the sites).  bb 53's only predecessor, the merged inlined malloc test (bb 21), is in the middle of trace 29 (20, 21, 22), so bb 53 gets no end-of-trace priority either.
- `if (loadBaseFile(..) || e->size != 0x60) r = defaultBl60(e);`: one call block with two predecessors, so neither test gets PRED_CALL: sites 179, r = 1 18, still under 20.  Measured: 6/10 with precheck and label gone (r = 1 still after the return, and the size store moves: attempt 4's crossjump order), 2/2 with them kept.  `xb.glitch2mfg && (.. || ..)` is the same; the nested `if (xb.glitch2mfg) {..}` is IDENTICAL with the label and 4/8 without (the same CFG as src); the inverted `if (!loadBaseFile(..) && e->size == 0x60) break;` 10/18.
- The glitch2mfg test's 29% is the factor that would decide it (50% would give 234 at the sites, r = 1 24), but it gets PRED_CALL from loadBaseFile's block in every order that keeps loadBaseFile after it, and its break side has no block of its own.

### Don't retry (attempt 22)

- exp_t24 by any middle test (it needs 89% of its own now), by chain reorderings (the room and warning blocks keep one predecessor in all of them), or as a threading question (the warning is never copied).
- exp_upd by raising the mask block's probability with a moved expect (gen_bd330: structural, 100/177).
- lab_none by case 24's forms (gen_bd331): `||` reaches 18 of the 21 needed and moves the size store.

### Costs now (strict/loose, removed alone; 14 tricks, unchanged)

lab_t5le 7/0, exp_pr 18/2, exp_upd 18/12, pin_d 23/14, exp_t24 29/7, exp_devgl 43/7, pin_size 82/40, exp_t10 116/46, vol_fail 296/126, lab_none 333/231 (`bdhints.py`, re-measured on c941f014).

### What to try next

- Use the measured windows above rather than the dump-derived margins: exp_t24 needs the warning above 117 (x1.57), exp_devgl 75% (has 73%), exp_upd P23 <= 28% (has 39%), lab_none r = 1 >= 21 (has 14).  `bdpwin.py`'s method (one expect per function, vary the param, ignore call displacements) is quick and worth rerunning after any landing.
- Attempt 20's lever needs a path that a thread creates after profile_estimate.  None of these four has one: the exp_t24 warning, the devgl arms, isUpdateBl's pair and the r = 1 block all exist at prediction, and what's missing is a predictor on a block that natural code gives none (exp_t24 and lab_none: PRED_CALL on a single-predecessor call block; exp_upd: an OR of two bools; exp_devgl: two call-free arms).
- The closest is exp_upd: the window is exactly the nonequal heuristic (28%), so a natural spelling of the `type == 23 || type == 15` pair whose branch compares against a non-zero constant or a variable, while keeping `type == 23` as an SSA bool for the body's reuse, would land it.  None is known; check any candidate in isUpdateBl's profile_estimate (bb 2 must show "opcode values nonequal") before scoring.
- Otherwise build stays parked at 14.

## Attempt 23

Goal: exp_upd by a spelling whose first branch gets "opcode values nonequal" at isUpdateBl's profile_estimate (attempt 22's lead), then the others with the same lever.  Generators gen_bd340 to gen_bd342 on src as of 604028f1.  Scratch in build/bd/a23 (not kept).

### exp_upd: landed (14 -> 13, IDENTICAL BYTES, full build SHA256 matches)

`if (type == 23) return 1; if (type == 15) return 1; return type == 16 || type == 9 || type == 10 || type == 24 || type == 25;` with no expect.  Mechanism, read from the dumps (`bddump.sh build/bd/a23/land.c isUpdateBl t-profile_estimate`, `.. addUpdateBls t-ifcombine,t-dom2,t-reassoc1`):

- At profile_estimate each lone `if (type == N) return 1;` is a GIMPLE_COND against a non-zero constant: nonequal 28% + early return 39% = 19.9% (bb 2 and bb 3), inside the <= 28% window.
- Post-IPA, in addUpdateBls, **ifcombine** pairs the two lone tests into `_142 = type == 23; _143 = type == 15; _141 = _142 | _143; if (_141 != 0)`, i.e. the same `(23|15)` OR the front end used to fold from `||`, keeping the outer block's 19.9%.  It only pairs a following block that holds nothing but its cond, so the pair has to be two lone ifs (the `||` group after them is a block of computed bools, so ifcombine stops there).  dom2 then reuses `_142` for the body's `type == 23` (two uses), so reassoc1 keeps 23 out of the bit test as before, and the exported copy (one use) still gets 0x3818600.
- gen_bd342 (36 cases): the two lone tests in either order, `if`/`else if`/`if (group) return 1; return 0;`, and 6 orders of the group: IDENTICAL whenever 9 and 10 aren't adjacent in the group (`9 10 ..` and `10 9 ..` fold to a range test and cost 109 loose; `25 24 16 10 9` 108).  Landed the order closest to the old one.
- Flagged in src as "Borderline, for review": live, not redundant, but chosen for what gcc does with it (as attempt 15's `(e->size & ~3)`).
- `bdpwin.py`: addUpdateBls is now 0/0 at every p from 50 to 99.  The whole object still matches at p = 96, 98, 99 only (loadBlFiles' expects decide: 89 to 94 and 97 cost 35 or 36), so the param stays at 98.

### What didn't work first (gen_bd340): a result variable

- `int r = type == 23; if (!r) r = <rest>; return r;`: forwprop always combines a compare into a cond, so `if (!r)` becomes `if (type != 23)` and gets nonequal (19.9%), while the PHI still takes `r_5`.  addUpdateBls' head is then laid out like the reference (only register choices differ: 69 loose), but 23 stays out of the *exported* isUpdateBl's mask too (`cmp 23; je`), because a non-constant PHI argument breaks reassoc's range chain; sink only moves `r_5` into the branch after reassoc1 (dom3 folds it there).  112 loose.  `if (r) return r;` 171, `if (r) return 1;` (r dead) 264.
- `(23 || 15) != 0`, a named `cf2 = type == 23` in the `||`, `r = 23 || 15`: all the old 39% (a zero compare on an OR of bools), 12 loose.
- A lone `if (type == 23) return 1;` before an `||` group starting with 15 (`m 23 | 15 ..`, gen_bd341): 226 or 311: the group's block isn't cond-only, so ifcombine can't pair 23, and a lone GIMPLE_COND joins the mask.  All seven tests as lone ifs: 119 (ifcombine chains them all into one block).  Two-case switch `case 23: case 15:` 303.

### Don't retry (attempt 23)

- exp_upd is gone; don't revisit the result-variable forms (exported copy keeps 23 separate).
- exp_devgl by fuse as one expression (gen_bd343, 10 forms: `g != 0 || dev`, `dev || g != 0`, ternary, if/else, `!=` chains with JTAG, `|` of the two bools): none better than src without the expect (7 loose); `(g != 0) | (dev)` is 9 (setbe + or where the reference has cmovbe), the `!=` chain 53.  The lone-if lever doesn't help it: two lone dev tests multiply in the wrong direction (52%, attempt 4), and sink needs the non-dev side above 75%.

### Costs now (strict/loose, removed alone; 13 tricks)

lab_t5le 7/0, exp_pr 18/2, pin_d 23/14, exp_t24 29/7, exp_devgl 43/7, pin_size 82/40, exp_t10 116/46, vol_fail 296/126, lab_none 333/231 (`bdhints.py`, unchanged by the landing; exp_upd's entry is gone from bdhints.py and bdtricks.py).

### What to try next

- The lever that landed exp_upd is new: a test written as its own `if` gets its own predictor at profile_estimate (here nonequal on a lone `==`), and ifcombine rebuilds the OR after inlining, so the later passes see the same GIMPLE as the folded `||`.  It only helps where a folded OR (an `||` of simple compares) has the wrong probability and the OR's members are cond-only blocks after inlining.  Candidates to check for that shape: the retail arm's `type == 23 || type == 25` in addBlsToImage (exp_t24's path starts after it), and any `||` of compares feeding a frequency hint in loadBl or loadConsoleBlFiles.
- Otherwise the attempt 22 windows stand for the rest: exp_t24 x1.57 on the warning, exp_devgl 75% (has 73%), lab_none r = 1 >= 21 (has 14).

## Attempt 24

Goal: attempt 23's lever (lone tests get their own predictor, a later pass rebuilds the OR) on exp_t24 first, then exp_devgl, loadBl's hints and lab_none.  Generator gen_bd350 on src as of 892a28f1.  Scratch in build/bd/a24 (not kept).

### exp_t24: landed (13 -> 12, IDENTICAL BYTES)

The lone-if lever itself has nothing to act on in addBlsToImage: the retail-skip flow is only 8% of the chain (bb 36 3762 of 4095), so lone 23/25 tests there could add at most x1.09, and the kit arm's OR isn't on the warning's path.  But re-reading attempt 16's gen_bd270 (the kit arm in the chain, `else if (xb.type > BUILD_DEVGL16 && (type == 23 || type == 25))`) on the current src showed what was left of it:

- At profile_estimate that form sends the kit path's not-23/25 flow into the `type == 25` test (bb 38 3272, against 1881 in src), so the warning gets about 128 with no expect, above the seReplacesCf found-SE block's 114 to 117 that it has to beat (attempt 22's window).  The warning's placement was right in gen_bd270 already; the 27 loose lines were all the kit path's `cmp edi,0x19` copy, i.e. vrp1 not threading the kit-false edge past the `type == 25` test.
- Why vrp1 didn't (vrp1 dump of gen_bd270's best): the kit test's false edge gets two chained asserts from the folded OR, `type_206 = ASSERT_EXPR <type_21, != 23>; type_207 = ASSERT_EXPR <type_206, != 25>`.  The threader's simplify_control_stmt_condition looks up the operand through lhs_of_dominating_assert (tree-ssa-threadedge.c), which returns the first ASSERT_EXPR whose operand is `type_21` itself, i.e. type_206 with the range ~[23, 23]; that can't decide `type_21 == 25`, so the path isn't threaded.
- **gen_bd350: IDENTICAL whenever the kit test is written `(type == 25 || type == 23)`**: the first assert is then `!= 25` and the threader takes the kit path straight past the warning test, as the reference has it.  The retail test's order doesn't matter (r23 and r25 both match: its false edge goes through the `xb.type > 5` test first, and the reference keeps it entering the `type == 25` test anyway), nor does `> BUILD_DEVGL16` against `>= BUILD_DEVKIT`, nor the room test flat or nested.  `(type == 23 || type == 25)` in the kit test is the old 63 loose (27 in addBlsToImage, .rdata and buildFlash).
- Landed `k25 r25 flat`: both skip tests spelled `(type == 25 || type == 23)` so they read alike, the kit test in the chain like the retail one, `else if (type == 25 && e->offset < imgSize())` without the expect.  Same behaviour: a kit entry of another type now reaches the room test, which is false for it.
- Borderline, marked in src: live and not redundant, but the 25-first order is chosen for vrp1's assert order (as attempt 15's `(e->size & ~3)`).  The kit arm in the chain is arguably the more natural form (it matches the retail arm), not borderline in itself.
- `bdpwin.py`: addBlsToImage is now 0/0 at every p from 50 to 99.  The whole object matches at p = 96, 98, 99 only (89 to 95 and 97 cost 26 loose in loadBlFiles), so the param stays at 98.
- **New lever: the order of the leaves in a folded `||` decides which `!=` assert vrp1's threader can use on its false edge (only the first).  Where a hint fixes a path that vrp1 should thread past a later test of one of the OR's leaves, put that leaf first.**  The same applies to any `(a == x) | (a == y)` false edge followed by a test of `a == y`.

### Costs now (strict/loose, removed alone; 12 tricks)

lab_t5le 7/0, exp_pr 18/2, pin_d 23/14, exp_devgl 43/7, pin_size 82/40, exp_t10 116/46, vol_fail 296/126, lab_none 333/231 (`bdhints.py` on the landed src; exp_t24's entry is gone from bdhints.py and bdtricks.py).

### The assert-order lever on loadBl (gen_bd351, 48 cases)

- loadBl's only folded `||` of a local is the signature test `type == 5 || type == 17 || type == 11` (fold makes `(5|17)` one block and the third leaf a lone cond).  Its six orders crossed with t5le, exp_pr, both, exp_t10, the dead `else if (type)` as a plain else, the barrier, and t5le + exp_pr + plain else off: nothing beats src.  Other orders only change the compare order (4 or 6 loose with every hint on, and the hints cost the same on top: t5le 4/11, exp_pr 6/22, exp_t10 48/118); the plain-else cases are 94 loose and up (56 with t5le and exp_pr off too), the barrier cases 126 and up, src's order best in each.  No later test on the signature path reads one of the leaves the way addBlsToImage's room test reads 25, so the order has nothing to thread.
- The other folded `||`s left in build.c are of memory (`xb.type == .. || xb.type > ..`: not simple operands, so the front end keeps them as separate conds) or range tests (`xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16`: one `t - 4 <= 1` cond, no assert pair), so the lever doesn't reach exp_devgl, lab_none, exp_t10 or t5le.

### Don't retry (attempt 24)

- exp_t24 is gone; don't revisit the kit-in-chain form with 23 first (vrp1 can't thread it).
- The signature test's leaf order with loadBl's hints off (gen_bd351).
- Lone 23/25 tests in addBlsToImage's retail arm for the warning: the retail skip is 8% of the chain's flow, x1.09 at most.

### What to try next

- Two levers now come from reading which predecessor flows into a test at profile_estimate: attempt 23 (a lone `if` gets its own predictor) and this one (a shape that sends extra flow through a test at profile_estimate, which vrp1 threads away later if the assert it needs is the first on that edge).  The second is worth checking wherever a hint raises a block's frequency: give the block a predecessor whose flow is later threaded past it, and check vrp1's ASSERT_EXPRs (`bddump.sh f fn t-vrp1`, grep ASSERT_EXPR) on the new edge.
- exp_devgl (sink's 75% against 73%) and lab_none (r = 1 at 14 against 20/21) are the cheapest left; neither has a folded `||` of a local on its path.

## Attempt 25

Goal: the brief's targets in order (exp_devgl, lab_none, loadBl's tail), using attempt 24's lever (an extra predecessor at profile_estimate whose flow vrp1 threads away later).  Generators from gen_bd360 on src as of 3778d12d.  Scratch in build/bd/a25 (not kept; `singles.py file.c [pairs]` there scores each bdhints entry off on a base).

### exp_devgl: why the lever can't act there (read, not swept)

- At sink (`bddump.sh .. buildFlash t-sink`), the def block is bb3 (826: load, setne, the dev test) and the setne goes to the split 3->5 edge block (603 < 0.75 x 826).  Threading changes that ratio only if a path is threaded *through* bb3 (update_bb_profile_for_threading lowers bb3 and rescales its edges): flow threaded through bb3 along the dev edge would raise the non-dev share (`0.73 (826 + F) / 826 >= 0.75` needs F >= 23), along the non-dev edge it lowers it (gen_bd264's JTAG case).  bb3's only predecessor is the function entry's JTAG test, so no path into bb3 can know the type is devgl; a thread that starts *on* the dev edge (towards `if (fuse)`, after calls) copies blocks after bb3 and leaves its ratio alone.
- sink only moves the setne because 3->5 is critical (split_critical_edges at the start of the pass; find_bb_for_arg returns the edge's source).  The join always has the JTAG, dev and non-dev predecessors and bb3 always has two successors, so the edge stays critical in any form that keeps the reference's code.
- Stuck as attempts 15 and 16 said; nothing new to sweep.

### exp_t10: the update fallback's forms (gen_bd360 to gen_bd362, expect off)

- gen_bd360 (11 forms: 10 first, positive call tests with a label, the non-update types first, `else { if (type != 10 || !CG) break; goto chk; }`, `type == 9 && CF` / `type == 10 && CG` arms, an `ok` flag, lone 10 test): **`and9`, `if (type == 9 && CF) ; else if (type == 10 && CG) goto chk; else break;`, is 28 loose in loadBlFiles (src without the expect: 46), and IDENTICAL BYTES with the expect kept** (build/bd/a25/and9e.c).  The other spellings of the same CFG (gen_bd361 `not9`, `not9b`, `nest9`: `if (type != 9 || !CF) { if (type != 10 || !CG) break; goto chk; }`; gen_bd362 `go_or`, `go_in`) are the same 28.  What the family shares: the CF-failure path goes on to the `type == 10` test instead of breaking (an extra predecessor there at profile_estimate, which vrp1 threads to the break since type == 9 is known).  It fixes src's setFlashBuild placement; what's left is the CF path's checkBl result test (bb-reorder copies the `if (r)` test after it: `test edi,edi; je` where the reference jumps) and the type-11 no-key block's place.
- 10 first (`g10first`, `cg_ret`, `lone10`) 100, the non-update types first 136, an `ok` flag 150, clearing *pr on success then one `if (*pr) break;` (loadConsoleBlFiles' exp_t9 shape, gen_bd361 `clr*`) 116 and up, the same without the CG goto (gen_bd362 `nogo*`) 34.
- **The window, measured (build/bd/a25/pwin.py):** and9e without the exp_pr expect matches only at p >= 94, so the CG path's `type == 10` edge needs <= 6% at profile_estimate where natural code gives 19.9% (nonequal 28%, PRED_CALL from the suGetCG block, and the else break's early return).  Taking away both early returns (13.7% and CG success 50%) would give x0.56; it needs x0.3.  So exp_t10 isn't a predictor question within the fallback; it would need the CG flow taken out of this path by structure.
- Side result: and9e (both loadBl expects kept) matches at p = 94 to 98 contiguously, where src matches at 96, 98 and 99 only.  Not landed: it removes nothing, and src's if/else-if reads better.  Note it if the param's value ever matters.
- gen_bd363 (160 cases): the and9 family (and9, nest9, nogo) x exp_t10 on/off x loadBl's tail (src, without t5le, without exp_pr, both off, attempt 10's plain `if (xb.type <= BUILD_DEVGL16) break;`) x the size error through fail or its own `*pr = -1; break;` x the barrier.  The family doesn't change what t5le and exp_pr cost (0/7, 2/18, 2/13 together, the same as src); the plain tail is 8 loose with and9 (src: 38 with the barrier kept), attempt 10's near miss (plain tail, size break, no barrier) is now 9 on src (it was 3 in attempt 10).  `nogo` (no CG `goto chk`) with src's tail: 8 loose in loadBlFiles plus displacements.  No new match.
- Read from and9e + plain tail (8 loose): the sig-failed setFlashBuild copy reads e->data (`mov eax,[ebx]`) where the reference recomputes `xb.files[i].data` from i (attempt 21's dom2-before-ivopts thread), and the sig-failed `<= 5` exit gets a `mov edi,-1; jmp` block of its own instead of jumping to the shared one; plus t5le's SE-copy `ja`.  So the plain tail still needs attempt 14's "`<= 5` exit as a statement of its own".

### lab_none: the r = 1 block and the not-entered return, re-read (no sweep)

- bbro of src with precheck and label gone (build/bd/a25/nonone.c, 4 loose / 8 strict): round 4 takes 16 (priority), 27 (priority), 62 (the shrink-wrapped not-entered `xor eax,eax; ret`, key -20), 53 (r = 1, key -14).  53 needs a key below -20: frequency 21 or more, or a predecessor that ends a trace (bb_to_key's priority).  Its only predecessor is the crossjumped malloc test (21), which sits inside trace 28 (20, 21, 22) because 22 (the copy, 90%) always follows it; so the priority route is shut.
- r = 1's frequency: the two inlined defaultBl60 sites (60 + 76 at .optimized) x 10.1%.  The sites can at most reach the glitch test's true flow (716 x 29% = 207.6) and need about 208, so the glitch test itself has to change: it needs >= 34% with the `||` call form or >= 44.5% with src's two calls, and has 29% from PRED_CALL (the loadBaseFile block is dominated by it and holds a call; the break side goes to the switch join, which isn't).  Attempt 24's lever would need a second predecessor of that loadBaseFile block; the only code that could supply one is case 25's own `loadBaseFile(e->name, e)`, and sharing it means a merged case 24/25 nobody would write.
- The not-entered side: its 20 is the loop's PRED_LOOP_EXIT (first match, 9% / n_exits = 4.5% with the `i < nFiles` and `if (r) return -1` exits), halved by shrink-wrap's duplicate.  A third exit would give 3%, but diagnostic dead exits (`if (i == 0) return 0;` once or twice, build/bd/a25/diag_x1.c, diag_x2.c) cost 121 and 131 loose: the `if (r)` exit's probability drops too and the whole loop body moves.  An expect on the loop condition (diagnostic) 34.
- Stuck as attempt 22 said.

### Don't retry (attempt 25)

- exp_devgl by any threading idea: bb3 can't get a predecessor that knows devgl (see above).
- exp_t10 by the fallback's spelling: the and9 family (gen_bd360 to gen_bd362) is the best natural form at 28 loose and the measured window (<= 6% on the CG path's `type == 10` edge) is out of reach of every predictor combination.  10 first, `ok` flags and clear-on-success forms are 100 and up.
- loadBl's tail in the and9 family (gen_bd363): t5le and exp_pr cost the same as on src.
- lab_none by the not-entered return (n_exits; diagnostics only) or by the r = 1 block's trace priority.

### Costs now (strict/loose, removed alone; 12 tricks, unchanged)

lab_t5le 7/0, exp_pr 18/2, pin_d 23/14, exp_devgl 43/7, pin_size 82/40, exp_t10 116/46, vol_fail 296/126 (on and9e: 232/60), lab_none 333/231 (4/8 with the precheck gone too).  On the and9e base (build/bd/a25/and9e.c, IDENTICAL) every other single costs the same as on src.

### What to try next

- exp_t10 is now known to need its CG path at <= 6%, i.e. a structural change, not a predictor; the and9 family (28 loose) is the closest natural fallback.  If loadBl is ever rewritten as a whole (attempt 9's reconstructions), start from and9 + the plain tail (8 loose with exp_t10 kept).
- vol_fail halves on the and9 family (60 loose against 126): worth a look at the barrier with that fallback, e.g. attempt 10's mergephi2 reading redone on and9e.
- Otherwise build stays at 12: each remaining frequency hint has a measured window that natural predictors can't reach (exp_devgl 75% against 73%, lab_none's glitch test 34%+ against 29%, exp_t10 6% against 19.9%, t5le/exp_pr per attempt 18's formula), and the pins are IRA ties.

## Attempt 26

Goal: vol_fail (the empty asm at loadBl's `fail:`) on attempt 25's and9 base, then the other loadBl tricks on whatever base that gives.  Generators gen_bd370 to gen_bd374 on src as of 9744ca00 (all apply the and9 fallback in a PRE step unless they say otherwise).  Scratch in build/bd/a26 (not kept): `dumps.sh file.c outdir` (all tree dumps with vops, plus expand/jump2/bbro), `m1.sh file.c` (loadBlFiles' -1 sets per RTL block at expand and jump2, and jump2's crossjumps), `negs.py dump` (every edge carrying -1 into a PHI at a tree pass, with the source block's chain position), `fd.sh file.c [fn]` (compact objdump diff against the reference, relocations and addresses dropped).

### What keeps `fail:` with the barrier, read on and9e (IDENTICAL) against and9e minus the barrier (`nob`, 60 loose)

- nob: fail (fre3 bb 106, preds t5le `*pr` test 25, size log 83, smc test 102) has a virtual PHI and is removed by mergephi2, as attempt 10 read on src: the smc and t5le edges are split into new forwarders (they also reach the `if (r)` join directly), the size log goes straight to the join.  vrp1 then redirects all of them past the `if (r)` test with FSM `nocopy` threads (`Registering FSM jump thread: (83, 107) incoming edge; (107, 127) nocopy`: the join holds only the test, so each edge is redirected on its own and no shared copy is made).
- and9e: the asm keeps fail through every pass.  At crited1 its preds are the size log (84) and two split-edge forwarders (130: the signature-failed `<= 5` exit, 189: the smc test); **PRE's tail merge** (`find_duplicates: <bb 130> duplicate of <bb 189>`) merges the two forwarders into one block with a virtual PHI (`.MEM_55 = PHI <.MEM_243(24), .MEM_466(123)>` at .optimized), which survives because no mergephi runs after mergephi3 (104t).  At expand: [merged forwarder] -> [fail: asm, -1 appended] -> log, i.e. the reference's 33d4 block with the size log, the smc test and the signature copy in front of it.
- In nob tail merge also merges the two forwarders, but they then go straight to the log: no virtual PHI is needed, so the block is an unprotected empty forwarder and the post-optimizing cleanup removes it.  The size log keeps its own -1 (`mov edi,-1` scheduled before its call: the first difference).
- So for no asm, the reference needs a GIMPLE block in front of the log that the size log reaches and that holds a PHI or a statement at expand.  A forwarder with a PHI survives only if it is made after mergephi3 (dom2, tail merge, later threaders); one without PHIs only if a predecessor also reaches its successor directly with another r (remove_forwarder_block's phi_alternatives_equal), which after vrp1's threads of `if (r)` no -1 source does (the smc test's other edge goes to the latch, the size log has one successor).
- Crossjump can't do it at RTL either (attempt 10's rule, re-checked with `m1.sh`): the size log's block (expand bb 105) is lower than every wholly matched -1 block (split edges 128 to 152, placed right before the log), so it is always the 'from' side and isn't wholly matched; it can't be the log's fallthrough predecessor while .rdata pins it before cases 27 and default.

### Sweeps (barrier off in all; loadBlFiles loose/strict)

- gen_bd370 (55 cases): each source to fail or its own -1 (`*pr = -1; break;` / `return;`), the tail with or without t5le and the `*pr` expect or plain, and a `bad` flag set at the sources with one `if (bad) *pr = -1;` after the switch.  Best `brk g plain` (the size log's own -1, attempt 10's near miss on and9) 17/107; src's three gotos 60; the flag forms 94 and up (vrp1 threads the flag's test the same way).
- **gen_bd371 (40 cases), fail's position in the source.**  `c2`, fail closing case 2 (`if (e->offset) break; fail: *pr = -1; break;`, so the smc test falls into it): **9/81**, and t5le makes no difference there (9/81 with or without it; with exp_pr off too 11/85).  Mechanism: split_edge_bb_loc puts mergephi2's split forwarders after their source only when fail's prev_bb falls into fail; with fail at the end they all go where fail was.  What's left at 9: the size log's own -1, the CF/case 6 checkBl path's `test edi,edi; je` copy where the reference jumps to the shared test at 2f23, and the CG path jumping to the shared checkBl call where the reference has its own copy.  The label inside the size log's if or inside an `if (!e->offset) {..}` block (`c23`, `c2b`) is the same as the end (60), and moving case 2 ahead of case 23 is worse (17).
- gen_bd372 (20 cases): a local `uint32_t r = 0` stored once (`*pr = r;`, fail storing -1) or returned (`static uint32_t loadBl(e, i)`, `return -1;` at fail, the caller `r = loadBl(e, i);`), fail at the end or in case 2: returned with c2 15/88, returned at the end 65, stored once 334 and up (it changes inlining: defaultBl60.isra differs).
- gen_bd373 (88 cases), the c2 position with the barrier kept: IDENTICAL (on and9 and on src's fallback), so the position is free.  Every other loadBl trick costs the same on it as on src (t5le 0/7, pin_d 14/23, the constant_p entry 26/78, exp_t10 28/80 on and9) except exp_pr: **0 loose / 14 strict** (src 2/18): only the type-11 block's `.p2align` and one other padding move, the same mechanism as before.
- gen_bd374 (80 cases): c2 without the barrier x the fallbacks (src, and9, nest9, nogo, type == 10 expect on or off) x the size error through fail or its own -1 x the tail forms.  Best `src t10 brk plain` 9/37 with no other function moved: that is attempt 10's near miss (the size log's own -1, fail with case 2 alone, plain tail), unchanged by the c2 position (fail has one predecessor there); its three differences are the size log's -1, appendAddonPatches' block placed after the latch, and the SE copy's `ja`.
- Hand runs (build/bd/a26/t1.c, t2exp.c): fail inside the tail's `<= 5` arm (`if (!*pr) break; fail: *pr = -1; break;`, so the `*pr` test falls into it and its split forwarder lands before the size log): 93 loose, 100 with the expect: vrp1's joiner copies take that edge away before it matters.

### Why no natural form was found (the mechanism, as far as it was read)

The reference's 33d4 block is the size log's, the smc test's and the signature copy's -1 in one block.  It can only come from (a) a GIMPLE block in front of the log that the size log reaches and that lives to expand, or (b) crossjump.  (b) is shut by block order (above).  For (a), mergephi2/3 remove any empty block with a PHI, cleanup removes any empty block without one unless a predecessor also reaches its successor with another value, and after vrp1's FSM threads no -1 source has such a second edge.  The asm block lives, and PRE's tail merge then builds the PHI block in front of it.  Every source shape tried (gotos, own -1s, a flag, a local returned or stored once, label positions, case order) runs into one of those three rules.  The only ways left would be a statement in fail that GIMPLE keeps and RTL drops (an asm, a clobber of a variable that stays addressable: nothing natural in loadBl), or a -1 source with a second edge to the log carrying another r (a behaviour change).

### Don't retry (attempt 26)

- vol_fail by the -1 sources' forms on and9 or src (gen_bd370: own -1s, `return`, a `bad` flag), by a local r stored once or returned (gen_bd372), by fail's label inside the size log's if, inside an `if (!e->offset)` block, in the tail arm or with case 2 moved first (gen_bd371, hand runs).
- Crossjump routes for the size log's -1: its block is always lower than every wholly matched -1 block, and .rdata keeps it before cases 27 and default.
- The c2 position with loadBl's other hints (gen_bd373): it moves only exp_pr's cost (0/14, still the type-11 `.p2align`; no p from 75 to 99 matches it).

### Costs now (strict/loose, removed alone; 12 tricks, unchanged)

On src (attempt 25's numbers, not re-measured: src is unchanged): lab_t5le 7/0, exp_pr 18/2, pin_d 23/14, exp_devgl 43/7, pin_size 82/40, exp_t10 116/46, vol_fail 296/126, lab_none 333/231.  vol_fail on other bases: and9 232/60, **and9 + c2 81/9** (with t5le off too 81/9, with t5le and exp_pr off 85/11), attempt 10's near miss with c2 37/9 (vol_fail, t5le and exp_pr together, no other function moved).  On and9 + c2 with the barrier (IDENTICAL, drafts/build_loadBl_c2_fail.patch): exp_pr 14/0, the rest as on src.

### What to try next

- vol_fail: the two open routes are a GIMPLE statement at fail that expand drops (nothing natural is known) and a -1 source that also reaches the log with another r value (would change behaviour unless such a path exists in the reference; none was found).  Otherwise vol_fail stays.
- If loadBl is ever rewritten, start from and9 + c2 (fail closing case 2): it's IDENTICAL with the barrier and the cheapest base without it (9 loose, t5le free there).
- exp_pr on and9 + c2 costs no instructions, only the type-11 block's alignment (attempt 18's frequency rule); a natural change to that block's frequency would land it on that base.

## Attempt 27

Goal: on attempt 26's and9 + c2 base (drafts/build_loadBl_c2_fail.patch, IDENTICAL with the barrier): exp_pr and t5le through the alignment they cost, then exp_t10.  Generators gen_bd380 on, on src as of 7a9a2b41 (gen_bd380.c2base rebuilds the base from src).  Scratch in build/bd/a27 (not kept; `mk.py in out hint,hint` writes a bdhints.off copy).

### exp_pr and t5le on the c2 base: which alignment, read (`bddump.sh f loadBlFiles alignments`)

- Base: bb 102 (sig-failed log + its `<= 5` copy, 29), 103 (`cmp 14; mov edi,-1; jne`, 26), 104 (its setFlashBuild copy, 4), 105 (the type-11 block, 22), ..., 110 (SE copy, 4), 111 (jmp after it, 0), 112 (5/17's no-key log, 17, aligned: 17 > 10 x 0).
- exp_pr off (14 strict, 0 loose): **two** alignments move, not one.  The sig copy's P(<= 5) goes to 100% (103 and 104 drop to 0), so 105 is aligned (22 > 10 x 0); and the SE copy's P(<= 5) falls (formula: the `*pr` test's q enters both copies), so 111 becomes 2 and 112 loses its alignment.  t5le off: only the second (111 = 2).  Both off: 2/13, the SE copy's `jbe` becomes `ja` (P(<= 5) under 50%) and the alignment moves from 112 to 105.
- Why q is 50% on this base (profile_estimate): the `*pr` test's two arms are both early returns now (fail's block `*pr = -1; break;` has the return block as its single successor, so every edge into it gets PRED_TREE_EARLY_RETURN not taken, and so does the break edge): 39% and 61% cancel.  On src it was 61%.  Attempt 18's formula still needs q <= 4.4% with the label (p = 85%).

### exp_pr through the return predictor (gen_bd380, 48 cases): closed, as attempt 9 said

- The 2% exp_pr gives is what PRED_NEGATIVE_RETURN gives (4% in gcc 6, it fires on a negative INTEGER_CST in the return PHI): loadBl returning its result (`static int loadBl(e, i)`, `return -1;` or `r = -1; break;` at fail, the caller `r = loadBl(e, i);`) gives the `*pr` test 4% with no expect.  But it also lands on the other two -1 sources: the size test goes from 80.1% to 9.7% (it needs the nonequal heuristic's hot error path, attempt 15) and the smc test from 50% to 96% towards its break.  int forms 310 loose and up in loadBlFiles; uint32_t return (an unsigned -1 is a positive constant, so no prediction) 8/26 with the expect, 26/43 without; int return with a uint32_t local 232.  Attempt 9's gen_bd202 rule ("a helper returning r puts return predictors on its arms") holds on the c2 base.  Don't retry.

### exp_t10: the hint is on the CG success edge's flow, and it is two layout effects (read, diagnostics)

- Diagnostic d1: the expect moved from `type == 10` to the CG success test (`type == 10 && __builtin_expect(suGetCG(..) != 0, 0)`) is IDENTICAL.  With exp_pr off too (e1) and the param varied, d1's loadBlFiles is exp_pr's 14 strict for p >= 82 and 38 at p <= 80: the CG success edge needs <= 18% (natural 61%, the failure break's early return).  Load failure at 2% (d4, 182 loose) or `type == 9` at 98% (d5, 82) are not the same thing.
- What the 28 loose (exp_t10 off on the c2 base) are, from bbro (`bddump.sh .. loadBlFiles bbro`; bddump.sh now takes `BDP=N` for the param):
  1. **The type-11 block (bbro 24) drops from 22 to 18.**  vrp1 threads CG's flow into chk with type 10 known, and that flow is taken out of the shared checkBl copy's `type == 11` test, so more CG flow means a colder type-11 block.  At 18 it loses its round-4 tie with block 18 (21) and moves to the end (the 24 lines of moved code).  It needs 21 or more, and less than block 29 (31 to 33), or it moves before the sig-failed log (e2, 34).
  2. **The merged checkBl call block (bbro 116, type 9's non-SE path 70 + CG success) reaches 99**, over connect_traces' duplication threshold (max entry frequency 882 x 100 / 1000 = 88), so bbro copies the `if (r)` test into it (`Duplicated bb 117`, `test edi,edi; je`: the 2 loose lines).  With the expect it is 73.  It needs CG success flow <= 17 (29 natural): CG success <= 35%, or P(type == 10) x P(success) <= 7.0% (12.1% natural).
- **gen_bd382 (constant_p weight x exp_t10 x the entry's type value, 52 cases): effect 1 can be fixed by the __builtin_constant_p entry's weight.**  `(char *)__builtin_constant_p(i) == (char *)1 && __builtin_constant_p(type) == 1` (`pi it`) or the mirror (`ii pt`) with exp_t10 off: **2 loose / 53 strict in loadBlFiles** (the strict lines and the other functions' 40 are displacement from the 2 extra instructions), bbro 24 at 30.  Only effect 2 is left.  With the expect kept those weights cost 26 (the block is then too hot, as attempt 14 found).  The weight forms with only one constant_p (`pi x`, `x pt`) are 28/80.  The entry's type value (18, type) makes no difference or is worse.
- On that near miss (build/bd/a27/w1.c), t5le off and exp_pr off each add only 3 strict lines (2 loose unchanged), and both together 4 loose / 59 strict, so the alignment picture changes with the type-11 block's weight too; it can't be read cleanly while the dup shifts everything after it.
- gen_bd381 / gen_bd383 (14 + 42 cases): CG arm forms on the base and crossed with the weights: nested `if (type == 10) { if (!CG) break; goto chk; }` and `if (CG) goto chk; break;` are the same code as and9 (2/53 with `pi it`); `nogo` (CG success falls through to the SE test) 8/74; CG calling checkBl itself (`own10`, `owntype`, `ownnest`: PRED_CALL on the success edge, attempt 16's idea) 45/218 on the base, worse with the weights: the CG checkBl call block then crossjumps differently and the could-not-read log moves (attempt 16's reading still holds).
- Why no natural form lowers CG's success flow: the success edge goes to chk (a join, so no PRED_CALL), the failure edge to the return block (early return, which raises success to 61%); type == 10 is nonequal + PRED_CALL + the else-break's early return (19.9%).  Without both early returns it would be 13.7% x 50% = 6.85%, just under the 7.0% needed, but every break in loadBl goes to the return block, and moving the could-not-read test into loadBl (attempt 21's gen_bd323) costs 95.  And even at 17 the type-11 block (with `pi it`) would sit at about 32 against block 29's 32: a knife edge.
- gen_bd384 (18 cases): the fallback's order and spelling x weights, exp_t10 off.  src's own if/else-if, and9 and `type != 10 || !CG` are all 2/53 with `pi it` / `ii pt`; 10 first in any spelling 56 and up.  **The near miss doesn't need the and9 or c2 reshaping: on src itself, exp_t10 off plus `__builtin_constant_p(type) == 1` in place of the pointer compare is 2 loose / 53 strict in loadBlFiles** (drafts/build_loadBl_t10_weight_nearmiss.patch, 93/42 over the object with the displaced callers).  The two `__builtin_constant_p` stay, so it would remove exp_t10 and add nothing, if the dup went.

### The dup (effect 2), worked out

- 116 = 559 (the arm) x [(1 - f) x 0.28 x 0.919 (load ok, type 9, not SE) + f x 0.863 x 0.199 x 0.61 (load failed, not 9, 10, CG ok)] with f = P(load failed) = 50%: 70.8 + 29.  The threshold is 88 (`max_entry_frequency` 882 is the entry block; the loop's iteration estimate fixes it).
- Ways to get under it, and why each is shut: CG success <= 35% (needs a predictor on the success edge: only PRED_CALL, i.e. an own checkBl call, which crossjumps differently: gen_bd381/383); P(type == 10) x P(success) <= 7% (needs both of CG's breaks to stop being early returns: every break in loadBl reaches the return block); f >= 66% (needs PRED_CALL against the load-ok arm, whose first block is the SE test's `type == 9`, no call); `type == 9` in the SE test at 13.7% instead of 28% (needs a call in the SE arm).  The block 117 copy can't be avoided by size or trace shape (it's the 4-byte `test edi,edi; jne` single-block trace before the latch, as in the reference).
- Diagnostic `--param max-grow-copy-bb-insns` (2, 4, 6) to stop the copy: it changes copies all over the object (base.c 625 strict at 6), so it can't isolate the dup.

### Don't retry (attempt 27)

- exp_pr by returning r from loadBl (gen_bd380): NEGATIVE_RETURN gives the `*pr` test 4%, but also flips the size and smc tests (attempt 9's rule).
- exp_pr / t5le by the joiner formula on the c2 base: q is 50% there (both of the `*pr` test's arms are early returns), still far from 4.4%; nothing new for p or S / Xc.
- exp_t10 by CG arm forms (own checkBl, nogo, nested, `type != 10 || !CG`, 10 first) with or without the weight change (gen_bd381, gen_bd383, gen_bd384).
- The constant_p weight with exp_t10 kept (gen_bd382: 26 loose, the type-11 block too hot) and one-constant_p weights (28/80 with exp_t10 off).

### Costs now (strict/loose in loadBlFiles unless said; 12 tricks, unchanged)

On src: lab_t5le 7/0, exp_pr 18/2, pin_d 23/14, exp_devgl 43/7, pin_size 82/40, exp_t10 116/46, vol_fail 296/126, lab_none 333/231 (not re-measured; src unchanged).  New: **exp_t10 with the constant_p entry's second compare as `__builtin_constant_p(type) == 1`: 53/2 in loadBlFiles (93/42 in the object)**, the same on and9 + c2.  On and9 + c2 with the barrier (IDENTICAL): exp_pr 14/0, lab_t5le 7/0, both 13/2, exp_t10 80/28, vol_fail 81/9.  On the weight near miss: t5le off +3 strict, exp_pr off +3 strict, both 59/4.

### What to try next

- exp_t10 is now one bbro duplication away (drafts/build_loadBl_t10_weight_nearmiss.patch): the merged checkBl call block must stay under 88 with CG's natural flow, i.e. about 12 of its 99 must go.  Any natural change that lowers the type-9 non-SE checkBl path (70.8) or CG's success flow (29) by that much, without moving the type-11 block out of [21, block 29's ~32) (it rises as CG's flow falls: 30 at 29, 34 at 1 with this weight), lands it.  Check candidates with `bddump.sh f loadBlFiles bbro` (block 116's frequency, `Duplicated bb 117`) before scoring.
- t5le and exp_pr: their alignments move with the type-11 block's weight; on the near miss each costs only 3 strict lines, so once the dup is gone, re-measure them there first.

## Attempt 28

Goal: exp_t10 from attempt 27's near miss (drafts/build_loadBl_t10_weight_nearmiss.patch: exp_t10 off, the constant_p entry's second compare `__builtin_constant_p(type) == 1`; 2 loose / 53 strict in loadBlFiles), i.e. take about 12 of the merged checkBl call block's 99 away so bbro doesn't copy the `if (r)` test into it.  Generators gen_bd390 on, on src as of f2823155 (each applies the near miss in gen_bd390's PRE).  Scratch in build/bd/a28 (not kept).  New tools: `bddup.py gen.py` (bdrun.py's scoring plus loadBlFiles' `Duplicated bb X<-A[freq of A]` lines from the same compile's bbro dump) and `bdblocks.py build/bd/dump/loadBlFiles.bbro` (bbro's final blocks: new index, trace-list index, frequency, calls and REG_BR_PROB, to tie a trace-list frequency to code).  gcc.gnu.org's git web is behind bot protection now (WebFetch gets an Anubis page), so bb-reorder.c couldn't be read; everything below is from dumps.

### What block 116 is, read off bbro (`bdblocks.py`) and the reference

- 116 is the crossjumped tail `mov [esp],eax; call checkBl; mov edi,eax` (reference 36e8), and its frequency is the sum of the two blocks crossjump merged: the type-9 non-SE argument block (old 115, 72; reference 36d2) and CG's argument block (old 114, 27; reference 320f, which jumps to 36e8).  try_crossjump_to_edge adds the redirected block's whole frequency.
- The type-9 block is fed by the 'S' test (old 11, 78: the S-false 72% plus E-false 28% x 72%, so 92% of it).  78 is 28% (the SE test's `type == 9`, nonequal) of load-ok (257) plus CF success (21.4): vrp1 threads the CF path through the `type == 9` block, but update_bb_profile_for_threading takes its flow out of the true edge, so the S test keeps 0.28 x (257 + 21.4).  So in loadBlFiles units **116 = 0.2576 x (257 + CFok) + CGok = 66.2 + 5.5 + 27**, CGok = 257 x 0.863 x 0.199 x 0.61.  The reference has the same blocks (load-ok type 9 tests `cmp esi,9` at 3500 and jumps to the shared S test at 36c7, as the CF path falls into it), so the composition is fixed by the bytes; only the flows can move.
- Confirmed by a diagnostic (gen_bd390 `u16`: the SE test as one `*(uint16_t *)e->data == 0x4553` compare, 28% for SE instead of 7.8%, so the type-9 block gets 72% of 78): **no dup, 5 loose / 50 strict, and every other function back to matching** (the displacement goes with the copy).  The 5 loose lines are only the word compare itself.  So the near miss is exactly this one frequency.
- On that diagnostic base the other loadBl hints were re-measured (gen_bd393): **lab_t5le is free** (5/50, unchanged), exp_pr costs 1 loose (6/43), both together 6/43; pin_d 19/73, the plain `else` 58, vol_fail 64 (and the copy comes back: its 116 is 141).  So a natural fix of the copy would take exp_t10 *and* t5le, and leave exp_pr one line away.  Saved as drafts/build_loadBl_t10_u16_diag.patch (`patch -p0`; diagnostic, not a candidate: the word compare isn't the reference's code).

### Why no natural predictor gets 116 under 88 (read from loadBl's profile_estimate, `bddump.sh .. loadBl t-profile_estimate`)

In loadBlFiles units, with f = P(load failed), s9 / s10 the CF / CG success probabilities and p10 = P(type == 10 | failed, not 9): **116 = 0.28 x 0.92 x 513 x [(1 - f) + f x 0.137 x s9] + 513 x f x 0.863 x p10 x s10**; at f = 50%, s9 = s10 = 61%, p10 = 19.9% that is 66.2 + 5.5 + 27 = 98.7.  Each factor and what fixes it:
- f (`if (*pr)` after the load): no predictor applies (compare with 0, no pointer).  PRED_CALL against load-ok would need the load-ok edge's dest to hold a call and be dominated by the load test, but that dest is the SE test, which the CF path also enters.  Needs f >= 66%.
- The SE test's `type == 9` (28%) and the 'S' / 'E' compares (28% each): the opcode-nonequal heuristic, which any `==` / `!=` of a non-zero value gets (`!(x != 'S' || ..)`, nested ifs, `x - 'S' == 0` all fold back; gen_bd390 `nest`, `ne`: the same 99).  `(a == 'S') & (b == 'E')` (one cond, 50%) changes the code (`amp` 74 loose, `amp3` 246); an early-inlined `isSe(d)` helper (bool PHI, 50% join) loses the copy but costs 114 (`helper`).  The S test's flow is 0.28 x (everything that enters the `type == 9` test): flow that vrp1 later threads through it with type known (either way) still counts at 28% of the total, so extra predecessors only raise it, and the CF path entering the S test directly (skipping the type test) is worse (0.28 x 257 + 21.4 = 93 against 78).
- s10 and p10: the CG failure and the other types' `else break` are early returns (every break in loadBl reaches the bare return block; the heuristic only checks that the dest's last statement is the GIMPLE_RETURN, so statements in front of it don't help).  Without both early returns CGok would be 513 x 0.5 x 0.863 x 0.137 x 0.5 = 15.2 (116 about 87, just under).  The only way found to take them away is the could-not-read log inside loadBl after the switch (attempt 21's gen_bd323, rerun on the near miss as gen_bd394, 48 cases): 95 loose at best, and its merged block is then 128 (every arm's probabilities move).
- CG calling checkBl itself (PRED_CALL on the success edge, gen_bd391 `own10`, `owntype`, `own10b`): the copy goes (CG success 29%, 12.8), but CG's call now crossjumps with case 6's checkBl (the same register use) instead of the type-9 tail, which moves the could-not-read log: 83 loose.  In the reference CG's arguments go through eax and its jump lands at 36e8, three insns before the type-9 call's end, which is the shared GIMPLE copy of chk (vrp1 groups the S-false, E-false and CG edges into one thread copy with type as a PHI <9, 9, 10>), not an RTL crossjump (that needs 5 insns or a wholly matched block); so CG has to `goto chk`, and then its success edge goes to a join and can't get PRED_CALL.
- The threshold side: max_entry_frequency is loadBlFiles' entry (882 = the loop's two 4.5% PRED_LOOP_EXIT exits, before inlining), so it would need about 13% fewer iterations, which also moves bbro's round thresholds (exec 500/200/50 per mille of it: block 3 at 450 is round 1 only while the entry is <= 900).  The none test spelled as the other loops in build.c have it (`if (!strnicmp(..) && !e->crc) continue;`, gen_bd392, 4 forms) leaves 116 at 99 and costs 94 loose.  `--param`-free changes to the copied block itself are shut: 117 is `test edi,edi; jne` (4 bytes, a one-block round-3 trace, already connected after 99 as in the reference).
- Threading conserves flow (a threaded copy carries its incoming edges' frequencies; folding a redundant test moves the dead edge's probability onto the taken one), and the only lossy events (dead edges leaving stale frequency downstream, the constant_p entry's mechanism) add flow, they never take it away.  So a repeated or redundant test on the CG or type-9 path (attempt 20's lever) can't lower 116 either; nothing was swept for it.

### Sweeps (near miss base, loadBlFiles loose/strict, bddup.py)

- gen_bd390 (7): SE test spellings.  `u16` (diagnostic) 5/50 no copy; src, `nest`, `ne` 2/53 with the copy (116 at 99); `amp` 74/236, `helper` 114/365, `amp3` 246/472.
- gen_bd391 (6): CG arm forms.  `go2` (`if (CG) goto chk; break;`) 2/53, the same; `nogo` 34/98; `own10`, `owntype`, `own10b` 83/246 (no copy of 117).
- gen_bd392 (5): loop-level none test forms (`continue`, nested `if (r)`): 94/207, copy kept.
- gen_bd393 (16): diagnostic, hint costs on the u16 base (above).
- gen_bd394 (48): the log inside loadBl: 95/264 and up.
- A `__builtin_expect` on `e->crc` with the param varied (to scale the whole loadBl call site) is useless as a diagnostic: the param moves exp_pr and exp_devgl too.

### Don't retry (attempt 28)

- exp_t10 by any predictor on the SE test, the load test, the fallback or CG's arm within the `goto chk` structure: each factor of the formula above is fixed by the nonequal, early-return or call heuristics, and the needed change (f >= 66%, P(non-SE) <= 75.5%, or p10 x s10 <= 7.1%) is out of their reach.
- CG's own checkBl (crossjumps with case 6), the log inside loadBl (95), loop-level none-test forms (94), bool-AND or helper SE tests.
- Repeated / redundant tests to drain 116: flow is conserved through threading and folding.

### Costs now (strict/loose in loadBlFiles unless said; 12 tricks, unchanged)

On src as attempt 27 (not re-measured; src unchanged): lab_t5le 7/0, exp_pr 18/2, pin_d 23/14, exp_devgl 43/7, pin_size 82/40, exp_t10 116/46, vol_fail 296/126, lab_none 333/231.  exp_t10 with the weight near miss 53/2 (93/42 object).  On the u16 diagnostic (no copy): exp_t10 + lab_t5le 50/5 (only the word compare), + exp_pr 43/6, + pin_d 73/19.

### What to try next

- exp_t10 is now known to need one of three flows changed that no heuristic in gcc 6 reaches in loadBl's current structure; the payoff would be two tricks (exp_t10 and t5le, see the u16 diagnostic), maybe three (exp_pr is then one line).  A route would have to change the structure of the 5..21 arm or of loadBl's exits so that the CG and other-type breaks stop being early returns *without* moving the other arms' probabilities (gen_bd394 moves everything).  The 5..21 arm as a static helper of its own doesn't do it (reasoned, not built): the helper is too big for early inlining, so it gets its own profile, with its own bare return block and the same early returns.
- Otherwise build stays at 12; the remaining hints' windows are as attempt 25 listed.

## Attempt 29

Goal: attempt 28's route for exp_t10 (and t5le with it): take PRED_TREE_EARLY_RETURN off the CG failure and the other types' `else break` so block 116 (the merged checkBl call, 99 against the duplication threshold 88) drops under 88, on the near miss (drafts/build_loadBl_t10_weight_nearmiss.patch, 2 loose / 53 strict).  Generators gen_bd400 on, on src as of 1caeb924 (each applies the near miss through gen_bd390's PRE).  Scratch in build/bd/a29 (not kept).

### The early-return rule, and what it takes to switch it off (read from loadBl's profile_estimate)

- At profile_estimate (`bddump.sh build/bd/a29/nm.c loadBl t-profile_estimate`) the return block is bb 98 and fail is bb 97, its prev_bb.  The CG test (bb 7) has only `early return 39%` on its failure edge (s10 = 61%), the `type == 10` test (bb 6) has nonequal 28% + call 29% + early return 61% on the else edge (p10 = 19.9%), exactly as attempt 28 had it.
- predict.c (tree_estimate_probability_bb, from memory, consistent with the dumps here and in image_write/options) predicts an edge e not taken when e->dest is the return block and **e->dest != bb->next_bb**, or, for a bb whose single successor is the return block (and isn't its prev), every edge into bb.  So the only exemptions are: the edge's source is the return block's prev_bb, or the edge goes to a non-empty block that is the return block's prev_bb (fail has that place now, which is why the edges into fail get no early return in src).  Statements in front of the return don't help (they merge into the return block), and an empty block is a forwarder that cleanup removes before profile_estimate.
- So in a natural loadBl the two edges can only lose the predictor by going to a test (not the return block), or to a shared non-empty block laid out last.  Both were measured.

### Sweeps (near miss base, loadBlFiles loose/strict, `bddup.py`: block 116's frequency)

- **gen_bd401, diagnostic (not candidates): the failures to a label at the end of loadBl whose block holds an empty asm** (`out: __asm__ __volatile__("");` after fail, so it is the return block's prev and isn't a forwarder).  CG failure only: **116 = 94** (the formula's 93.8), 17/182; else only: **90**; **both: no copy of 117 (116 under 88)**, 53/210 and every other function matching.  With `out` before fail (fail keeps the last place) nothing changes (99).  So attempt 28's arithmetic is confirmed to the digit: both early returns have to go, and either one alone isn't enough.  What's left in `both` (saved as drafts/build_loadBl_t10_noearly_diag.patch, `patch -p0`, diagnostic only): the CG block (suGetCG test and its argument block) laid out at the end, because the else edge now runs through the asm block and `cmp esi,0xa` jumps to CG instead of falling into it, and the type-11 block moved (it rises as CG's flow falls, attempt 27's effect 1).  Both are the asm block's doing or the constant_p weight's; neither says anything about a natural form.
- gen_bd400 (7 cases): the failures joined at the checkBl result test instead (`goto res` to `res: if (*pr) break;` after the checkBl call, by edge: CG, else, both, all three; and two natural spellings that make the same CFG: checkBl inside `if (!*pr || (type == 9 && CF))` / the SE+checkBl block entered by gotos).  The copy goes in `res_cg` (116 not copied, 159/383) but every form moves the tail: res_cg 159, res_else and res_cg_else 238, res_all, blk_g, cond 272.  Read from res_cg: the failure flow now passes the result test at profile_estimate (61% of it continues into the signature tests), vrp1 threads it away but leaves the tail's frequencies (signature tests turn into a bit test `mov eax,0x20820; bt`, the CG argument block loses its stores, the 25/xell arm moves).  The clr forms of attempt 25 join the failures *before* the SE test and fail for the same reason.

### Other readings (no sweep)

- **Frequencies are rebuilt at inline time.**  optimize_inline_calls returns TODO_rebuild_frequencies when a profile is guessed (gcc 6 tree-inline.c, from memory), so loadBl's frequencies are recomputed from its edge probabilities when it is inlined into loadBlFiles.  A test folded before IPA inlining leaves no stale frequency; only tests folded by vrp1 and later can drain a block (attempt 20's lever), and on the type-9 and CG paths nothing natural is foldable only by vrp1.  This backs attempt 28's "threading conserves flow".
- The switch's 12 targets get even probabilities (`12 edges in bb 2 predicted to even probabilities`: 1, 2, 3, 4, the 5..21 group, 6, 22, 23, 24, 25, 27, default), so each arm is 1/12 of loadBl's entry; 14 targets would put 116 at 85.  Only an extra case label with a body of its own that a later pass merges back could do that, and loadBl has no case whose body could naturally be duplicated (the jump table, .rdata 0f50, has 0 and 26 on default).  Not built.
- The constant_p entry's weight can take more values than gen_bd253 and gen_bd382 swept: `(char *)__builtin_constant_p(x) != (char *)0` (pointer NE, 85%) and `__builtin_constant_p(x) > 0` (positive, 73%) are both false at run time.  But they are hotter than the forms swept, and the hotter weights were already worse (attempt 14, attempt 27 with exp_t10 kept), and the coolest weight (15% x 15%) is src's; no lower one exists with two terms.  Not swept.
- gen_bd402 (32 cases): gen_bd401's mechanism with the existing barrier instead of a new asm (`fail: *pr = -1; out: __asm__ __volatile__("");`, the failures `goto out`), crossed with which failures go there (CG + else, or with CF), four constant_p weights and t5le / exp_pr.  The early returns go, but so does the barrier's own job: a new copy (`dup 120<-119[145]`) and the shared -1 block both move, 88/262 at best (`cg_else pi_it`), 112 and up with t5le or exp_pr off.  The asm has to stay at fail's head (attempt 26's reading: it is what keeps fail through mergephi2/3).

### Why the route is closed for natural code

The two edges lose the predictor only if they reach the return block through a non-empty block that is the return block's prev_bb.  In natural loadBl code that place belongs to fail (whose -1 can't be shared with a failure that keeps loadInputFile's code in r), or, with fail moved (attempt 26's c2 position), to the default arm or whichever case is last; and the fallback's failures come before the SE test and chk in any natural order, so they can't be the last code.  A test in between (gen_bd400) is the other way, and it changes the tail's frequencies, because at profile_estimate the failure flow passes that test before vrp1 threads it away.  So exp_t10 stays, as attempts 25, 27 and 28 concluded, and the payoff attempt 28 described (exp_t10 + t5le, exp_pr one line away) stays out of reach.

### Don't retry (attempt 29)

- The fallback's failures joined at checkBl's result test, by goto or by putting checkBl in an `if (!*pr || CF)` block (gen_bd400): 159 loose and up.
- The failures to a label at loadBl's end, with a new asm (diagnostic gen_bd401) or the moved barrier (gen_bd402): the first is only a diagnostic, the second breaks the barrier's -1 block.
- Higher constant_p weights (pointer `!= 0`, `> 0`): hotter than forms that already lost.

### Costs now (strict/loose, removed alone; 12 tricks, unchanged)

Re-measured on src (`bdhints.py`, 1caeb924): lab_t5le 7/0, exp_pr 18/2, pin_d 23/14, exp_devgl 43/7, pin_size 82/40, exp_t10 116/46, vol_fail 296/126, lab_none 333/231.  Near miss (exp_t10 off, `pi it` weight) 53/2 in loadBlFiles, 93/42 in the object, block 116 at 99.  Diagnostics on it (gen_bd401): CG failure without its early return 116 = 94, the else without it 90, both: no copy (53/210 with an asm block in the way).

### What to try next

- exp_t10: nothing natural is left on the frequency side.  The numbers are now exact (116 = 94 / 90 / under 88 for one, the other, both early returns gone), so a future idea can be checked by arithmetic before it's built: it must take about 11 off block 116 and leave the tail's profile alone.
- The only structural lever not built is the switch's target count (even probabilities over 12 targets: 14 would put 116 at about 85, and every other arm would move by the same factor).  It needs a case whose body is written twice and merged later, which loadBl doesn't have.
- Otherwise build stays at 12, with the windows attempt 25 listed.

## Attempt 30

Goal: a fresh whole-function reconstruction of loadBl with all seven of its hints off together (exp_t10, exp_pr, lab_t5le, vol_fail, both `__builtin_constant_p`, `else if (type)`), scored hint-free so the ranking isn't the one measured with the other hints on; then the pins if nothing comes of it.  Generators gen_bd410 on, on src as of 6083630d; `bdgen/a30lib.py` has `off7(text, keep=())` (the seven off; pin_d kept) and `setfn`.  Scratch in build/bd/a30 (not kept).  Loose lines in loadBlFiles unless said; "+displ" means loadBlFiles changed size, so later functions' call offsets add about 40 lines.

### Baseline (gen_bd410)

src off7: **165**.  On attempt 25/26's and9 + c2 base, off7: **89** (no displacement).  Each hint kept back alone on that base: etype 37 (+displ), vol_fail 84, exp_pr / t5le 87, cp 89, exp_t10 89 (+displ); on src: vol_fail 84, etype 88, exp_pr 138, exp_t10 165+.  So with everything off the and9 + c2 base is still the best start, and `else if (type)` is worth about 50 lines on it.

### Whole-structure axes, everything off (gen_bd411, 288 cases)

Result (src's `*pr` / a local `uint32_t r` returned, caller `r = loadBl(e, i);` / `int` returned / a local stored once), fallback (src / and9), fail position (end / c2 / `return -1;` at each site), signature form (src / verify positive / no key first / no key first + verify positive), tail (src's / plain `if (xb.type <= 5) break;` / `xb.type > 5 && type == 14`).
- Best: `retu and9 c2 nkp plain` 67 (+displ, and 2 .rdata strings move: passed before failed); `ptr and9 c2 nk and` and `retu and9 c2 nk plain` 71 (+displ, .rdata right); `ptr and9 c2 srcp and` 77 (.rdata: passed before failed); `retu and9 c2 src plain` 81 (no displacement; saved as drafts/build_loadBl_a30_hintfree_reconstruction.patch, `patch -p0` on an LF copy of src/build.c: the best hint-free form that keeps .rdata and the function's size).
- The c2 position decides most of it (every `end` form is 119 and up); `int` returned is 381 and up (NEGATIVE_RETURN, attempt 27's rule); `return -1` at each site is the same as `end`.
- The signature's polarity is the biggest single item with everything off: the verify test is 50/50 (PRED_CALL on both arms), and bb-reorder's tie (better_edge_p: equal probability and frequency -> the dest that is the next block) takes the failed log, the then-block.  With the positive form the passed log is first and wins the tie, but it is then also first at expand, so its string moves before the failed one in .rdata.  `else if (type)` gives the passed edge a test block, so only the failed edge gets PRED_CALL (29%).

### `else if (type)` back on those structures (gen_bd412), and the other hints back on the best (gen_bd413)

- With etype kept: `retu and9 c2 nk plain` **25** (+displ), `retu and9 c2 src plain` **35** (no displacement; ptr form 43).  What's left on the 35 is the known set: the size log's own -1 (vol_fail), bbro's copy of the `if (r)` test into the type-9 checkBl block (exp_t10's dup, attempt 27), the type-11 block at the end (cp), the SE copy's `ja` (t5le), and one new one: the sig-failed setFlashBuild copy reads `e->data` instead of recomputing `xb.files[i].data` (attempt 25 saw it on the plain tail).
- **retu is not an equal base:** with every hint back (barrier, cp, exp_t10, src's tail with t5le and exp_pr, etype) it is still 8 loose / 26 strict, only that sig-failed copy (`mov eax,[ebx]` and its own `mov edi,-1; jmp` block).  The ptr form with the same hints is IDENTICAL (attempt 26).  So the returned local trades the CG argument block (right in retu without exp_t10) for the e->data copy.
- no key first (`nk`) on src with every hint kept (gen_bd416): 10 loose +displ, not an equal base either; its hint costs are no lower.  src's signature form is the original one (it is also the Linux build's .rdata order: failed, passed, no key).

### Signature check moved or factored (gen_bd414, gen_bd415)

- The signature check (and the type-14 tail) after the switch, behind `if (r) return r;` or with `!r &&` in the tests, so every arm passes it at profile_estimate and vrp1 threads the known types past it: **220 and up** in every combination (gen_bd414, 192 cases).  The arm is the only place.
- A helper for it (`static int|uint32_t checkSig(e)`: no key 0, failed -1, passed 0; nested like src; or a BOOL helper with the caller setting -1), so the failed `return -1` gets a return predictor in the helper's own profile; and `*pr = verify ? 0 : -1; if (*pr) failed log; else passed log;` / `if (!verify) *pr = -1; if (*pr) ..`: 71 (BOOL helper, +displ) to 124, none better than the same base with src's form (81 / 89) (gen_bd415, 32 cases).

### Case order (gen_bd417, 248 cases)

Every arm moved to every other position, the numeric order and the order the .rdata strings imply, with every hint kept and with the seven off.  With hints: only `6, 5..21, 24, ..` (case 6 first) and default moved one place are IDENTICAL (equal bases); everything else 4 loose and up.  With the seven off: 163 (case 6 first) against src's 165, the rest 165 and up.  The order is src's (or equivalent); no gain.

### New near miss: vol_fail at 1 loose / 7 strict (gen_bd418 to gen_bd421)

- gen_bd418 (hint costs on the equal bases: src, case 6 first, default one place up, and9 + c2, and9 + c2 + case 6 first): every single costs the same as on src on each base, **except vol_fail on and9 + c2 + case 6 first: 1 loose / 7 strict** (src 126/296, and9 + c2 9/81).  Oddly that combined base is not IDENTICAL with the barrier (40 loose): case 6 first and and9 each keep the barrier's match, together they don't, and without the barrier they're the best base found.
- What's left (drafts/build_loadBl_c6_nobarrier_nearmiss.patch, `patch -p0`; vol_fail off, every other hint kept): only the size log's own `mov edi,-1` (scheduled before its call) and `jmp` to the log, where the reference jumps to the shared -1 block (33d4).  The smc test and the sig-failed `<= 5` exit already share that block, made by jump2's crossjump (`Cross jumping from bb 146 to bb 129`: the smc test's split -1 block into the sig-failed one, which is the log's fallthrough predecessor), with no asm.
- Why the size log doesn't join (jump2 dump): its -1 is an out-of-SSA copy appended to its own block (bb 104: args, call, -1, jmp; one successor, so no split block), and the -1 blocks are the RTL edge splits of the smc and sig-failed critical edges, placed right before the log (bb 129).  try_crossjump_bb pairs the size log's edge with the fallthrough edge as `from` = the size log, and with any other edge only as the lower index = the size log (104 < 129); `from` has to be wholly matched for a 1-insn match, and it isn't.  So the size log joins only if its block comes after a wholly matched -1 block in the chain (case 23 moved after case 2: .rdata moves, gen_bd419), or if one of the -1 copies lands in a block placed early (a GIMPLE forwarder after its source that survives to expand, i.e. one with a PHI made after mergephi3, which is what the barrier's PRE tail merge gives).
- gen_bd419 (266 cases): every arm moved to every place on the near miss, with the size error through fail or as its own `*pr = -1; break;`: nothing under 1 loose; moving case 23 or 2 later moves .rdata or is 9 and up.
- gen_bd420 (16 cases): fail's position on the case-6-first base (c2, inside the size log's if, the size arm with its good path first and the log falling into fail, src's end) x src / and9 fallback x barrier: only `and9 c2` without the barrier is close (1/7); `src c2` and `src end` with the barrier are IDENTICAL (equal bases), every other no-barrier form 7/28 (+displ) to 83.
- gen_bd421 (30 cases): on the near miss, the tail (src's, t5le off 1/14, exp_pr off 1/21, both off 3/20, attempt 10's plain 11/85), the size arm's spelling (src, good path first, `else`) and the sig-failed arm's order (`*pr = -1` before the log): the size arm and sig-failed spellings are the same code; nothing moves the size log's line.
- Every other hint removed singly on the near miss (build/bd/a30/singles.py, not kept): exp_t10 29 (+displ), exp_pr 1/21, lab_t5le 1/14, cp 35, etype 55 (+displ), pin_d 15, lab_none / exp_devgl / pin_size their usual costs in their own functions.  So the base makes nothing else free.
- Not landed: the barrier is still needed for the size log's line, and case 6 first plus and9 are two reorderings whose only purpose here would be that line.  If a natural way to get the size log's -1 into a split block (or its block after the -1 block) turns up, this base takes vol_fail.
- The near miss in the retu form (a local returned): 7 loose (+displ).  Worse.

### Case 6 sharing the 5..21 arm (gen_bd423, 36 cases)

For type 6 the 5..21 arm does exactly case 6's work (load; checkBl(.., 6, ..) if it loaded; no CF/CG, SE, signature or type-14 step applies), so `case 6: if (!xb.cbb) break; /* fall through */ case 5: ..` (or `goto load;` from case 6's old place) is the same behaviour, and vrp1 could thread a type-6 copy like the reference's case 6 code (`[esp+8] = 6`, `jmp 2f23`).  It isn't how it was written: 156 loose with every hint kept (src or and9 + c2), 186 with the seven off.

### pins (gen_bd422 and reading)

- pin_d by the case order (IRA ties may follow pseudo numbers, which expand order sets): every arm moved to every place on src and on and9 + c2, pin_d off, other hints kept (266 cases): 14 loose on every equal base (src, case 6 first, default up, case 2 last), 18 and up elsewhere.  The pop order isn't a numbering tie.  On the c6 near miss pin_d is 15.
- pin_size: no new idea with real odds beyond attempt 20's (the kit sum needs its own allocno in ebx from IRA's region at the 14 loop; whole-function forms, scopes, types and helpers are measured).  Not swept.

### Why the reconstruction is no closer than src's structure

Every whole-function axis tried (result through `*pr` / a returned or stored local, fallback, fail's position, the signature form, its position, a signature helper, case order, case 6 sharing the arm) either keeps src's structure or is worse once the hints are put back: the returned local leaves the sig-failed setFlashBuild copy reading `e->data` (8 loose with every hint), the no-key-first form 10, the signature after the switch 220, fall-through for case 6 156.  With everything off the best natural forms are 67 to 89 loose against src's 165, but that gain is attempts 25/26's and9 + c2 reshaping, and on those bases each hint costs what it costs on src.  The one thing the reconstruction found is the base where vol_fail is one line (above).

### Don't retry (attempt 30)

- Whole-function reconstructions of loadBl with every hint off over the axes above (gen_bd411, gen_bd414, gen_bd415): result kind, fallback, fail position, signature form or position, a signature helper (int, uint32_t, BOOL, nested), `*pr = verify ? 0 : -1` forms, the type-14 tail's three forms.  Ranking with hints off doesn't open anything that the hints-on ranking hid, except the c6 base below.
- A returned local (`static uint32_t loadBl(e, i)`) as a base: not an equal base (the sig-failed copy's `e->data`, 8 loose with every hint).
- No key first in the signature block (gen_bd416: 10 loose with every hint, +displ).
- The signature check after the switch (gen_bd414, 220 and up).
- Case 6 falling into or jumping to the 5..21 arm (gen_bd423, 156 and up).
- Case order for pin_d (gen_bd422) or for the size log's -1 on the c6 near miss (gen_bd419: case 23 later moves .rdata).
- On the c6 near miss: fail's position (gen_bd420), the size arm's and the sig-failed arm's spellings, the tail's forms (gen_bd421): none moves the size log's line.

### What to try next

- vol_fail on the c6 near miss (drafts/build_loadBl_c6_nobarrier_nearmiss.patch, 1 loose / 7 strict): the size log's -1 has to land in a block of its own that jump2 can crossjump with the shared -1 block, i.e. either the size log's block comes after a wholly matched -1 block in the chain (a thread copy would: jump-thread duplicates go to the chain's end, like the smc test's bb 121), or the size log's edge into the log becomes critical (then expand splits it and its -1 is a wholly matched block).  Neither has a natural source yet; check any idea against the jump2 dump (`bddump.sh .. loadBlFiles jump2`, the `Cross jumping` lines and the `const_int -1` sets) before scoring.  If one turns up, check that the base is still worth it: case 6 first and the and9 fallback are reorderings chosen only for that line.
- `else if (type)` is still the largest single item with everything off (about 50 lines on any base): the verify test needs one predictor on the failed edge only, and every natural form has PRED_CALL on both arms (50/50, and bb-reorder's tie picks the then-block, which .rdata pins as the failed log).  A non-call first statement on the passed side would do it, but no natural one is known.
- Otherwise build stays at 12; the windows are as attempt 25 listed.

### Costs now (strict/loose, removed alone; 12 tricks, unchanged)

On src (bdhints.py, unchanged src): lab_t5le 7/0, exp_pr 18/2, pin_d 23/14, exp_devgl 43/7, pin_size 82/40, exp_t10 116/46, vol_fail 296/126, lab_none 333/231; etype 128/54, the constant_p entry 78/26.  All seven loadBl hints off together: src 320/165, and9 + c2 199/89, best natural reconstruction 120/67 (+displ, .rdata) or 145/81 (no displacement).  New: **vol_fail on and9 + c2 + case 6 first: 7/1** (exp_pr 21/1, lab_t5le 14/1, pin_d 30/15, cp 119/35, exp_t10 87/29, etype 135/55 on that base with the barrier off).

## Attempt 31

Goal: vol_fail on attempt 30's c6 near miss (drafts/build_loadBl_c6_nobarrier_nearmiss.patch, 1 loose / 7 strict: only the size log's own `mov edi,-1`), by the two routes attempt 30 named: (a) the size log's block after a wholly matched -1 block in the chain, (b) the size log's edge into the log made critical so that expand splits it.  Generator gen_bd430 on src as of 48ce6ada; scratch in build/bd/a31 (not kept: `nm.c` is the near miss, `diag_c23last.c` the diagnostic below).

### Reproduced, and where the -1s are (`bddump.sh .. loadBlFiles t-optimized,jump2`)

- nm.c: 1 loose / 7 strict, as attempt 30 had it.
- At .optimized the could-not-read log (bb 109) has -1 PHI arguments from the smc test (121, critical edge), the sig-failed `<= 5` test (27, critical), the size log (86: the call and `goto 109`, one successor) and the sig-failed setFlashBuild copy (33, one successor; the reference keeps that one as its own -1 too, 37d9).  At expand the two critical edges are split (blocks placed right before the log); 86's and 33's -1 are appended to their own blocks.  jump2: `Cross jumping from bb 146 to bb 129; 1 common insns` (smc into sig-failed, 129 being the log's fallthru predecessor); the size log (bb 104) is in no crossjump.

### Why route (a) is shut (crossjump's pred loop)

From gcc 6's cfgcleanup.c try_crossjump_bb as I remember it (the official git web is behind a bot wall; consistent with every jump2 dump read so far):
- try_crossjump_bb walks the log's preds once.  For each pred e it first tries `try_crossjump_to_edge(e, fallthru, dir_forward)`, so e is always 'from' against the fallthru pred, and only then pairs e with the other non-fallthru preds of higher index (dir_both; can_replace_by gives dir_backward only for a constant set against a register set with a REG_EQUAL note, never for two `(set edi (const_int -1))`).
- So every wholly matched -1 block merges into the fallthru -1 block on its own visit, before any pairing could make the size log the 'to' side.  After that the size log can only be 'from', and it isn't wholly matched (nmatch 1 < min-crossjump-insns 5): no join, whatever its index.
- The only order that would work is the size log as the log's fallthru predecessor at jump2 (a wholly matched -1 block is then 'from' and the size log is split as 'to').  It can't be: rtl_split_edge puts each split block of a non-fallthru edge right before the log and force_nonfallthru()s the old fallthru predecessor, so the last split -1 block always takes that place.  Diagnostic `diag_c23last.c` (case 23 moved last in the switch, so the size log is the last GIMPLE block before the log; .rdata moves, 353 lines): jump2 still has the size log's own -1 (bb 123) and `146 to 129` as before.  Confirmed.
- .rdata pins case 23 anyway: its string (0xeb0) sits between case 4's `KV_alt_dec.bin` (0xe9f) and case 27's `config.bin` (0xee8), so the size log is expanded before case 27 and default.  A jump-thread copy of the size log at the chain's end would leave the original as well (two size logs, not the reference) or move the string.

### Why route (b) is shut for natural code

- commit_one_edge_insertion splits an edge only when its source has more than one successor (or ends in a non-simple jump) and its destination more than one predecessor; otherwise the copy goes at the end of the source or at the head of a single-pred destination.  A single-pred destination after the size log is merged into it by GIMPLE cleanup (gimple_can_merge_blocks_p: log_printf doesn't end a block; nothing natural makes the next block a loop header or a forced label).
- So the size path's last block before the log must end in a conditional at expand that is gone from the final code (the reference's size log is `call; jmp 33d4`).  GIMPLE folds any test whose outcome the size path knows (vrp/dom/threading; a cond whose two edges meet becomes unconditional), and a test it can't resolve (xb.type, or e->size after the call) stays in the code.  A test only RTL folds would be a dead test written for gcc.
- Put another way: a -1 reaches a split block only through a conditional block that only -1 paths reach (the sig-failed `xb.type <= 5` test is the reference's example).  Case 23 has no such test.

### gen_bd430 (36 cases): case 23's forms and case 2's smc spelling on the near miss

Case 23 as src, `own` (`log; *pr = -1; break;`), `ownpre` (the -1 before the log), `ownret` (`return`), `nest` (`if (!*pr) { if (bad) { log; goto fail; } append; } break;`), `nestelse` (good path first inside), `nestown`, `good` (good path first, the log then `goto fail`), `diag_szfirst` (the size test before the load-result test: it reads a failed load's e->size, diagnostic only); the test as `(e->size & ~3) != e->size` or `e->size & 3`; case 2 as c2 (`if (e->offset) break; fail: ..`) or `c2blk` (`if (!e->offset) { fail: *pr = -1; } break;`).
- src, nest, nestelse and good with c2: 1/7, the same code as the near miss.  `e->size & 3`: 7/33 (attempt 15's nonequal effect).  Own -1 forms (own, ownpre, ownret, nestown): 53 (loadBlFiles 13 plus displacements, .rdata).  diag_szfirst 69 and up.  c2blk: 89 and up (the smc test no longer falls into fail; attempt 26's split_edge_bb_loc rule).
- As the mechanism says, no spelling moves the size log's line.

### Not done

- The brief's other items were already measured: fail's position and the size arm's spellings (attempt 30, gen_bd420 and gen_bd421), case order (gen_bd419), and9 / c2 / c6 dropped one at a time (gen_bd420: only all three together give 1/7), t5le and exp_pr on this base (1/14, 1/21).  The size error and the smc error "in one block" would mean cases 2 and 23 sharing code with different strings; the nearest real form is fail itself, which they already share.
- No other trick was attempted.

### Don't retry (attempt 31)

- vol_fail through crossjump in any block order (route (a)): wholly matched -1 blocks always merge into the fallthru one first, and split blocks always take the fallthru place (diag_c23last).
- vol_fail by making the size log's edge critical (route (b)) without a test after the log: no natural source; a test GIMPLE can't fold stays in the code.
- Case 23's spellings on the near miss (gen_bd430): own -1, return, nested, good path first, `e->size & 3`; case 2's smc test as a `{ fail: }` block.

### What to try next

- vol_fail needs a GIMPLE block in front of the log that the size log reaches and that lives to expand (attempt 26's route): a statement at fail that GIMPLE keeps and RTL drops, or a PHI made after mergephi3.  No natural candidate is known, and the asm is the honest form of it.  Unless a new reading of the original's structure turns up (the Linux build has the same single -1 site, attempt 9), leave vol_fail.
- The c6 near miss stays the best base for vol_fail if that changes; its other costs are attempt 30's.

### Costs now (strict/loose, removed alone; 12 tricks, unchanged)

On src: lab_t5le 7/0, exp_pr 18/2, pin_d 23/14, exp_devgl 43/7, pin_size 82/40, exp_t10 116/46, vol_fail 296/126, lab_none 333/231; etype 128/54, the constant_p entry 78/26 (attempt 30's numbers; src unchanged).  vol_fail on the c6 near miss (and9 + c2 + case 6 first): 7/1, unchanged by every case 23 spelling.
