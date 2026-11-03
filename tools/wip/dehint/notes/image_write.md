# image_write (whole object)

Tools (all compile in about 0.6 s, a sweep of 100 takes 20 s):

- `tools/wip/dehint/iwlib.py <file.c> [-p N|-np] [-v [fn]]`: compile as build.sh does, compare with
  `build/iw/reference.o` (copy of the last matching build/obj/image_write.o; recreate it from a matching
  build). Prints `IDENTICAL` (every byte of the .o) or lines per function, plus any data section that differs.
- `iwtricks.py singles|pairs|greedy|show a,b,c [-o out.c]`: the tricks as named edits. `IWBASE=<file>` picks
  the base source. `iwsubsets.py names...`: every subset.
- `iwsweep.py gen_iwN.py [-n top] [-k label]`: cross product of source edits from a generator; best variant
  goes to `build/iw/gen_iwN_best.c`.
- `iwdump.py <file.c> <dir> <func> [-fdump-...]`: dumps cut down to one function.

## Attempt 1

Landed in `src/image_write.c`, with `sh build.sh` reproducing the SHA256. Where this section says "the draft", start from that
file. README's old count of 18 had 7 dead tests where the source has 8, so the real change is 19 -> 18 tricks; the "17" and "16"
below are off by one in the same way.

### Confirmed

- **buildImage pin (`"b"(bb)`) removed**: 17 tricks. `if (xb.type != BUILD_JTAG) { switch ... } else { jtag }`, plain
  `if (xb.bigBlock)`. `mov ebx,xb.bigBlock; test ebx,ebx` isn't a pseudo: it's peephole2 turning `cmp mem,0`
  into load + test with a scratch from `peep2_find_free_register`, whose search start rotates. Peephole2 walks
  blocks in reverse, so the arm later in the source takes the scratch first: JTAG's `bigBlock` must be
  processed first (edx), then the switch arm (ecx busy, so ebx). **General lever: `mov rX,mem; test rX,rX`
  register differences are block order, not allocation.** gen_iw2.

Result: **18 -> 17, whole object byte-identical to reference.o.** Nothing else removed so far. Near miss:
`drafts/image_write_near.c` (from the draft: pin_end and dead_add2 gone, shapes next=2, t=1, pages=1 in iwanneal's terms)
differs by exactly one `cmp esi,edx` -> `cmp edx,esi` in writeFsTable's big-path (0x2c) copy, with the optimize attribute kept
(`if (ivtmp_273 != _366)` where the reference has `_130 != ivtmp_237`: a version-number order). It'd be 16 if that one flips.
Tried on it without success: 2880 writeFsTable forms (gen_iw15), 2672 random neutral shapes (`IWFIX='{"t":1,"next":2,"pages":1}'
iwrand.py 420 7 pin_end,dead_add2`), annealing 3100 states (iwanneal.py --from). Note pin_end only stops mattering once dead_add2 is gone.

Warning: iwrand/iwanneal only understand names in iwanneal.TRICKS; other names (lab_c1, exp_file) are silently ignored, so a
"hit" on them means nothing. README counts 7 dead tests; the source has 8 (6 imgAdd + 2 imgAddFile).

### What to try next

1. The near miss: anything that makes the end value's SSA version lower than the iv's in the big copy, or try removing dead_add1 or
   dead_add4 too from there (each costs writeFsTable lines: 26 and 50 at best alone, with shapes `range=1, next=2, t=1, pages=3, wf_big, wf_small,
   big_lba, blkvar=2, type0`).
2. Removing all of imgAdd's dead tests loses the off-0 clone (evaluation under 500): needs a natural source of time benefit on off in the loop.
3. imgAddFile fully natural (`gen_iw10`, `lim+ret`, 147 lines; the control flow is mostly right but the error block is 28%, round 2).
4. imgAddMobile (gen_iw8 `v2-gofits`, gen_iw14: 62 lines at best, needs a register fix) and it's goto-heavy, so at best a candidate.

Don't retry: variable reuse for the buildImage pin (no effect, solved anyway), helpers for imgAddMobile, plain-C bodies for dead_add2/4 (gen_iw16, no
exact match with them other than the asm one).

### What removing each trick does (from the draft, other tricks kept)

Lines = differing disassembly lines; `iwtricks.py singles` reproduces this.

| Trick | Lines | Where |
|---|---|---|
| `opt` (no-tree-scev-cprop) | 4 | writeFsTable: `cmp edx,ecx` swapped twice in the small-path (0x30) copy's page loop |
| `pin_end` | 4 | imgAddFile: `end > raw` becomes `raw < end` |
| `pin_t` | 10 | imgAdd: slots of t and partial swap (LRA sorts by frequency; the asm raises t's) |
| `dead_add2` | 12 | imgAdd sched order, writeFsTable compare order |
| `exp_mob` | 26 | imgAddMobile: fits block placed after the else-if block |
| `dead_add1` | 38 | |
| `dead_add4` | 76 | |
| `dead_c1` / `lab_c1` | 180 / 107 | imgAddFile |
| `xmalloc` | 180 | finalizeImage: memcpy prologue gone |
| `dead_lenpp` | 182 | imgAddFile alone; only 8 with pin_end too (`raw < off`, `raw < end`) |
| `lab_lnp2` | 183 | imgAddFile |
| `dead_add3`, `5`, `6` | 170-206 | |
| `pin_hdr` | 243 | finalizeImage |
| `param` | 292 | |
| `exp_file` | 332 | |

Subsets of {opt, pin_end, pin_t, dead_lenpp, dead_add1..6} (1023 tried, `iwsubsets.py`, result in
build/iw/subsets_10.txt): nothing is identical, the differences nearly add up. Best by size: 5 removed
(`opt,pin_end,dead_lenpp,dead_add4,dead_add5`) 28 lines; 8 removed 81 lines; 9 or 10 lose the off-0 clone.

### Mechanics found

- **imgAddMobile's expect + param needs exactly 50/50 on the small path's fits test.** bbro: fits must have
  key >= the else-if traces (edge freq >= 2500, p >= .5) and the shared error block must beat it (p <= .5).
  The predictors: both arms have calls (71/29 cancel), and PRED_TREE_EARLY_RETURN fires on an arm that goes
  straight to the return block unless the arm is the block just before it (`e->dest != bb->next_bb`). In
  natural source the error arm is last, so only fits fires: 39%. Both arms firing cancels to 50, so neither
  may be the last block before the return block. Helpers don't work (not inlined at profile_estimate: bb 2 gets
  71%). Big path after the small one: exact probabilities, but bbro's tie takes the lower-index successor, so small
  comes first (gen_iw6 `first-*`, 137 lines). gen_iw7 (tail after if/else): 99, split_edge then places the
  store block before the tail. gen_iw8 `v2-gofits`, with two gotos: control flow correct, 62 lines, only esi/edi
  and lea/add in the big path. Candidate shape at best (`goto place`, `goto fits`).
- **finalizeImage `pin_hdr`:** the hdr prephi (r201) is the first spill candidate in the region of l5 (pri=1, cost 232),
  so it pops after r189 and takes ebp. The asm adds a use (pri=2, cost 368) and it's no longer first. 195 shapes of
  the ECD loop (gen_iw3, gen_iw4): best 219. To try: shortening r201's range (pri = cost / excess pressure points).
- **`xmalloc`:** CCP sets malloc's alignment only through gimple_call_builtin_p, and bit-CCP keeps it through casts,
  PHIs and +528 steps; no natural form found. Not attacked further.
- **`pin_t`:** r235 = partial's compare, r236 = t. MEM cost 360 vs 267, the asm brings t to 402. Reordering `t`, its type or
  decls is no use (gen_iw9); the forms of `partial` (gen_iw11) give 10 at best.
- **`opt`:** 136t.ldist is the first differing dump: without the attribute sccp leaves loop-exit forwarder blocks (e.g. the FS
  loop's), which changes names later. 60 forms of the loop and calls (gen_iw12, gen_iw13) stay at 4.

## Attempt 2

Written as I go. `drafts/image_write.c` holds the best verified reduction.

- **pin_end removed, whole object identical (18 -> 17)**: `if (end < off && (len & 0x3fff) > 0x3fff) len++;` in imgAddFile. The dead
  len++ test that stays anyway now uses `end`, so `end` lives through the early passes without the asm (gen_iw18 `nopin+L2`). General lever:
  a value kept by an asm output can be kept by a conjunct of a dead test that's staying anyway.
- Near draft's compare: `iw_names.py <dumpdir> writeFsTable [versions]` lists per pass which SSA versions appear/vanish. iv2 (`ivtmp_273`) comes from
  split-paths' copy of the latch, end (`_366`) from ivopts. 2560 forms of the remaining dead tests (gen_iw17) didn't flip it.
- **Dead tests merged (17 -> 16)**: gen_iw19 `m34ob`: `if (x + 0x4000 < first || (len & 0x3fff) > 0x3fff) blocks++;` replaces imgAdd's two dead tests add3 and add4
  (and an empty asm), identical. Merges that aren't identical: m23 (6 lines), m234 (6), m32 (4, writeFsTable).
- **c1's cold label gone (16 -> 15)**: gen_iw21 `ab7`: `if ((end & 0x3fff) > 0x3fff) abort();`. PRED_NORETURN is first-match at 0%, same as PRED_COLD_LABEL. Gimple was equal but for one SSA
  version (npages_128 vs _214 in the big copy, the bad version flips one compare, which flips the loop layout, 116 lines); using `end` in that test fixes it.
- imgAddFile simplified on top: `end` and the `end < off` conjunct are gone again: plain `if ((len & 0x3fff) > 0x3fff) len++;` and, in the fits arm, `if ((len & 0x3fff) > 0x3fff) abort();`
  are identical (gen_iw22 `Lp+Cl`). So pin_end's job is done by the cold->noreturn change. `exp_file` then costs 78 lines rather than 332; PRED_CALL on the error arm gives 71/29 and the expect 50.
- lnp2 removal: gimple identical, only bb freq 630 -> 40 (`if (npages != 0)` guard after `len > 16383`, 15/85 from the hot label vs 45/55): frequency only (183 lines).
- noopt: the 2 small-copy compares flip, gimple otherwise equal: `iw_ifs.py <file> <fn>` shows that sort of thing fast; `iw_passdiff.py` finds the first pass that differs structurally.
- **lnp2 hot label:** `if (partial <= 0) npages = 32;` (gen_iw30 `le`; `partial > 0` too) instead of `!partial` + label: PRED_TREE_OPCODE_POSITIVE gives 73%, the guard block's frequency is 900*(2p-1) = 414 (label: 85% -> 630). Only 12 lines left, in imgAddFile: slots 0x30 (npages) and
  0x34 (off+len) swap. LRA sorts spill slots by frequency, higher frequency = lower address. Needs p higher, or end's references lower. gen_iw31 forms don't do it.
- **pin_t mechanism (better than attempt 1's):** the t test is split by threading in two blocks, 765 and 135, REG_FREQ rounds to 76 + 13 = 89, whereas partial's one test has 900 = 90. So partial wins the slot
  sort by one unit of rounding. The asm adds a use. A def of t earlier gets sunk (gen_iw29 t0: 16 lines). No natural fix yet; with a 50/50 split (no lnp2) it'd be 45 + 45 = 90, a tie that regno decides.
- All three loop dead tests in one if, no empty asm left in imgAdd: `if (x + 0x4000 < first || x > first + 0x4000 || (len & 0x3fff) > 0x3fff) blocks++;` plus `end` in imgAddFile's tests (build/iw/a2/m2D.c): 4 lines in writeFsTable, gen_iw33 sweeps that.

### Attempt 2 result

`drafts/image_write.c`: whole object byte-identical to reference.o with the same flags (`-O3 --param builtin-expect-probability=50`). Removed: `pin_end` asm, `c1` cold label, one dead `if` (add3 + add4 merged; also one empty asm gone).
Count: param 1, dead `if`s 7, pins 2 (t, hdr), expect 2, label 1 (lnp2), optimize 1, xmalloc 1 = **15** (16 if the merged `if`'s two dead conditions are counted as two tests).

Levers that worked, in order of value:
1. **Noreturn call for a cold label.** PRED_NORETURN and PRED_COLD_LABEL are both first-match at 0%. `if (dead) abort();` replaces `if (dead) { c1: cold; name++; }`. Dead arm vanishes before expand, so no `_abort` import.
2. **Merge dead tests** into one `if`: the SSA names are nearly the same. Not every merge works, see gen_iw19 and gen_iw33.
3. **A dead test can keep a value alive** instead of an asm output (`end < off && ...`, gen_iw18). Not needed in the end, but worth retrying elsewhere (filelist_ini, etc.). Check that the value is really initialized.
4. **`partial <= 0` for the 73% PRED_TREE_OPCODE_POSITIVE** (comparisons with 0 via ==/!= get no prediction, `<= 0` does).

Tools added: `iw_names.py` (SSA versions appearing/vanishing per pass), `iw_passdiff.py` (first pass with a structural difference between two dump dirs),
`iw_ifs.py <file> <func> [base]` (final conditionals and bb frequencies; run this first on any big diff: often one compare or one frequency), `iwanneal2.py <secs> <seed> [fixed]` (annealing on the new base, `IWDRAFT=` picks another; log in build/iw/a2).
For slot questions: `grep "Slot . regnos"` in -fdump-rtl-reload-details, then count pseudo refs by bb freq in -fdump-rtl-ira-all (higher freq, lower address; REG_FREQ = freq/10, floored per ref).
Generators: gen_iw17 (dead test forms on near), 18 (pin_end), 19 (merges), 20-22 (abort), 23, 27, 30, 31 (lnp2), 24 (exp_file), 25, 33 (add2/opt with merges), 26 (subsets), 28, 29 (pin_t), 32 (add2 bodies).

Per trick, from this draft (`IWBASE=tools/wip/dehint/drafts/image_write.c iwtricks.py singles`; the old names for pin_end, c1, add3, add4, lenpp no longer apply):

| Trick | Lines | State |
|---|---|---|
| `opt` | 4 | two small-copy compares flip; 1000 random shapes stay at 4; gimple otherwise equal |
| add2 (`x > first + 0x4000`, empty asm) | 12, 2 with shapes | `drafts/image_write_near2.c`: merged into the one `if` (no asm in imgAdd) with `end` in imgAddFile's tests: **one compare off**, same as attempt 1's |
| `pin_t` | 10 | only the two byte slots swap: rounding, see above. Natural fix not found |
| `lnp2` | 183; 12 with `partial <= 0` | `drafts/image_write_nolnp.c`: slots r148 (npages, 8 + guard freq/10) and r136 (off+len, about 57 by my hand count, so the threshold is an estimate) swap. Guard freq = 900(2p-1), p=.73 gives 414, needs >= 500: p >= .78 |
| `exp_file` | 78 (was 332) | PRED_CALL 71/29 on the error arm vs the expect's 50; moving the dead test after the strcpy doesn't help (gen_iw24), and the arm's first block has no call |
| `exp_mob` | 26 | not attempted beyond notes from attempt 1 |
| `xmalloc` | 180 | no natural form; gimple_call_builtin_p needs matching arg types, so a function-pointer cast might avoid it (from memory, untested) but that would be a disguised hint |
| `pin_hdr` | 243 | not attacked |
| a1 / a5 / a6 | 40 / 176 / 66 | see gen_iw26 output; `a1+c3` 18 lines, `a1+a5+a6+len` 28 lines (removes 4!) are the promising subsets |

The writeFsTable compare (`ivtmp_273 != _366`, big copy): `_366` is `end` from ivopts, `ivtmp_273` is the latch copy from split-paths. Both were first popped by cunrolli (360 116 366 273 vs the reference's 195 323 364 351) and released at fre3; in the reference those go to other roles and `end` and the copy get 130 and 237 from the ccp2 batch. So the difference is how deep ivopts reaches into the free list. The list doesn't behave as a pure stack judged from dump appearance (vrp1 pops older names first), so "gone from dump" isn't the release moment. Sweeps: about 2560 (gen_iw17) + 3024 (gen_iw33) on top of attempt 1's 8600 didn't flip it. Forms that only change later passes never change it; it wants a change before cunrolli in writeFsTable's inlined copies.

What I'd try next: (1) `a1+c3` and `a1+a5+a6+len` with `iwanneal2.py` fixed on them; those remove real dead conditions, and every line is a compare or sched order. (2) a p >= .78 predictor for lnp2, or fewer references on r136. (3) Natural forms of a 'first' bb before cunrolli for the near2 compare. (4) exp_mob with a noreturn block placed between the error arm and the return block (makes both arms fire early-return, cancels to 50) but that adds a dead test for one expect, so no net gain unless exp_file goes too, then param goes as well (-3).
Don't retry: plain-C single bodies for add2 (gen_iw32: 8 lines at best), noreturn on lnp2 (gen_iw23), moving t's def (sunk back; gen_iw29), abort for the len++ test (gen_iw22 La, Lb).

## Attempt 3

Written as I go. Base: landed src/image_write.c (aac860d6), 16 tricks. New tools: `iw3.py singles|subsets|show` (the 16 tricks as named edits on the
landed source, `lnp2le` = `partial <= 0` form), `iw3anneal.py <secs> <seed> <fixed> [--workers N] [--free a,b] [--pen N]` (annealing over natural shapes; log and hits in build/iw/a3).

- Singles on the landed base: opt 4, pin_t 10, lnp2le 12, a2 16, exp_mob 26, c3 38, a1 40, a6 66, exp_file 80, c4 80, len 140, a5 174, xmalloc 180, ab 182, lnp2 183, pin_hdr 243, param 292. All 2047 subsets of {a1,a2,c3,c4,a5,a6,len,ab,opt,pin_t,lnp2le}: nothing identical (build/iw/a3/subsets11.txt).
- **Lever found:** a1,c3 removal leaves 18 lines; `t` order fixes imgAdd (8), `end < off && ...` in the len++ test fixes imgAddFile (4), and giving a2 a plain-C body that writes `blocks` (`if (x > first + 0x4000) blocks += 2;`, no asm!) fixes constprop.2 (4): c3's job in constprop.2 was keeping `blocks` a loop PHI (c4 folds there because len is constant). build/iw/a3/v2.c: a1, c3 and the asm gone, 2 lines left: the known writeFsTable big-copy compare.
- The near compare in v2: ivopts pops run [325..330] in order 419 start, 419 incr, 432 incr (327), end (328), ... so incr < end inside a run. The reference has incr 239 from another run than end 130. So a shift of the pops before it (ivtmp.408, 414 etc. of the small copy, or names released above) moves the run boundary. `iw_ver.py` and build/iw/a3/roles.py-style lists show it.
- Ruled out for the compare in v2: writeFsTable forms (gen_iw39 = gen_iw15's 1440, gen_iw40's 576 length-argument forms).
- xmalloc: index forms of the raw pointer (gen_iw34): CCP keeps the alignment through `mem + off` and the ivopts iv, still `rep movs` without prologue. Worse than `raw`.
- lnp2: no PRED_GOTO in the C front end (gen_iw36 goto forms give the same 27%).
- exp_file: dead conjunct in the fits test so the error block isn't dominated (gen_iw37): loses constprop.4 or 350 lines. exp_mob: one error block in the source (gen_iw35): 131+ lines.
- Sweeps on v2 for the one compare: gen_iw41 (3456 forms of the dead tests' conds and bodies) nothing; iw3anneal 2692 states nothing. `iw3anneal.py 0 0 - --probe '{}'` (IW3BASE=file): every single shape change with lines and writeFsTable's four iv compares; this is how to see who moves what. The wanted tuple is `ivtmp.44x != _e`, `_e != ivtmp.43x` (both), `_e != ivtmp.43y`.
- v3.c = v2 with a6's body `start++`: big-copy compare right, FS loop compare wrong (`_170 != ivtmp.448`: 66 lines but one root, RA follows). v5.c = v3 + `i = blk - xb.fsStart` + `setBeU16(off >> 14, ...)`: FS right, outer (ivtmp.435) wrong: 4 lines.
- gen_iw42 (a1, c3, a2 forms x t, e, a5/a6 bodies, 480) and gen_iw43 (near sets x writeFsTable forms, 320): nothing identical; 4 lines at best: `A0te` (a2 gone, t, e: both big-copy compares wrong), `A1b2te` (a1 gone, a2 body `blocks += 2`, t, e: imgAdd 2 + writeFsTable 2).
- Single-shape probes: only `pad == 1 && tail` (non short-circuit, its names live until ccp2 in the inlined copies) gets all of writeFsTable's compares right, but costs 512 lines in imgAdd and the clones. Temporaries around the memset die in early forwprop, before inlining, and don't move the free list (gen_iw44, 140). So: to shift names in the inlined copies a form must survive early opts and fold only after inlining.
- gen_iw45 (near sets x `pages`, `next`, `tail`, partial's type, a6 bodies, writeFsTable store/tail forms, 1728): two 2-line families: `A0te+pg1+nx2` (a2 gone; drafts/image_write_near3a.c) and `A1C3b2te+pg1+nx2+sb` (a1, c3, asm gone; drafts/image_write_near3.c). Each is the one writeFsTable compare: the split-paths copy of ivtmp (273) below `end` (366). That copy's name was `i_273`, released at fre3 (the reference's is `_237`, released at ccp2), so the free list isn't simply LIFO from what the dumps show.
- Annealing from each 2-line file with `iw3anneal.py` (with writeFsTable shapes): seeds 51 and 52, 4250 states each, seeds 41 and 42, 2250 each: nothing identical. Logs in build/iw/a3.

### Attempt 3 result: NO MATCH

Nothing identical with fewer tricks; src/image_write.c stays best at 16. `drafts/image_write.c` here is only a plain copy of the landed source, because `iwanneal.py` (imported by iw3anneal) opens it.

Closest: `drafts/image_write_near3.c`: a1 and c3 removed and imgAdd's last empty asm gone (would be **14**), natural shapes only, **one flipped compare** in writeFsTable's big copy (2 lines, `cmp esi,edx`). `drafts/image_write_near3a.c`: a2 removed (would be 15), same one compare. Everything else in the object is byte-equal in both.

What it takes, in order of what each fixes (from `iw3.py show a1,c3` at 18 lines):
1. `t` after `partial`: imgAdd's register order (8 lines).
2. `uint32_t end = off + len;` and `if (end < off && (len & 0x3fff) > 0x3fff) len++;` in imgAddFile: `rawSize` vs `end` operand order (4 lines; attempt 2's lever again).
3. a2 with plain body `blocks += 2` instead of the asm: keeps `blocks` a loop PHI in constprop.2, where c4 folds because len is constant; that fixes the `b` vs `blocks` compare (4 lines). **An asm can become plain C here on its own**, but that alone doesn't lower the count.
4. `pages = len % 512 ? ...`, `start + i - xb.fsStart`, a6's body `blocks++`: move writeFsTable's compares.

The last compare: `ivtmp.434_273 != _366` where the wanted order has `end` lowest. 273 is the split-paths copy of the iv, a recycled name (`i_273`, a single-argument PHI of an inlined FS loop, gone at fre3); the reference's copy is 237 and end is 130. Tuple to look for with `--probe`: `ivtmp.44x != _e`, `_e != ivtmp.43x` twice, `_e != ivtmp.43y`.

Per trick after this attempt:

| Trick | State |
|---|---|
| a1, c3, a2 | near3/near3a above: one compare. Any pair of them gets there |
| a5, a6, len, ab, c4 | not gained: `a1,a5,a6,len` 28 lines, annealed to 22 in 15 min, then stopped for the better family |
| opt | still 4; root found: sccp's final_value_replacement calls split_loop_exit_edge on single-exit loops with known niter whose exit block has several preds, leaving 4 forwarder blocks up to dce6. Without sccp those blocks don't exist. The gimple only differs in names |
| pin_t | t's slot 89 vs partial's 90, tie goes to lower regno (r235 = partial); needs a t-test split with a multiple of 10 AND t's regno lower, or partial's def in a colder block. Not solved |
| lnp2 | `partial <= 0` 12 lines; no second predictor available: no PRED_GOTO in C (gen_iw36) |
| exp_file | 80; dead conjunct to undominate the error block fails (gen_iw37) |
| exp_mob | 26; PRED_TREE_EARLY_RETURN only fires if the arm has a single successor and isn't the last block: a test inside the fits arm would give 50/50, but that's a new dead test, net 0 unless exp_file falls too. One-error-block source fails (gen_iw35) |
| xmalloc | bit-CCP keeps alignment through index forms (gen_iw34) |
| pin_hdr | not attacked further |

Scripts, all run from the repo root: `iw3.py singles|subsets a,b,..|show a,b [-o f]`; `IW3BASE=f iw3anneal.py <secs> <seed> <fixed|-> [--workers N] [--free a,b] [--pen N]`, `... 0 0 - --render '<json>' out.c`, `... 0 0 - --probe '<json>' [--workers N]`; `iw_ver.py <dumpdir> <asm name> <versions>` (who owned an SSA number per pass; note clones are addressed as imgAdd.constprop.2). Generators: gen_iw34 (raw forms), 35 (mobile), 36 (lnp2 goto), 37 (fits conjunct), 38 (`hi` local), 39 (`IWB=` base, gen_iw15's forms), 40 (`IWB=`, length argument forms), 41 (dead test bodies), 42, 43, 45 (near sets), 44 (memset forms). `iwsweep -k label` reruns the whole sweep, so render with `iw3.py show` where possible.

What I'd try next:
1. Continue from near3/near3a: only that compare. A shape that survives early opts and folds after inlining is the only kind that moves the free list (`pad == 1 && tail` moves it but costs CFG). Candidates: conditions on `type` and `next` in arms that die in writeFsTable's copies, with real extra operations (not copies, which die in early forwprop), and the order of the two calls in writeFsTable.
2. On a hit, retry a5/a6/len on top (each compare problem is the same kind).
3. Don't retry: writeFsTable's own forms on these files (gen_iw39, 40, 2016 forms), dead test conditions and bodies alone (gen_iw41, 3456), memset temporaries (gen_iw44), annealing with the current shape list (about 15000 states so far).
