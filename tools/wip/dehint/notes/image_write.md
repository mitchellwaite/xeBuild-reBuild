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

## Attempt 4

Written as I go. New tools: `iw_tuples.py <gen>` (each variant's lines and writeFsTable's iv compares grouped by operand pattern; wanted: `i<e e<i e<i e<i i<e i<e i<e i<e`).

- **First reduction, `drafts/image_write_a4.c`, IDENTICAL to reference.o (same flags):** near3 minus the a6 test, abort test on `end`. gen_iw55 (all subsets of the remaining dead tests on near3) showed removing a6 (and c4) gets all of writeFsTable's compares right at once; gen_iw59 then fixed imgAddFile (`if ((end & 0x3fff) > 0x3fff) abort();`).
- Per trick from a4 (gen_iw60, lines): `end < off` conjunct removed 4 (one compare `_60 < end`; `end` must stay alive until dom2 so `off + len` becomes `end_10`), whole len++ test removed 12 (no dead test between head and the fits test: VRP1 threads head -> fits -> abort test, the head block is copied with high names, 3 compares flip; gen_iw61: the abort test can only go first in the arm), c4 10 (imgAdd `_1 != ivtmp` compare + imgAddFile), opt 4, pin_t 10, lnp2le 12.
- pin_hdr mechanism: r201 (hdr PHI) pri = cost/(excess points + 1): 232/(147ish) = 1; the asm raises it to 368 (pri 2) and class AREG, so it's pushed after r196, r260, r261, which lets r327/r331/r332 (memcpy block) pop before r187/r192 (ECC v and data). A hdr load before spare's (`const uint8_t *h = xb.hdr;` first, gen_iw46/47 `h1`) swaps the tie: hdr gets eax, spare ebp, 104 lines left (best so far; only load order and esi/edi for data/v in the ECC loop). Type-mismatch reload (`const void *h`, gen_iw48/49): names of different pointer types aren't coalesced so the PHI gets a real copy, but the copy *replaces* a load and a plus in that pseudo: cost falls to 192, not up. No extra ref on hdr without code found. Pressure can't drop: r165 is uncprop's zero (`_36`) live through, and in the original too.
- Attempt 3's leads on near3's compare: order of writeFsTable's calls x type-arm forms x opt (gen_iw50, 450): nothing. Mechanism: ivopts pops incr then end from one run of names, 325..339 in near3: the FS loop's else arm in the inlined big copy, released in sequence when `next` kills it. A form with a short arm (gen_iw52 `v5`, gen_iw53 `ci`) does give the wanted tuple but changes generic imgAdd, because SWAP16's first half only narrows to short arithmetic when the macro argument is the full expression (gen_iw51, 53, 54). What actually moved it was removing a6: gen_iw55.
- opt: on a4 the small copy's compares flip (`ivtmp.410_55 != _78`, `_78 != ivtmp.410_159`). The 4 forwarders sccp leaves are the exits of the page loop and FS loop, whose exit blocks have several preds because of the zero-trip guard. Annealing on a4 with opt gone (seed 71, 1264 states): stays at 4.
- pin_t: t 89 vs partial 90, same as before: annealing with pin_t gone (seed 72, 1244 states) stays at 10. A tie needs a test split that is a multiple of 10 and t's regno below partial's, and `t` is a temporary (`_280`), not a named variable. An extra use must reach IRA and emit no code, same as hdr.
- `end < off` conjunct (a4p, build/iw/a4/a4p.c): annealed 1392 states (seed 73), stays at 4. Forms with one condition and another body (gen_iw62, 162: end++, lim--, off++) give the same 4 lines or 138+. A body that keeps len unchanged doesn't help: the threading needs the PHI on len or off.
- a5/a2: spelling the loop's block number from off, `#define BLK ((off >> 14) + b)`, is a natural ipa-cp time benefit: with a2 AND a5 gone the off-0 clone stays and its body is 2 lines off (gen_iw67 `xA5+xA2+b1`). But it costs a second value next to `(off - x) >> 14`: 748 lines. The original has only the latter, and `off >> 14` for start costs 221 (`s0`). Anything spelled the same as start is merged by FRE1 before ipa-cp (`b2` identical, no benefit), and `off - (off & 0x3fff)` folds to `off & ~0x3fff`. `x` recomputed in the loop gives no benefit either (FRE1).
- imgAddFile entirely natural on a4's imgAdd (no expect, no dead tests, gen_iw64 `noxp+A0+L0`, gen_iw65): 136 lines, 114 in imgAddFile: head registers (`lea eax,[ebp+0x3ffff]` for the limit), PRED_CALL does cancel on both arms. `imgFits(off, len)`: 184, same size. Not annealed from there: try that next, it would remove 4 (expect, ab, len, end < off).

### Attempt 4 result: MATCH, 16 -> 14

`drafts/image_write_a4.c`, flags unchanged (`-O3 --param builtin-expect-probability=50`), .o byte-identical to reference.o. Removed conditions: a1 (`x > first + 0x4000` before memcpy), c3 (`x + 0x4000 < first` in the merged test), a6; imgAdd's empty asm is gone too (a2's body is now `blocks += 2`, not a count change). Added: conjunct `end < off`, so dead conditions go 8 -> 6, not 5. Left: param 1, dead 6 (a2, c4, a5, end<off, len&, ab), pins 2, expect 2, hot label 1, opt 1, xmalloc 1 = 14.

Scripts (repo root): `iw_tuples.py <gen>`, `iw4probe.py <base.c> [fn..]` (single iwanneal shapes, per-function lines); generators gen_iw46-49 (hdr: local load order, pointer types), 50-54 (near3 compare: calls, type arms, FS arm), 55 (subsets on near3, `IWB=` base), 56-59 (imgAddFile on a6/c4a6; 59 is the hit `eF0+A1`), 60 (subsets on a4), 61, 62 (abort position, one-condition dead test), 63 (a2 forms), 64, 65 (natural imgAddFile), 66, 67 (off in loops). Some use build/iw/a4/{a6,c4a6,lp1}.c: a6 is near3 minus its `x + 0x4000 < first` test, c4a6 is that minus `(len & 0x3fff) > 0x3fff` in the loop too (recreate them with gen_iw55 -k). Annealing logs build/iw/a3/an3_7x.log.

Next:
1. Natural imgAddFile (above) with iw3anneal from gen_iw65's `lim` form: head registers, then one compare at a time.
2. c4 (10 lines from a4): imgAdd's `_1 != ivtmp` compare; only a second x test in the loop fixes it so far (gen_iw57 `lpgbp`, no net gain; gen_iw63 a2 forms don't).
3. `off`-derived in-loop values for a2/a5: something that isn't merged by FRE1 but merges with start after ipa-cp.
4. pin_hdr's 104-line form (`h1cu8`): needs hdr pushed after r196/r260/r261; pin_t and hdr both want a use that reaches IRA and emits no code; none known.
Don't retry: near3 forms (done, a6 removal solved it), pointer-type reload for hdr, end++/lim-- bodies (gen_iw62), abort elsewhere in the arm (gen_iw61).

## Attempt 5

Written as I go. New tools: `iw5.py singles|subsets|show` (the 14 tricks of 8b2855b3 as named edits, `IW5BASE=` other base), `iw5d.py <file> [-np] [fn..]` (diff with jump and call targets blanked: real instruction differences only; a layout flip reads as moved blocks).

- **Breakthrough: imgFits written with an `if`** (`if (a >= b) return 1; return 0;`). Its own code is unchanged, but the PHI of constants survives early inlining (no early phiopt in gcc 6), so its callers get the original's probabilities and threading. imgAddMobile needs no expect and no param once its big arm is `if (imgFits(off, len)) { adding...; return ret; } error; return 0;` (error string after: `if (!imgFits)` first flips .rdata). drafts/image_write_a5.c: exp_mob gone, identical (13). gen_iw69 (imgFits forms), 70, 71 (mobile forms).
- **imgAddFile natural:** `if (imgFits(off, len)) {...} else {error}` with the if-form imgFits has the head right; one compare left in the big copy (`npages > p`, flips loop layout, 116 lines; build/iw/a5/m1.c). One dead `if ((len & 0x3fff) > 0x3fff) len++;` before it flips the compare: IDENTICAL with no flags (gen_iw78 `L`, drafts/image_write_a5.c). So exp_mob, exp_file, param, ab and `end < off` are gone: 14 -> 9.
- Why the compare moves: `_Bool partial; partial = 0; if (...) partial = 1;` on m1 also gets imgAddFile and writeFsTable right with no dead test in imgAddFile, leaving 8 lines in imgAdd (build/iw/a5/m3.c, gen_iw73 `_Bool+pa`). The 8 are t's `lea`: PRE inserts the loop's invariants on the preheader by value id, and value ids follow SSA versions (run_scc_vn walks versions), so `len <= 16383`, popped at ifcombine, must get a version below t's. With `int partial` the copy `partial_68 = iftmp` is released after release_ssa and ifcombine pops 68, below t_69; in the _Bool form it pops 75, above t_68.
- Family without any dead test in imgAddFile: `_Bool partial; int small; small = type != 0 && type != '0'; if (small && len < 0x4000) partial = 1; else partial = 0;` + `i = blk - xb.fsStart; fsTable[i] = ...` in writeFsTable: build/iw/a5/c12.c, only 2 compares of writeFsTable's big copy (6 lines). Gets there via gen_iw80 (`_Boolint+c10`), probe (`wst0`), gen_iw81 (`f2+i`). gen_iw39 (writeFsTable forms) on c11: stays at 8.
- Mechanism of the last compare in c13 (`ivtmp.433_71 != _176` where the reference has `_174 != ivtmp.434_405`): the copy in split-paths pops a free name. In the reference the top of the free list is 405 (a temporary made and released after ivopts, in no dump), in c13 it's 71, `b_71`, the outer loop's iv that ivopts released. So the free list wants one more late-released high name. `build/iw/a5/ns2.py <dumpdir>` lists split-paths' new names, `ns3.py <dumpdir> <ver>` a version by pass.
- Singles on the a5 draft: `opt`: still the 2 small-copy compares, 4 lines. pin_t 10. lnp2le 12 (npages/off+len slots 0x30/0x34 swap). lnp2 183, xmalloc 180, pin_hdr 243, a2 and a5 alone lose the off-0 clone (10000+), c4 alone 140 and lenp alone 138 (each the imgAddFile compare; in the c1x family they cost far less, see below). Shape probes (one trick x one shape) on a5 find nothing for opt, pin_t, lnp2le.

### Attempt 5 result: MATCH, 14 -> 9

`drafts/image_write_a5.c`, compiled with plain `-O3` (no --param), .o byte-identical to build/obj/image_write.o. build.sh's image_write case must become `cflags="-O3"` and lose its comment about imgAddMobile's hint.

Removed: both `__builtin_expect`, the --param, `(end & 0x3fff) > 0x3fff` abort test, `end < off` conjunct. Left: dead 4 (imgAdd loop `x > first + 0x4000` and `(len & 0x3fff) > 0x3fff`, FS loop `x > first + 0x4000`, imgAddFile `(len & 0x3fff) > 0x3fff`), pins 2 (t, xb.hdr), hot label lnp2, optimize on writeFsTable, xmalloc = 9. Source changes: imgFits has an if; imgAddMobile's big arm is `if (imgFits) {...; return ret;} error; return 0;`; imgAddFile uses imgFits, no lim, no end, unused locals dropped.

Closest to 8: `drafts/image_write_near5.c` (build/iw/a5/c13.c, no dead test in imgAddFile): `_Bool small; int partial; small = 0; if (type != 0 && type != '0') small = 1; partial = small && len < 0x4000;` and `i = blk - xb.fsStart; fsTable[i] = ...`: **one flipped compare**, writeFsTable's big copy, 2 lines. Not reached in: gen_iw83 (1215: dead bodies, small's test, t, lengths), gen_iw84 (432: small and partial forms), gen_iw85 (512: dead conditions), gen_iw39 (1440: writeFsTable forms), annealing seed 504 (1100 states).

Others: build/iw/a5/m3.c (`_Bool` partial, imgAdd's t 8 lines). `iw5cross.py` on m3, c10-c13, a5: c1x with len++ kept and c4 gone is 6 lines (constprop.1 2, writeFsTable 4): would also be 8.

Scripts (repo root unless stated): `IW5NP=1 IW5BASE=<file> python tools/wip/dehint/iw5.py singles|subsets a,b|show a,b [-o f]`; `python tools/wip/dehint/iw5d.py <file> -np [fn]` (the diff to read first); `python tools/wip/dehint/iw5cross.py <files>` (from anywhere, paths as given; c4, opt, pin_t subsets with and without len++); `IW3BASE=<file> python tools/wip/dehint/iw3anneal.py 0 0 param --probe '{"param":true}'` still works with param as the fixed name (no --param then). Generators (iwsweep.py, `PYTHONPATH=tools/wip/dehint` for 69, 71, 72): 68 natural imgAddFile, 69 imgFits forms, 70 mobile forms, 71 exp_mob only (`if1+Bif+S0`), 72 imgAddFile-only forms (480, no effect on the compare), 73 partial type and form, 74, 75 t position, 76 straight-line partial, 77 t and partial forms, 78 the dead test in imgAddFile (`L` is the hit), 79 broad cross, 80 extra copy (`_Boolint+c10`), 81 (`f2+i`), 82 (`s5+p7+pi+sb`, c13), 83-85 around c13. Generators read base files in build/iw/a5/: m1 = gen_iw70 `Bif+S0` on if1 (gen_iw69 `if1+fits+mob`), m3 = gen_iw73 `_Bool+pa`, c10 = gen_iw80, c11 = wst0 on c10, c12 = gen_iw81 `f2+i`, c13 = gen_iw82.

Lessons:
1. **Look at helpers' shape first.** `return a >= b` vs `if (a >= b) return 1; return 0;` compile to the same function but differ a lot when inlined early: this one change replaced 2 expects, the param, 2 dead conditions. Worth trying wherever a small helper is inlined and hints sit around its callers (other objects too).
2. Literal order: `if (imgFits) {adding} error` puts error's string after, which is what .rdata wanted.
3. PRE's preheader insertions follow SSA version order (run_scc_vn walks versions), so an ifcombine-popped name above a later statement's version reorders hoisted code, hence RA.
4. A copy from a COND_EXPR temp (`int partial = a && b`) survives until release_ssa and is freed later: it decides which low name ifcombine pops.

Next:
1. near5's compare: a form that leaves one more name released after ivopts in writeFsTable's big copy.
2. Same `if`-shape thinking for what the rest hide: pageErased/spareUsed/calcPageEcc forms for pin_hdr (finalizeImage inlines them), imgSizeAligned for imgAdd's callers.
3. a2/a5 (off-0 clone): still needs a natural time benefit for off in the loops; look for a real expression, a test of the kind that folds when off is 0.
4. lnp2: needs p >= .78 for `partial <= 0` or a change in r136's references.
Don't retry: imgAddFile-only forms for the compare (gen_iw72), dead conditions on c13 (gen_iw85), t position on `_Bool` (gen_iw74, 75).

## Attempt 6

Written as I go. New tools: `iw6cp.py <file.c>` (ipa-cp's evaluations: is the off-0 clone made, by what margin). Base is plain -O3; sweeps set `FLAGS = []`.

- **Breakthrough: `pg = start * 32;` as a local in the inner loop** (`s = xb.spare + (pg + p + b * 32) * 16;`) replaces a2/a5's job. ipa-cp's time benefit counts statements whose operands all derive from params, so an `off`-only value computed in the loop is what the off-0 clone needed (evaluation 557 with the dead tests; 757 with `start * 32` and no dead tests; threshold 500). Forms that fold back to `(start + b) * 32` at parse time (`(start * 32 + b * 32 + p)`) have no effect: it has to be a separate statement. Ruled out for this job: `start` computed per loop (gen_iw86: benefit is there but `sub/shr` in place of the head's `shr`, 1300 lines).
- With it all four dead tests can go: gen_iw88 `noc4+nolp+pd` 91 lines, then `start - xb.fsStart + blocks - 1` in the 0x1fff store (constprop.1's 51), then `partial = (len < 0x4000) & (type != 0) & (type != '0');` (gen_iw91 `f11`): **2 lines: one compare, writeFsTable's big copy** (`drafts/image_write_near6.c`, build/iw/a6/r0.c; same compare as earlier attempts: `ivtmp.433_92 != _317`, wants the split-paths copy's name above end's).
- The last compare's mechanism (r0 vs reference, `iw6last.py`, `iw6ver.py`): ivopts' pops for the big copy's `end` come from the FS loop's dead else arm of an inlined copy. Reference: first copy's arm, low names (174); r0: second copy's arm (317), because r0 has about 10 free names more on top of the list (the reference's cunroll runs out and allocates up to 407, r0 stays at 391). The split-paths copy then takes the top of the list, the last name ivopts released (reference 405, r0 92 = reassoc1's `_128 * 32`). So r0 wants about 10 more names popped between ccp2 and ivopts and live until ivopts, or a higher name for reassoc1's statement. Sweeps that don't reach it: gen_iw92 (1440 writeFsTable forms), gen_iw93 (dead tests back), gen_iw94 (pg forms), annealing seed 603 (2872 states from r0).
- gen_iw104 `bv` (`for (blk = start, b = 0; b < blocks; b++, blk++)`, all LBA stores on blk): writeFsTable matches, but b's iv goes in constprop.4 (167). gen_iw105: `blk = start + b;` local at the top of the outer loop used only by `s[1]`, `s[0]` (`u2+u4+lo`, build/iw/a6/c0.c) gets the big-copy third compare right too, 61 lines with the 4th compare wrong. A named block number does move the free list: lever to continue.
- Family with a `small` temporary: gen_iw113 `e+u1+lo` (`drafts/image_write_near6c.c`, build/iw/a6/f0.c): `blk = start + b;` at the top of the outer loop used by big-arm `b2lo = blk >> 8`; `small = 0; if (type != 0 && type != '0') small = 1; partial = small && len < 0x4000;`. 2 lines: the big copy's other compare (`ivtmp.433_314 != _316`, its first pair member). r0 and f0 are complementary: in the big copy's two compares, r0 has (389 good, 92 bad), f0 (314 bad, 360 good). A state with ivopts' incr high (r0's 389, a cunroll temp) and split-paths' copy high (f0's 360) would be identical in writeFsTable.
- Other near states: `drafts/image_write_near6b.c` (build/iw/a6/c2.c: `s[1] = blk; s[0] = blk;`, `&` partial, original fsend): 10 lines, only compare operand orders in constprop.2 and writeFsTable. `partial = (type != 0) & (type != '0') && len < 0x4000;` on it (build/iw/a6/c1.c with `lo`, d0 with `lm`): writeFsTable fully right, but imgAdd 16 (t's lea, two byte slots) and constprop.2 6. The imgAdd lines track the ifcombine-popped name: `&` and `small` forms fix imgAdd and move writeFsTable's compare; that's the same coupling attempt 5 saw.
- imgAdd's t pin on r0: 10 lines, same slot swap. Range forms of the test (gen_iw103: `type >= '1' && type < '@'` etc.) 16. Unchanged.
- lnp2 on r0: `if (partial) {...} else npages = 32;` (gen_iw96 n1, n2, n3, n6, n9) gets imgAddFile to 12 lines (the 0x30/0x34 slots) with no label, plus writeInitialHeader 89, which wasn't looked at. Best trick to try after the compare.
- opt on r0: its own cost is now one compare (the small copy's `cmp edx,ecx`).

### Attempt 6 result: NO MATCH

Nothing identical with fewer tricks; src/image_write.c stays best at 9. But the closest states have **all four dead tests gone (would be 5 tricks)** with one flipped compare left:

- `drafts/image_write_near6.c` (r0): 2 lines, writeFsTable big copy, `cmp esi,edx` at its second site (line 360 of the function's disassembly). Changes from src: dead tests removed; `pg = start * 32; s = xb.spare + (pg + p + b * 32) * 16;` in the inner loop; `partial = (len < 0x4000) & (type != 0) & (type != '0');`; `tail = rem; if (rem >= 0x4000) tail = rem % 0x4000;`; `fsTable[start - xb.fsStart + blocks - 1]` in the 0x1fff store.
- `drafts/image_write_near6c.c` (f0): 2 lines, the same compare's first site (line 316). As r0, plus `blk = start + b;` used by big-arm `b2lo = blk >> 8`, and `small = 0; if (type != 0 && type != '0') small = 1; partial = small && len < 0x4000;`.
- `drafts/image_write_near6b.c` (c2): 10 lines, operand orders only.

What each near draft still keeps: pins on t and xb.hdr, hot label lnp2, optimize on writeFsTable, xmalloc.

Per trick now:

| Trick | State |
|---|---|
| 4 dead tests | near6/near6c above: one compare. Their ipa-cp job is solved by `pg = start * 32` (evaluation 757, threshold 500; a second such statement risks passing 500 for the off-0x80 value too, which needs time >= about 265: extra clone, seen with gen_iw98 `ip`) |
| opt | on r0 costs one compare of its own (small copy) |
| pin_t | 10, slots only, range forms of the test worse (gen_iw103) |
| lnp2 | `if (partial) {...} else npages = 32;` (gen_iw96 n1): imgAddFile 12, writeInitialHeader 89 not examined |
| xmalloc | reference keeps malloc's result in a stack slot, no reload of xb.raw, so no natural load breaks the alignment; not attacked further |
| pin_hdr | not attacked |

Scripts (repo root): `iw6cp.py <file.c>` (ipa-cp evaluations; full dump to build/iw/a6_cp.txt); `iw6ver.py <dumpdir> <fn> <first pass number> <versions> [-m]`, `iw6last.py <dumpdir> <fn> <pass number> <versions>` (who owns a name by pass, who released what a pass pops; dumpdir from `IWNP=1 iwdump.py <file> <dir> writeFsTable -fdump-tree-all`); `iw6anneal.py <secs> <seed> <base.c> [--workers N] [--state json] [--render json out.c]` (extended shapes, plain -O3; log build/iw/a6/an6_<seed>.log, stops on IDENTICAL writing an6_<seed>.c). `iw_tuples.py <gen>` is the view to use on generators: it shows the eight iv compares (wanted `i<e e<i e<i e<i i<e i<e i<e i<e`). Generators: gen_iw86 (start per loop), 87, 88 (pg, dead subsets), 89, 91 (partial, type, fsend, tail), 90, 93 (dead tests back; `IWB=`), 92 (gen_iw15's writeFsTable forms, `IWB=`), 94 (pg forms), 95, 97 (all forms x dead subsets from src), 96 (npages shapes for lnp2), 98, 100, 101 (`off & 0x1ffff` local instead of pg; s1 family, worse), 99 (pg outside inner loop: clone lost), 102 (off + len local: `end` at the head gets the compare right but ifcombine merges the head's tests, 356), 103 (t range), 104, 105, 108, 110 (blk local), 106, 107, 111 (around c2), 109, 112, 113, 114, 115 (small temporary, f0). Bases in build/iw/a6: r0 = near6, r1 = r0 without pg, r2 = r0 with `blk` declared, c0, c1, c2 = near6b, d0, e0, f0 = near6c; c0 = gen_iw105 `u2+u4+lo`, c1 = gen_iw101 `fo+p0` on c0 (`IWB=`), c2 = same `fo`, d0 = gen_iw108 `u2+u4+lm+fo+f0`, e0 = gen_iw110 `u1+lm+t32+f0+fo`, f0 = gen_iw113 `e+u1+lo`.

Searches that stayed at their start: iw3anneal seed 603 (r0, 2872 states), iw6anneal 611 (r0, 2200), 612 (c2, 1204), 613, 614 (e0, c1), 615 (f0, 2040).

Next:
1. Get r0's incr and f0's copy in one state. The levers that moved these compares: a named block-number local (position barely matters, which stores use it does), `partial`'s form, `small`. Try other natural temporaries of the same kind (a named `BLK >> 8`, a named `next` test, a name for `start - xb.fsStart` in the FS loop), viewed with iw_tuples, not lines.
2. Once it's identical, count again: if a dead test has to come back for it, it's still a reduction, so land the first identical state. Then opt (one compare), then lnp2 n1.
3. Don't retry: gen_iw92's writeFsTable forms on r0, dead tests back on r0 or c2 (gen_iw93), pg's spelling (gen_iw94: only whether it survives as a separate statement counts), `&`/`&&` orders of partial (gen_iw111), FS else-arm forms (gen_iw53 on r0: lose imgAdd).

Lesson: an ipa-cp benefit doesn't need a dead test. An ordinary local computed from params alone inside a loop counts as time saved, then reassoc folds it back into the same code. Worth checking wherever another object uses dead tests for a clone.
