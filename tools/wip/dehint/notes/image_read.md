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
