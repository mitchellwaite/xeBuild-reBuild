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

## Attempt 7

Written as I go. New tools: `iw7wf.py <secs> <seed> <base.c,...> [--workers N] [--dead MAX] [--noopt P]` (random forms of writeFsTable's own code plus up to MAX dead tests inside writeFsTable; only writeFsTable can change; hits in build/iw/a7/wfhit_*.c, log wf_<seed>.log), gen_iw116 (FS-loop temporaries on r0), gen_iw117 (one dead test in writeFsTable on r0), gen_iw118 (lnp2 forms x memset forms on src).

- **Key lever: writeFsTable is decoupled.** A change in writeFsTable's own body can't touch imgAdd or its clones. So near6c's one remaining compare can be moved by something local to writeFsTable.
- **First reduction, `drafts/image_write_a7.c`, IDENTICAL to reference.o (plain -O3): near6c (f0) plus one dead test in writeFsTable just before the calls: `if ((off & 0x3fff) > 0x3fff) off += 0x4000;`.** All 4 old dead tests gone, 1 new: 9 -> 6 tricks. The body matters: `off++` gives 6 lines.
- Variants, all IDENTICAL (gen_iw122): the same condition with body `off = 0;` before `p = buf`, before the malloc, or before the fsTable store (build/iw/a7/b_p0.c, b_p1.c, b_p5.c). On r0, or with `small` or `blk` undone, no position or body in that grid matches (best 24). What the test does is put a PHI on `off`, alive until vrp1 (checked in the dumps: `> 16383` is gone after 096t.vrp1), ahead of both inlined copies. The test needs f0's imgAdd.
- Why the free list matters (dumps of r0, f0, src; build/iw/a7/names_after.py): ivopts' pops come from the list as it stood before the pass; nothing it releases is reused in that pass (no name is in both its new and gone sets). The processing order follows the ivtmp numbers: small inner loops, small outer, big inner, big outer, memcpy loop. reassoc2 and split-paths then pop what ivopts released last: 3 names to reassoc2, then 3 to split-paths, the last being the big copy's copy. In r0 that name is `_92 = _128 * 32`, in f0 it's `b_360`, the outer PHI: that's why f0 has that site right. In src cunroll goes up to 407 where r0 stops at 391.
- Remaining tricks from a7:
  - `opt`: 2 lines, one compare in the small copy (`_90 != ivtmp.409_148`, wants the iv first; end is a low name without the attribute). gen_iw123 (240 positions and bodies of the dead test) stays at 2. Searches: iw7wf seeds 702 (r0, f0, up to 1 dead test), 704 (a7 and b_p* with writeFsTable's forms), iw6anneal seed 721 from build/iw/a7/a7no.c: see the result below.
  - `pin_t`: 10, t and partial's byte slots. Measured: r234 partial total 180, r235 t 178 (LRA's `Assigning` freq lines). Needs t's total above partial's or a tie with t's regno lower. Only a split of t's test whose two parts are multiples of 10 ties, and the hot label's 85/15 isn't one. gen_iw119 (t's position, range form) no better.
  - lnp2: much worse on a7 than on src: `partial <= 0` is 12 lines on src but 213 on a7; gen_iw118, gen_iw124. Best: `if (partial) {...} else npages = 32;` with `&` partial (build/iw/a7/n1p1.c): imgAddFile 12 (slots 0x30/0x34: r139 off+len vs r181 npages; off+len has 7 refs, all of which are in the reference's code, so npages has to rise), writeInitialHeader 89 (its off-0x80 call gets inlined: big_speedup, 3569 -> 3206 is just over 10%; gen_iw125's temporaries fold before the estimate and don't change it), constprop.1 2, writeFsTable 8.
  - pin_hdr: gen_iw121 (forms of pageErased, calcPageEcc and the call, 96) stays at 241 or more in finalizeImage.
  - xmalloc: not attacked. Read from memory of gcc, unverified: bit-CCP's alignment comes from a builtin-malloc call.
- Don't retry: gen_iw117's single dead tests on r0; helpers for pin_hdr (gen_iw121); temporaries for inlining (gen_iw125, they die early).

### Attempt 7 result: MATCH, 9 -> 6

`drafts/image_write_a7.c`, plain -O3, .o byte-identical to reference.o, which is identical to build/obj/image_write.o. Differences from src: the 4 dead tests in imgAdd and imgAddFile gone; `pg = start * 32;` in the inner loop; `blk = start + b;` used by big-arm `b2lo`; `_Bool small`, set by an `if`, then `partial = small && len < 0x4000;`; `tail = rem; if (rem >= 0x4000) tail = rem % 0x4000;`; `fsTable[start - xb.fsStart + blocks - 1]`; one new dead test in writeFsTable. Left: dead 1 (writeFsTable), pins 2 (t, xb.hdr), hot label lnp2, optimize on writeFsTable, xmalloc = 6.

Searches that found nothing further:
- iw7wf seed 703: no dead test, r0 and f0, 1956 states, best 2.
- iw7wf seed 702: attribute gone, up to 1 dead test, 1924 states, best 2.
- iw7wf seed 704: attribute gone, a7 and b_p*, 2322 states, best 2.
- iw6anneal seed 721: from a7 with the attribute gone, 2832 states, stays at 2.
Seed 701 (900 s, up to 2 dead tests) found the two hits, build/iw/a7/wfhit_701_1.c and _2.c.

Scripts (repo root): `iw7wf.py` as above; `iw_tuples.py gen_iw116|117|122|123.py`; `iwsweep.py gen_iw118|119|120|121|124|125.py`. gen_iw122 is the grid around the dead test (`IWB=` other base), gen_iw123 the same with the attribute removed. gen_iw125 reads build/iw/a7/n1p1.c (gen_iw124 `n1+p1`). build/iw/a7/names_after.py <src|r0|f0> and regfreq.py are small dump readers, run from build/iw/a7.

Next:
1. The dead test: a form on f0 that puts a PHI on `off` ahead of the copies and survives to vrp1, without a test that's dead. 703's forms didn't find one. The grid shows any early `off` PHI with `off = 0` works, so the PHI is what counts.
2. `opt` on a7: one compare, `_90 != ivtmp.409_148` in the small copy. The attribute changes which names top the list at ivopts. A second dead test would fix it only at net 0, so it wants a natural form: not found in 702, 704, 721.
3. lnp2: three separate problems (see above), so only after the rest.

Lesson: **look for the function that's decoupled.** writeFsTable isn't inlined anywhere and nothing depends on its names, so a local change there settles a compare that 20000 states of imgAdd forms couldn't without disturbing the clones. A dead test local to one such function can replace several shared ones.

## Attempt 8

Written as I go. New tools: `iw8wf.py <secs> <seed> <base.c> [--mode dead|opt|both|any] [--workers N]` (structural forms of writeFsTable: helpers, loop shapes; log build/iw/a8/wf8_<seed>.log), gen_iw126 (raw pointer forms for xmalloc), 127 (head forms without the dead test), 128-133 (lnp2 and pin_t family, see below).

- **xmalloc:** `-fdump-tree-optimized-alias`: `mem_40 = malloc` has `# ALIGN = 4` and the PHI, `raw + 528` follow; index forms (`mem + (b*32+p)*528`, gen_iw126 `idx*`, `off*`, `blk*`, struct and array cursors) still end in `raw_103 = (uint8_t *) ivtmp` with ALIGN 4. The only unaligned origin in the file is a load (the MU loop's `raw = xb.raw + ...` has the prologue). -fdump-passes shows a ccp4 after vrp2, so nothing after ivopts can lose it either. The reference has no reload of xb.raw (`mov [esp+0x28],eax` is malloc's result, read back from the slot), so a load can't be the source. `-fno-builtin-malloc` plus a prototype with `__attribute__((malloc))` gets finalizeImage to 2 lines but costs writeFsTable 193: that one's buf needs the alignment, so it's per call, not per file. No natural form found; don't retry forms of raw.
- **lnp2/pin_t family (gen_iw128-138):** without the hot label, `if (partial) {npages..} else npages = 32;` (50/50 split, t and partial tie, `unsigned t` + `if ((uint8_t)t < 15)` takes the slot: pin_t gone, imgAdd right) but writeInitialHeader inlines `imgAdd(0, &hdrTemplate, sizeof, 0, 0x1ffb, 1)`: saving 10.17% (`-fdump-ipa-inline-details`), from the `(op2 changed)` statements: `pages` in the inner loop. **Moving pages into the arms where it's used stops the inline** (gen_iw132 `arm`, gen_iw136, gen_iw138). imgAddFile's slots 0x30/0x34 want npages' guard block hotter than 450 (`partial > 0`, 73%: 657, fine). build/iw/a8/n7.c = gen_iw138 `Bin+Stop+n3+tp`: no hot label, pin kept: only constprop.1 one compare and writeFsTable 28.
- From n7: pages' spelling matters in the big arm: `pages = len / 512; if (len % 512) pages++;` (gen_iw141 `Bi+St`, build/iw/a8/n8.c) takes writeFsTable from 28 to 8. Left in n8: constprop.1 one compare (`ivtmp.110_82 != ivtmp.107_97`, wants the split-paths copy below 82; the copy reuses ivcanon's released `ivtmp_97`, the reference's is 55) and writeFsTable's big copy compares. `char t` with `(uint8_t)t` (n9.c) flips constprop.1 right but then constprop.4's `blocks + ivtmp` (blocks_35 from dom2, below ivtmp.144_43). Sweeps that didn't move these: gen_iw139 (480: blk uses, tail, end, partial order), 140, 142 (t types x pages place), 143 (blocks and tail forms), 144 (type temporaries). iw8an.py (annealing with writeFsTable out of the score, hits an8_<seed>_<n>.c): seeds 821 (n8), 822 (n9).
- Per trick, measured on src (plain -O3): `optimize` 2 lines (`cmp edx,ecx`, small copy), dead test 2 (`cmp esi,edx`, big copy, second site), both 4; pin_t 10; xmalloc 180.
- writeFsTable alone: iw8wf seed 803 (500 s, 3488 states over helpers that inline, loop shapes, named locals, statement order; modes dead, opt, both): best dead 2, opt 2, both 4, no hit. Seeds 801, 802 were cut short, same bests. gen_iw127's head forms that keep a PHI on off with no dead test (a `pad` flag tested twice, `blk = (off = ...) >> 14`, a helper-free `a` local): `none`, f12, f14 stay at 2, the flag forms are 69-171. So static helpers don't rescue either trick. Writing the dead test as a flag isn't enough: what it does isn't only the PHI.

### Attempt 8 result: NO MATCH

Nothing identical with fewer tricks; src/image_write.c stays best at 6. reference.o is still identical to build/obj/image_write.o and src compiles to it.

The new thing is the **hot label's mechanism is now solved structurally**; before this attempt lnp2 had three separate problems. Closest, all plain -O3 with no hot label:

- `drafts/image_write_near8.c` (build/iw/a8/n8.c, would be 5): **constprop.1 one compare (2 lines) + writeFsTable 8 lines (two compare sites in the big copy, 4 flips).** imgAdd, constprop.2, constprop.4, imgAddFile, writeInitialHeader and everything else byte-equal. Keeps pin_t, pin_hdr, dead test, optimize, xmalloc. Differences from src: `partial = (len < 0x4000) & (type != 0) & (type != '0');`, `if (partial > 0) {npages from len} else npages = 32;`, no `small`, pages computed where used (big arm: just before `left`, spelled `pages = len / 512; if (len % 512) pages++;`; small arm: top of the else).
- `drafts/image_write_near8b.c` (n9, would be 5): `char t` + `(uint8_t)t`, pages at the top of the `type > 1` block in the big arm and top of the else: constprop.4 one `lea` (2 lines, `_200 = blocks_35 + ivtmp.144_43`: blocks wants the higher name) + writeFsTable 68.
- `drafts/image_write_near8c.c` (n6, would be 4: **pin_t gone as well**): `unsigned t` + `(uint8_t)t`, `if (partial) ...` (50/50, tie, regno favours t). imgAdd and all clones right. imgAddFile 128 = one compare that flips the loop layout + the 0x30/0x34 slots (12), writeFsTable 30. A dead `if ((len & 0x3fff) > 0x3fff) len++;` in imgAddFile (gen_iw145, gen_iw146) fixes the compare, leaving the 12 slot lines, and that would be net -1 if the slots were solved.

Mechanisms confirmed by dumps:

1. **writeInitialHeader's inline.** Without the label the call that inlines is `imgAdd(0, &hdrTemplate, sizeof, 0, 0x1ffb, 1)` at frequency 0.5, not the 0x80 call attempt 7 assumed: `-fdump-ipa-inline-details` shows predicates on `op2` (len), `time w/o inlining 3569.5, time w inlining 3206.5` = 10.17%. `(op2 changed)` is 495 of it: `pages` computed in the inner loop. Moving pages into the arms removes the inline. Each arm's position matters separately, see gen_iw136 and gen_iw138's table: Bin+Stop and Btop+St1 are the useful ones.
2. **imgAddFile's slots 0x30/0x34.** Reference: r191 npages in slot 6, r136 off+len in slot 7. npages' refs are 2 at freq 81 and the guard at 900 x P(partial): 450 at 50% loses, 630 (hot label) and 657 (`partial > 0`, 73%) win. So P(partial) above about .55 is all it takes. `partial == 1`, `partial != 1` fold to the same test as `partial`, no prediction (gen_iw134). `uint8_t partial` loses the prediction too (gen_iw135).
3. **pin_t.** t's total is 2 x (floor(a/10) + floor(b/10)) where a + b = 900 and a, b are the arms of partial's test; partial's is 180. 85% and 73% both give 178. 50% gives 180, a tie, and then `unsigned t` with `if ((uint8_t)t < 15)` wins it (gen_iw128): no asm. On src's hot label that form costs 16 + 53 (gen_iw129). So pin_t and the 73% that imgAddFile wants conflict: the only predicted splits giving a tie are multiples of 10 (60, 70, 80, 90) and neither available predictor lands on one exactly.
4. **constprop.1's compare in near8:** `ivtmp.110_82 != ivtmp.107_97`, where the reference has `ivtmp.106_55 != ivtmp.109_82`. The copy from split-paths reuses the name ivopts released from ivcanon's `ivtmp_97` (the reference's is `ivtmp_55`), and ivcanon popped it from what sccp released of unswitch's new names: near8 40, 95, 96, 97, 99..., reference 53, 54, 55, 58.... The names diverge from `forwprop2` on and show at `pre` (`iw8ver.py <dir> imgAdd.constprop.1 90 -n`).
5. **`partial > 0` is what flips constprop.4's lea:** with `if (partial)` (n6) both clones are right, with any 73% spelling one of them is off: u8 t flips constprop.1, char or unsigned t flips constprop.4 (gen_iw149).
6. **xmalloc:** see above: no natural form. Ruled out: raw's forms, index forms, struct and array cursors (gen_iw126), and a whole-file non-builtin (writeFsTable needs the builtin).

Tried without moving constprop.1 or constprop.4: gen_iw139 (480: blk uses, tail, end, partial order), 140, 142, 143 (blocks and tail, on n8 and n9), 144 (224 on each: named type temporaries), 147 (dead tests in imgAdd, partial grid, its `h` position also hits imgWriteHdr and doesn't compile), 148 (126: `small` set by an if, `&` on len), 149 (100: spellings of the 73% test x t), 150 (63: t's position; `e`, t before the outer loop, fixes constprop.4 but costs imgAdd 357), gen_iw131 on n8 and n9 (FS loop, pg, pages forms). Annealing with writeFsTable out of the score: iw8an seeds 821 (n8, 1720 states), 822 (n9, 1384), 823 (n9, 3288): stays at 2. iw6anneal 811, 812, 813 on n4p, n5, n7: 26, 26, unchanged.

Scripts (repo root; generators with `python tools/wip/dehint/iwsweep.py tools/wip/dehint/gen_iwN.py -n TOP [-k label]`, `IWB=` base): gen_iw126 (raw forms; base build/iw/a8/nox.c = src with `malloc` in finalizeImage), 127 (head forms), 128 (t type on n1p1t), 129 (t type on src), 130 (npages x partial x t), 131 (FS, pg, pages forms), 132, 136, 138 (pages position), 133, 135 (arm spellings), 134 (73% spellings), 137 (imgAddFile's own forms), 139-144, 147-150 as above, 145, 146 (imgAddFile dead test and arm order). `iw8wf.py`, `iw8an.py` (extra shapes in iw8shapes.py), `iw8ver.py <dir> <asm name> <first pass> [-n] <versions>` (owners of an SSA version in a clone, or new and gone names per pass; dumps from `IWNP=1 iwdump.py <file> <dir> writeFsTable -fdump-tree-all`). Bases in build/iw/a8: n1p1t = build/iw/a7/n1p1.c minus the pin, n2 = that with `unsigned t`, n3 = gen_iw132 `arm`, n4 = gen_iw133 `b1+p1+tb`, n4p = n4 with the pin, n5 = gen_iw134 `n3+p1`, n6 = gen_iw136 `Btop+St1`, n7 = gen_iw138 `Bin+Stop+n3+tp`, n8 = gen_iw141 `Bi+St`, n9 = gen_iw142 `ch+Bt1t+Stopt`.

What I'd try next:

1. near8's one compare, then writeFsTable with iw8wf and gen_iw122's dead-test grid (`IWB=`): writeFsTable is decoupled, so once the clones are right it's likely a local fix. Don't sweep imgAdd's spellings again: use `iw8ver.py -n` and find the earliest pass where near8 and src diverge in constprop.1 (forwprop2's list has `30 34 35 36 37` in src, not in near8) and ask what statement owns them. Those names come from src's `small`/`if` form, which is the one thing near8 dropped; `small` written so that it doesn't add a branch before the predictors (gen_iw148's forms) didn't do it.
2. near8c (would be 4): needs P(partial) above about .55 without a test that isn't `!= 0` on partial, or fewer references on r136 in imgAddFile. Something other than a predictor on partial's test that raises the guard block relative to imgAddFile's head: its fits arm is 50/50 because PRED_CALL fires on both arms (strcpy, log_printf).
3. Don't retry: forms of raw for xmalloc; static helpers in writeFsTable (iw8wf); head forms for the dead test (gen_iw127); partial as `&&` without the hot label (imgAdd 102+); pages in the inner loop without the label (the inline, always).

Lesson: **read the inliner's dump before assuming which call inlines.** Attempt 7 thought it was the 0x80 call and tried temporaries; the real saving was a hot statement depending on one known parameter, and moving that statement to where it's used is natural and fixes it.
