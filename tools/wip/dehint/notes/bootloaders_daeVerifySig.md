# bootloaders daeVerifySig + daeSigCheck (queue 9)

Tools: `tools/wip/dehint/dvsweep.py <gen.py> [-v N]` (plain -O3, outputs in build/dv/<gen>/; n = differing lines of the whole .s text of daeVerifySig + verifyDae, labels and .p2align included; o= other bootloaders functions changed;
rd=1 the object's whole string list and order equal the reference's). The reference is commit 5c78c82's hinted src/bootloaders.c, which built the right SHA256. Generators `gen_dv1.py`, `gen_dv2.py`.

## The hypothesis held: one function, one source

The two copies (`!ok` first standalone, `ok` first inlined) were an artefact of the hinted source. The original has `if (ok)` good first in both, and verifyDae's copy is daeVerifySig itself, inlined at IPA.

gen_dv1, verifyDae calling a single daeVerifySig, with key and hash at function level:
- `if (!ok)` first: 10 lines (8 + 2) and rd=0. daeVerifySig: the `mov eax,1; ret` block lands before FAIL. verifyDae: the `mov [esp+60],ecx` spill is in the good block instead of FAIL. "FAIL" comes first in .rdata.
- `if (ok)` first: 22 lines (14 + 8), rd=1. FAIL falls through in both functions.

So expand order has to be good first (the literal order and verifyDae's spill both show it), and it's the profile that's wrong for `if (ok)`.

## The mechanism (from -fdump-tree-profile_estimate)

Early-return predictor on the `ok` test (bb 4), for `if (ok)`:

    key/hash at function level   early return (on trees) 39.0%, DS 39.0%   good unlikely, FAIL falls through
    key/hash in the if's block   no early return,        DS 50.0%          good stays first

The clobbers explain it. At function level, they're in the return block (`key = {CLOBBER}; hash = {CLOBBER}; return ok_1;`), so the good arm is a block going to the return block with FAIL between them, the CFG the predictor looks for. In the block, they end the block, in a join of their own (`key/hash CLOBBER`, then a separate `return ok_1;` block), so the good arm's successor isn't the return block and the predictor doesn't fire.

That the predictor's test is on the successor being the return block and not next_bb comes from memory of predict.c and the memory file bootloaders-progress.md, and fits this dump; gcc's source wasn't read.

The other tricks fell away with it, none needing separate work:
- literal asm: with good first at expand, "good" comes before "FAIL" by itself.
- always_inline: 50/50 survives IPA inlining, so verifyDae's copy keeps the good-first order, and LRA's spill lands in FAIL.
- no-early-inlining and hint(): they were moving the ret-1 block after FAIL; at 50/50 the `mov eax,1; ret` block lands there on its own. Not traced further, as nothing's left to explain: the text is identical.

## Shapes

gen_dv2 (20; head x key/hash scope x test sense, all with verifyDae calling daeVerifySig):
- 5 at 0 lines, o=0, rd=1: exactly the ones with `if (ok)` and key/hash in the block, for all 5 heads (`ok = 1` + `&&`, `ok = 1` + nested ifs, `else ok = 1`, early returns then a bare block, `||` early return then a bare block). Head form makes no difference, so it's stable.
- 10: fn scope + `!ok`. 12: inner scope + `!ok`. 22: fn scope + `ok`.

## State: landed

src/bootloaders.c, gen_dv2's `nest1|in|ifok` (`int ok = 1; if (xb.pubPirs && size >= 288) { uint8_t key[16]; ... } return ok;`); daeSigCheck and hint() are gone and verifyDae calls daeVerifySig.
fncmp with no flags: MATCH for both. Full build: SHA256 10dac648... matches. drafts/bootloaders_daeVerifySig_best.c is the landed src/bootloaders.c.
Reproduce: python tools/wip/dehint/dvsweep.py tools/wip/dehint/gen_dv2.py ; python tools/re/fncmp.py src/bootloaders.c daeVerifySig ; python tools/re/fncmp.py src/bootloaders.c verifyDae ; sh build.sh

Nothing borderline: no flag beyond the return value itself, no redundant test, locals in the block that uses them. `nest1` was picked as the plainest of the five; crlVerifySig next to it uses early returns instead, but the same style with a bare block reads worse.

For queues 10-12 (cb/cd/ceDecrypt): not tested, but they have `key` at function level, so check where the clobbers land in their profile_estimate dumps too. cfDecrypt and this function both moved by scoping `key`.
