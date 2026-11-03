# bootloaders cbDecrypt (queue 10)

Tools: `tools/wip/dehint/cbsweep.py <gen.py> [-v N]` (plain -O3, outputs in build/cb/<gen>/; n = fncmp lines, a = differing lines of the whole .s text against the hinted
build (build/cb/hinted_bootloaders.c, commit 28bd769), o = other functions changed, rd = string list and order equal). It takes `FN` = cbDecrypt, cdDecrypt or ceDecrypt.
`tools/wip/dehint/cbdump.sh <file.c> <outdir>`: every tree and rtl dump. Generators `gen_cb1..7.py`.

## The brief's description holds

Without the attribute, locals at function level (gen_cb1 v0): fncmp 1 line, a=1: one missing `xor ebx,ebx` at the calloc-fail log. Unlike cfDecrypt, it was right. But the fix isn't in that block: the original's failure paths simply join.

## The general mechanism (for cd/ceDecrypt too)

The original returns all its failures through a scope-end clobber block, and the good arms return from inside the scope:

    if (cb) {
        if (magic) {
            uint8_t key[16]; ...
            if (buf) {
                ...
                if (pub) {
                    if (verify) { log ok; if (outLen) ...; return buf; }
                    log error; free(buf);                   /* falls out */
                } else { log warn; if (outLen) ...; return buf; }
            } else
                log alloc;                                  /* falls out */
        } else log magic;
    } else log null;
    return 0;

Five things follow from that one shape, each one measured in dumps (-fdump-tree-uncprop1, -profile_estimate, -fdump-rtl-cse1-details):

1. **uncprop.** The return from inside the scope makes tree-eh copy the clobber, so the fall-out has `<bb 16>: key = {CLOBBER}` with two preds, the alloc-fail log (bb15) and the free path (bb12). uncprop1: `_1 = PHI <buf_16(18), cb_6(D)(20), 0B(19), 0B(16)>`.
   The 0 is on bb16's edge, and the test's false edge doesn't dominate bb16, so it stays 0. In the hinted shape bb15 itself was the PHI's pred and its 0 became `buf_14`, no copy, no xor. (What the attribute's no-tree-dominator-opts really switched off was this.)
2. **CSE, what no-cse-follow-jumps was for.** Even with uncprop off, expand's `retval = 0` in bb15 (buf and the result are one pseudo, 110) goes in cse1. `-fdump-rtl-cse1-details` has `Following path ... 2 3 4 5 15`: CSE walks the single-pred path past the jump, knows the pseudo is 0 there, and the set is a no-op. gen_cb5 proves both halves were needed: either alone is still the same 1 line.
   In the landed shape the set is in the two-pred block, so no path reaches it knowing anything. Same cause, same fix: both halves of the attribute were doing one job.
3. **The xor's place.** The one `xor ebx,ebx` of the clobber block is a copy of the PHI's edge. bbro duplicates that 1-insn block into each pred (it's smaller than a jump), and sched2 (after bbro) moves it above the log call. So the `xor`s that look like per-path code in the original come from one source block. The `free` path's `mov [esp],ebx; xor ebx,ebx; call _free` is the same.
4. **Null-return prediction.** gen_cb1's key in `if (cb)` already had the xor, with `free(buf); buf = 0; ... return buf` kept: 20 lines, all layout (L179/L180 swapped, a return copy). The free path's 0 was then in an inner PHI at the return's clobber block, `buf_1 = PHI <0B(12), buf_17, ...>`, and apply_return_prediction only looks at the PHI of the return itself. So bb9's test lost `null return heuristics: 90%` and went to 50/50.
   Falling out puts the free path's 0 on `0B(16)`, a direct argument, and bb9 is back to 90%. That's why `buf = 0` has to go and not only the alloc path: no extra tests, no hints, just no `buf = 0`.
5. **key's block.** Block where the failures can join: key in the magic block has {free, alloc} in the clobber block and magic's own 0 direct: a=0. In `if (cb)` it also takes magic (gen_cb3 `fall|cb`): fncmp MATCH but a=7 (p2align/labels). In `if (buf)` alloc-fail is outside the scope, nothing to share: 1 line. Function level: no copy of the clobber: 1 line.

What's measured and what's inferred: the PHIs, the predictions, the cse1 path and the deleted insn are in the dumps. Item 3's bbro duplication and sched2 move, and "only the return's own PHI" in item 4, are inferred from the output and memory of gcc's passes; gcc's source wasn't read and no pass-by-pass trace of the xor was done.

Types don't do it (gen_cb2, return x buf type): when they differ uncprop leaves the 0 since it can't coalesce, but then result and buf are two pseudos and the result takes eax: 12 lines. The original has one pseudo: `mov eax,ebx` in the return block.
buf's own scope and len's never matter (gen_cb1, gen_cb4).

## Shapes

gen_cb1 (36; key x len x buf scope, hinted control flow): 1 (key at fn), 20 (key in if (cb)), 21 (magic or buf). len and buf no effect.
gen_cb2 (32; types): 1 when same type, 12 when different, 122+ for integer returns.
gen_cb3 (36; sig-failure tail x key scope x alloc's else):
- `fall` key=magic: **MATCH, a=0, o=0, rd=1**
- `fall` key=cb: MATCH, a=7. `goto` (sig failure `goto fail` past the scope; label before `return 0`) key=cb: MATCH, a=5.
- `zero`/`ret0` (buf = 0 or return 0 in the free arm): with scoped key 20-21 lines, the inner PHI above.
- `fall2` (shared `if (outLen)` after the join): 7-8 lines (that join isn't in the original).
gen_cb4 (15; fall + key in the magic block, x buf/len scope, order, initialisers): all 15 MATCH a=0 o=0 rd=1. Stable, not a fluke of one spelling.
gen_cb5: the hinted shape with one half of the attribute: 1 line each way.

## Look-ahead for queues 11 and 12 (not landed, their hints untouched)

- cdDecrypt (gen_cb6, same shape): fncmp MATCH, a=0, o=0, rd=1. Should land as it is.
- ceDecrypt (gen_cb7, same shape, no pin): fncmp MATCH, o=0, rd=1, but a=1: one `.p2align 4,,10` before a block is missing against the hinted build. So the pins aren't needed for the code; only the alignment of one block is left, and the full build would catch it. Check that block's frequency first (`-falign-jumps` threshold in final, as in the other p2align notes).

## State: landed

src/bootloaders.c: gen_cb4's `buf=magic len=magic buf,len,key`, no attribute. fncmp with no flags: MATCH. Full build: SHA256 10dac648... matches. drafts/bootloaders_cbDecrypt_best.c is the landed src/bootloaders.c.
Reproduce: python tools/wip/dehint/cbsweep.py tools/wip/dehint/gen_cb4.py ; python tools/re/fncmp.py src/bootloaders.c cbDecrypt ; sh build.sh

Nothing borderline: no flag, no redundant test, no `goto`, all three locals at the top of the block that uses them. The one judgement call: key is one block further out than its innermost use (the magic block, not `if (buf)`), but it sits with `buf` and `len`, and `len`/`buf` could live elsewhere without changing anything.
The comment on cdDecrypt was carrying "as cbDecrypt", so the explanation moved there (and ceDecrypt's says "as cdDecrypt"); comments only.
