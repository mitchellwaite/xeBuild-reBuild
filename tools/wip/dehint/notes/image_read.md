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

## Attempt 5

Measurements so far (gen_ir80-85, irmmc.py):
- ce1's IF-CASE-2 (find_if_case_2): the hoisted block's cost is checked against BRANCH_COST scaled by its own probability, so one insn hoists at P >= ~33%, two at >= ~67%.  The hot label on the size test (85%) is why ce1 hoists `addr = 0x1000` in getImageSmc; at a natural 50.4% it wouldn't.
- PRED_CALL needs the guarded block dominated by the test and with the call in its first block; P(bad addr) is 35% with the log first in the arm.
- copyMmcImage standalone: IF-CASE-2 fires at 19-61% alike (gen_ir82, forms of gen_ir79); the zeropair test's probability is the same in the inlined copy (irmmc.py).
- parseDump's entry: exit forms (gen_ir85, 180 variants), nesting the whole body under dst != -2 or else-if chains (gen_ir83, 7 loose lines all), addRemap's end (gen_ir84): all stay 60/5.  irfqp on `if (rr)`: entry 59 needs P(not rr) 62% (natural 61).
- ce1 and ce2 change nothing in getImageSmc: its hoist is **ce3** (post-RA), `IF-CASE-2 start 20, else 8`, the size-bad arm's two moves.  `no-if-conversion2` is the option doing the job.  (P + 12.5%) x BRANCH_COST 3 > 2 insns: it hoists from P(size bad) 54.2%.  `shot`'s 85% is what makes it hoist.
- `a != x && a != y` on a local is one test at profile_estimate (`_1 & _2`, fold_truth_andor): no opcode prediction: P(size bad) 50%, P(bad addr) 29% (call only).  50% loses the tie in bb-reorder (needs 52.7% to beat the ok arm).  **Nested on the same variable: 2 x nonequal, 51.8%, but VRP puts constants into the join's PHI and ifcombine then won't merge.  Nested on `int s; uint32_t size = s;`: 51.8% and it merges (gen_ir88)**.  The size part then lays out like the reference.  Reading h->smcBootSize again in the test (gen_ir87): extra load, no.
- gen_ir89: bad address, no hint: P(bad) stays under 50% because the log is in the arm's first block (call 29%; nested: 72% x 50%).  A dead `if (addr)` first in the arm folds in fre1, before profile_estimate: no effect.  Natural best with the size part right is 99 loose lines: the bad arm isn't the fall-through.
- gen_ir90: attribute + shot gone, size nested on `int s`, other hints in a lattice: 60 at best.  The reference's prologue (addr's load and swap finish before size's load, eax as temp) only comes with pin_addr; every form without it loads both up front.  So pin_addr isn't only about the second name (edi/ebx); `a`/`addr` of two types doesn't reproduce it.
- Re-checked singles on the current source: nothing moved (opt_smc 32, lit_anchor 10, exp_ok1 7, pin_found 7, exp_nok1 20, pin_t 23).

### State at the end of attempt 5

No match, nothing landed, 21 tricks stands.  Mechanisms worth keeping:
1. getImageSmc's attribute has three jobs, separately: `no-if-conversion2` stops ce3's hoist (2 loose lines left with only it, 28 strict: `mov edi,ebx` lands in the good block instead of T), `no-tree-tail-merge` gives that `mov edi,ebx` (12 strict with only it), `no-if-conversion` does nothing (ce1 and ce2 make 0 changes).  So the attribute can be cut to two options; not a count change.
2. Windows for getImageSmc's tests: P(size bad) in [52.7%, 54.2%) does both layout and no hoist; `int s; uint32_t size = s;` nested gives 51.8% and merges (bb-reorder needs a bit more, or frequencies).  P(bad addr) must be over about 50% for the fall-through, and call prediction blocks that; find what stops PRED_CALL (a test or join between the addr test and the log), that's the missing idea.  The zero test must stay first in source (`test ebx; je` is first) and needs two logs (literal 0, crossjumped).
3. copyMmcImage: IF-CASE-2 is ce1/ce2/ce3 by postdominance: it fires at every probability in the standalone (19-90%), and the probability is the same in the inlined copy.  `cost` is the only other brake, and predictable_edge_p at <= 2%.  What stops the hoist in the reference's standalone is unknown; its attribute has only no-if-conversion, so check which of ce1/ce3 it is before anything else (not done: the same split as in point 1).
4. parseDump's dead test: exit forms can't move entry, except `continue` after -1's addRemap (136).  irfqp: `if (rr)` 62% gives entry 59 (natural 61), but expect itself costs 107 there.

Don't retry: gen_ir83-85's spellings (entry 60/5 for all); reading the header field again for the tests (gen_ir87); `a`/`addr` nested forms without a way past PRED_CALL (gen_ir88, 89); hint placement without the attribute (gen_ir86, stays 6 at best).
What to try first next: (1) point 3's split for copyMmcImage, cheap.  (2) point 2: what stops PRED_CALL on the bad arm.  Attempt 5 left unread: tmp/xeBuild64's getImageSmc (gcc 4.9, structure only; the brief said to leave tmp/ alone) would show whether the author's tests or helpers differ, e.g. a helper for the size fix.  (3) a static helper for the size arm (`size = fixSmcSize(addr)`): a call in the first block at profile time if it isn't early-inlined; untried.

Late additions:
- gen_ir91: the size arm as a static helper called in the arm (shot and unr_smc gone, attribute, pin_addr and exp_smc kept): 29 loose lines, only the arm's placement and one lea.  The call makes P(size bad) go down (<50%), the wrong way for layout, though it shows those two hints do nothing but that placement.
- gen_ir92: gen_ir90 with the attribute kept: same scores, 60 at best (the second variable costs the prologue).

## Attempt 6

tools/wip/dehint/ir64.py <addr> <size> prints a function of tmp/xeBuild64 (older Linux build) with strings; addresses in tmp/strs/match.txt (L 417960 findAnchor, L 416c10 getImageSmc).

**findAnchor: 3 expects + barrier gone, IDENTICAL (gen_ir97).** Whole-function sweep with no hints (gen_ir93): both valid, clear the older block's flag: `if (ok0 && ok1) { if (v0 < v1) ok0 = 0; else ok1 = 0; } if (ok0) S0; if (ok1) S1; return 0;` compiles to the reference's code exactly, the only difference being .rdata order (lit_anchor kept for now).  21 -> 17 tricks.
Why it works: `_ok0 & _ok1`'s false edge gives VRP and dom2 nothing, so the join after I1 stays a real join with a PHI until dom3, and the I1 block has no ok0 test to thread when J's threads are chosen.
lit_anchor (gen_ir94-96, 98, 102, 103; S1's string must be expanded after V1 and before I1, chain order): S1 in the valid arm: V1 -> T always proves ok0 (true edge of `_a & _b` or false edge of `_a | _b`), so vrp1 threads V1's path past T, T merges with I1 and dom2 splits I1 (17-37).  `if (ok1) V1; if (ok0 && ok1 && v0 < v1) ok0 = 0; if (ok1 && !ok0) S1; if (!ok1) I1; if (!ok0) return 0; S0` (gen_ir96 hnr) has the right CFG but dom3 keeps (4,5)(5,6)(6,9), so both V1s are copies (string last) and v1/ok0 swap regs: 24.  clr only works because (6,11) starts a thread of its own, which cancels (4,5)(5,6)(6,11): needs V1's false edge straight to the PHI block; PRE's `_4 = ok0 == 0` block gets in the way, and spellings of ok0's two tests (gen_ir102) don't remove it.  goto-spelled block order (gen_ir103): strings right, layout 31.  Also mark_threaded_blocks: unordered_remove on a cancelled joiner moves the last path up, so which of a second joiner path survives depends on how many paths are registered after it.
fsGetFile calling the real fsFindFile (gen_ir100): v goes to memory, 174.  getImageSmc no hints, 336 forms incl. flags and ladders (gen_ir101): 110 at best.  detectController found's placement and types (gen_ir99): 7 for all, int found 46.  scanMobiles without exp_scan (gen_ir104, 60 forms: order of the two len tests, newer flag, polarity): 81 at best, block layout only.
loadFlashFile: `while (size - done > 0x4000)` as the Linux build has it (gen_ir105): IPA size stays 45, still inlined.  `if (left > 0x4000) { while ... }` or do-while (gen_ir106 el, dw): not inlined, no attribute, only RA left in loadFlashFile: 60 strict, 41 loose (the loop's frequency halves).
**noinline gone, IDENTICAL (gen_ir107 i3-i9):** `if (left) { off = fsOffset + (block << 14); memcpy(...); }`: off recomputed before the last copy although the loop just did it.  Extra statements at IPA time push growth past the limit, later passes remove them and the code is the same.  Spelling it in the memcpy (i5, i6) is the same.  (Without a first computation before calloc, `ini2`, 47.)  Borderline: live, redundant.  16 tricks.
fsGetFile pin_v, correction: r106 in the IRA dump is `off`, not name.  Pop order is by thread freq (r104 block, off's thread 582, then retval), with the pin too; the pin only makes off choose edi (retval's SIREG preference shows up in off's conflict costs).  So a natural form has to pop retval before off or give it esi's preference.  72 forms of off, next block and single exit (gen_ir109): 70 for all.
Linux getImageSmc (ir64 416c10): same two tests, both to ONE log; `cmp ebx,eax` unsigned PHI next to r12d int: the second name for addr is natural (int addr vs the unsigned compare).  Sane arm falls through in Linux, ok path falls through too (unlike the reference).
**getImageSmc, big lead (gen_ir110):** `if (!addr || (addr != 0x800 && addr != 0x1000)) goto bad;` with bad: at the end and no bhot, no vhot, no attribute (shot, unr_smc, pin_addr, exp_smc kept): only 25 loose lines; with the attribute 20.  Because `bad` has two predecessors at profile_estimate, it isn't dominated by the second test: no PRED_CALL there, which is what bhot was for (predicted above in Attempt 5's point 2).  What's left: the string (`bad` expands last), `mov edi,ebx` place, and the `mov [esp+8],0; jmp` block: needs a second log at expand, crossjumped.
gen_ir111, 112: `or` form's lattice: attribute, bhot, vhot and unr_smc all drop out with it (shot, pin_addr, exp_smc kept: 25 loose; shot gone too: 45).  Not landable yet, one log: no `mov [esp+8],0; jmp` block and the string expands last.  Two logs (t1, t2): PRED_CALL is back, wrong arm falls through, 46.  Inline arm reached by two edges (`if (addr) { if (addr == 0x800 || addr == 0x1000) goto ok; } log; ok:`, i1): string right, attribute not needed, pin_addr not needed for layout, but the prologue and size's mask (kept in a register over the call, ebp) differ: 44.  Zero arm inline plus a second edge to the bad arm from a test only VRP can fold (gen_ir112: `if (addr) ...` after the zero arm, `addr <= 0`, `< 0`): 62-65, and `addr < 0` is live (`js`).
Why two logs must exist at expand: `mov [esp+8],0; jmp` into the middle of the other log is crossjumping; a PHI with 0 would be one store from a register.  Threading could make the copy only if the bad block ends in a test known on the zero edge, and nothing there is.

### State at the end of attempt 6

`drafts/image_read_attempt6.c` is IDENTICAL, irlib checked, 16 tricks (21 before): exp_ok0, exp_nok1, exp_ok1, bar_anchor, noinline gone.  Left: 5 pins (addr, v, t, found, lo), 2 expects (smc, scan), 4 hot labels (vhot, shot, bhot, mmcbad), 2 optimize attributes, 1 unreachable, 1 literal asm (findAnchor), 1 dead test (parseDump).
Borderline: loadFlashFile's `off = ...` again before the last memcpy (live, redundant, size at IPA).  findAnchor's cleared flags aren't borderline: they read as the author's shape.
Method that worked: drop every hint of the function at once and sweep whole-function shapes, reading the loose diff; a shape with state (a flag) rather than a compound condition hides knowledge from VRP and dom2.  And a block with two predecessors isn't "guarded" for PRED_CALL.
Costs on this draft: lit_anchor 6 (only .rdata now), pin_found 7, pin_t 23, opt_smc 32, unr_smc 46, pin_lo 52, pin_v 70, opt_mmc 74, exp_scan 137.
Don't retry: fsGetFile's off forms, exits (gen_ir108, 109); findAnchor with S1 in the valid arm (gen_ir94, 95, 98); `size - done` loops for loadFlashFile (gen_ir105).
What to try first next: (1) getImageSmc from the `or`/i1 lead: how two logs can coexist with no PRED_CALL on the second, or the i1 form's size mask (stop the `and` being kept over the call).  That's up to 5 tricks (attribute, vhot, bhot, unr_smc, pin_addr).  (2) exp_scan with the same idea (a block with two predecessors, flags).  (3) checkBlock's pin_t: no_side_effect_bb / suitable_cond_bb in reassoc refuse a second test block with a PHI, or a join PHI whose args differ on the two false edges; the Linux build keeps both tests as well, so something in the source stops it; untried.  (4) lit_anchor: a dom3 thread of V1 -> T that survives with S1 written before I1.  (5) IPA size as a lever: anything that used an attribute only to stop inlining (copyMmcImage).

## Attempt 7

New tools: irbb.py <file.c> <fn> [pass..] prints each block's freq, successors and test from a tree dump (optimized by default).
gen_ir113-117, getImageSmc, whole-function, no hints:
- Threading raises P(bad): T's bad edge keeps its freq while the zero path's share of T's ok edge goes away.  Nested tests on a uint32_t copy (`uint32_t a = addr; if (a != 0x800) { if (a != 0x1000) {...} }`, `a` in gen_ir114) merge in ifcombine and end at 60.6% x 85.8% = 52%: the bad arm falls through with no bhot, vhot or attribute (two logs, string order right, crossjump gives `mov [esp+8],0; jmp`).
- `mov ebx,0x1000` before the call in the hint-free forms isn't ce3 (attribute options make no difference, gen_ir116): both edges out of the size test start with the same constant moves and crossjump's head merge hoists them.  The reference has a real ok-join block holding `ebx = (unsigned)edi`, so the two edges differ.  The hinted source gets that block from pin_addr's asm.
- gen_ir117: a real `uint32_t a` set in the arms (`a = addr;` at the end of the bad arm and in the else) gives that join with no asm: prologue, `cmp ebx,eax`, edi/ebx and `mov ebx,edi` all right, with no expect either.  `b.and.k3.a.e0`: 54 loose lines, all layout: P(bad) is 40.9% with `&&` on addr, and the two return copies from the 50% sane test.
- gen_ir118 `t6.and.k3.ex`: **9 loose lines with only exp_smc kept (attribute, 3 hot labels, unreachable, pin_addr gone):** `unsigned t = addr; if (t != 0x1000) { if (t != 0x800) {...} }` (0x1000 first: t7, 0x800 first, is far worse), `size` tested with `&&`, `a = addr;` at the end of the bad arm and in the else, `a < 528 * xb.dumpPages`, `xb.dump + a`.  Saved as build/ir/a7k3.c's shape.  What's left, three things:
  A. prologue tail `mov esi,ecx; and esi,0xff00; add esi,eax` vs `and ecx,0xff00; lea esi,[eax+ecx]`: IRA tie for `_28`, decided by P(size ok): with P(size bad) 85% (shot or an expect) it comes right.  So it wants P(size bad) above 50, E's freq lower.
  B. `mov edi,ebx` in T: shrink-wrap's prepare_shrink_wrap sinks the copy `addr = _20` from bb2 until a block where edi is live on both ways.  In the reference T stops it, because the bad arm's log still reads addr's pseudo at that time (cprop_hardreg changes it to ebx later).  Here global cprop has replaced it with _20's pseudo (r88 = a's, canonical), so it sinks into the ok arm.
  C. `mov edi,0x1000; mov ebx,edi` (with the ok path jumping to the second insn): a real conversion in the ok join.  PRE always rewrites `a = addr` there into a PHI and a copy in the ok predecessor, whichever way it's spelled (by_some is true because the other two edges have constants).  The asm is what keeps it in the hinted source.  Nothing natural found.
- Partition numbers follow the root's SSA version, and pseudos follow partitions: hinted r87 addr, r88 size, r98 _20; a7k3 r87 size, r88 a, r126 addr, since addr has no PHI at the final join from into-SSA.  `addr = 0x800` in the 3800 arm (g4, gen_ir123) gets r88 addr, r89 size, r90 a, but B stays.
- gen_ir126: else arm `size = s` from `uint32_t s` keeps the join with no named a: same A, B, C, plus `cmp eax,ebx` (prephitmp's name is high).  gen_ir127: size nested on s: not merged or ok path splits, 19+.
- C and B share one cause.  In cse, the bad arm's log keeps addr's pseudo only if addr's pseudo is live out of the extended block and _20's isn't (make_regs_eqv), which holds only when that edge sets addr alone, with the conversion in the join.  So both need a conversion PRE can't touch; the hinted source has one because the operand is an asm output.  pin_addr can't go until something else PRE-proof shows up.  Also the forwarders of the zero and bad edges must not be tail-merged (the attribute's other job): merged, the path ends at the log and addr isn't live out.
- gen_ir125, 128 (pin_addr kept, t6, k3): 21 loose lines, no attribute, no hot labels, no unreachable: the size half of the prologue and `mov edi,ebx`; with no-tree-tail-merge, regs swap (79): no partial landing found in that lattice.
- Checked vs inferred: B's shrink-wrap is checked (with `no-shrink-wrap` added to the hinted source, `mov edi,ebx` stays above `test ebx,ebx`).  The make_regs_eqv and PRE explanations, and find_if_case_2 below, are from my memory of the gcc sources plus the dumps, not read at the tag: check them before building on them.
- copyMmcImage, mechanism (not swept): ce1 hoists `ret = 1` when P(else) >= 50 or when SUCC(else) postdominates the log arm.  The attribute's job is only this: with `no-if-conversion2` alone the hoist moves `ret` above the test, ret conflicts with eax and takes edx (6 lines); with nothing, 9.  A natural form needs the success path's successor not to postdominate the log arm at ce1 (a block on the success path only that's gone by bbro), then P decides, which also explains standalone not hoisted and inlined hoisted.  Untried.

### State at the end of attempt 7

No match, nothing landed: 16 tricks stands.  `drafts/image_read_attempt7.c` is NOT identical: it's the near miss, getImageSmc with only exp_smc (attribute, vhot, bhot, shot, unr_smc, pin_addr gone): 9 loose lines in getImageSmc; the 46 lines in _fsFindFile, _imgGetSecurityFiles and _loadDump look like only cross-function offsets (_fsFindFile's are `jmp -f70` vs `-f60`; the others not read), because getImageSmc ends 0x10 bytes earlier.  Its source shape:
`if (!addr) {log; addr = 0x1000;}  unsigned t = addr; if (t != 0x1000) { if (t != 0x800) {log; addr = 0x1000;} }  if (size != 0x3000 && size != 0x3800) {arms; a = addr;} else {a = addr;}  if (__builtin_expect(a < 528 * xb.dumpPages, 0)) ... xb.dump + a`
Linux's r12d/ebx pair is the same pair as a and addr.
Left: A, B, C above.  A wants P(size bad) over 50 at no cost to the rest (window [52.7, 54.2) from attempt 5, at the crossjumped block).  B and C want a conversion of addr in the ok join that PRE can't rewrite.  With pin_addr kept (gen_ir125 `t6.D.k3.ex`): C is fixed and 21 loose lines remain (size half of the prologue, `mov edi,ebx`), and that form has no attribute, hot label or unreachable, so finding the prologue's cause lands 5 tricks if `mov edi,ebx` can be had without no-tree-tail-merge.
What to try first next: (1) gen_ir125 `t6.D.k3.ex`: the prologue's IRA tie (A's relative) and the tail merge of the two forwarders: make the zero and bad edges' forwarders differ at PRE, or get the zero edge threaded only after PRE (dom3).  (2) A statement in the ok join PRE can't rewrite.  What rules PRE out: by_some is true from the constants on the other two edges, so any pure conversion or arithmetic on addr is rewritten; only an operand phi_translate fails on, or a cold edge, escapes.  (3) copyMmcImage's mechanism above.
Don't retry: `a`/addr assignment spellings in the arms for C (gen_ir119, 123); else `size = s` (gen_ir126: same A, B, C); size nested on s with a (gen_ir127: 19+); 0x800 first in the nested addr test (t7: 158); attribute options on the near miss (gen_ir120: no help).  pin_t: reassoc's refusals are a second block with a vuse or an outside use, or PHI args differing on the two false edges; none of them survive to reassoc2 and vanish afterwards in any form I could think of; not swept.
