# image_read de-tricking

Goal: `build/ir/reference.o` (copy of a matching build/obj/image_read.o) byte-identical
from plain `-O3`, with fewer hints.  31 tricks at the start of attempt 1.

## Attempt 1

Tools (tools/wip/dehint/): `irlib.py <file.c> [-v [fn]]` (IDENTICAL or per-function lines),
`irtricks.py singles|pairs|greedy|show` (named edits of each trick, IRBASE=<file> for the base),
`irsweep.py` (added later, see below).

Cost of removing each trick alone (lines, total incl. functions moved by knock-on effects):

| trick | lines | where |
|---|---|---|
| if0_smc | 0 | `return;` then the labels instead of `if (0) {` : IDENTICAL |
| pin_cb | 4 | parseDump (xor ebp,ebp; mov [esp+2c],ebp and an `xchg ax,ax`) |
| pin_lo2 | 4 | detectController: `movzx edx` vs `eax` |
| bar_hdr | 6 | checkHeader: size test first |
| exp_ok1 | 7 | findAnchor: alignment only |
| pin_found | 7 | detectController: head-merged xor eax |
| lit_anchor | 10 | findAnchor, .rdata order |
| lit_smc | 16 | getImageSmc, .rdata order |
| exp_nok1 | 20 | findAnchor (7 together with exp_ok1) |
| unr_remap | 21 | remapBadBlocks |
| pin_t | 23 | checkBlock |
| unr_p2 | 26 | parseDump |
| opt_smc | 37 | getImageSmc |
| unr_smc | 46+ | getImageSmc |
| bar_p | 45+ | parseDump |
| pin_lo | 67 | detectController |
| pin_v | 70 | fsGetFile |
| unr_p1 | 70+ | parseDump |
| opt_mmc | 74 | copyMmcImage 14, parseDump 6, loadDump 54 |
| exp_ok0 | 93 | findAnchor |
| lab_bhot | 93 | getImageSmc |
| lab_shot / pin_addr / lab_vhot / exp_smc | 119-158 | getImageSmc |
| exp_scan | 137+ | scanMobiles |
| bar_anchor | 67+ | findAnchor |
| lab_mmc | 296 | loadDump |
| pin_b2 / lab_rem | 308 / 382 | parseDump |
| noinline | 1083 | imgGetSecurityFiles, loadDump |

Everything of a function removed at once: findAnchor 42, getImageSmc 156, detectController 96,
parseDump 358.  Useful pairs: exp_nok1+exp_ok1 7, pin_found+pin_lo2 11, bar_p+opt_mmc parseDump 51
with loadDump only 2 (so loadDump's 54-56 lines is one effect shared by parseDump/copyMmcImage).

### Findings as they came

- **if0_smc: IDENTICAL.** `return;` + the labelled blocks at the end replaces `if (0) {`.
- **bar_hdr (checkHeader's asm): IDENTICAL.** ifcombine only merges two tests when the inner block
  holds nothing but the condition (cf is FRE'd from the earlier `size < cf` test).  So a load between
  the tests, which the sink pass moves past the test later, does the asm's job with no code:
  `count = SWAP16(hdr.sysUpdateCount);` (uint32_t; a uint16_t count gives 116 lines) between
  `goto badSysUpdate` and the cf test.  gen_ir8.py.  Other shapes, gen_ir7.py: `||` 6 lines (ifcombine),
  reversed `||` 220 (not combined, wrong order), separate blocks 300+.
- findAnchor (5 tricks, 42 all gone), gen_ir1..6:
  - .rdata order (e8 valid, e8 invalid, ec valid, ec selected, ec invalid, e8 selected) is met without
    lit_anchor by `if (ok1) { valid; if (!ok0 || v0 < v1) { sel1; return 1; } } else invalid; if (ok0) sel0`
    ("or" in gen_ir1.py, 58 lines).  The reference's threading isn't: dom2 threads the I block's ok0 test
    (I = `ec invalid; if (ok0)`), the reference keeps it.  What keeps it in HEAD is bar_anchor: an asm
    stops thread_through_normal_block in I.  In dom3's input J (the sha call) is split only if nothing
    threaded it in dom2; each incoming edge keeps one joiner thread (first registered wins).
  - Natural idea not yet found: I block must end without a cond (K separate) until dom3, or ok0's
    knowledge must not reach it.
  - With the two asms kept, all 3 expects go at 14 lines: `if (ok0) { if (ok1 && v0 < v1) { sel1 } sel0 } if (ok1) sel1`
    (gen_ir2/3).  Left: v1/ok0 swap (ebx/edi).  IRA pops by spill cost: ref v0 > ok0 > v1 (v0 10625, ok0 10000,
    v1 7797), draft ok0 10000 > v1 8687 > v0 7915.  v0 must beat ok0's constant 10000, which needs P(ok0) of the
    FIRST test above 50% (both arms hold a call: call heuristics 71/29 cancel).  `int ok0; if (ok0 > 0)` on
    the first test (opcode-positive predictor) gets it to 4 lines, only `jle` where the ref has `je` (gen_ir4).
    `uint32_t ok0 > 0` folds to != 0 in the front end: no effect.  Single exit (`ret`, gen_ir5) no effect.
    One expect alone: on `ok1` in the nested && it is the same 14, on the second ok0 20, gen_ir6.
- **unr_remap: IDENTICAL** with `int i` in both remapBadBlocks and findFreeRemap (gen_ir17): VRP derives numBad != 0 from a signed IV.
  One of the two alone leaves 4 lines.  Draft at this point: 28 tricks (if0_smc, bar_hdr, unr_remap gone).
- parseDump (gen_ir11-16): a signed `for (blk = 0; blk < blocks; blk++)` (VRP knows blocks >= 0 from uint / {32,256}, so the guard is
  still `je`) removes the need for u1, u2, bar_p, pin_cb, pin_b2 **at once** (all five free of one another: 52-48 loose lines left
  with lab_rem kept, IRLOOSE=1 irlib).  What's left then: ch gives blk a late SSA name (blk_170 vs dst_30), so `blk != dst`
  canonicalises to `dst != blk`: cmp operands swapped in 3 places, plus `xor ebp,ebp`, plus one block's place.  HEAD's `blk = (int)n`
  has its own low name, which is what the reference's compares want (dst_2 < blk < dst_30).  do-while avoids ch but layout breaks
  (410 lines, `blk == 0` handled as separate).  `(int)n < blocks` on an unsigned counter: same as the signed loop (FRE'd into the header).
  Dropping `dest < numBlocks` (always true) from addRemapP with the unsigned loop gets the compares right and needs no unreachable, but its
  callee-side prediction lowers the log block's frequency: without it blk is hoisted out of the inner loop by IRA (41 loose lines).
  A later attempt should start from this: signed loop plus something for the SSA order, or a test with the same prediction.

### State at the end of attempt 1

`drafts/image_read_attempt1.c` is IDENTICAL with 28 tricks: if0_smc, bar_hdr, unr_remap gone.
Borderline: checkHeader's `count` read between the tests (live, and it reads naturally; it's there for ifcombine).
`if (0)` is now `return;` + labelled blocks at the end of getImageSmc.

Tried without a result, in the order to read them (generators under tools/wip/dehint/):
- loadFlashFile's noinline (gen_ir18-20): size 45, growth 39, limit 40.  A separate mask statement leaves `_27 & 65535` in gimple
  at IPA time (+1 size: not inlined, combine drops it later), but the extra pseudo changes RA: 88 lines (fsOffset spilled, block in edi).
  `(uint16_t)SWAP16(...)` stays out too and leaves only 18 lines, but bswap turns it into `rol bx,8`.  Types of params/return/locals: no effect.
  Next: another +1 size statement that doesn't touch the swap.
- fsGetFile's pin_v (gen_ir23): pure esi/edi swap of v and name, plus stack slots; shape doesn't matter (70 for all).  IRA tie.
- detectController (gen_ir9, 10): pin_lo2 gives 4 lines for every spelling of the second test; pin_found 7 for every placement.  pin_lo: the sum
  takes hi's register only because lo is live past it; without it i moves to ecx (copy after the call), 52 lines.
- getImageSmc, all ten hints gone, written like getImageKv (gen_ir21, 22): 90-98 loose lines, 138-146 strict; structure is already right, block order
  and arm polarity differ.  Ref: the bad-addr arm falls through (P(bad) > 50), `cmp ebx,eax; jb`.  Best `ii.zlast.ne.ge`.  Next attempt: model profile_estimate on it.
  Note ebx/edi copies of addr in the ref and `edi = 0x1000` are RA from the hints or real; unknown.
- checkBlock's pin_t: reassoc's range test merges `t <= 0x29 && m` into `(m - 1) <= 0x28`; reassoc2 runs after sink, so the
  checkHeader trick won't hold.  Not swept.

What to try first next: (1) parseDump's signed loop (5 tricks at once) and the SSA order after ch; (2) findAnchor at 4 lines with `int ok0; ok0 > 0`
if P(ok0) above 50 can come from elsewhere, or the 'or' shape; (3) `sink moves it` as a natural replacement for other empty asms.
Don't retry: declaration order in findAnchor (no effect), `uint32_t > 0` spellings (fold early), single-exit findAnchor.

## Attempt 2

Compiles take 0.5 s, so whole-object sweeps of hundreds are cheap.  New tools: irasm.py (a function's disassembly), irinl.py (grep ipa-inline dump),
irfreq.py (per-pass block frequencies from `-fdump-tree-all-blocks-details`).  irdump takes the name without the underscore (`parseDump`).
loadDump's 54-56 lines in earlier cost tables are only call offsets: parseDump's size moved.  Ignore it.

parseDump (gen_ir24-28, 33):
- ch2 (107) runs AFTER vrp1 (96).  It renames every header PHI's body uses to a new, highest SSA name, so with `for (blk...)` signed, blk is always above dst and above `blocks - 32`:
  compares print (dst, blk) and (tmp, blk).  fold_stmt canonicalises by version (forwprop4 is after ch2), source order is irrelevant.  Only a blk NOT defined by a header PHI can be low: a body statement or a do-while.
- do-while (gen_ir26, 27): compares come out right, but `blk == 0` loses `guess loop iv compare` 0% (for: bases 0 and 0 coherent; do-while's exit IV `++blk` has base 1), goes to 50%,
  spareLbaOk then inlines (freq 3358 instead of 0).  That's the "410 lines".  `while (blk++ < blocks - 1)` (base 0) didn't bring it back either (566).
- `for (n = 1; n <= blocks; n++) { blk = n - 1;` (gen_ir28): compares right, but VRP doesn't fold blk < blocks (site 3 keeps `cmp edi,esi`), exit test differs: 238.
- `-4` arm rejoining before `dst != blk` (gen_ir25): no help, 177-219.
- Unsigned n kept (gen_ir33): passing n instead of blk changes nothing with int params (FRE back to blk); uint32_t block param moves one `cmp` at site 3 the wrong way.
  pin_cb + pin_b2 together are only 12 loose lines (25 strict): the `xor ebp,ebp` and esi loaded before the log call instead of after it.  b2 is a pseudo defined in the arm, before the log;
  no natural fresh SSA name exists in the arm with an unsigned n, since (unsigned)blk folds to n.
- `xor ebp,ebp; mov [esp+2c],ebp` (and detectController's `xor eax,eax; mov [esp+1c],eax`) is IRA region splitting: outer allocno gets a hard reg, the loop's is memory, the border move stores it.
  It needs the outer allocno's accumulated cost a bit higher.

findAnchor (gen_ir29-32):
- exp_ok1 + exp_nok1 leave only bb10's alignment (`nop`): dom2/dom3's threads clip the edge to bb10 to 0%, freq 0, so compute_alignments skips it.  Reference has 16.9%.  84 spellings of the final tests and the ok1 test (&&, nested, `> 0`, polarity, int ok1): always 7.
- Final CFG spelled out with gotos (gen_ir30): dom3 threads ok0 in the shared invalid block: 85+.  Not worth more.
- A `goto` in the first test's invalid arm gives no PRED_GOTO in profile_estimate for C here (gen_ir32): no effect on P(ok0).

getImageSmc: **lit_smc: IDENTICAL** with the zero arm written inline at the top (`if (!addr) { log; addr = 0x1000; } else { vhot: }`, gen_ir34 'a') instead of a labelled block at the end: its string is then expanded first. 27 tricks.

detectController: **pin_lo2: IDENTICAL** by moving pin_lo's asm into the taken arm, `if (lo2 + ... == i) { __asm__("" : : "a"(lo));` (gen_ir40): lo stays live over the second test, so one asm does both jobs. 26 tricks.
fsGetFile pin_v (gen_ir37): IRA pops off (r106) before the return value (r149) in the top region: 96 shapes of the copy part (types, order, pointer q, return v): always 70.
checkBlock pin_t (gen_ir39): 18 &&/nested/type spellings all merge to `(m - 1) <= 0x28`, 23 (reassoc walks through the casts; both reassoc passes).

parseDump, hints doing several jobs (gen_ir41-44, unsigned loop):
- Site 2's `if (blk < blocks)` guard is unneeded next to its unreachable: IDENTICAL without it (a dead test gone, not a counted trick; in the draft).
- **Near miss, -2 tricks at 2 lines (strict and loose):** one unreachable just before `if (blk == 0)`, the guard kept at site 2, no barrier, no other unreachable (gen_ir42 `z.and+d`).  Only `cmp [esp+2c],ebp` for `cmp ebp,[esp+2c]` in the last `dst != blk`.
  Mechanism: gimple is otherwise the same.  dom2 threads the -4 arm's edge past the unreachable's test, so the block after it gets a second PHI, dst_185 = PHI <dst_1, blk_24>, and `blk_24 != dst_185` prints blk first (HEAD: the barrier stops that thread, `dst_1 != blk_24`).
  Tried: the test's spelling (&&, nested, reversed, continue, goto), unreachable positions (a4, else arm top/end, before the copy loop: 26-146), decl order: no effect.
  `dst != n` (gen_ir44, n's late name puts dst first) fixes that compare at 6 lines, but `(unsigned)dst` is then FRE'd into site 3, so `cmp ebp,[badBlocks]` swaps there, and the summary loop's `cmp [numBad],ebx` flips (numbering).
  Next: a way to compare with dst first and no shared conversion, or stop dom2's thread on that edge without asm (block the guard's knowledge from reaching the join), e.g. the guard's true path ending differently.  SSA versions are recycled from the free list, so dst_185 isn't necessarily high: a lower free name at dom2 would also do it.
- pin_b2's asm carrying extra uses of blk doesn't replace pin_cb (4 lines either way, c1/c3).
- getImageSmc (gen_ir35, 36, 45): attribute options: only no-tree-tail-merge left 12 (5 loose), none 32 (6 loose): what's left is ce1 hoisting addr = 0x1000 and addr's copy above the size test.  Polarity of the last test doesn't help hints go; addr pin position doesn't either.

### State at the end of attempt 2

`drafts/image_read_attempt2.c` is IDENTICAL with 26 tricks: lit_smc and pin_lo2 gone, and site 2's dead guard.
Don't retry: fsGetFile's copy-part shapes; checkBlock's &&/nested/type spellings; findAnchor's final-test spellings with exp_ok0 kept (always 7) and spelled-out CFG; do-while or `n = 1` for parseDump without a fix for iv-compare's 0%; goto as a predictor (none in C).
What to try first next: (1) the parseDump near miss above, (2) ce1's two hoists in getImageSmc with the attribute off (6 loose lines), (3) moving a hint so it does two jobs: this found both pin_lo2 and the parseDump near miss cheaply, so try it on the other pins.

## Attempt 3

Note: the near miss above counts as only -1 from 26 (u1, u2, bar -> one unreachable + the site 2 guard, a dead test that counts).

- gen_ir46: detectController, 80 shapes keeping b[513] in a local `m` (int/uint32 sums, order): pin_found is always 7 and they're all IDENTICAL with it kept; pin_lo not helped.
  pin_found by IRA: found (r108) l0 is the first potential spill, pri 83 = cost 751 / 9.  The reference must give it eax (outer allocno, border store `mov [esp+1c],eax`, both `= 0` edges head-merged).  Its cost is store 324 + load 243 at the loop's edges (freq 81) + l1's 184; the caps next to it have pri ~140, so it needs about double.  Same kind of decision as pin_cb's `xor ebp,ebp; mov [esp+2c],ebp`.
- **u2 gone, IDENTICAL (gen_ir49 v1+u1k+u20+bk):** addRemapP computes `int valid = dest == -1 || (uint32_t)dest < numBlocks;` before its loop and tests `valid`.  (uint32_t)blk is n (FRE) and the loop test is n < (uint32_t)blocks, so at site 3 it folds in fre3 without an unreachable; -1 at sites 1 and 2 folds too.
  Why before the loop: inside the conjunction (gen_ir47 `(dest == -1 || (uint32_t)dest < numBlocks)`) ifcombine leaves `_148 = dest == -1` in the test block T, so T isn't an empty forwarder when the test folds, and the log block merged with it takes T's freq (760, not 220).  That gives blk a register in the site 3 loop: IRA's mem cost 2 uses * 4 * freq/10 against the border's 464, limit freq 580 (a54(r96,l4): 176 base, 608 draft).  6 loose lines.
  Single compares that don't need `||` (`(uint32_t)(dest + 1) <= numBlocks`, gen_ir48): don't fold, 359.
- u1's job: it raises the ECD block's freq from 25 to 58 at profile_estimate.  PRED_CALL only looks at the first block of the guarded arm; with a test there it doesn't see the log call.  A guard must reach 042 and fold later.
  gen_ir50, 51: `blk < blocks`, `blk != blocks` stay as code (70+); `n != blocks`, `n < blocks` fold in fre1 (sccvn records them), no effect on the profile.
- **Barrier gone, 2 lines (gen_ir52 rj):** the -4 arm rejoins before `if (dst != blk)` (`rem:` label after it) instead of `else`.  With the `else` and no asm: 4 loose lines (site 2's two exits reach Z on two edges, LRA inherits edi on one).  Left: site 2's compare prints `n_100 == _125`, the reference has the load first.  n's name is what ch2 pops from the free list, whose top is dce2's last deletion (in rj site 1's dead `dest.43_98 = -1`; with the barrier `_133`).
- **Barrier gone too, IDENTICAL (gen_ir61 v16 on rj):** `int valid = dest == -1; if ((uint32_t)dest < numBlocks) valid = 1;`.  Why: the free list holds dce2's dead statements under its dead PHIs, n pops deep into it, and the form of `valid` decides how many there are.  irname.py groups variants by that compare; spellings elsewhere shift n and the load together (constant offset 27, gen_ir55, 1024 variants) but forms of `valid` move n alone (gen_ir60, 61: n_40..n_180).  v14 is IDENTICAL as well.
  Also no help: `long`/short types on ppb and p (conversion folds or changes code), p's init before the zero test, literal -1 at site 1 (right compare, but site 1's tail schedules like site 2's, 10 loose), (uint32_t)p (right compare, 2 ppb pseudos, 150), `iu` (14).
  hot label on rj: every other position 394+, stays.
- pin_cb (gen_ir64, 65): `Spilling a129r153 for a4r99` in the IRA dump: improve_allocation gives n's l0 allocno ebp once its cost beats the cap of the p loop's ivtmp (5559).  n costs 5307 without the asm, 5547 with three uses (not enough), 5627 with four.  So it needs +5% on n's uses, or -5% on the p loop's frequency relative to the loop top.  for/while/local d,s in the p loop: no effect; do-while goes the wrong way; continue vs goto, `dst != -2` nesting: no effect.
  pin_cb + pin_b2 together: 25 lines, 12 loose: this `xor ebp`, esi loaded before site 2's log, and the summary loop's compare flips (names; forms of `valid` move those, untried).
- copyMmcImage + loadDump (gen_ir62, 63): no attribute, no hot label, loadDump calling copyMmcImage: 307-327, 86 loose for loadDump.  What's left is the log block's place, and copyMmcImage's hoisted `mov edx,1`.  `> 0` and `<= 0` forms fix most of copyMmcImage (11) but loadDump keeps 296.  Reference: standalone copy not hoisted (P <= 50%), inlined one hoisted.  One source test with two probabilities is the nested-if/ifcombine effect in the memory notes; nested forms not swept yet.
- pin_found's cost problem may be the same as pin_cb's: check for `Spilling ... for a1r108` when the costs move.

### State at the end of attempt 3

`drafts/image_read_attempt3.c` is IDENTICAL with 24 tricks: the unreachable before `dst != blk &&` and the barrier in the -4 arm are gone (from 26).
Borderline: addRemapP's `valid`, always true at its three call sites, see above.  The -4 arm rejoining before `if (dst != blk)`, which is then false for it, is live and natural.
Costs on this draft: pin_cb 4, unr_p1 96, pin_b2 307, lab_rem 415, opt_mmc 74.
Don't retry: guards `blk < blocks`, `blk != blocks`, `n != blocks` in the -4 arm (stay as code or fold in fre1); spelling changes elsewhere in parseDump to shift n's name (constant offset to the load); `long`/short on ppb and p.
What to try first next: (1) pin_cb: a natural 5% on n's uses, or the p loop's frequency; (2) pin_cb + pin_b2 with `valid`'s forms for the summary loop compare; (3) copyMmcImage with nested forms; (4) unr_p1's job is only to keep PRED_CALL off the -4 arm: a test that reaches profile_estimate, folds after, and isn't FRE-foldable; (5) getImageSmc's attribute and findAnchor are unchanged.  The free list idea (irname.py) applies to any operand-order difference: try forms of a redundant value before anything else.

## Attempt 4

**New direction, big one: parseDump with a signed `for (blk = 0; blk < blocks; blk++)` and calling the REAL `addRemap` (addRemapP gone, `int block`, no `uint32_t b` line), with no pin, no unreachable, no hot label (gen_ir67 `real+sfor+nolab+nou+ib+inob`): only 20 loose lines in parseDump, 2 in addRemap.** That is 4 tricks (pin_cb, pin_b2, unr_p1, lab_rem) plus the borderline `valid` and addRemapP's gotos, and looks like the author's source.  Left at this point: operand order of `dst != blk` and `blk < blocks - 32`, a `mov ebp,eax; jmp` block, the return 1 epilogue, summary loop's `i < numBad` order, addRemap's `cmp [mem],esi`.
Mechanism for what's left (gen_ir67's base, drafts/image_read_attempt4_base.c): blk's header-PHI name at ch2 is popped from the free list (dce2's deleted names, then copyprop1's), here blk_71 (dce2's `i_71 = PHI<0>`).  The reference needs blk below dst_32 and _40; that also fixes the `mov ebp,eax` block (DOM's equivalence on dst == blk picks the lower name).  In the stack the neighbours of i_71 are found_10 and .MEM_11, so one dead name more or fewer around dce2/copyprop1 should do.
gen_ir68: `uint32_t i` for the summary loop pops one name less at ch2 (no conversion in the copied header): blk_10, exactly as predicted, 69 strict / 11 loose.  Left then: uncprop reuses `bootFlags & 0x40000000`'s zero for i = 0 (types agree), `mov ebx,[0x60]; and` instead of `test BYTE`; and the summary's `return 1` isn't given its own epilogue.  `else if (dst != blk)` for the -4 arm and others: worse.  `continue` for `goto next`, nested last test: no change.
gen_ir69: `(int)xb.bootFlags & 0x40000000` stops uncprop's reuse (types differ): 27 strict lines, and they are all one thing: the summary's tail isn't copied its own epilogue, offsets follow (drafts/image_read_attempt4_base2.c).  connect_traces duplicates the return block only if EDGE_FREQUENCY >= entry * 100 / 1000 (integer): tail edge 5, entry 60 here against 58 under the hinted source, threshold 6 vs 5.  So entry must drop to 59, or the tail reach 6.  Traces: outer loop head 1282 from entry 36 (draft) vs 1280 from 34 (hinted): the return 0 exits take a bit more here.
gen_ir70, 71: spellings of the exits (`== 0`, `<= 0`, else forms, nested site 3, return types) and of the end (return 1 in arms): no change to entry 60 / tail 5.  Reading the profile (irfq.py prints entry and tail): the -4 arm is 13.7% here, 6.4% under the hot label (that's what lab_rem was doing: it gave entry 58).  After inlining rebuild_frequencies scales to the hottest block, which is SITE 3's inlined search loop (33 iterations guessed from badBlocks[32], 303 * 33 = 9700), so entry falls when site 3's reach rises (arms less likely) and rises with exit mass.  tail/entry is fixed, so entry must land on 58 or 59.
irfqp.py (measurement only, builtin-expect at N on one test): parseDump is byte-exact at P(not -2) 73-78 (natural 72), -3 87-88, -1 87, -4 88, site 3 52-53 (natural 51.2).  So a hair of frequency.  gen_ir74: `if (dst == -2) { if (blk >= 0) continue; }`, a dead test VRP folds (P(-2) about 22% at the rebuild): **parseDump and loadDump byte-exact**, entry 56, tail 5, drafts/image_read_attempt4_base3.c; addRemap's 2 lines remain (load vs (uint32_t)block order, its name from the free list at PRE; a `b = block` copy fixes it but costs parseDump 166).
gen_ir75-77 (addRemap's 2 lines): `uint32_t b = block` at entry or a uint32_t param fixes the standalone but moves the conversion out of the loop in the inlined copies: 166 lines (the sites' `xor; xor; test; jne` hoist needs the conversion in the loop).  Forms of the loop, casts in logs and stores, return shapes: always 2.  Mechanism: PRE inserts block's conversion in the preheader, first insertion pops `_40` (found_40, freed by phicprop1), the second pops `_1`.  Below load `_11` only with `_1`.  **gen_ir78 `d`: `uint32_t d = dest;` at the top of the loop body, used for the store: PRE inserts that one first, block's gets _1: IDENTICAL.**
gen_ir79: copyMmcImage + loadDump forms again on the new draft, with a stored result: 177 at best, not landed.

### State at the end of attempt 4

`drafts/image_read_attempt4.c` is IDENTICAL, irlib checked.  Gone: pin_cb, pin_b2, unr_p1, lab_rem (24 -> 20), plus addRemapP with its gotos and borderline `valid`, `b2`, `n`, and addRemap's dead `uint32_t b = block`.  Added: one dead test, `if (dst == -2) { if (blk >= 0) continue; }`: 21 if a dead test counts (README's list), which it should until someone finds a live form.
parseDump is now: signed for loop, real addRemap(int block, ...), three calls.  That this nearly matches on its own strongly suggests it is the author's shape.
Borderline, flagged:
- `blk >= 0` dead test (entry frequency only; see the windows above).
- `(int)xb.bootFlags & 0x40000000`, a plain cast (not counted): stops uncprop reusing the test's zero for `i = 0`.  Note bootFlags being `int` in the original would explain it, and might explain others; untried (xebuild.h, all objects).
- `uint32_t i` for the summary loop with %d (needed: blk's name; int i pops one more name).
- `uint32_t d = dest;` in addRemap's loop (PRE order).
Costs on this draft: pin_found 7, exp_ok1 7, lit_anchor 10, exp_nok1 20, pin_t 23, opt_smc 32, unr_smc 46, pin_lo 52, pin_v 70, opt_mmc 74.
Method that worked, for any function: (1) replace a written-out copy with the real callee and the natural loop first, however bad the first number; read the loose diff, not the count.  (2) operand order = names: work out the free list from the Deleting/Removing lines in dce2/copyprop1/phicprop and PRE's Inserted lines, then find what shifts it by one.  (3) a frequency threshold: irfqp.py measures what probability window would match before you look for a form.
Don't retry: `&&` for a folded guard (cheap compares gimplify to `a & b`, opcode prediction lost); `blk < blocks`, `blk != blocks`, `blk <= blocks` as guards (fold in fre1 or no effect); forms of the exits or return types for the frequency (gen_ir70); addRemap forms without a new conversion (gen_ir76, 77).
What to try first next: (1) a live form with P(dst == -2) of 22-27%, or -3/-1 at 12-13%, or site 3 at 52-53%, instead of the dead test.  (2) The same "real callee" idea on loadDump's written-out copyMmcImage (opt_mmc + lab_mmc, 2 tricks); `bootFlags` as int might bear on it.  (3) getImageSmc written like the natural getImageKv with a look at types (`uint32_t addr`, `size`): its attribute and hot labels look like the state parseDump was in.  (4) pin_found, same IRA cost question, costs may have moved.
