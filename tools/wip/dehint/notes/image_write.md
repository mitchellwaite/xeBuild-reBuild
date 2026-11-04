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

## Attempt 9

Written as I go. New tools: `iw9exp.py <base.c>` (expect + param grid on the ECC test, pin removed; mechanism test only), `iw9ira.py <file.c> [flags]` (finalizeImage's l5 spill pushes and pops, hdr/spare pseudos, block freqs; full dump build/iw/a9/ira/fi.ira).

### pin_hdr: what the asm really does (dumps, `-fdump-rtl-ira-all`)

- xb.spare is at xb+0x30, xb.hdr at xb+0x38. Reference: hdr in eax, spare in ebp, data (r192) esi, v (r187) edi. Without the pin both pairs are swapped; that's all of the 241 lines (51 core), the rest is jump offsets.
- r201 (hdr) and r202 (spare) have equal cost: only 3 refs in l5, head use at freq 34 and reload def + use at freq 10 (each ref costs 4 x freq; the memcpy's hdr + off is another pseudo, r267). The asm adds a ref at freq 34: 232 -> 368, pri 1 -> 2 (pri = cost / (excess points + 1), about 148), and an AREG preference. That lets r201 be pushed after r196 and the ECC group, so r327 (the memcpy's esi) stays uncolorable and pops first, which is what makes r192 take esi.
- A "use that emits no code" is **not** required. Two separate things fix it without any extra ref:
  - **(A) head/tail block freq >= 350 instead of 345.** Freq 345 = 100 / P(ECC), with 100 the ECC loop's exit (normalised, 1% of the 10000 top) and P(ECC) = 29% from PRED_CALL on calcPageEcc's arm (`_265 == 0` where pageErased is a PHI of 0 and pageErased.part.0). REG_FREQ floors 345 to 34; at 35 r187 takes edi and r192 esi, with no change of the push or pop order. `iw9exp.py src/image_write.c`: `__builtin_expect(!pageErased(...), 0)` with builtin-expect-probability 72..77 (P(ECC) 23-28%) leaves 57 lines (only hdr/spare swapped), <= 71 and >= 78 are 243+.
  - **(B) spare's pseudo number below hdr's.** They tie at pri 1 and the same cost, so the lower allocno is pushed first and popped last. Pseudo order = lowest SSA name of each PHI partition (hdr {288,294,295,461,462}, spare {290,299,300,465,466}).
- gen_iw153 `h1cu8+tHh` on the expect stand-in (build/iw/a9/h1.c, `iwlib.py build/iw/a9/h1.c -p 75 -v _finalizeImage`): `{ const uint8_t *h = xb.hdr; if (__builtin_expect(!pageErased(h + X, xb.spare + Y), 0)) calcPageEcc(xb.hdr + X, xb.spare + Y); } { const uint8_t *h2 = xb.hdr; memcpy(raw, h2 + X, 512); }`, no pin: **4 lines, the two preheader loads in the other order (hdr before spare)**, everything else in the object identical. The pin's whole job is reproduced without an asm, given (A).
- Load order vs (B): PRE inserts by value id at the preheader, then PHIs in the same order, popping a descending free stack (pops: 304 303 | 300 spare 299 298 | 295 hdr 294 293 | 290 spare 289 288 hdr ...). So the value inserted first has the higher names: spare first in the preheader (reference) means hdr's inner PHI (288) is lowest. To have both, spare's inner PHI must be the last name on the free stack (then hdr's inner PHI gets a new high name and hdr's lowest is 294 > 290). The stack at PRE holds only the unrolled spareUsed chain, 3 of every 5 names, 30 pops down to 256 (`pretmp_256` then 435). It'd have to be 9-10 names long. Not reached; gen_iw152 (384 finalizeImage forms) doesn't move it.
- (A) has no natural source so far. `continue heuristics` is 50% in this gcc (PRED_CONTINUE has no effect). The other predictors are too strong in DS with call's 71: anything >= .6 gives >= 78%, which is outside the window; the window needs a second predictor of .513-.58. gen_iw151 (96 forms of calcEcd, calcPageEcc: no flip at 345). A dead conjunct (untested, `&& p < 32`) would be net 0.
- Reloads after the ECC (gen_iw159, on the expect stand-in): `spare = xb.spare;` at the top of the page, `spare = xb.spare;` again in the arm after calcPageEcc, `memcpy(raw + 512, spare + Y, 16)` (`sa`, **drafts/image_write_near9_hdr.c**, `python tools/wip/dehint/iwlib.py tools/wip/dehint/drafts/image_write_near9_hdr.c -p 75 -v _finalizeImage`): natural source, no local for hdr, same 4 lines as h1: only the preheader's two loads swapped. It still has __builtin_expect in it, standing in for (A), so it isn't a candidate. A named variable's SSA version comes after all the gimplifier's temporaries, so `spare` loses to the `xb.hdr` temporary on value id, hence hdr's load first. gen_iw159's `hsc`, `hsb` (both named, spare first) have the preheader order and the ECC exit's order right but eax/ebp swapped (55). gen_iw160 (page pointers `sp = xb.spare + Y`, so the load stays a temporary): best 51. In these the first of the two tied allocnos popped isn't always the higher number's eax: see `iw9ira.py`, don't reason from numbers alone.

### near8's compare in constprop.1 (traced, not fixed)

`iw8ver.py` on near8 and src (dumps from `IWNP=1 iwdump.py <file> <dir> writeFsTable -fdump-tree-all`). Comparing src's and near8's name lists pass by pass is no use from the start: they differ from fixup_cfg4 on because the statements moved. What counts:

- Reference: `ivtmp.106_55 != ivtmp.109_82`, `ivtmp.106_78 != ivtmp.109_82` (end 82, both copies lower). near8: `ivtmp.109_78 != ivtmp.106_96`, `ivtmp.106_74 != ivtmp.109_78` (end 78, one copy 96 is higher). `Btop+St1` (build/iw/a9/bt.c): `107_59 != 110_82`, `110_82 != 107_177`: its low copy is now right and the other copy is a **fresh** 177.
- Chain for that name: split-paths' copy pops what ivopts released last, which is ivcanon's `ivtmp`; ivcanon pops 96, 98 in near8 and 55, 58 in src; those were `iftmp.20_95, _96` (near8: the small arm's `pages ?:`) and `iftmp.17_54, _55` (src: `pages` at the top of the inner loop). **They're released at dce2**, backwards, so the lowest name that's dead at dce2 is on top. A `pages` inside `if (type > 1)` is gone by ccp2 in the type-0 clones and doesn't count; one at an arm's top survives until dce2.
- So moving the names low works for that compare: gen_iw154 `sBi`, `sBt` (small arm's pages computed at the top of the block loop) fix constprop.1 but cost imgAdd 508+ (generic imgAdd's LIM order and the arm's frequency), and gen_iw155 (arms inverted, `if (!xb.bigBlock)`) costs 406 with imgAdd 261.
- Tried, stays at the one compare: gen_iw158 (81: 3 positions x 3 spellings of pages per arm), gen_iw143, 139, 144 on build/iw/a9/bt2.c (`Btope+St1i`, 744 forms). gen_iw156 (named `len >> 8` or `len / 512` ahead of the arms, to add a low dead-at-dce2 name): hi costs imgAdd 246+, `pg0 = len / 512` at the inner loop's top (`qiT`, build/iw/a9/qiT.c) keeps imgAdd right but constprop.1 53 (21 core), constprop.4 2, imgAddFile 4, writeFsTable 4. gen_iw157 (the same names on src with the dead test or optimize gone, 48): stays at 2 with no name, 248+ with one.

### Attempt 9 result: NO MATCH

Nothing identical with fewer tricks; src/image_write.c stays best at 6, reference.o is identical to build/obj/image_write.o and src compiles to it. No source file changed, no background work left.

Per trick after this attempt:

| Trick | State |
|---|---|
| pin_hdr | mechanism solved, see above: (A) freq >= 350 and (B) the tie, then the preheader's load order. All reproduced without an asm on the expect stand-in, 4 lines. (A) is what's missing: P(ECC) must fall from 29% to 28.5% or less without an expect |
| lnp2 | near8 unchanged: constprop.1's compare + writeFsTable 8 |
| pin_t, dead test, optimize, xmalloc | not moved. Named `len` values don't help them (gen_iw157) |

Scripts (repo root; `iwsweep.py gen_iwN.py -n TOP [-k label]`): `iw9exp.py`, `iw9ira.py`; gen_iw151 (calcEcd, calcPageEcc forms, no flip at 345), 152 (384 finalizeImage forms on build/iw/a9/ex.c at expect 75, no effect on the swap), 153 (gen_iw47's load orders there, `h1cu8+tHh` 4 lines), 154, 155, 156, 158 (near8's pages), 157 (src), 159, 160 (explicit reloads). build/iw/a9/ex.c = src with the pin removed and `__builtin_expect(!pageErased(...), 0)`; recreate with sed from src, compile with `-p 75`. build/iw/a9/{cmp1,own,ifs}.py are small dump readers, run from build/iw/a9 (dumps in src/, n8/, bt/ there). Careful: `iwlib.py` with neither -np nor -p adds the 50 param; and a stray `cat` or `python -` in a shell blocks on stdin, redirect `</dev/null`.

What I'd try next:

1. pin_hdr's (A): anything that lowers P(ECC) by 0.5 to 6 points without an expect. The test is `_265 == 0`, `_265 = PHI <0, pageErased.part.0()>`; PRED_CALL on the arm gives exactly 29. Look at where else a probability enters: pageErased not being split (fnsplit) so its loops' exits count before calcPageEcc's test, or the ECC loop's 1% exit block being split. A dead conjunct such as `&& p < 32` (not tried) is net 0: it would turn an asm into plain C, which the user prefers, but wouldn't lower the count.
2. Then the preheader's load order: spare's value id below hdr's with hdr's pseudo still below spare's.
3. near8: one more free low name in constprop.1's list at ivopts in the `Btop+St1` family, whose only bad copy is a fresh 177.

Lesson: **an asm pin's job can be two unrelated things.** Removing it changed the push order, so it looked as if it needed a code-free use; a frequency grid with expect + param showed the same allocation needs no extra reference at all. Use expect as a probe for what frequency a pin stands in for, before looking for a use.

## Attempt 10

Written as I go. New tools: `iw10a.py [probe..|file.c]` (expect probes on pageErased's loops, or any source file plain -O3: finalizeImage lines, the pseudos' registers, the `r267 -> r192` move copy's freq, depth-2 block freqs), `iw10b.py <gen>` (an expect-75 generator of attempt 9 with the expect stripped), gen_iw161-163 (forms of pageErased's loops).

- **(A) isn't about P(ECC).** With the ECC test untouched (P 29%, head block still 345), `__builtin_expect(spare[i] != 0xff, 1)` at -p 5..15 in pageErased, or the data test at -p 6..8, gives `r187 di, r192 si` and leaves **finalizeImage at 57 lines and everything else right** (build/iw/a10/grid.py). What moves is the not-erased flow: the threaded ECC entry block (bb48, 317) holds `r192 = r267` (cp freq 31), and it needs block freq >= 320 (cp 32). Head >= 350 was the same thing seen from the other side: bb48 scales with head. The window: per-byte mismatch 5-15% in the spare loop (>= 20 breaks pageErased, >= 25 blockEccOk too), 6-8% in the data loop.
- Why 4.5% today: PRED_LOOP_EXIT, first match, (100 - 91) / n_exits with 2 exits (`-fdump-tree-profile_estimate-details`). 4.5 is just below the window.
- The threshold is exact: q 5% gives bb48 320, cp 32, flipped; 4.5% gives 317, cp 31 (build/iw/a10/q5.py). It's 3 units short. Flows are conserved (M + C + E = 345: data mismatch 282, chain mismatches 35 with rounding, erased 28), so rounding won't supply them (`d4`, do-while data loop: M 284, but C falls, bb48 315).

### Forms that can't deliver (A), and why

All on src minus the pin, plain -O3; `iwsweep.py gen_iwN.py`:

- gen_iw161 (49: index in the test, countdown, do-while, `continue`, for both loops). `spare[i++]` etc. don't change anything: the loop has simple latches, so there's no header edge on the test and PRED_LOOP_EXIT stays. Only `if (spare[i] == 0xff) continue; return 0;` (`s5`) moves q: a PRED_CONTINUE on the block makes predict_loops skip PRED_LOOP_EXIT (dumps show no loop exit line), so DS decides: 62%. That's far past 15: pageErased 40, blockEccOk 35 (finalizeImage 61). Same for the data loop (`d5`, 222+).
- gen_iw162 (48): a test after the loop (`if (!spareUsed(spare)) return 1; return 0;`, `break` + `if (i == 16)`). u1, u3-u7, b1, b5 keep pageErased and all its callers right (finalizeImage 242, imgAddRaw 2), but **no flip**: the predictor is on that test (early return 39%), and threading then rebuilds the chain from the incoming edges, so the test's probability vanishes. Only the mismatch edge's own probability survives to bb48.
- gen_iw163 (21): flag forms of the whole loop (`ok = 1; for (i = 0; ok && i < 16; i++) ...`): 500+, not examined further. `c2`, a `break` in a braced arm, changes nothing.
- gen_iw164 (14): the ECC test itself. `<= 0`, `< 1`, `> 0` add opcode-positive: P(ECC) 18%, head 546, finalizeImage 405. `!= 1`, `== 1` work against it, 694. goto forms: same code as the plain test (241). Window is P(ECC) 23-28.7%, DS with call's 71 needs a second predictor of .503-.58. Hitrates read from this file's profile_estimate dump: opcode nonequal 72, opcode positive 73, pointer 85, call 71, const return 67, early return 61, continue 50, negative return 96: none fits.
- Ways that would work but aren't natural or don't count: a dead conjunct on the ECC test or a test that folds after inlining (factor .79-.989 on the way into the ECC loop; net 0, a swap at best, and (B) is still open, so no swap draft). Unknown bound on calcEcd's loop: exit edge is 1% from the max-predicted-iterations cap, 0x1066 can't reach 80-98.
- iw10b.py on gen_iw159, 153, 160 (attempt 9's reload forms without the expect): no flip. `sp = xb.spare + Y;` (gen_iw160 `Hs+A+`, build/iw/a10/n1.c) reads 102 lines but it's not near: the reload of xb.spare is gone and coloring is off.
- (B)'s load order: gen_iw166 (27: spareUsed's forms and its call, on near9_hdr and h1 at -p 75): stays at 4 or worse. spareUsed's form doesn't change PRE's stack.

### pin_t

gen_iw165 (180: 10 forms of partial x its type x t's position and type, src minus pin): best 10, unchanged. As attempt 8 says, it's t's 2 x (floor(a/10) + floor(b/10)) with the hot label's 85/15.

### lnp2: a new near state, and the inline reconsidered

gen_iw167 (72, on near8): one `pages` statement back at the inner loop's top, written as src writes it. `rm+I0q` (build/iw/a10/l1.c): **imgAdd and all three clones right, constprop.1's compare fixed**, no hot label, as predicted by attempt 9's dce2 chain. Left: writeInitialHeader inlines imgAdd.constprop again (93 + small call-offset lines elsewhere), imgAddFile 114, writeFsTable 4. `-fdump-ipa-inline-details`: time 3574.5 -> 3206.5, 10.3% against big_speedup's 10%: 368 saved, limit 357. So about 11 units at frequency .5, about 21 at callee scale, in `(op2 changed)` (505 in the clone's summary).

gen_iw168 (16): cheaper spellings. `rem512 = len % 512;` in the block loop and `pages = rem512 ? len / 512 + 1 : len / 512;` (`r1`) does stop the inline, but constprop.1's compare comes back (2), imgAddFile 114. `r5`, `quot` and `rem512` in the block loop: constprop.1 2, constprop.4 2, imgAddFile 137, writeFsTable 4. `len / 512 + (len % 512 != 0)`: imgAdd 147, constprop.1 53. gen_iw169 (24): partial, npages, t ahead of the block loop: 370+. `pg` moved (gen_iw167 g1-g3): the off-0 clone goes.

So the two facts conflict so far: the low name wants all of pages' statements in the inner loop's top, and the inline wants fewer of them there. Something else on len has to give up those 21 units, or the caller needs about 105 more time of its own (writeInitialHeader's own is 9.5).

### Attempt 10 result: NO MATCH

Nothing identical with fewer tricks, src stays best at 6. No source file changed. reference.o is identical to build/obj/image_write.o and src compiles to it (`iwlib.py src/image_write.c -np`: IDENTICAL). No background work left. Closest: **drafts/image_write_near10.c, no pin_hdr and no expect, 22 lines** (next section).

| Trick | State |
|---|---|
| pin_hdr | (A) solved by a natural helper, see the next section. Left: finalizeImage's two preheader loads swapped (4), blockEccOk 18 |
| lnp2 | near8 (2 + 8) still closest by lines; l1.c has the clones right but the inline and imgAddFile 114 |
| pin_t | gen_iw165: 10, unchanged |
| dead test, optimize | 2 lines each, not moved. `iw8ver.py` on src and src minus the attribute: the same names go at sccp vs at ldist, and the free stack then differs (ivcanon's pops {77 79 80 87 90 91 117 136} vs {56 57 58 67 77 79 80 87}), read-only so far |
| xmalloc | not attacked; thought through again, nothing new |

Scripts (repo root): `iw10a.py [probe|file.c]`, `iw10b.py <gen>`, `iwsweep.py gen_iw161.py` .. `gen_iw169.py` (`-k label` writes the variant to build/iw/<gen>_best.c). `build/iw/a10/grid.py` (the q window), `q5.py`. `build/iw/a10/l1.c` = gen_iw167 `rm+I0q`, `nopin.c`, `noopt.c` = src minus one trick, `fi_nopin.ira`, `fi_ex75.ira` = IRA dumps for finalizeImage, `ws/`, `wn/` = tree dumps with and without the attribute.

Lesson: **a probe with expect on a different branch can move the threshold you assumed was elsewhere.** Attempt 9 read (A) as head frequency because that's where its probe was. Grid the probe across every branch on the path before concluding which number matters.

### A real lever for (A): the byte helper

The heading "Forms that can't deliver" above is about those forms only; this one does. A byte test through an if-shaped helper leaves a PHI of 1 and 0 tested by the loop's exit (no early phiopt, the imgFits lesson). The profile_estimate dump shows a second `loop exit heuristics: 9.0%` line in such loops; read from memory of predict.c, unverified, that's predict_extra_loop_exits, undivided by n_exits. The chain's flow keeps 4.5% but each mismatch block now carries 9%, so bb48 comes to 346 (cp 34).

Two classes (gen_iw170, 171, 172: parameter type and spelling don't matter, only which edge reaches the 1):

- **Class u** (`static int byteUsed(uint8_t b) { if (b != 0xff) return 1; return 0; }`, and n, V, E, W shapes, `b < 0xff` on int, `b ^ 0xff`): r187/r192 flip with no expect, pageErased right, blockEccOk 18, finalizeImage 61 (hdr/spare swapped).
- **Class v** (`if (b == 0xff) return 0; return 1;`, and e, U, N, X shapes, inline flag `fl1`): no PRED_LOOP_EXIT on the mismatch, DS's 72% (50% with `b >= 0xff` on int: finalizeImage 65). **hdr/spare right with the natural load order**; left in finalizeImage: stack slots 0x28/0x2c/0x30 and the last bytes' layout (34). But pageErased 36, blockEccOk 26: their layout can't take that much. Push and pop order are the same as class u's; what differs is r256's choice of eax vs ebp at its pop, with bb48 at 796 (cp 79). Threshold not found: only those classes exist. A helper used by finalizeImage alone (`pageUsed`, gen_iw173) doesn't help: inlined whole early, there's no part.0, 167+.

On class u, attempt 9's reload forms work **without an expect** (gen_iw174): `spare = xb.spare;` at the page's top, reloaded in the arm after calcPageEcc (`sa`): finalizeImage 8. gen_iw176 `a`: the spare loop `break`s and `if (i == 16) return 1; return 0;`: the MU compare is right too, finalizeImage 4.

**drafts/image_write_near10.c** (`python tools/wip/dehint/iwlib.py tools/wip/dehint/drafts/image_write_near10.c -np`): plain -O3, pin_hdr gone, no expect, ordinary source. 22 lines:

1. finalizeImage 4: the two preheader loads, `mov eax,[hdr]` before `mov ebp,[spare]`. The conflict from attempt 9 stands (gen_iw177, 65; gen_iw178, 24): spare's head load as a temporary, or both named with spare first, gets the order right but eax/ebp swapped (55). In those forms the lower of the two tied pseudos ends up in eax (`iw9ira.py`), so hdr would need the lower pseudo with the later load. `h = xb.hdr;` ahead of the block loop (gen_iw178 `hH`) gets the registers right in the loop, but the loads go ahead of the `xb.blocks` test (30).
2. blockEccOk 18, every class u form: a forwarder block in the optimized dump holds the spare[12] PHI (`bb49: prephitmp_119 = PHI <...>; goto bb11`), where the reference has the PHI in bb11. The last compare is also `_168 == 255` rather than `!= 255`. In the RTL that shows as spare[12]'s load merged ahead of byte 11's compare, plus edx/ecx swapped at pageEccOk's first compare. gen_iw175 (blockEccOk's own forms) leaves it at 18 or worse.

What I'd try next:

1. near10's blockEccOk: anything that removes the forwarder, e.g. other shapes of the spare loop's exit on class u (gen_iw176 tried 13; `return !spareUsed(spare)` with spareUsed using the helper, `s1`, is blockEccOk 12 but finalizeImage 140; worth a look at why 12).
2. near10's load order: r256's or hdr's cost arithmetic at the pop (`update_conflict_hard_regno_costs`-style hops through r267); class v's flip shows it's reachable without touching the load order. bb48 between 346 and 796 would show the threshold, if some form gives it.
3. l1.c: find the 21 units. Read `(op2 changed)` statement by statement (`-fdump-ipa-inline-details`, `-fdump-tree-all` at einline's output), then ask which other statement on len can leave the loop without touching pages' spelling. Look at imgAddFile 114 at the same time.
4. Don't retry: plain loop forms in pageErased (gen_iw161), tests after loops without the helper (162), comparison forms on the ECC test (164), spareUsed's forms for the load order (166), partial x t grids for pin_t (165).

Scripts added since the list above: gen_iw170 (helper classes), 171 (parameter x shape), 172 (comparison spellings), 173 (finalizeImage-only helper), 174 (reload forms, `IWB=`), 175 (blockEccOk and MU forms, `IWB=`), 176 (spare loop's exit, on near10), 177, 178 (load order). Bases in build/iw/a10: b_us.c, b_vs.c = gen_iw170 `us`, `vs`; c_sa.c = 174 `sa`; d0.c = b_us.c with the `a` exit; d1.c = near10 with an unused local.

Lesson: **helper shape again, and on a loop's test this time.** `if (x) return 1; return 0;` inlined into a loop's exit test changes which predictor applies to it. Before concluding a predictor's value is fixed, check what makes a different one fire on that edge.

## Attempt 11

Written as I go. Base bases in build/iw/a11. New tools: `iw11cfg.py <dump>` (one line per block), `iw11trace.py <dumpdir> <fn>` (block order per pass), `iw11sched.py <file>` (sched2 trace of finalizeImage), `iw11refs.py`, `iw11probe.py <base>` (expect grid on pageErased/ECC test), `iw11inl.py <files>` (inliner numbers for writeInitialHeader), `iw11slots.py <file> <fn> [flags]` (LRA slots), `iw11p2.py <base>` (expect grid on `if (partial)`).

- **New lead: build/iw/a11/g1.c (gen_iw183 `P1+G` + gen_iw184 `nopin+ui`): no hot label AND no pin on t, pages at src's place.** `partial = (len < 0x4000) & (type != 0) & (type != '0');`, `if (partial) {npages..} else npages = 32;`, `unsigned t;`, `if ((uint8_t)t < 15)`. imgAdd and all clones right. Left (with the PROBE flag `--param inline-min-speedup=11`): imgAddFile 12 (slots r163 npages / r136 off+len), writeFsTable 8. Without the flag writeInitialHeader inlines (saved 363 of 3569.5 = 10.17%).
- **The inline has a second lever:** big_speedup is saved / (time w/o inlining), and imgWriteHdr is inlined into the caller first, so its statements raise the denominator: `iw11inl.py`. `(p / 32)` for the block number in imgWriteHdr: +49 and same final code (gen_iw181 `blk`). Needs +61 on g1.
- **drafts/image_write_near11.c (build/iw/a11/g3.c = g1 + gen_iw187 `f`): plain -O3, no hot label, no pin on t, no flag: 20 lines (imgAddFile 12: the slots; writeFsTable 8).** gen_iw187 `f`: imgWriteHdr's block number from the page: `*(..) = p >> 5`, `s->b2lo = p / 32 >> 8`: same code, but it stops writeInitialHeader's inline.
- imgAddFile's slots: r163 npages vs r136 off+len. Expect grid (`iw11p2.py`): flips at P(partial) >= about 55%. r136 has 2 refs in the head, so head:guard counts: e3 (early return on the error arm) has head 317 and the slots flip, P(fits) 61%. But the error block must be >= head/2 to be in bbro's round 1 (`tr.py`-style trace dump, build/iw/a11/tr.py): in the reference it's trace 2; with P(fits) > 50% it comes after the ret chain and its position costs lines (gen_iw185 e1, build/iw/a11/g2.c, 65 lines, only that block and two peephole2 scratch registers). Via imgFits the head edge stays 50/50 after threading and better_edge_p then takes the colder error arm as fallthrough (gen_iw182 e3). Raising P(big arm) with an early return on the small arm duplicates nFsFiles++ and that doesn't merge (gen_iw186, 210).

### pin_hdr (read before retrying it)

- Unsharing the helper (the task's lead) doesn't settle blockEccOk. gen_iw179: blockEccOk spelling its test with isErased, spareUsed, its own loops or a static copy of pageErased: 72 at best (`l1`), 119 for the static copy. The reference's blockEccOk needs pageErased inlined after its own early optimisation (split into head and part.0): PRE then reuses spare[12]'s load (`movzx eax,[edi+0x20c]`). A whole early inline or plain loops lose that. A static copy called once isn't split.
- What near10's 18 is: not a stray forwarder as such. Both src and near10 have a forwarder holding the prephitmp PHI. In src it sits straight after spare[0]'s mismatch block, with the unrolled chain below it and the ECC loop after the chain; in near10 the ECC loop comes before the chain, because threading through the helper's PHI (vrp1) duplicates every chain block, and duplicates go at the end (`iw11cfg.py`, `iw11trace.py`; order flips between vrp1 and copyprop1). That index order then changes crossjump/head merging: byte 11's mismatch load gets head-merged with the next block's.
- What near10's load-order conflict is: **it's decided at IRA's l0, not l5.** l0's a20/a21 are created walking the preheader block backwards, so the first load in the block gets the higher allocno number; costs tie (220), so it's pushed later, popped first and takes eax (fi_n10.ira, fi_et1.ira in build/iw/a11). So spare-first in the block gives spare eax. sched2 doesn't swap them: same priority (3), RFS_TIE on LUID (`iw11sched.py`). So the reference needs one of: hdr's cost above spare's at l0 (the asm's effect: any extra ref, 4 x freq), or eax already taken at l0 when spare pops (class v: the cap of r331 holds eax, spare gets ebp, hdr is spilled at l0 and gets eax in l4).
- `iw11probe.py` on et1 (spare-first, helper): expect on the helper's test at -p 7..9 gives finalizeImage 8 lines with load order and registers right, but that's a per-byte mismatch of about 40% (chain freqs 58, 42, ...), far beyond what pageErased's own layout takes (36). Plain base (et1p): stays 59+. So the hdr/spare flip wants a much bigger chain flow than the reg-order threshold (A).
- gen_iw180 (pageErased and the test via isErased/spareUsed, 40): nothing, 243 at best; `p8` (`return isErased(spare, 16)` after the data loop) is unchanged from plain.

### lnp2 and pin_t: near11

Base g0 = gen_iw183 `P1+G` with the probe flag `--param inline-min-speedup=11`, a way of looking past the inline: pages back at src's place, `if (partial)`, `&` partial. g1 = gen_iw184 `nopin+ui`. Family table (gen_iw183, 72, probe flag):

| Form | imgAdd, clones | imgAddFile | writeFsTable |
|---|---|---|---|
| `if (partial)` (G), `&` | constprop.1 2 (0 with `unsigned t` + no pin) | 12 (slots) | 8 |
| `if (partial > 0)` (A, D, E) | right with uint8 t and pin | 114 (compare `npages_134 > p_145`) | 4 |

- A's compare: p is split-paths' copy, which pops what reassoc2 released, which reassoc1 popped from dom2/phicprop1's dead names (`i_46 = PHI <0>` in src, 145 in l1): `iw8ver.py`. gen_iw182 (500 imgAddFile-only forms) doesn't move it.
- Slots in G: only r163 npages and r136 off+len swap (`iw11slots.py`). r136 has two refs in the head block. Tried: fits arm 61% by early return (gen_iw182 e3, 185): slots right, but only with the error block out of bbro's round 1; see above. One hint in imgAddFile instead (gen_iw189: hot label or expect on the big arm 165, dead tests 22-328): no. Predictors on partial's test: types and spellings of `> 0` (gen_iw188, 280: 130 at best); `!= C` on a kind variable (gen_iw190: K1, K3, K5, K6 predict 72% but imgAdd 106 with `&&`; K2, K4 fold and predict nothing). Early-return arms with nFsFiles++ duplicated (gen_iw186, 210: no merge).
- writeFsTable: decoupled. On near11 4 flips of 2 compare pairs in the big copy. gen_iw122 grid stays at 8. iw8wf seed 1101 (g1, modes dead, opt, both): see the log build/iw/a8/wf8_1101.log; some forms with the attribute gone reach 2 lines there, which is no better than src's.
- Borderline in near11, if it ever lands: `p >> 5` next to `p / 32 >> 8` in imgWriteHdr is there only to raise the caller's time (+61 needed; two spellings stop FRE from merging them); `(uint8_t)t` on an `unsigned t` is there for the slot tie. Other imgWriteHdr spellings in gen_iw187 don't reach the threshold.
- gen_iw191 (npages' spelling x the loop's head, 30): the 12 slot lines don't move.
- iw8wf seed 1101 was stopped early (at least 528 states). Its bests on g1: attribute gone 2 lines in writeFsTable, dead test gone 4. No hit; don't read this as a full search.

### Attempt 11 result: NO MATCH

Nothing identical with fewer tricks; src stays best at 6. `iwlib.py src/image_write.c -np`: IDENTICAL; reference.o is identical to build/obj/image_write.o. No src change, no background work left.

Closest: **drafts/image_write_near11.c, would be 4 (dead test, optimize, pin_hdr, xmalloc), both lnp2 and pin_t gone, plain -O3: 20 lines** (`python tools/wip/dehint/iwlib.py tools/wip/dehint/drafts/image_write_near11.c -np`): imgAddFile 12 (only slots 0x30/0x34 swapped, every reference to them), writeFsTable 4 flips (8 lines). imgAdd, all clones and writeInitialHeader byte-right.

| Trick | State |
|---|---|
| lnp2, pin_t | near11; the slots are what's missing |
| pin_hdr | near10 unchanged; both remaining differences explained above; unsharing the helper doesn't work |
| dead test, optimize | writeFsTable only, 2 lines each from src; on near11 8 with both kept |
| xmalloc | not attacked |

Next:
1. near11's slots: r163 needs about +5 REG_FREQ units against r136 (P(partial) about 55% in the expect grid, guard 500), while t's tie needs a guard freq that's a multiple of 10 (500 is one, so P of exactly 5/9 would serve both). Or fewer on r136. Don't sweep imgAddFile's forms or npages' spelling again.
2. If slots can't go naturally, spend one hint there if it's net -1: anything but what gen_iw189 tried.
3. Then writeFsTable on near11 with `iw_tuples.py` and iw7wf (decoupled), wanted: both big-copy compare pairs flipped.
4. Don't retry: blockEccOk unshared forms (179), isErased/spareUsed forms (180), imgAddFile-local forms for A's compare (182), partial's types (188).

Scripts: `iwsweep.py gen_iw179..191.py` (`IWB=` other base; gen_iw183, 184 use the probe flag), bases in build/iw/a11: g0 = 183 `P1+G`, g1 = 184 `nopin+ui` (finalizeImage's `t` reverted to uint8_t by hand; no effect on bytes), g2 = 185 `e1`, g3 = near11, et1 = gen_iw177 `et1`, et1p = et1 with the plain spare test, tr.py <file> (bbro traces for imgAddFile, run from build/iw/a11).

Lessons: **a probe flag that removes one known difference (`--param inline-min-speedup=11`) lets a sweep see the state underneath: this family had been discarded for its 89 inline lines.** And big_speedup is a ratio, so the caller's own time is a lever: statements in another inlined callee can stop an inline without touching the callee in question.

## Attempt 12

Written as I go. New tools (repo root): `iw12blocks.py <file.c> <pass> [fn] [flags]` (one line per block: freq, successors with probability), `iw12arms.py <file.c> [fn]` (profile_estimate's predictions per block), `iw12slotfreq.py <file.c>` (slot lines and, per stack slot, its memory refs with block freqs and the REG_FREQ total; `IWFN=` other function), `iw12probe.py <base.c> [big|fits|raw1|outer|inner|partial]` (expect + param grid on one branch; edit GRID), gen_iw192-195.

### imgAddFile's slots, in numbers

- `iw12slotfreq.py` on near11: off+len (r136) refs: head 386, 97, 26, 89: REG_FREQ 38 + 9 + 2 + 8 = 57. npages (r163): 81, guard 450: 8 + 45 = 53. src: npages 8 + 63 = 71. The higher total gets the earlier slot; a tie goes to the lower regno, r136. So npages needs +5.
- The ratio doesn't depend on the 10000 anchor: scaling inner loops moves both sides. What moves it: P(partial), or the head relative to the big copy (joint P(fits) x P(big)), or the outer loop's iteration count.
- **New probe result: P(big) in imgAddFile, `if (!xb.bigBlock)`, at 57, 58, 59, 60 (expect + param, `iw12probe.py near11 big`) puts imgAddFile byte-right: only writeFsTable 8 left.** At 56 the slots are still swapped (head 345, 34 + 9 + 2 + 8 = 53, tie, regno loses); at 61 the error block leaves bbro's round 1 (head 317, error 158 < 158.5, a rounding), 62: 111, 65: 55, 70: 69, 80: 111.
- P(fits): 51-53 stays 12, >= 54 costs the error block's place (52+); that's attempt 11's head/2 rule. So the lever is P(big) alone, and the target is 57..60 with no flag.

### Getting P(big) into 57..60 without a flag: what's been ruled out

Available hitrates (profile_estimate dumps): call 71, early return 61, opcode nonequal 72, opcode positive 73, pointer 85, negative return 96; a combination DS(a, b) has to land in .57-.60. Nothing natural does:

- **Early return (gen_iw192).** `if (!xb.bigBlock) { imgAdd; nFsFiles++; return; } imgAdd; nFsFiles++;` (`e1`): 50%: predictors fire on both arms (dump shows 61 and 39) because a block only escapes the heuristic if it's the one right before the return block, and the log arm sits there. Reordering so that big falls into the return block puts the log arm under the heuristic, P(fits) 61, which loses the error block's place (attempt 11). A static helper holding the two calls (`h1`, `h2`, 67 lines): the helper itself gets P(big) 61, but then imgAddFile's fits arm is a single block and it's the one with the early return: P(fits) 39, head 406. And 61 itself is above the window (head 317, error 158).
- **Dead null test in the big test (gen_iw194, gen_iw196: 104 forms; a dead test local to imgAddFile, which would be net -1).** The null test on `time` or `name` dies at VRP after the dereference and the predictor fires at profile_estimate, so the mechanism works, and the error stays local. Shapes `a && b` / `a || b` change PRED_CALL too: read from the dumps, test1's edge to the second test gets 71 and the second test gets one call 29 combined with its own predictor. D1 `!big && time`: test2 DS(85, 29) = 69.8, P(big) .504. D3 `time && !big`: test1 93.3, test2 29, P(big) .73, head 265. So P(big) = 1 - .71 x DS(.29, x). To land in the window x would need .76-.79; the ones available give .504 (85), .636 (72), .627 (73). No hit, best stays 12 (gen_iw196's shapes A-M x 8 conditions, including a dead return in either arm and a dead arm with a call).
- `__builtin_expect` at its default 90: as x in the same formula, P(big) .558 (`if (xb.bigBlock && X)`): head 346, 34 + 9 + 2 + 8 = 53, a tie, and regno favours r136. Not run: computed only.

### Other levers on the slots, ruled out

- **An asm on npages in imgAdd (gen_iw195), net -1 if it replaced lnp2 and pin_t:** best 50 (imgAdd 28, imgAddFile 14). Other positions 600+.
- **Dead `break` in the outer loop for a second exit (gen_iw197):** 676+, the clones go. Don't retry.
- **Partial's own forms (gen_iw193, 64: S1-S12 x `if` spelling x pin):** none flips the slots. I read one by dump, S10: its guard is still 450 (bb19 50%). `small = type != 0 && type != '0'; partial = small && len < 0x4000;` (`S2`) ties near11 at 20 and may read better than the `&` chain. `&&` forms keep imgAdd at 102+, as attempt 8 said; imgAddFile 22 (slots plus a compare), writeFsTable 4.
- **Family A (`if (partial > 0)`, pin kept) as a one-trick reduction:** build/iw/a12/A.c: imgAddFile 114, writeInitialHeader 93 (the inline is back), writeFsTable 4. gen_iw192's helpers on it: 158 at best.

### Other arithmetic worth keeping

- `iw12slotfreq.py` with `IWFN=imgAdd`: t's slot total is 6 + floor(a/10) + floor(b/10), partial's 6 + 90. near11 96 v 96 (tie, regno favours t), near8 95 v 96. A tie needs round(900 P) to be a multiple of 10: P .5778, .5889, .6, .6222, .6333, ... of the DS values only DS(.72,.39) = .622 and DS(.73,.39) = .6335 land on one, and there's no early return on that test.
- Head's flow to the loop: 386 x .25 = 97, x .96 x .96 (the two `return -1` tests) = 89, x .91 (the loop's entry test, from PRED_LOOP_EXIT on the copied header) = 81, x 11.1 = 900. Removing the .91 alone would tie (35 + 8 + 2 + 8 = 53), and it can't go: the reference has both entry tests.

### imgWriteHdr's spelling (gen_iw198, 36: hi x lo byte)

Only `p / 32 >> 8` for the high byte stops the inline; the low byte can be `p >> 5` or `(p >> 5) & 0xff` (`h0l5`, same 20 lines, reads slightly better as a byte store). Every other pair is 117 (writeInitialHeader 89). No tidier form found.

### writeFsTable on near11

iw7wf seed 1201 (500 s, 2376 states, attribute kept, up to 1 dead test): best writeFsTable 6, no zero: `{'base': 0, 'head': 0, 'store': 3, 'buf': 1, 'loop': 0, 'log': 1, 'tail': 0, 'cf': 0, 'lb': 1, 'ls': 7, 'dead': [(5, 3, 0)]}` (build/iw/a7/wf_1201.log; render by iw7wf's `render`). Seed 1202 (420 s, 1 worker, 660 states, attribute off): best 10. Both are short samples, not exhaustive; base imgAddFile's 12 is in their totals. As the task said, re-tune this last.

### Attempt 12 result: NO MATCH

Nothing identical with fewer tricks; src stays best at 6. `iwlib.py src/image_write.c -np`: IDENTICAL; reference.o identical to build/obj/image_write.o. No source draft is new: near11 stays closest (20 lines, would be 4). No image_write_a12.c because nothing verified. No background work left.

| Trick | State |
|---|---|
| lnp2, pin_t | near11; imgAddFile is fixed by P(big) 57..60 and only that, so far as probes go; no natural or single-dead-test source reaches it |
| dead test, optimize | writeFsTable 6 at best on near11, with both kept |
| pin_hdr, xmalloc | not attacked this attempt |

Reproduce the probe: `python tools/wip/dehint/iw12probe.py tools/wip/dehint/drafts/image_write_near11.c big` (GRID at the top of the script; at time of writing it holds a `partial` grid, set 57..60), or `python tools/wip/dehint/iwlib.py build/iw/a12/bigx.c -p 58` (near11 with `__builtin_expect(!xb.bigBlock, 0)`): only writeFsTable 8. The expect and the param are a probe, never a candidate. `partial`'s probe is noisy (the expect itself costs constprop.1 53 lines through names), so read only imgAddFile's column there.

Scripts: `iwsweep.py gen_iw192.py` (early returns, helpers; `IWB=build/iw/a12/A.c` for family A), 193 (partial's forms), 194, 196 (dead test in the big test), 195 (asm on npages), 197 (dead break), 198 (imgWriteHdr's spelling). Bases in build/iw/a12: bigx.c, A.c, D1.c, D3.c, E1.c, e1.c, h1.c, s10.c.

What I'd try next:

1. A P(big) of 57..60 from something not in the list above. The test: `iw12arms.py <file>` for the predictions, `iw12blocks.py <file> optimized` for head (wanted 322..339).
2. A second predictor on the dead test in `big && x`: x has to be .76-.79. DS(.85, .39) = .783 and DS(.67, .39)= .7605 would do, so a dead test that also carries an early return is the shape to think about, though it may no longer read as code.
3. pin_hdr and xmalloc weren't touched here, and near10's blockEccOk 18 and load order (4) are independent of everything above.
4. Don't retry: helpers holding the two calls (fits goes to 39), a second exit on the outer loop, asm on npages, partial's spellings for the guard's frequency, tidier imgWriteHdr spellings by hi and lo byte.

Lesson: **grid the probe across every branch on the path, then do the arithmetic per slot.** Attempt 11 probed only `partial`; the same slot flip was available from `if (!xb.bigBlock)` with no effect anywhere else, which only the slot totals explain. Knowing the exact window also rules out whole families on paper before compiling them.

## Attempt 13

Written as I go. New tools: `tools/wip/dehint/iw13x64.py [addr]` (image_write's functions in tmp/xeBuild64: extents from .eh_frame, strings, callees; with an address, one function's disassembly). build/iw/a13/nohdr.py in.c out.c drops imgWriteHdr from any draft.

### What the Linux build shows

Function order and set in tmp/xeBuild64 match src exactly: 41b810 buildImage, 41c360 pageErased, 41c1b0 blockEccOk, 41c6c0 imgSizeAligned, 41c960 imgAdd (generic, 1180 bytes), 41ce00 imgFits (25 bytes, a real function), 41ce20 imgAddFile, 41d210 imgAddFileAs, 41d280 imgAddMobile, 41d580 addSmcConfig, 41d610 writeInitialHeader, 41d7e0 checkBootImage, 41dbc0 writeFsTable, 41e4e0 finalizeImage, 41eef0 imgAddRaw. Clones in front of buildImage: 41b1b0 (off 0, type 0, pad 1), 41b3b0, 41b5c0 (type 0, pad 1).

- **There's no static helper that src lacks**, and no block or page arithmetic helper. imgAdd is one body with the same statements as src: rawSize tests, x/first/rem/tail/blocks, the two spellings `(len + 512) / 512` and `len / 512 + 1`, the `left` formula, the arms' order.
- **imgWriteHdr isn't real.** Linux's writeInitialHeader has no helper: `if (xb.bigBlock) imgAdd(0, &hdr, 0x80, 0, 0xf1f1, 1); else imgAdd(0, &hdr, 0x80, 0, 0x1ffb, 1);`, and gcc inlines one of the two.

**drafts/image_write_nohdr.c = src with imgWriteHdr deleted and that plain call: byte-identical (`iwlib.py ... -np`: IDENTICAL).** Everything said in earlier notes about imgWriteHdr's spelling (the inline threshold, `p >> 5`, gen_iw181, 187, 198, "the caller's time") is obsolete: with the plain call, near11 is the same 20 lines without `p >> 5`, and the writeInitialHeader inline that discarded so many states isn't there any more (near8 + nohdr: 10 lines; l1 + nohdr: no inline, imgAddFile 114 + writeFsTable 4). Reproduce: `python build/iw/a13/nohdr.py <draft> out.c`.

### The block type is a bitfield

Linux's stores read like bitfield writes, and the struct is the one every Xbox 360 NAND tool has (`FsBlockType:6, ECC3:2` in spare byte 12). src's bits b2lo/b1lo are bitfields already, byte 12 wasn't. `((struct spt *)s)->type = type;` for `s[12] = (s[12] & 0xc0) | (type & 0x3f);` with `struct spt { uint8_t b[12]; uint8_t type:6, ecc3:2; };` emits the same RMW at expand but has no load in gimple, so every SSA number in imgAdd moves. On near8 + nohdr (build/iw/a13/n8_bf.c): **constprop.1's compare is fixed, lnp2 gone, only writeFsTable 4 lines** (two flips); attribute removal costs nothing there (n8_bfna.c, also 4). gen_iw204: both arms need it (one arm: 28).

**drafts/image_write_near13.c (= build/iw/a13/w2.c), would be 4 tricks (pin_t, pin_hdr, optimize, xmalloc: lnp2 and the dead test gone), plain -O3: 2 lines, one compare operand order in writeFsTable's big copy.** `python tools/wip/dehint/iwlib.py tools/wip/dehint/drafts/image_write_near13.c -np`. It's near8 + nohdr + bitfield + two iw8wf writeFsTable spellings (`fsTable[-xb.fsStart + blk]`, `setBeU16(off >> 14, ...)`).

The compare: bb15 `ivtmp.429_158 != _212`, the reference has `_319 != ivtmp.433_391` (`iw13cmp.py <file>` lists all of them). Reference: small copy inc < end, big copy end < inc. ivopts allocates inc first and the end later, so the big copy needs a stack that hands out a high name and then a lower one, i.e. a run boundary between the two pops. In the reference inc 391 is the last of the high run (369, 389, 391) and the end comes from the next run (313..322). In near13 inc and end are both from the ascending run released at ccp2 (158, 159, 160, 162, 212, 214, ...: `start + i`, `len & 511`, dead there once the constants arrive). `-fdbg-cnt=ivopts_loop` doesn't exist in this gcc, so the pop order is inferred, not read.

Borderline in near13: `int partial = (len < 0x4000) & ...; if (partial > 0)` gives P(partial) 73% from the positive-opcode predictor, which is what flips imgAddFile's slots without P(big). `_Bool partial`, `partial >= 1` are the same bytes. `pages` spelled differently in the two arms. `fsTable[-xb.fsStart + blk]` has no reason other than names.

### Tried on the bitfield family, all stuck (2 lines on near13 unless noted)

- Whole-file random: iw8wf seeds 1303, 1304 (n8_bf, all modes: dead gone 2, attribute gone 4, both 6), 1305 (near13, 2400 states); iw7wf 1301, 1302 (attribute off, 4), 1307 (4 bases, 3608 states, up to 2 dead tests: 2). iw13an seed 1306 (anneal over imgAdd + writeFsTable forms, 1480 states). All 0 hits; samples, not exhaustive.
- Sweeps, `iwsweep.py gen_iwN.py`: 205 (end, size, head, loop spellings), 206 (one dead test: position x condition x body), 207 (blk vs start + b per use, blk's position, pages), 208 (the attribute's flag swapped for each of gcc's 203 optimizer flags: only flags with no effect tie), 209 (602 spellings of imgAdd's FS chain), 210 (typed local struct pointers per arm: no effect on bytes, so real struct code is free to use), 211 (one empty asm in writeFsTable: no effect), 212 (src + nohdr, each trick on/off x bitfield: nodead 2, noattr 2, both 4, bitfield with src's `pages` 53+). gen_iw203 reruns any older generator on a new base, no FOCUS, no flag: 139, 140, 143, 144, 147, 156, 158, 193 on near13 stay at 2.
- pin_t on the family (gen_iw201): `np` imgAdd 10. With P(partial) 73: t total 6 + 65 + 24 = 95 v partial 96, the carry from 657 + 243. Needs P x 900 to round to a multiple of 10, none of the predictors gives one. Range test `if (type >= '1' && type <= '?')` replaces `t` naturally on near11 at 2 extra lines (constprop.1, gen_iw200 t0).
- `pages` at the inner loop's top with the bitfield (l1_bf.c): writeFsTable 2 but imgAddFile 114, gen_iw182 doesn't move it.

### xmalloc

Linux's memcpy shows the alignment prologue too, but that's no evidence: gcc 4.9 may not use the dest alignment alone. In this gcc a known dest with an unknown source gets no prologue. Late CCP restores the alignment whatever the form: gen_iw199 (`mem + (b * 32 + p) * 528` etc., 201 lines, no prologue, no continuing pointer), build/iw/a13/xm.py (ways of storing the result, 180). `raw` is malloc's SSA value in the reference (`[esp+0x28]`, no reload of xb.raw). No natural source found.

### Attempt 13 result: NO MATCH

No byte-identical state under 6. Useful and landable with no change of count: **drafts/image_write_nohdr.c (src minus imgWriteHdr), IDENTICAL.**

| Trick | State |
|---|---|
| lnp2 | gone in near13; the bitfield fixed constprop.1's compare |
| dead test | gone in near13, the one compare left; or kept with 4 lines (n8_bf) |
| optimize | n8_bfna: attribute gone, dead test kept: 4 lines; both gone 6 |
| pin_t | 10 lines without it, see above |
| pin_hdr | not moved; Linux's preheader loads spare then hdr, as the reference. Not attacked |
| xmalloc | see above |

Next:
1. Near13's one compare: more of the real source. The two finds of this attempt both came from reading what the code really was, not from names, so look for a third: other things the original had as fields or expressions (byte 12 was one). `s[9]`, `s[7]`, `s[8]` as FsPageCount and FsSize, `(off & 0x1ffff) ? ... : 256` etc. moved as one value.
2. Don't take the `imgWriteHdr`, inline-threshold or big_speedup notes above as live; re-judge anything a sweep rejected for writeInitialHeader's 89 lines. Rerun with gen_iw203 and nohdr.py.
3. Run big forms against n8_bf and near13 by total lines; writeFsTable is not decoupled in this family.

Scripts: iw13x64.py, iw13cmp.py, iw13an.py, gen_iw199-212. Bases in build/iw/a13: n8.c, n8_bf.c, n8_bfna.c, n8_nd.c (byte form, no attribute, no dead test: 6 lines, constprop.1 2 + writeFsTable 4), w2.c, w2na.c, l1_bf*.c, n_nohdr.c (near11 + nohdr), trace.py (one name through every pass, run in a cmp_* dir).

Lesson: **the Linux build settled in one read what five attempts of arithmetic hadn't.** A helper in our source that the older build lacks is suspect, and a store that reads as a bitfield write is one. Test a claim in a source comment before building on it: imgWriteHdr's comment said the plain call couldn't inline, and the plain call matches. I didn't work out why it inlines there.

Landed after attempt 13: drafts/image_write_nohdr.c is now src/image_write.c (imgWriteHdr gone, still 6 tricks, full build matches), so the draft is removed. Treat "src + nohdr" above as plain src; nohdr.py is only needed for older near drafts.

## Attempt 14

Written as I go. New tools in tools/wip/dehint: `iw14names.py <file.c> [fn] [-p pass]` (per tree pass, SSA versions that appear and go; dumps in build/iw/a14/nm_<name>), `iw14pop.py <dumpdir>` (every name ivopts takes, per candidate, with what it held before), `iw14def.py <dumpdir> <n>...` (one version's definition per pass), `iw14gap.py <dumpdir>` (versions in no dump), `iw14rejudge.py <base> <log> [cap] [first] [last]` (reruns old generators on a new base by total lines, dropping options that don't apply, dedupes, logs `WF0` for any state with writeFsTable clean and saves it as build/iw/a14/wf0_*.c), gen_iw214-217.

### Where ivopts' names come from (checked with dumps)

- **The versions "in no dump" are virtual operands.** Default dumps hide `.MEM_n`. With `-fdump-tree-oaccdevlow-vops`, near13's 352, 372, 373, 374, 376 are VDEFs (372-374: `s[9] = xb.spare9`, `s[8] = xb.spare8`, `s[7] = xb.spare7` in the second copy; src's 389-391 are the same three stores). So **the reference's big-copy increment `ivtmp.430_391` is the name of src's dead `s[7] = xb.spare7` store**, and the next pop `ivtmp.430_279` is that store's load (`_279 = xb.spare7`). In near13 the increment is `_158 = start + i` from the big copy's FS chain and the bound `_212 = _37 & 511`.
- High versions match across drafts at a fixed offset (near13 n = src n + 17), so the two have the same stores, in a different stack order: src pre takes pair 2 (390, 278), ivopts gets pair 1 at position 7-8 and pair 3 at 14-15. near13 pre takes pair 3 (374, 264), ivopts gets 372 at 9 and pair 2 (373, 263) at 17-18. The increment of the big copy is position 14 (three candidates from iw14pop.py: PHI, increment, init; bound after).
- The sequence isn't monotonic in release order, so I read it as passes taking names and releasing them again inside themselves (vect, cunroll), which reorders the stack. That part is inference; I couldn't read the pop order directly and iw14pop.py's order inside a candidate is assumed from what the dumps show. It means counting by hand doesn't predict a flip.
- `tail && pad == 1` and `pad == 1 && tail` both give the same result, as gen_iw44's old note suspected: **the big copy's compare is right there**, writeFsTable 6 (bb16's split-paths copy and the outer compare wrong instead). The front end folds them to one `&` branch, so imgAdd has one branch where the reference has two: 571 lines. It's evidence that spending a few more names in imgAdd's pad code moves this compare, nothing more.
- Checked in the gimple dump: `pad == 1 && tail` is `D = pad == 1; E = tail != 0; F = D & E; if (F != 0)`, the nested form is two `if`s.

### Tried on the family (totals; base 2 lines unless noted)

- **drafts/image_write_a14.c = near13 with `fsTable[blk - xb.fsStart]` for `fsTable[-xb.fsStart + blk]`: same 2 lines, one borderline spelling gone.** Would be 4 tricks. Linux has `mov eax,ebx; sub eax,[fsStart]`, so this is the real form. `python tools/wip/dehint/iwlib.py tools/wip/dehint/drafts/image_write_a14.c -np`.
- `setBeU16(blk, ...)`, which Linux shows (`movzx edi,bx`): 48 lines, writeFsTable only, stack slots shift by one (build/iw/a14/a14_t0.c). `off >> 14` stays as the one spelling there with no reason but the result; compare still wrong with it.
- gen_iw214: FsPageCount, FsSize and pages forms (5 pages x 7 left/count x 4 store orders x st0 x t0, 560): floor 2. `left` as the free count first (`c1`), reusing `pages` (`c2`, `c3`, `c4`), or `pages` holding the 256 part (`c5`) don't flip it. c3, c4: imgAdd 2 more. `(len + 511) / 512` is worse.
- gen_iw215: type-arm shapes (order, `||` form, `goto`, where s[5] goes, small arm order, 64): floor 2. Swapped arms: imgAdd 66. `s[2]` before `s[9]`: 8. Worth knowing: `continue` for `if (type == '0')` in the small arm is the same bytes (`s3`).
- gen_iw216: writeFsTable's length (`p - buf`, a running size, `i << 10`, 0x4000 in a variable, 88 with attribute on/off): floor 2, or 6 with the attribute off, same as `i * 0x400`. Nothing tells the attribute apart from the spelling of i.
- gen_iw217: pad forms that keep two branches (`int zero = ...`, `s2`, `s3`, 19): those keep 2. The rest lose the two branches or the order: 150 to 1214. `if (tail) if (pad == 1)`, Linux's order: 662, imgAdd's test order is pad first.
- gen_iw218: the block offset as one local (`bo` or `pg` = off & 0x1ffff; place x partial's form, 40): in the arm or at the use, 2; at the top of the page loop, 12. A value at the head or per block: 227+.
- gen_iw219: FS chain as one store (ternary, `v` local, `k` local, `SWAP16(cond ? next : k + 1)`, 12): 128 at best.
- **iw14rejudge.py over gen_iw1-213 on a14** (cap 120 per generator, repeats skipped; log build/iw/a14/rj2.log; a first pass on near13 at cap 150 stopped around gen 165 with no hit): nothing at 0. Of the generators with something that ran, 81 had a best of exactly 2, none below. It's a sample where a generator has more than 120 combinations, not exhaustive. **Only 4 states have writeFsTable clean, all from other families:**

| State | Change | Total | Why it can't land |
|---|---|---|---|
| gen_iw100 `m+pb` (same as gen_iw218 `ms+aa`, `for+aa`) | `partial = type != 0 && type != '0' && len < 0x4000` + block offset as a local before the arms | 122: imgAdd 100, imgAddFile 22 | Tail tested before pad and registers rotated in imgAdd. This is `&&` partial's old cost (attempt 8). gen_iw217 on it doesn't fix the order: 122 floor |
| gen_iw52 `v9` (`fsTable[..] = cond ? a : b`) | one store in the FS loop | 128: constprop.2 104, constprop.1 6, imgAdd 8 | constprop.2's loop has a `cmov` and isn't unswitched. Real structure wrong: the reference has two stores |
| gen_iw147 `e03`, `x03` | a dead test on `len` in imgAdd's FS section | 140, 150 | new dead test; imgAddFile 114 |

So the compare can flip, and every way found so far costs more elsewhere. `&&` partial reads best of them and Linux's `setne, setne, and, setbe, and` doesn't argue against it, but that's gcc 4.9 and it folds to `&` anyway.

### Attempt 14 result: NO MATCH

No byte-identical state under 6. `iwlib.py src/image_write.c -np`: IDENTICAL. Closest: drafts/image_write_a14.c, would be 4 tricks (pin_t, pin_hdr, optimize, xmalloc), plain -O3, 2 lines (`cmp esi,edx` vs `cmp edx,esi`, writeFsTable's big copy). No pin_t, pin_hdr or optimize work beyond what's above, since the compare didn't yield; re-read Linux's finalizeImage and got nothing usable for pin_hdr. src-side check: `gen_iw201` forms without pin_t on src: none under 7.

Next:
1. Read the stack as far as it's readable: iw14pop.py on a14 against src. Target is any high VDEF name or later-released name at the increment's place (position 14). Names from the dead `xb.spare*` arm are the candidates, because that's what src has there.
2. Why does pre take pair 2 in src and pair 3 in near13? `pre new 18` vs `19` is the one count that differs in the table. A difference in what PRE inserts in imgAdd's copies, rather than in what's released, hasn't been looked at.
3. `&&` partial is the only natural state with writeFsTable clean, so its imgAdd cost (pad and tail order, registers) is the thing to understand. It hasn't been looked at since the name-stack reading.
4. Don't retry: spellings of FsPageCount, FsSize, left and pages (214), type-arm shapes (215), length spellings (216), pad forms (217), one store in the FS loop (219). Rejudging older generators on this family (rj2.log).

Reproduce: `python tools/wip/dehint/iw14names.py <file> writeFsTable -p ivopts`, then from build/iw/a14 `python ../../../tools/wip/dehint/iw14pop.py nm_<name>`. For VDEFs: compile with `-fdump-tree-oaccdevlow-vops`. `python tools/wip/dehint/iw14rejudge.py tools/wip/dehint/drafts/image_write_a14.c build/iw/a14/rj2.log 120` took under 40 minutes with 4 threads. Scratch bases in build/iw/a14: pa.c, pb.c (`&&` pad), foraa.c, v9.c, c1.c (if/else calls, 50 lines: slots and block order).

Lesson: **`.MEM` names share the SSA counter and the free list, and default dumps hide them.** A "name in no dump" is usually a store. A store dead in one inlined copy can name a loop variable in the other, so what's dead in a copy matters as much as what's live.

## Attempt 15

Written as I go. New tools in tools/wip/dehint: `iw15dump.py <name> <file.c> [flags]` (tree dumps with `.MEM` names and pre-details, build/iw/a15/d_<name>), `iw15stack.py <dumpdir> [fn] [first] [last]` (names new and gone per pass, `.MEM` marked `m`), `iw15src.py <dumpdir> [fn]` (each name ivopts takes, the last pass it was live in, what it held, `.MEM` included), `iw15pre.py <dumpdir> <fn>` (what PRE inserts, with value ids), `iw15sig.py <file.c>...` (writeFsTable's compare signature), `iw15grid.py <base.c> [kmax] [mmax]` (probe grid by signature), gen_iw220-227.

GCC source: I tried CLAUDE.md's official URL for tree-ssanames.c once. gcc.gnu.org answered with an Anubis access-denied page, so nothing below comes from reading source. I didn't try to get round it or use a mirror. Anything about how the free list works internally is inferred from dumps.

### The signature

`iw15sig.py` reads the five `if (ivtmp != _bound)` tests in writeFsTable's ivopts dump, in dump order: `<` when the increment's version is below the bound's, `>` above. Later passes put the lower version first, so this predicts the emitted operand order. Target (src): **`<>><<`**. The positions are the small-copy loop, the big copy's inner loop (the known compare), the big copy's outer loop, and the two page loops of the other copy (C1 and C2 below; each emits two compares after split-paths). a14 is `<<><<`.

### Item 1: what puts a name at the increment's position (from dumps unless marked)

- Names come in tuples of (PHI, increment, init, bound), and the bound comes straight after its loop's candidate, not where iw14pop.py lists it (iw14pop groups it under the outer candidate that the bound's expression later uses). Real order: src `102 67 68 282 | 369 58 226 389 | 277 240 314 313 241 | 315 391 279 319 | 317 318 321 320 322 74 | 75 76 84 108 ...`, a14 `51 121 233 130 | 352 120 162 160 | 159 372 301 300 302 | 214 158 215 212 | 373 263 217 304 303 219 | 305 218 216 309 ...`. Inferred from the tuples holding up across a dozen states; nothing reads the pops directly.
- **src versus src without the dead test (build/iw/a15/nd.c, 2 lines, the same compare):** add 2 to nd's numbers and the two stacks are the same layer. nd has `... 389 240 314 313 241 315 391 279 316 319 318 ...` with the big tuple at `279 316 319 318` (316 < 318, wrong). src has 58, 226 and 277 above that layer, so the big tuple lands on `315 391 279 319` (391 > 319, right). **So 391 isn't special. The dead test works by adding names above the ccp2 layer, which moves the window over the same list.**
- Most of the names in play last appear in oaccdevlow: they go at ccp2, from arms dead for that copy's constants. Names freed later sit above them.
- **Position doesn't matter, count does.** gen_iw220: K names freed by a dead arm, at 3 positions: same lines per K at every position. gen_iw221, lines by K on a14: 0:2 1:8 2:8 3:30 4:28 5:28 6:8 7:4 8:4 ... 16:4, never 0 up to 80. Bodies aren't neutral, though: src's `off += 0x4000` on nd gives 0 and `off++` gives 6, so a body can change more than the count (I read that as FRE matching it to the log's `off + 0x4000`; inferred, not traced).
- **K = 7, 8, 16 fix the big copy's compare and only C1 is wrong (`<>>><`).** C1's bound is `_39`, a low name from writeFsTable's own arm, and C1's increment is around 129. Every K >= 1 on a14 gets C1 wrong. writeFsTable's own names are lower than the inlined copies', so an arm there can't supply a bound above it (the reason is inference; the `>` at every K is measured). gen_iw223: 3000 random arms on a14, floor 2; 3000 on a14 with `setBeU16(blk, ...)`, floor 4. Samples, but the arms vary length, nesting, target and count.
- Why a low name freed at VRP1 sits above an ifcvt name, under pcom's, isn't explained. Stretches of the stack read as ascending runs, and I'd guess some passes release in version order, but that's inference. The stack isn't one LIFO by pass.
- On paper, using a14's tuples: 2 or 3 more names above the layer break the big outer compare (212 v 304, 215 v 217). 3 fewer (or 3 more taken live by earlier passes, off the top of the layer) makes the compares listed there right. Probe: `M` partially redundant `off >> n` in iw15grid.py (each one a PRE PHI, the mechanism of a14's `off >> 14`). M = 0..6 x K = 0..30: no `<>><<` on a14. M's own names disturb everything else, so this doesn't refute the paper result, but it isn't a way to reach it.

### Item 2: pre new 18 v 19

**The extra PRE name is the tail spelling.** a14's first insertion is `prephitmp_278 = PHI <blk_8, blk_8, blk_14>` for `off >> 14` (`iw15pre.py`); src writes `setBeU16(blk, ...)` and has no such PHI. After it the two insert parallel lists (read for writeFsTable's first iteration). So I read the different store and load pair as a consequence of one extra pop plus the different layer above it, not a separate lever (inferred; not tested in isolation).

### Item 3: what `&&` partial costs in imgAdd

- **The pad and tail order is a naming race.** ifcombine merges the two tests into `_1 & _N` in both a14 and foraa (gen_iw218 `for+aa`). In the optimized dump the order comes from the two compare names PRE makes on the path to the memset: a14 `_315 = pad == 1; _316 = len != 0; _315 & _316`, foraa `_317 = len != 0; _320 = pad == 1; _317 & _320`. PRE handles `&` before `tail != 0` in a14 (ids 0061 v 0182) and after it in foraa (0180 v 0179).
- The id order looks like version order (inferred): a14's `&` result is `_49`, foraa's is `_237`, with tail's compare at 233 and 235. 49 and 237 are both among the names dce2 frees: `i_49` versus `iftmp.16_237 = PHI <1(18)>`, a single-arg PHI left after VRP1's threading of the `&&`.
- A dead arm or an unused-after-VRP local in imgAdd doesn't move this (gen_iw224, build/iw/a15/p1.py): imgAdd stays 100+ across K. Note gen_iw224's condition is `(x & 0xff) > 0xff`, which does survive once the body assigns off.
- **`small` removes almost all of it. gen_iw225: foraa with `small = type != 0 && type != '0'; partial = small && len < 0x4000;` is 12 lines, down from 122**: imgAdd 6 (`and edi,0x1ffff` and `and eax,..` scheduled differently), imgAddFile 4 (a cmp and ja order), writeFsTable 2 (a different compare, line 359). `a && b && c`, ternary and `if` forms stay 122+; `if (&&)` with no variable 46+.
- gen_iw226, 227: the block offset's place on this family. In the arm or at the use: 2, the known compare. At the top of the loop (`for`, `forv`, `forw`, `forx`, `ms`): 12. In the big arm or type test (`big`, `bt`): 54, or 10 with `setBeU16(blk, ...)`. Above the page loop: 227+.
- **Without the block offset local, `small` is byte-identical to a14 with the same SSA numbers.** That's drafts/image_write_a15.c. It replaces `(len < 0x4000) & (type != 0) & (type != '0')` with something a person would write.

### Item 4: small landings

- **drafts/image_write_a15_dead.c = a14 with src's dead test and `setBeU16(blk, ...)`, would be 5 tricks (lnp2 gone): 4 lines, signature `<>>><`.** Same SSA numbers as attempt 13's n8_bf, now understood: everything is right except C1 (`ivtmp.405_120 != _106`, two lines after split-paths). The bound is `pages_106`, the first copy's `len / 512`. It needs a name above 120.
- iw14rejudge over gen_iw205-219 on it (cap 300, build/iw/a15/rj_dt1a.log): floor 4, except gen_iw212's `nodead+tl`, which just goes back to the 2-line family.
- gen_iw222: a14 x one dead test (3 positions, 7 conditions, 18 bodies, tail spelling; 756): floor 2.
- Dropping the dead test or lnp2 from src alone: gen_iw212's results stand, nothing new.

### Not candidates, but worth knowing

iw15grid on nd (src family, dead test swapped for a K arm): `<>><<` at K = 12, 19, 23, 24, with 46 lines; I read K = 12's and they're a stack-slot rotation ([esp+0x1c], 0x20, 0x24 become 0x20, 0x24, 0x10). a14 with `setBeU16(blk, ...)` has 48 lines, which attempt 14 also read as slots. It keeps lnp2 and a long dead arm, so it isn't a reduction. It shows the signature and the slots are separate targets, and that the src family keeps C1 right under K where the bitfield family doesn't: its C1 increment is 79, a14's about 129.

### Attempt 15 result: NO MATCH

No byte-identical state under 6. `iwlib.py src/image_write.c -np`: IDENTICAL; build/iw/reference.o is identical to build/obj/image_write.o. Closest: drafts/image_write_a15.c, would be 4 tricks (pin_t, pin_hdr, optimize, xmalloc), 2 lines. With a dead test and 5 tricks: drafts/image_write_a15_dead.c, 4 lines. optimize, pin_t and pin_hdr weren't attacked because the compare didn't yield.

Next:
1. C1 in image_write_a15_dead.c. It's the one thing left in a 5-trick state, and the target is concrete: C1's bound above C1's increment (`iw15sig.py <file>`, then `iw15dump.py` and `iw15src.py` for what each is). `pages_106` is the first copy's `len / 512` in the big arm. Move that name, or lower the increment (a `.MEM` taken at vect).
2. The 12-line `small` state: three small independent diffs. Its writeFsTable compare is a different one from a14's, so read it with the signature first.
3. Rerun older generators keyed on the signature, not total lines, logging any state with the big copy's compare right. A state fixing it at a cost elsewhere has been invisible to every sweep so far. It needs two compiles per state.
4. Don't retry: dead arms in writeFsTable on a14 (gen_iw221, 223), K arms in imgAdd (gen_iw224), M probes (iw15grid), a second dead test on the dead draft (gen_iw206 in the rejudge).

Reproduce: `python tools/wip/dehint/iw15dump.py a15 tools/wip/dehint/drafts/image_write_a15.c`, then `python tools/wip/dehint/iw15stack.py build/iw/a15/d_a15 writeFsTable pre ivopts` and `python tools/wip/dehint/iw15src.py build/iw/a15/d_a15`. K table: `python tools/wip/dehint/iwsweep.py tools/wip/dehint/gen_iw221.py -n 81`. gen_iw225 needs foraa, which is a14 with gen_iw218's `for+aa`: `python tools/wip/dehint/iwsweep.py tools/wip/dehint/gen_iw218.py -n 1 -k for+aa` writes build/iw/gen_iw218_best.c; point `IWB` at it. gen_iw220, 221, 223, 224 and iw15grid are probes, never candidates.

Lesson: **sweep by counting first.** A dead arm with K throwaway statements showed in seconds that position doesn't matter and the count does, which no sweep of plausible spellings could show. And score by compare signature as well as lines: a state with the target compare right can look worse than the one you have.

## Attempt 16

Written as I go. New tools in tools/wip/dehint: `iw16rej.py <base.c> <log> [cap] [first] [last] [threads]` (iw14rejudge with a signature per state, one compile each), `iw16sweep.py <gen>` (one generator crossed, histogram by full signature), gen_iw228 onward. Scratch in build/iw/a16.

### The signature was incomplete

iw15sig reads five compares in the ivopts dump, but split-paths then copies each page loop's test, so the object has eight. **The 12-line `small` state has iw15sig's target `<>><<` and still a wrong compare**: the second copy, bb16 `ivtmp.429_114 != _213`, where src has `_319 != ivtmp.430_362`. Full signature, read from the optimized dump in order (`<` when the ivtmp comes first): **target `<>>><<<<`**. iw16rej and iw16sweep report both. a15 is `<<>><<<<`, a15_dead `<>>>>><<` (C1, both copies), the 12-line state `<><><<<<`.
The copy's name is a separate race from ivopts': split-paths' first name is whatever ivopts released last, `b_362` in src, `_114 = _89 * 32` in the 12-line state, `_347 = _89 * 32` in a15 (from the dumps; I didn't work out the release order).

### Item 2: rerunning old generators by signature found it

`iw16rej.py` over gen_iw1-227 (cap 100 per generator, build/iw/a16/rs_a15.log, rs_dead.log; the a15 run finished; I stopped the dead run around gen 95 once c4 had turned up) printed states that had always been hidden behind a worse line count:

| State | Lines | Full signature | What's wrong |
|---|---|---|---|
| a15_dead + gen_iw214 `c4` (`left` as the free count, `pages` rounded in place, build/iw/a16/c4d.c) | 4: imgAdd 2, writeFsTable 2 | `<><><<<<` | C1 right. bb16 and imgAdd's outer compare |
| c4d + gen_iw207 `g` (`blk = start + b` in the page loop, build/iw/a16/c4g.c) | 2: imgAdd | `<>>><<<<` | writeFsTable clean. imgAdd's `cmp [esp+0x4c],eax` |
| c4d + gen_iw207 `a+e`, `c+e` | 2: writeFsTable | `<><>...` | imgAdd clean |

gen_iw207's `g` had been run before, but scored on a base without `c4`. Attempt 13's sweeps of 214 and 207 were on the no-dead-test family, and attempt 15's rejudge on the dead draft was scored by total lines, where each alone showed nothing below 4.

imgAdd's compare on c4g (from dumps): the bound is `_322 = start + blocks`, where a15_dead has `_46` and src `_18`. `c4` has no `left = (int)pages`, so PRE has 121 new names against 126 and the pops land elsewhere.

### The match

gen_iw234 on c4g (types and forms of `pages`, `left`, s[9]): **`(left - (int)pages) >> 2` makes imgAdd clean** and moves writeFsTable to `<<>><<<<`, one compare. gen_iw235 crossed that with left's spellings, blk's position and the tail spelling. **960 states, 48 IDENTICAL.** All of them have the signed `s[9]` form (e1 or e2), `g` and `setBeU16(off >> 14, ...)`.

**drafts/image_write_a16.c: byte-identical at plain -O3, 5 tricks** (dead test, pin_t, pin_hdr, optimize, xmalloc). lnp2 is gone. Against src:

- `blk = start + b;` in the page loop, above memset, not per block.
- `small = type != 0 && type != '0'; partial = small && len < 0x4000;`, tested as `if (partial > 0) { npages... } else npages = 32;`.
- `s[12]` through `struct spt`'s 6-bit `type` field.
- Big arm: `pages = len / 512; if (len % 512) pages++; left = (off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256; if (pages & 3) pages = (pages + 4) & ~3; s[9] = (left - (int)pages) >> 2;`. Small arm: its own ternary `pages`.
- `setBeU16(off >> 14, ...)` for the FS block.

Measured on it, one change at a time: no dead test 8 lines (writeFsTable), blk per block 2, no `(int)` 6, `setBeU16(blk, ...)` 2, `if (partial)` 244, no pin_t 10 (imgAdd), no pin_hdr 243, no optimize 4 (writeFsTable), plain malloc 180. `uint8_t *buf, *p` or `*p, *buf`: same bytes, so the draft has src's.

gen_iw236 (partial's forms, `if (partial)`, dead test on/off, pages spellings, tail, 96): IDENTICAL only for `''`, `si`, `sm`, `sm+si`. Unifying pages (`bt`) is 4 (constprop.1 2, writeFsTable 2). `small` gets rid of the `&` form at no cost, so the draft has it.

### Borderline shapes in the draft, for review

- `(int)pages` in `(left - (int)pages) >> 2`. Plausible (`left` is int, `pages` unsigned), but the only reason it's there is that it changes imgAdd's compare. I didn't work out why from dumps; it's a measured effect.
- `pages` spelled two ways in the two arms. Unifying costs 4.
- `if (partial > 0)` for a boolean: `if (partial)` costs 244, from the predictor (attempt 13's reading).
- `off >> 14` where `blk` is in scope in writeFsTable, and Linux reads as `blk` (attempt 14). `blk` costs 2.
- `blk` and the `BLK` macro both used in imgAdd. gen_iw207 `b`, `d` (all `blk`) are 900+; `a`, `c` are the same bytes.
- `blk` in the page loop: fine as code, but its reason here is names.

### Attempt 16 result: MATCH (5 tricks)

Verification: `python tools/wip/dehint/iwlib.py tools/wip/dehint/drafts/image_write_a16.c -np` IDENTICAL; compiled by hand with `gcc -c -O3 -Isrc -x c -` (`#line 1 "image_write.c"` first, build.sh's flags for this object) and `cmp` against build/obj/image_write.o: identical, SHA256 cf10057d...2b0a. build/iw/reference.o equals build/obj/image_write.o. The full `sh build.sh` wasn't run, since src is the parent's to change.

Next, if this lands:
1. Drop the dead test: 8 lines on the draft, signature `<<<<<<<<`. a15's other states are 2 lines with `<<>><<<<`, so try gen_iw232-style name counts in natural code instead of a dead arm, keyed on the full signature.
2. Rerun gen_iw1-236 with iw16rej on the draft and on the draft minus each trick. This method found the match after 15 attempts of ranking by lines, and it wasn't used on `optimize` (4 lines off), which is now the smallest gap.
3. Rerun with a full signature for any other function that's a compare off: imgAdd's outer compare and constprop.1 have them too.

Don't retry: `bo` local placements for this family (gen_iw229, 230; imgAddFile's `_45 > _53` version is what they cost); dead test bodies on c4d (gen_iw232: bb16 stays wrong without `g`).

Reproduce: `python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw235.py -t 4`, about 8 minutes. `IWB=<base>` overrides the base. Rejudge: `python tools/wip/dehint/iw16rej.py <base> <log> 100 1 236 3`.

Lessons: **test the measure itself.** The five-compare signature said the 12-line state was right when it wasn't, because split-paths copies four of the tests later. And **two separate wins can be hidden by one local cost**: `c4` looked like no gain and `g` showed nothing, on their own. Scoring by what each state gets right, not by total lines, is what showed them. Heredoc Python mangles `\n` as CLAUDE.md warns; a filename built from labels collides on Windows (L3re1, L3Re1), which briefly gave me a different state from the label I thought I had.

Landed after attempt 16: drafts/image_write_a16.c is now src/image_write.c (5 tricks, full build matches), so the draft is removed. `iw16rej.py` bases and gen_iw236's "m0" are that source.

## Attempt 17

Written as I go. New generators gen_iw237-244 in tools/wip/dehint. Scratch in build/iw/a17. Base names below: na = src minus optimize; nd = src minus dead test; ifb = na with `if (xb.bigBlock) imgAdd(...); else imgAdd(...);`.

### What optimize does (from dumps)

scev-cprop does no value replacement in writeFsTable. Diffing the copyprop3 dumps of src and na shows only four extra blocks with one single-argument `.MEM` PHI each: the exits of both FS loops and of the two unswitched page loops of the second copy. Those are the loops whose exit block has another predecessor (`blocks != 0` guard, or the join of the unswitched pair). So the pass splits those exits and takes 4 names (.MEM_110, 223, 152, 151 on na). Src gets the same PHIs later, at vect, with other names (.MEM_78, 124, ...); that part reads from iw15src.py. That I'm reading "split the exit" as the pass's behaviour is inferred: the GCC source wasn't read.

Compare with iw15src.py: ivopts' pops on src and na are the same list from pop 6 on, except the pops that hold these PHIs. C1 is `pop 2 != pop 12`, the second copy's FS exit PHI against the first copy's: src 124 < 131, na 223 > 151. C2 is `pop 5 != 163`: src 122, na 175.

So C1 needs FS2's PHI below FS1's. sccp takes names off a descending run (110, then 223, 152, 151, 142, 135, ...), visiting FS2 before FS1, so inside the run FS2 is always the higher. K arms and M PRE PHIs on na (gen_iw237, 240: 84 + 62 states) never flip position 6 of the signature. It does flip on ifb, where the dumps show the exits taking names in another order (FS1 223, FS2 110). That the sign of the call test sets the visit order is inferred.

### Tries that led to the match

`iw16rej.py` on na (100 per generator, gen 1-236, finished, build/iw/a17/rs_na.log): nothing at 0. Best 2, on gen_iw223 only: a second dead arm, so no reduction. Rejudge runs on the bases below were stopped as soon as a better base turned up, so they are partial: ifb, n12, n8, n8d, s4a, s4t, s2c, bp2. None of them is a full search.

Each step below was found by crossing or rejudging, and scoring by signature. Lines are totals at plain -O3:

| Base | Change from the row above | Lines | Left |
|---|---|---|---|
| na | src minus optimize | 4 | writeFsTable C1, C2 |
| ifb | `if (xb.bigBlock) imgAdd(...); else imgAdd(...);`, Linux's form (gen_iw202's call forms) | 14 | C1, C2 right, others wrong, `cmp blocks` 1 v 2 |
| n12g | no dead test, goto form back, `left = left - pages; s[9] = left >> 2;` (gen_iw242) | 10 | constprop.1, writeFsTable |
| n8 | unsigned left, ternary big `pages`, `(int)(left - pages) >> 2` (gen_iw243 on n12g) | 8 | writeFsTable only; no dead test, no optimize |
| s4a | int left, if-form pages, `(left - pages) >> 2`, optimize on (gen_iw245) | 4 | imgAdd, writeFsTable position 2 |
| s4t | a `bo` local and ternary pages (gen_iw230, 246) | 4 | writeFsTable clean; imgAdd, constprop.1 |
| s2c | `t = type - '1'` after `p = 0` (gen_iw184 `aft`, found by the rejudge) | 2 | constprop.1 |
| bp2 | if-form big pages, bo inside the type test (gen_iw248 `bi+pi`) | 2 | writeFsTable position 2 |
| match | `len = i * 0x400` as a local used by the log and both calls, `setBeU16(blk, ...)` (gen_iw249 `e2+t2`) | 0 | |

`bo` then turned out unnecessary (gen_iw250 `nobo`: IDENTICAL), so the draft has src's `left`.

A 5-trick side result, superseded: bp2 + `setBeU16(blk, ...)` + the dead test (no `len`) is also IDENTICAL.

### The match

**drafts/image_write_a17.c: byte-identical at plain -O3, 4 tricks: pin_t, pin_hdr, optimize, xmalloc. The dead test is gone.** Against src:

- `t = type - '1';` right after `p = 0;`, next to its only test.
- `s[9] = (left - pages) >> 2;`, without src's `(int)`.
- writeFsTable has `uint32_t len; len = i * 0x400;`, used for the log's end and both calls. The dead test and its comment are gone.
- `setBeU16(blk, ...)`, Linux's form (attempt 14 read it there), for `off >> 14`.
- The comment on `blk = start + b` reworded with the measured number; the old claim (2 lines) no longer holds here.

Why `len` replaces the dead test isn't explained: it's a measured effect on names, I didn't trace it.

Measured on the draft, one change at a time (gen_iw250): no optimize 2 (writeFsTable, `<>>><><<`), `(int)` back 2, no `len` local 8, no pin_t 10, t back at the top 10 (imgAdd), `off >> 14` 29, blk per block 37, if/else calls 41, `if (partial)` 158, plain malloc 180, no pin_hdr 243 (finalizeImage). `len = 0x4000` loses the clones (40006): `i * 0x400` being unknown at inlining still matters.

pin_t, re-measured on the moved base: without it 10 lines, the same two byte slots swapped. gen_iw201, 236 and 239 (types, range tests `type >= '1' && type <= '?'`, t's place, partial's forms) don't move it; the range tests are also 10, or 106 with a wider compare. IRA's MEM costs for r153 (partial) and r172 (t) tie at 1346, and t's test is split in two blocks, so I read it as the old rounding loss; LRA's own totals weren't printed, so that reading is inferred. A tie would also need t's regno below partial's (153 v 172 here).

GCC source wasn't needed or fetched this attempt. Item 2's natural replacement for the dead test was found by accident of crossing, not reasoned from the K count.

### Borderline shapes in the draft, for review

- `len` local: fully ordinary code, but its only reason here is names (8 lines without it).
- `t` next to its test: ordinary; 10 lines if it moves back, with the pin still on.
- `goto small` / `goto done` is unchanged from src. if/else, which Linux reads as, costs 41 here.
- Carried over from src: `if (partial > 0)` on a boolean (158), `pages` spelled two ways in the arms, `blk` and the `BLK` macro both used, `blk` set in the page loop (37).

### Attempt 17 result: MATCH (4 tricks)

Verification: `python tools/wip/dehint/iwlib.py tools/wip/dehint/drafts/image_write_a17.c -np`: IDENTICAL. Compiled by hand with build.sh's flags for this object (`gcc -c -O3 -Isrc -x c -`, `#line 1 "image_write.c"` first): `cmp` identical to build/iw/reference.o and build/obj/image_write.o, SHA256 cf10057d...2b0a. Full `sh build.sh` not run, since src is the parent's to change.

Next, if this lands:
1. optimize: 2 lines on the draft, signature `<>>><><<`, one compare (C1). The smallest gap. Read the sccp section above: FS2's PHI must get a name below FS1's. Rerun iw16rej on the draft minus the attribute and gen_iw245-style crosses.
2. Don't take any line count in earlier notes as a measure of a shape: `(int)`, `off >> 14`, `bo`, `tb` each changed sign across this attempt's bases. Rejudge rather than reuse.
3. pin_t and pin_hdr haven't moved. xmalloc not attacked.

Reproduce: gen_iw250 on the draft. Bases n8, s4a, s4t, s2c, bp2 are in build/iw/a17 (not committed); each is the draft's text with the edits in the table, and generators 243-249 name their base in the header, so set `IWB`. Rejudge: `python tools/wip/dehint/iw16rej.py <base> <log> 150 100 250 3`.

Lessons: **cross what looks like it costs something.** Several steps here were worse on some axis than the state they came from (n8 is 8 lines against na's 4). Removing a trick first, then searching around the broken state, reached places attempt 16's base couldn't. And **a rejudge on each new base pays**: `t`'s place (gen_iw184, attempt 11) and `bo` (gen_iw229, attempt 16) were old options that only worked here.

Landed after attempt 17: drafts/image_write_a17.c is now src/image_write.c (4 tricks, full build matches), so the draft is removed.
