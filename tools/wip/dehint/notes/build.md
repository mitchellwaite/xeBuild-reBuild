# build de-tricking

Goal: `build/bd/reference.o` (copy of a matching build/obj/build.o) byte-identical from plain
`-O3`, with fewer hints.  52 tricks at the start of attempt 1.

## State after attempt 70

**0 tricks** (1 before): exp_devgl is gone; build.c has no hints left and compiles at plain `-O3`.  buildFlash's salt memset and fuse decision are `fuse = initFlash(salt);`, attempt 69's r-class helper with its last line `return fuse & 1;` instead of `return fuse != 0;`.  `!= 0` leaves two statements in the inlined return block after vrp1 (a `_Bool` compare and its int conversion; vrp1 makes the conversion a copy, dce2 deletes the compare, copyprop1 the copy); `& 1` is one statement (vrp1 makes it a copy, copyprop1 deletes it), which takes one name out of the SSA free list that ch2 pops when it copies the six findFile loops' headers, and the findFile(24) loop's nFiles copy then gets a high version again (`i_N != _M` with N < M), as in the original.  `fuse > 1 ? 1 : fuse`, `fuse < 0 ? 0 : fuse`, `fuse % 2`, `fuse &= 1;` and the MIN / MAX spellings are IDENTICAL too.  fncmp MATCH; `sh build.sh` SHA256 matches.  Borderline shapes (attempt 60's table, attempt 68's setKitBuild entries, plus the new row):

| Where | Shape | Why it's borderline |
|---|---|---|
| initFlash (buildFlash's start) | the salt memset and the fuse decision as a helper, `return 1;` for devgl, and a redundant `return fuse & 1;` | new (attempt 70): the helper is chosen so that only IPA inlines it (the memset is its call) and buildFlash gets its profile (devgl as an early return, replaces exp_devgl); `& 1` on a 0/1 value keeps a statement in the return block (JTAG skip off the early-return rule) and is one statement where `!= 0` is two, which is what fixes the loop compare's SSA numbering |
| setKitBuild (loadBlFiles' tail) | `return type == 14;` ignored at its only call | attempt 68 |
| loadBlFiles' tail | `(int)r < 0` | attempt 68 |
| useBuiltIn (loadBlFiles cases 1 and 22) | the built-in payload / core copies as a helper | attempt 60 |
| defaultBl60 | `memmove` for the built-in copy, and not through useBuiltIn | attempt 60 |
| loadBl24 (both loaders' case 24) | two calls where `||` would do | attempt 49 |
| loadBlFiles case 24, second arm | loadBl24's body written out, leading `r = 0;` | attempt 49 |
| loadBlFiles case 27 | the fallbacks as a sequence of `r` tests | attempt 49 |
| findFileOffset / findFileSize | return `int` | attempt 58 |

## State after attempt 69

Attempt 69 landed nothing; src/build.c and build.sh are unchanged, so the count (1, exp_devgl) and attempt 60's review table, plus attempt 68's setKitBuild entries, still stand.  It reopened the helper route attempt 53 had closed, using attempt 68's lever, and got to **2 loose / 2 strict**: one loop compare's operand order.  Attempt 53's memset-holding fuse helper (`dret2`, 3/285) failed only because its JTAG skip went straight to the helper's return block, so that edge picked up the early-return prediction too (19.9%) and the JTAG `fuse = 1` ended up in a block shared with the dev arm (ce1's IF-CASE-2 needs the else block to have one predecessor).  Give the helper's return block a non-PHI statement that lasts until profile_estimate (`return fuse != 0;` on an `int fuse` that is already 0/1, a `_Bool` return type, or an out-parameter store `*fuse = f;`) and the JTAG edge no longer goes to the return block, so it keeps 72/28.  The dev arm's `return 1;` still gets early return (19.1%), the setne stays in the dev test's block and ce1 makes the reference's `mov ebx,1 ... setne; sub; cmp; mov eax,1; cmovbe`.  What's left is an SSA-numbering tie: six inlined findFile loops in buildFlash compare `i` with `xb.nFiles` in an order set by version numbers, and every helper class gets some of them wrong (the best, `int initFlash(uint8_t *salt)` returning `fuse != 0`, only the `if (fuse)` block's findFile(24) loop).  Saved as `tools/wip/dehint/drafts/build_buildFlash_initFlash_nearmiss.patch`.  See "## Attempt 69".

## State after attempt 68 (landed by the orchestrator)

**1 trick** (3 before): exp_devgl in buildFlash.  exp_pr and the `--param` are gone; build.c compiles at plain `-O3` (bdlib's P98 is now `[]`).  The candidate below (drafts/build_loadBlFiles_setKitBuild_candidate.patch) was landed as borderline, at the user's standing rule that plausible author code is landed with a "Borderline, for review:" comment: `static int setKitBuild(uint32_t i, int type)` whose `return type == 14;` is ignored at its only call site, and the tail's `(int)r < 0` (r is 0 or a negative code there).  Both are marked in src.  IDENTICAL; full build SHA256 matches.  The paragraph below is the subagent's, written before landing.

Attempt 68 (as written by its subagent) landed nothing; src/build.c and build.sh were unchanged, so the count (3) and attempt 60's review table stood.  It found why attempt 67's setKitBuild helper leaves 6/31: the inlined body's return block R' always has preds (false edge, call path) (the inline copy makes edges in callee block order); cleanup removes the empty continuation and then R', which leaves the false edge last at the switch join, and vrp1's first thread (the none skip) moves it into slot 0, ahead of the call path, for dom2's FSM search.  If R' keeps a non-PHI statement until DCE (after vrp1), the call path comes first and dom2 threads through the setFlashBuild block as in src: `static int setKitBuild(uint32_t i, int type)` reading `xb.files[i].data`, with an unused `return type == 14;` (or any other non-PHI return expression), the tail `(int)r < 0`, no expect and no param, is IDENTICAL, and `sh build.sh` with build at plain `-O3` gives the right SHA256.  Not landed: the return value is unused at the only call site, so it is dead code chosen for gcc (a trick); saved for review as `drafts/build_loadBlFiles_setKitBuild_candidate.patch` (2 tricks fewer if accepted).  No natural form with the same effect was found (callee shapes, argument spellings, 0 / 1 and pass-through returns, gotos, the kit test inside the helper, callee return types, 132 case-block moves).  See "## Attempt 68".

## State after attempt 67

Attempt 67 landed nothing; src/build.c and build.sh are unchanged, so the count (3) and attempt 60's review table stand.  Attempt 66's leads are closed: tl_k's 4/21 (no param, expect kept) is only the setFlashBuild argument read through the IV (`e->data` CSEs with the loop pointer), with the chain unchanged; p_se moves the SE block to 42; 13 sig_t variants (no-key log or key test outside the helper, tri-state, switch, r passed in, + tl_k / p_se) cost 63 to 200 loose.  New mechanism found: the tail's `if (type == 14) setFlashBuild(..)` as an IPA-inlined `setKitBuild(e, type)` (einline refuses it: growth 6 over 14 / calls) puts a call in the tail test X's >5 successor at profile_estimate, so X gets PRED_CALL (71 / 29) and **the alignment chain closes with no expect and no param** (`(int)r < 0`: SE copy 71.0 / 29.0%, jmp block 1, no-key copy aligned; `r != 0`: 87.5 / 12.5%).  It costs 6/31 in loadBlFiles (+40 call displacements from the shorter code), the same with every helper body, argument and tail orientation tried (a67_kx.py): the inlined helper's false edge is appended last to the switch join's predecessors, vrp1's unordered edge removals move it to slot 0, and dom2's FSM threader then takes the `type != 14` path first and never copies the setFlashBuild block before ivopts (so the sig-failed copy reads `e->data` through the IV and its r = -1 lands in the fail block).  See "## Attempt 67".

## State after attempt 66

Attempt 66 landed nothing; src/build.c and build.sh are unchanged, so the count (3) and attempt 60's review table stand.  It tried helpers over loadBlFiles' 5..21 arm and signature / tail region (a66_h.py, 49 variants): the signature check with its logs (10 forms), the tail (4), the CF/CG fallback (10), load + fallback, load + fallback + SE + checkBl, the whole arm (8), checkBl / case 6 helpers and call-free predicates, each measured on the SE chain at p90 / p99 with the expect and at p0 with `(int)r < 0`.  Nothing that holds a log call is einlined (growth 7 to 19 against the per-call limit), and every IPA-inlined signature helper removes the vrp1 joiner thread that gives src's SE copy its 38.1% (the copy goes to 50%), so the param-alone condition (< 37.5%) moves the wrong way.  Einlined boolean predicates reach profile_estimate as a 50% PHI test (isSe: SE block 42 instead of 7).  Best non-equal variants: tl_k 4/21, p_se 9 loose in loadBlFiles (+40 displacement lines).  Equal bases: checkEntry, loadChecked, isRetailGlitch.  See "## Attempt 66".

## State after attempt 65

Attempt 65 landed nothing; src/build.c and build.sh are unchanged, so the count (3) and attempt 60's review table stand.  It tried buildFlash at whole-function level: the header step, the loads, the fuse setup, the glitch blmod step, the encode step and the slot-overflow writers as helpers, and the fuse decision inside a call-holding setup helper (a65_bf.py).  The loading helper is an equal base (IDENTICAL, exp_devgl off 7/43); the rest cost 66 to 838 loose with the expect kept.  The reading that closes this route: tree-sink's decision on the setne depends only on the dev arm's frequency ratio to the def block (73% < 75%, the opcode-positive 27% on the dev test), and nothing outside the fuse decision feeds that ratio.  IPA's frequency rebuild after inlining recomputes from the same edge probabilities, and a fuse decision inside an IPA-inlined setup helper (initFlash(&fuse) with the header step, kept out of einline by its calls, growth 26) brings its own profile, which is 27 / 73 again because the dev arm can't be an early return there.  See "## Attempt 65".

## State after attempt 64

Attempt 64 landed nothing; src/build.c and build.sh are unchanged, so the count (3) and attempt 60's review table stand.  It took attempt 63's second alignment route for exp_pr (the no-key copy at frequency >= 21 with the SE jmp block at 2) with the key in a local, so that the second key test of attempt 63's `ver_flat` is an SSA value vrp1 can thread: `flat_local` gets no-key 29 and the alignment, but the failed / no-key blocks and the signature strings' .rdata order move (89 loose with the expect, 90 without).  Every single-test form keeps the no-key edge's PRED_CALL (its block has one predecessor and holds the log call), so Pk stays at 85% and no-key at 14.  exp_devgl: 20 more natural spellings of the fuse decision (a64_dev.py: range, switch, ternary, `|=`, a dev local, BOOL / uint8_t fuse, else form, JTAG last, `!fuse &&`) are 7/43 at best; the dev test is still positive-27% and tree-sink still moves the setne into the non-dev forwarder (73% < 75%).  See "## Attempt 64".

## State after attempt 63

Attempt 63 landed nothing; src/build.c and build.sh are unchanged, so the count (3) and attempt 60's review table stand.  It read vrp1's joiner update for the param on its own (exp_pr kept, gcc's default 90) down to the integers: the other copy of the tail test gets P(>5) = (freq26 x (1 - p) - S + freq27 x q) / (freq26 - S) = (74.5 - 41 + 7.5) / 108, because the signature-failed thread runs first and takes min(S x p, freq27 x q) = 7.5 off the `<= 5` side (gcc 6's freqs_to_counts_path / compute_path_counts / update_profile).  Every term is a block frequency fixed by Psig 0.64, Pk 0.85, Pf 0.5, p 0.5 and q 0.1, and rounding can't give the +1 on S it needs, so the param alone has no natural route on this CFG.  A second route to the no-key copy's alignment was found: 112 >= 21 (instead of 111 <= 1) works with 111 at 2, and Pk = 69.8% (PRED_CALL off the no-key arm) gives 29, but only forms with a second pub1bl test do that (57 loose).  Target B by the `<= 5` exit inside the failed arm (attempts 14 and 47) re-run on the current src: 22 loose at best, and it can't close the chain at all (no thread on X, so P(>5) is 50%).  See "## Attempt 63".

## State after attempt 62

Attempt 62 landed nothing; src/build.c and build.sh are unchanged, so the count (3) and attempt 60's review table stand.  It tried attempt 61's lead (a predictor on the checkBl result test) and found it can't be done the way it needs: the closing edge is the *break* side (P(r == 0) has to go under 50%), and every predictor a natural form of that test can get points the other way.  `(int)r < 0` / `<= -1` (opcode positive) sends 73% to r == 0 (215 loose); an `int r` local, checkBl's return type (long, unsigned long, uint32_t, int32_t, ssize_t) and the assignment-in-test spellings leave the test with no predictor (7 / 4 / 2); a static checkBl gets the local calling convention (457 loose).  The new reading is for the param alone: with exp_pr kept at gcc's default 90 (no `--param`), the SE copy's P(>5) is 38.1% and needs < 37.5% (at p91 it is 37.4%).  By the joiner formula that needs S / Xc >= 0.28 (S 41 -> 42 at Xc 149; it is 0.275, Psig 0.64 x Pk 0.85 x Pf 0.5), so freeing the param needs only a 2% rise in the signature-failed share, but Psig, Pk and Pf only take fixed heuristic values (the next one up, Pf = 71%, costs 29 loose).  A diagnostic with 13 switch targets (SE = 6) closes the chain on its own, but the reference's jump table has exactly 12.  See "## Attempt 62".

## State after attempt 61

Attempt 61 landed nothing; src/build.c and build.sh are unchanged, so the count (3) and attempt 60's review table stand.  It measured exp_pr's alignment chain straight off the final `-dA` output for every variant (new `a61_semeas.py`): SE block 109 = 7, the copy of the tail test 110 = RDIV(7 x 50%) = 4 (3.5 rounds up), its jmp block 111 = RDIV(4 x 49.8%) = 2, no-key copy 112 = 14 (aligned only if 14 > 10 x 111).  All 24 of attempt 60's estimate / inline-order / helper edits leave it at exactly 7 / 4 / 2: IPA inlining and its frequency rebuild don't touch loadBlFiles' own blocks (the SE chain is 10000 x 95.5% x 75% / 12 x 50% x 0.28^3 at profile_estimate and nothing after it recomputes those blocks), so that lever can't reach exp_pr.  The only change found that fixes the chain is a call in the SE block (the SE arm calling `checkBl(.., 14, ..)` itself, the else arm the usual one): the 'E' edge gets PRED_CALL (13.7%), SE = 6, 110 = 3, 111 = 1 and the no-key copy is aligned, but the type == 9 test's false edge gets PRED_CALL too (48.8% instead of 28%), and even with that cancelled (diagnostic call) the second call site's CFG moves the 5/17/11 and signature blocks: 124 loose.  exp_devgl: no new lever (attempt 53's einline reading stands).  See "## Attempt 61".

## State after attempt 60

**3 tricks** (5 before): `--param builtin-expect-probability=99` and 2 `__builtin_expect` (`r != 0` in loadBlFiles' tail, devgl in buildFlash).  Removed: **lab_devgl** (the hot `devgl:` label in loadBlFiles' case 24) and **vol_fail** (the empty asm barrier on `fail:`).  loadBlFiles' cases 1 and 22 now call a `useBuiltIn(e, data, size)` helper (malloc, NULL test returning 1, size, memcpy, return 0) that einline takes into loadBlFiles before profile_estimate; with it the r = 1 block is laid out before the suGetCF block without the label.  And case 2's SMC failure is `if (!e->offset) goto fail; break;`, with `fail: r = -1; break;` after the default case (attempt 55's `end` form); on the useBuiltIn base that form needs no barrier at all (attempt 55's base left the size log's 1/7).  IDENTICAL at p95 / p97 / p99 (0/7 at p0 and p90, as before); full build SHA256 matches.  exp_pr 2/4 and exp_devgl 7/43 cost what they did.  See "## Attempt 60".

| Where | Shape | Why it's borderline |
|---|---|---|
| useBuiltIn (loadBlFiles cases 1 and 22) | the built-in payload / core copies as a helper | natural sharing, but chosen because its inlined CFG moves the layout (new; defaultBl60 doesn't use it, see the next row) |
| defaultBl60 | `memmove` for the built-in copy, and not through useBuiltIn | memcpy would do; memmove is chosen for its inline-size estimate; through useBuiltIn costs loadBlFiles 14/34 and console 4/8 (cases 1 / 22 back to memcpy, inside useBuiltIn) |
| loadBl24 (both loaders' case 24) | two calls where `||` would do | unchanged from attempt 49's table |
| loadBlFiles case 24, second arm | loadBl24's body written out, leading `r = 0;` | unchanged |
| loadBlFiles case 27 | the fallbacks as a sequence of `r` tests | unchanged |
| findFileOffset / findFileSize | return `int` | unchanged from attempt 58 |

## State after attempt 59

**5 tricks** (6 before): `--param builtin-expect-probability=99`, 2 `__builtin_expect` (`r != 0` in loadBlFiles' tail, devgl in buildFlash), the empty asm barrier on `fail:`, the hot `devgl` label in loadBlFiles.  Removed: **lab_none** (loadConsoleBlFiles' cold `none:` label and the `nFiles <= 1` precheck that jumped to it).  The three built-in copies (defaultBl60's, loadBlFiles' cases 1 and 22) use `memmove` instead of `memcpy`.  gcc folds memmove back into memcpy only after alias analysis (dce3 / forwprop3 time), so the code is the same, but until then memmove is an ordinary call to the inline-size estimator: defaultBl60 is 14 instead of 18 (einline growth 6 instead of 10), loadBl24 32 instead of 40, so IPA's small-function inliner takes loadBl24 into loadConsoleBlFiles *before* loadXell, and console's blocks come out in the original's order without the label.  defaultBl60's memmove alone does it too (cases 1 / 22 changed for consistency; both IDENTICAL).  IDENTICAL at p95 to p99 (0/7 at p0 and p90, as before); full build SHA256 matches.  Every other hint costs what it did (exp_pr 2/4, vol_fail 58/220, exp_devgl 7/43), except lab_devgl, now 14/34 (57 before).  See "## Attempt 59".

| Where | Shape | Why it's borderline |
|---|---|---|
| defaultBl60, loadBlFiles cases 1 and 22 | `memmove` for the built-in copies into fresh malloc memory | memcpy would do; memmove is chosen for its inline-size estimate (new) |
| loadBl24 (both loaders' case 24) | two calls where `||` would do | unchanged from attempt 49's table |
| loadBlFiles case 24, second arm | loadBl24's body written out, leading `r = 0;` | unchanged |
| loadBlFiles case 27 | the fallbacks as a sequence of `r` tests | unchanged |
| findFileOffset / findFileSize | return `int` | unchanged from attempt 58 |

## State after attempt 58

**6 tricks** (7 before): `--param builtin-expect-probability=99`, 2 `__builtin_expect` (`r != 0` in loadBlFiles' tail, devgl in buildFlash), the empty asm barrier on `fail:`, 2 hot and cold labels (`devgl` in loadBlFiles, `none` in loadConsoleBlFiles).  Removed: **pin_size** (calcBlAreaSize's `__asm__("" : "+b"(size))`).  findFileOffset (build.h) and findFileSize now return `int`, like findFile: after inlining into calcBlAreaSize each result is converted to the uint32_t sums, and those conversion statements move the SSA names PRE hands out, so the kit sum is `size_273 + prephitmp_282` (the reference's operand order, attempt 35's tie) and IRA keeps it in ebx.  Either return type alone doesn't do it.  image_write's `SWAP32_IMAGE_WRITE(findFileOffset(9))` takes a `(uint32_t)` cast marked `TODO(prototype cast)` (with an int the swap's shifts are arithmetic).  IDENTICAL at p95 to p99 (0/7 at p90 and with no param, as before); full build SHA256 matches.  No borderline shape added or removed; attempt 49's review table stands.  The type sweep of every other shared declaration build.c's tricks touch (a58_types.py, a58_ret.py, a58_none.py) found only equal bases or worse.  See "## Attempt 58".

## State after attempt 57

Attempt 57 landed nothing; src/build.c and build.sh are unchanged, so the count (7) and attempt 49's review table stand.  It tried the two loaders at whole-structure level together: the static helpers' definition order (no effect: every placement and order is an equal base, each hint costs what it costs on src), the two loaders as one static loop with a mode parameter (ipa-cp clones it, but the one-line wrappers are inlined into buildFlash first, so the console clone stays out of line: 11600 loose and up), the per-entry work as a static helper with a mode parameter (522 and up), a per-entry helper holding the switch and the could-not-read log so the breaks reach the r test (112 loose and up; the PRED_CALL on the none test it brings doesn't pay for the helper), and the case order of both switches on the loop form (only swapping case 2 and the default is an equal base; console nothing below its 4/8).  See "## Attempt 57".

## State after attempt 56

Attempt 56 landed nothing; src/build.c and build.sh are unchanged, so the count (7) and attempt 49's review table stand.  It took vol_fail on attempt 55's SMC equal base: 13 case-23 forms of the patch-size failure (own -1, -1 before the log, nested, else, good path first, repeated test, ternary, logging or size-check helpers; a56_fail.py) are all the 1/7 or worse, and the dumps (a56_dump.py, a56_trace.py) show the empty `fail` block is removed by mergephi1's CFG cleanup even though the SMC test has a conflicting edge to the switch join (cleanup splits that edge rather than keeping the forwarder), so only a statement RTL drops keeps it, which is the asm.  exp_pr's spellings on the SMC base across p0 to p99 (a56_negp.py) don't interact with the barrier (they add).  See "## Attempt 56".

## State after attempt 55

Attempt 55 landed nothing; src/build.c and build.sh are unchanged, so the count (7) and attempt 49's review table stand.  It read the two focus tricks on the current form.  **vol_fail's 58/220 is not the barrier's own effect**: with the SMC failure spelled `if (!e->offset) { fail: r = -1; } break;` (or `if (!e->offset) goto fail; break;` with `fail: r = -1; break;` after the default case) the source is an equal base (IDENTICAL with the barrier, every other hint costs the same) and the barrier off is attempt 10's **1/7** again (a55_smc.py).  The 58 came from vrp1: in src's fall-through form the `fail` forwarder is removed early, the SMC block becomes a joiner of jump threads (its two preds, the dump and the nand moves), and the threader's profile update leaves the SMC test at 92.5% / 7.5% instead of 50%, so bbro no longer lays the -1 block before the could-not-read join (in 26aca4bb^ those joiner threads were cancelled).  The 1/7 line is still closed (the size log's -1 is a 1-insn tail; min-crossjump-insns only waives the 5-insn minimum for a *wholly* matched from-block, so the log block can't be redirected into the -1 block unless the -1 sits in a block of its own, which only the asm keeps).  lab_devgl: the r = 1 block (arm 1's retest falls into it, with cases 1 / 22's and arm 2's malloc failures) is placed before the suGetCF block only when its heap key carries a trace-end priority, which it gets from arm 2's malloc block ending a **round-2** trace (bbro freq >= 176 = 0.2 x 882; 180 with the label, 51 without); its own frequency doesn't help (a `useBuiltIn(e, data, size)` helper for cases 1 / 22 / defaultBl60 raises it from 37 to 57, an equal base with the label, still 14 loose without).  See "## Attempt 55".

## State after attempt 54

Attempt 54 landed nothing; src/build.c and build.sh are unchanged, so the count (7) and attempt 49's review table stand.  It applied the IPA-inlined-helper lever to exp_pr and lab_none.  exp_pr: the signature check as a call-holding helper (six bodies: 1 on failure, 0 on failure, -1 on failure, a result flag; a54_sig.py) is 63 loose and up even with the expect kept, so the inlined body costs more than any probability it brings, and its -1 return is PRED_NEGATIVE_RETURN (4%), which lowers the signature-failed flow S, the wrong way for the joiner formula (S has to rise to about 62).  The tail with `type == 14` tested first, so `xb.type > 5` guards setFlashBuild directly (PRED_CALL), is 114 loose and up (a54_t14.py).  lab_none: console's case 24 written out with `||` (`xb.glitch2mfg && (load || size)`) gets only a 0.80 share (its loadBaseFile test keeps PRED_CALL: it dominates the merged call block), 6/10 without the label and 2/2 (the size store) with it; written out with two calls it is an equal base.  The size store's place is the alias oracle's: the copy's destination is a fresh malloc result (points-to {HEAP}) and the store a decl ref to xb.files[i].size, so nothing orders them with one copy.  See "## Attempt 54".

## State after attempt 53

Attempt 53 landed nothing; src/build.c and build.sh are unchanged, so the count (7) and attempt 49's review table stand.  It looked for a natural way to keep attempt 52's fuse helper out of early inlining (so IPA scales its early-return profile into buildFlash) and found none: gcc 6's einline refuses a callee only for growth > 14, growth x (calls + 1) > 14, a cold edge (callee cold/hot attributes, noreturn or main: nothing else sets a node's frequency without a profile), a callee not yet in SSA (a call-graph cycle), or uninlinable bodies (va_start, setjmp, alloca, nonlocal labels); the fuse decision is a 6-insn leaf and the only call that runs before it in the reference is the salt memset.  The memset helper is also out on its own terms: with the JTAG test inside and *no* early return on it (`dret2`), the JTAG edge still goes straight to the helper's return block, so it gets early return 61% (80.1% instead of 72%) and the `fuse = 1` block moves out of line (3/285, as `dret`).  In that IPA-inlined form the 5 loop-compare differences of the -fno-early-inlining diagnostic are gone (only the JTAG block differs), so the residue was the diagnostic's.  The Linux v1.16 build (tools/ref/xeBuild64, gcc 4.9.2) has the same inline `setne; sub 4; cmp 1; mov 1; cmovbe` at buildFlash's start and no fuse helper, and the reference has no fuse/devgl string near buildFlash other than "Virtual Fuses set to:", so nothing suggests the original had a helper there.  See "## Attempt 53".

## State after attempt 52

Attempt 52 landed nothing; src/build.c and build.sh are unchanged, so the count (7) and attempt 49's review table stand.  It applied the sharing lever to calcBlAreaSize and buildFlash.  **exp_devgl has a confirmed mechanism now**: a fuse helper whose dev arm is an early return (`int fuse = xb.glitch2mfg != 0; if (dev) return 1; return fuse;`) gets dev = ds(27, 39) = 19.1% in its *own* profile (opcode positive + early return), and once it is inlined by IPA (not einline) that profile is scaled in, the non-dev arm is 80.9% >= 75%, tree-sink leaves the setne in the def block and ce1 makes the reference's `setne; sub; cmp; mov eax,1; cmovbe` (diagnostic with -fno-early-inlining: buildFlash differs from src only in 5 loop-compare operand orders, i.e. SSA numbering).  But every such helper is a 6-insn leaf, so einline always takes it (growth <= 14, no calls) and then buildFlash's own profile re-predicts it at 27% (7/43, as src without the expect).  A call in the helper keeps it for IPA (a51/a50's loaders); the only call that fits at buildFlash's start is the salt memset (diagnostic `initFlash(salt)`: 3 loose, the JTAG early return's own 19.9% moves the `fuse = 1` block), and a helper that clears the salt and returns the fuse flag isn't something an author writes.  pin_size: the CF-area tail (`setPatchSlot; + 2 * imgCfSize`) shared by kit and retail is early-inlined and an equal base (pin still 40/82); the xell room test as a helper (IPA-inlined: it holds the log call) leaves the kit sum unflipped (46 loose without the pin, 10 with it, the xell block's own registers); retail's whole end as a helper isn't inlined (333).  The shared "virtual fuses in use" predicate in addBlsToImage / addUpdateBls costs 20 to 500 lines there.  See "## Attempt 52".

## State after attempt 51

Attempt 51 landed nothing; src/build.c and build.sh are unchanged, so the count (7) and attempt 49's review table stand.  It read lab_none's 4/8 directly off bb-reorder and pinned the exact condition: the r = 1 block gets a trace-end priority (key -100xx) only if console's merged defaultBl60 malloc block starts a round-2 trace and its copy block doesn't follow it, i.e. **176 <= malloc < 196** (0.2 x the entry's 880; src 145 = 716 x guard 29% x loadBl24 share 70%), with round 1 also needing the guard's skip edge >= 440 (guard <= 38.5%).  So guard x share has to land in [0.246, 0.272] with the guard in [35.1%, 38.5%] or the share in [0.846, 0.94].  gcc 6's PRED_TREE_EARLY_RETURN rule (an edge that jumps, not falls through in block order, to the return block) caps every two-call loadBl24 at 70.0%, and no predictor combination puts the guard in its window (call + early return in a guard-holding helper = 39.0%: round 1 breaks by 3; `> 0` = 52.5%; `continue` is 50% in gcc 6 and changes the CFG).  The one-call share (85.9%) fixes the order, but the size store then loses its only dependent (sched2's RFS_DEP_COUNT tie-break), and no defaultBl60 spelling gives it one.  New equal bases (IDENTICAL): loadBl24 as g0 (`== 0x60` then `return 0`), r2, r3, r4; the defaultBl60 forms `if (e->data) {..}`, result variable, `== NULL`.  See "## Attempt 51".

## State after attempt 50

Attempt 50 landed nothing; src/build.c and build.sh are unchanged, so the count (7) and attempt 49's review table stand.  It corrected attempt 49's mechanism: **loadXell, loadBl24, loadBaseFile and defaultBl60 are not early-inlined** (each is a call at profile_estimate in both loaders, then inlined by IPA with its own profile scaled to the call block), so the helpers change case 24's and 25's profiles, not the CF/CG arm's (identical before and after); exp_t10's job was bbro's: without the helpers and the expect, connect_traces copies the shared `if (r)` block (the `test edi,edi; jne` line) into the checkBl block, because case 27's extractSmcConfig trace has already taken it.  Then more sharing: the CF/CG load as a helper (85 loose and up), case 23 as a helper (28 and up), the signature check as a helper (95 and up), the nand-dump moves as `useNandData(e, &xb.kv)` (kv and kvAlt in both loaders: **equal base**; smc: 0/2), the could-not-read log as a helper (equal base), case 24's second arm through loadBl24 (25 loose, as attempt 49).  None frees a hint.  New for lab_none: loadBl24 in its one-call `||` form frees the precheck and cold label (loadConsoleBlFiles then differs only in the size store's place), because its own profile gives the defaultBl60 call 85.9% against the two-call forms' 70% at most; but the one call loses the crossjump that orders the size store (attempt 4's borderline) and moves case 27's block in loadBlFiles (24 loose).  See "## Attempt 50".

## State after attempt 49

**7 tricks** (8 before): `--param builtin-expect-probability=99`, 2 `__builtin_expect` (`r != 0` in loadBlFiles' tail, devgl in buildFlash), 1 pin (size), the empty asm barrier on `fail:`, 2 hot and cold labels (`devgl` in loadBlFiles, `none` in loadConsoleBlFiles).  Removed: **exp_t10** (the `type == 10` expect on the CG fallback).  The two loaders now share two helpers: `loadXell(e)` (case 25's retail/kit test and the three-place xell search, identical in both loaders) and `loadBl24(e)` (case 24's file or defaultBl60, called by loadBlFiles' first arm and by console's case 24 as `if (xb.glitch2mfg) r = loadBl24(e);`).  Both are early-inlined.  IDENTICAL at p95 to p99 (a wider window than before, when 96 to 98 were 60 loose); 0/7 at p90 and with no param (exp_pr's alignment); full build SHA256 matches.  See "## Attempt 49".  Borderline changes: the "two calls where `||` would do" note moved from case 24 to loadBl24; case 24's second arm keeps loadBl24's body written out with its leading `r = 0` (calling loadBl24 there is 25 loose); console's case 24 no longer has its own copy of the body.

| Where | Shape | Why it's borderline |
|---|---|---|
| loadBl24 (both loaders' case 24) | `if (loadBaseFile(..)) return defaultBl60(e); if (e->size != 0x60) return defaultBl60(e); return 0;` | two calls where `||` would do (attempt 4's entry, now in the helper) |
| loadBlFiles case 24, second arm | loadBl24's body written out, with a leading `r = 0;` | the helper isn't called there (25 loose if it is); live, shape chosen for the match |
| loadBlFiles case 27 | the fallbacks as a sequence of `r` tests | unchanged from attempt 34's entry |

## State after attempt 48

Attempt 48 landed nothing; src/build.c and build.sh are unchanged, so the count (8) and attempt 46's review table stand.  It scored every combination of exp_pr (expect, `r != 0`, `(int)r < 0`), the barrier, the devgl label and exp_t10, plus lab_none and exp_devgl, at p90 to p99 and no param (a48_combo.py): **no interaction** (loadBlFiles' items add; lab_none and exp_devgl live in other functions; the matching params stay 95 and 99).  Then it read the two near misses' arithmetic exactly.  exp_pr: the no-key copy is aligned only if 14 > 10 x the SE copy's jmp block (2; needs 1), and that 2 comes from the SE block's profile_estimate frequency 7 = 7162 / 12 switch edges x 50% x 0.28^3 = 6.54: it needs 6 (the case arm about 0.8% lower) with the no-key log kept at 11 or more; every factor is a fixed heuristic, the equal-base edits leave it at exactly 7, and a loop-exit r test (first-match 2 to 3%) moves the whole loop (234 loose and up).  lab_none: in bb-reorder's last round the not-entered return (20) goes before the r = 1 block (14); r = 1 would pass at 21, which console's glitch2mfg guard at 50% instead of PRED_CALL's 71% gives, but no natural guard form escapes PRED_CALL (a48_none.py).  See "## Attempt 48".

## State after attempt 47

Attempt 47 landed nothing; src/build.c and build.sh are unchanged, so the count (8) and attempt 46's review table stand.  It took the two cheapest tricks on the loop form.  exp_pr: the tail's test spelled `(int)r < 0` (r is 0 or -1 there) gets opcode-positive 27% in place of the expect's 1% and is **0 loose / 7 strict** (the SE copy's `jbe` comes out right; only the no-key log copy loses its `.p2align`, lab_t5le's old effect), drafts/build_loadBlFiles_negtail_nearmiss.patch; nothing natural closes the alignment (it needs P(<=5) >= 62.5% on the SE copy, i.e. q <= ~9% on the r test or a predictor on the `xb.type` test).  The barrier: every `fail:` placement and -1 spelling in the loop form is attempt 10's 1/7 (mergephi, crossjump rule).  devgl: a none-test predicate helper is 284 loose and up.  See "## Attempt 47".

## State after attempt 46

**8 tricks** (11 before): `--param builtin-expect-probability=99` (was 98), 3 `__builtin_expect` (type == 10, `r != 0` in the tail, devgl in buildFlash), 1 pin (size), the empty asm barrier on `fail:`, 2 hot and cold labels (the new `devgl` hot label on loadBlFiles' case 24 second arm, and loadConsoleBlFiles' `none`).  loadBl is gone: loadBlFiles is attempt 45's n1 (the switch in the loop as loadConsoleBlFiles has it, `r` a loop-body local, one `fail:` site closing case 2, console's CF/CG fallback, case 23 as `e->size & 3`) plus one hot label at the head of case 24's `DEVGL || DEVGL16` arm, found by a sweep of one hint at every `if` (a46_hint1.py, 146 variants, the only IDENTICAL one).  Removed: `else if (type)`, both `__builtin_constant_p` (with the dead default entry and `chk:`), lab_t5le; added: lab_devgl, so a net of 3.  IDENTICAL BYTES at p95 and p99 (not 96 to 98, 92 and below 42 loose and up); full build SHA256 matches.  See "## Attempt 46".  Borderline changes: loadBl case 23's `(e->size & ~3) != e->size` is gone (console's `e->size & 3` now), the `else if (type)` row below (attempt 26's table) is gone with the dead test; case 24's two calls, arm 2's `r = 0` and case 27's re-tested `r` stay, in loadBlFiles with `r` for `*pr`.  No new borderline shape.

| Where | Shape | Why it's borderline |
|---|---|---|
| loadBlFiles case 24 (both arms), loadConsoleBlFiles case 24 | `if (loadBaseFile(..)) r = defaultBl60(e); else if (e->size != 0x60) r = defaultBl60(e);` | unchanged from attempt 4's entry, now in loadBlFiles' switch |
| loadBlFiles case 24, second arm | leading `r = 0;` | unchanged ("For review" comment), `*pr` -> `r` |
| loadBlFiles case 27 | the fallbacks as a sequence of `r` tests | unchanged from attempt 34's entry, `*pr` -> `r` |

## State after attempt 45

Attempt 45 landed nothing; src/build.c and build.sh are unchanged, so the count (11) and the review tables stand.  It rebuilt loadBlFiles in loadConsoleBlFiles' style (the switch in the loop, `r` a loop-body local, one `r = -1` site closing case 2, r tested once after the switch) from src's *current* arms (a45lib.py), and found the closest structure so far: with console's update fallback (a good fallback clears r, then `if (r) break;`), case 23's test as `e->size & 3` and the param at 99, **`else if (type)`, both `__builtin_constant_p` and lab_t5le all go and loadBlFiles is 14 loose / 34 strict, every other function matching** (drafts/build_loadBlFiles_loop_nearmiss.patch).  The one block left is case 24's r = 1 block after the first arm: it needs priority in bbro's round 4, which in src comes from the arm-1 malloc block ending its trace (edge 171 < exec_th 176); in the loop the case arms are 597 instead of 513 (the none test gets no PRED_CALL without a call in the guarded block, attempt 9's reading), so the edge is 199 and the trace runs on.  No natural case 24, fallback, defaultBl60 or guard form moved it (gen_bd560 to gen_bd562, a45_*.py).  Putting the same arms back in a helper (any result form) is 100 loose and up.  See "## Attempt 45".

## State after attempt 44

Attempt 44 landed nothing; src/build.c and build.sh are unchanged, so the count (11) and the review tables stand.  It audited the static predictors: a table of which gcc 6 predictors fire on every critical test in loadBl, loadBlFiles, loadConsoleBlFiles, defaultBl60, buildFlash and calcBlAreaSize (new tool `bdpred.py` on profile_estimate dumps), the predictor each window would need, and the natural constructs that trigger it.  A probe (drafts/build_pred_probe.c) settled which predictors gcc 6.2 has: no PRED_GOTO, no PRED_INDIR_CALL (indirect calls get the plain call 29%), no loop guard, no cold attributes in the toolchain's headers; noreturn only from exit/abort, which only fit dead paths here.  Every gap needs a predictor that points the other way in gcc 6, a call or return the reference doesn't have, or a cross-object value range (`!= 1` for suGetCG, `<= 0` for glitch2mfg), so nothing natural was left to build.  defaultBl60's result-variable form was re-read for lab_none: its NULL edge still goes straight to the return block (10.1%).  See "## Attempt 44".

## State after attempt 43

Attempt 43 landed nothing; src/build.c and build.sh are unchanged, so the count (11) and the review tables stand.  It read attempt 42's wt / no-param near miss (4 loose) and closed it.  Block 116 is the same 72 + 27 = 99 without the param (loadBl's profile has no expect left, so attempts 27 to 29's arithmetic holds to the digit).  The `ja` is the SE copy of the tail's `xb.type <= 5` test: neither successor follows it, so fixup_reorder_chain points the jcc at the edge with P >= 50%, and vrp1's joiner copy gets P(<=5) = Xc p (1 - q) / (Xc - S) = 211 x 0.5 x 0.39 / 178 = 23.2% (attempt 18's formula, read off nm.vrp1 to the digit); `jbe` needs p (1 - q) >= 0.422, and the natural T spellings give q >= 36.6% with p fixed at 50%.  The tail's forms on the near miss (gen_bd550, 10 cases) are all 4 loose or worse.  See "## Attempt 43".

## State after attempt 42

Attempt 42 landed nothing; src/build.c and build.sh are unchanged, so the count (11) and the review tables stand.  It swept hint interactions: every pair of the 9 removable items on src, and every single / pair / triple of the 6 loadBl-side items on the and9, c2, c6, no-`i` and weight bases (gen_bd540, 276 cases), plus the param at 50 to 99 and with no `--param` on the cheap subsets (bdpsweep2.py).  The loadBl items are **not** additive (attempt 18's "all triples additive" no longer holds): with the constant_p entry off, exp_t10 costs only +2 (28 against 46 alone), and once exp_t10 and the entry are both off, exp_pr and t5le add only 2 more.  With exp_t10 and exp_pr both gone the param can go too (buildFlash's exp_devgl matches at gcc's default 90).  **New best composite near miss** (drafts/build_loadBl_wt_noparam_nearmiss.patch): attempt 27's weight form of the entry, exp_t10, exp_pr and t5le off and **no `--param`**: 4 loose in loadBlFiles (the bbro dup of `if (r)`, block 116 at 99 against 88, and the SE copy's `ja`), i.e. 4 tricks for those two effects.  Without the weight the cluster {param, exp_t10, exp_pr, cp, t5le} (6 tricks) is 30 loose (the type-11 block's place on top); with c2 and case 6 through `goto chk` also vol_fail, 7 tricks, 20 loose.  Nothing natural fixed the dup; the SE test's spellings with a 0-compare fold back (closed).  lab_none by case 24's forms with the precheck and label off: no change (gen_bd543).  Full matrix in "## Attempt 42".

## State after attempt 41

Attempt 41 landed nothing; src/build.c and build.sh are unchanged, so the count (11) and the review tables stand.  It took the two tricks outside loadBl.  exp_devgl from the RTL side: once tree-sink has moved the setne into the non-dev arm, ce1/ce2/ce3 all find the IF-THEN block but can't convert it, because the arm's compare sets the flags the condition uses (gcc 6 refuses any then-block insn that sets the cc register); so the cmovbe needs GIMPLE that sink leaves alone, which is attempts 15, 16 and 25's closed problem.  lab_none: the none test as a `continue`, or the `if (r)` exit inside the none test's block, costs 169 loose and up (the skip path must pass the r test, gen_bd530, gen_bd531), and defaultBl60 written out in case 24 lowers the r = 1 block to 12 (9% in the caller's profile against the helper's 10.1%, gen_bd532).  See "## Attempt 41".

## State after attempt 40

Attempt 40 landed nothing; src/build.c and build.sh are unchanged, so the count (11) and the review tables stand.  It took attempt 39's inlining lead and corrected its mechanism: loadBl is **not** inlined for its speedup (the u8 form has big_speedup too, measured with the auto limit raised as a diagnostic) but refused by ipa-inline's early **min_size** check (`min_size - call size > max(insns-single 400, insns-auto 40)`, reported as "max-inline-insns-auto limit reached"): min_size is the size outside every predicate, about 30 in src, 500 when the switch has no case predicates.  A rescan of every generator from gen_bd320 to gen_bd503 that still runs on src (about 80) found **no loadBl refusal row at all**; the only refused families were attempt 39's and attempt 9's gen_bd202 `in` rows (the none test inside a helper returning r).  Rescued so that loadBl stays inlined (the type loaded before strnicmp, or `switch (e->type)` with a narrow local), every one is worse than src: the none test inside loadBl 207 loose with every hint (and the hints stop mattering), narrow locals 138 and up, gen_bd202's `in` 347 and up hint-free (gen_bd520, gen_bd522).  New equal base: loadBl without its `i` parameter (`edata` plus the constant_p entry's first term on `e->crc`, `e->size` or `e->offset` in place of `i`) is IDENTICAL (gen_bd521); it frees nothing.  See "## Attempt 40".

## State after attempt 39

Attempt 39 landed nothing; src/build.c and build.sh are unchanged, so the count (11) and the review tables stand.  It stepped back from per-hint spellings to how the data reaches loadBl, each form crossed with every loadBl-side trick off alone.  The tail reading `e->data` instead of `xb.files[i].data`, and loadBlFiles' `r` (or `e` and `r`) declared in the loop body (so `&r` gets a scope CLOBBER each iteration), are **equal bases**: IDENTICAL with every hint, and every hint costs what it costs on src (gen_bd510).  A pointer IV is 355 loose.  case 2's slot through a local pointer is 18 loose.  checkBl's type argument as `e->type` (gen_bd512 `fld_ck`) is 9 loose with every hint, and worse than src with the constant_p entry or exp_t10 off.  New reading: **loadBl is inlined only while the IPA inliner can split its size by case predicates** on the parameter load `e->type` (`op0[ref offset: 8224] == N`; unconditional size 29).  loadBl taking `i` and computing `e` itself, any narrow `type` local (uint8_t, uint16_t, signed char, short), or the "none" test moved into loadBl as an early return all make the size unconditional (234.5), and then loadBl stays out of line with "max-inline-insns-auto limit reached" (gen_bd510, gen_bd511).  See "## Attempt 39".

## State after attempt 38

Attempt 38 landed nothing; src/build.c and build.sh are unchanged, so the count (11) and the review tables stand.  pin_size (gen_bd500): a live type test at retail's start (the xell lookup hoisted, `x = 0; if (xb.type != BUILD_RETAIL) x = findFile(25);`) does open attempt 37's route (kit sum `size_254 + prephitmp_269`) but moves the findFile(25) loop ahead of the sums (313 loose); one-expression sums and the kit/retail tail written once (5-test nested in an else) don't flip or cost more.  So the route needs a statement that is live, isn't a count load, and leaves no code; none was found, and the reasons each kind fails are now listed.  Rotation: `break` after the signature block's no-key and passed logs (same behaviour; gen_bd501) is worse for t5le / exp_pr / `else if (type)` (47 loose and up); case 6's checkBl through `goto chk` (gen_bd502) makes exp_t10 irrelevant once the constant_p entry is off (20/90 either way) but leaves bbro's `if (r)` copy in case 6's checkBl block and the CG/SE checkBl setups crossjumped into it (20 loose with every hint), and the reference keeps case 6 apart from chk anyway; exp_devgl by a re-tested fuse (`if (!fuse && dev) fuse = 1;`, gen_bd503) keeps a branch where the reference has cmovbe (10 loose / 598 strict).  See "## Attempt 38".

## State after attempt 37

Attempt 37 landed nothing; src/build.c and build.sh are unchanged, so the count (11) and the review tables stand.  It swept attempt 36's open route for pin_size and confirmed the mechanism: a statement at the start of retail's arm (so its first block isn't the findFileOffset(5) loop header when ch2 runs) gets the kit laid out first *and* flips the kit sum, with src's JKR order.  An unused `n = xb.nFlashFiles;` leaves 10 lines, an unused `n = xb.nFiles;` leaves **2** (drafts/build_calcBlAreaSize_nfiles_load_diag.patch, diagnostic only: a dead load is a trick).  What's left is always the operand order of the loop compares that use the new load as their bound: a source-level load's SSA version is below every inlined loop's `i`, so fold writes `n != i` (`cmp n,i`), where the reference's bound is ch2's guard copy (a high version, `cmp i,n`).  Every natural statement that could sit there is either such a load or folds away before ch2 (constants, a `type != RETAIL` flag, an `xb.type` copy); the helpers reading their count into a local first flip their own standalone compare.  Sweeps gen_bd490, gen_bd491.  See "## Attempt 37".

## State after attempt 36

Attempt 36 landed nothing; src/build.c and build.sh are unchanged, so the count (11) and the review tables stand.  It worked attempt 35's switch near miss and closed it: gcc 6's switch expansion can't give the reference's `cmp 2; je J; cmp 5; jbe R` from any case set that also lets PRE reach retail first (retail must be the default for that, and a default has no case node, so the kit is tested by its own low bound: `jb; cmp 6; jb` with a range up to 0xffffffff, `lea; cmp 3; ja` with 6..9; a switch's 1/3 edges also give JTAG the wrong frequency).  New mechanism, read from the dumps: in the if-forms PRE's walk and bbro's tie both follow the 5-test's **first edge**, through the loop tree: loops are rebuilt in RPO (edge order), ch2 creates the arms' preheaders in that order and puts each right after the test, so the first edge's arm ends up with the higher block index and PRE (dominator sons, highest index first) walks it first; connect_traces also takes the first edge when probability and trace length tie (both arms' head traces are 4 blocks).  A diagnostic (JRK with the kit at 51-52%) gives the reference's layout with only cold-block order and one register swap in retail's xell loop left.  Sweeps gen_bd480 to gen_bd484.  See "## Attempt 36".

## State after attempt 35

Attempt 35 landed nothing; src/build.c and build.sh are unchanged, so the count (11) and the review tables stand.  It read pin_size in IRA as attempt 34 asked and found the mechanism is a copy-order tie, not a frequency: the kit add `r105 = r197 (prephitmp) + r104 (size)` makes two shuffle copies of the same freq (cp30 r197-r105, cp31 r104-r105), copy_freq_compare_func breaks the tie by copy number (operand order), so r105 threads with the prephitmp; r197 conflicts with r104, so cp31 can't merge afterwards, and r105 pops after r99's thread and takes esi.  The reference has r104 = r105 = ebx, the thread {r104, r105}: attempt 7's operand order is the whole question.  New: **the build-type chain's order flips that operand order** (gen_bd470, `bdorder.py`): `if (JTAG) .. else if (xb.type <= BUILD_DEVGL16) retail else kit` (JRK) and a switch with retail as the default (`sw_*_dR`) give `size_N + prephitmp_M` and exactly the reference's kit-arm registers (`mov ebx,esi` before the 14 loop, `add ebx,eax`), but JRK lays the retail arm out first (288 loose) and the switch's kit range test is `lea; cmp 3; ja` (92 loose).  In the if-forms the 5-test's true arm is both the arm PRE's insert walk reaches first (it takes the free SSA names) and bbro's round-2 tie winner, so the kit can't be laid out first and still get fresh names.  Drafts drafts/build_calcBlAreaSize_JRK_nearmiss.patch and drafts/build_calcBlAreaSize_sw_JKR_dR_nearmiss.patch.  Also: lab_none by a re-tested r in loadConsoleBlFiles' case 24 (gen_bd471): no movement.  See "## Attempt 35".

## State after attempt 34

**11 tricks** (12 before): `--param builtin-expect-probability=98`, 3 `__builtin_expect` (type == 10, `*pr != 0`, devgl), 1 pin (size), the empty asm barrier, 2 hot and cold labels (t5le, none), 2 `__builtin_constant_p`, 1 dead test (`else if (type)`).  pin_d is gone: case 27's fallbacks are written as a sequence of `*pr` tests inside the first load's failure arm (`if (load(name)) { *pr = load("config.bin"); if (*pr) *pr = load("config_raw.bin"); if (*pr) { smc take-over } }`, gen_bd463 `c_seq`).  Mechanism (IRA dump, attempt 33's reading taken one step on): the join's thread {base, n*0x42c, n} pops in ALLOCNO_FREQ order, and the re-tested `*pr` sends half of the first failure's flow past the smcConfig test at profile_estimate (vrp1 threads it away later), so n's reloads on the fallback paths outweigh the base (n pops first and takes edx, the base follows it along the copies, d gets eax).  The same re-test over the whole case (`two_pr`) also flips the registers but lowers the extract block's edge to 320, under the loadBinFile block's 322 in bbro's round 2.  IDENTICAL BYTES, full build SHA256 matches.  Every other hint costs what it cost before.  See "## Attempt 34".  New borderline shape, marked in src:

| Where | Shape | Why it's borderline |
|---|---|---|
| loadBl case 27 | `if (loadBaseFile(name)) { *pr = loadBaseFile("config.bin"); if (*pr) *pr = loadBaseFile("config_raw.bin"); if (*pr) { smc take-over } }` | Same behaviour as the old `&&` chain of the three loads, and nothing in it is dead, but it is chosen for what gcc does with it: the re-tested `*pr` adds flow to the fallback paths at profile_estimate, which sets IRA's pop order at the join |

## State after attempt 33

Attempt 33 landed nothing; src/build.c and build.sh are unchanged, so the count (12) and the review tables stand.  It swept six angles no earlier attempt had closed, each crossed with the loadBl hints off one at a time: real types in loadBl and both loops (gen_bd450: neutral or worse; `int type`'s retyping costs 38 loose), `else if (type)` by a repeated test of a *local* key copy (gen_bd451: a local's dead re-test folds before profile_estimate, so it scores as the plain else, 54; the `key && !verify` / `else if (key)` join is 50 plus .rdata), defaultBl60 returning a computed value instead of constants (gen_bd452: 142 and up), the author's nested ifs for the SE test, case 25, case 27's chain and the skip test (gen_bd453: equal bases, every hint costs what it costs on src), case 27's smcConfig moves in every order (gen_bd454: cases 2/3/4's data-size-NULL-0 order is an equal base; pin_d still 14), and the CF/CG fallback as an inner switch or `type != 9 && type != 10` guard (gen_bd455: 110 and up).  New reading of pin_d from IRA (`-fdump-rtl-ira`): the join's base is a thread {r535 base, r534 n*0x42c, r125 n} that is popped before n's own constraints apply; n is kept off eax by loadBaseFile's live result, so base takes eax first and d gets edx.  See "## Attempt 33".

## State after attempt 32

Attempt 32 landed nothing; src/build.c and build.sh are unchanged, so the count (12) and the review tables stand.  It tried four angles the notes hadn't closed, each a quick sweep with every other hint kept: lab_none by the loop's exit count (the console's -1 errors jumping straight to a could-not-read label after the loop, so PRED_LOOP_EXIT's 9% is split over more exits and the not-entered return cools: 69 loose and up, the log and the body move; gen_bd440), `else if (type)` by flag and result-variable joins on src (attempt 30 had scored them only with all seven loadBl hints off: best 25 loose in loadBlFiles plus displacement, `else` 54; gen_bd441), exp_devgl with the dev override tested *before* the glitch2mfg def (no def above the dev test for sink to move: 11 loose at best against src-minus-expect's 7; gen_bd442), and lab_none by defaultBl60's body (nested, result variable: the same 4/8 on the plain-`for` base; gen_bd443).  Also: the param swept 60 to 99 with lab_t5le, exp_pr or pin_d off: none matches at any value.  See "## Attempt 32".

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
- gen_bd164: loadBlFiles written like loadConsoleBlFiles, switch in the loop and r a local. 164 loose at best, mostly layout; registers and code line up. This is still the shape I'd bet the author wrote, since the console function matches that way and tools/ref/xeBuild64 (v1.16) keeps r in a register tested after the switch.
- gen_bd165: console's fallback (`if (suGetCF(..)) *pr = 0;`, then `if (!*pr)`) with *pr: 115 loose at best, about the same with `seq`, `and` and `nest2`.
- gen_bd166: more fallbacks. c7 and c9 (no `goto chk`) are 33 loose, 192 strict, without constant_p. It's the most natural form short of the loop, and worth one more look.
- gen_bd167: 12 tail forms x `*pr` expect or not x hints: nothing beats the source's own tail; 0 loose, 7 strict at best, as above.
- gen_bd168: case 23 nesting, order and `% 4` (lab_badsize): 6 loose whatever the form, with and without the outer nest.
- t0 (no expect on type 10): adds `test edi,edi; je` after the CF and CG checkBl (4 loose), and block 24 goes to the end (key 0).

### Evidence from the Linux build (tools/ref/xeBuild64, older version, gcc 4.9)

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

Read from the reference's loadBlFiles (objdump, IDA's build/decomp_22.txt) and tools/ref/xeBuild64's (build/x64.dis, the function at 405280; strings found by address):
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

Reading: tools/ref/xeBuild64's scan (404839..4048a2, build/x64.dis) tests the bound, then `found != 1`, calls smcConfigOk, and on a hit (`cmp eax,1; je`) jumps back to the bound test **without advancing i**; on a miss it advances i and loops.  That is a loop whose condition holds both tests and whose body only moves i on a miss, i.e.

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

No match; src is unchanged.  Goal: attempt 12's lever (loop structure read off tools/ref/xeBuild64, build/x64.dis) on every function that still has a hint.  Generators gen_bd240 (isUpdateBl forms) and gen_bd241 (loadFileCrc with a padded-size local) run on src/build.c as of f735084.  Linux strings were found by file offset + 0x400000 (static ELF) and grepped as `mov esi,0x...` in x64.dis.

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

## Attempt 32

Goal: an angle the notes hadn't closed, on any trick.  Picked by what earlier attempts measured only with other hints off, or not at all: lab_none's exit count, `else if (type)`'s flag joins with every other hint on, exp_devgl with the override first, defaultBl60's body, and the param value with single hints off.  Generators gen_bd440 to gen_bd443 on src as of ccf9746b; `tools/wip/dehint/bdpsweep.py` (param sweep).  Scratch in build/bd/a32 (not kept).  Loose/strict lines in the focus function unless said.

### lab_none by the loop's exit count (gen_bd440, 254 cases)

- The not-entered return's frequency (20, against the r = 1 block's 14) is PRED_LOOP_EXIT's 9% split over the loop's exits (two: `i < nFiles` and `if (r) return -1`), halved by shrink-wrap's duplicate.  Attempt 25 tried dead exits as a diagnostic (121 loose).  Here the exits are real: the console's -1 errors (kv, kvAlt, patch size, smc config, smc load, smcSetLoad) as `r = -1; goto bad;` with `bad:` the could-not-read log after the loop (vrp1 threads `r = -1; break; if (r)` to the log anyway), every subset, with and without the precheck and label, with the in-loop test as `if (r) {log; return -1;}` or `if (r) goto bad;`.
- Best 69/200 (one goto, `if (r) goto bad;`); every form moves .rdata (the log is now expanded after the loop) and the loop body, as attempt 25's diagnostic did.  With any goto the precheck and label make no difference.  Closed.

### `else if (type)` with every other hint kept (gen_bd441, 15 forms)

- Attempt 30's gen_bd415 scored the flag and `*pr`-as-result forms with all seven loadBl hints off; here only the signature block changes, on src.
- `else` 54 loose (as before), `ok` local with `else` the same 54, `ok` tested twice (`if (!ok) failed; if (ok) passed;`) 59, `*pr` tested again (`if (!*pr) passed`) 100, `*pr = verify ? 0 : -1; if (*pr) ..` 103, `if (!verify) *pr = -1; if (*pr) ..` 89, no key first 64, `else if (*pr == 0)` (also dead) 40, passed first 66 (no displacement, .rdata order), `int ok = 1; .. if (ok && xb.pub1bl) passed` 25 (+displ): that one re-tests pub1bl in the code (`mov eax,ds:0x29c; test; je` before the passed log) and moves the no-key log, so it isn't closer in kind.
- So the flag join, the lever in options and mode_client, doesn't act here: vrp1/dom thread the second test, but the passed log's frequency comes out as the plain else's (both are 50/50 from PRED_CALL on the two logs).  Closed.

### exp_devgl with the override first (gen_bd442, 28 cases)

- Attempts 15 and 16 swept the src order (def, then the dev override) and its spellings.  Here the glitch2mfg test is the dev test's else arm or guarded by it (`if (JTAG) 1; else if (dev) 1; else g != 0;`, nested, `fuse = 1; if (!JTAG && !dev) fuse = g != 0;`, `if (!g && !dev) fuse = 0;` ...), memset before or after.  There is then no def above the dev test for sink to move, so the reference's setne-then-cmovbe would have to come from RTL if-conversion speculating the setne.
- Best 11/46 (`if (JTAG) .. else if (dev) .. else ..` and its nested spellings: the same code as src without the expect plus a moved fuse = 1 block); `&&`-joined conditions 56/686.  If-conversion doesn't speculate it.  Closed.

### lab_none by defaultBl60's body (gen_bd443, 14 cases)

- On src (label kept) nested success-first, a result variable (`int r = 1; .. r = 0; return r;`), `r = 0 .. else` and `== NULL` are IDENTICAL; on the plain-`for` base (no precheck, no label) all are the same 4/8 as src's body (the r = 1 block keeps 14).  uint32_t returns 111 and up (loadBl changes).  Nothing moves the r = 1 block's frequency: it is the malloc test's 10.1% of the case 24 sites, and the body's spelling doesn't change that predictor.

### The param with single hints off (bdpsweep.py)

- lab_t5le, exp_pr, pin_d each off, `builtin-expect-probability` 60 to 99: lab_t5le is 7 strict / 0 loose at 96, 98, 99 and worse elsewhere; exp_pr and pin_d never under 12 strict.  No value makes a hint free.

### Don't retry (attempt 32)

- lab_none by extra loop exits from real error sites (gen_bd440) or by defaultBl60's spelling (gen_bd443).
- `else if (type)` by flag / result-variable joins, `*pr` re-tests or passed-first forms, with the other hints on (gen_bd441) or off (gen_bd415).
- exp_devgl by putting the override before the glitch2mfg def, in any nesting (gen_bd442).
- pin_d by a loop over the case 27 file names (hand run, 228 loose).
- The param value as a lever for lab_t5le, exp_pr or pin_d alone.

### What to try next

- Nothing new opened.  The windows are attempt 25's; vol_fail's best base is attempt 30's c6 near miss, exp_t10's attempt 27's weight near miss (block 116 at 99 against 88).
- pin_d with the case 27 fallbacks as a loop over the three names (`static const char *const names[] = { NULL, "config.bin", "config_raw.bin" }`, `*pr = loadBaseFile(k ? names[k] : e->name, ..); if (!*pr) break;`, pin off; one hand run, not kept): 228 loose in loadBlFiles and the whole object displaced.  The loop isn't given back as straight-line calls.  Closed.
- Otherwise build stays at 12.

### Costs now (strict/loose, removed alone; 12 tricks, unchanged)

On src: lab_t5le 7/0, exp_pr 18/2, pin_d 23/14, exp_devgl 43/7, pin_size 82/40, exp_t10 116/46, vol_fail 296/126, lab_none 333/231 (4/8 with the precheck gone too); etype 128/54, the constant_p entry 78/26 (re-measured for pin_d, pin_size, lab_none, exp_devgl, lab_t5le; the rest attempt 30's).

## Attempt 33

Goal: an angle the notes hadn't closed, preferring the brief's list (real types, a local through which a test can fold, nested ifs, a helper's return form, statement order in a block no sweep had touched).  Generators gen_bd450 to gen_bd455 on src as of 5a0bc459 (`python tools/wip/dehint/bdrun.py tools/wip/dehint/bdgen/gen_bd45N.py`); each crosses its edits with the loadBl hints off one at a time (bdhints names plus `etype` = plain else and `cp` = the constant_p entry as `if (0)`).  Scratch in build/bd/a33 (not kept: `nopind.c` / `nopins.c` are src minus pin_d / pin_size, `lbf_ira.txt` loadBlFiles' IRA dump).  Loose/strict lines in loadBlFiles unless said.

### Real types (gen_bd450, 99 cases)

- loadBl's `type` local as uint32_t or unsigned: 38/104 plus .rdata and displacement with every hint kept (worse on every single off); loadBl's `i` as int, the console loop's r as int or its `type` as uint32_t: IDENTICAL (equal bases), every hint's cost unchanged; loadBlFiles' or the console loop's `i` as int (no cast): 4/4 (the loop test's signedness); `int *pr` with `int r`: 71/352.
- No type frees a hint.  Closed for these locals (calcBlAreaSize's, isUpdateBl's and fuse's were closed before: gen_bd283, gen_bd282, gen_bd192).

### `else if (type)` by a re-test of a local key (gen_bd451, 75 cases)

- Attempt 32's `ok && xb.pub1bl` re-tested the global after cbVerifySig, which may change it, so the reload stayed in the code.  Here `struct rsapub *key = xb.pub1bl;` (or const), and the forms `if (key && !verify) {failed} else if (key) passed; else nokey;`, `.. else if (!key) nokey; else passed;`, src's nesting with `else if (key)`, src's nesting with a plain else, and `ok = !key || verify; if (!ok) .. else if (key) ..`.
- `else if (key)` inside `if (key)` (dead, for the record): 54, the plain else's score: a local's dominated re-test is folded before profile_estimate, so it can't do what `type` does (type's test survives because only vrp1 knows its range).  `else if (xb.pub1bl)` (global, dead only by assumption): 7/82, the reload stays.
- The `&&` joins with a local key: 50/67 plus .rdata (the passed/no-key logs swap places); `!key` second: 66.  The ok forms are worse.  Closed.

### defaultBl60 returning a computed value (gen_bd452, 15 cases)

- gen_bd281 / gen_bd443 only tried forms that return constants (PRED_CONST_RETURN against the malloc-failed path, directly or through the return PHI).  `return e->data == NULL;`, `return !e->data;`, `e->data ? 0 : 1`, a local `p`: 142/398 in loadBlFiles and 114 in the console function with the label, 222 on the plain-`for` base (the value is computed with setcc, the r = 1 block is gone).  Closed.

### Nested ifs (gen_bd453, 42 cases)

- The SE test as `if (type == 9) { if (S && E) .. }` or three nested ifs, case 25's `RETAIL || > DEVGL16` as two ifs, case 27's `&&` chain as nested ifs: all IDENTICAL with the hints (equal bases), and each hint costs exactly what it costs on src (t5le 0/7, exp_pr 2/18, pin_d 14/23, exp_t10 46/116, etype 54, vol_fail 86/126).
- loadBlFiles' skip test as `if (!strnicmp(..) && !e->crc) continue;` (or nested): 120/237 (.rdata).  Closed.

### Case 27's smcConfig moves (gen_bd454, 48 cases)

- No sweep had touched the fallback block itself (src: data, NULL, size, 0, unlike cases 2/3/4's data, size, NULL, 0).  Every valid order of the four moves, `*pr = 0` first or last, `if (!xb.smcConfig.data) break;` or nested: with `break`, src's order, data-size-NULL-0 and data-size-0-NULL are IDENTICAL (so cases 2/3/4's order is an equal base) and `*pr = 0` first is the same code; the size move first is 117 loose, the nested forms 127 and up (.rdata).  pin_d off is 14/23 on every equal base.  Closed.

### The CF/CG fallback as an inner switch (gen_bd455, 40 cases)

- `if (*pr) { switch (type) { case 9: if (suGetCF) goto se; break; case 10: if (suGetCG) goto chk; break; } break; }` (case 10 first, `default: break;`, `return` arms), and `if (type != 9 && type != 10) break;` before an if/else: 110/232 at best (the guard form with attempt 27's weight), switches 118 and up; .rdata moves in all.  Attempt 1's gen_bd18 result stands on the current src.  Closed.

### pin_d read from IRA (`-fdump-rtl-ira` of build/bd/a33/nopind.c, pin off)

- The join after the case 27 loads (bb 142) recomputes the base from the reloaded nFlashFiles: r125 (n, pretmp_80) -> r534 = n * 0x42c -> r535 = r534 + xb -> d (r263) = [r535 + 0x422bc], size (r493) = [r535 + 0x422c0].  Copies cp3 (r534-r125) and cp4 (r535-r534) put the three in one thread, which is popped first: r535 gets reg 0 (eax), r125 reg 1 (edx: it is loaded while loadBaseFile's result is live in eax), r534 eax, then d edx and size eax.  The reference has n, base and size in edx and d in eax, i.e. n's register propagated along the thread.
- So the pin stands for "n's constraint decides the thread's register"; d itself has no preference (all costs 0).  No source form tried in any attempt changes the thread's membership (the smc fallback's own base r477 is a separate allocno: the GIMPLE recomputes the base at the join on every form).

### Don't retry (attempt 33)

- Retyping loadBl's type, i, *pr or the loops' i, r (gen_bd450).
- `else if (type)` by a local key's re-test or `key && !verify` joins (gen_bd451).
- defaultBl60 returning a computed value (gen_bd452).
- Nested ifs for the SE test, case 25, case 27's chain, the skip test (gen_bd453): equal bases, nothing freed.
- The smcConfig fallback's statement order or nesting for pin_d (gen_bd454).
- The CF/CG fallback as an inner switch or a `!= 9 && != 10` guard (gen_bd455).

### What to try next

- pin_d: a form where the join's base is *not* recomputed from a reloaded n (so the thread doesn't start at n), e.g. a base the fallback path and the first-load path share as one SSA name; none of the case 27 forms so far does that (every one reloads nFlashFiles after the calls, as the reference does), so this is speculative.
- Otherwise build stays at 12; attempt 25's windows, attempt 27's exp_t10 weight near miss and attempt 30's c6 vol_fail near miss are the closest bases.

### Costs now (strict/loose, removed alone; 12 tricks, unchanged)

On src (re-measured by gen_bd450's `src|` rows): lab_t5le 7/0, exp_pr 18/2, pin_d 23/14, exp_t10 116/46, vol_fail 296/126, lab_none 333/231, etype 168/94 in the object (128/54 in loadBlFiles), the constant_p entry 118/66 in the object (78/26 in loadBlFiles); exp_devgl 43/7 and pin_size 82/40 as attempt 32.

## Attempt 34

Goal: pin_d, from attempt 33's IRA reading (the join's base is popped before n, so it takes eax and d gets edx); then pin_size in the same light.  Generators gen_bd460 to gen_bd464 on src as of 34b3ab10 (`python tools/wip/dehint/bdrun.py tools/wip/dehint/bdgen/gen_bd46N.py`).  Scratch in build/bd/a34 (not kept: `nopind.c` / `nopins.c` are src minus pin_d / pin_size, `*.ira` loadBlFiles' IRA dumps, `bbro_*.txt`, `dd.py` a unified diff of loadBlFiles against the reference).  Loose/strict lines in loadBlFiles unless said.

### Why the base pops first (`-fdump-rtl-ira` of nopind.c, read with the pushes and pops)

- The thread is {r535 base 135, r534 n*0x42c 100, r125 n 131} (r460/r457 join it later by a freq-1 copy; thread freq 422).  Inside one thread bucket_allocno_compare_func falls through to ALLOCNO_FREQ (gcc 6 ira-color.c, from memory; consistent with the push order r534, r125, r535 and the pops r535, r125, r534), so the most frequent member pops first and takes the first free register, eax.  n can't follow it into eax (its conflicts' copies prefer eax) and gets edx; d conflicts with the base and gets edx.
- The freqs, from loadBlFiles' .optimized (case 27 entry 513, join 509, extract block 355): r534 is a def and a use at the join; the base has those two refs plus the size load in the extract block (35); n has the first block's hoisted load (51), the join's use and the fallback paths' reloads (RTL bbs 107/109/111/112, about 30 together).  So n wins when the fallbacks' refs outweigh the extract block's.  Diagnostic (gen_bd461, not candidates): `__builtin_expect(d != 0, 0)` gives the reference's join registers (the layout moves, 143 loose); `expect(.., 1)` doesn't.
- Probabilities at loadBl's profile_estimate: load1 and load2 failure 29% (call heuristic), load3 50%, smcConfig null 21.6% (pointer + call + early return), the d test 69.8% (pointer 85% with the call's 29%; its two early returns cancel).  The d test can't be cooled naturally (attempt 29's early-return rule: neither edge can lose its 39%), so the lever is the fallbacks' flow.

### Sweeps

- gen_bd460 (15 cases, pin off and on): the load chain as `||` with an empty then-arm, as gotos to a label before the extract, as `*pr = load; if (*pr) ..` for all three (`seq`) or nested (`seqn`); the d test as `if (!d) break;`.  `||` and the gotos are IDENTICAL with the pin and 14 without (the same CFG); seqn 26, seq 70.
- gen_bd462 (5 cases, pin off): **`if (l1 && l2) *pr = l3; if (*pr) {..}` (`two_pr`) and its `else *pr = 0;` spelling give case 27 exactly as the reference has it** (base edx, d eax; IRA: n 196 against the base 122), but 26 loose elsewhere: the type-11 block and a log_printf move.  bbro: the extract block's edge into the `if (r)` test (bb 117's priority) falls 355 -> 320, because the `*pr` test (50%, no predictor) sends half of case 27 past the smcConfig test, whose null exit (21.6%) bypasses the join; the loadBinFile block (bb 87, priority 322) now comes first in round 2.  `return` for the smc break: 14 (same as break).  `*pr = -1` after a void chain: 83.
- Window from the two end points (linear in q, the share of case 27 that reaches the smcConfig test): IRA flips for q above about 0.07, bbro keeps bb 117 first for q under about 0.47; src's q is 0.04, two_pr's 0.5.
- **gen_bd463 (6 cases, pin off): the `*pr` re-test only inside the first load's failure arm (q about 0.145): `c_seq`, `c_nested` (`if (l2) *pr = l3; if (*pr)`) and `c_else0` (with `else *pr = 0;`) are all IDENTICAL.**  Landed `c_seq` (it doesn't rely on *pr coming in as 0).  `c_and` (`if (l1) { if (l2 && (*pr = l3)) {..} }`) and `c2_nested` (`if (l1 && l2) { *pr = l3; if (*pr) .. }`) are src's CFG again: 14.
- pin_size, diagnostic (gen_bd464): an expect either way on the JTAG or kit test moves the whole function (190 loose and up), so the arms' frequencies can't be read off this way.  Its mechanism (attempt 12: PRE's operand order puts the kit sum's shuffle copy on the prephitmp, not on the running size; attempt 20: the sum needs its own allocno in ebx at the 14 loop) isn't shown to be a pop-order tie, so the pin_d lever wasn't carried over.  Not swept further.

### Other notes

- `python tools/re/fncmp.py src/build.c loadBlFiles` doesn't print MATCH for this object even at HEAD (with or without the param); bdrun.py's score and the full build are the checks here.
- bdhints.py has lost its pin_d entry, so generators that call `bdhints.off(.., 'pin_d')` now raise; run them against 34b3ab10's src.

### Don't retry (attempt 34)

- pin_d: done.  For the record: the load chain as `||` or gotos (the same CFG), `seq` / `seqn` (gen_bd460), `two_pr` over the whole case (the bbro tie, gen_bd462).
- pin_size by the arms' frequencies through expects (gen_bd464, diagnostic).

### What to try next

- The lever that worked: a re-test of a result variable that vrp1 threads away later still changes the flow at profile_estimate, and with it IRA's ALLOCNO_FREQ order inside a copy thread, not only bb-reorder's keys.  Where a pin decides which member of a thread pops first, compare the members' freqs (the "Forming thread" lines print them) and look for natural flow that tips them.  pin_size is the next place to read with this in mind: find the kit sum's thread in `-fdump-rtl-ira` of nopins.c and see whether its register comes from a freq order at all.
- Otherwise attempt 33's list stands (attempt 25's windows, attempt 27's exp_t10 weight near miss, attempt 30's c6 vol_fail near miss).

### Costs now (strict/loose, removed alone; 11 tricks)

On src (`bdhints.py` on the landed form): lab_t5le 7/0, exp_pr 18/2, exp_devgl 43/7, pin_size 82/40, exp_t10 116/46, vol_fail 296/126, lab_none 333/231; etype and the constant_p entry not re-measured (attempt 33's: 128/54 and 78/26 in loadBlFiles).

## Attempt 35

Goal: pin_size from IRA, as attempt 34 asked (the kit sum's copy thread), then attempt 34's lever (a re-tested result whose flow vrp1 threads away) on the frequency hints.  Generators gen_bd470, gen_bd471 on src as of a5bae5e6 (`python tools/wip/dehint/bdorder.py tools/wip/dehint/bdgen/gen_bd470.py` prints each case's score and the statement before each setPatchSlot; `bdrun.py` for gen_bd471).  Scratch in build/bd/a35 (not kept: `nopins.c` is src minus pin_size; `*.ira`, `*.pre`, `*.pe`, `*.bbro` its dumps and those of the JRK case).  Loose/strict lines in calcBlAreaSize unless said.

### pin_size read from IRA (`-fdump-rtl-ira` of nopins.c)

- Pseudos: r99 = the sum after 11, r171 after 12, r104 after 13 (insns 280, 666, 680), r197 = the 14 lookup's prephitmp (files[x].size, PHI'd), r105 = r197 + r104 (insn 360, the kit sum), r338 / r207 = files[0].size loaded early (copies into r197).
- The reference's registers: r171 esi, r104 ebx (the `mov ebx,esi` before the 14 loop is LRA's output reload of the 13 add, as attempt 7 said, not an IRA region: `-fira-region=all` leaves calcBlAreaSize at 40, and the dump colours only loop 0, pressure 6 of 7), r105 ebx, r197 eax, r338 ebx (the reference's early `mov ebx,ds:0x422c0`).
- Ours: threads {r104 175, r171 166, r99 175, r135 168} (684) and {r338 16, r207 72, r197 179, r105 264} (531).  r99's thread pops first (r99 esi; r104 and r171 follow into esi); r105 then takes esi too.
- Why r105 isn't with r104: the add makes cp30 r197-r105 and cp31 r104-r105, both freq 11 (one insn).  copy_freq_compare_func sorts by freq, then by copy number, and the numbers follow operand order, so cp30 merges first; r197 conflicts with r104 (both live into the add), so cp31 can't join the threads afterwards.  There is no frequency to tip here: the operand order (attempt 7: `prephitmp_229 + size_254`, the lower SSA version first) decides it.  With the order flipped, r105 joins r104 and the pair takes ebx (checked below).
- The `"+r"` diagnostic (attempt 20, 9 loose) isn't a test of this: the asm output is a new pseudo (r254) that takes eax, and the sum then picks ebx alone.

### Where the prephitmp's name comes from (PRE dump of nopins.c)

- The free list at PRE holds about 20 names (136, 243, 242, 237, 236, 229, 228, 227, 226, 129, 92, 51, 48, 33, 32, 31, 24, 18, 17, 16).  The kit's 14 lookup is the first insertion and takes 136 to 229; the rest of the kit arm takes the others (14, 13, 12, 11 in that order); retail then gets fresh 260 to 283 and JTAG 284 to 301 (which is why JTAG's sum is right).  Far too many free names for any form to shorten the list below the 6 the 14 lookup needs.
- So the kit arm must be reached later in PRE's insert walk.  The visit order isn't plain block-index order (JTAG's head is bb3 and is reached last); read off results instead.

### gen_bd470: the build-type chain's order and nesting, and switches (pin off, 104 cases)

- if-chains: JKR (src) and its nested spelling, nJ_KR_J (`if (type != JTAG) { if (> DEVGL16) K else R } else J`), `>= BUILD_DEVKIT`: 40 loose, kit sum not flipped.  **JRK (`else if (xb.type <= BUILD_DEVGL16)` retail, kit last), JRK nested, `< BUILD_DEVKIT`: kit sum flipped (`size_257 + prephitmp_264`), and the kit arm's code is the reference's** (`mov ebx,esi`, `add ebx,eax`, files[0].size in ebx), but 288 loose: retail is laid out first.  Kit first (KJR, KRJ, nested): flipped, 145 to 153 (the 5-test comes before the JTAG test).  Retail first as filelist_ini spells it (`type != JTAG && type <= DEVGL16`, both orders after it): 304 and up.
- Why JRK's layout can't be fixed: in the 5-test the true arm is both what PRE reaches first (JKR: kit true, takes the free names; JRK: retail true, takes them) and bbro's round-2 winner (both arm heads are seeds with key -1088880, frequency 880 each, 50/50 with no predictor; the true arm pops).  Breaking it needs a predictor on the 5-test (none for `<=` / `>` against a constant; PRED_CALL needs a call in an arm's first block, and both arms start with an inlined findFile loop).
- switches (every case order, default retail or kit, the default inside a case list, retail with case 0): the case order doesn't matter (one canonical form each).  **Default retail: flipped, 92 loose** (sw_JKR_dR, drafts/build_calcBlAreaSize_sw_JKR_dR_nearmiss.patch): the kit code is right; what's left is the kit's range test (`jb; lea eax,[ecx-6]; cmp eax,3; ja`, where the reference has `cmp ecx,5; jbe`) and a few cold blocks in another order.  It also sends types above 9 to retail, which src doesn't.  Default kit (the reference's `> 5` test): not flipped, 363 and up.
- JRK saved as drafts/build_calcBlAreaSize_JRK_nearmiss.patch (288 loose; the kit arm is the reference's).

### gen_bd471: lab_none by a re-tested r in loadConsoleBlFiles' case 24 (12 cases)

- `r = loadBaseFile(..); if (r || e->size != 0x60) r = defaultBl60(e);`, the two-arm and sequence spellings, a dead re-test: without the label all 231/333, the same as src minus the label; with it `r_two` is IDENTICAL and the rest cost 2 to 6.  The loop's own `if (r)` already tests r, so re-testing it adds no flow there.

### Not done

- gcc's bb-reorder.c couldn't be read (the gcc.gnu.org git web answered with a bot check), so the bbro tie rule above is read from the dumps (both seeds equal, the true arm pops).
- exp_t10, exp_devgl: no new form; attempts 25 to 29 close their frequency side for the re-test lever too (exp_devgl's def block has no thread through it; block 116 needs about 11 off with the tail unchanged).

### Don't retry (attempt 35)

- pin_size through a frequency in the kit sum's thread: the tie is copy order (operand order), not frequency.
- pin_size by the chain's order or nesting as if-forms (gen_bd470): the kit can't be laid out first and get fresh PRE names at once.  Switch case order (one canonical form).
- lab_none by a re-tested r in case 24 (gen_bd471).

### What to try next

- pin_size: a form where the kit is reached by the 5-test's false edge but laid out first, or where PRE reaches retail before the kit while the kit is still the true arm.  The switch with retail as default does both (92 loose); what's left is a natural way to get `> 5` as the kit's test with retail as the switch's default.  Check any idea with bdorder.py first: the kit line must read `size_N + prephitmp_M`.
- A predictor on the 5-test: only worth it with a call that belongs at the start of an arm.
- Otherwise attempt 33's list stands.

### Costs now (strict/loose, removed alone; 11 tricks, unchanged)

As attempt 34 (src unchanged): lab_t5le 7/0, exp_pr 18/2, exp_devgl 43/7, pin_size 82/40, exp_t10 116/46, vol_fail 296/126, lab_none 333/231.

## Attempt 36

Goal: attempt 35's lead, pin_size by a switch on the build type (sw_JKR_dR, 92 loose): keep PRE reaching retail before the kit but get src's semantics (types above 9 to the kit) and the reference's range test and layout.  Generators gen_bd480 to gen_bd484 on src as of 85f296f9 (`python tools/wip/dehint/bdorder.py tools/wip/dehint/bdgen/gen_bd48N.py`; each imports `arms` from gen_bd470).  Scratch in build/bd/a36 (not kept: `nopins.c`, `jrk.c` and `jrk_diag.c`, `max_d_JKR.c`, `all*/` full `-fdump-tree-all` runs, `ch/` the ch2 details dump).  Loose/strict lines in calcBlAreaSize unless said; pin_size off throughout.

### Where the operand order is set (`-fdump-tree-all` of nopins.c)

- The kit sum is `size_41 = size_254 + _40` until PRE, which makes it `prephitmp_229 + size_254`; reassoc2 writes it `size_254 + prephitmp_229` (the order we want) and forwprop4 swaps it back (fold puts the lower SSA version first).  So the order at RTL is purely the two versions.
- size_254 is a PHI that dom2 makes at the 14 loop's exit: dom2 threads the `nFiles <= 0` path through the 13 add into the 14 guard, so the 13 add has two copies (size_37, size_225) merged by size_253 and size_254.  prephitmp_229 comes off the free list: dom2's released names (its SSA-update list ends `.. size_229 _236 size_237 _242 size_243`, popped from the end) under about five names released between dom2 and PRE (136, 195, 109, 87, 214).  The kit's 14 lookup is PRE's first insertion and the prephitmp is its fifth name.  Neither version can be moved past the other by a few names: the free list would have to be empty (about 20 more names used first), or size's PHI made before dom2.

### Why the 5-test's true arm wins both PRE and bbro (ch2, PRE and bbro dumps)

- PRE's insert walk is a preorder of the dominator tree with sons in **descending block index**: bb2's sons, the 5-test bb20 is walked before the JTAG head bb3 (attempt 35's "JTAG is reached last"); bb20's sons, the kit head bb23 before the retail head bb21 in src.
- The arms' block order comes from ch2.  Both arms start directly with a loop header, so each needs a preheader on its edge from the 5-test, and split_edge_bb_loc puts both right after the test: the one created last ends up first.  They are created in FOR_EACH_LOOP order (the loop tree's preorder), and the tree is rebuilt in RPO, i.e. by the test's edge order: the first edge's arm is DFS-visited and finished first, so it is iterated first, its preheader is made first and lands *after* the other arm's.  Before ch2 (tailr2) the kit head is bb23 and retail's bb45; after ch2 retail's copied guard is bb23 and the kit's bb25.  The JRK and switch flips follow exactly this (a switch's first edge is its default's).
- bbro (JRK's dump): both arm heads are round-2 seeds of equal key, and the traces they start are both 4 blocks (guard, copied header, body, latch).  connect_traces joins the test's trace to the successor trace with the higher probability, then the longer trace, then the first edge: in JRK `Connection: 33 37`, retail, the first edge.
- So in an if-form the first edge decides both, and a GIMPLE_COND's first edge is always its true arm.  Ways to decouple them: a probability (but the arms must stay 50/50 to keep the reference's frequencies), a longer kit head trace (fixed by findFile's loop shape), or a retail arm whose head is not a loop header at ch2 time (then retail needs no preheader, the kit's preheader alone goes right after the test, the kit gets the lower index and PRE walks retail first, while the kit stays the true edge and bbro's winner).  The last needs a statement at retail's start that lives until ch2 and leaves no code; retail's first block in the reference is its findFileOffset(5) guard, and I found no such statement (not swept: the obvious candidate, a `type != RETAIL` flag computed there, would likely be forwprop'd into its test before ch2).
- Diagnostic (`jrk_diag.c`: JRK with `__builtin_expect(xb.type <= BUILD_DEVGL16, 0)` at `-p 51` / `52`; not a candidate): the kit is laid out first and its code is the reference's; what's left is 36 lines of cold-block order and one register swap in retail's xell loop (`cmp ecx,eax`), probably both from the 52/48 frequencies.  So a 50/50 way to break the tie would very likely be the match.

### gen_bd480: whole switch, retail as default, kit as a GNU case range (66 cases)

- `case BUILD_DEVKIT ... 0xffffffff:` (src's semantics), `... UINT32_MAX`, `... BUILD_TESTKIT16` (attempt 35's semantics); retail as default, listed plus default, or listed with case 0 and no default; every case order: all flip the kit sum; best 91 loose (`max_d_JKR`, `max_d_RJK`).  Expansion: `cmp 2; je J; jb R; cmp 6; jb R; K..` where the reference has `cmp 2; je J; cmp 5; jbe R; K..`, plus cold-block order.
- Why it can't get closer (the decision tree as gcc 6 emits it): with two case nodes the root is the lowest (JTAG's 2); a single value with only a right child tests `< 2` to the default unless 2 is the type's minimum, and the kit's range is then tested by its own low bound (`< 6`), not by retail's high bound.  Retail is the 5-bound only as a case node, but then it isn't the default, and the default's edge is the one PRE walks first.  Listing every retail type with no default doesn't help: the gimplifier makes the first label (retail's) the default when the labels cover the type contiguously.
- A switch also gives each edge 1/3, so JTAG is 33% instead of the reference's 28% (nonequal on `== 2`); the cold-block order follows from that.

### gen_bd481 to gen_bd483: JTAG as an if, a switch for the rest (36 cases)

- Inner switch with retail as default (`case BUILD_DEVKIT ... 0xffffffff: K; default: R`, or both listed with `0 ... BUILD_DEVGL16` first, which the gimplifier turns into the same): flipped, but expands to `cmp 6; jae K` and lays retail first, 290 loose.  Retail as `case 0 ... BUILD_DEVGL16` with the kit as default: the same code as src, not flipped (40).
- Retail listed without 2 (`case 0 ... BUILD_RETAIL: case BUILD_GLITCH ... BUILD_DEVGL16:`, no default; type 2 can't reach the else): the default goes past the switch, retail stays a case node and the test is `cmp 5`, but the three-node tree adds `ja K; cmp 3; jae R; cmp 1; jbe R` and the layout is retail first (304 and up).  Leaving out case 0 changes type 0's behaviour; not pursued.
- The whole switch with retail as ranges around 2 (`sw_r2*`): the same as gen_bd480 (91); the kit as default 377 and up.

### gen_bd484: an arm through a static helper (12 cases)

- In case an inlined helper's loops keep copy_loops' order instead of the RPO rebuild: the flip still follows the 5-test's true arm, and every helper form moves the setPatchSlot code (134 loose and up).

### Don't retry (attempt 36)

- pin_size by any switch on the build type: whole, inner (after the JTAG if), any case order, GNU ranges, retail or kit listed or as default, case 0, type 2 left out (gen_bd480 to gen_bd483).  The expansion and the default-first walk are incompatible, as above.
- pin_size by arm helpers (gen_bd484).
- Moving prephitmp's or size's version past the other by name counts (the free list is about 20 names deep at the kit's insertion).

### What to try next

- pin_size: the only open route found is a retail arm whose head block isn't the findFileOffset(5) loop header at ch2 time (a statement at retail's start that lives until ch2 and leaves no code, or leaves the reference's), with src's chain order (JKR).  Check with bdorder.py (the kit line must read `size_N + prephitmp_M`) and the ch2 dump (the kit's guard copy must come right after the 5-test).
- Otherwise attempt 33's list stands.

### Costs now (strict/loose, removed alone; 11 tricks, unchanged)

As attempt 34 (src unchanged): lab_t5le 7/0, exp_pr 18/2, exp_devgl 43/7, pin_size 82/40, exp_t10 116/46, vol_fail 296/126, lab_none 333/231.

## Attempt 37

Goal: attempt 36's open route for pin_size: keep src's JKR chain and give retail's arm a first block that isn't its findFileOffset(5) loop header when ch2 runs, so ch2 makes no preheader on the 5-test's retail edge, the kit's preheader alone goes right after the test (lower index), PRE walks retail first (kit sum flipped) and the kit stays the first edge (bbro's tie winner).  Generators gen_bd490, gen_bd491 on src as of 1bf763ac (`python tools/wip/dehint/bdorder.py tools/wip/dehint/bdgen/gen_bd49N.py`; gen_bd491 with `bdrun.py`, it changes other functions).  Scratch in build/bd/a37 (not kept: `nopins.c`, `n_unused.c`, `nfiles_unused.c`, `off_decl.c`, `all/` a pass list).  Loose/strict lines in calcBlAreaSize unless said; pin_size off throughout.

### The route works (gen_bd490)

- `n = xb.nFlashFiles;` (unused local) as retail's first statement: kit sum `size_248 + prephitmp_264`, **10 loose / 10 strict**, and the whole layout is the reference's.  The 10 lines are retail's five loop compares with the operands swapped (`cmp eax,edx` for `cmp edx,eax`).
- `n = xb.nFiles;` (unused): flipped, **2 / 2**: only findFile(25)'s compare (`cmp ecx,eax` for `cmp eax,ecx`).  Saved as drafts/build_calcBlAreaSize_nfiles_load_diag.patch (diagnostic: an unused load whose only job is to steer is a trick).  Both loads (`both_loads`): 12.
- Why the load survives: it is unused in the source, but fre (before ch2) makes it the leader of the later loop-header loads of the same count, so it is live; sink and the guards put it back where the reference loads the count, so it costs no code of its own.  A load nothing later reads (`xb.nFlashFiles2`) is removed by DCE before ch2: 40.
- Why the compares swap (`.optimized` of n_unused.c: `if (n_47 != i_127)` against src's `if (i_127 != _164)`): tree_swap_operands_p puts the lower SSA version first.  In src the loops' bound is ch2's copy of the header load into the guard (`_164`, a late name); with the source load it is n, numbered at into-SSA, below every name einline makes for the inlined loops (einline works through the callees in reverse source order, so retail's calls are inlined first and get fresh names; only names freed by earlier inlines, as JTAG's i_12, come out low).
- Folds before ch2, so the route doesn't open (all 40, src's order): `xs = 0x40000;` (constant), `n = xb.type != BUILD_RETAIL;` tested later (forwprop puts the compare into the cond; also used twice, `flag_twice`: 44 with the order unflipped), `n = xb.type;` (fre reuses the chain's load), `size = findFileOffset(5); size += findFileSize(5);` and `findFileSize(5) + findFileOffset(5)` (the first block is still a loop header).
- The loops' shared guard written out (`size = 0; if (xb.nFlashFiles > 0) { sums }`, and with `else size = 0;`): flipped but 310 loose (the source test is kept as a block of its own, and its load has the low version too).
- JRK with the nFiles load: 300 (retail is the first edge, bbro lays it out first).
- `xb.type >= BUILD_GLITCH` for the xell test (record only, type 0 differs): 44.

### Where the order comes from (ch2 details of nopins.c)

- Loop tree order (`FOR_EACH_LOOP`, preorder): JTAG's 4, 1, 2, 3, then the kit's 5..9, then retail's 15, 10..14; within an arm the loops are in reverse code order (9 is the kit's findFile(11), 14 retail's findFileOffset(5), 15 findFile(25)).  flow_loops_find pushes headers in RPO and flow_loop_tree_node_add prepends, so siblings come out in reverse RPO; the 5-test's first edge (kit) is DFS-finished first, is later in RPO, and so is iterated first.  Preheaders are made for loops 4, 3, 9, 15, 14: retail's 14 is made last and split_edge_bb_loc puts it right after the test (its header's layout predecessor is its own latch, which has an edge into it), in front of the kit's 9: retail gets the lower index.  This is the same as attempt 36 found, read from the loop numbers.
- So the other two ways to keep retail's preheader off the test are closed too: the header's layout predecessor is always the inlined callee's latch, and a second entry edge into retail's head needs a second test whose failure goes there (`&&` in the kit test, a dead or behaviour-changing test; vrp1 runs before ch2 and folds a redundant one).

### gen_bd491: the helpers read the count first

- findFileOffset (and findFileSize) as `int i, n = xb.nFlashFiles; for (i = 0; i < n; i++)` (and `n = ..;` as a statement, in the for's init, declared first): inlined in retail the load is the first block and calcBlAreaSize flips (2 lines left: retail's findFileOffset(5) compare, n's copy numbered before its own loop's i; the later loops and JTAG/kit are fine), but **findFileOffset's own compare swaps** (2 lines there, the same version rule), 4 loose in all; with findFileSize too 6.  findFile in that form: 512 and up (it changes every function that inlines it).

### Don't retry (attempt 37)

- pin_size by a statement at retail's start: any source-level load of a count (nFlashFiles, nFiles, both; unused, or as a written-out guard), constants, a type flag (once or twice), an `xb.type` copy, splitting or reordering the sums (gen_bd490).  The load works for the layout and the kit sum but swaps the loop compares it bounds; the rest fold before ch2.
- pin_size by the helpers reading the count into a local first (gen_bd491): their own standalone compare swaps.
- pin_size by the kit arm's first block (the mirror): the kit's preheader is made first because the kit is the first edge; a kit with no preheader leaves retail's alone right after the test, which is worse.

### What to try next

- pin_size: what's needed now is narrow and known: a block at retail's start at ch2 time whose bound for the following loops is *not* a source-level SSA name (or none at all).  Only an inlined helper's load numbered after retail's loops' i would do (a helper called at retail's start is inlined after them, as einline goes in reverse source order), and no natural helper is there to call; I found no other statement kind that survives to ch2 and leaves no code.  Unless a new idea for that turns up, pin_size is as closed as the switch route.
- Otherwise attempt 33's list stands (attempt 25's windows, attempt 27's exp_t10 weight near miss, attempt 30's c6 vol_fail near miss).

### Costs now (strict/loose, removed alone; 11 tricks, unchanged)

As attempt 34 (src unchanged): lab_t5le 7/0, exp_pr 18/2, exp_devgl 43/7, pin_size 82/40, exp_t10 116/46, vol_fail 296/126, lab_none 333/231.

## Attempt 38

Goal: (A) pin_size by a *live* statement at retail's start (attempt 37's route without its dead `n = xb.nFiles;`), and (B) a rotation onto the less-recently-worked tricks with attempt 34's lever (a re-tested result) and attempt 37's (a statement that changes ch2 / block order).  Generators gen_bd500 to gen_bd503 on src as of 14d2096d (`python tools/wip/dehint/bdorder.py tools/wip/dehint/bdgen/gen_bd500.py`; the others with `bdrun.py`).  Scratch in build/bd/a38 (not kept: `fd.py file.c fn` a unified diff of one function against the reference, `no_*.c` src minus one hint, `*.s` `-dA` assembly with block frequencies, `c6chk*.c`, `dev_*.c`).  Loose/strict lines in the function named unless said.

### (A) What a retail-start statement has to be, by kind

- It must survive to ch2 (so retail's first block isn't the findFileOffset(5) loop header) and then leave no code, or the reference's.  Kinds, and why each fails:
  - a constant, a copy, `size = 0`, a constant address (`xb.files`): gone at into-SSA or ccp1.
  - a flag or compare (`xb.type != BUILD_RETAIL`, used once or twice): forwprop1 puts it into the cond; phiopt1 folds a flag set by an if.
  - an `xb.type` reload: fre1 (no store or call between it and the chain's load).
  - a load of a field nothing else reads (`xb.files[0].type`, `nFlashFiles2`): DCE.  The loops' `files[i].type` loads have a PHI index at fre1, so a `files[0]` load isn't their leader.
  - a load of a count (`nFlashFiles`, `nFiles`): lives as fre1's leader of the later loop-header loads, so it becomes those loops' bound with a source-level (low) version and the compares swap (attempt 37).  Any other spelling of the same load (through a pointer, a cast) value-numbers the same.
  - a load numbered *above* the loops' `i`: only an inlined helper's, and only for a helper called first in retail (einline goes in reverse source order).  Every helper retail calls starts with a loop header; a helper whose body starts with a load swaps its own standalone compare (attempt 37's gen_bd491; the load, gimplifier temp or into-SSA name, is below the loop's `i_2`).
  - a call (log, imgCfSize early): code the reference doesn't have there, or a reordered call.
  - a test whose arms do live work: works for the route, but the work moves (below).
- gen_bd500 (6 cases, pin off): **`x = 0; if (xb.type != BUILD_RETAIL) x = findFile(25);` first, then the sums, then `if (xb.type != BUILD_RETAIL && xb.files[x].offset > size)` (and the nested spelling): kit sum flipped (`size_254 + prephitmp_269`)**, so a real test at retail's start is enough for PRE's walk; but the findFile(25) loop now runs before the sums, 313 loose / 476 strict.  One-expression sums (`size = findFileOffset(5) + findFileSize(5) + .. + findFileSize(8);`): the same GIMPLE as src (40/82).  The kit's and retail's `setPatchSlot(size); size += 2 * imgCfSize();` written once after a nested 5-test: KR 104 loose (not flipped; the tail becomes a PHI join), RK 312.

### (B) Rotation

- gen_bd501 (32 cases), loadBl's signature block with `break` after the arms that leave `*pr` at 0 (the no-key log, the passed log): the same behaviour (type 5/11/17 with `*pr` 0 does nothing in the tail), it takes those paths off the merge `<= 5` block and gives them the early-return predictor.  Crossed with `else if (type)` / plain else and t5le / exp_pr kept or off.  Nothing better than src: no-key break 16/28 at best (with t5le off) plus .rdata (the jump table moves), passed break 47/117, both 82 and up, plain else 54 and up as before.  The failed arm can't break (attempt 14).
- Reading for t5le, rechecked with `-dA` (src minus the label): only the no-key log copy's `.p2align` (final bb 112, freq 17, no fallthru; compute_alignments aligns it when 17 > 10 x its layout predecessor, bb 111, the jmp after the SE copy's `<= 5` test, freq 4 x 42% = 2).  As attempt 19 had it; nothing in gen_bd501 moves the SE copy's P(<= 5) above 62.5% or the no-key log to 21.
- gen_bd502 (11 cases), case 6's checkBl as `if (*pr) break; goto chk;` (the same behaviour: after a good checkBl with type 6 the signature block and the tail do nothing), as a real entry into chk next to the `__builtin_constant_p` one: with every hint 20 loose / 88 strict; with the constant_p entry off **exp_t10 makes no difference** (20/90 with or without it, src minus the entry is 26/78).  What's left in both: bbro copies loadBlFiles' `if (r)` test into case 6's checkBl block (attempt 27's duplication threshold, now on case 6's flow), and the CG and SE paths jump to case 6's checkBl argument setup instead of having their own (crossjump), plus the type-11 block's place when the entry is off.  Case 6's own flow can't be lowered (its load-failure test is a call result, 29%), so not taken further.
- gen_bd503 (7 cases), exp_devgl by a re-tested result (`if (!fuse && dev) fuse = 1;`, `fuse == 0 &&`, nested, `if (!fuse) fuse = dev;`, the dev test first, raw glitch2mfg): the re-test keeps a branch on the flag (`je`) where the reference has `cmovbe` (10 loose / 598 strict; the `fuse = dev` assignment 12/181).  Expect off throughout; src minus the expect is 7/43.
- Not swept: lab_none and the barrier (no new lever: lab_none's two round-4 blocks are ordered by frequency, 14 against 20, not by a tie that block numbering could break; the barrier's crossjump order is fixed by the fallthru predecessor, attempt 31).

### Don't retry (attempt 38)

- pin_size by a live test at retail's start that hoists the xell lookup (gen_bd500: the loop moves), by one-expression sums, by the kit/retail tail written once.  The kinds of statement listed above.
- t5le / exp_pr / `else if (type)` by `break` closing the no-key or passed arm (gen_bd501).
- The constant_p entry or exp_t10 by case 6 through `goto chk` (gen_bd502).
- exp_devgl by a `!fuse` re-test (gen_bd503).

### What to try next

- pin_size: the only form found that flips the kit sum with src's chain and no dead code is a real test at retail's start, and the only test retail has is the xell one, whose work can't move.  Unless the program has another reason to test something at retail's start, pin_size stays.
- gen_bd502 is the first form where exp_t10 is free (with the constant_p entry off), but only because case 6's flow swamps the shared chk copy; the reference's case 6 has its own checkBl call that jumps straight to loadBlFiles' `if (r)` test (`mov edi,eax; jmp b3`), i.e. src's case 6, so this is not the reference's structure.  Worth a look only as a reading of what the shared copy's frequency does.
- Otherwise attempt 33's list stands.

### Costs now (strict/loose, removed alone; 11 tricks, unchanged)

As attempt 34 (src unchanged, re-measured with bdhints.py): lab_t5le 7/0, exp_pr 18/2, exp_devgl 43/7, pin_size 82/40, exp_t10 116/46, vol_fail 296/126, lab_none 333/231.

## Attempt 39

Goal: step back from the per-hint levers and change how the data reaches loadBl: parameters against computed locals, a field against a local, the loop's scopes and IV, the split between loadBl and loadBlFiles, the type of the switch variable.  Each form is crossed with the loadBl-side tricks off one at a time (exp_t10, exp_pr, lab_t5le, vol_fail, lab_none, `etype` = plain else, `cp` = the constant_p entry as `if (0)`).  Generators gen_bd510 to gen_bd512 on src as of a9cb46e0 (`python tools/wip/dehint/bdrun.py tools/wip/dehint/bdgen/gen_bd51N.py`; gen_bd511 and gen_bd512 import `off` / `OFFS` from gen_bd510).  Scratch in build/bd/a39 (not kept: `*.inl` are `-fdump-ipa-inline-details` of src and of the uint8_t case).  Loose/strict lines in loadBlFiles unless said.

### gen_bd510: the interface (80 cases)

- **Equal bases (IDENTICAL with every hint; each hint off costs exactly src's 7/0, 18/2, 116/46, 296/126, 333/231, etype 128/54, cp 78/26):**
  - `edata`: the type-14 tail as `setFlashBuild(getBeU16(e->data + 2))`.  So the reference's `imul` recompute of `xb.files[i].data` (attempts 11, 21) comes from the threads, not from the spelling.  With this form `i` is only used by the constant_p entry, which would make `i` part of the trick if the entry ever goes.
  - `rscope` / `escope`: `uint32_t r = 0;` (and `struct fileent *e = &xb.files[i];`) declared in loadBlFiles' loop body.  The CLOBBER of the address-taken r at the end of each iteration changes nothing after SRA / into-SSA.
- `c2slot` (case 2 through `struct fileent *f = &xb.files[xb.nFlashFiles];`): 18 loose, .rdata moves.  The slot address isn't reloaded after the call, and the reference reloads it.
- `eptr` (`for (i = 1, e = &xb.files[1]; ..; i++, e++)`): 355 loose.
- `iarg` (`loadBl(uint32_t i, uint32_t *pr)` with `e = &xb.files[i]` inside), `noneinbl` (the strnicmp / crc skip as loadBl's first statement, `if (..) return;`), `noneinbl+iarg`, `iarg+escope`: **loadBl is not inlined** (loadBl / loadBl.constprop out of line, 10000+ lines).

### gen_bd511: narrow `type` locals (48 cases)

uint8_t, uint16_t, signed char, short, int8_t, int16_t: every one leaves loadBl out of line, as `iarg` does.

### Why loadBl is inlined at all (read from `-fdump-ipa-inline-details`, src against the uint8_t case)

- In src, loadBl's inline summary splits its size by predicates on the parameter load `e->type` (`op0[ref offset: 8224] == 27`, `== 24`, `<= 21`, ...): unconditional size 29, plus one entry per case.  The call is enqueued (badness -0.0017) and inlined ("net change of -39").
- With `uint8_t type` the switch is on a converted value, so ipa-inline-analysis makes no case predicates: unconditional size 234.5, and the edge is refused with "--param max-inline-insns-auto limit reached".  With `iarg`, `e` is no longer a parameter (it is `&xb.files[i]` with i the parameter), so the same thing happens.  With `noneinbl`, the early return comes before the switch.
- So any reshaping of loadBl must keep `switch (type)` on a full-width copy of the parameter's field load, with nothing before it that the predicates can't see through.  That explains part of the 9999 rows in earlier sweeps too.

### gen_bd512: chk's type from the field (54 cases)

- `fld_ck` (checkBl's argument as `e->type`): 9/58 with every hint, so not an equal base.  cp off 35 (src 26), exp_t10 off 55 (src 46), cp + exp_t10 off 37.  The reload after loadInputFile / suGetCF / suGetCG does take the constant type away from vrp1's shared copy (that is what cp imitates), but it adds a load and moves the 9/10 arms.
- `rl` (`chk: type = e->type;`), `fld` (all uses after chk), `fld_tail`, `fld_t0`, `fld_t2`: 103 loose and up.

### Don't retry (attempt 39)

- The tail through `e->data`, a loop-body r or e (equal bases: they free nothing).
- loadBl taking i instead of e, any narrow type for its `type` local, the skip test inside loadBl: loadBl stops being inlined (see the inline reading).  Don't build forms that put a statement before the switch or switch on a converted value without checking the inline dump first (`-fdump-ipa-inline-details`, "Inline summary for loadBl").
- A pointer IV in loadBlFiles' loop; case 2's slot through a local pointer.
- chk's type, or the tests after chk, read from e->type (gen_bd512).

### What to try next

- If the constant_p entry is ever replaced, `edata` lets `i` go from loadBl's parameters.  Score that form together with the entry's replacement.
- The inline reading gives a check for whole-function reshapes (attempt 9's and 30's reconstructions): a reshape that only scores 9999 is an inlining refusal, not a bad shape.  Reconstructions that lost that way might be worth rescoring with the switch kept first on the parameter's field.
- Otherwise attempt 33's list stands (attempt 25's windows, attempt 27's exp_t10 weight near miss, attempt 30's c6 vol_fail near miss).

### Costs now (strict/loose, removed alone; 11 tricks, unchanged)

As attempt 34 (src unchanged; re-measured by gen_bd510's `src|` rows): lab_t5le 7/0, exp_pr 18/2, exp_t10 116/46, vol_fail 296/126, lab_none 333/231, etype 168/94 in the object (128/54 in loadBlFiles), cp 118/66 in the object (78/26 in loadBlFiles); exp_devgl 43/7 and pin_size 82/40 as attempt 38.

## Attempt 40

Goal: attempt 39's lead.  If loadBl is inlined only while the inline summary splits its size by case predicates, earlier sweeps may have rejected good shapes only because loadBl went out of line; find those families, give them a form that stays inlined, and rescore them with the hints on and off.  Then attempt 39's "What to try next".  Generators gen_bd520 to gen_bd522 on src as of 53c5fc43 (`python tools/wip/dehint/bdrun.py tools/wip/dehint/bdgen/gen_bd52N.py`).  Scratch in build/bd/a40 (not kept: `inl.sh file.c` prints loadBl's inline decision from `-fdump-ipa-inline-details`, `d_src`, `d_u8`, `d_u8b` are the inline dumps of src, the uint8_t form, and the uint8_t form with `--param max-inline-insns-auto=2000` (diagnostic only, to print the refused edge's badness), `fd.py file.c fn` is a unified diff of one function against the reference, `scan/` holds the rescan below).  Loose/strict lines in loadBlFiles unless said.

### What really gates loadBl's inlining (read from `-fdump-ipa-inline-details`)

- src: `Considering loadBl/55 with 533 size ... size growth 494, time 37  big_speedup ... time w/o inlining 664, time w inlining 552, overall growth -39`.  It is inlined by the small-function inliner, not as a function called once.
- The uint8_t form, with the auto limit raised only to print the badness, also has `big_speedup` (671 against 559).  So the speedup isn't what differs.  In the normal compile the edge is refused before badness is computed (`not inlinable: loadBlFiles/56 -> loadBl/55, --param max-inline-insns-auto limit reached`), and its summary has `min size: 500` (src: about 30, the size outside every predicate).  That fits want_inline_small_function_p's early test (from memory, consistent with both dumps): for a callee not declared inline, refuse when `min_size - call_stmt_size > MAX (max-inline-insns-single = 400, max-inline-insns-auto = 40)`.
- min_size is the size under the `(true)` predicate plus the calls outside a predicate.  In src nearly everything is under a case predicate (`op0[ref offset: 8224] == N`), because the switch index is an unmodified load of the parameter's field.  With no case predicates (a converted index, an index loaded after a call such as strnicmp, `e` not a parameter) the whole body is unconditional, about 500, over 400.  Statements before the switch are fine as long as the switch still gets its predicates and the unconditional part stays under about 400.

### Rescan: which earlier sweeps had a refusal (build/bd/a40/scan/summary.txt)

- Every generator from gen_bd320 to gen_bd503 was rerun against src (`bdrun.py -n 1000`, then the 9999 rows counted).  Those that still run (most of them; gen_bd330, gen_bd340 to gen_bd342, gen_bd350, gen_bd454, gen_bd460 have ERR rows from older bases, gen_bd461 to gen_bd463 stop on bdhints' missing pin_d) have **no loadBl refusal row**.  gen_bd372's two 9999 rows are a `defaultBl60.isra.0` clone, not loadBl.  gen_bd411, gen_bd414 and gen_bd415 (attempt 30's reconstructions) were checked first, by hand: 0 refusals.
- Older generators mostly don't apply to today's src.  Of the attempt 9 reconstructions, gen_bd202 runs: its 24 `in` rows (the none test inside `static int loadBl(e, i)`, r returned) are refusals, because the type is loaded after strnicmp.  gen_bd204 has none.
- So the refusals are attempt 39's families (`iarg`, `noneinbl`, narrow locals) and gen_bd202's `in` rows.  The 9999 rows attempt 39 mentioned were in those generators only, not spread through the earlier sweeps.

### gen_bd520: attempt 39's refusals redone so that loadBl stays inlined (56 cases, every hint on and each loadBl-side hint off alone)

- `nib_and` / `nib_nest`: the none test as loadBl's first statement after `type = e->type;` (the load comes before strnicmp, so the case predicates stay), the caller calling loadBl without the test.  Inlined, but **207 loose / 443 strict with every hint, and the same with exp_t10, t5le, exp_pr or cp off**: the hints stop mattering because the whole profile has moved.  In src the none test gets PRED_CALL (29%) from the loadBl call in its guarded block (attempt 9).  Inside loadBl it is an early return.
- `sw_<type>`: `switch (e->type)` on the field with a narrow `type` local for the rest: inlined; uint8_t 143, uint16_t 138 loose with every hint (byte and word compares, and VRP knows the range).  `unsigned` / `uint32_t` 38 loose, as gen_bd450's retyping.
- `iarg` (`e` computed from `i` in loadBl) can't be rescued this way: a switch on `xb.files[i].type` isn't a load through a parameter, so it has no predicates.  The natural way to drop the interface change is the next item.

### gen_bd521: loadBl without `i` (98 cases)

- Attempt 39's `edata` (the tail's setFlashBuild reads `e->data`) leaves `i` used only by the constant_p entry.  With that entry's first term on a field (`(char *)__builtin_constant_p(e->crc) == (char *)1 && ..`, also `e->size`, `e->offset`) and `i` dropped from loadBl's parameters (`loadBl(e, &r)`): **IDENTICAL** with every hint, and each hint off costs what it costs on src (t5le 0/7, exp_pr 2/18, lab_none 231/333).  The entry on `e` itself is cp-off's 26/78, and on `type` alone 26/69 (attempt 27's one-constant_p weight).
- An equal base that frees nothing: the two `__builtin_constant_p` stay, now naming a field.  Note it if the entry is ever replaced: loadBl then needs no `i` at all.

### gen_bd522: attempt 9's reconstruction C with the none test inside, rescued (48 cases, no hints, as gen_bd202)

- With `int type = e->type;` above the none test, the helper returning r is inlined again.  The `in` rows are 347 loose at best against gen_bd202's own `r0` call form at 225 (both are far from src's hint-free 165).  The none test inside the helper is worse for the same reason as gen_bd520's `nib`.

### Don't retry (attempt 40)

- The inlining lead for old sweeps: nothing in gen_bd320 to gen_bd503 was rejected by a refusal, and the families that were (attempt 39's, gen_bd202's `in`) are worse once they stay inlined.
- The none test inside loadBl in any form that keeps loadBl inlined (gen_bd520, gen_bd522): the call site's PRED_CALL is part of the reference's profile.
- `switch (e->type)` with a narrow or unsigned `type` local (gen_bd520).
- loadBl without `i` as a lever (gen_bd521): an equal base only.

### What to try next

- When a reshape scores 9999 on loadBl, check `min size` in the inline summary first: the fix is to keep the switch on an unmodified load of `e->type` (load it before any call or store), not to shrink the body.  The budget for code outside the switch is about 370 size units.
- Nothing new opened for the remaining tricks.  The closest bases are still attempt 27's exp_t10 weight near miss (block 116 at 99 against 88), attempt 30's c6 vol_fail near miss and attempt 25's windows.  The edata / no-`i` base is an alternative start if the constant_p entry is reworked.

### Costs now (strict/loose, removed alone; 11 tricks, unchanged)

As attempt 39 (src unchanged; re-measured by gen_bd520's and gen_bd521's `src|` rows): lab_t5le 7/0, exp_pr 18/2, exp_t10 116/46, vol_fail 296/126, lab_none 333/231, etype 168/94 in the object (128/54 in loadBlFiles), cp 118/66 in the object (78/26 in loadBlFiles); exp_devgl 43/7 and pin_size 82/40 as attempt 38.

## Attempt 41

Goal: the two tricks outside loadBl with the least recent work, exp_devgl (buildFlash) and lab_none (loadConsoleBlFiles), from the RTL if-conversion side for exp_devgl and by natural loop / case 24 shapes for lab_none.  Generators gen_bd530 to gen_bd532 on src as of 932a083f (`python tools/wip/dehint/bdrun.py tools/wip/dehint/bdgen/gen_bd53N.py`; gen_bd531 and gen_bd532 import PRECHECK / TAIL from gen_bd530).  Scratch in build/bd/a41 (not kept: `nodev.c` is src without exp_devgl, `nonone.c` src without the precheck and the cold label, `hand2.c` gen_bd532's `plain two_fail1st`).  Loose/strict lines in the focus function unless said.

### exp_devgl: why if-conversion can't make the cmovbe once sink has moved the setne (read, `bddump.sh build/bd/a41/nodev.c buildFlash ce1,ce2,ce3`)

- Without the expect, ce2 (after combine) sees `IF-THEN-JOIN block found, pass 1, test 3, then 4, join 5`: test 3 is the dev test (`add -4; cmp 1; jleu`), then-block 4 is sink's split edge holding `(set flags (compare g 0))` and `(set fuse (ne:SI flags 0))` (`*setcc_si_1_movzbl`), and `fuse = 1` is already set in the entry block (insn 33, moved up by ce1's IF-CASE-2 on the JTAG test, which is why `mov ebx,1` leads both versions).  The conversion fails and nothing is logged for it: gcc 6's multi-insn then-block support (bb_valid_for_noce_process_p / insn_valid_noce_process_p, from memory, consistent with the dump) refuses any insn that sets the condition's cc register, and the setne's compare sets flags.  ce1 sees the same block before combine; ce3 after reload too.  noce_convert_multiple_sets has the same cc rule.
- So the reference's `setne` above the test followed by `cmovbe` can only come from GIMPLE that keeps `_64 = _63 != 0` in bb3 (the dev test's block) through sink: the dev arm is then an empty block, out-of-SSA puts `fuse = 1` on it, and ce1 if-converts a one-insn arm with a constant (the cmovbe from `mov eax,1`).  That is attempt 15's rule again (non-dev edge >= 75% of bb3, has 73%), or a second use of the value in bb3, or the value reaching the PHI on two edges; attempt 16 and 25 closed those.  No RTL-side shape is left to try: every then-block that computes the flag contains a compare.
- Not swept (each was already tried or follows from the above): ternary / min-max / `|` forms all fold to the same GIMPLE (gen_bd236, gen_bd343); the override first (gen_bd442); `!fuse` re-tests (gen_bd503); the def hoisted above the JTAG test (bb2 is hotter, so sink moves it further).

### gen_bd530: lab_none by the none test as a `continue` (28 cases)

- Idea: PRED_CONTINUE on the skip edge would raise the switch's share of the loop body (75% from the `||`), and so case 24's sites and the r = 1 block (14, needs 21), without moving the not-entered return (20).  Forms `!strnicmp && !crc` continue, `== 0` spelling, nested; crossed with case 24 two calls / `||`, the precheck + label kept or gone, and loadBlFiles spelled the same or not.
- All 169 loose and up in loadConsoleBlFiles (buildFlash and blmodMissing move too, .rdata changes); loadBlFiles with continue +120.  The skip path no longer passes the `if (r)` test at profile_estimate, and that test's frequency is part of the reference's layout.  Src's `label src or lb` (the `||` case 24 with the label) is 2/2, irrelevant.

### gen_bd531: the `if (r)` exit inside the none test's block (4 cases)

- `if (r) { log; return -1; }` moved inside the `if (strnicmp || crc)` block, r = 0 at the top or inside the block: 169 / 173 loose, the same as gen_bd530's continue: it is the skip path's pass through the r test that matters, not the continue predictor.

### gen_bd532: defaultBl60 written out in loadConsoleBlFiles' case 24 (8 cases)

- Idea: the malloc NULL test predicted in loadConsoleBlFiles' own profile instead of the late-inlined defaultBl60.isra.0's 10.1%.  Two copies or one under `||`, failure or success first, precheck + label kept or gone.
- Worse: the inlined test gets 9% (bbro `call malloc p9100`), so r = 1 drops to 12; plain base 8/16 (the two error logs' order flips too), `||` 6/10, with the label 2/2 (`||`) and 4/8 (two copies).  So the helper's own profile is already the more favourable one for r = 1.

### Don't retry (attempt 41)

- exp_devgl by any shape whose setne ends up in the non-dev arm: RTL if-conversion refuses a then-block containing the compare (ce1 / ce2 / ce3 dumps); only GIMPLE that sink leaves alone can give the cmovbe.
- lab_none by a `continue` for the none test, or by testing r only inside the none test's block (gen_bd530, gen_bd531): the skip path must pass the `if (r)` test.
- lab_none by defaultBl60's body written out in case 24 (gen_bd532): 9% instead of 10.1% for the NULL arm.

### What to try next

- exp_devgl stays where attempts 15, 16 and 25 put it: a second predictor on the dev test, a use of the flag in bb3, or the flag reaching the join on two edges, each by code with no other effect; none is known.  Don't spend another attempt on it without one of those three.
- lab_none: the r = 1 block (14) and the not-entered return (20) are set by defaultBl60's own profile (10.1%), case 24's PRED_CALL tests (29% each) and the loop's two exits (4.5%); attempts 18, 22, 25, 32, 35 and 41 have now moved each factor alone with no natural form.  A route would have to change two factors at once (for example the `||` case 24, 18 of 21, plus anything worth 17% more at the sites).
- Otherwise attempt 40's list: the closest bases are still attempt 27's exp_t10 weight near miss, attempt 30's c6 vol_fail near miss and attempt 25's windows.

### Costs now (strict/loose, removed alone; 11 tricks, unchanged)

As attempt 40 (src unchanged): lab_t5le 7/0, exp_pr 18/2, exp_t10 116/46, vol_fail 296/126, lab_none 333/231 (8/4 with the precheck gone too), etype 168/94 in the object (128/54 in loadBlFiles), cp 118/66 in the object (78/26 in loadBlFiles); exp_devgl 43/7 (re-measured: `bdlib.py build/bd/a41/nodev.c`), pin_size 82/40 as attempt 38.

## Attempt 42

Goal: interactions, as the brief asked: remove every pair (and the cheap triples) of hints on src and on the known near-miss bases, look for any set whose cost is far below the sum or near 0, check whether the param value interacts once expects go, then attempt 41's "What to try next".  Generators gen_bd540 to gen_bd543 on src as of 92fa270c (`python tools/wip/dehint/bdrun.py tools/wip/dehint/bdgen/gen_bd54N.py -n 1000`), and `tools/wip/dehint/bdpsweep2.py base:hint,hint ... [-r LO-HI]` (bdpsweep.py on gen_bd540's bases with etype / cp, plus a no-`--param` row).  Scratch in build/bd/a42 (not kept: `mk.py base hints out.c` writes one case, `mat.py` / `matf.py` turn bdrun output into the tables below, `np.py` the no-param runs, `u16.py` / `se.py` the SE-test runs).

Items: bdhints' 7 (exp_t10, exp_pr, lab_t5le, vol_fail, lab_none, pin_size, exp_devgl), `etype` (the plain else for `else if (type)`) and `cp` (the constant_p entry as `if (0)`, two tricks).  Bases (gen_bd540's `BASES`): `src`; `and9` (attempt 25's fallback); `c2` (and9 + fail closing case 2, barrier kept; IDENTICAL); `c6` (c2 + case 6 first; a base only once vol_fail is off); `noi` (gen_bd521's `noi_crc`: edata, the entry's first term on `e->crc`, loadBl without `i`; IDENTICAL); `wt` (attempt 27's weight, `.. && __builtin_constant_p(type) == 1`; 26/36 with every hint, the near miss once exp_t10 is off).

### The matrix (gen_bd540, 276 cases)

"+d" = the callers' 40 loose lines of call displacement on top (loadBlFiles changes length; loadConsoleBlFiles 18, buildFlash 20, blmodMissing 2), which is all the other-function cost of the cp-off and exp_t10-off rows.  The src table is the whole object, so its cp, etype and exp_t10 cells carry that 40.

Object loose/strict, src (diagonal = alone):

| | exp_t10 | exp_pr | lab_t5le | vol_fail | etype | cp | lab_none | pin_size | exp_devgl |
|---|---|---|---|---|---|---|---|---|---|
| exp_t10 | **46/116** | 70/124 | 68/120 | 144/312 | 114/191 | 68/120 | 277/449 | 86/198 | 53/159 |
| exp_pr |  | **2/18** | 2/13 | 119/278 | 56/128 | 68/122 | 233/351 | 42/100 | 9/61 |
| lab_t5le |  |  | **0/7** | 126/296 | 80/146 | 66/118 | 231/340 | 40/89 | 7/50 |
| vol_fail |  |  |  | **126/296** | 172/339 | 86/257 | 349/625 | 166/378 | 133/339 |
| etype |  |  |  |  | **94/168** | 120/191 | 317/497 | 134/250 | 101/211 |
| cp |  |  |  |  |  | **66/118** | 289/447 | 106/200 | 73/161 |
| lab_none |  |  |  |  |  |  | **231/333** | 271/415 | 238/376 |
| pin_size |  |  |  |  |  |  |  | **40/82** | 47/125 |
| exp_devgl |  |  |  |  |  |  |  |  | **7/43** |

loadBlFiles loose/strict on the other bases:

| and9 | exp_t10 | exp_pr | lab_t5le | vol_fail | etype | cp |
|---|---|---|---|---|---|---|
| exp_t10 | **28/80+d** | 30/84+d | 28/80+d | 87/234 | 74/151+d | 28/80+d |
| exp_pr |  | **2/18** | 2/13 | 93/258 | 56/128 | 28/82+d |
| lab_t5le |  |  | **0/7** | 60/232+d | 54/121 | 26/78+d |
| vol_fail |  |  |  | **60/232+d** | 132/299+d | 86/257 |
| etype |  |  |  |  | **54/128+d** | 80/151+d |
| cp |  |  |  |  |  | **26/78+d** |

| c2 | exp_t10 | exp_pr | lab_t5le | vol_fail | etype | cp |
|---|---|---|---|---|---|---|
| exp_t10 | **28/80+d** | 28/80+d | 28/80+d | 35/105+d | 74/151+d | 28/80+d |
| exp_pr |  | **0/14** | 2/13 | 9/81+d | 54/126 | 26/78+d |
| lab_t5le |  |  | **0/7** | 9/81+d | 54/121 | 26/78+d |
| vol_fail |  |  |  | **9/81+d** | 63/175 | 35/119 |
| etype |  |  |  |  | **54/128+d** | 80/151+d |
| cp |  |  |  |  |  | **26/78+d** |

| c6 (barrier kept: 80/171) | exp_t10 | exp_pr | lab_t5le | vol_fail | etype | cp |
|---|---|---|---|---|---|---|
| exp_t10 | **68/189** | 68/192 | 68/191 | 29/87+d | 104/242 | 28/80+d |
| exp_pr |  | **40/131+d** | 42/135+d | 1/21 | 84/217+d | 26/78+d |
| lab_t5le |  |  | **40/131+d** | 1/14 | 84/216+d | 26/78+d |
| vol_fail |  |  |  | **1/7** | 55/135+d | 35/119 |
| etype |  |  |  |  | **84/219** | 80/151+d |
| cp |  |  |  |  |  | **26/78+d** |

| noi | exp_t10 | exp_pr | lab_t5le | vol_fail | etype | cp |
|---|---|---|---|---|---|---|
| exp_t10 | **46/116** | 30/84+d | 28/80+d | 104/272+d | 74/151+d | 28/80+d |
| exp_pr |  | **2/18** | 2/13 | 119/278 | 56/128 | 28/82+d |
| lab_t5le |  |  | **0/7** | 86/256+d | 80/146 | 26/78+d |
| vol_fail |  |  |  | **86/256+d** | 132/299+d | 86/257 |
| etype |  |  |  |  | **54/128+d** | 80/151+d |
| cp |  |  |  |  |  | **26/78+d** |

| wt (26/36 itself) | exp_t10 | exp_pr | lab_t5le | vol_fail | etype | cp |
|---|---|---|---|---|---|---|
| exp_t10 | **2/53+d** | 4/60+d | 2/56+d | 60/234+d | 56/130+d | 28/80+d |
| exp_pr |  | **28/47** | 28/40 | 111/272 | 56/128 | 28/82+d |
| lab_t5le |  |  | **26/43** | 86/252+d | 54/121 | 26/78+d |
| vol_fail |  |  |  | **86/252+d** | 114/279+d | 86/257 |
| etype |  |  |  |  | **54/128+d** | 80/151+d |
| cp |  |  |  |  |  | **26/78+d** |

Triples (loadBlFiles loose): on src exp_t10+exp_pr+cp 30, exp_t10+lab_t5le+cp 28, exp_pr+lab_t5le+cp 28, exp_t10+exp_pr+lab_t5le 30; on c2 exp_t10+vol_fail+cp 35, exp_pr+vol_fail+cp and lab_t5le+vol_fail+cp 35, exp_pr+lab_t5le+vol_fail 11; on c6 exp_pr+lab_t5le+vol_fail 3/20.  Every triple with etype is 54 and up; with vol_fail on src / and9 / noi 86 and up.  None is below its cheapest pair.

Readings:
- **Not additive any more.**  Attempt 18 found all triples additive (16 tricks then); now the loadBl items form one cluster.  cp off makes exp_t10 cost +2 (28 against 46 alone on src and noi), and with exp_t10 and cp both off exp_pr and t5le add only 2 more (30 for 5 tricks).  The 28 is always attempt 27's two effects (bbro's dup of `if (r)` into the merged checkBl call block, block 116 at 99 against 88; the type-11 block moved after the SE copy), so cp off and exp_t10 off are two routes to one layout.  On and9 / c2 exp_t10 alone is already 28: the fallback reshape does half of what cp does.
- **etype is independent of the cluster** (54 on top of anything), and vol_fail only drops on c2 / c6 (attempts 26 and 30's mechanism, unchanged by the others).  lab_none, pin_size and exp_devgl are additive with everything (other functions).
- No pair or triple is near 0 except the known alignment-only ones: lab_t5le 0/7 (every base), exp_pr on c2 0/14, exp_pr+lab_t5le 2/13, vol_fail on c6 1/7 (with t5le 1/14, with exp_pr 1/21, both 3/20).

### The param (bdpsweep2.py, 50 to 99 and no `--param`)

- No value makes any near-zero set IDENTICAL: lab_t5le 0/7 at 94 to 98 on and9 / c2, 96 to 99 on noi; c2 exp_pr 0/14 at 94 to 98; c6 vol_fail 1/7 at 96 to 98; exp_pr+lab_t5le 2/13.  Below about 94 they all jump to 26 and up (the remaining expects need the param).
- **Without `--param` (gcc's 90) every function except loadBlFiles still matches**: exp_devgl only needs the non-dev edge >= 75%, so the param is there for exp_t10 and exp_pr alone.  With both expects off the param can go: src exp_t10+exp_pr at no param 30/84, + cp + lab_t5le 30/82 (6 tricks for 30 lines), c2 + vol_fail 37/109 (7 tricks).  src exp_t10 alone is 46 at p = 98 and 28 at no param (exp_pr's expect at 90 instead of 98).
- **wt at no param (new near miss, drafts/build_loadBl_wt_noparam_nearmiss.patch):** exp_t10 off 2/55 (the dup only); exp_t10 + exp_pr + lab_t5le off **4/59**, the same at every p from 85 to 99 and with no param (the dup and the SE copy's `ja` for `jbe`).  So on the weight base the param, exp_t10, exp_pr and t5le are one dup and one branch sense away.  BDP=90 bbro dump of that case: block 116 still 99 (`Trace 47 (round 3): 11 [78] 115 [72] 116 [99]`, `Duplicated bb 117`), the frequency attempt 27 read at 98, so the param doesn't touch the dup.
- On attempt 28's u16 diagnostic (the SE test as one word compare) with wt: exp_t10 off 4/39 at no param, + exp_pr + t5le 6/43 (the word compare's lines and exp_pr's one line).  So a natural SE-frequency fix would take the param, exp_t10 and t5le together (diagnostic only; build/bd/a42/u16.py).  Without wt the u16 base with exp_t10 and cp off is 30 (the type-11 block again).

### Natural changes on the cluster's residue

- gen_bd541 (108 cases): the signature test's leaf order (all six, the Linux build's 17, 5, 11 among them) on src / and9 / c2 with the cluster sets off: nothing below the src order's numbers (each other order adds 4 or 6 loose, as attempt 24 found).
- gen_bd542 (28 cases): gen_bd502's case 6 through `goto chk` on the bases with the cluster off: c2 + exp_t10 + cp + vol_fail **18/70**, + exp_pr + lab_t5le 20/74 (6 tricks); at no param with exp_t10 + exp_pr off the c6 base is 17/61.  What's left is five separate items (the size log's own -1, the dup, case 6's checkBl crossjumped into the others, the type-11 block, `ja`), and case 6 through chk isn't the reference's structure (attempt 38).  Not taken further.
- The SE test with a 0-compare spelling (so PRED_TREE_OPCODE_NONEQUAL would not apply; build/bd/a42/se.py): `!(d[0] ^ 'S')` and `d[0] - 'S' == 0` fold back to `== 'S'` before profile_estimate (the same 4/59 on wt); `((d[0] ^ 'S') | (d[1] ^ 'E')) == 0` and `getBeU16(e->data) == 0x5345` change the code (80 and up).  Closed, and the first two would have been hint spellings anyway.

### Attempt 41's "What to try next": lab_none by two factors (gen_bd543, 18 cases)

- Case 24's forms in loadConsoleBlFiles (two calls, `||`, the glitch test folded into the condition, the glitch test as an enclosing if, breaks on the keep path, nested, `r = load; if (r || size)`), each with the precheck + cold label kept or gone: with the label kept two calls and the enclosing-if form are IDENTICAL and the `||` forms 2/2; without it src's two calls (4/8) are still the best (`||` forms 6/10, break forms 10/18).  The residue is the same two tail blocks in the other order (`mov edx,1; jmp` against `xor eax,eax; ret`).  No case 24 form adds the 17% attempt 41 asked for.
- exp_devgl: nothing new (attempt 41's rule: it needs a second predictor, a use of the flag in bb3 or two edges to the join).

### Don't retry (attempt 42)

- Pair / triple removal sweeps on these bases (the matrix above), and param sweeps of the near-zero sets (none matches at any value).  Dropping the param while exp_t10 or exp_pr stays.
- The signature test's leaf order with the cluster off (gen_bd541); case 6 through chk with the cluster off (gen_bd542).
- The SE test through 0-compares, an or of xors, or getBeU16.
- lab_none by case 24's forms with or without the precheck (gen_bd543).

### What to try next

- The one target worth an attempt is the dup on the wt / no-param base (drafts/build_loadBl_wt_noparam_nearmiss.patch): block 116 at 99 must drop under 88 (attempts 27 and 28's formula: 70.8 from type 9's non-SE path plus 29 from CG success).  If it goes, re-check the `ja` (t5le / exp_pr's line) on that base first; together they would take 11 to 7 (param, exp_t10, exp_pr, t5le) and leave the two constant_p in the weight form.  Read attempt 28's factor list before sweeping: each factor was found fixed by gcc 6's heuristics.
- If cp is ever replaced naturally, exp_t10 is nearly free with it (28 on any base, the dup and type-11 effects), and the param follows exp_pr.
- Otherwise attempt 40's list stands.

### Costs now (strict/loose, removed alone; 11 tricks, unchanged)

As attempt 41 (re-measured by gen_bd540's src rows): lab_t5le 7/0, exp_pr 18/2, exp_t10 116/46, vol_fail 296/126, lab_none 333/231, etype 168/94 in the object (128/54 in loadBlFiles), cp 118/66 in the object (78/26 in loadBlFiles), exp_devgl 43/7, pin_size 82/40.

## Attempt 43

Goal: attempt 42's new near miss (drafts/build_loadBl_wt_noparam_nearmiss.patch: the `wt` weight of the constant_p entry, exp_t10, exp_pr and lab_t5le off, no `--param`; loadBlFiles 4 loose / 59 strict), i.e. its two effects, the bbro dup of `if (r)` into block 116 and the SE copy's `ja` for `jbe`, by re-reading attempts 18 and 27 to 29 in the no-param context.  Scratch in build/bd/a43 (not kept: `nm.c` is src with the patch, `show.py file fn ctx [-np]` prints a function's diff with context, `nm.bbro` / `nm.vrp1` / `nm.pe` the dumps at BDP=90).  Generator gen_bd550 (run with `BDEXTRA='--param builtin-expect-probability=90'`: bdrun always passes 98 first and the later `--param` wins, and 90 is gcc's default).

### Block 116 on the near miss (bbro, `bdblocks.py build/bd/a43/nm.bbro`, against src's)

- Unchanged from attempt 28: old 115 (type 9's non-SE argument block) 72 and old 114 (CG's argument block) 27, crossjumped into old 116 at 99 against the threshold 88 (entry 882).  On src the CG block is 2 (exp_t10 at 98%), so 116 is 74.  The param doesn't reach these: with no expect left in loadBl, loadBl's profile_estimate is the same at any value (BDP=90 and 98 dumps agree), so attempt 28's formula `116 = 0.2576 x (257 + CFok) + CGok` and attempt 29's "both early returns must go" stand to the digit.  Nothing new to cut: every term is fixed by the nonequal, early-return and call heuristics (attempt 28), and the threshold side needs entry > 990 (fewer predicted iterations), which the loop's fixed exits don't allow.

### The `ja`: which branch it is, and why (bbro RTL, vrp1)

- It is the SE copy of the tail's `xb.type <= BUILD_DEVGL16` test X (final bb 112, old 119), after `call checkBl; test eax,eax; mov edi,eax; jne`.  Neither successor follows it in the layout, so fixup_reorder_chain adds a jmp and points the jcc at the edge with probability >= 50% (it inverts when REG_BR_PROB < 5000).  So the sense isn't a layout choice at all, it's P(<=5) on that copy: src has `leu` 9862 (the hot label plus exp_pr), the near miss `gtu` 7678, i.e. P(<=5) = 23.2%.
- vrp1 (nm.vrp1 bb 24): X has freq Xc = 211 from five edges (117: 76, 20: 33 the signature-failed path with r = -1, 118: 58, 22: 24, 23: 20), p = 50% (no predictor), and T (`if (*pr != 0)`, bb 25) q = 61% (the break's early return).  Attempt 18's formula for the r = 0 copy, Xc p (1 - q) / (Xc - S) = 211 x 0.5 x 0.39 / 178 = 23.1%, matches the 23.2%.  For `jbe` it needs p (1 - q) >= 0.5 x 178 / 211 = 0.422: with p = 50% that is q <= 15.6%, with PRED_CALL-strength p (71%) q <= 40.6%.  The natural spellings of T give q = 61% (`!= 0`), 37.8% (`== (uint32_t)-1`), 36.6% (`(int)*pr < 0`), and X has no natural predictor (attempt 21's list), so no natural pair reaches 0.422.
- vrp1 registers only the T-side joiner thread for X's incoming edges (`(e, 24) incoming; (24, 25) joiner; (25, 120) nocopy`), because type isn't known at X yet (the SE copy only becomes the type-14 copy by later threads), so the other successor's count can't set the copy's probability either.

### gen_bd550 (10 cases, the tail's forms on the near miss, no param; loadBlFiles loose/strict)

- `*pr == (uint32_t)-1`, the `<= 5` arm as `if .. else if (type == 14)`, `if (!*pr) break; goto fail;`, nested else: all **4/59**, the same two effects (as the formula says: q moves to 37.8% at best).  `(int)*pr < 0` 4/60.
- Kit first (`if (xb.type > BUILD_DEVGL16) { .. break; } if (*pr) goto fail;` and its else-if spelling): 44/167 but with no displacement in the other functions: the size log's -1 block moves before the SMC arm, the sig-failed setFlashBuild copy reads through the IV (attempt 21's PHI-order reading), and the dup and `ja` stay.
- The tail as two `&&` tests: 60/189 and 132/252.

### Don't retry (attempt 43)

- The SE copy's `ja` by the tail's spelling on the near miss (gen_bd550): it is P(<=5) on the copy, fixed by p = 50% and q >= 36.6%; nothing natural gets p (1 - q) to 0.422.
- Block 116 by anything already in attempts 27 to 29: the no-param base has the same 72 + 27.

### What to try next

- Nothing on this near miss: both effects need a probability that no gcc 6 heuristic gives these blocks (the dup: 11 off block 116; the `ja`: p (1 - q) >= 0.422 on X).  If a natural form ever gives X a predictor towards `<= 5` (a call or an early return on the `> 5` side), re-check the near miss first: with p >= 69% the `== (uint32_t)-1` spelling of T would give `jbe` by the formula.
- Otherwise attempt 40's list stands.

### Costs now (strict/loose, removed alone; 11 tricks, unchanged)

As attempt 42: lab_t5le 7/0, exp_pr 18/2, exp_t10 116/46, vol_fail 296/126, lab_none 333/231, etype 168/94 in the object, cp 118/66 in the object, exp_devgl 43/7, pin_size 82/40.  Near miss (wt, exp_t10 + exp_pr + lab_t5le off, no param): 4/59 in loadBlFiles, 44/99 in the object.

## Attempt 44

Goal: the brief's predictor audit.  Every probability gap left is a static-predictor question, so: which gcc 6 predictors fire on each critical test, which would be needed to reach the measured window, which natural source constructs trigger those predictors in gcc 6.2, and which of those the notes haven't tried.  src as of 919f620b, unchanged.  New tool `tools/wip/dehint/bdpred.py fn.profile_estimate` (each conditional bb's GIMPLE test with its "Predictions for bb" lines; feed it a `bddump.sh .. fn t-profile_estimate` dump).  New probe `tools/wip/dehint/drafts/build_pred_probe.c` (one tiny function per predictor kind, compiled with the pinned gcc and `-fdump-tree-profile_estimate-details`).  Scratch in build/bd/a44 (not kept: `off.c` is src with exp_t10, exp_pr, lab_t5le, lab_none and exp_devgl off, and `off.<fn>.pe` its dumps at BDP=90).

### Which predictors gcc 6.2 has (build_pred_probe.c, read from its profile_estimate dump)

| Construct | What gcc 6.2 does with it |
|---|---|
| call with side effects in a dominated, non-post-dominating dest block | call 29% against that edge (PRED_CALL, hitrate 71); the whole block is scanned, so a statement before the call doesn't help |
| indirect call (function pointer) | the same call 29% (gcc 6 has no PRED_INDIR_CALL) |
| pure / const call (strlen) | nothing |
| `goto` | nothing (no PRED_GOTO from the C front end) |
| `continue` | continue 50% (no effect on the edge; it only stops PRED_LOOP_EXIT on that block) |
| `exit()` / `abort()` (noreturn from stdlib.h) | noreturn 0%, first match (every other predictor on the edge ignored) |
| `return <negative constant>` (int) | negative return 4% |
| `return NULL` (pointer function) | null return 10% |
| `return <constant other than 0, 1>` | const return 67% |
| `return 0` / `return 1` | nothing |
| `x > 0`, `x <= 0`, `x < 0`, compares with 1 or -1 | opcode positive 73% / 27% |
| `x == c` (c non-zero, or two non-constants) | opcode nonequal 28% (`!=` 72%) |
| `x == 0`, `x != 0`, `x < y` (two non-constants) | nothing |
| `ptr != NULL` / `ptr == NULL` | pointer 85% / 15% |
| `d == 1.5` | nothing (no FP opcode prediction for an equality) |
| edge to the return block (not its next_bb), or into a block whose single successor is the return block | early return 39% against it |
| loop exit / latch / IV compare against a constant | loop exit 9% / n_exits, loop iterations, guess loop iv compare |
| loop guard (`if (n > x) for (i < n)`) | nothing (no PRED_LOOP_GUARD in gcc 6) |
| cold attribute | nothing in the toolchain's own headers uses it (only libiberty's ansidecl.h, which the app doesn't include); noreturn comes only from exit, _exit, _Exit, abort, longjmp |

### The critical tests (`bdpred.py build/bd/a44/off.<fn>.pe`; probabilities are of the GIMPLE true edge)

| Trick | Function, test (bb at profile_estimate) | Predictors that fire | Combined | Needed (window from the notes) | Predictor that would close it | Natural constructs that trigger it, and what happened |
|---|---|---|---|---|---|---|
| exp_t10 | loadBl, `type == 10` (bb 6) | nonequal 28, call 29 (suGetCG block), early return 61 (on the else break, i.e. towards the test) | 19.9% | <= 6% on src (attempt 25); on the wt near miss p10 x s10 <= 7.0% (p10 <= 11.5% at s10 = 61%) | a second NOT_TAKEN predictor of <= 34% on the true edge (DS), or the else break losing early return | call: one per edge, already used.  early return: the CG arm reaches chk, so it can't be a return; taking it off the else break needs a non-empty block before the return that isn't fail (attempt 29: only an asm block does it).  noreturn/cold: only on a dead path.  opcode: one per test.  pointer: type is an int.  All tried or impossible (attempts 25, 27 to 29) |
| exp_t10 | loadBl, CG success `suGetCG(..) == 0` (bb 7) | early return 39 (on the failure break) | success 61% | success <= 35% | NOT_TAKEN on the success edge | call in the success dest: the dest is chk, a join, so only CG's own checkBl call gives it (attempts 16, 27, 28: crossjumps with case 6, 83 loose); `!= 1` would get nonequal 72 towards failure (80% failure) but is `cmp eax,1` where the reference has `test eax,eax` (suGetCG returns uint32_t 0/1 from another object, so no VRP range); return predictors: loadBl returns nothing |
| exp_t10 | loadBl, load result `*pr != 0` (bb 3) | none | 50% | failed >= 65.5% (116 = 132.2 - 67.5 f <= 88) | TAKEN towards failed | call in the load-ok dest: that dest is the SE test, which the CF path also enters, so it isn't dominated; early return on the ok edge: no; loadInputFile's result is an int compared with 0.  Untriggerable (attempt 28) |
| exp_t10 | loadBl, SE test `type == 9`, `d[0] == 'S'`, `d[1] == 'E'` (bb 8 to 10) | nonequal 28 each | 28% each | P(non-SE) <= 75.5% | anything raising the SE side | 0-compare spellings fold back (attempt 42); `&` / helper / word compare change the code (attempt 28) |
| etype | loadBl, verify `cbVerifySig(..) == 0` (bb 16) | call 29 (failed log only, because `else if (type)` keeps the passed log out of the dominated block) | 29% | 29% with no dead test | PRED_CALL on the failed edge only | the passed log in a block that isn't dominated (a second predecessor) or holds no side-effect call: nothing natural; a zero test gets no opcode predictor, `== 1` / `!= 1` point the wrong way (nonequal says the `==` side is unlikely) and change the compare; `<= 0` gets positive 27 but is `jle` for `je`.  Tried: flags, re-tests, joins, returns (attempts 6, 8, 18, 30, 32, 33, 38) |
| lab_t5le | loadBl, tail `xb.type <= BUILD_DEVGL16` (bb 21) | none | 50% | >= 53% on src (q = 2%); p (1 - q) >= 0.422 on the near miss | TAKEN towards `<= 5` of any strength | call in the `> 5` arm's first block: that block is the `type == 14` test and setFlashBuild depends on it; early return on the `> 5` edge: same block; opcode positive needs 0 / 1 / -1 (`< 6`, `- 6 < 0` fold to `<= 5`); no loop.  Untriggerable (attempts 11, 18, 21, 43) |
| exp_pr | loadBl, tail `*pr != 0` (bb 22) | early return 61 (on the break) | fail 61% | fail <= 4.4% on src, <= 15.6% on the near miss | NOT_TAKEN on the fail edge, at negative-return strength | negative return (4%): loadBl returning int -1 also lands on the size and smc -1 sources (attempt 27); opcode positive `(int)*pr < 0` 36.6%, nonequal `*pr == -1` 37.8% (gen_bd263, gen_bd550); call: fail holds no call; noreturn: dead.  Nothing reaches 15.6% |
| exp_devgl | buildFlash, dev `(xb.type - 4) <= 1` (bb 3) | opcode positive 27 | dev 27% | dev <= 24.9% | a second predictor <= 47% on the dev edge | call in the dev arm (the reference has cmovbe, no arm); every other kind checked in attempt 16 (no return, loop, pointer; `== 4 || == 5` folds to the range) |
| lab_none | loadConsoleBlFiles, case 24 `xb.glitch2mfg == 0` (bb 17) | call 71 (loadBaseFile block) | load side 29% | load side >= 44.5% (two calls) or >= 34% (`||`), attempt 25 | TAKEN towards the load side >= 66% (or >= 56% with `||`) | early return on the break edge would give DS(29, 61) = 39%, enough for the `||` form, but the break goes to the `if (r)` test (the loop goes on); opcode positive `glitch2mfg <= 0` / `> 0` would give 52.5% but is `jle` / `jg` for `je` and nobody writes it for a flag; pointer: glitch2mfg is an int.  Tried: case 24's forms (attempts 22, 41, 42) |
| lab_none | defaultBl60, `e->data != NULL` (isra clone, bb 2) | pointer 85, early return 61 (the NULL edge goes straight to the return block) | NULL 10.1% | r = 1 block >= 21 (14 now): NULL >= 15.2% at the sites' 136 | the NULL edge without early return | the NULL edge must pass a non-empty block before the return, i.e. a statement on the failure path; the result-variable form (`int r = 1; if (e->data) {..; r = 0;} return r;`) still sends the NULL edge to the return block with `r = 1` as a PHI argument: the dump shows the same pointer 85 + early return 61 = 10.1% (re-read this attempt on gen_bd443's `rvar plain`: loadConsoleBlFiles' bbro is identical, block 53 at 14) |
| lab_none | loadConsoleBlFiles, loop test `i < nFiles` (bb 55) | loop exit 95.5 (9% / 2 exits) | 95.5% | not-entered return < 14 (20 now) | a third exit, or a loop predictor | a third exit moves the `if (r)` exit too (attempts 25, 32); no loop guard predictor in gcc 6; PRED_CONTINUE stops loop exit on its block (attempt 41: 169 loose) |
| pin_size | calcBlAreaSize | (an IRA copy-order tie, attempt 35, not a frequency) | | | | |
| vol_fail, cp | loadBl | (block survival and an entry's weight, attempts 26 and 27; no predictor closes them) | | | | |

### Readings

- Every gap is one of three kinds: the predictor that would close it points the other way in gcc 6 (nonequal for the verify and CG tests, early return on the tail's T and on CG's failure), it needs a call or a return where the reference has none (exp_devgl's dev arm, the tail's `> 5` arm, the load-ok edge), or it needs a value range gcc 6 doesn't have across objects (`!= 1` for suGetCG, `<= 0` for glitch2mfg: either would be the reference's code only if VRP knew the value is 0 or 1).
- The probe rules out the kinds the brief listed beyond the notes: indirect calls give the same 29% as direct ones, `goto` and loop guards give nothing, the toolchain's headers mark nothing cold, and a noreturn call only fits a dead path (a trick), since none of these functions exits.  The return predictors (negative 4, null 10, const 67) need loadBl, buildFlash or defaultBl60 to return a value they don't return: loadBl's int -1 was attempt 27 (it flips the other -1 sources); buildFlash returns r, 1 and 0 at its exits, none near the dev test; defaultBl60 returns 0 and 1 (no prediction), and returning anything else changes the could-not-read log's `%i`.
- So nothing new was built beyond the probe and the defaultBl60 re-read: every natural construct that triggers a predictor in the needed direction is already in the notes with its cost, or changes the reference's instructions.

### Don't retry (attempt 44)

- Indirect calls, gotos, loop guards, `continue` or cold attributes as predictors at any of these sites: gcc 6.2 has none of them (build_pred_probe.c).
- defaultBl60's result-variable form for lab_none: its NULL edge still goes straight to the return block (10.1%).
- Opcode spellings against 1 or 0 for suGetCG, cbVerifySig or glitch2mfg (`!= 1`, `<= 0`, `> 0`): they change the jcc, and the `==` side always comes out unlikely.

### What to try next

- Nothing on the predictor side.  The windows are exact and every gcc 6 predictor has now been checked against each test in the table above; a new attempt should start from a new reading of the original's structure (a different CFG), not from a predictor.
- Otherwise attempt 40's list stands.

### Costs now (strict/loose, removed alone; 11 tricks, unchanged)

As attempt 43 (src unchanged): lab_t5le 7/0, exp_pr 18/2, exp_t10 116/46, vol_fail 296/126, lab_none 333/231 (8/4 with the precheck gone too, with any defaultBl60 body), etype 168/94 in the object, cp 118/66 in the object, exp_devgl 43/7, pin_size 82/40.

## Attempt 45

Goal: the whole-structure hypothesis again, with what attempts 10 to 44 learned: loadBlFiles written like loadConsoleBlFiles (switch in the loop, `r` a loop-body local, one `r = -1` site, r tested once after the switch), built from src's current arms rather than attempt 9's text, scored hint-free and with each hint back, and with the param swept.  src as of e7466e21, unchanged.  New tools in `tools/wip/dehint/bdgen`: `a45lib.py` (`loop(text, fb=, fail=, tail=, c6=, rdecl=, none=, sz=, helper=, off=(..), c24=..)` takes loadBl's switch out of src, `*pr` -> `r`, and writes it into loadBlFiles' loop, or back into a helper; CLI `python tools/wip/dehint/bdgen/a45lib.py out.c fb=con2 sz=and3 off=etype+cp+lab_t5le`), `a45psweep.py` (variants x param values: `python tools/wip/dehint/bdgen/a45psweep.py -p 98,99 'lab:fb=con2,off=etype+cp'`), generators gen_bd560 to gen_bd562, hand-run scripts `a45_c24.py`, `a45_c24b.py`, `a45_dbl.py`, `a45_cf.py`, `a45_bl60.py`, `a45_diag.py` (each reads build/bd/a45/n1.c, written by the CLI line above; run from the repo root).  Scratch in build/bd/a45 (not kept).  Loose/strict lines in loadBlFiles; "+displ" means loadBlFiles changed size and loadConsoleBlFiles / blmodMissing / buildFlash pick up 40 lines of call offsets (not real differences).

### The loop form at the param's 98 (gen_bd560, 342 cases)

Axes: fallback (src's nested with `goto chk`, attempt 25's and9, `con2` = loadConsoleBlFiles' form: `if (r) { if (type == 9) { if (suGetCF(..)) r = 0; } else if (type == 10) { if (suGetCG(..)) r = 0; } } if (r) break;`), the -1 site (`c2`: `fail: r = -1; break;` closing case 2, as attempt 26; `c23`: closing case 23 after the size log; `each`: `r = -1` at every site, as console), tail (src's, `if (xb.type <= 5) break;`, `xb.type > 5 && type == 14`), case 6 first, and the hint set (all on, all off, each off alone).  The loop form has no helper to keep inlined; defaultBl60 and the other callees inline as in the reference (no 9999 rows).
- Best: `con2 c2 src` with only `else if (type)` off, **108 loose** (no displacement); with every hint on it is 158 (+displ): in the loop form the dead test costs 50 lines instead of saving them.  All off: `con2 c2 src` 107 (+displ), src's fallback 155 (+displ).  c2 and c23 score the same everywhere (the label moves, the code doesn't); `each` is 185 and up.
- Attempt 9's loop form was 128 hint-free; the gain is case 23's and case 27's current spellings.

### The param on the loop form (a45psweep.py)

- `con2` with etype off: p88 / 92 / 99 **26 loose**, p90 to 98 108, p78 20 (+displ; buildFlash's devgl needs p >= 75).  The param acts here only through exp_t10 and exp_pr: at 99 the CG edge is 1% instead of 2%.
- With etype and the constant_p entry off (`cp`: the entry as `if (0)`): **p99 18 loose / 60 strict**, no .rdata or other function moved.  Two blocks: the appendAddonPatches call (laid out last) and case 24's r = 1 block.
- Case 23 as `e->size & 3` (console's spelling; src's `(e->size & ~3) != e->size` is attempt 15's borderline): **p99 14 / 34**, appendAddonPatches back in place, and lab_t5le is then free (14 / 34 with it off).  This is the near miss **n1**: `fb=con2 sz=and3 off=etype+cp+lab_t5le` at p99, drafts/build_loadBlFiles_loop_nearmiss.patch (plus 98 -> 99 for build.c in build.sh).  It would remove 4 tricks (etype, both constant_p, lab_t5le) and the case-23 borderline; exp_t10, exp_pr, the barrier and the param stay (exp_pr off +2 loose, the barrier off +1, both +5, exp_t10 off 98 +displ).
- Every other function matches at p99 on n1 (attempt 24's "the object matches at 96, 98, 99 only" holds).

### What n1's 14 lines are (bbro, `bdblocks.py`, `-fdump-rtl-rtl_dce-blocks`)

- One block: case 24's r = 1 block after the first arm's malloc fails (`mov eax,xb.type; sub 4; cmp 1; jbe <arm 2>; mov edi,1; jmp <log>`, freq 32).  The reference has it right before the suGetCF block (freq 41); n1 lays it after that block and after appendAddonPatches.  Both are round-4 heap items with no priority, so 41 goes first.
- In src the same block (51, freq 31) gets priority (`key -1001931`, edge 19) because its predecessor, the arm-1 malloc block (47, freq 191), ends its trace in round 2: the malloc-ok edge is 191 x 0.899 = 171.6, under round 2's exec_th = 882 x 200 / 1000 = 176.4, so the memcpy block starts a trace of its own.  In n1 the malloc block is 221 (the two crossjumped defaultBl60 copies, 98 + 123), the edge 198.6, and the trace runs on through memcpy into arm 2's test, so the r = 1 block never gets priority.
- 221 / 597 = 191 / 513: the whole case-24 arm is scaled by the arm's frequency.  The switch's 12 edges each get 1/12 of the switch block, 7162 in the loop against 6160 in src: in src the none test's strnicmp edge gets PRED_CALL (29%) because the guarded block is the loadBl call; in the loop the guarded block is the switch (no call, 50%).  This is attempt 9's reading, now down to a single block: every other block of loadBlFiles lines up at the loop's 597 scale with four fewer hints.
- So the reference's arms were at about 513, which says the guarded block held a call at profile_estimate (src's helper), while the loop's arms match the reference's code with fewer hints.  Neither structure is the whole story yet.

### Sweeps on n1 (p99 unless said)

- gen_bd561 (288 cases): fail site, tail, case 6 first, `r` declared at the top or in the body, case 24's `||` forms (`or1` first arm, `or2` second, `orb` both), exp_pr / vol_fail off.  Best 14 (`or2` is an equal base: the second arm's `||` costs nothing here); `or1` moves the size store as src's borderline comment says (16 +displ, 206 strict); `plain` / `and` tails 48 and up.
- gen_bd562 (135 cases): the fallback's forms (`con2`, console's own `con` with the SE test after `if (r) break;`, `con2n` with `!= 0`, flat `&&` pairs, `else`-joined pairs, nested `&&`, an inner switch, `brk` = failures break and a good fallback falls to `r = 0`) x c2/each x tail x exp_t10 / exp_pr / vol_fail.  `con`, `con2`, `con2n` are equal (14); `brk` 34; the rest 96 and up.
- a45_c24.py / a45_c24b.py: arm 2 with `else r = 0` instead of the leading `r = 0;` (18 +displ); arm 2 as `if (!loadBaseFile(..) && e->size == 0x60) r = 0; else r = defaultBl60(e);` (**equal**, 14); arm 1 nested `if (!loadBaseFile(..)) { if (size != 0x60) .. } else ..` (equal); `glitch2mfg != 0`, `r = 0;` before arm 1, `DEVGL16 || DEVGL`, `>= DEVGL && <= DEVGL16`, `!(type != JTAG && !glitch2mfg)` (all equal, 14); `glitch2mfg || type == JTAG` 122 (+displ).
- a45_dbl.py: defaultBl60 as a result variable, `if (e->data) {..; return 0;} return 1;`, a local pointer, the assignment in the test, `== NULL`: all 14 (the same GIMPLE, attempt 44).
- a45_cf.py: CG tested first 141 (+displ), `suGetCF(..) == 1` 100, `if (r != 0)` equal, `r && type == 9` pairs 103.
- a45_bl60.py: a `loadBl60(e)` helper for case 24's arms (five bodies, with and without console's case 24 using it too): 39 at best (`||` bodies), 100 for the two-call bodies.
- a45_diag.py (diagnostic only): a 1% `__builtin_expect` on arm 1's size, glitch or load test is far too strong to measure the window (14 to 258); not pursued.
- Guard forms (a45psweep): the r test inside the guard (`rin`) or the none test as a `continue` (`cont`, with r at the top or in the body): 201 at p99.  A diagnostic expect on both none-test edges (p71, i.e. 29%) is 208 and up: an expect is not PRED_CALL (it is first-match and moves the crc edge too).
- The arms back in a helper (a45lib `helper=`): src's `*pr` helper with n1's arms 202 (116 with src's case 23 and every hint); r a local in the helper with `*pr = r;` at the end, returned (`uint32_t loadBl(e, i)`), the could-not-read log inside the helper, or `if (r) *pr = r;`: 95 (log inside, src's arms) to 418.  The helper's breaks are early returns at its own profile_estimate, which the loop form doesn't have, and n1's arms only line up without them.

### Don't retry (attempt 45)

- The loop form at the param's 98, or with `else if (type)` kept: the dead test costs 50 lines there.
- n1's last block by case 24's spellings, the fallback's spellings, defaultBl60's bodies, a loadBl60 helper, or the guard's forms (above): the block needs the arm-1 malloc block under 196 (exec_th 176.4 / 0.899), or the r = 1 block over 41, or suGetCF's block under 32; every natural form keeps 221 / 32 / 41.
- n1's arms in a helper of any kind (`*pr`, a stored or returned local, the log inside, a conditional store).
- `each` (`r = -1` per site) and the `plain` / `and` tails in the loop form.

### What to try next

- n1 is the closest base found for loadBl's cluster: one block, and it would take etype, both constant_p and lab_t5le (4 tricks) plus the case-23 borderline.  What's missing is a factor of about 0.86 on case 24's arm (597 -> 513), or a natural reason for the arm-1 malloc block to end its trace.  Not tried: a case 24 with one shared defaultBl60 call per arm that still gives the reference's two copies; anything that gives the switch more than 12 edges at profile_estimate and merges them before bbro (tail merge runs in PRE, after profile_estimate), though every case value is already accounted for.
- Check any idea against `bdblocks.py` on the bbro dump first: the r = 1 block must be laid out right before the suGetCF block, and in round 2 the arm-1 malloc block's trace must stop there.
- One hint in place of the four (a45_hint1.py, p99): a cold label on the CF fallback 96 (+displ), on arm 1 or on an `if (r)` after it 80 to 466, a hot label there 127, a 1% expect on arm 1's size test 39.  None closes the block, so n1 isn't even a 4-for-1 trade yet.

### Costs now (strict/loose, removed alone; 11 tricks, unchanged)

As attempt 44 (src unchanged): lab_t5le 7/0, exp_pr 18/2, exp_t10 116/46, vol_fail 296/126, lab_none 333/231, etype 168/94 in the object, cp 118/66 in the object, exp_devgl 43/7, pin_size 82/40.  New: the loop form n1 (fb=con2, sz=and3, etype + cp + lab_t5le off, p99) 34/14 in loadBlFiles, nothing else differing; on n1 exp_pr off 38/16, vol_fail off 41/15, both 51/19, exp_t10 off 215/98 (+displ).

## Attempt 46

Goal: attempt 45's n1 (drafts/build_loadBlFiles_loop_nearmiss.patch: 14 loose / 34 strict in loadBlFiles, case 24's r = 1 block laid out after the suGetCF block): natural ways to give its case-24 arms the reference's frequency, then trades (n1 plus one hint, n1 minus each remaining hint).  src as of d1bcd1e6.  New tools in `tools/wip/dehint/bdgen`: `a46run.py <script.py> [-p ..] [-k label]` (scores `V = {label: [(old, new)..] or fn}` on build/bd/a46/n1.c, written by a45lib's CLI on d1bcd1e6's src, see its docstring), and the scripts `a46_loop.py`, `a46_exit.py`, `a46_a1exp.py`, `a46_a1flag.py`, `a46_hint1.py` (on n1), `a46_m1hints.py`, `a46_devgl.py` (on src after this attempt).  Scratch in build/bd/a46 (not kept: `dump.sh file.c outdir [p]` writes profile_estimate and bbro dumps, `split.py dir [fn]` cuts one function out of them for bdpred.py / bdblocks.py).  Loose/strict lines in loadBlFiles unless said.

### n1's window, read off the dumps (bdpred.py, bdblocks.py)

- The none test is bb 3 / bb 4, 50% each (no predictor); in src the strnicmp edge got PRED_CALL (29%) because its destination was the loadBl call block.  gcc 6's call heuristic only looks at the edge's immediate destination block, which in the loop form is the switch block (no call), and the crc edge's destination isn't dominated by it, so no ordering of the two tests gives it (`crcfirst`: 318).
- Case 24 at 597: arm 1's tests are JTAG `p1371` (nonequal 28% with call 29%, combined 13.7%: its true edge's destination is arm 1's loadBaseFile block, which it dominates) then glitch2mfg 50% (same destination, not dominated, so no call heuristic).  P(arm 1) = 0.137 + 0.863 x 0.5 = 0.568, 339; the two defaultBl60 copies 98 + 123 = 221.  For the malloc block to stop round 2's trace it needs P(arm 1) about 0.49 (src's 0.568 x 0.86), which is what nonequal alone on the JTAG test and the call heuristic on the glitch test give (0.28 + 0.72 x 0.29 = 0.489), i.e. the glitch test first (`gfirst`, 122: right frequency, wrong test order).
- So the reference's case 24 is consistent with src's helper scaled by the none test's PRED_CALL, not with any shape of arm 1 in the loop.

### Sweeps on n1 (p99, and p95 where said)

- a46_loop.py: `while` loop, `switch (type = e->type)`, `if (r != 0)`, `!= 0` on the none tests, the none test as `if (!a && !b) ; else {..}`: all equal (14).  Pointer IV 388, crc first 278, `int r` 117 (+displ each).
- a46_exit.py: the could-not-read exit moved after the loop (`if (r) break;` + log after, 54; log inside then break and `return r ? -1 : 0` or `if (r) return -1`, 54), `i = xb.nFiles` in place of the return (639), r in the loop condition (627).  The `return -1` inside the loop is the reference's shape.
- a46_a1exp.py / a46_a1flag.py, arm 1's probability: an expect on the glitch test (68 at p95, 258 at p99) or on the whole arm (258), `glitch2mfg == 1` (121), the two arms' bodies duplicated as `if (JTAG) .. else if (glitch) ..` (163), a flag (`g = glitch; if (JTAG) g = 1; if (g)`, 144; `g = JTAG || glitch`, 94).  The arm's window is narrow: too low breaks the rest of case 24's layout.
- The param on n1 (a45psweep, 50 to 99): only 95 and 99 give 14; nothing lower.
- **a46_hint1.py**: one hint at every `if` in defaultBl60 and loadBlFiles (`__builtin_expect(c, 0)`, `(c, 1)`, hot and cold labels at each braced then-block), at p95 and p99: **one IDENTICAL**, a hot label at the head of case 24's second arm (`if (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16) { devgl: __attribute__((hot)); ...`), at both values.  Next best 14 (88 variants, i.e. no effect); nothing else under 14.

### What the hot label does (dumps of the landed source, build/bd/a46/dm2)

- The arm-2 test is `opcode values positive 27%` (the folded `(type - 4) <= 1`) with call 29%: 13.1%; with the label (hot label 85%) DS gives 46.1%.  Arm 2 goes from 78 to 275, and round 2's trace from arm 1's malloc block (`45 48 49`) runs on into arm 2 (`45 48 49 41 51`).  Round 4's traces are unchanged (the r = 1 block 46 is still its own trace, after suGetCF's 10); it's connect_traces that now takes `46 108` before `10 15`, so the r = 1 block lands before the suGetCF block as in the reference.  That's a different route from attempt 45's (round 2's malloc trace ending); no natural form of arm 2 was found that raises its probability (below).

### Landed

src/build.c: loadBl and its helper call replaced by n1's loop (re-indented as loadConsoleBlFiles, `chk:` and the dead `if (0)` entry gone, the case-23 borderline comment gone with the spelling, the `fail:` comment moved over), plus the devgl hot label with a comment; build.sh's param 98 -> 99.  `sh build.sh` ends with 10dac648197fa5cdbb82d975ab9ff11f64075c9686908dfd9a33edc533f1971c.  bdhints.py's table now names exp_pr (`r != 0`), lab_devgl and vol_fail by the new text; bdlib's default flags (`P98`) are now the build's 99.  Tools that edit loadBl's text (a45lib, gen_bd* that use loadBl's lines) need d1bcd1e6's src.

### Trades and costs on the landed source (a46_m1hints.py, a46_devgl.py)

- Each remaining hint removed alone (p99; p95 the same): exp_pr 2/4 (the SE copy's `jbe` becomes `ja; jmp`, lab_t5le's old effect), vol_fail 1/7 (the -1 appended to the size log, attempt 9's reading), both 5/17, lab_devgl 14/34 (= n1), exp_devgl 7/43 (buildFlash), pin_size 40/82 (calcBlAreaSize), exp_t10 102/208 (+displ), lab_none 231/333 (loadConsoleBlFiles).
- The param: 95 and 99 match; 85, 88, 92 are 42 loose; 90, 96 to 98 60 and up; no `--param` 102.
- Natural forms for the devgl arm without the label (a46_devgl.py): `!(type != DEVGL && type != DEVGL16)`, `(uint32_t)(type - DEVGL) < 2`, `type > GLITCH && type < DEVKIT` all 14 (the same range test); an inner `switch (xb.type) { case DEVGL: case DEVGL16: .. }` gives the arm 50% at profile_estimate and is 14 loose / 204 strict (+displ): the switch expands to other code.

### Don't retry (attempt 46)

- The none test's 29% in the loop form by test order or spelling: gcc 6's call heuristic needs a call in the edge's immediate destination, which is the switch block.
- Arm 1's probability by expects, `== 1`, flags or duplicated bodies (above); the glitch test first has the right frequency but the wrong code order.
- The could-not-read exit anywhere but inside the loop, or the loop as a pointer IV.
- A single hint elsewhere on n1 (a46_hint1.py covers every `if`).

### What to try next

- lab_devgl: a natural reason for case 24's second arm to be likely (DS ~46% on its test), or for connect_traces to take the r = 1 block's trace before suGetCF's.  The window: the arm-2 test's edge must make round 2's trace from arm 1's malloc block continue through the DEVGL test into arm 2.  Gcc 6 predictors that raise an edge: pointer != NULL (85%), the call heuristic on the *other* edge (71%), opcode positive TAKEN (`x > 0`, `x >= 0`), none of which fits a build-type test.
- exp_pr (2 lines) and vol_fail (1 line) are the cheapest now; both were looked at before on src (attempts 9, 43); re-read them on the loop form, where the tail and `fail:` sit in the switch.
- exp_t10 is 102 here; with the cp entry gone it no longer has attempt 42's "nearly free" pairing.

### Costs now (strict/loose, removed alone; 8 tricks)

exp_pr 4/2, vol_fail 7/1, lab_devgl 34/14, exp_devgl 43/7, pin_size 82/40, exp_t10 208/102 (+displ), lab_none 333/231.

## Attempt 47

Goal: the two cheapest tricks on attempt 46's loop form (exp_pr 2/4, vol_fail 1/7), then lab_devgl with the 0.86 factor in mind.  src as of 5877c248, unchanged.  New scripts in `tools/wip/dehint/bdgen`, all run with `python tools/wip/dehint/bdgen/a46run.py <script> [-p ..] [-k label]` and reading src/build.c itself (BASE): `a47_pr.py` (the tail's r test and arm forms, each with and without the barrier; `V2` at its end has four more), `a47_fail.py` (the -1 site without the barrier), `a47_neg.py` (`(int)r < 0` with the signature block's and SE test's forms), `a47_rfirst.py` (r tested before `xb.type`), `a47_sigfail.py` (the `<= 5` exit inside the signature-failed arm), `a47_none.py` (the none test through a predicate helper).  Scratch in build/bd/a47 (not kept: `ref_lbf.txt` is the reference's loadBlFiles objdump, `cmp5.py dump.bbro` prints each `xb.type` vs 5 compare's REG_BR_PROB).  Loose/strict lines in loadBlFiles unless said; p99 unless said.

### Re-measured on src (a46_m1hints.py)

As attempt 46: exp_pr 2/4, vol_fail 1/7, both 5/17, exp_devgl 7/43, pin_size 40/82, exp_t10 102/208 (+displ).  lab_none with its `nFiles <= 1` precheck removed too is still 4/8 (loadConsoleBlFiles; the cold label alone is the 231/333 in the table).

### exp_pr: what the 2 lines are and what decides them

- The diff is the SE copy of the tail's `xb.type <= 5` test (reference 388a: `jbe 2f30; jmp 358e`); without the expect it is `ja 358e; jmp 2f30`: fixup_reorder_chain points the jcc at the edge with P >= 50%, so this is attempt 18's closed form again, P(<=5 on the copy) = Xc p (1 - q) / (Xc - S), with p = 50% (bb 26, `xb.type <= 5`, no predictor) and q the r test's probability.
- In the loop form the r test is bb 27 (`r_3` = PHI of checkBl's r on three edges and -1 from the signature-failed log); `r != 0` / `r` have no predictor (50%), so the copy's P(<=5) is under 50% and the jcc flips (`ja`).
- **`(int)r < 0`** gets opcode-positive (27%): the copy is 50.23% (`leu 5023`), so the `jbe` is right and loose is **0**; strict 7 is the `.p2align` of the no-key log copy (38a0) that follows the SE copy's jmp block: compute_alignments aligns it (freq 14, no fallthru) only if the previous block's freq is <= 1.4, and the jmp block is 4 x P(>5) = 2.  That needs P(<=5) >= 62.5% on the copy, i.e. (from K = 0.5023 / 0.73 = 0.688) q <= ~9%, or p raised.  attempt 11's t5le margin, now with exp_pr's spelling.  drafts/build_loadBlFiles_negtail_nearmiss.patch.
- No other predictor fits: `r == -1` (nonequal 28%) is 2/11, `r > 1` 2/4, `(int)r <= -1` and `(int)r < 0 && r != 0` 0/7.  p has no predictor (5 isn't 0/1/-1, neither successor holds a call), and the only way to give it one is a call on the >5 side (attempt 11: `setFlashBuild(0)` as a probe).
- On `(int)r < 0` (a47_neg.py, 24 cases): the signature block's arm order (`!xb.pub1bl` first: 10 / 23 and up; `cbVerifySig` true arm first: 16 and up), the `5 || 17 || 11` order (4 to 6), the SE test as `!memcmp(e->data, "SE", 2)` (166 and up, memcmp is a call): none moves the no-key log's or the SE copy's frequency the right way.  The param on it (60 to 99): only 95 and 99 give 0/7; 94, 96 to 98 are 60 loose.

### Tail forms (a47_pr.py, a47_rfirst.py, a47_sigfail.py)

- kit arm first (`if (xb.type > 5) { if (type == 14) ..; break; } if (r) goto fail;`): the same as src's (2/4 with `r`, 0/7 with `(int)r < 0`); `if (xb.type > 5 && type == 14) .. else if (r) goto fail;` 2/4 with any spelling.
- A plain `break` for `<= 5` (r is already -1 or 0): 25 loose (+displ); `xb.type > 5 && type == 14` alone 37 (+displ).
- r tested first (`if (r && xb.type <= 5) goto fail;`, nested, `else if`, `else if (type == 14)`): 16 to 42 (+displ), `(int)r < 0` first 34 / 192.
- The `<= 5` exit inside the signature-failed arm (`if (xb.type <= 5) goto fail; r = -1;`, or after it, or `else`), tail without an r test: 23 loose and up (+displ).

### The barrier on the loop form (a47_fail.py)

- Without the asm, `fail:` at the end of case 2 (src), at the end of case 23 after the size log, the size log's own `r = -1; break;` (with r = -1 before or after the log), the tail's own `r = -1;`, or `r = -1` at every site: **all 1/7**, the same line (the size log's `mov edi,-1` before its jmp, where the reference jumps to the shared -1 block).  Attempt 10's mechanism holds unchanged in the loop form: mergephi2 takes the `fail` forwarder (its predecessors bring different memory states, so it has a virtual PHI), the size log's edge isn't critical so its -1 lands in the log's block, and crossjump won't take a 1-insn tail from a block that isn't wholly matched.
- `if (!e->offset) goto fail;` with `fail:` after the default case, or `if (!e->offset) { fail: r = -1; }`: 59 / 238 (+displ).

### lab_devgl: a none-test predicate (a47_none.py)

- `isNone(e)` (`!strnicmp(..) && !e->crc`, or with an early return) or `isUsed(e)` in loadBlFiles alone or in both loops, with and without the label: **284 loose and up**.  Early inlining keeps it inlined, so the guarded block still has no call, and the predicate's boolean evaluation changes the none test's code itself.
- Reading the reference's jump table (.rdata 0xf50): entries 0 and 26 are the default case, so no extra case edge (13 or 14 switch edges, which would give 7162 / 14 = 512 per arm) is in the original.
- Read for arm 2's probability: an edge's predictors that could lift `(type - 4) <= 1` (opcode positive 27%, call 29%) to the label's 46% are a call in the skip edge's destination (DS of 71% and 27% is 47.5%), which in case 24 is the switch's join (not dominated), or a destination without a call (27% alone); every spelling of the devgl test folds to the same range test (attempt 46).  No natural form found.

### Don't retry (attempt 47)

- The tail's r test by spelling: the best is `(int)r < 0` at 0/7, which can't reach q <= 9%; `r == -1` and `r > 1` are worse.
- Tail arrangements on the loop form (kit first, `else if`, r first, the `<= 5` exit in the signature arm, plain `break`).
- `fail:` placement or -1 spellings without the barrier: all 1/7 (attempt 10's mechanism, unchanged by the loop form).
- The signature block's arm orders, the `5 || 17 || 11` order and a memcmp SE test as levers on the no-key log's alignment.
- A predicate helper for the none test.

### What to try next

- exp_pr: `(int)r < 0` (0/7) only lacks the no-key log copy's `.p2align`.  Any natural change that lowers the SE copy's frequency to 3 or less (jmp block 1), or raises the 5/17 no-key log copy above 20, without moving anything else, would land it; check with `bdblocks.py` (blocks old 17/118 and old 30 in the dump of the near miss).  Whether a cast in `(int)r < 0` reads as natural is for the user: r is uint32_t in src (declaring it `int` costs 117, attempt 46) though loadInputFile returns int; the -1 comes from the signature, size and SMC failures.
- The barrier and lab_devgl: no new lever; both need either a statement that survives to expand with no code, or a predictor gcc 6 doesn't have for these tests.

### Costs now (strict/loose, removed alone; 8 tricks, unchanged)

exp_pr 4/2 (`(int)r < 0` in its place 7/0), vol_fail 7/1, lab_devgl 34/14, exp_devgl 43/7, pin_size 82/40, exp_t10 208/102 (+displ), lab_none 333/231 (8/4 with the precheck gone too).

## Attempt 48

Goal: the three near misses jointly (exp_pr as `(int)r < 0` 0/7, vol_fail 1/7, lab_none with its precheck 4/8), every combination with the devgl label, exp_t10 and exp_devgl, and the param at 90 to 99; then the exact frequency arithmetic behind (a) and (c).  src as of 28c25d7f, unchanged.  New scripts in `tools/wip/dehint/bdgen`, all run with `python tools/wip/dehint/bdgen/a46run.py <script> [-p ..] [-k label]` on src/build.c: `a48_combo.py` (the matrix), `a48_exit.py` (the tail's r test as a loop exit), `a48_perturb.py` (equal-base edits around the SE path on `(int)r < 0`), `a48_edges.py` (13-edge switch diagnostic), `a48_none.py` (console case 24 guards without the precheck and label).  Scratch in build/bd/a48 (not kept: `track.py` follows blocks matching a pattern through every `-fdump-tree-all-details-blocks` dump; `dn/`, `dcb*/` the dumps; `n.s` / `m.s` the near miss and src with `-dA`).  Loose/strict lines in the named function; p99 unless said.

### The matrix (a48_combo.py, 27 rows x no param, p90 to p99)

- loadBlFiles rows: exp_pr {expect, `r != 0`, `(int)r < 0`} x barrier {on, off} x devgl label {on, off} x exp_t10 {on, off}.  Nothing beats the single removals.  With exp_t10 on, p95 and p99: expect 0, `r != 0` 2/4, `(int)r < 0` 0/7, barrier off 1/7, `r != 0` + barrier 5/17, `(int)r < 0` + barrier 3/20, and each label-off row is n1's 14/34 plus the rest; p92: 2/53, 4/57, 2/56; p93, 94, 96 to 98: 60 loose and up; p90, 91 and no param: 62 and up.  With exp_t10 off every row is flat in p (62 to 103 loose).
- So the items don't interact: (a) and (b) add, and (c) is in loadConsoleBlFiles, a separate function (each function's frequencies are normalised to its own loop header, so nothing there can reach loadBlFiles' blocks).  loadConsoleBlFiles without precheck and label is 4/8 at p93 to p99, 22/26 at p92 and below; lab_none's label alone 231/333; exp_devgl 7/43 at p93 to p99, 27/63 below.
- The matching params stay 95 and 99.

### (a) exactly: what the no-key copy's .p2align needs (the `(int)r < 0` near miss, `-dA` and profile_estimate / vrp1 dumps)

- compute_alignments: block 112 (the 5/17 copy of the no-key log, freq 14, no fallthru predecessor) is aligned only if its branch frequency (14) exceeds max / align-threshold (10000 / 100, never here) or if 14 > 10 x prev with prev <= entry / 2.  prev is block 111, the SE copy's `jmp` block: freq 2 = RDIV(block 110's 4 x P(>5) 49.8%).  The reference has 1 there (src's expect gives P(>5) 31.9%).  So it needs block 110 at 3 or less, or P(>5) under 37.5%, or block 112 at 21 or more.  Hot/cold isn't the limit (the entry is 882, so anything >= 1 is maybe-hot).
- Block 110's 4 comes straight from profile_estimate: the SE block (bb17 there) is **7** and keeps it through vrp1 (block 109 = 7, block 110 = RDIV(7 x 50%) = 4).  bb17 = bb14 (the `type == 9` test, 298) x 0.28^3 (`type == 9`, 'S', 'E', each nonequal) = 6.54; bb14 = 597 x 50% (bb13, the r test after the CF/CG fallback, no predictor); 597 = the switch block's 7162 / 12 edges; 7162 = 10000 (header) x 95.5% (PRED_LOOP_EXIT 9% / 2 exits) x 75% (the none test's two 50% tests).
- The window: with A = bb13's 597, the SE block = A x 0.010976 must be under 6.5 (A < 592, i.e. -0.8%), and the 5/17 no-key log = A x 0.5 x 0.5 x (0.5 + 0.5 x 0.28) x 15% = A x 0.024 must stay at 11 or more (A >= 458).  Every factor is a fixed heuristic: the header's 95.5% (3 exits would give 97%, the wrong way; 1 exit 91% would do, but the in-loop `return -1` is always an exit), the switch's 1/12 per edge (the reference's jump table has no 13th target), the none test's 0.75, bb13's 50% (a zero compare gets no opcode predictor; `(int)r < 0` would be 73% to continue, the wrong way), and the three 28%s.
- a48_edges.py (diagnostic only, not natural): a 13th switch edge (the default's log duplicated under `case 26:`) isn't merged back: 190 loose and up.
- a48_perturb.py (every subset of up to 3 of: `e->data + 2` in the tail, the SE test nested, the SE stores swapped, `type = 14; e->type = type;`, `xb.type < BUILD_DEVKIT`, the checkBl test as `(int)r < 0`, `e->type == 14` in the tail; 64 cases): the equal-base edits are all exactly 0/7 (same GIMPLE); the SE stores swapped 4/11, the checkBl test 153 loose and up, `e->type == 14` 160 and up.
- The other routes, from the joiner formula P(<=5) = Xc p (1 - q) / (Xc - S) = 149 x 0.5 x 0.73 / 108: S (signature failed, 41) would need 62, i.e. the verify at about 76% failed (the two arms' logs cancel PRED_CALL to 50%; one-sided gives at most 71%), and a higher Pk for S lowers the no-key log, which has to stay up.  The no-key log at 21 needs the pub1bl test block at 140 (has 95).  p has no predictor (a call on the >5 side would have to be in the test's immediate successor).

### (a) through a loop exit (a48_exit.py, 12 cases at p95 and p99)

- PRED_LOOP_EXIT is first-match, so an r test whose true edge leaves the loop gets 9% / n_exits (2 to 3%), well under the 9% q needs.  The tail jumping straight to the could-not-read log (`bad:` inside the `if (r) {..}` block; r is already -1 there), or a copy of the log and `return -1` in the tail, each spelling of the test, with and without the barrier: **234 loose and up** (+.rdata, displacement): the extra exit changes the loop's whole profile.  The log after the loop (`fail: r = -1; bad: log`) needs r out of the loop body (didn't compile as written); attempts 32 and 46 measured that family at 54 and up.

### (c) exactly (the no-precheck, no-label source; bbro and profile_estimate dumps)

- bb-reorder's round 4 holds the not-entered return (old bb 62, freq 20: entry 880 x 4.5%, halved by shrink-wrap's copy) and the r = 1 block (old bb 53, freq 14).  Neither's predecessor ends a trace (bb 53's is defaultBl60's malloc test inside round 3's trace `20 21 22`), so the heap takes them by frequency, the return first; the reference has r = 1 first (with the cold label the return is 0).
- r = 1 = (60 + 76, the two defaultBl60 call blocks) x 10.1% (pointer 15% DS early return 39%).  It would pass the return at 21 and up, which console's glitch2mfg guard at 50% would give (about 24): the guard is 71% to break because loadBaseFile's call block is its immediate, dominated successor (PRED_CALL).  loadBlFiles' glitch test escapes PRED_CALL only because the JTAG test also reaches that block.
- a48_none.py (console case 24 without precheck and label): nested `if (xb.glitch2mfg) {..}` 4/8 (same CFG), `||` 6/10, `glitch && (load || size)` 6/10, `!load && size == 0x60` then break 10/18, the guard repeated in both arms (`glitch && load` / `else if (glitch && size)`) 20/54 (the re-test stays in the code: `mov eax,ds:0x14; test; je` before the size compare, and registers move).

### Don't retry (attempt 48)

- Combinations of exp_pr / vol_fail / lab_none / lab_devgl / exp_t10 / exp_devgl at any param 90 to 99 or none (a48_combo.py): they don't interact.
- (a) by edits that leave the SE block at 7 at profile_estimate (all equal bases), by a loop-exit r test, or by switch edges.
- (c) by spellings of console's case 24 guard (a48_none.py) or of defaultBl60 (attempt 32).

### What to try next

- (a) has an exact target: the SE block at 6 or less at profile_estimate (bb13 under 592, -0.8%) with the 5/17 no-key log at 11 or more, or the SE copy's P(>5) under 37.5%.  A natural form that moves bb13 (the r test after the CF/CG fallback) slightly off 50%, adds one more nonequal-class test on the SE path only, or lowers the 5..21 arm's 1/12 share without a new jump-table target would land exp_pr as `(int)r < 0` (borderline cast).  None found.
- (c): a reason for the glitch2mfg guard's continue edge not to get PRED_CALL (a second predecessor into the loadBaseFile block, or a block between the guard and the call that leaves no code), or r = 1 at 21.
- (b): unchanged from attempt 47.

### Costs now (strict/loose, removed alone; 8 tricks, unchanged)

exp_pr 4/2 (`(int)r < 0` in its place 7/0), vol_fail 7/1, lab_devgl 34/14, exp_devgl 43/7, pin_size 82/40, exp_t10 208/102 (+displ), lab_none 333/231 (8/4 with the precheck gone too).

## Attempt 49

Goal: attempts 45/46's lesson (whole-function structure beats local spellings) applied to the functions holding the other tricks: loadConsoleBlFiles (lab_none), buildFlash (exp_devgl), calcBlAreaSize (pin_size), and code the two loaders could share.  src as of a1c62d7f.  New scripts in `tools/wip/dehint/bdgen`, all run with `python tools/wip/dehint/bdgen/a46run.py <script> [-p ..]` on src/build.c: `a49_con.py` (loadConsoleBlFiles restructures without the precheck and label; it also defines `strip`, `c24` and `SH` = loadBl24, which the others use), `a49_con2.py` (console's case 24 through a helper that holds the glitch guard), `a49_con3.py` (case 24 tested before the switch, diagnostic), `a49_share.py` (helpers both loaders call: loadXell `x1` without and `x2` with the retail test, a CF/CG fallback helper `cf`, loadBl24 `24`; `L_` rows keep console's precheck and label, `n_` rows drop them), `a49_shhints.py` (each hint off on those bases; `A49_STAGE=2` runs the second stage on the landed base), `a49_arm2.py` (forms of case 24's second arm on the landed source; written before src was landed, so it reads src/build.c as it is now).  Scratch in build/bd/a49 (not kept).  Loose/strict lines; p99 unless said.

### loadConsoleBlFiles restructured (a49_con.py, a49_con2.py, a49_con3.py; precheck and label off)

- Base 4/8 (attempt 48).  `r` in the loop body, a result variable with `break` (`ret = -1`), and case 24 moved before case 3 are all exactly 4/8 (same CFG).  Case 24 moved to the end or before case 2: 20.  The glitch2mfg load hoisted out of the loop into a local: 80.
- The switch in a per-entry helper returning r (`static`): 317 loose (inlined; its early returns change the profile).  Not static: 323 plus the out-of-line copy.
- Case 24 through a helper that holds the glitch guard (`if (!xb.glitch2mfg) return 0; ...`, four bodies): 201 (the guard's skip edge becomes an early return).
- Case 24 tested before the switch (nonequal 29% instead of 1/10 of the switch, which raises the r = 1 block past 21): 216 and 268.  The arm's frequency rises, but the code moves with it.
- Shared loadBl24 in console only, or in both loaders: console 4/27 (4 loose, as the base) plus displacement.

### Helpers both loaders share (a49_share.py, a49_shhints.py)

- loadXell (x1 or x2) with console's label kept: IDENTICAL; with loadBl24 as well: IDENTICAL (equal bases).  Without the label all of them are console's 4/8.  The CF/CG fallback as a helper returning 1 on failure is 350 loose and up, and it changes r's value, so behaviour too; dropped.
- Each hint off on those bases: x1 and x2 alone are as src (pr 2/4, dev 7/43, pin 40/82, lab 14/34, none 4/8; bar 1/7 on x1, 9/74 on x2; t10 102 on x1, 42 on x2).  **x2 + loadBl24 (x2_24) with exp_t10 off: IDENTICAL at p95 to p99**; x1 + loadBl24 with exp_t10 off is 60.  So it takes the retail test inside loadXell and the case-24 helper together.  Landed (below).
- On the landed base (stage 2, p0, p90, p95 to p99): pr 2/4, dev 7/43, pin 40/82, lab 14/57, none 4/8 (unchanged by the helpers), **bar 58/220** (the barrier is now much dearer than 1/7), pr + bar 62/224.  At p90 and with no param only loadBlFiles' 0/7 is left (exp_pr's 1% expect becomes too weak for the no-key log's alignment), and buildFlash's exp_devgl matches at p90 here too.  So the param stays at 99 (95 to 99 all match).
- Mechanism: not read this attempt.  The bytes are identical, so the inlining matches the reference.  The CG test's 2% was needed for the CG edge's place, and the inlined helpers' blocks reach profile_estimate in a different order or shape that apparently gives it naturally.  Worth a `bdpred.py` / `bdblocks.py` read next time, together with the vol_fail jump.

### Case 24's second arm on the landed source (a49_arm2.py, p95 and p99)

- `r = loadBl24(e);` with the label 25/73 (+displ), without it 39/87; without the leading `r = 0` 9/59; `else r = 0` at the end 4/19; `||` 14/34.  The written-out body with `r = 0;` stays (flagged).

### buildFlash, calcBlAreaSize

- Not swept.  The notes' mechanisms (sink's 75% rule needs a predictor gcc 6 lacks; pin_size's IRA copy tie) are about one block each, and every decomposition the brief suggested is already covered by gen_bd179, gen_bd192, gen_bd236, gen_bd264 and gen_bd442 (fuse) and by gen_bd105, gen_bd176, gen_bd195, gen_bd310 to gen_bd312 and gen_bd500 (pin_size).  A fuse helper that isn't early-inlined would keep the callee's early-return predictor, but it is a tiny leaf called once, so einline always takes it, and inlined bodies are re-predicted without their GIMPLE_PREDICT hints (attempt 17's isUpdateBl reading).

### Landed

src/build.c: `loadXell` and `loadBl24` added after defaultBl60.  loadBlFiles' case 25 is `r = loadXell(e);` and its case 24 first arm `if (xb.type == BUILD_JTAG || xb.glitch2mfg) r = loadBl24(e);`.  Console's case 25 is the same call and its case 24 `if (xb.glitch2mfg) r = loadBl24(e);`.  The `type == 10` expect is gone.  The case-24 borderline comment moved to loadBl24; the second arm's comment now names the written-out body.  bdhints.py drops exp_t10; README's build entry says 7 tricks.  `sh build.sh` ends with 10dac648197fa5cdbb82d975ab9ff11f64075c9686908dfd9a33edc533f1971c.

### Don't retry (attempt 49)

- loadConsoleBlFiles as a per-entry helper, with a result variable, with case 24 moved, with the glitch load hoisted, with case 24 ahead of the switch, or with a guard-holding case-24 helper (above): lab_none's window isn't reached by structure.
- Case 24's second arm through loadBl24, or without its `r = 0` (above).
- A CF/CG fallback helper (it changes r).

### What to try next

- vol_fail is now 58/220 instead of 1/7: read why (the helpers' inlined blocks move the -1 sites).  A different set of shared helpers might make it cheap again or free.  Try the other shareable pieces: case 23's size check (identical except for the retail test and `goto fail`), case 2's and cases 3/4's "from the dump" moves, a helper for the could-not-read log.
- lab_devgl and exp_pr on helper bases: the sweep only crossed x1, x2 and 24, and more helpers may move case 24's arm frequency (the 0.86 factor).

### Costs now (strict/loose, removed alone; 7 tricks)

exp_pr 4/2, vol_fail 220/58, lab_devgl 57/14, exp_devgl 43/7, pin_size 82/40, lab_none 351/225 (8/4 with the precheck gone too).

## Attempt 50

Goal: (1) why attempt 49's helpers freed exp_t10, read from the dumps; (2) more code the two loaders share, as helpers, each with the remaining hints off one at a time; (3) attempt 49's "What to try next".  src as of 26aca4bb, unchanged.  New scripts in `tools/wip/dehint/bdgen`, all run with `python tools/wip/dehint/bdgen/a46run.py <script> [-p ..] [-k label]` on src/build.c unless said: `a50_base.py` (src and each hint off), `a50_share.py` (helpers su / p23 / nand / slot, every subset; it also holds the text pieces the others import), `a50_nand.py` (useNandData at every subset of its sites, two store orders), `a50_su.py` (four CF/CG helper bodies, in one loader or both), `a50_sig.py` (the signature check as a helper), `a50_bl24.py` (eleven loadBl24 bodies), `a50_orc.py` (the `||` loadBl24 with loadBlFiles' arm 1 written out), `a50_arm2.py` (case 24's second arm through loadBl24, three forms), `a50_x1.py` (loadXell's retail test back in the callers, with the barrier and exp_t10), `a50_fail.py` (the could-not-read log as a helper), `a50_eq.py` (the equal bases together, param sweep), `a50_neg.py` (exp_pr's spellings again), `a50_cases.py` (cases 1 / 22 and 3 / 4 as shared helpers); standalone `a50_pebb.py <dump> [fn]` (bb frequencies of a profile_estimate dump) and `a50_bl24share.py` (loadBl24's own defaultBl60 call share per body).  Scratch in build/bd/a50 (not kept: `prev_t10.c` is 26aca4bb^'s src with exp_t10 off, `cur.c` src; `dump.sh` / `split.py` copied from a46; `d_*/` the dumps).  Loose/strict lines; p99 unless said.

### (1) Why loadXell and loadBl24 freed exp_t10

- **The helpers are not early-inlined.**  At profile_estimate both loaders hold calls to loadBl24 and loadXell (and to loadBaseFile and defaultBl60.isra.0, which attempt 18 already had as late-inlined); IPA inlines them later and scales each callee's own profile into the call block.  So attempt 49's "both are early-inlined" is wrong, and so is attempt 49's guess that inlined bodies drop their predictors: the callee's early-return and call predictions shape its blocks, scaled to the caller's call-block count.  This is also why loadBl24's body sets console's r = 1 block (below).
- The CF/CG arm's profile is **identical** before (26aca4bb^ with exp_t10 off) and after: the same predictions (bdpred.py on both dumps) and the same frequencies for every block of the 5..21 arm (597, 298, 41, 20, 257, ...; a50_pebb.py).  Only case 24 and 25 change (one call block each instead of loadBaseFile + two defaultBl60 calls, and the xell search's three calls).
- The 2 lines exp_t10 fixed are bbro's: in 26aca4bb^ without it, the shared `if (r)` block after checkBl (freq 95, `p5947`) is copied into the checkBl call block by connect_traces (`Duplicated bb 116`: the extra `test edi,edi; jne`), and case 2's nand-dump group moves.  The copy happens because round 1's trace `122 [571] 97 [398]` (case 27's d test and the extractSmcConfig call) runs on, so in connect_traces `97 116` takes the `if (r)` block first and `115 116` finds it connected; in src round 1 stops at the d block (`118 [571]` alone) and round 2's trace `93 [398] 112 [95]` holds the `if (r)` block mid-trace, so there is nothing to copy.  Why round 1 decides differently isn't settled: both have the same frequencies there, but bdblocks shows the d block's jump as p10000 in the old layout and p6983 in the new, so the CFG around it differs (the scaled-in helper bodies change which blocks are trace starts in round 1).  Next time: dump `-fdump-rtl-bbro-details` with `-dA` and read the d block's successors in both.

### (2) Sharing between the loaders (a50_share.py, a50_nand.py, a50_su.py, a50_sig.py, a50_fail.py, a50_eq.py)

| Helper | Where | Result (all hints on) | Notes |
|---|---|---|---|
| `useNandData(e, &xb.kv)` / `&xb.kvAlt` (free, take data and size, clear) | cases 3, 4 of both loaders, any subset | **IDENTICAL** | equal base: each hint costs what it costs on src (pr 2/4, bar 58/220, lab 14/57, none 4/8, dev 7/43), at p0, 90, 95, 99 |
| the same for `&xb.smc` | loadBlFiles case 2 | 0/2 | a jump displacement |
| the same for `&xb.smc` | console case 2 | 3/27 | console reloads `e->size` for smcSetLoad after the inlined stores |
| the same with the clears swapped (size first) | anywhere | 4 to 16 | the reference clears data first |
| `takeSlot(e)` (the same from xb.files[nFlashFiles]) | loadBlFiles cases 2, 3, 4 | 106 | |
| `loadUpdateBl(e, type)` (loadInputFile + the CF/CG fallback, four bodies) | both / loadBlFiles / console | 193 / 85 / 64 and up | late-inlined, so the arm becomes one call block at profile_estimate; every body the same |
| `loadPatchFile(e)` (case 23 with its log and -1) | both | 163 (loadBlFiles 28) | the patch-size -1 no longer reaches `fail:` |
| `checkBlSig(e)` (three bodies) | loadBlFiles | 95 and up | |
| `notRead(e, r)` (the could-not-read log; returning -1 or void) | both loops | **IDENTICAL** | equal base, every hint costs the same |
| `loadBuiltIn(e, fmt, data, size)` (a bin-dir file else the built-in copy; a50_cases.py) | loadBlFiles cases 1 and 22 | 22 loose | the hints off cost what they cost on src on top |
| `loadKv(e, name1, name2, &xb.kv)` (the keyvault chain; a50_cases.py) | loadBlFiles cases 3 and 4 | not inlined (an out-of-line loadKv, every function moves) | |

Combinations (16 subsets of su, p23, nand, slot) don't beat their parts.  On the two equal bases together the param sweep is unchanged: p0 and p90 leave only exp_pr's 0/7 alignment, p95 and p99 match.

### loadBl24's body and lab_none (a50_bl24.py, a50_bl24share.py, a50_orc.py)

- loadBl24's own profile is what IPA scales into console's case 24, so it sets the r = 1 block.  Its defaultBl60 call blocks get 70% of its entry in src's body (loadBaseFile failed 20.7%: call 29% with early return; size bad 62.2%), and every two-call body tried gets 65 to 70% (`r2`, `r3`, `r4`, `g0`, `n2`, `n3`, `ok1`/`r5`).  The one-call bodies (`||`, `!a && b` then the call, nested) get **85.9%** (the call block has two predecessors, so the size test gets no call heuristic).
- **With a one-call body the precheck and cold label are free**: loadConsoleBlFiles without them differs only in the size store's place (`mov [ebx+4],0x60` after the copy instead of before); the label makes no difference any more (`or_all` = `or_none`).  But that is attempt 4's borderline in reverse: the two calls are what crossjump merges to keep the size store before the copy (they replace a pin and an assume_aligned), and loadBlFiles moves case 27's config.bin block too (24/83).  With loadBlFiles' arm 1 written out again (a50_orc.py) loadBlFiles is 2/53: bbro's `if (r)` copy, i.e. exp_t10's effect back.
- So lab_none has a new, exact route: loadBl24's call blocks at about 86% of its entry with two calls kept.  Two calls in dominated blocks each get the call heuristic's 29% on their edge; nothing natural lifts both.

### Case 24's second arm and other items (a50_arm2.py, a50_x1.py, a50_neg.py)

- Arm 2 as `r = loadBl24(e);`: 25/73 with the label, 39/87 without, on src and on the nand base (attempt 49's numbers).  As `if (!DEVGL && !DEVGL16) break;` then loadBl24 67 and up, then the written-out body 42 and up.
- loadXell's retail test back in both callers (attempt 49's x1, as a `break` or an `if`): exp_t10's expect is needed again (60 loose without), and the barrier off is 59 to 118: x1's old 1/7 for the barrier was without loadBl24.
- exp_pr's spellings (`r != 0`, `(int)r < 0`, `(int)r <= -1`, `r == (uint32_t)-1`) on src and the equal bases at p0, 95, 99: as attempt 47 (2/4, 0/7, 0/7, 2/11).  At p0 (no `--param`) `(int)r < 0` leaves only its 0/7 in the whole object (buildFlash matches without the param now), so closing that alignment would remove exp_pr and the param together (2 tricks, with the cast as a borderline).
- The barrier off is 58/220: the size log's own -1 (attempt 10's line) plus a 130-line move of cases 4 and 27's blocks; the same on every base here.

### Don't retry (attempt 50)

- The CF/CG fallback, case 23, the signature check or the spare-slot moves as helpers (above).
- useNandData / notRead as levers: equal bases, nothing freed, every hint the same cost.
- Two-call loadBl24 bodies for lab_none (65 to 70% call share; it needs about 86%).
- Arm 2 through loadBl24 in any form, loadXell's retail test in the callers.

### What to try next

- lab_none: a loadBl24 that keeps two defaultBl60 call sites (for the size store) but whose own profile gives them about 86%, or a natural reason for the size store to stay before the copy with one call (the borderline's crossjump stands in for an alias question: sched2 moves the store because the copy's destination is a fresh malloc).  If a one-call form could keep the store, lab_none goes (precheck + label) and the `||` replaces attempt 4's borderline; loadBlFiles' case-27 block (24 loose) would still need a look.
- exp_t10's bbro reading isn't finished (why round 1's case 27 trace differs); a `-dA` read of the d block in both layouts may show what else the helpers' scaled profiles change.
- The late-inlining reading is a lever no earlier attempt used on purpose: a static helper too big for early inlining puts one call block in the caller's profile and brings its own profile in at IPA.  Tried here: cases 1 / 22 as one helper (22 loose), cases 3 / 4 as one (stays out of line).  Left: case 27's fallback chain as a helper, or helpers whose *own* profile is the lever (as loadBl24's is for lab_none above).

### Costs now (strict/loose, removed alone; 7 tricks, unchanged)

exp_pr 4/2 (`(int)r < 0` in its place 7/0, and then no `--param` needed), vol_fail 220/58, lab_devgl 57/14, exp_devgl 43/7, pin_size 82/40, lab_none 351/225 (8/4 with the precheck gone too; 0 loose but the size store with loadBl24's `||` body).

## Attempt 51

Goal: attempt 50's lead for lab_none (a loadBl24 with two defaultBl60 call sites whose own profile gives them about 86%), computed from the dumps before full scoring; whether a new loadBl24 body lets the DEVGL arm call it (lab_devgl); whether any of it moves exp_pr's alignment.  src as of b9136db8, unchanged.  New scripts in `tools/wip/dehint/bdgen`: `a51_pred.py` (loadBl24's predictions and defaultBl60 call share per body in `a51_bodies.py`), `a51_fpred.py <variant.c> <fn>` (predictions, block frequencies, tests and calls of one function from a variant's profile_estimate dump; works on any `a46run.py -k` output), and, run with `python tools/wip/dehint/bdgen/a46run.py <script>`: `a51_bl60.py` (defaultBl60 forms), `a51_guard.py` (console's case 24 guard spellings), `a51_se.py` (a size test in the SE condition, exp_pr), `a51_arm2.py` (a50_bl24's bodies x arm 2 written or calling loadBl24 x devgl label x console's precheck/label), `a51_store.py` (defaultBl60 store/copy forms on the `||` body), `a51_negb.py` (`(int)r < 0` at p0 on the bodies), `a51_wrap.py` (console's case 24 through a guard-holding helper), `a51_cont.py` (the guard as `continue`).  `bdbbro.sh` now compiles at the build's 99 (was 98).  Probe files in build/bd/a51/probe (not kept).  Loose/strict lines, p99 unless said.

### lab_none read off bb-reorder (bdbbro.sh on src with the precheck and label off, and on a50's `||` body)

- Without the precheck and label the only difference is the order of the last two blocks: round 4 takes the not-entered return (bb 63, freq 20) before the r = 1 block (bb 21, 14).  With the `||` body the r = 1 block (18) goes first although its frequency is lower, because its key carries a trace-end priority (`Possible start point of next round: 53 (key: -1001818)`): its predecessor, the inlined malloc block, ends a round-2 trace.
- In src's two-call form the two inlined defaultBl60 copies are already one malloc block by bbro (freq 145 = 43 + 102), and it sits mid-trace in round 3 (`22 [165] 20 [145] 24 [131]`: size test, malloc, copy), so the r = 1 block gets no priority.  In the one-call form the malloc block (178) starts a round-2 trace alone and the copy (160) can't follow it (round 2's exec threshold is 0.2 x the entry's 880 = 176).
- So the exact condition is **176 <= malloc block < 196** (the copy is 0.899 of it and must stay under 176).  malloc = case arm 716 x guard (29%: PRED_CALL alone) x loadBl24's share (70%).  The r = 1 block's own frequency can't do it (it would need 21, i.e. a malloc block of 208, which already meets the condition above).
- A second constraint, found with the guard helper below: in round 1 the case 24 guard block's trace must run on into the latch block (`18 [716] 57 [9120]`), which needs the skip edge's frequency >= 0.5 x 880 = 440, so the guard <= 38.5%.  So: guard x share in [0.246, 0.272], with the guard at most 38.5% (share >= 0.64).

### loadBl24's share: why two calls stop at 70% (a51_pred.py, probe q.c)

- gcc 6's "early return (on trees)" isn't the front end's: tree_estimate_probability_bb predicts NOT_TAKEN any edge that **jumps** (dest != bb->next_bb) to the return block (a block ending in the return with one successor, EXIT); if the edge's source has a single successor, the prediction goes on that block's incoming edges instead.  Block order is source order.  So exactly one block can fall through to the return block.
- Values seen: call 29/71, nonequal 72/28, early return 39/61, pointer 85, opcode positive 73, const return 67 (constant other than 0/1), negative return 4.  defaultBl60's NULL edge is 10.1% (pointer 15 + early return 39) in every form returning 0/1 (`if (e->data) {..} return 1`, a result variable, `== NULL`, `return e->data == NULL` all predict the same; a51_bl60.py: all IDENTICAL but the last, all 4/8 without the precheck); only `return 2` / `return -1` change it (behaviour).
- Two calls: the size test always has PRED_CALL against its call, so it is at most ds(72, 61, 29) = 62.2% (call B falling through to the return, the `return 0` edge jumping); the load test is 20.7% with call A jumping to the return, 29% with A last.  Best: 0.207 + 0.793 x 0.622 = **70.0%** (src, g0, r2..r4), else 0.29 + 0.71 x 0.512 = 65.4% (ok1, n2, n3).  The `||` body: load test 29%, size test ds(72, 61) = 80.1% with no call heuristic (its call block has two predecessors), 85.9%.
- So the share window [0.846, 0.94] needs one call site, and the guard window needs a guard predictor near 57-61% combined with the call's 29%.

### The guard (a51_guard.py, a51_wrap.py, a51_cont.py)

| Form | Guard | Result (precheck and label off) |
|---|---|---|
| src `if (xb.glitch2mfg)` / `!= 0` | 29% | 4/8 |
| `> 0` / `>= 1` (opcode positive 73%) | 52.5% | 225 (case 24 joins round 1's trace) |
| `== 1` | 13.7% | 43 |
| a wrapper `if (!xb.glitch2mfg) return 0; return loadBl24(e);` (three forms) | early-inlined | IDENTICAL with the label, 4/8 without (no change) |
| a guard-holding copy of loadBl24 (`if (!xb.glitch2mfg) return 0;` then the body; w4, w5), not early-inlined | **39.0%** (call + early return) | 209 to 233: malloc 196 (copy 176, the trace runs on) and round 1's skip edge 716 x 61% = 437 < 440 |
| `if (!xb.glitch2mfg) continue;` / `{ ..; break; } continue;` | PRED_CONTINUE is 50% in gcc 6 | 313 and up (the skip edge bypasses the r test: CFG change) |

Nothing lands in [35.1%, 38.5%]: no gcc 6 predictor sits between the call's 29% and ds(29, 61) = 39%.

### One call and the size store (a51_store.py, a51_arm2.py)

- The `||` body with loadBlFiles' second arm calling loadBl24 and the devgl label kept: console differs **only in the size store** (2/2), loadBlFiles 61 (the same store in its first arm, plus case 27's and the SE setFlashBuild blocks); with arm 2 written out, loadBlFiles 24 and console 20 (+displ).
- The store's place is sched2's: in the copy block the ready list is the store, `ecx=0x18`, `edi=eax`, `esi=defBl60`, and rank_for_schedule's RFS_DEP_COUNT tie-break prefers insns with more dependents.  The three register sets feed the rep movs; the store has none (the copy's destination is the malloc result, so points-to separates it from `e->size`), so it goes last.  With two calls crossjump drops the copy's memory attributes, the store gets the rep movs as a dependent, and the tie falls to source order (store first).
- defaultBl60 spellings (the copy before the store, a local pointer `p` either way, `sizeof(defBl60)`, `e->size` as the copy's length): all the same 2/2 and 61.  Nothing natural gives the store a dependent.

### Other items

- Bodies x arm 2 x labels (a51_arm2.py, 11 bodies x 2 x 2 x 2): with arm 2 written out, g0, r2, r3 and r4 are IDENTICAL (equal bases), n2/n3/ok1 put console at 4/8; arm 2 calling loadBl24 is 25/73 and up with the label, 39 and up without, for every two-call body; the one-call bodies are 61 (above).  So no body frees lab_devgl.
- exp_pr (a51_negb.py at p0): `(int)r < 0` stays 0/7 on every body and arm form (the 5..21 arm's profile doesn't see case 24).  A size test in the SE condition (a51_se.py) adds a compare the reference doesn't have (72 loose and up), so it can't help: the alignment needs a predictor change on the *existing* tests.
- exp_devgl's 7 lines re-read: the `sub/cmp/jbe` branch where the reference has `cmovbe`; attempt 41's mechanism, not retried.

### Don't retry (attempt 51)

- Two-call loadBl24 bodies for the share (capped at 70.0% by the early-return rule above; 65.4% is the only other value).
- Console guard spellings `> 0`, `>= 1`, `== 1`, `!= 0`; wrappers around loadBl24 (early-inlined, no change); a guard-holding loadBl24 copy (39.0%, just past round 1's 38.5%); the guard as `continue`.
- defaultBl60 forms for the NULL edge (10.1% in every 0/1 form) or for the size store (sched2's tie-break, above).
- A size test in the SE condition for exp_pr.

### What to try next

- lab_none's condition is now exact (malloc block in [176, 196), guard <= 38.5%, so guard x share in [0.246, 0.272]).  Levers not tried: the case arm's 716 (console's switch has 10 edges; 9 would give 796, i.e. a malloc block of 161 at 29% x 70%, still short; 8 edges, or a higher switch-block frequency from the none test, would be needed), and the entry's 880 (the thresholds are 0.5 and 0.2 of it: a loop predicted to iterate longer, e.g. a third loop exit splitting PRED_LOOP_EXIT's 9% three ways, lowers both thresholds; but every other block of loadConsoleBlFiles is measured against them too).
- The size store with one call: anything that makes the copy's destination may-alias `e->size` (points-to losing the malloc result), or a natural dependent of the store in the copy block.

### Costs now (strict/loose, removed alone; 7 tricks, unchanged)

exp_pr 4/2 (`(int)r < 0` in its place 7/0, and then no `--param` needed), vol_fail 220/58, lab_devgl 57/14, exp_devgl 43/7, pin_size 82/40, lab_none 351/225 (8/4 with the precheck gone too; 2 loose, the size store, with loadBl24's `||` body and arm 2 calling it).

## Attempt 52

Goal: the sharing lever (attempts 46, 49) on the two tricks outside the loaders: calcBlAreaSize (pin_size) and buildFlash (exp_devgl), with helpers shared with addBlsToImage, addUpdateBls and the loaders where the same code appears; check which inliner takes each helper.  src as of c7288fb6, unchanged.  New scripts in `tools/wip/dehint/bdgen`, run with `python tools/wip/dehint/bdgen/a46run.py <script> [-k label]` on src/build.c: `a52_base.py` (src, pin / dev off), `a52_cba.py` (calcBlAreaSize helpers: `addCfArea` = setPatchSlot + 2 x imgCfSize for kit and retail, three spellings; `blAreaEnd` with the 16K round; `blSize(t)` = files[findFile(t)].size for JTAG and kit), `a52_xell.py` (the xell room test as `xellEnd(size)`, three bodies, with or without addCfArea), `a52_rhelp.py` (retail's sums and xell test as `retailBlEnd()`), `a52_dev.py` (a "virtual fuses in use" predicate `vfusesUsed()`, six bodies, in buildFlash and/or addBlsToImage's case 23 / case 24 and addUpdateBls' case 24), `a52_devdiag.py` (the same with a call added; diagnostic), `a52_devms.py` (the fuse helper with the salt memset in it; diagnostic); standalone `a52_cmp.py <a.c> <b.c> <_sym> [gcc flags]` (one function's diff between two sources under extra flags, e.g. -fno-early-inlining).  Scratch in build/bd/a52 (not kept).  Loose/strict lines, p99.

### exp_devgl: the callee-profile route, confirmed (a52_dev.py, a52_cmp.py)

- buildFlash's dev test is `(unsigned)(type - 4) <= 1`, opcode positive 27% (a51_fpred.py on src minus the expect); tree-sink moves the setne into the non-dev arm unless that arm is >= 75% of the def block.
- In a helper `int fuse = xb.glitch2mfg != 0; if (DEVGL || DEVGL16) return 1; return fuse;` (`dret`) the dev edge also gets the early-return rule (it jumps to the return block): **ds(27, 39) = 19.1%** in the helper's own profile_estimate (read off the dump: `succ: 4 [19.1%]`, `3 [80.9%]`).
- With `-fno-early-inlining` as a diagnostic (`python tools/wip/dehint/bdgen/a52_cmp.py src/build.c dret.c _buildFlash -fno-early-inlining`), buildFlash with the helper and **no expect** differs from src (with the expect, same flag) only in 5 loop compares' operand order (`cmp ecx,eax` / `cmp eax,ecx`: the helper's SSA names); its start is the reference's `setne bl; sub eax,4; cmp eax,1; mov eax,1; cmovbe ebx,eax`.  So the IPA-scaled callee profile is exactly what the expect stands in for.  The `flag` body (src's statements in a helper, no early return) and `d1st` (dev test first) don't do it (53, 56 there).
- But einline takes every such helper: size 6, growth under 14 and no calls (einline dump: `Inlining vfusesUsed into buildFlash`), and buildFlash's own profile_estimate then re-predicts the inlined test at 27%: all six bodies in buildFlash only are 7/43 (`dret`, `flag`), 11 (`d1st`, `dret` with `fuse = JTAG || ..`), 12 (`g1st`), 21 to 27 (`||` bodies).
- A helper stays for IPA only with a call (growth x (calls + 1) > 14, a50's reading).  A log or imgSize call put first in the helper (a52_devdiag.py) is still early-inlined (size 9) and adds code (91 loose and up).  The salt memset (a real call at GIMPLE, expanded at RTL) moved in (`fuse = initFlash(salt);`, a52_devms.py) does keep it for IPA: `dret` 3 loose / 285 strict (the JTAG test is now an early return too, 19.9% instead of 28%, so the `fuse = 1` move ce1 makes into the entry block becomes an out-of-line `mov ebx,1; jmp` block), `flag` 11.  Not natural (a helper that clears the salt and returns the fuse flag), not pursued.
- Sharing the predicate: addBlsToImage's case 23 (`glitch2mfg ? 0x60 : dev ? 0x60 : 0x10`) and case 24, addUpdateBls' case 24 through `vfusesUsed()` cost 21 to 500 lines in those functions for every body (addUpdateBls 2/18 with the `||` bodies, addBlsToImage 21/55 at best with `dret`/`flag` in case 23 only), so no place shares it for free.

### pin_size (a52_cba.py, a52_xell.py, a52_rhelp.py)

- `addCfArea(size)` (setPatchSlot then `size + 2 * imgCfSize()`), the tail both kit and retail write: early-inlined (size 6, two calls, growth x 3 <= 14), IDENTICAL with the pin and 40/82 without it in all three spellings: an equal base that frees nothing.  With the 16K round inside (`blAreaEnd`, a return from each arm): 100/220 with the pin, 132 without.
- `blSize(t)` for JTAG's and the kit's `xb.files[findFile(t)].size`: 278 loose in calcBlAreaSize.
- `xellEnd(size)` (findFile(25), the room test and the warning; three bodies): IPA-inlined (it holds the log call), 10/10 with the pin (the inlined block's own compare `cmp esi,eax; jae` for `cmp eax,esi; jbe` and an address computed in another order), 46/88 without: the kit sum stays `prephitmp + size` (unflipped).  The IPA-inlined body's fresh names don't reach PRE's kit insertion.
- `retailBlEnd()` (retail's four sums and the xell test): not inlined at all (333 loose; calcBlAreaSize calls it).

### Don't retry (attempt 52)

- exp_devgl by any call-free fuse or devgl predicate helper (einline takes it, then the caller re-predicts); by sharing that predicate with addBlsToImage / addUpdateBls (both move).
- pin_size by the shared CF-area tail (equal base), the files[findFile(t)].size helper, the xell test or retail's end as helpers.

### What to try next

- exp_devgl now has a precise, verified condition: the fuse decision must arrive in buildFlash through IPA inlining, from a body whose dev arm is an early return (or any other form whose own profile gives dev <= 24.9%), and the JTAG test must keep 28% (in buildFlash, or in the helper without an early return).  What's missing is a natural reason for that helper to hold a call; a call is only natural if the function does real work.  Look at whether a "virtual fuses" helper could own work that the reference really does at buildFlash's start (it doesn't seem to: memset, then the fuse flag, then the header / checkBootImage branch), or whether the fuse flag could be the return value of a helper that does work that happens later in the reference (no: the loads must come before the calls).
- The callee-profile lever generally: every frequency trick here is a predictor window; an IPA-inlined helper brings its own early-return / const-return predictions.  Map which remaining windows (lab_devgl's arm 2, exp_pr's SE copy) sit in code that a call-holding helper could naturally own.
- Otherwise attempt 51's list stands.

### Costs now (strict/loose, removed alone; 7 tricks, unchanged)

exp_pr 4/2, vol_fail 220/58, lab_devgl 57/14, exp_devgl 43/7, pin_size 82/40, lab_none 351/225 (re-measured pin and dev with a52_base.py; the rest as attempt 51).

## Attempt 53

Goal: attempt 52's exp_devgl lead: a *natural* fuse helper that stays out of early inlining, so IPA brings in its own profile (dev arm as an early return, 19.1%).  src as of 4ec63755, unchanged.  No new scripts; `a52_devms.py`'s third body `dret2` (not reported by attempt 52) was scored and read with `a51_fpred.py`.  Loose/strict lines, p99.

### Which callees gcc 6's early inliner refuses (read against the einline behaviour seen in attempts 50 to 52)

- want_early_inline_function_p: growth <= 0 is always taken; otherwise refused if the edge is not maybe_hot, if growth > early-inlining-insns (14), or if the callee has n non-inexpensive calls and growth x (n + 1) > 14.  memset counts as a call (attempt 52's initFlash stayed out).
- maybe_hot_p at einline time: buildFlash has no profile yet, so every edge has frequency CGRAPH_FREQ_BASE; the edge is cold only if the callee's node frequency is UNLIKELY_EXECUTED or EXECUTED_ONCE, and without profile feedback compute_function_frequency sets those only from cold/hot attributes, noreturn, main and static ctors/dtors.  Nothing natural.
- can_early_inline_edge_p: a callee not yet in SSA form (only in a call-graph cycle), or one inline_forbidden_p rejects (va_start, setjmp, alloca, nonlocal goto / label addresses), which IPA can't inline either.
- So a call-free fuse helper (size 6, growth ~4) is always einlined, and the only ways out are a call or ~17 insns of body that later passes remove; the latter is dead code.

### Calls a fuse helper could own

- The reference's buildFlash runs only the salt memset before the fuse flag; the next calls are the header log and writeInitialHeader / checkBootImage, which must come after it (they could change xb, so gcc keeps the flag ahead of them), so a helper that computes the flag and then writes the header would need two results (the flag and checkBootImage's r).  The `if (fuse)` block's findFile(24) / setFuseCpuKey come after keysInit, so a helper doing that work computes the flag too late (the reference computes it at entry).
- **`dret2`** (a52_devms.py): `int fuse = 1; memset(salt, 0, 16); if (xb.type != BUILD_JTAG) { fuse = xb.glitch2mfg != 0; if (dev) return 1; } return fuse;`: **3/285**, the same as `dret`.  The helper's profile (`python tools/wip/dehint/bdgen/a51_fpred.py build/bd/a46/dret2.c initFlash` after `a46run.py a52_devms.py -k dret2`): bb 2 (`_7 != 2`) 80.1% = nonequal 72% + early return 61%, bb 3 (dev) 19.1%.  The JTAG test's not-JTAG side falls to the same return block, so the early-return predictor fires on it whichever way it is spelled; the JTAG 19.9% moves `mov ebx,1` from the entry into an out-of-line block (`je 1320`).  Moving the JTAG test back into buildFlash leaves the memset on one path only.
- In this IPA-inlined form the diff is only that block: the 5 loop-compare operand orders that `-fno-early-inlining` showed in attempt 52 are absent, so they came from the diagnostic flag (other functions' SSA), not from the helper.

### Evidence about the original

- tools/ref/xeBuild64 (v1.16, gcc 4.9.2): buildFlash (0x409a70) starts `mov ebp,1; ...; cmp eax,2; je; mov r8d,[glitch2mfg]; xor ebp,ebp; test; setne bpl; sub eax,4; cmp eax,1; mov eax,1; cmovbe ebp,eax`, the same shape, inline; gcc 4.9 kept some helpers gcc 6 inlined, but there is no fuse helper here.
- build.o's strings with fuse / glitch / devgl / virtual: only "
Virtual Fuses set to:" (showFuses' title) and the type-24 messages; no log a fuse helper could print.

### Don't retry (attempt 53)

- exp_devgl by any fuse helper kept out of einline: the salt memset is the only call available and makes the JTAG edge an early return in the helper (3/285 with or without the dev early return's JTAG spelling); other calls run after the flag; the einline refusal conditions above leave no natural alternative.
- Reading the 5 loop compares of the -fno-early-inlining diagnostic: they don't appear in a real IPA-inlined form.

### What to try next

- exp_devgl looks closed by static predictors (attempt 44's audit) and by the callee-profile route (here).  Unless the user accepts a memset-owning helper as borderline (it would still need its JTAG test's 28%, which no helper body gives), spend attempts on the other tricks.
- exp_pr's `(int)r < 0` near miss (0/7, the no-key log copy's `.p2align`) and lab_none's one-call loadBl24 (size store) remain the closest; attempt 51's list stands.

### Costs now (strict/loose, removed alone; 7 tricks, unchanged)

exp_pr 4/2, vol_fail 220/58, lab_devgl 57/14, exp_devgl 43/7, pin_size 82/40, lab_none 351/225 (as attempt 52).

## Attempt 54

Goal: the brief's lever, a helper that IPA (not einline) inlines and that brings its own profile, on (a) exp_pr's `(int)r < 0` near miss (the SE copy's P(<=5) needs >= 62.5%: q <= ~9%, or S up, or p up) and (b) lab_none's one-call loadBl24 (the size store), then (c) if time remained.  src as of 762425c6, unchanged.  New scripts in `tools/wip/dehint/bdgen`, run with `python tools/wip/dehint/bdgen/a46run.py <script> [-p ..] [-k label]` on src/build.c: `a54_neg0.py` (baseline: src and `(int)r < 0`), `a54_sig.py` (the signature check as a helper, six bodies x the tail as expect / `r` / `(int)r < 0`), `a54_t14.py` (the tail with `type == 14` first, five orders x three r spellings), `a54_or.py` (console's case 24 forms: loadBl24 `||`, the guard and `||` written out, nested, two calls written out; with and without the precheck and label); standalone `a54_dump.py <variant.c> <fn> [bb lo hi]` (one function's whole profile_estimate dump) and `a54_rdiff.py <variant.c> <_sym> [p]` (one function's diff against build/bd/reference.o).  Scratch in build/bd/a54 (not kept).  Loose/strict lines, p99 unless said.

### (a) exp_pr: the profile it works with (a54_dump.py on `(int)r < 0`)

- loadBlFiles' 5..21 arm at profile_estimate: bb6 (loadInputFile's r, 597, 50%), bb13 (`if (r) break` after the fallback, 50%), bb14 `type == 9` 298 (28%), bb15/16 'S'/'E', bb17 the SE block **7**, bb18 checkBl's r (298, 50%), bb19/20 `5 || 17 || 11` (149), bb21 pub1bl (95, pointer 85%), bb22 the verify (81, call 71/29 both ways, 50%), bb23 failed log S = 41, bb24 passed 41, bb25 no-key 14, bb26 `xb.type <= 5` Xc = 149 (p 50%), bb27 `(int)r < 0` (q 27%), bb28 `type == 14`.  As attempt 48: P(<=5 on the copy) = Xc p (1 - q) / (Xc - S) = 0.50.
- bb13 is the one free factor left in the SE block: SE = 597 x c x 0.022 must be under 6.5 and the no-key log 597 x c x 0.048 at 10.5 or more, so c (bb13's continue share) in [0.37, 0.496].  ds(72, 29) = 48.8% would do, but that needs a nonequal compare (r against a nonzero constant) and a call in bb14, neither natural (loadInputFile's r is any nonzero on failure, so `if (r)` can't be respelled).

### (a) The signature check as an IPA-inlined helper (a54_sig.py, 18 cases at p0 and p99)

| Body | Call site | expect kept | `r` | `(int)r < 0` |
|---|---|---|---|---|
| `sigFailed`: 1 on failure, pass last | `if ((5 or 17 or 11) && sigFailed(e)) r = -1;` | 63/136 | 65/138 | 63/136 |
| the same, nested call site | `if (..) { if (sigFailed(e)) r = -1; }` | 63 | 65 | 63 |
| `sigFailed`, failure last | as above | 91 | 93 | 91 |
| `sigOk`: 0 on failure | `&& !sigOk(e)` | 63 | 65 | 63 |
| `sigOk` with an `ok` flag | as above | 124 (+displ) | 126 | 124 |
| `checkBlSig`: -1 on failure, failure last | `r = checkBlSig(e);` | 103 | 103 | 139 |

- The cost is the helper itself (with the expect kept it is already 63 and up): the inlined body's blocks and the caller's test of its result are new code against the reference.  And the lever points the wrong way here: a -1 return is PRED_NEGATIVE_RETURN (4%), so S (the failed flow) falls, where the formula needs S at about 62 of 149 (the verify about 76% failed); a 0/1 return gets no return predictor, and the caller's test of the result is 50% again.  Attempt 50's three bodies (95 and up) agree.

### (a) The tail's order (a54_t14.py, 15 cases at p0 and p99)

- `type == 14` first (r is 0 for type 14: it skips the signature check, and checkBl's failure already broke), so `if (xb.type > 5) setFlashBuild(..)` puts the call in the test's dominated successor (PRED_CALL, which would give P(<=5) 71% on the original): `{ if (> 5) set; break; } if (<= 5 && r) goto fail;` 141 loose; with `else if` 116; `type == 14 && xb.type > 5 .. else if` 114 to 141; nested 141.  The SE path's threading and the block order change wholesale.  Kit first (`e`) is attempt 47's: 2/4 with `r`, 0/7 with `(int)r < 0`, IDENTICAL with the expect.

### (b) lab_none: console's case 24 without loadBl24 (a54_or.py, a54_rdiff.py)

- loadBl24 `||` (attempt 50's body): loadBlFiles 24/83, console 20 (+displ: the only real line is the size store).  Read with a54_rdiff.py: console differs from the reference in `mov [ebx+4],0x60` after the three register sets instead of before them, plus call displacements.
- Console's case 24 written out, loadBl24 unchanged for loadBlFiles: `if (xb.glitch2mfg && (loadBaseFile(..) || e->size != 0x60)) r = defaultBl60(e);` and the nested form: **6/10 without the precheck and label, 2/2 with them** (only the size store).  Its loadBaseFile test keeps PRED_CALL (29%: it dominates the merged call block even with two predecessors), so the share is 0.29 + 0.71 x 0.72 = 0.80 (call block 166 of 208), not loadBl24's own 85.9%, and the malloc block (166) stays under round 2's 176: the r = 1 block goes after the return again.  Two calls written out (`if (load) r = dB(e); else if (size) r = dB(e);` under the guard): 4/8 without, IDENTICAL with: an equal base for src (console needn't call loadBl24).
- Why nothing orders the store with one copy: in console e is &xb.files[i], so the store is a decl reference `xb.files[i].size` and the rep movs destination is the malloc result (points-to {HEAP}); the oracle separates them, sched2's ready list puts the three register sets first (they feed the rep movs) and the store last.  Only two crossjumped copies (attempt 51) lose the destination's memory attributes.  Anything that keeps the copy's pointer from being a fresh malloc result (realloc, a pointer through memory, calloc via setFileData) changes behaviour or code.

### (c) Not reached

vol_fail (58/220) and lab_devgl (57/14) were not swept.  lab_devgl's arm-2 test is 13.7% because arm 2's own block holds loadBaseFile (PRED_CALL); joining the arm into arm 1's call block would load twice for a glitch2mfg devgl build (behaviour), and a helper keeps the call in the guarded block, so the lever doesn't reach it.

### Don't retry (attempt 54)

- The signature check as a helper in any return form (63 loose and up even with the expect; its -1 is 4%, the wrong way).
- The tail with `type == 14` tested first, in any of the five orders (114 and up).
- Console's case 24 with the guard and `||` written out (share 0.80, PRED_CALL on the load test) or nested: still the size store with the label.

### What to try next

- exp_pr: what is left is bb13's 50% (the r test after the CF/CG fallback; a continue share in [37%, 49.6%] would do) or a predictor on the `xb.type <= 5` test; neither has a natural source here.  An IPA helper only changes frequencies *inside* itself, and every candidate region (the signature check here, the fallback as attempt 50's loadUpdateBl) costs 63 lines and up on its own.
- lab_none: the size store is the whole problem for every one-call form; look for a natural defaultBl60 whose copy destination is not a fresh malloc result to the alias oracle and that still compiles to the reference's malloc / test / store / rep movs (none found), or a second defaultBl60 copy in console that crossjump could merge.
- Otherwise attempt 51's list stands.

### Costs now (strict/loose, removed alone; 7 tricks, unchanged)

exp_pr 4/2 (`(int)r < 0` in its place 7/0, then no `--param`), vol_fail 220/58, lab_devgl 57/14, exp_devgl 43/7, pin_size 82/40, lab_none 351/225 (as attempt 53; lab_none with console's case 24 written out with `||` and the label kept: 2/2, the size store).

## Attempt 55

Goal: the brief's two focus items on the current form: why vol_fail went from 1/7 (5877c248 / 28c25d7f) to 58/220 with attempt 49's helpers, and lab_devgl's bbro picture without the label in the light of the IPA-inlined helpers.  src as of 74b66abd, unchanged.  New scripts in `tools/wip/dehint/bdgen`, run with `python tools/wip/dehint/bdgen/a46run.py <script> [-p ..] [-k label]` on src/build.c: `a55_bar.py` (loadXell / loadBl24 written back into loadBlFiles only, exp_t10 back or not, each with and without the barrier), `a55_smc.py` (two SMC-failure spellings x barrier x pr / lab / `(int)r < 0`), `a55_dev.py` (a `useBuiltIn` helper for cases 1 / 22 and defaultBl60, with and without the label); standalone `a55_r1.py <variant.c>..` (loadBlFiles' r = 1 block, retest, malloc and suGetCF blocks with freq / seq / preds from `-dA`).  Scratch in build/bd/a55 (not kept: `old.c` = 28c25d7f's src, `pre49.c` = 26aca4bb^, `h49.c` = 26aca4bb, each with an `_nb` copy without the barrier; `det_*/` full `-fdump-tree-all-blocks-details` dumps; `smcp.py` (the SMC test's succ probabilities through every tree pass), `ob.py`, `blk.py`, `fn.py`).  Loose/strict lines in loadBlFiles, p99 unless said.

### vol_fail: where the 58 comes from (a55_bar.py, dumps)

| Base (loadBlFiles only; console keeps the helpers) | barrier on | barrier off |
|---|---|---|
| src (both helpers, no exp_t10) | IDENTICAL | 58/220 |
| both helpers, exp_t10 back | IDENTICAL | 59/238 + displ |
| loadBl24 written out, loadXell called | 2/53 + displ | 9/74 |
| the same + exp_t10 | IDENTICAL | 9/74 |
| loadXell written out, loadBl24 called | 62/168 + displ | 118/307 |
| the same + exp_t10 | IDENTICAL | 59/238 + displ |
| both written out (no exp_t10) | 62/168 + displ | 63/175 + displ |
| both written out + exp_t10 (= 26aca4bb^) | IDENTICAL | **1/7** |

- So the 1/7 picture needs the pre-49 shape of both cases with exp_t10; neither helper alone brings it back.
- The 58 lines (a54_rdiff.py on src without the asm): the size log's own -1 (attempt 10's line) plus a move: the reference's -1 block (`mov edi,-1` after case 2's smcSetLoad test) falls into the could-not-read join; without the asm the join is laid out after the `type == 10` test's false edge instead, and the CG block moves to the end.
- Why, from `-dA` and the tree dumps: without the asm the SMC failure's `r = -1` is an empty forwarder into loadBlFiles' `if (r)` join; the SMC call block has two preds (the bin-dir file's moves and the nand-dump moves, `r_9 = PHI <r_241, 0>`), so vrp1 registers joiner threads `(103,108) J (108,109) (109,111) nocopy (111,130)` for both and executes them (`Threaded jump 107 --> 108 to 167`, `103 --> 108`): one copy of the SMC block whose failure edge goes straight to the log.  The threader's profile update leaves that copy's test at **92.5% / 7.5%** (dce2 onwards; 50/50 up to vrp1), so the -1 block is 38 instead of 253 and bbro joins the log (430) to another trace.  With the asm, `fail` is a real block with three preds and the SMC test stays 50/50.  In 26aca4bb^ without the asm the same joiner threads are *cancelled* (`Cancelling jump thread: (101, 106) .. (106, 107) joiner ..`), which is why that base only had the size-log line.  (Not read: which edge of the path holds the conflicting thread in each base; mark_threaded_blocks cancels a joiner path when a later edge on it starts a thread of its own.)
- **a55_smc.py**: the SMC failure as `if (!e->offset) { fail: r = -1; } break;` (`if`) or as `if (!e->offset) goto fail; break;` with `fail: r = -1; break;` after the default case (`end`): with the barrier both are **IDENTICAL** at p95 / p99 (equal bases; p0 0/7 as src), and without it **1/7** (the size-log line only).  The other hints cost what they cost on src (pr 2/4, lab 14/57, `(int)r < 0` 0/7) and add to the barrier's 1/7 (nb + pr 5/17, nb + lab 15/64, nb + neg 3/20).  So on these forms the barrier is back to attempt 47's 1/7 (attempt 47 had scored the same two spellings at 59/238 on the pre-helper form).
- The 1/7 line itself, re-read: at jump2 the size log block ends `call log_printf; mov edi,-1` (out-of-SSA puts the copy at the end of a single-successor source; sched2 later moves it before the call), and the SMC -1 block is the join's fall-through predecessor.  Crossjump would have to redirect the log block's 1-insn tail into the -1 block, and min-crossjump-insns (5) is waived only when the from-block is wholly matched, which the log block isn't.  So the -1 must be in a block of its own on the size path at expand time: a critical edge out of the log block (it has one successor) or a block that survives to RTL.  The tree passes leave no such block without a statement (mergephi / cfgcleanup remove empty forwarders; a `fail` PHI of constants folds; tree_forwarder_block_p only protects loop headers, latches, preheaders and nonlocal / forced labels).  Attempt 31's verdict stands.

### lab_devgl: the bbro picture without the label (a55_r1.py, bdbbro.sh)

- The 14 lines are one block pair: arm 1's retest (`mov eax,[xb.type]; sub 4; cmp 1; jbe arm2`, freq 24, after arm 1's defaultBl60 failure) falling into the shared **r = 1 block** (`mov edi,1; jmp log`; preds: arm 2's malloc failure 10.1%, cases 1 and 22's malloc failures 9.0% each, the retest's fall-through, which the threader leaves at ~0%).  The reference lays the pair out before the suGetCF block; without the label it lands after the SE test's log.
- In bbro numbering the r = 1 block is 104, the retest 122, arm 2's malloc block 48, the suGetCF block 10.  With the label, arm 2's malloc block is 180 and makes a round-2 trace of its own (`Trace 28 (round 2): 48 [180]`), and as that trace ends bbro gives 104 a trace-end priority (`Changing key for bb 104 from -50 to -1001850`, priority 18 = 180 x 10.1%); in round 3 104 is taken right after 13 and before 15 [95] and 84 [76], and connect_traces then places `122 104` there.  Without the label arm 2's malloc block is 51 (round 3, mid-trace `48 [51] 49 [46]`), 104 keeps its plain key -37 and becomes a round-4 trace after the suGetCF block's 10 [41] (`Connection: 122 104` comes later).
- So the condition is a trace-end priority for 104, i.e. arm 2's malloc block >= 176 (0.2 x 882) at bbro, x3.5 of what arm 2 gets naturally (the arm-2 test is 13.1%: opcode 27% with PRED_CALL on its dominated loadBaseFile block); 104's own frequency doesn't help below 96 (on plain keys it would have to beat 15 [95] and 84 [76]).  The other preds can't give priority: cases 1 / 22's malloc blocks are mid-trace (their copy blocks follow), the retest is round 4 (24).
- a55_dev.py: `useBuiltIn(e, data, size)` (malloc, NULL test, size, memcpy; returns 1 / 0) for cases 1 and 22, with or without defaultBl60 written as `return useBuiltIn(e, defBl60, 0x60);`: **IDENTICAL with the label** (an equal base), 14/34 without (src 14/57).  Its own profile gives the NULL edges 15% (pointer heuristic, no early-return rule in the callee), so the r = 1 block rises from 37 to 57 and moves into round 3, but with key -57 (no priority): taken after 15 and 84, still after the suGetCF block.  `uint32_t` return: 14/57.  One case only: 14/55.
- The 0.86 factor (attempt 46) belongs to the other route (arm 1's malloc trace ending in round 2, attempt 45), which the current form doesn't use: arm 1's malloc block is 237 and its copy block 0.899 of it, so that trace runs on unless the case arms fall to about 0.83 x; and the priority that matters now is 104's, from arm 2.

### Don't retry (attempt 55)

- vol_fail by helper boundaries in loadBlFiles (a55_bar.py): only the full pre-49 shape (both helpers written out and exp_t10) gives 1/7; the SMC spellings below give it with the helpers.
- vol_fail on the `if` / `end` SMC forms by any -1 site or `fail:` placement: the remaining line is attempt 10/31's crossjump rule.
- lab_devgl by raising the r = 1 block's own frequency (useBuiltIn, malloc-test spellings): it needs a trace-end priority, not frequency.

### What to try next

- If the barrier is ever removed by some other route, start from a55_smc.py's `if` form (equal base, barrier 1/7 instead of 58/220).
- lab_devgl: a natural reason for arm 2's malloc block to end a round-2 trace (freq >= 176 at bbro), or for some other predecessor of the r = 1 block to end a trace in rounds 1 to 3.  None of its preds can as the code stands, and arm 2's frequency would need x3.5 (attempt 46: no gcc 6 predictor does that for a build-type test).
- Otherwise attempt 54's list (exp_pr's bb13 share, lab_none's size store) stands.

### Costs now (strict/loose, removed alone; 7 tricks, unchanged)

exp_pr 4/2 (`(int)r < 0` in its place 7/0), vol_fail 220/58 on src (7/1 on a55_smc.py's equal bases), lab_devgl 57/14, exp_devgl 43/7, pin_size 82/40, lab_none 351/225 (as attempt 54).

## Attempt 56

Goal: (1) vol_fail on attempt 55's SMC equal base: a natural case-23 shape that gives the patch-size failure's -1 a block of its own at expand, or lets crossjump merge the log block; (2) the SMC base + exp_pr's `(int)r < 0` + the barrier off together, across the param; (3) attempt 55's list.  src as of 48b210a4, unchanged.  New scripts in `tools/wip/dehint/bdgen`, run with `python tools/wip/dehint/bdgen/a46run.py <script> [-p ..] [-k label]` on src/build.c: `a56_fail.py` (13 case-23 forms x the `if` / `end` SMC bases from a55_smc.py x exp kept / `(int)r < 0`, barrier off), `a56_negp.py` (the `if` base x barrier on/off x expect / `r != 0` / `(int)r < 0`, for a param sweep); standalone `a56_dump.py <variant.c> <outdir>` (every tree dump with blocks and details, plus expand / jump2 / bbro) and `a56_trace.py <outdir> [text]` (the block holding a statement, by default the size log, through every tree dump: its successor, that block's preds and first statements).  Scratch in build/bd/a56 (not kept: `nb/` and `b/` are the dumps of a55's `if_nb` and `if_b`).  Loose/strict lines in loadBlFiles, p99 unless said.

### (1) Case 23's forms on the SMC bases, barrier off (a56_fail.py; `if` and `end` give the same numbers)

| Form | Result | exp_pr as `(int)r < 0` too |
|---|---|---|
| src (`log; goto fail;`) | 1/7 | 3/20 |
| `own` (`log; r = -1; break;`) | 1/7 | 3/20 |
| `pre` (`r = -1; log; break;`) | 1/7 | 3/20 |
| `nest` (`if (!r) { if (bad) { log; goto fail; } append; } break;`) | 1/7 | 3/20 |
| `else` (`if (bad) { log; goto fail; } else append;`) | 1/7 | 3/20 |
| `good` (good path first, then `log; goto fail;`) | 59 (+.rdata) | 61 |
| `rep` (`if (bad) log; if (bad) goto fail;`) | 62 (+.rdata) | 62 |
| `tern` (`r = bad ? -1 : 0; if (r) { log; break; }`) | 347 | 349 |
| `h_ret` (`r = badPatchSize(e);`, a helper logging and returning -1) | 7/16 | 9/29 |
| `h_v` (a void helper for the log, then `goto fail`) | 7/16 | 9/29 |
| `h_chk` / `h_chkf` / `h_okf` (the size test in a helper returning -1 / 1 / 0 on failure) | 61 (+.rdata) | 63 |

- Every form that keeps the reference's CFG is exactly the 1/7 (the size log's own `mov edi,-1`); the helpers are IPA-inlined but reload `e->size` through another base (`mov eax,[ebp+0x410]`) and move the log's argument stores, so the -1 is still appended.  No form moves the line.
- Where the empty `fail` block goes (a56_trace.py on `if_nb`): it is a real block up to fre1 (preds: the size log, the sig-failed `r` test, the SMC test), and is removed by mergephi1's CFG cleanup.  Correction to attempts 31 / 55's picture: the SMC test also has an edge straight to the switch join (its `break`, r = r_9) whose PHI argument differs from fail's -1, and that does **not** keep the forwarder: cleanup splits that one edge (a new empty block, `pred: 91` only) and redirects the rest, so fail goes anyway.  So no pred-sharing arrangement keeps an empty fail; only a statement does, and it has to be one RTL drops (the asm is exactly that).
- At .optimized the could-not-read log's PHI takes -1 from the size log (single successor: appended at expand), the SMC test and the sig-failed `<= 5` test (both critical: split at expand, placed right before the log, the last split being the fallthru), and the setFlashBuild copy (the reference's own -1 at 37d9).  The reference's 564 block is reached by the SMC fallthru, the size log's `jmp` and the sig-failed `jbe`.
- Crossjump, once more: for the size log to be the 'to' side it would need to be the log's fallthru predecessor or the higher-index member of a dir_both pair with a wholly matched -1 block; split blocks sit right before the log, so after compaction they always have the higher index and the fallthru place.  The only way left is a size log laid out after the log, which needs the could-not-read test before the switch in the source (not the reference's order).

### (2) exp_pr with the SMC base (a56_negp.py, p0, 80, 90, 95, 97, 99)

- Barrier on: expect IDENTICAL at p95 to p99, 0/7 at p90 and below (as src); `(int)r < 0` 0/7 at every p; `r != 0` 2/4 at every p.
- Barrier off: expect 1/7 (p95 to p99), 1/14 (p0, p90), 3/20 (p80); `(int)r < 0` 3/20 at every p; `r != 0` 5/17.
- So the new -1 structure doesn't touch exp_pr's alignment: they add, as attempt 48 found on the old base.

### (3) Attempt 55's list

- lab_devgl: an inner `switch (xb.type)` for arm 2 (50% at profile_estimate) was attempt 46's (14/204); not retried.  No new lever for arm 2's malloc block (needs >= 176 at bbro).
- exp_pr's bb13 share and lab_none's size store: nothing new to try beyond attempt 54's readings; not swept.
- pin_size re-read (src minus the pin): the reference copies the sum `mov ebx,esi` before the findFile(14) loop and keeps it in ebx across setPatchSlot / imgCfSize, and uses ebx for the first `files[x].size` load; without the pin the sum stays in esi.  The same picture as attempts 33 / 52; not swept.

### Don't retry (attempt 56)

- vol_fail by any case-23 spelling on the SMC bases (own -1, -1 before the log, nested, else, good path first, repeated test, ternary, a logging helper returning -1, a void log helper, a size-check helper in three return forms).
- vol_fail by giving the SMC test or another pred a conflicting edge to the join: cleanup splits that edge and removes fail anyway.
- exp_pr's spellings on the SMC base across the param (no interaction with the barrier).

### What to try next

- vol_fail: closed for natural code by four readings now (attempts 10, 31, 55, 56).  The only remaining structural route is the size log after the could-not-read log in layout (the r test ahead of the switch), which is not the reference's source order; leave the asm unless a different whole-loop structure turns up.
- Otherwise attempt 54's list stands (exp_pr's bb13 share, lab_none's size store), and attempt 55's for lab_devgl.

### Costs now (strict/loose, removed alone; 7 tricks, unchanged)

exp_pr 4/2 (`(int)r < 0` in its place 7/0), vol_fail 220/58 on src (7/1 on a55_smc.py's equal bases, every case-23 spelling the same), lab_devgl 57/14, exp_devgl 43/7, pin_size 82/40, lab_none 351/225 (as attempt 55).

## Attempt 57

Goal: the brief's structure-level search for the two loaders together (4 of the 7 tricks live there: exp_pr, vol_fail, lab_devgl in loadBlFiles, lab_none in loadConsoleBlFiles): one shared per-entry function or one loader with a mode flag, a per-entry helper both loops call, the static functions' order, a shared r-handling helper (attempt 50's notRead already covers the log alone: equal base).  src as of fc92709b, unchanged.  New scripts in `tools/wip/dehint/bdgen`, run with `python tools/wip/dehint/bdgen/a46run.py <script> [-k label]` on src/build.c: `a57lib.py` (shared: OFFS = the four loader hints, each removable; `cross(name, edits)`; `helpers(t)` cuts the defaultBl60 / loadXell / loadBl24 block out), `a57_base.py` (src and each hint off), `a57_order.py` (helper placement and order), `a57_merge.py` (the loaders as one `loadFiles(int console)` loop, rows `bl_*` / `con_*`; the per-entry `loadEntry(e, console)`, rows `ent_*`), `a57_ent.py` (a per-entry helper holding the switch and the could-not-read log), `a57_corder.py` (case order; `A57_CON=1` for console).  Scratch in build/bd/a46 (`-k` output) and build/bd/a57_corder*.txt (not kept).  Loose/strict lines, p99.

### Baseline (a57_base.py)

As attempt 56: src IDENTICAL; pr 2/4, bar 58/220, lab 14/57, none 4/8 (loadConsoleBlFiles), all four off 80/241.

### Static function order (a57_order.py, 48 rows)

- The three helpers moved as a block (static prototypes ahead of the loaders) to between the loaders, after loadConsoleBlFiles, the end of the file, or right after loadBaseFile; or reordered in place (dbx, xdb, bdx, bxd): **every placement is an equal base**, and each hint off costs exactly what it costs on src (pr 2/4, bar 58/220, lab 14/57, none 4/8, all 80/241).  The out-of-line functions keep their order (build.c has no -fno-toplevel-reorder; the output is in source order anyway), and the helpers' place changes neither einline's nor IPA's decisions.

### The loaders as one function with a mode flag (a57_merge.py)

- `static int loadFiles(int console)` holding the loop, both switches under `if (console)` inside the none test, r in the body or at the top, console's precheck shared or dropped, either switch first; `int loadBlFiles(void) { return loadFiles(0); }` and the same with 1 for console (16 rows).  ipa-cp clones loadFiles per constant and loadBlFiles' clone is inlined into its wrapper (loadBlFiles itself 137/187 with every hint), but the wrappers are tiny and IPA's small-function pass inlines them into buildFlash first, so the console clone has two callers (its wrapper and buildFlash), stays out of line as `loadFiles.constprop.6` (loadConsoleBlFiles is a `jmp` to it, buildFlash calls it directly) and buildFlash changes by 1000 lines: **11600 loose and up**.  The reference's buildFlash calls both loaders, so a one-function-plus-wrappers form is out without an inlining attribute (a trick).
- The per-entry work as `static uint32_t loadEntry(struct fileent *e, int console)` (both switches, `return r`), both loops calling it (4 rows): 522 loose and up (each loader 235 to 330): the arms' breaks become early returns, attempt 49's 317 for console alone, worse with both.

### A per-entry helper holding the switch and the log (a57_ent.py, 88 rows)

- The idea: attempts 45/46 put the reference's case arms at about 0.86 of the loop form's, which is what PRED_CALL on the none test's strnicmp edge gives (0.29 + 0.71 x 0.5 = 0.645 against 0.75).  A call in the guarded block brings that, and with the could-not-read log inside the helper (`if (r) { log; return -1; } return 0;`) the arms' breaks go to the r test rather than the return block, so they escape the early-return rule that made attempt 45's helpers (log outside) cost 95 and up.
- Return forms neg (-1 / 0), one (1 / 0), r (`if (r) log; return r;`), first (`if (!r) return 0;` first), each with the call nested in the none test or `&&`-joined to it, loadBlFiles only or both loaders, every hint subset: **112 loose and up** (r: loadBlFiles 112/241; neg, one, first 195 to 212).  pr and lab off cost nothing on these bases (their windows go with the structure), the barrier off adds 16.  Nested and `&&` call sites are identical; console through its own helper adds 172 and up.

### Case order on the loop form (a57_corder.py; 132 moves x 4 hint sets for loadBlFiles, 90 x 2 for console)

- Attempt 30 swept case order on the old helper form only.  loadBlFiles, every case block moved to every other place, with pr, bar or lab off: only swapping case 2 and the default is an equal base (IDENTICAL; pr 2/4, bar 58/220, lab 14/57 there); next, cases 1 and 22 swapped (4 loose with every hint, 6 / 18 with pr / lab off).  The barrier off is best with case 24 moved after case 2 (41/155) or case 2 before case 24 (41 + 4 in console), not under 41.
- loadConsoleBlFiles with lab_none off: every move is 4/8 at best (as src).  So the source's case order is the reference's (up to the default's place) and is not a lever.

### Don't retry (attempt 57)

- The static helpers' place or order in the file (equal bases).
- One loader with a mode parameter behind two wrappers (the wrappers are inlined into buildFlash; the console clone stays out of line), or a per-entry function with a mode parameter (early returns).
- A per-entry helper holding the switch and the could-not-read log, in any of the four return forms, nested or `&&`, for one loader or both (112 and up).
- Case order in either loader's switch.

### What to try next

- The structure-level list is covered: no whole-function arrangement of the two loaders found beats the current one, and on every equal base found the four loader hints cost what they cost on src.  Attempts 54 to 56's per-trick readings (exp_pr's bb13 share, vol_fail's crossjump rule, lab_devgl's arm-2 malloc block at bbro >= 176, lab_none's size store with a one-call loadBl24) stand as the exact conditions.
- Giving the none test's strnicmp edge PRED_CALL without a helper would need a call with side effects in the switch block at profile_estimate that is gone by expand; the reference's guarded block holds only the `e->type` load and the jump table, so nothing natural can be that call.

### Costs now (strict/loose, removed alone; 7 tricks, unchanged)

exp_pr 4/2 (`(int)r < 0` in its place 7/0), vol_fail 220/58 on src (7/1 on a55_smc.py's equal bases), lab_devgl 57/14, exp_devgl 43/7, pin_size 82/40, lab_none 351/225 (as attempt 56).

## Attempt 58

Goal: the brief's new angle: the *types of shared declarations* (fields of `xb` and `struct fileent` / `struct netfile`, and the return and parameter types of the functions build.c calls, in their headers) rather than of locals, each crossed with every hint off alone; for anything that moves, a check of every other object.  src as of 69fcd0cf.  New scripts in `tools/wip/dehint/bdgen`: `a58lib.py` (the runner: `python tools/wip/dehint/bdgen/a58lib.py <script.py> [-p 99] [-o "set;set"] [-k label]`; a script defines `V = {label: ({header: [(old, new)]}, [(old, new) for build.c])}`, header edits go to copies of src/*.h in build/bd/a58/ov/<label>/ put ahead of src on the include path, `-o` names the hint sets as bdhints names, default each alone), `a58_types.py` (31 shared-declaration types), `a58_cba.py` (fileent.size spellings and calcBlAreaSize's local types), `a58_ff.py` (findFile* return and loop types), `a58_ret.py` (build.c's own callees' return types, netfile-typed fields as uint32_t, `char *data`), `a58_none.py` (lab_none with loadBl24 / defaultBl60 return types, two-call and `||` bodies), and `a58_objs.sh <overlay dir> [build.c variant]` (every app object compiled with build.sh's flags and the overlay, compared with build/obj).  Scratch in build/bd/a58 (not kept).  Loose/strict lines, p99.

### What the reference fixes (objdump of xeBuild.exe)

- `glitch2mfg` is read as a dword into a register and tested (`mov edx,[..eb4]; test`), and written `mov dword [..],1`: a 4-byte field, so int and uint32_t are the only candidates, and they compile the same here (only zero tests).  No `_Bool` / uint8_t value range is possible.
- `xb.type`'s relational jumps are all `ja` / `jbe` (29 of them): it stays unsigned.
- findFile's inlined loops have a signed guard (`test eax,eax; jle`) on nFiles, and findFileOffset's on nFlashFiles (`jl` in one): both counts stay int.

### a58_types.py (31 types x 6 hint sets)

| Change | Result |
|---|---|
| fileent.data `unsigned char *`; netfile-typed smc / kv / kvAlt / smcConfig with a uint32_t size; glitch2mfg, glitch2 or fromConsole uint32_t; suGetCF/CG returning int; cbVerifySig uint32_t; smcSetLoad int (return or parameter); setPatchSlot void or int parameter; setFlashBuild uint32_t; log_printf int level; loadBinFile / loadLocalFile uint32_t | **equal bases** (IDENTICAL; every hint costs what it costs on src) |
| fileent.size int (or int32_t, signed) | **calcBlAreaSize matches without the pin**, but loadBlFiles 10/172, buildFlash 37/369, addUpdateBls, patchBlsResign, fixupPatchSet (loop-compare operand orders), and consoleinfo and keys differ |
| fileent.size long | loadFileCrc 70 and more on top |
| fileent.size unsigned long / size_t / unsigned | equal bases (useless conversions: no GIMPLE statement), pin 40/82 |
| fileent.type uint32_t | 462 (encodeBls 379) |
| fileent.offset int | 302 (addBlsToImage, addUpdateBls) |
| fileent.crc int | 50 |
| netfile.size uint32_t | buildFlash 22/314 |
| nFiles uint32_t / nFlashFiles uint32_t | 659 / 174 (the signed guards) |
| xb.type int | 30 (jle for jbe) |
| cbb int, seReplacesCf int | encodeBls 1/4, 0/2 |
| imgCfSize int | addUpdateBls 71 |
| getBeU16 unsigned int | 69 |
| findFile uint32_t | 697 |
| findFileOffset/findFileSize with a uint32_t parameter | 36 (the bodies' mixed compare) |
| loadBaseFile uint32_t | not inlined |

- No change touched exp_pr (2/4), lab_devgl (14/57), vol_fail (58/220), lab_none (225/351; 4/8 with the precheck too) or exp_devgl (7/43): they are probability, trace-priority and block-survival questions, and none of these types changes a predictor (the tests involved are zero tests, nonequal compares or already-unsigned ranges).

### pin_size: the conversion lever (a58_cba.py, a58_ff.py, dumps)

- fileent.size as int frees the pin because each inlined read gets a conversion statement `(unsigned int) load` in calcBlAreaSize.  Read off `-fdump-tree-optimized`: in src minus the pin the kit add is `size_41 = prephitmp_229 + size_254` (PRE's temporary has the lower version, so it comes first and IRA threads the sum with it: esi); with int sizes it is `size_48 = size_272 + prephitmp_278`.  The conversions consume SSA versions (including freed ones PRE would otherwise reuse), so the prephitmp is numbered after the size PHI.  That is attempt 35's operand-order tie, decided by numbering, as attempt 37's dead load had shown.
- The same through calcBlAreaSize's locals: `int size` 145, `int x` 79, `int xs` 2/2 (pin kept; 42 without), `unsigned long size` / `size_t size` equal bases.  An explicit `(int)` cast on a uint32_t field folds away.
- **findFileOffset and findFileSize returning `int`** (findFile already does): the inlined `return xb.files[i].offset` / `.size` are converted to the uint32_t sums at every JTAG, kit and retail call, and calcBlAreaSize then matches **without the pin** (`fofs_i`; dump: kit add `size_273 + prephitmp_282`).  findFileOffset alone or findFileSize alone: the pin still costs 40/82.  Their loop variables as uint32_t: 132 and 127.
- Other objects (a58_objs.sh): only image_write differs: `SWAP32_IMAGE_WRITE(findFileOffset(9))` with an int argument has arithmetic shifts.  `SWAP32_IMAGE_WRITE((uint32_t)findFileOffset(9))` matches; a separate `cf = findFileOffset(9); cf = SWAP32_IMAGE_WRITE(cf);` doesn't.  The cast is marked `TODO(prototype cast)`, as the repo does for prototype disagreements.
- On that base every other hint costs what it costs on src, and the param window is p95 to p99 (0/7 at p90 and with no param).  Landed: build.h, build.c (both definitions, the pin and its comment gone, a comment on the return types), image_write.c (the cast), build.sh (the param comment, which still said 96 to 98 fail: they have matched since attempt 49).

### Return types of build.c's own callees (a58_ret.py, a58_none.py)

- loadInputFile uint32_t (r is uint32_t): loadInputFile itself 47/181; checkBl uint32_t 390; extractSmcConfig uint32_t 10000+ (not inlined the same way); defaultBl60 uint32_t 115; loadXell uint32_t 70; loadBl24 uint32_t 42 (loadBlFiles 2/53 with every hint, 7/179 with the barrier off: the closest vol_fail number on the helper form, but still the size log's -1 plus a moved block); all three helpers uint32_t 119.
- lab_none on the two-call and `||` loadBl24 with every int / uint32_t pairing of defaultBl60 and loadBl24 (precheck and label on and off): nothing below src's 4/8 (two-call) or the `||` form's 66; the size store's place doesn't depend on these types.

### Don't retry (attempt 58)

- glitch2mfg, glitch2, fromConsole, cbb, seReplacesCf, xb.type, nFiles, nFlashFiles as other integer types; fileent.type, offset, crc, data; netfile.size; suGetCF/CG, cbVerifySig, smcSetLoad, setPatchSlot, setFlashBuild, log_printf, imgCfSize, getBeU16 signatures; findFile uint32_t (a58_types.py).
- fileent.size as int: it frees the pin too but moves six functions and two objects; findFile*'s int returns do the same job alone.
- Return types of loadInputFile, checkBl, extractSmcConfig, loadBinFile, loadLocalFile, defaultBl60, loadXell, loadBl24 for the loader tricks (a58_ret.py, a58_none.py).

### What to try next

- The conversion lever (an int-to-unsigned conversion that a natural type puts in the code, moving SSA numbering) is new to this file's notes as a *type* effect.  It only reaches tricks decided by SSA numbering or operand order, and of the six left none is: exp_pr (an alignment from the SE copy's probability), exp_devgl (tree-sink's 75% rule), lab_devgl and lab_none (bbro trace priorities; lab_none's one-call residue is the alias oracle's store order), vol_fail (block survival).  If any of them ever comes down to an operand order or IRA tie, try types first.
- Otherwise attempts 54 to 57's per-trick readings stand.

### Costs now (strict/loose, removed alone; 6 tricks)

exp_pr 4/2 (`(int)r < 0` in its place 7/0), vol_fail 220/58 (7/1 on a55_smc.py's equal bases), lab_devgl 57/14, exp_devgl 43/7, lab_none 351/225 (8/4 with the precheck).

## Attempt 59

Goal (scripts written against cf9d40fe's src, before the landing; their edits no longer apply to the new src): test attempt 58's conclusion (the six left are probability / trace-priority / block-survival / alias-oracle questions) with type- and helper-level levers on the things it named, starting with lab_none's one-call loadBl24 residue (the size store's place, attempt 54's alias reading).  src as of cf9d40fe.  New scripts in `tools/wip/dehint/bdgen`, run with `python tools/wip/dehint/bdgen/a58lib.py <script> [-p ..] [-o "set;set"] [-k label]`: `a59_store.py` (defaultBl60's copy forms x two-call / one-call loadBl24 x lab_none's precheck and label kept / off), `a59_mm.py` (the memmove base x one-call body x arm 2 through loadBl24 x memmove in cases 1 / 22, across hint sets and the param), `a59_mmx.py` (on the landed base, every other memcpy in build.c as memmove, x each remaining hint off).  Scratch in build/bd/a59 (`mc_N/`, `mm_N/`: full `-fdump-tree-all -fdump-ipa-all` of the memcpy and memmove forms without lab_none; not kept).  Loose/strict lines, p99.

### a59_store.py: defaultBl60's copy forms (`_N` = precheck and cold label off)

| defaultBl60 | two-call loadBl24 | `_N` | one-call `||` (either) |
|---|---|---|---|
| src (`memcpy(e->data, defBl60, 0x60)`) | IDENTICAL | 4/8 | 66/125 (the size store) |
| malloc into a local `p`, copy from `p` | IDENTICAL | 4/8 | 66 |
| `memcpy(.., e->size)` | IDENTICAL | 4/8 | 66 |
| `sizeof(defBl60)` everywhere | IDENTICAL | 4/8 | 66 |
| `(char *)` destination cast | IDENTICAL | 4/8 | 66 |
| byte loop | 470 | 472 | 517 |
| `return setFileData(e, defBl60, 0x60);` (calloc) | 49 | 49 | 75 |
| **`memmove`** | IDENTICAL | **IDENTICAL** | 66 |

- The alias-oracle line itself didn't move: the one-call body is 66 loose with every copy form (the destination pointer's type, a typed local or a char cast don't change points-to: it is {HEAP} from malloc whatever its type, and the store is a decl ref into xb).  The store-order route to lab_none stays closed.
- But **memmove frees lab_none on the two-call form**, by another route.

### Why memmove works (dumps in build/bd/a59)

- memmove stays a call (`memmove (_5, &defBl60, 96)`) through every pass up to dce3, then is folded to memcpy once PTA can tell the destination (malloc) and source (a const decl) apart; from there the code is memcpy's (rep movs), so the object is byte-identical.
- Before that the inline summaries see it as a plain call: einline's `loadBl24 -> defaultBl60.isra.0` growth is **6 instead of 10**, IPA sizes defaultBl60.isra.0 at **14 instead of 18** and loadBl24 at **32 instead of 40**.  (memcpy is costed as a builtin with a known expansion; memmove isn't.)
- That reorders IPA's small-function inliner (-.074i.inline): with memcpy it inlines loadXell (29) into loadConsoleBlFiles, then loadBl24 (40); with memmove loadBl24 (32) goes first, then loadXell.  The inline order changes console's block numbering and the profile scaling of the inlined bodies, and bb-reorder then lays out the r = 1 / return blocks as the reference does: no cold label and no `nFiles <= 1` precheck needed.  (Not read further: which bbro tie or trace start flips.  Attempt 51's window analysis was of the precheck route.)
- So this is an inline-order lever, not a probability or alias one: attempt 58's "probabilities, trace priorities, block survival" verdict was right about what decides each trick, but the *inputs* to those (block numbering, which inlined body scales which profile) also move with IPA's inline order, which a callee's size estimate decides.

### a59_mm.py / a59_mmx.py

- On the memmove base, each remaining hint off costs what it did on src: exp_pr 2/4, vol_fail 58/220, exp_devgl 7/43; lab_devgl **14/34** (57 strict before, the same 14 loose lines).  The param window is unchanged: IDENTICAL at p95 / p97 / p99, 0/7 at p0 and p90.
- One-call loadBl24 on the memmove base: 66 (the size store again); arm 2 through loadBl24: 65; both: 63.  The two-call and written-out borderline shapes stay.
- memmove in cases 1 and 22 too: IDENTICAL, every hint the same cost; landed for consistency (the three built-in fallbacks read alike).
- The other memcpy sites as memmove (a59_mmx.py): setFileData equal base; appendAddonPatches (either copy) 4 to 14 in that function; extractSmcConfig's sector copy 158; patchBlsBlmod 12.  None touches the remaining hints.

### Landed

src/build.c: defaultBl60 and cases 1 / 22 use memmove (Borderline comment on defaultBl60), loadConsoleBlFiles loses the precheck, the cold label and its comment.  bdhints.py: lab_none gone.  README.md: build 5 tricks.  Full build SHA256 10dac648..1c.

### Don't retry (attempt 59)

- lab_none's one-call loadBl24 by defaultBl60's copy form or types (typed local, `e->size` as length, sizeof, char cast, byte loop, setFileData, memmove): the size store stays, 66 and up.
- memmove at the other memcpy sites in build.c for the remaining hints (a59_mmx.py).

### What to try next

- The inline-size / inline-order lever is new: a callee's size estimate decides IPA's inline order, which moves block numbering and profile scaling in the caller without changing code.  Try it on lab_devgl (loadBlFiles inlines loadBl24, loadXell and defaultBl60 by IPA too; what order does it take them in, and does any size change, e.g. a log_printf in loadXell, a strcpy/strcat vs a sprintf in loadBaseFile/loadBinFile, move arm 2's malloc block's bbro frequency or the r = 1 block's trace position?) and on vol_fail (its 58 came from vrp1's jump threads, which depend on the inlined CFG).  Also exp_devgl: buildFlash's IPA inline order (patchConsoleBlmod, the loaders) could change the profile around the devgl test.
- Otherwise attempts 54 to 58's per-trick readings stand.

### Costs now (strict/loose, removed alone; 5 tricks)

exp_pr 4/2 (`(int)r < 0` in its place 7/0), vol_fail 220/58 (7/1 on a55_smc.py's equal bases, not re-checked on the memmove base), lab_devgl 34/14, exp_devgl 43/7.

## Attempt 60

Goal: the brief's inline-order / estimate lever (attempt 59) on the four in-source tricks left (exp_pr, vol_fail, lab_devgl, exp_devgl), plus attempt 55's SMC equal base re-swept on the memmove src.  src as of 862bda0c.  New scripts in `tools/wip/dehint/bdgen`, run with `python tools/wip/dehint/bdgen/a60lib.py <script> [-p ..] [-o "set;set"] [-f substr] [-k label]` (a58lib's runner without header overlays; edits are `(old, new[, count])` lists or callables; a script may give per-label hint sets in `SETS`): `a60_est.py` (24 code-neutral or nearly neutral edits x each hint off), `a60_ub.py` (useBuiltIn: 6 bodies x 4 signatures x 5 site sets, devgl label off), `a60_mc.py` (the a60_ub matches x the SMC `if` / `end` forms x each other hint off), `a60_rest.py` (on the landed src: the still-applicable edits and useBuiltIn's forms, for exp_pr / exp_devgl, with and without `(int)r < 0`).  Scratch in build/bd/a60 (`src/`, `new/`, `ubmm/`: ipa-inline / einline dumps; `ub_nl.c` and its alignments dump; not kept).  Loose/strict lines, p99.

### IPA inline order on 862bda0c (-fdump-ipa-inline-details)

- Out of line for size reasons: loadBaseFile, loadBinFile, loadInputFile, loadLocalFile into the loaders (large-stack-frame-growth: their 0x400-byte paths).  loadXell is fnsplit (loadXell.part.2, 9) and loadBl24 too (loadBl24.part.1, 7).
- IPA small-function order, with sizes: loadBl24 (32) -> loadConsoleBlFiles, loadXell (29) -> loadConsoleBlFiles, loadBl24 -> loadBlFiles, defaultBl60.isra (14) -> loadBlFiles (the written-out second arm's two calls, line 1351 then 1349), loadXell -> loadBlFiles.  buildFlash takes patchConsoleBlmod (18) early in the queue, then makeTimestamp's copies late.
- On the landed src the loadBlFiles order is loadBl24, loadXell, then the two defaultBl60 calls (loadXell moved ahead of them); useBuiltIn is not in the IPA list at all: einline takes its isra clone into loadBlFiles before profile_estimate (both with memcpy and with memmove inside).

### a60_est.py (estimate edits on 862bda0c x each hint off)

| Edit | Result |
|---|---|
| memcpy back in case 1, case 22 or both; `uint8_t salt[16] = {0}` for the memset; useNandData for kv / kvAlt (both loaders); the could-not-read log as `notRead` (int or void); loadXell nested or with an `r` local; defaultBl60 through a `p` local | **equal bases** (IDENTICAL; every hint costs what it does on src) |
| SMC failure `if` / `end` forms (attempt 55) | equal bases; vol_fail off **1/7** again (58/220 on src): the memmove src didn't change attempt 55's picture |
| `struct fileent f = {0}` in buildFlash | 96 (buildFlash) |
| patchConsoleBlmod written into buildFlash / with the test the other way | 66 / 28 |
| useNandData for smc too | 3/29 (console) |
| loadXell's retail test as `< BUILD_JTAG` | 72 |
| loadBaseFile's baseDir test as an early return | 42 |
| defaultBl60's size store after the copy | 6 |
| **useBuiltIn (memmove) for cases 1 and 22** | **loadBlFiles 0 loose / 50 strict with the label kept or off**: the layout is the reference's without the label; the one difference is a `.p2align` on the r = 1 block (`mov edi,1; jmp`), the rest displacements |

- The alignment, from `-fdump-rtl-alignments` of that form minus the label: the r = 1 block (final bb 91) has a fallthru pred of frequency 0 (the retest) and branch frequency 115 > freq_max / 100 = 9550 / 100, so compute_alignments' "internal loop alignment" rule fires (branch > 4 x fallthru).  The reference's r = 1 block must have branch frequency <= 95.  Attempt 55's bbro reading (r = 1 on plain keys needs >= 96 to beat block 15 [95]) says there's no frequency window between bbro and the alignment on that route, so the layout has to come some other way.

### a60_ub.py: useBuiltIn's forms (label off)

- With useBuiltIn in **one** case only (1 or 22), any body (plain, nested, `r` local, assignment in the test, `p` local; int / size_t / void * signatures): **IDENTICAL without the label**.  `uint32_t` return: 14/34 (as without the helper).
- In both cases: the memmove bodies are 0 loose / 50 strict (the alignment above); the **memcpy body is IDENTICAL** (also with size_t / int sizes).
- defaultBl60 through useBuiltIn (sites `b`, `12b`): 14/34 and up, and with memcpy console's 4/8 (lab_none) comes back.  So defaultBl60 keeps its own memmove copy.
- Not read in the dumps: which profile_estimate frequency the einline'd helper moves (its `return 1` / `return 0` arms and return PHI become part of loadBlFiles' CFG, where the source had `r = 1; break;`), and why memcpy vs memmove inside the helper moves the r = 1 block across 95 (both are einline'd, so the difference is in what the early passes and profile_estimate make of the call: memmove is an ordinary call until it folds, memcpy a builtin with a known expansion).

### a60_mc.py: the matches x the SMC forms x each other hint

| Base (label off) | all kept | exp_pr off | vol_fail off | exp_devgl off |
|---|---|---|---|---|
| useBuiltIn memcpy, cases 1 + 22 (`mc_12`, also int / size_t sizes) | IDENTICAL | 2/4 | 59/219 | 7/43 |
| `mc_12` + SMC `if` or `end` form | IDENTICAL | 2/4 | **IDENTICAL** | 7/43 |
| useBuiltIn in case 1 or 22 only (any body) + SMC `if` / `end` | IDENTICAL | 2/4 | 1/7 | 7/43 |

- So on the two-case memcpy helper the SMC `end` form needs no barrier: the size log's own -1 line (attempts 10 / 31 / 55 / 56's crossjump rule) is gone.  Not read in the dumps (which jump2 crossjump or block index order changed); the helper's inlined blocks and their `return 1` joins change the CFG ahead of the SMC blocks, the kind of index / pred change attempt 56 said the 1/7 depended on.

### Landed

src/build.c: `useBuiltIn` (memcpy) before defaultBl60, cases 1 and 22 call it (memmove gone from them); the devgl hot label and its comment gone; case 2's SMC failure `if (!e->offset) goto fail; break;` and `fail: r = -1; break;` after the default case, the asm and its comment gone.  defaultBl60's Borderline comment updated (memmove now only there; it doesn't use useBuiltIn).  bdhints.py: lab_devgl and vol_fail gone.  README.md: build 3 tricks.  IDENTICAL at p95 / p97 / p99 (0/7 at p0 and p90).  Full build SHA256 10dac648..1c.

### a60_rest.py (on the landed src)

- Equal bases again: salt `= {0}`, useNandData kv / kvAlt, notRead (both forms), loadXell nested / `r`, defaultBl60's `p` local, **useBuiltIn with memmove** (IDENTICAL now, on the `end` SMC form), useBuiltIn nested.  On each, exp_pr 2/4, `(int)r < 0` 0/7, exp_devgl 7/43: unchanged.
- useBuiltIn returning uint32_t 15/41; defaultBl60 with memcpy 14/34 + console 4/8; patchConsoleBlmod with the test the other way 28.

### Don't retry (attempt 60)

- The a60_est.py edits listed as equal bases, for exp_pr / exp_devgl (no change on either the old or the landed src).
- defaultBl60 through useBuiltIn, or with memcpy (lab_none and the devgl layout come back).
- useBuiltIn returning uint32_t.
- `struct fileent f = {0}` and patchConsoleBlmod's shapes for exp_devgl (28 and up).

### What to try next

- exp_pr: still the SE copy's jmp block (needs frequency 1, has 2) and the no-key log's `.p2align`; `(int)r < 0` stays 0/7.  The einline'd-helper lever that freed lab_devgl changes profile_estimate's input itself; a helper in the 5..21 arm that einline takes (so its arms enter loadBlFiles' own profile) is the untried variant of attempt 50's loadUpdateBl / signature helpers (those were IPA-inlined calls with their own profile, 85 and up).  Check which bodies einline accepts (growth <= 14, `-fdump-tree-einline-details`) before scoring.
- exp_devgl: attempt 53's einline rules still stand; nothing in buildFlash's IPA order moved it.
- If the param ever goes (exp_pr gone), check exp_devgl at gcc's default 90 (it matched there in attempt 42).

### Costs now (strict/loose, removed alone; 3 tricks)

exp_pr 4/2 (`(int)r < 0` in its place 7/0), exp_devgl 43/7; the param only exists for exp_pr (0/7 at p0 and p90).

## Attempt 61

Goal: the brief's two leads on the 3 tricks left: (a) exp_pr's alignment through the inline-order / estimate / helper levers of attempts 58 to 60 (does any of them move the SE block below 6.5, measured directly), with `r != 0` and `(int)r < 0`; (b) exp_devgl through a fuse helper that IPA (not einline) inlines.  src as of a14fd5c7, unchanged.  New scripts in `tools/wip/dehint/bdgen`: `a61_freq.py <variant.c> [-p N] [-f fn]` (max block, the 'E' test, no-key and sig-failed blocks' frequencies at profile_estimate, fixup_cfg4 (the first dump after IPA inlining), vrp1 and optimized), `a61_da.py <variant.c> <fn> [out.s]` (one function's `-S -dA` output), `a61_semeas.py <a60-style script> [-x] [-p N] [-f substr]` (for each variant, with the tail's expect replaced by `(int)r < 0` unless `-x`: the final frequencies of the three blocks after `cmpb $69` (SE, its tail-test copy, the jmp block) and of the no-key log blocks, and which no-key block is aligned), `a61_diag.py` (diagnostic: the checkBl r test under an expect at low params; not natural), `a61_secb.py` (the SE arm with its own checkBl call; run with a60lib.py).  Scratch in build/bd/a61 (not kept).  Loose/strict lines in loadBlFiles, p99.

### exp_pr's chain, final RTL (a61_semeas.py on src)

- Without the expect (`(int)r < 0`): block 109 (SE stores + its checkBl copy) freq 7, block 110 (the SE copy of the tail's `xb.type <= 5` test) 4, block 111 (its `jmp`) 2, block 112 (no-key log copy) 14, not aligned.  With the expect: 7 / 4 / **1** / 14, aligned (14 > 10 x 1).
- 110 is RDIV(7 x 5000 / 10000) = RDIV(3.5) = 4: the checkBl r test is 50/50 (no predictor) and 3.5 rounds up.  So the chain closes with any of: SE <= 6, the checkBl r test's continue edge under 50% by any amount (110 = 3, then 111 = RDIV(3 x 49.8%) = 1), or P(>5) on the copy under 37.5% (attempt 48's figure).
- a61_freq.py: the SE chain's frequencies are the same at profile_estimate and fixup_cfg4 ('E' test 23, no-key 14, sig-failed 41); the header is the 10000 max both times.  IPA inlining adds callee blocks scaled into their call blocks and the rebuild recomputes from the same edge probabilities, so no IPA-inlined callee can move loadBlFiles' own blocks (only an inlined *loop* hotter than the header would renormalise them, and none of the callees has one).
- **a60_est.py's and a60_rest.py's 24 edits** (salt `= {0}`, `struct fileent f = {0}`, patchConsoleBlmod inline or reversed, useNandData, notRead, loadXell nested / `r` / range, defaultBl60 local / memcpy / late store, useBuiltIn memmove / uint32_t / nested, the loadBlFiles placement): **every one is 7 / 4 / 2 / 14** (x_range only renumbers the blocks).  The estimate / inline-order family doesn't reach exp_pr.

### The SE arm with its own checkBl call (a61_secb.py)

- `if (type == 9 && S && E) { stores; r = checkBl(e->data, e->size, 14 (or type), e->crc); } else r = checkBl(e->data, e->size, type, e->crc);`: the SE block now holds a call, so the 'E' test's SE edge gets PRED_CALL as well as nonequal: 13.7%, SE = 5.6.  Final chain **6 / 3 / 1**, the no-key copy (11) aligned, exactly what exp_pr needs.
- But the else block (the usual checkBl) is dominated by the type == 9 test and doesn't post-dominate it, so the test's false edge gets PRED_CALL too: type == 9 is 48.8% instead of 28%.  loadBlFiles is **124 loose / 210 strict** with every tail spelling (expect kept, `r`, `r != 0`, `(int)r < 0`; `14` or `type` as the argument).  The instruction multiset is the reference's but for one `test; jne` and the padding: the loss is layout (the 5 / 17 / 11 tests, the pub1bl and signature blocks and the type-11 test placed in line).
- Diagnostic (not natural): an extern call in the S test's block cancels the type == 9 test's PRED_CALL (28.0% again), and loadBlFiles still differs in the same region (the second call site's CFG changes vrp1's threads into the 5/17/11 blocks).  So the route isn't a near miss even with the type == 9 probability restored.
- Ways to keep PRED_CALL off the type == 9 test (the else block reached from outside that test, e.g. the CG fallback's success or case 6 jumping to a shared checkBl) need gotos or change case 6's and the CG arm's own predictions; not built.

### exp_devgl

- Re-read attempt 53's einline rules against gcc 6's want_early_inline_function_p and cgraph_edge::maybe_hot_p: no call-free helper is refused (at einline every edge frequency is CGRAPH_FREQ_BASE, and a node is EXECUTED_ONCE only for main, noreturn or a cold/hot attribute).  The early-return predictor in a call-holding helper fires on every edge to a return block that isn't the test's next block, unless the test is already predicted by NULL / CONST / NEGATIVE_RETURN (CONST_RETURN only for constants other than 0 and 1), so a memset-holding helper's JTAG edge can't keep 28% (attempt 53's dret2).  build.c has no predicate helper that does the kit-type test with a call (isUpdateBl, blmodMissing checked).  Nothing scored.

### Don't retry (attempt 61)

- Inline-size / inline-order / helper edits for exp_pr (all 24 of a60_est / a60_rest): the SE chain is decided at profile_estimate and IPA doesn't change it.
- The SE arm with its own checkBl call, any argument and tail spelling (124 loose), and cancelling the type == 9 test's PRED_CALL with a call in the S test's block (still the 5/17/11 layout).
- Expect-at-low-param diagnostics of the checkBl r test (a61_diag.py): the param also moves other functions and the expect changes the test's code; read the -dA frequencies instead.

### What to try next

- exp_pr now has three exact closing conditions on the final chain (above): SE <= 6, the checkBl r test's continue edge a hair under 50%, or the copy's P(>5) under 37.5%.  The second is new: any predictor, however weak, on `r = checkBl(..); if (r) break;` toward the break (a call in the r == 0 side's immediate block, dominated by the test, or an opposing pair whose DS lands just under 50%) would do it, as long as it leaves the non-SE path's layout (the no-key log has to stay at 11 or more).  None is in the reference's code there (the r == 0 side's next block is the 5 / 17 / 11 test).
- exp_devgl: unchanged since attempt 53.

### Costs now (strict/loose, removed alone; 3 tricks, unchanged)

exp_pr 4/2 (`(int)r < 0` in its place 7/0), exp_devgl 43/7; the param only exists for exp_pr (0/7 at p0 and p90).

## Attempt 62

Goal: attempt 61's lead (give the checkBl result test in loadBlFiles' 5..21 arm a predictor through checkBl's return type or the test's form), its other two closing conditions, and the param on its own.  src as of d3e56593, unchanged.  New scripts in `tools/wip/dehint/bdgen`: `a62_semeas.py` (a61_semeas.py plus the SUCC probabilities of the SE copy's tail test; `python tools/wip/dehint/bdgen/a62_semeas.py <script> [-x] [-p N] [-f substr]`), `a62_ck.py` (forms of the checkBl result test and the r local's type, with each tail spelling), `a62_ret.py` (checkBl's return / local types, static checkBl), `a62_s.py` (S / Xc at the default param: diagnostics and signature-block forms), `a62_diag.py` (13 switch targets; not natural).  Score with `python tools/wip/dehint/bdgen/a60lib.py <script> [-p 0|99] -o "-" [-f substr]`.  Scratch in build/bd/a62 (not kept: `ref_lbf.txt` reference disassembly, `p90.s`..`p95.s` -dA output).  Loose/strict lines.

### Which side of the checkBl test has to rise

- Final -dA (src, `(int)r < 0` tail): block 109 (SE stores + checkBl copy) freq 7, SUCC 61 [50%] (the break, a loop exit by then) and 110 [50%] (r == 0, the copy of the tail test).  So the chain needs **P(r == 0) < 50%**: the break side up.  attempt 61's "continue edge under 50%" means that.
- Predictors that would do it on `if (r) break;`: TAKEN towards r != 0.  Opcode positive says values tend to be positive (`x < 0` / `x <= 0` unlikely), so with checkBl's -1 / -2 / -3 failures it always points at r == 0.  PRED_CALL would need a call in the r == 0 side's first block (the 5 / 17 / 11 test: none in the reference).  Pointer, loop exit, early return and negative return don't fit (r is an integer, the break isn't a loop exit or a return at profile_estimate, checkBl isn't inlined).  So no natural test form closes it, and the measurements agree:

| Variant (a62_ck.py, a62_ret.py) | SE / copy / jmp, no-key | Score (p99, all hints kept unless noted) |
|---|---|---|
| src, `r != 0`, `if ((r = checkBl(..)))`, `!= 0` in the condition | 7 / 4 / 2, 14 not aligned | equal (src) |
| checkBl test `(int)r < 0`, `(int)r <= -1` | 7 / **5** / 2, 21 aligned | 215/386 (tail `r`), 215/382 + displ (tail `(int)r < 0`) |
| `int r` loop local | 7 / 4 / 2 | 158/455 (as attempt 46's `int r` 117+) |
| `int r` + `r < 0` at the checkBl test | 7 / 5 / 2 | 232 to 244 loose |
| checkBl returning long / unsigned long / uint32_t (with a uint32_t local) / int32_t / ssize_t | 7 / 4 / 2 | not scored (no change in the chain; uint32_t was 390 in attempt 58) |
| `static int checkBl` | 7 / 4 / 2 | 457/721 (local calling convention, every caller moves) |

### The param on its own (exp_pr kept, gcc's default 90)

- The param exists only for exp_pr, and exp_devgl matched at 90 in attempt 42, so exp_pr's expect working at 90 would free one trick.  The -dA chain with the expect kept (a62_semeas.py -x): p90 copy SUCC 61.9% / **38.1%** (>5, the jmp block 111 = RDIV(4 x 0.381) = 2); p91 37.4% (111 = 1, aligned); p92 36.7%, p93 36.0%, p94 35.3%, p95 34.6%.  The threshold is 37.5% (4 x P < 1.5).
- Attempt 18's joiner formula fits: P(<=5) = Xc p (1 - q) / (Xc - S) = 149 x 0.5 x 0.9 / 108 = 62.1% (61.9% read).  At q = 10% it needs Xc / (Xc - S) >= 1.389, i.e. **S / Xc >= 0.28** (S 41 -> 42 at Xc 149).  It is 0.275 (real 0.272 = Psig 0.64 x Pk 0.85 x Pf 0.50, rounded up).  Diagnostics confirm it: the pub1bl test under an expect (Pk 90%) gives 36.9% / jmp 1, but the no-key log falls to 10 (needs >= 11); the verify under an expect (Pf 90%) gives 11.2%.
- Natural values of the three factors (attempt 19's lists, rechecked at profile_estimate on src with bdpred.py): Psig is 50% (5|17 packed) then nonequal 28%, whatever the order of the three compares (5,11,17 / 11,5,17 / 17,5,11 give the same chain); Pk is the pointer 85% (`!= NULL` the same; calls on both arms cancel); Pf is 50% (calls on both arms; `== 0`, `r = -1` before the log the same).  The next value up for any factor is a whole heuristic away: Pf 71% (the passed log out of the first block; diagnostic with a dead `else if (xb.pub1bl)`) costs 29/104 with the param gone, and its chain doesn't even close (46.4%: the dead test adds its own thread).  The window Pk in [0.865, 0.885] (S up, no-key still >= 11) would need a second predictor of 53% to 57% on the pub1bl test; gcc 6 has none that weak.
- So the param needs +2% on the signature-failed share and the heuristics move it in steps of 20% or more.  Recorded as the cheapest-looking target so far, not as a lead: nothing natural gives a 2% step.

### SE <= 6 (13 switch targets, diagnostic)

- The SE block is 7162 / 12 x 0.5 x 0.28^3 = 6.55 and needs < 6.5.  The 12 is the switch's distinct targets (gcc 6 splits a switch's probability evenly over its edges).  Diagnostic `case 26: break;` or `case 0: break;` (13 targets; behaviour change: no "unhandled" log): SE 6, copy 3, jmp 1, no-key 13 aligned, the chain closes.  But the reference's jump table (.rdata 0xf50, 28 entries for 0..27) has exactly 12 distinct targets, with 0 and 26 on the default.  So a 13th target has to be merged into an existing one after profile_estimate.  A copy of the default log as `case 26:` isn't merged (60/329 at p0 and p99, and every other block scales by 12/13).
- The other factors are fixed: the loop test is first-match loop exit 95.5% (two exits), the none test 75% (two 50% tests, no call in the switch block), the 0.5 at the fallback join's `if (r) break;` and the three nonequal SE tests.

### Don't retry (attempt 62)

- Predictors on the checkBl result test in loadBlFiles (any compare form, `int r`, checkBl's return type, static checkBl): the side that has to rise is the break's, and opcode positive / call / pointer can't point there with negative failure codes.
- Signature-test compare order (5/17/11 in any order), `xb.pub1bl != NULL`, `cbVerifySig(..) == 0`, `r = -1` before the failed log: no change to S / Xc.
- An extra switch target for SE <= 6: the reference has 12; a duplicated default case isn't merged back.

### What to try next

- The param alone is now a 2% problem: S / Xc from 0.275 to 0.28 at the default 90 (or Xc down by 3 with S fixed).  Any natural change to the signature block or to the flows into the tail test X that moves one of them by a little (not a whole heuristic step) is worth `a62_semeas.py -x -p 90` first (it must show the copy's >5 edge under 37.5%, no-key >= 11 and aligned), then `a60lib.py -p 0`.  Watch for a change that moves the integer roundings: S is 40.53 real (rounds to 41) and needs to round to 42.
- exp_pr itself: the three conditions of attempt 61 stand, each now with its blocking reason (above and attempt 61).
- exp_devgl: unchanged since attempt 53.

### Costs now (strict/loose, removed alone; 3 tricks, unchanged)

exp_pr 4/2 (`(int)r < 0` in its place 7/0), exp_devgl 43/7; the param only exists for exp_pr (0/7 at p0 and p90, IDENTICAL at p95 / p97 / p99; p91 to p94 not scored).

## Attempt 63

Goal: the brief's two targets: (A) the param on its own (exp_pr kept, gcc's default 90), by moving one factor of the signature-failed share S / Xc a little; (B) exp_pr and the param together.  src as of a17c6183, unchanged.  New scripts in `tools/wip/dehint/bdgen`: `a63_sf.py` (attempt 47's a47_sigfail.py forms on the current src), `a63_sf2.py` (the `<= 5` exit in the failed arm: 4 arm forms x 4 tails x the setFlashBuild argument), `a63_misc.py` (11 natural edits of the 5..21 arm not in a62_s.py), `a63_diff.py` (`python tools/wip/dehint/bdgen/a63_diff.py <script> <label> [fn] [-p N]`: loose unified diff of one function against the reference).  Chains with `a62_semeas.py <script> -x -p 90`, scores with `a60lib.py <script> -p 0 -o "-"`.  Scratch in build/bd/a63 (not kept: `-dA` output of src at p90 / p99 and of s1brk, vrp1 dumps of both).  Loose/strict lines, no param unless said.

### The joiner update in integers (vrp1 dump, `-details-blocks`, p90)

- At vrp1 the tail test X is block 26 (freq 149), its preds 124 (non-signature types, 54), 24 (passed, 41), 25 (no-key, 14) and 23 (failed, S = 41, r = -1); T (`if (r) goto fail`, the expect) is 27 (freq 75, 10% to fail).  Four threads are registered, the failed edge's first (`Threaded jump 23 --> 26`), then the three r = 0 edges into one copy.  The SE path isn't separate yet: at vrp1 the type-9 paths (15 / 16 / 17 -> 18) get their own checkBl copy and join the type-11 test, so the SE flow is part of X's 149.
- gcc 6 converts frequencies to counts for the path (freqs_to_counts_path: block freq x 10000, edges by probability).  For the failed path (23 -> 26 joiner -> 27 -> 111) compute_path_counts scales the joiner edge by S / freq26 (74.5 x 41 / 149 = 20.5), the normal edge 27 -> 111 isn't scaled (75 x 10% = 7.5), and the path takes the minimum, 7.5; update_profile takes 41 off block 26 and 7.5 off 26 -> 27, and the probabilities are recomputed from those counts.  So the copy the other three edges get has **P(>5) = (freq26 x (1 - p) - S + freq27 x q) / (freq26 - S) = (74.5 - 41 + 7.5) / 108 = 38.0%** (38.1% read; post-vrp1 blocks 130 / 132: 17.5% / 61.9%).  It needs < 37.5%: numerator under 40.5, i.e. S = 42 (37.4%) or freq26 <= 146 with S at 41.  Done in the other order (r = 0 edges first) it would be 50%.
- S is the failed log block's own frequency (40.53, already rounded up), freq26 and freq27 X's and T's (149.07, 74.5 -> 75).  The ratio S / freq26 is Psig x Pk x Pf whatever the flow into the arm, so rounding can't supply the missing 2.4% (S would need 41.5 real), and every factor takes only fixed values: Psig 0.5 (one packed or switch test), 0.627 (three separate tests) or 0.64 (any 2 + 1 grouping: `a || (b || c)` keeps `a` alone because a TRUTH_OR operand isn't simple for fold_truth_andor, and gives 0.28 + 0.72 x 0.5, the same); Pk 69.8 / 85 / 93.3; Pf 29 / 50 / 71.  The DS pairs that land near 50 (call 71 + nonequal 28 = 48.8, positive 73 + call 29 = 51.8, const return + early return 56.5) each need a predictor kind the test can't get (no opcode heuristic for `_66 != 0` or a zero test, no return on any of these paths).  p (X itself, `xb.type <= 5`) would need only 50.6%, but X gets no opcode heuristic and neither arm's first block can hold a call.
- So target A has no natural route on this CFG: it needs a second r != 0 flow into X (none is behaviour-preserving: checkBl's or the load's failure would reach `fail` and lose its -2 / -3 in the log) or r = 0 flow that leaves the signature region without X (the reference sends the passed, no-key and non-signature paths through X: final block 77's preds 76, 105, 112).

### A second closing condition for the alignment

- compute_alignments aligns the no-key copy (final bb 112, no fallthru, branch freq 14 < 100) only by `freq > 10 x prev_bb freq`; prev_bb is the SE copy's jmp block 111.  So besides 111 <= 1, **112 >= 21 with 111 at 2** closes it.  112 is the no-key flow (95 x (1 - Pk)); Pk = 69.8% (pointer 85 with only the verify block's PRED_CALL, the no-key arm's call not counted) gives 29.  That needs the no-key log block not dominated by the pub1bl test.  `a63_misc.py`'s `ver_flat` (`if (xb.pub1bl && !cbVerifySig(..)) {fail} else if (xb.pub1bl) passed; else no-key`) gets exactly that: no-key 29, **aligned**, with P(>5) 48.5%, but the second pub1bl test is a real reload and test after the verify call and the failed / passed blocks move: 57 / 127.
- No form with one pub1bl test can do it (the dest block is scanned whole, a label doesn't split it, and nothing else reaches the no-key log).

### Target B by the failed arm's own `<= 5` exit (a63_sf.py, a63_sf2.py)

- Attempt 14 / 47's form (`log; if (xb.type <= BUILD_DEVGL16) goto fail; r = -1;`, tail `if (xb.type <= 5) break; if (type == 14) setFlashBuild(..); break;`) has no r test left, so exp_pr and the param would both go.  On the current src: **22 / 71** in loadBlFiles (the other functions only move by call displacements), with every arm form (-1 before / after the test, `if (> 5) r = -1; else goto fail;`) and either setFlashBuild argument; the `&&` / nested kit tails 39, `type == 14 &&` first 79.
- vrp1 registers exactly the same threads as src (`Registering jump thread` lists identical).  The residue is layout: the signature strings' .rdata order (the failed log expanded first), the sig-failed setFlashBuild copy reading `e->data` through the IV (`mov eax,[ebx]`, attempt 11's ivopts line), no duplicate of the pub1bl test and no-key log on the type-11 path, an extra `test edi,edi; jne` after a checkBl.
- And it can't close the alignment chain at all: with no T there is no joiner thread on X, so both copies keep X's own 50% and 111 = RDIV(4 x 50%) = 2 (needs 1; SE <= 6 would give RDIV(1.5) = 2 as well).

### a63_misc.py (chain at p90 with the expect, score with no param)

| Variant | SE / copy / jmp, P(>5), no-key | Score |
|---|---|---|
| `unsigned type`, SE test nested, `type = 14; e->type = 14;`, a `const uint8_t *key = xb.pub1bl` local | 7 / 4 / 2, 38.1%, 14 | equal (0/7) |
| SE stores reordered (`e->type = type = 14` last) | same chain | 2/9 |
| checkBl called with `e->type` | same chain | 16/185 |
| no-key arm first (`if (!xb.pub1bl) .. else if (!verify) ..`) | same chain | 10/23 (.rdata order) |
| passed arm first (`if (cbVerifySig(..)) passed; else {..}`) | same chain | 16/29 |
| sig test on `e->type` (three separate tests) | chain gone (SE block 7, copy 258) | 196 |
| sig types as a nested `switch (type) { case 5: case 11: case 17: }` | 7 / 23 / 11, 49.6%, 6 | 49/215 |
| `ver_flat` (second pub1bl test) | 7 / 4 / 2, 48.5%, **29 aligned** | 57/127 |

### Don't retry (attempt 63)

- The param alone through S / Xc on this CFG: the joiner update above leaves only Psig, Pk, Pf, p, q and integer roundings, all fixed or too small; this closes attempt 62's "2% problem" as stated.
- The `<= 5` exit inside the failed arm for target B, any arm form or tail (a63_sf2.py): 22 loose, and the chain can't close without a joiner thread on X.
- a63_misc.py's edits (the table): none moves the chain; the equal bases are equal.
- Raising the no-key flow by a second pub1bl test (`ver_flat`).

### What to try next

- The 112 >= 21 condition is the one new handle: any natural shape where the no-key log isn't dominated by the pub1bl test, or where the no-key flow is otherwise 50% higher, closes the alignment with 111 at 2 (then check the failed / passed blocks' places).  Nothing with a single pub1bl test was found.
- exp_devgl: unchanged since attempt 53 (not swept this attempt).
- Otherwise build stays at 3; the remaining tricks need a different CFG for the signature region or the tail, not a predictor.

### Costs now (strict/loose, removed alone; 3 tricks, unchanged)

exp_pr 4/2 (`(int)r < 0` in its place 7/0), exp_devgl 43/7; the param only exists for exp_pr (0/7 at p0 and p90, IDENTICAL at p95 / p97 / p99).

## Attempt 64

Goal: the brief's two leads: (1) exp_pr / the param by attempt 63's second closing condition (the no-key log copy, final bb 112, at frequency >= 21 with the SE copy's jmp block 111 left at 2), from a form with a single key test or one vrp1 threads away; (2) exp_devgl by a fuse decision whose dev arm gets <= 24.9% or whose setne tree-sink leaves in place.  src as of 7059a2db, unchanged.  New scripts in `tools/wip/dehint/bdgen`: `a64_nk.py` (signature-region forms with the key in a local and the no-key log reached past a second test; chains with `python tools/wip/dehint/bdgen/a62_semeas.py tools/wip/dehint/bdgen/a64_nk.py -x -p 99`, scores with `python tools/wip/dehint/bdgen/a60lib.py tools/wip/dehint/bdgen/a64_nk.py -p 99 -o "-;exp_pr"` and `-p 0`), `a64_dev.py` (buildFlash's fuse decision without the expect, 20 spellings; `python tools/wip/dehint/bdgen/a60lib.py tools/wip/dehint/bdgen/a64_dev.py -p 99 -o "-"`).  Diffs with `a63_diff.py <script> <label> <fn>` (fn without the leading underscore: `loadBlFiles`, `buildFlash`).  Scratch in build/bd/a64 (not kept).  Loose/strict lines.

### exp_pr: the no-key flow (a64_nk.py)

- Why no single-test form moves Pk (re-read on src's profile_estimate dump, `a51_fpred.py` on loadBlFiles): bb 21 `_76 != 0B` has pointer 85% and two call predictions (71 / 29) that cancel, combined 85%.  The no-key edge's PRED_CALL needs its dest block dominated by the test and holding a side-effect call; the no-key log block has the test as its only predecessor and is one block, so every spelling that keeps one test (nested, `!key` first, `== NULL`, a key local, passed first) has 85% and no-key 14.  Only a second predecessor (a second test) or a call-free first block (a branch before the log) changes it; the code has neither.
- With the key in a local, the second test is vrp1-threadable (no reload across cbVerifySig), unlike attempt 63's `ver_flat`:

| Variant | SE / copy / jmp, copy SUCC, no-key | Score p99 (all / exp_pr off), p0 the same |
|---|---|---|
| src | 7 / 4 / 1, 68.1 / 31.9, 14 aligned | IDENTICAL / 2/4 |
| `flat_local`: `key && !cbVerifySig(..)` fail, `else if (key)` passed, else no-key | 7 / 4 / 2, 57.1 / 42.9, **29 aligned** | 89/120 / 90/111 (+displ in the callers) |
| `flat_local2`: `key && cbVerifySig(..)` passed, `else if (key)` fail, else no-key | 7 / 4 / **0**, 88.4 / 11.6, 29 not aligned | 74/163 / 76/162 |
| `flat_local3`: `!key` no-key first (one test) | 7 / 4 / 1, 14 | 10/20 / 12/24 (.rdata order, as attempt 63's nokey_first) |
| `r_res`: `if (!verify) r = -1; if (r) fail log else passed log` | 7 / 4 / 1, 14 | 42/61 / 44/65 |
| `flat_xb_ok`: `!xb.pub1bl` no-key, `else if (verify)` passed, else fail | 7 / 4 / 1, 14 | 14/24 / 16/28 |

- `flat_local` does close the alignment the second way (29 > 10 x 2), and with exp_pr off it costs the same as with it, so the alignment itself is no longer the difference; but the higher no-key flow reorders bbro: the sig-failed log block and its setFlashBuild copy move after the type-11 test, the type-11 path's no-key copy is placed before it, and the no-key string is expanded last (every .rdata reference after it moves by 0x24).  So raising the no-key flow by 2x moves more than the padding; the reference's no-key copy is at about 14.

### exp_devgl: spellings (a64_dev.py)

- Re-read the mechanism on src minus the expect (`a51_fpred.py` on buildFlash): bb 3 `(unsigned)(type - 4) <= 1` gets opcode positive 27% and nothing else; the setne pass_sink puts into the split non-dev edge (73% < 75% of the def block; the load stays), after which ce1 has a three-insn else block and keeps the branch (`sub; mov edx; cmp; jbe` for the reference's `setne; sub; cmp; mov eax,1; cmovbe`).

| Variant | buildFlash loose/strict |
|---|---|
| src minus the expect, `>= DEVGL && <= DEVGL16`, a `t` local, a `dev` local, `!!glitch2mfg`, `BOOL fuse`, `if (JTAG) fuse = 1; else {..}` | 7/43 (same GIMPLE) |
| `fuse |= dev` | 9/45 |
| `fuse = JTAG ? 1 : glitch2mfg != 0; if (dev) fuse = 1;` | 9/45 |
| `if (!fuse && dev)`, `if (!fuse) { if (dev) }` | 10/598 |
| `fuse = 0; if (glitch2mfg) fuse = 1; if (dev) fuse = 1;` | 11/47 |
| `uint8_t fuse` | 12/49 |
| `switch (xb.type) { case DEVGL: case DEVGL16: fuse = 1; }` inside the JTAG test | 12/600 |
| `fuse = dev ? 1 : glitch2mfg != 0` | 13/48 |
| `fuse = glitch2mfg ? 1 : dev` | 14/183 |
| JTAG last, `fuse = 0; if (glitch2mfg || dev) fuse = 1;`, one switch with JTAG | 25 to 28 |
| dev test first (`JTAG && !dev` then the setne) | 56/686 |

- Opcode alternatives for the dev test: `< 2u` folds to `<= 1` (positive 27%); `& ~1` would be nonequal 28%; `== 4 || == 5` folds to the range.  None goes under 25%.
- The helper route (attempts 52, 53, 61) was not rebuilt: nothing new answers attempt 53's objection (the only call before the flag is the salt memset, and a memset-holding helper's JTAG edge becomes an early return).  The 58-60 estimate levers (memmove / helpers / inline order) only change which IPA inliner takes a call-holding helper; a call-free fuse helper is still einlined (growth ~4) and re-predicted at 27%.

### Don't retry (attempt 64)

- exp_pr by a second key test on a local (`flat_local`, `flat_local2`): no-key 29 and the alignment, but 74 to 90 loose from the reordered failed / no-key blocks and the .rdata order.
- `!key` / `!xb.pub1bl` first, passed first with one test, an `r` result tested for the logs: no change to the chain.
- exp_devgl by any spelling in a64_dev.py's table, or by the fuse variable's type.

### What to try next

- exp_pr: the two closing conditions are both reachable only with a second predecessor of the no-key log (112 >= 21), which costs the layout, or a predictor on the checkBl / tail tests that attempts 61 to 63 showed the code doesn't have.  Unless a whole-tail or whole-signature-region reconstruction turns up, build stays at 3.
- exp_devgl: unchanged since attempt 53; a second predictor on the dev edge needs something in the dev arm, and the reference's dev arm is a cmov.

### Costs now (strict/loose, removed alone; 3 tricks, unchanged)

exp_pr 4/2 (`(int)r < 0` in its place 7/0), exp_devgl 43/7; the param only exists for exp_pr (0/7 at p0 and p90, IDENTICAL at p95 / p97 / p99).

## Attempt 65

Goal: the brief's whole-function lever on buildFlash (restructuring into / out of helpers the way an author might, which landed in attempts 46, 49, 59, 60), aimed at exp_devgl: either the non-dev arm at >= 75% of the dev test's block at sink time (so the setne stays there) or the fuse decision arriving through an IPA-inlined helper with its own profile (attempt 52's 19.1%).  src as of 882d70c9, unchanged.  New script `tools/wip/dehint/bdgen/a65_bf.py` (C text written with 4-space tabs), run with `python tools/wip/dehint/bdgen/a60lib.py tools/wip/dehint/bdgen/a65_bf.py -p 99 -o "-;exp_devgl" [-f label] [-k label]`.  Dumps with `BDP=99 sh tools/wip/dehint/bddump.sh <file> buildFlash t-sink,t-einline,i-inline`.  Scratch in build/bd/a65 (not kept).  Loose/strict lines, p99.

### buildFlash's structure against the reference and the Linux build

- The reference (and tools/ref/xeBuild64's buildFlash at 0x409a70, gcc 4.9.2) start with the fuse decision inline (`setne; sub 4; cmp 1; mov 1; cmovbe`), then the fromConsole header / checkBootImage branch, suLoadDir, the loaders, verifyBlSigs, fsStartBlock / calcBlAreaSize, the glitch / devgl patch step, patchHeaderOpts, keysInit, the fuse setup (findFile(24), setFuseCpuKey, the offset), the encoders, showFuses, the add step, the FS fixup, the three slot-overflow writers, then the firmware and security-file loops.  Natural sub-steps: header, loads, glitch blmod, fuse setup, encode, overflow writers (three near-identical blocks).  In the reverse direction only patchConsoleBlmod is a static helper (attempt 60: written out 66, reversed test 28).
- What decides exp_devgl (re-read on src minus the expect, sink dump): bb 2 (entry, freq 1148) tests JTAG (72%), bb 3 (826) holds the glitch2mfg load and the dev test `(unsigned)(type - 4) <= 1` (opcode positive, 27%), the split non-dev edge block bb 4 is 603.  gcc 6's select_best_block sinks a non-memory statement when best->frequency < early->frequency x 75 / 100 at the same loop depth: 603 < 619.5, so `_64 = _63 != 0` and the int conversion go to bb 4 (`Sinking .. from bb 3 to bb 4`).  The only inputs are that ratio (the dev test's probability) and the loop depths; integer rounding could only help if buildFlash's entry frequency were around 10 (inlined loops nested three deep), which no restructure gives and which would move every alignment.
- IPA inlining doesn't change the ratio: the inline transform asks for TODO_rebuild_frequencies and estimate_bb_frequencies recomputes from the same edge probabilities, so a helper elsewhere in buildFlash can scale the entry frequency but not bb 4 / bb 3.

### a65_bf.py (exp_devgl kept / off)

| Variant | all kept | exp_devgl off |
|---|---|---|
| src | IDENTICAL | 7/43 |
| `ld`: suLoadDir, the loaders, the missing-files log, verifyBlSigs and "done!" as `loadFlashFiles()` returning r / 1 / 0 | **IDENTICAL** (equal base) | 7/43 |
| `hdr`: the header / checkBootImage branch as `initImage()` (returns 0 or r, logs the error) | 809/1344 (+.rdata) | 824 |
| `hdr_ld`: both | 809 | 824 |
| `fz`: the fuse setup as `setVfuses()` under `if (fuse)` | 77/735 | 84 |
| `blmod`: the blmod.bin / console blmod step as `patchBlmod()` | 66/103 | 73 |
| `enc`: the two encoders as `encodeFlashBls(salt, blocks)` | 337/1296 | 344 |
| `ovf`: the three slot-overflow writers as `addSlotOverflow(msg, name, cf, cg, off)` | not inlined (out-of-line copy, every function's displacements move) | the same |
| `setup_ptr`: the fuse decision and the header step as `initFlash(&fuse)` | 815/1350 | 824 |
| `setup_ret`: the same returning fuse, r through a pointer | 838/1437 | 845 |

- `setup_ptr` is the brief's "setup helper that computes the fuse flag along with other real work": einline refuses it (growth 26 > 14) and IPA inlines it, so its own profile is what reaches buildFlash.  But in that profile the dev test is still 27% / 73% (sink dump: the same `Sinking .. from bb 3 to bb 4`): the helper's dev arm joins the header step, not a return, so there is no early-return prediction.  The 19.1% of attempt 52 needs the dev arm to be an early return, i.e. the helper's work must all come before the fuse decision, and the only work the reference does before it is the salt memset (attempt 53's dret2 and its JTAG early-return problem).
- No variant moved loadBlFiles, loadConsoleBlFiles or any other function except `ovf` (out of line); `ld` is the only equal base.

### Don't retry (attempt 65)

- exp_devgl by moving any later part of buildFlash into a helper (header, loads, fuse setup, blmod, encode, overflow writers) or by writing patchConsoleBlmod out: none of them reaches the dev test's probability, which is the only input to sink's decision.
- exp_devgl by a setup helper that computes the fuse flag and then does the header step (`initFlash(&fuse)` or returning fuse): IPA-inlined with its own profile, but that profile is 27 / 73 with no early return.
- The overflow writers as one helper: gcc keeps it out of line.

### What to try next

- exp_devgl: the condition is now fully stated in sink's own terms: P(dev) <= 25% at the dev test, a use of the setne in bb 3, the use block at a deeper loop depth than bb 3, or entry frequency ~10.  Nothing in buildFlash's real code gives any of them; only a helper whose dev arm returns early (with all its work before the decision) gets P(dev) under 25%, and the reference has no such work.  Treat exp_devgl as closed unless a reason to doubt the reference's source order turns up.
- exp_pr / the param: attempts 61 to 64's readings stand.

### Costs now (strict/loose, removed alone; 3 tricks, unchanged)

exp_pr 4/2 (`(int)r < 0` in its place 7/0), exp_devgl 43/7; the param only exists for exp_pr (0/7 at p0 and p90, IDENTICAL at p95 / p97 / p99).

## Attempt 66

Goal: the brief's whole-structure lever on loadBlFiles' 5..21 arm and its signature / tail region: helpers (early- or IPA-inlined, the useBuiltIn / memmove family of attempts 59-60) for the signature check with its three logs, the tail, the checkBl call, the arm's load + checkBl, the CF/CG fallback and the whole arm, each measured on the SE chain (SE block, its tail-test copy, the jmp block, no-key, the copy's >5 edge) at gcc's default 90 and at 99 with the expect kept, and with the tail as `(int)r < 0` and no param, before scoring.  src as of 0f13d148, unchanged.  New script `tools/wip/dehint/bdgen/a66_h.py` (helpers inserted before loadBlFiles), run with `python tools/wip/dehint/bdgen/a62_semeas.py tools/wip/dehint/bdgen/a66_h.py -x -p 90` (and `-x -p 99`, `-p 0`) for the chains and `python tools/wip/dehint/bdgen/a60lib.py tools/wip/dehint/bdgen/a66_h.py -p 0 -o "-;exp_pr"` (and `-p 99`) for scores; `-f <prefix>` picks a family (sig_, tl_, fb, ld_, ck_, lc_, w, p_).  Einline decisions from `BDP=99 sh tools/wip/dehint/bddump.sh build/bd/a60/<label>.c loadBlFiles t-einline` after `a60lib.py .. -k <label>`.  Scratch in build/bd/a60 (`<label>.c`, not kept).  A compile and score of 60 variants takes about 12 s.  Loose/strict lines; "+40 displ" is loadConsoleBlFiles 18, blmodMissing 2, buildFlash 20: call displacements from loadBlFiles' size.

### Which helpers einline takes

- Every helper holding a log call is IPA-inlined, not einlined: checkBlSig (growth 19 > 14), verifyBl (13, over 14 / (calls + 1)), finishBl.isra (7, the same rule), setKitBuild(e, type).isra (9).  So none of the signature / tail helpers enters loadBlFiles' CFG before profile_estimate; each brings its own profile at IPA, which the chains below show.
- Einlined: checkEntry (one checkBl call), loadChecked, setKitBuild(e) (one setFlashBuild call), and the call-free predicates isSigBl, isRetailGlitch, isSe.

### Chains and scores (a66_h.py)

| Variant | chain p90 -x: SE / copy / jmp, copy >5, no-key | chain p0 `(int)r < 0` | score p0 all kept / exp_pr off |
|---|---|---|---|
| src | 7 / 4 / 2, 38.1%, 14 | 7 / 4 / 2, 49.8% | 0/7 / 2/4 (IDENTICAL at p99) |
| sig_er: `checkBlSig(e)` with early returns, -1 on failure | 7 / 4 / 2, **50.0%**, 7 + 0 | 7 / 4 / 2, 50% | 103/170 / 103 |
| sig_nr: the same nested with an `r` local | 7 / 4 / 2, 50.0%, 11 | the same | 94 + 40 displ |
| sig_ok / sig_okn / sig_oknest: `sigOk(e)` 0 on failure, `&& !sigOk(e)` or nested | 7 / 4 / 2, 50.0% (p99: 46.9 to 48.8%) | 50% | 139 to 160 |
| sig_t / sig_tn: the type test inside (`r = checkBlSig(e, type)` for every type) | 7 / **2 / 1**, 46.1%, no-key 6 / 9 | 7 / 2 / 1, 35.6%, no-key 6 / 9 | 73/126 + 40 displ, either |
| sig_bn: `checkBlSig(e->data, e->name)` | 7 / 4 / 2, 50%, 7 | the same | 104/168 |
| sig_v / sig_vok: the key test stays, verify + two logs in `verifyBl(e)` (-1 / ok) | 7 / 4 / 2, 50%, 14 | the same | 59 + 40 displ / 110 to 132 |
| tl_fin: `if (r) goto fail; setKitBuild(e, type);` (the kit test inside) | 7 / 4 / 14 (copy gone) | the same | 64 + 40 displ |
| tl_fin2 / tl_r: `setKitBuild(e, type)` alone, `r = finishBl(e, type, r)` | 7 / 4 / 2, 39.0%, 14 | 39.0% | 40/117 + 40 displ |
| tl_k: `setKitBuild(e)` for the setFlashBuild line (einlined) | as src | as src | 4/21 / 6/18 |
| fb_*: the CF/CG fallback as `useSuBl(e, type)` (two bodies, nested or `&&`) or `suFallback(e, type, r)`, both loaders or loadBlFiles only | as src (38.0 to 38.1%) | as src | 134 to 142 (+ console 90 when shared) |
| ld_su / ld_su2: load + fallback as `loadSuBl(e, type)` (attempt 50's loadUpdateBl) | as src | as src | 85 + 40 / + console 86 |
| ld_all: load + fallback + SE + checkBl as `loadUpdBl(e, type)`, the caller re-reads `type = e->type` | chain gone (SE 8, copy 298), no-key 29 | the same | 191/369 |
| ck_all: `checkEntry(e, type)` at all three checkBl sites | as src | as src | **equal base** (0/7, 2/4; IDENTICAL at p99) |
| lc_6: case 6 as `loadChecked(e, 6)` | as src (38.0%) | as src | **equal base** |
| w1 to w4 (and `f`: the caller keeps `if (r && xb.type <= 5) goto fail`): the whole arm as `loadCbBl(e, type)`, four tail forms | 8 / 5 / 2, 39 to 40%, no-key 17 to 21 (w1 / w4: 21, aligned) | the same | 168 to 306 |
| p_sig / p_sigi: an `isSigBl(type)` predicate | 7 / 4 / 2, 42.7%, 11 | 50% | 34/115 + 40 displ |
| p_kit: `isRetailGlitch()` for the tail test | as src | as src | **equal base** (IDENTICAL at p99) |
| p_se: `isSe(e->data)` for the 'S' / 'E' tests | **SE 42** / 21 / 8 | the same | 9/177 + 40 displ |

### Readings

- An IPA-inlined signature helper always takes the joiner thread away: the -1 now reaches the tail test X through the helper's return PHI, which vrp1 doesn't thread the way it threads src's `r = -1` (the copy's >5 edge is 50%, or 46.9 to 48.8% at p99, instead of 38.1%).  So no signature helper can even reach the param-alone condition (< 37.5% at p90): the thread that gives src its 38.1% is the one these helpers remove.  This is attempt 63's joiner formula seen from the other side.
- sig_t is the only family where the jmp block reaches 1 (the copy at 2: checkBlSig(e, type) runs for every type, so the SE path's type 14 threads through the helper's type test), also with `(int)r < 0` and no param (35.6%).  But its no-key copy is 6 and not aligned, and the helper's own blocks cost 73 loose: the layout, not the alignment, is the difference.
- An einlined boolean predicate reaches profile_estimate as a 0/1 PHI tested at 50% (gcc 6 has no early jump threading), so isSe sends the SE block from 7 to 42 (it needs 6) and isSigBl puts Psig at 50% (S down, the wrong way).  isRetailGlitch folds back into the compare in the early passes (equal base).
- The whole-arm helper's own profile (early returns on the load and checkBl results) moves the SE block to 8, and its body is new code against the reference (168 and up).

### Don't retry (attempt 66)

- The signature check with its logs as a helper in any form (early returns, nested with `r`, ok-returning, type test inside, (bl, name) parameters, verify + two logs with the key test kept): 59 loose and up, and the IPA-inlined -1 loses vrp1's joiner thread (copy 50%).
- The tail as a helper (`setKitBuild(e, type)`, `finishBl(e, type, r)`): 40 and up.  `setKitBuild(e)` for the setFlashBuild line: 4/21.
- The CF/CG fallback as a helper (useSuBl, suFallback), load + fallback (loadSuBl), load + fallback + SE + checkBl (loadUpdBl), or the whole arm (loadCbBl, four tails): 85 and up.
- Call-free predicates for the SE test or the sig-type test (isSe: SE 42; isSigBl: Psig 50%).
- checkEntry / loadChecked / isRetailGlitch as levers: equal bases, the chain unchanged.

### What to try next

- exp_pr / the param: the helper lever is closed for this region.  einline can't take anything holding the logs, IPA-inlined helpers lose the joiner thread, and einlined predicates move the profile by whole 50% steps.  Attempts 61 to 64's readings stand; build stays at 3 unless the signature region's or the tail's CFG turns out to have a different reconstruction not yet seen.
- exp_devgl: closed since attempt 65.

### Costs now (strict/loose, removed alone; 3 tricks, unchanged)

exp_pr 4/2 (`(int)r < 0` in its place 7/0), exp_devgl 43/7; the param only exists for exp_pr (0/7 at p0 and p90, IDENTICAL at p95 / p97 / p99).

## Attempt 67

Goal: attempt 66's leads (tl_k, p_se, a sig_t variant that keeps the SE jmp block at 1 and restores the no-key copy's frequency, combinations with each other and with `(int)r < 0`), then anything new on the tail.  src as of 75100692, unchanged.  New scripts in `tools/wip/dehint/bdgen`: `a67_base.py` (src, `r != 0` and `(int)r < 0` tails, for a63_diff.py), `a67_st.py` (sig_t variants), `a67_kit.py` (the kit arm through a helper), `a67_kx.py` (that helper crossed with bodies, arguments, tails, orientation, the failed arm's r = -1 order, else forms, a pass-through / int return, and the none test as `continue`).  Chains with `python tools/wip/dehint/bdgen/a62_semeas.py <script> -x -p 0` (and `-x -p 90`, `-x -p 99`, `-p 0`), scores with `python tools/wip/dehint/bdgen/a60lib.py <script> -p 0 -o "-;exp_pr"` (and `-p 99`), diffs with `python tools/wip/dehint/bdgen/a63_diff.py <script> <label> loadBlFiles -p 0`.  Dumps: `gcc -c -O3 -fdump-tree-all` (and `-fdump-tree-dom2-details`, `-fdump-ipa-inline-details`) on `#line`-prefixed copies in build/bd/a67 (`ds/` src at p99, `dk/` k1_n at p0, `d3/` the b3 body; not kept); `fx.py` there pulls loadBlFiles' final body out of a dump.  Loose/strict lines.

### Attempt 66's leads

- **tl_k** (`setKitBuild(e)` for the setFlashBuild line, einlined) was scored in a66_h.py's "score p0" column: no `--param` (gcc's 90), expect kept 4/21, exp_pr off 6/18; at p99 4/14.  The whole loose residue is the setFlashBuild argument: `mov eax,[ebp+0x40c]` (e->data through the loop pointer) for the reference's `imul eax,[esp+0x2c],0x42c; mov eax,[eax+0x422bc]`.  Its chain is src's (7 / 4 / 2, 38.1% at p90), so even closed it would be an equal base, not a removal.
- **p_se** (`isSe(e->data)`): 9/177 at p0 and p99 plus 40 displacement lines; the einlined predicate is a 50% PHI test, SE block 42.  Nothing to work.
- **sig_t family** (a67_st.py; chain p90 -x / p0 `(int)r < 0`, score p0 kept):

| Variant | chain | score |
|---|---|---|
| sig_t (attempt 66) | 7 / 2 / 1, 46.1%, no-key 6 | 73/126 + 40 displ |
| tk_else / tk_nkfirst / tkn_else: key test before the helper (`if (xb.pub1bl) r = checkBlSig(e, type); else if (sig type) no-key log`), the type test inside | copy 258, jmp 34 (chain gone), no-key 22 | 195 to 200 |
| t3 / t3b: the helper returns 1 with no key, the caller logs (`r == 1` / `r > 0`) | t3: 7 / 2 / 1, no-key 13 **aligned** at p0 (50.0% at p90); t3b: jmp 0 | 105/172, 151 |
| tkf: key test first inside the helper, the no-key log there under the type test | chain gone, no-key 6 | 189 |
| ts: the type test as a switch inside | 7 / 11 / 5 (p90), 7 / 2 / 0 (p0) | 140 |
| tr: r passed in and returned | 7 / 2 / 0 (p90, no-key 6 aligned) | 152 |
| sig_t + tl_k / + p_se, tk + p_se | as their parts | 63 / 80 / 197 |

  t3 is the one sig_t form that keeps the jmp block at 1 and gets the no-key copy aligned (13), but its IPA-inlined helper and the caller's `r == 1` test are new code: 105 loose.  The sig_t family is closed.

### The kit arm through an IPA-inlined helper (a67_kit.py, a67_kx.py)

- Form: the tail unchanged up to `break; }`, then `setKitBuild(e, type);` in place of `if (type == 14) setFlashBuild(getBeU16(xb.files[i].data + 2));`, with `static void setKitBuild(struct fileent *e, int type) { if (type == 14) setFlashBuild(getBeU16(e->data + 2)); }`.  einline refuses it (growth 6 exceeds early-inlining-insns divided by number of calls), IPA inlines it first of loadBlFiles' callees, so at profile_estimate the tail test X's >5 successor block is the call: PRED_CALL, P(<=5) 71%.  That is the p attempts 61 to 63 said was missing (with q = 50% the joiner formula wants P(<=5) >= 70.5%), and it holds (`a62_semeas.py`, SE copy's <=5 / >5):

| Tail | p0 | expect kept |
|---|---|---|
| src | `(int)r < 0`: 50.2 / 49.8, jmp 2, no-key not aligned; `r != 0`: 34.4 / 65.6 (inverted: jmp 1 and aligned, but `ja` for `jbe`) | p90 61.9 / 38.1 jmp 2; p99 68.1 / 31.9 jmp 1 aligned |
| k1 `(int)r < 0` | **71.0 / 29.0, jmp 1, no-key 14 aligned** | |
| k1 `r != 0` | **87.5 / 12.5, jmp 0, aligned** | |
| k1 with the expect | 87.5 / 12.5 | p90 the same; p99 96.3 / 3.7 |

  So with the helper the alignment needs neither the expect nor the param.
- Scores: loadBlFiles 6/31 (`(int)r < 0`, or the expect at any param) and 8/38 (`r != 0`, `r`: the 6 plus the SE copy's `ja` / `jbe`), plus loadConsoleBlFiles 18, blmodMissing 2, buildFlash 20 (call displacements: the function is 11 bytes shorter).  exp_devgl still needs its expect (27/63 off at p0).  The residue, the same for every variant:
  - case 23's size log sets `edi = -1` itself and jumps to the could-not-read log, where the reference jumps to the shared `mov edi,-1` block; and the sig-failed path's `type != 14` / setFlashBuild exits go to that shared block, where the reference sets `edi = -1` before the `jne` (in the sig-failed block) and jumps to the log.
  - the sig-failed setFlashBuild copy reads `[ebx]` (e->data through the loop pointer) instead of recomputing `xb.files[i].data` from the spilled i.
- Which pass: dom2 (`-fdump-tree-dom2-details`).  src registers the FSM thread `(19, 22) (22, 23) (23, 100) (100, 101)` (sig-failed log -> the type == 14 test -> **the setFlashBuild block** -> the join's `if (r)` -> the log), so dom2 copies setFlashBuild onto the loop-exit path before ivopts (attempt 11's / 21's reading of the recomputed address).  k1 registers `(19, 22) (22, 100) (100, 101)` instead (the `type != 14` edge) and never copies the setFlashBuild block, so the copy is made after ivopts (IV read) and the -1 reaches the log as a PHI constant that crossjump merges into the fail block.  Every other thread registration is identical.
- Why: the FSM search walks the join's PHI arguments in order and marks blocks visited, so the first of the two edges from the type test wins.  At fixup_cfg4 the join's PHI is src's with one change: src has the type test's false edge in the middle (`.., -1(89), r_3(28), r_87(31), ..`, made at gimplification), k1 has it appended last (`.., -1(112), r_3(28)`).  The inlined body exits through the call's continuation block, a forwarder; cfg cleanup redirects its predecessors to the join (appending) and then removes its own edge (unordered_remove, so the last-redirected edge, the call path, takes the forwarder's slot 5 as in src, and the false edge stays last).  vrp1's thread updates then remove the join's slot-0 edge (the none skip, `0(4)`), and unordered_remove moves the last edge, the false edge, into slot 0: after vrp1 the PHI reads `r_453(22), .., r_453(23)` where src reads `r_455(23), r_455(22)`.  So the residue is an edge-order artefact of inlining, not a probability.
- What doesn't move it (a67_kx.py, all 6/31 with `(int)r < 0`, 8/38 with `r` / `r != 0`): helper bodies `if (type == 14) ..`, `if (type != 14) return; ..`, `{ ..; return; }` (all normalised to the same callee CFG by einline time), a `uint16_t build` local, `else return;`; the switch body 7/28; arguments `(e, type)`, `(&xb.files[i], type)`, `(type, xb.files[i].data)`, `(type, i)` with `xb.files[i].data` inside (the inlined load CSEs either way); kit-first orientation (`if (xb.type > BUILD_DEVGL16) { setKitBuild(..); break; }`), `else if` and `else` forms; `r = -1` before the failed log; an `int` helper returning 1 if it set the build.  `r = setKitBuild(e, type, r)` (r passed through) loses the PRED_CALL (49.8%) and is 6/34.  `seBuild(e)` testing `e->type` is 111.  The none test as `if (!strnicmp(..) && !e->crc) continue;` (to change the join's slot 0): 185 loose.
- The inline copy makes edges in callee block order (copy_edges_for_bb over the callee's blocks), and the type test comes before the call block in every body, so no callee shape makes the call path the appended edge.

### Don't retry (attempt 67)

- tl_k and p_se as levers (above), and the sig_t family: key test before the helper, no-key log outside / inside under the key test, tri-state return, switch type test, r passed in, combined with tl_k / p_se (63 to 200 loose).
- The kit helper's body spellings, arguments, orientation, else forms and return types (the list above): the false edge's slot is the same in all of them.
- The none test as a `continue`.

### What to try next

- The kit helper is the first route found that closes exp_pr's chain without the expect *and* without the param (2 tricks).  What's left is one edge's slot in the switch join's predecessor list after IPA inlining.  Levers not tried: something else that appends an edge to the join after setKitBuild's continuation is cleaned up (another IPA-inlined callee whose continuation is a forwarder to the join, e.g. a void helper in a later case arm, if the code has a natural one), so that edge rather than the kit false edge is moved into slot 0 by vrp1; or keeping vrp1 from removing the slot-0 edge.  Check a candidate's dom2 FSM registration for `(22, 23) (23, 100)` before scoring.
- exp_devgl: closed since attempt 65.

### Costs now (strict/loose, removed alone; 3 tricks, unchanged)

exp_pr 4/2 (`(int)r < 0` in its place 7/0; with the setKitBuild helper and `(int)r < 0`, no param: loadBlFiles 31/6 + 40 displacement), exp_devgl 43/7; the param only exists for exp_pr (0/7 at p0 and p90, IDENTICAL at p95 / p97 / p99).

## Attempt 68

Goal: attempt 67's lead (the IPA-inlined `setKitBuild` closes exp_pr's chain with no expect and no param; what's left is the order of the switch join's predecessors after inlining).  src as of 81ed9726, unchanged.  New scripts in `tools/wip/dehint/bdgen`: `a68_phi.py` (dumps a variant with `-fdump-tree-all` and prints the join's r PHI, the PHI with the most arguments, after fixup_cfg4 / ccp2 / mergephi2 / vrp1 / dce2 / dom2, plus dom2's FSM registrations; `-a` for every pass), `a68_fsm.py` (the cheap filter: one compile with `-fdump-tree-dom2-details`; 'good' when two of loadBlFiles' FSM paths have three edges, i.e. src's `(19, 22) (22, 23) (23, 100) (100, 101)` through the setFlashBuild block; `-s` scores the good ones), `a68_kit.py` (helper bodies, arguments, return values, caller gotos, the kit test inside the helper, callee return types), `a68_sw.py` (every single move of one case block of the switch, on the void helper).  Runs: `python tools/wip/dehint/bdgen/a68_fsm.py tools/wip/dehint/bdgen/a68_kit.py -s [-f label]`, `python tools/wip/dehint/bdgen/a60lib.py tools/wip/dehint/bdgen/a68_kit.py -p 0 -o "-"`.  Dumps in build/bd/a68 (not kept).  Loose/strict lines, p0 (no param) unless said.

### Where the false edge comes from (exactly)

- The callee's own CFG doesn't decide it.  `if (type == 14) X; else return;` does give the callee's return block preds (call, false) at cfg time, but eipa_sra's isra clone (`struct fileent *e` is only used for `e->data`) rebuilds the body with (false, call); with a pointer or index argument there is no clone and the callee keeps (call, false), but the inline copy (copy_edges_for_bb over the callee's blocks in chain order) recreates the edges source block by source block, so the inlined return block R' always has preds (type test's false edge, call block).
- In the caller: expand_call_inline splits the call block first, so the continuation K (empty, the `break`) has a lower index than the copied body.  fixup_cfg4's cleanup (index order) removes K first (R' takes K's slot in the join's PHI), then R': its preds are appended in order (false, call) and unordered_remove fills R''s slot with the last one, the call path.  So the false edge is last at the join; vrp1's first thread is the join's first edge (the none skip, `(4, 113)`, the first FSM registration), and the false edge takes slot 0, ahead of the call path, for dom2's FSM search.  (a68_phi.py on k1_n shows it pass by pass.)
- What fixes it: **R' must not be a forwarder until vrp1 has threaded the join.**  Then fixup_cfg4 leaves R' in place, vrp1 moves src's last edge (a threaded -1 edge) into slot 0, and when R' is cleaned up after vrp1 its preds are appended (false, call) with the call path taking R''s old slot, so the call path comes first and dom2 registers `(19, 22) (22, 23) (23, 100)` as in src.  A PHI in R' doesn't do it (mergephi2 removes PHI forwarders before vrp1: ri_n, ri1, an `int` helper returning 0 / 1); a non-PHI statement that only DCE removes (dce2 runs after vrp1) does.
- Diagnostics (a68_kit.py; `int setKitBuild(..)` whose return value the call ignores; tail `(int)r < 0`, no param):

| Variant | FSM | Score |
|---|---|---|
| `(e, type)`, `return xb.type;` / `return e->crc;` | good | loadBlFiles 4/14 (only the setFlashBuild argument through the IV, `mov eax,[ebp+0x40c]`); the 40 displacement lines are gone |
| `(e, type)`, `return e->size;` | good | 7/21 |
| `(e, type)`, `return type;` | bad (the copy is gone before mergephi2) | 6/31 |
| `(xb.files[i].data, type)`, `return xb.type;` | good | 3/7 |
| **`(uint32_t i, int type)` reading `xb.files[i].data` inside, `return xb.type;` / `xb.files[i].type` / `type == 14` / `xb.nFiles` / `xb.files[i].data != NULL` / `xb.seReplacesCf`** | good | **IDENTICAL**, every one |
| the same, tail `r != 0` / `r` | good | 2/11 |
| the same, the expect kept (no param) | good | IDENTICAL |
| void `(i, type)` (riv), `(int)r < 0` | bad | 6/31 + 40 displacement lines |

  With `return type == 14;` and build.sh's build flags at plain `-O3`, **`sh build.sh` ends with the right SHA256** (exp_pr and the param both gone, exp_devgl kept; it is 7/43 off as before).  Not landed: the return value is unused at the only call site, so the returned expression is dead code whose only job is to steer gcc (a trick by the README's rules, not a borderline shape).  Saved as `tools/wip/dehint/drafts/build_loadBlFiles_setKitBuild_candidate.patch` (src/build.c and build.sh) for the user's review.
- The argument matters separately: with `e` (or `&xb.files[i]`) the inlined `e->data` load becomes the IV read (4/14); passing `i` and reading `xb.files[i].data` inside gives the reference's `imul eax,[esp+0x2c],0x42c; mov eax,[eax+0x422bc]`.  The argument alone doesn't help (riv, void `(i, type)`: 6/31); the FSM order comes first.

### Natural forms tried for the same effect (none works)

- Callee bodies with the call path's block first: `if (type == 14) X; else return;`, `if (..) { X; return; } return;`, `if (type != 14) ; else X;`, a switch with the default first or last, `do { if (type != 14) break; X; } while (0);`, each with `e`, `e->data` and `xb.files[i].data` arguments (a68_kit.py b*, p*): 6/31 (switch forms 7/28 or 12/37); the inline copy reorders them as above.
- An `int` helper returning 0, 1 / 0, or r passed through (`r = setKitBuild(i, type, r)`, `uint32_t` or `int r`): a PHI or a copy, gone before vrp1 (6/31); the pass-through also loses PRED_CALL (50.2%, 6/34).
- A `goto` after the call (to a label before the `if (r)`), `else goto out;` in the helper: no effect.  C emits no GIMPLE_PREDICT for goto here (only `continue` does; predicts survive to fixup_cfg4 and are stripped before ccp2), so nothing keeps K or a false-path block alive.
- The kit test inside the helper (`if (xb.type > BUILD_DEVGL16 && type == 14)`, nested, early return), called on every build, the tail testing the build type only for the failure (`if (xb.type <= BUILD_DEVGL16 && (int)r < 0) goto fail;` before the call, or nested): FSM good, but the signature-log copies swap and the kit copy reads through the IV: 40/121.  The call before the failure test: FSM bad.  `type == 14 &&` first: bad.
- loadXell / loadBl24 / defaultBl60 returning `uint32_t` (their inlined return blocks become PHI forwarders that mergephi2 merges into the join after the false edge): FSM good in some combinations, but 59 to 93 loose in loadBlFiles, on src too (rt_*).
- a68_sw.py, the 132 single case-block moves on the void helper: 129 FSM bad; the good ones are m2_9 (case 24 after case 27) 30/142 and m2_10 / m2_11 115/280.

### Don't retry (attempt 68)

- Callee body shapes or argument spellings meant to reorder the inlined return block's preds: the inline copy creates edges in callee block order, the test block first.
- Int helpers whose result is a PHI or a copy (0 / 1, r pass-through): removed before vrp1.
- Gotos as predict carriers: C emits none.
- Callee return types of loadXell / loadBl24 / defaultBl60; case-block moves.

### What to try next

- The candidate removes two tricks for one dead return expression.  A natural form needs a statement in the inlined setKitBuild's return block that survives until vrp1 has threaded the join and is gone before dom2 (dce2, cdce, copyprop1 run in between), or anything else that appends an edge to the join after the false edge before vrp1 (mergephi2 merges PHI forwarders into it), or a first join predecessor that vrp1 doesn't thread.  A live use of the return value would keep the statement in the final code unless it is a copy that only copyprop1 removes; every natural use found so far is either dead or a copy the inliner removes at once.  If the user accepts an ignored status return (common C), the candidate lands as it is; `return type == 14;` ("nonzero if it set the build") reads most like a status.
- exp_devgl: closed since attempt 65.

### Costs now (strict/loose, removed alone; 3 tricks, unchanged)

exp_pr 4/2 (`(int)r < 0` in its place 7/0; with the void setKitBuild(i, type) and `(int)r < 0`, no param: loadBlFiles 31/6 + 40 displacement; with the candidate's unused `return type == 14;` IDENTICAL and the full build matches), exp_devgl 43/7; the param only exists for exp_pr (0/7 at p0 and p90, IDENTICAL at p95 / p97 / p99).

## Attempt 69

Goal: exp_devgl (the last trick) with the levers that landed after attempt 65: attempt 68's non-PHI statement in an inlined helper's return block, attempt 59's inline estimates, return types.  src as of 7198bf70, unchanged.  New script `tools/wip/dehint/bdgen/a69_dev.py` (sweeps s1..s22, labels below), run with `python tools/wip/dehint/bdgen/a60lib.py tools/wip/dehint/bdgen/a69_dev.py -p 0 -o "-" [-f label] [-k label]`.  Diffs with `python tools/wip/dehint/bdgen/a52_cmp.py src/build.c <variant.c> _buildFlash`; helper profiles with `python tools/wip/dehint/bdgen/a51_fpred.py <variant.c> initFlash`.  Scratch in build/bd/a69 (not kept; `all/` held the `-fdump-tree-all` runs).  gcc.gnu.org answered with a bot check (Anubis) for predict.c, so nothing was read from the gcc sources; the readings below come from the dumps.  Loose/strict lines in buildFlash, p0 (no param).

### Does tree-sink look at anything but the ratio? (src minus the expect, `-fdump-tree-sink-details-blocks`)

- No.  bb 2 (entry, freq 1148): memset, `_62 = xb.type`, `!= 2` (72%).  bb 3 (826): `_63 = xb.glitch2mfg`, `_67 = _62 - 4`, `_67 <= 1` (opcode positive 27%, the only predictor).  The dev edge goes to an empty forwarder (261, 223) and the non-dev edge to the split block bb 4 (603).  `Sinking fuse_65 = (int) _64; from bb 3 to bb 4`, then `_64`: 603 < 826 x 0.75 = 619.5, all at loop depth 0.  The PHI use sits on one edge, there is no other use and no loop-depth difference, so block order and edge order don't come into it.  P(non-dev) has to be at least 75.06%, or the entry frequency has to be about 10 for rounding to help (attempt 65).  Nothing about ordering will move it; only the dev edge's probability.

### The memset helper revisited: the JTAG edge, not the dev edge, was what broke attempt 53's `dret2`

- `dret2` (`int initFlash(uint8_t *salt)`: `int fuse = 1; memset; if (type != JTAG) { fuse = g != 0; if (dev) return 1; } return fuse;`, `fuse = initFlash(salt);`) is still 3/285.  Its profile: JTAG test 80.1% (nonequal 72 + early return 61), dev 19.1% (positive 27 + early return 39).  At sink time bb 3's non-dev edge is 80.9%, so the setne stays put (optimized dump: `_584 = _583 != 0; fuse_585 = (int) _584;` in bb 3), and ce1 does if-convert the dev arm (`IF-THEN-JOIN ... test 3, then 4, join 6`, succeeded).  What fails is `IF-CASE-2 found, start 2, else 5`: in the RTL the dev arm's `fuse = 1` block falls through into the JTAG edge's `fuse = 1` block (both PHI args are 1, and the GIMPLE dev forwarder sits on the dev edge instead of the non-dev edge as in src).  That leaves the JTAG block with two predecessors, ce1 can't hoist `mov ebx,1` into the entry, and the out-of-line `mov ebx,1; jmp` block is the whole 3/285.
- Lever (attempt 68's): give the helper's return block a statement other than a PHI, so that the JTAG skip and the non-dev arm reach the return through a block that isn't the return block itself.  Then the JTAG edge doesn't get the early-return prediction (`a51_fpred.py`: bb 2 72.0% nonequal only, bb 3 19.1%), and the CFG at expand matches src's.  Three ways to get that statement:

| Class (sweep labels) | Helper | buildFlash loose/strict | What's left |
|---|---|---|---|
| r (e_*, s8_*, s9_*, s18_r_s) | `static int initFlash(uint8_t *salt)`, `int fuse = 1; memset(salt, 0, 16); if (xb.type != BUILD_JTAG) { fuse = xb.glitch2mfg != 0; if (dev) return 1; } return fuse != 0;` (also `!!fuse`, `fuse ? 1 : 0`, `fuse > 0`, `fuse == 1`, BOOL return / local; 135 spellings in s8, every one the same) | **2/2** | the findFile(24) loop in `if (fuse)`: `cmp ecx,eax` for `cmp eax,ecx` |
| b (rt__Bool_*, t_*__Bool_dret2, c_bi_*) | the same with `static _Bool` and `return fuse;` (or `!= 0`) | 5/41 | the setne writes bl with no `xor ebx,ebx`: PRE moves the `(_Bool)` conversion into the arms, the PHI becomes `_Bool` and the zero extension comes after the join (REE drops it) |
| o (s13_op3, s14_*, s16 o) | `static void initFlash(uint8_t *salt, int *fuse)`, `int f = 1; memset; if (!JTAG) { f = g != 0; if (dev) { *fuse = 1; return; } } *fuse = f;` | 8/8 | four other loop compares (1057, 1700, 1872, 1887: the overflow writers' findFile loops and one more) |
| u (rt_uint32_t_*, rt_unsigned_*, s10c) | unsigned / uint32_t return type | 9/44 | ce1 makes `setne dl; movzx; cmp 2; cmovae ebx,edx` (the default the other way round) |
| short / uint16_t / uint8_t / char return | | 12 to 13 | |

- Without such a statement (plain `return fuse;`, long return, a PHI-only return, the JTAG test as `== JTAG` with `return 1`): 3/285 (`dret`, `dret2`, r_*, t_int_int_*, t_long_*) or the no-early-return form's 11/293 (`flag` bodies: r_flag1, r_jt1, r_nj3).  Callers that test the result (`if (initFlash(salt)) fuse = 1; else fuse = 0;`, `fuse = 0; if (..) fuse = 1;`, s10_1..3): 11/46 (the u class's cmovae).  `fuse = initFlash(salt) != 0` (c_ne_*) or `!!` folds to the plain call.  A raw `fuse = xb.glitch2mfg;` with `return fuse != 0;` (g_*) moves the setne after the dev test: 7/43.

### The tie (SSA numbering)

- Six inlined findFile loops in buildFlash compare the IV with a copy of `xb.nFiles` that ch2 makes when it copies the loop header (found with `-fdump-tree-all`: `_13 = xb.nFiles` first shows up in ch2).  The canonical operand order follows the SSA versions.  In src the first copy gets a fresh name (`_758`); in the r class it reuses a freed low name (`_13`), so the compare is built the other way round.
- Root, as far as the dumps show it: src's early body has a fuse PHI (`fuse_9`; early PHI versions are handed out in variable order: base 1-2, area 3, raw 4, k 5-8, **fuse 9**, blocks 10, r 11-12, i 13, found 14-15).  With the helper, buildFlash has no fuse PHI before IPA, so every later low version is one less (blocks_9 ... found_13 / found_14).  vrp1 frees the found names and they come back in a different order at ch2.  The helper's inlined names also shift everything allocated after IPA (`fixup_cfg4` max version 644 in src, 651 in r, 715 in o).
- Sets of wrong loop compares (line numbers in buildFlash's disassembly; src has none):

| Variant | Wrong compares |
|---|---|
| r, `(salt)` (s18_r_s, every s8 / s9 / s12 / s16 r spelling) | 123 |
| r, buildFlash's `fuse` unsigned / uint8_t / uint32_t / char / short (s11, s22) | 123, 173 |
| r, `(salt, len)` / `(salt, xb.type == JTAG)` (s20, s18_r_sj) | 123, 1700, 1872, 1887 |
| r, `(salt, xb.type)` (s18_r_st) | 123, 173, 1700, 1872, 1887 |
| o, `(salt, &fuse)` (s13_op3, s14 int / BOOL, s16 o) | 1057, 1700, 1872, 1887 |
| o, `(salt, type, &fuse)` / `(salt, len, &fuse)` (s18_o_st, s20) | 1700, 1872, 1887 |
| o, `(salt, jtag, &fuse)` | 123, 1057, 1700, 1872, 1887 |

  Parameter order doesn't matter, only the count (s20).  None of these change any set: fuse's declaration position (s19, 54 variants), the `if (fuse)` block's spelling (s12: an `i` index, an `e` declared outside, an index local; `xb.files + n` is 15/545), the dev test and glitch spellings, a local for `xb.type`, and attempt 65's `ld` restructure (s21, an equal base).  Attempt 65's other restructures cost what they cost on src (66 to 838).
- The helper is inlined first of buildFlash's six IPA inlines (ipa-inline dump: `build.c:2529`, net -6), since the inline transform goes in block order, so its names land straight after buildFlash's own.

### Is the r form landable if the tie closes?

- It would be borderline twice.  First, a helper that clears the salt and returns the fuse flag: attempt 53 judged it not something an author writes, though it reads as `initFlash`, "set up the flash build's salt and say whether virtual fuses are used".  Second, `return fuse != 0;` on a value that is already 0 or 1: live but redundant, chosen because gcc keeps it in the return block.  A `_Bool` return (class b) would be the natural way to write the second, and options.c already has `_Bool` helpers, but it loses the zero extension.

### Don't retry (attempt 69)

- Reading tree-sink for an order effect: the decision is the frequency ratio only.
- The memset helper with a PHI-only return (`dret`, `dret2`, `return fuse;`, long / BOOL return types): the JTAG edge goes to the return block (early return, and the shared `fuse = 1` block).
- `!= 0` / `!!` / `? 1 : 0` in the caller (folded), caller tests of the result (cmovae), the raw glitch2mfg value tested at the end (setne after the dev test).
- Spellings inside the r or o class (s8, s9, s14, s16: the GIMPLE is the same), parameter order, fuse's declaration position, the fuse block's spellings, and attempt 65's restructures.

### What to try next

- The tie: the r class's only miss is the findFile(24) loop in `if (fuse)`.  It needs src's free-list state at ch2, which src gets from the early fuse PHI.  Look for a natural statement that gives buildFlash one more early PHI, numbered before `found` (a variable declared before `blocks`, or fuse itself), without changing the code, or for another way to change which name ch2's first header copy gets.  Every parameter added so far also breaks the overflow writers' three loops (1700, 1872, 1887), which the r class with one parameter gets right.
- If the tie is closed, the result is a candidate for the user's review (the two borderline points above), not a plain landing.
- The b class (`_Bool` return): find what would put the zero extension back on the setne (after PRE the PHI is `_Bool`, and the int conversion comes after the join).

### Costs now (strict/loose, removed alone; 1 trick, unchanged)

exp_devgl 43/7 (unchanged).  With the r-class initFlash helper in its place: 2/2 (one loop compare's operand order).  The full build was not run for it, since it doesn't match.

## Attempt 70

Goal: attempt 69's r-class near miss (`fuse = initFlash(salt);`, `return fuse != 0;`: 2/2, the findFile(24) loop in `if (fuse)` compares `cmp ecx,eax` for `cmp eax,ecx`).  src as of 7198bf70.  New scripts in `tools/wip/dehint/bdgen`: `a70_dev.py` (sweeps s1..s5, run with `python tools/wip/dehint/bdgen/a60lib.py tools/wip/dehint/bdgen/a70_dev.py -p 0 -o "-" [-f label] [-k label]`), `a70_dump.sh <variant.c> <name> [gcc flags]` (one `-fdump-tree-all` compile into build/bd/a70/<name>), `a70_names.py <dumpdir> [fn] [first] [last]` (per pass, the SSA versions that disappear / appear in a function), `a70_src.py <dumpdir> [pass] [fn]` (for each version a pass (ch2 = 107) reuses, the earlier pass that released it).  Dumps in build/bd/a70 (not kept).  gcc.gnu.org answered tree-ssanames.c with the Anubis bot check, so nothing was read from the gcc sources.

### Readings

- Optimized dump: src `i_205 = i_751 + 1; if (i_205 != _758)`, r `i_197 = i_750 + 1; if (_13 != i_197)`.  The canonical order puts the lower version first, and the IV increment keeps its pre-ch2 version (~200), so the nFiles copy that ch2 makes for loop A (the `if (fuse)` findFile(24) loop) needs a version above it.  ch2 makes 74 names and every one is a recycled version (max version is unchanged); r's loop A gets `_13` (found_13, released by dce2), src's gets `_758` (r_758, a vrp1 copy released by dce2).
- So it is the order of ch2's free list, not the numbering of any one name.  Moving `found`'s declaration (s1: 15 positions and types) only renames the low name loop A gets (`_3` with found first): always 2/2.
- What differs between src and r after vrp1 (a70_names.py): r's inlined return block is `_588 = fuse_587 != 0; _589 = (int) _588;` (vrp1 turns `_589` into a copy of fuse_587), so dce2 releases `_588`, copyprop1 one more name (`_589`, 20 against 19), mergephi3 `fuse_587` (now mergeable), which phiopt1 takes back.  The free list is not a plain stack (src's phiopt1 reuses `_70`, released in dce2, although copyprop1 released 19 names after it; r's phiopt1 reuses mergephi3's fuse_587), which looks like released names being queued and flushed at some passes, but the model wasn't needed: one name fewer was enough.
- s2 / s4 (return expressions): every form whose GIMPLE is a single int statement that vrp1 reduces to a copy is **IDENTICAL**: `fuse & 1` (also `(fuse & 1)`, `& 1u`, `fuse &= 1; return fuse;`, `fuse = fuse & 1; return fuse;`), `fuse > 1 ? 1 : fuse` / `fuse < 1 ? fuse : 1` / `fuse >= 1 ? 1 : fuse` / `fuse <= 1 ? fuse : 1` (MIN), `fuse > 0 ? fuse : 0` / `fuse < 0 ? 0 : fuse` / `fuse >= 0 ? fuse : 0` (MAX), `fuse % 2`.  Compare forms (`!= 0`, `== 1`, `!(fuse == 0)`, `!!`, `? 1 : 0`, `(unsigned)fuse != 0`, `1 - (fuse == 0)`, `fuse ? 1 : fuse`, `if (fuse > 1) fuse = 1;`) stay 2/2; `> 0` / `>= 1` 13/49; folded forms (`| 0`, `^ 0`, `* 1`, `>> 0`, `- 0`, `-(-fuse)`, `& ~0`, `abs`, `fuse ? fuse : 0`, `if (fuse < 0) fuse = 0;`) are PHI-only returns again (3/285).
- s3 (buildFlash's fuse type x helper return type x helper local type, `!= 0` and plain return): nothing below 2/2 (char / uint8_t / unsigned caller 4/4, `_Bool` returns 5/41, `_Bool` locals 8/290 or 9/44).

### Landed

`static int initFlash(uint8_t *salt)` before patchConsoleBlmod with `return fuse & 1;` and a "Borderline, for review:" comment; buildFlash calls `fuse = initFlash(salt);`.  `python tools/re/fncmp.py src/build.c buildFlash` MATCH, `sh build.sh` ends with 10dac648197fa5cdbb82d975ab9ff11f64075c9686908dfd9a33edc533f1971c, progress 617 / 617.  README's tricks list drops build (options and mode_client renumbered, 2 files listed, 23 without tricks); bdhints.py's H is empty.

### Don't retry (attempt 70)

- `found`'s declaration position or type for the loop compare (renames the low name only).
- Caller / helper / local type combinations with `!= 0` (s3).

### What to try next

- build has no tricks.  If the user rejects `& 1`, the MIN / MAX / `% 2` spellings are the same lever; a natural form would need some other single-statement int return expression on a 0/1 value that vrp1 reduces to a copy, or one statement fewer elsewhere between vrp1 and ch2.

### Costs now

None: 0 tricks.

## Review (2026-11-10): all borderline shapes settled, four respelled

The user asked for build's sixteen borderline shapes (BORDERLINE.md) to be reviewed and
resolved. Each was first made plain on its own, then all of them again on the base the
matches left, then every pair of the remaining plain spellings (133 pairs). Four plainer
spellings give the same bytes and are in src; the other twelve stay, with `(approved)` on
their tags and this review's numbers in their comments. Full build SHA256
10dac648...1971c.

Tools (tools/wip/dehint/): `bdrv.py <variants.py> [label ..] [-b base.c] [-v label [fn]]
[-o label out]` scores variants of src/build.c against build/bd/reference.o with bdlib at
plain -O3; a label may join variants with `+`, and an edit given as `(header, old, new)`
goes to a copy of src/<header> searched first. `bdrv_a.py` (each shape plain alone),
`bdrv_b.py` (more spellings), `bdrv_c.py` (the tail test, one-call loadBl24). They were
written against 46fb4f14's build.c (`git show 46fb4f14:src/build.c > build/bd/rv/a0.c`);
the later rounds ran on a0 plus the matches so far. Counts are differing disassembly lines
in the functions named; loadConsoleBlFiles 18 / blmodMissing 2 / buildFlash 20 in a
loadBlFiles variant are call offsets.

### Same bytes, now in src

- **extractSmcConfig's struct copy:** `memcpy(e->data, buf + i, 0x400)` matches again.
  Attempt 5 put the struct copy in place of memcpy with an expect and a pin; what made it
  needed is gone since. `struct smcConfigData` is gone with it.
- **case 24's devkit arm:** `r = loadBl24(e);` matches (25 loose when attempt 49 tried it).
  The written-out body, its leading `r = 0`, and the tag are gone. The else form of the
  written-out body is the same bytes too; with `||` it is 34, written out in both arms 341.
- **loadFileCrc's log test:** `pad && size != e->size`. Attempt 13 found the size compare
  in the Linux build too, so it's the original's. The compare alone (or `e->size != size`),
  or `(size & 15) &&` in place of `pad &&`, makes ipa-cp clone loadFileCrc
  (`.constprop`, whole object); `pad && (size & 15)` alone 136. Still tagged (approved):
  `pad &&` is redundant.
- **The tail:** `if (xb.type > BUILD_DEVGL16) setKitBuild(i, type); else if (r == -1) goto
  fail;`. r is 0 or the signature check's -1 there. `r == -1` gets the opcode prediction
  `(int)r < 0` got; `if (r)` is 11 in every arrangement (kit test first, else-if, nested);
  `int r` with `r < 0` 478, with `if (r)` 324; one `&&` test with the kit test after 66.
  The kit-first and old nested forms with `r == -1` are the same bytes as well. Still
  tagged (approved): `r == -1` says what `r` would.

### Why the rest stay

| Shape | Plain spellings tried | Reason |
|---|---|---|
| align16 | macro at every site 2 | patchBlsBlmod's two spill stores (attempt 7's reading); a helper is ordinary C |
| findFileOffset / findFileSize `int` | `uint32_t` either or both 82 | calcBlAreaSize's sum register (attempt 58); findFile returns int |
| loadInputFile's `int crc` | `uint32_t` (ipa-cp clone, whole object) | int is the author's usual parameter type |
| patchCpuFan's own test | none 52, in place 52, caller's test gone 171, the gpu section's `goto` 518 | the warning blocks swap (the cpu one ends up before the gpu one) |
| extractSmcConfig's `int size` | `uint32_t` 8 (bound compares' operands swap) | the author writes `int size` / `int len` parameters throughout |
| useBuiltIn | written out 47 | setFileData is the same helper with calloc |
| defaultBl60's memmove | memcpy 42, through useBuiltIn 42, useBuiltIn with memmove 90, setFileData 234 | inline size estimate (attempt 59) |
| loadBl24's two calls | `\|\|`, nested ifs, good case first, an r local: all 139 | crossjump needs two copies (attempt 49) |
| setKitBuild's ignored return | void 61 | attempt 68's return-block statement; build.c ignores setPatchSlot's, imgAdd's and suLoadDir's returns |
| case 27's r sequence | `&&` chain 23, nested ifs 23 | IRA allocno order (attempt 34) |
| addBlsToImage's 25 before 23 | 23 first 175 (.rdata) | vrp1's assert order (attempt 24); neither order is plainer |
| isUpdateBl's lone ifs | one `\|\|` chain 18 | attempt 23; the Linux ranges fit either |
| initFlash's `& 1` | `!= 0`, `!!`, `? 1 : 0` 2; `return fuse` 285; `_Bool`/`uint8_t`/`char`/`uint32_t` local or return 41-44; in buildFlash 43; early returns 360 | attempt 70's SSA tie |

The best pairs are additive (al_macro + if_ne 4, al_macro + sc_u32 10, sc_u32 + if_ne 10,
al_macro + r_ne 13): no two shapes interact.

### Don't retry (review)

- Each plain spelling in the table, and their pairs.
- `goto cpuwarn` for patchCpuFan in the gpu section's style (518: the cpu literal moves).
- The memmove / useBuiltIn / setFileData combinations for defaultBl60.
