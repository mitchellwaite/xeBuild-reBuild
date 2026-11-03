# bootloaders ceDecrypt (queue 12)

## State: landed. The missing .p2align has no effect on the bytes.

gen_cb7's a=1 was never a blocker. L228 is at .text offset 0x1a15 of bootloaders.o, so the next 16-byte boundary is 0x1a20, 11 bytes away, and `.p2align 4,,10` skips at most 10: it emits nothing there. `a` compares .s text, so it counts a directive that assembles to no bytes. The look-ahead in bootloaders_cbDecrypt.md and the brief both assumed the full build would catch it; it doesn't.

Measured:
- gen_cb7 v0.s and ref.s assembled: .text identical (6784 bytes, 0 differing).
- v0.c compiled the way build.sh compiles it (`#line 1 "bootloaders.c"` through stdin, -O3): `cmp` with build/obj/bootloaders.o identical, before src/ was touched.
- Landed: fncmp with no flags MATCH for ceDecrypt, cdDecrypt, cbDecrypt, cfDecrypt, cgDecrypt, daeVerifySig. `sh build.sh`: every section 0 differing bytes, headers 0, SHA256 10dac648197fa5cdbb82d975ab9ff11f64075c9686908dfd9a33edc533f1971c, `cmp` with xeBuild.exe identical.

cbsweep on this shape keeps saying a=1, and will: it's the hinted .s that had the extra directive, not the original, as far as anyone can tell. The binary can't show whether the original's compiler emitted it. So everything below about the alignment is true of the directive, but wasn't needed to land, and the "window" isn't evidence about the original's source.

Check next time, before chasing an `a` difference that is only a .p2align: assemble both and compare .text.

Behaviour, traced against the hinted version: null bl/hmacKey logs, returns 0. Bad magic logs, returns 0. calloc failure logs, returns 0. Hash failure logs, frees buf, returns 0 (was `buf = 0; return buf`). Hash OK logs, sets *outLen if given, returns buf. No hash warns, sets *outLen if given, returns buf. Same on every path.

Nothing borderline: no flag, no redundant test, no goto. Same judgement call as cb/cdDecrypt: `key` sits with `buf` and `len` at the top of the magic block, one block further out than its innermost use. Key's block does matter here (gen_ce7: every a<=1 result has key in the magic block); len/buf's doesn't.

The pin and attribute are gone, so bootloaders.c has no `__attribute__` or `__asm__` left.
drafts/bootloaders_ceDecrypt_best.c is the landed src/bootloaders.c.
Reproduce: python tools/wip/dehint/cbsweep.py tools/wip/dehint/gen_cb7.py ; python tools/re/fncmp.py src/bootloaders.c ceDecrypt ; sh build.sh

The official gcc repo returned 429, then an Anubis denial, for predict.c, so no source was read; statements about predict.c and final.c below are from memory, checked against the dumps. No mirror was used.

Probes (ceprob.py, ceprob2.py) use __builtin_expect + --param to measure windows. They aren't source shapes.

Tools: `cbsweep.py <gen.py> [-v N]` (see bootloaders_cbDecrypt.md for the columns), `cbdump.sh`. Generators `gen_cb7.py` (the lead), `gen_ce*.py`.
Block/edge frequencies: compile with `-fdump-rtl-bbro-details-blocks` and read `;; basic block` / `;;  pred:` in the bbro dump.

## The missing alignment (measured)

gen_cb7: fncmp MATCH, a=1, o=0, rd=1. Missing: `.p2align 4,,10` before L228, the alloc-fail log (`Unable to allocate`), the target of `je` after calloc. It has one predecessor (1 use), no fallthrough.

compute_alignments' no-fallthrough rule (from memory of final.c, consistent with the numbers): branch freq > max_freq / align-threshold = 10000 / 100 = 100.

- plain: edge 6->15 is 1.9%, bb6 freq 5041: 97. Not aligned.
- hinted: same bb6, edge 15.0%: 756. Aligned. (bb15's own freq still reads 97 in the hinted dump: the threaded edge's probability was replaced, the count wasn't.)

Why the percentages differ, from -fdump-tree-profile_estimate:
- plain `if (buf)`: pointer 85, null return 90, call 71, call 29 (cancel): DS 98.1%, fail 1.923%.
- hinted: the *first* `if (buf)` (guarding only the asm) has pointer 85 alone: 85%, and jump threading keeps that edge. The second has 98.1% and is threaded away.

So the pin's block wasn't only pinning registers: it's what gave the alloc-fail edge its 15%.

## The window

Needs edge freq >= 101.
- Raising bb6 instead doesn't work: T1 of bbro stops at bb6 because bb7 (4945) is under the first-round threshold of 5000. Above that bb7, bb8, bb9 join trace 1 and the out-of-line blocks reorder (gen_ce1 `base two`: bb6 6663, 42 lines). So bb6 * (1-p) < 5000 and bb6 * p > 100, so bb6 <= ~5100 and p >= ~2.0%.
- So the alloc test's own probability has to move, from 1.923% to at least 2.003%.

## Shapes

gen_ce1 (arm spelling x magic form): `base one` is a=1. rd=0 for anything with the fail log first (`if (!buf) log; else`, `if (!magic) log; else`): .rdata order pins positive tests with the logs in the else. `two` (nested magic tests, two copies of the magic log): bb6 too high, layout changes, 37-42 lines. `ret0`/`retbuf`/`twotest`: 51+ lines.
gen_ce2 (magic through a flag): whole-magic flags 114 lines (rd=0), `ok = (..==..); if (ok && bl[1]=='E')` and `ok = bl[1]=='E'` a=1 (no change).
gen_ce3 (flag on buf): `if (buf) ok = 1; if (ok)` 64 lines, rd=0: edge 15% as hoped, but threading updates the block counts too (log 756), so IRA and the block order move. `ok = buf != 0` folds: a=1. memcpy under a first `if (buf)`: 52.
gen_ce4 (real code in a first `if (buf)` arm): 52-77, rd=0.
gen_ce5 (176, cleanup gotos and return placement): 20 fncmp MATCH, best a=1, none has the directive. `else { log; return 0; }` loses null return (85%), 41+ lines.
gen_ce6 (`n = buf ? len : 0` and similar): 64-83, rd=0, same as gen_ce3.
gen_ce7 (300, head spelling x hash form x key block x len block): alloc test 98.1% in all 300, best a=1.

Probe windows (a= against the hinted build):
- ceprob, P(buf) by expect: 99 a=1, 98 a=0, 97-91 a=55 (bl/hmacKey/len rotate: at 98 IRA pops r95, len, before r114, bl; at 97 the other way round), 90-75 a=67.
- ceprob2, second magic test by expect: 59 a=1, 60-64 a=17-31, higher worse. Confirms bb6 can't carry it.

The alloc test only ever took 1.9%, 6.7% or 15% from natural source. If the directive ever does matter, 2.0% to under 3% is what's needed and no natural shape tried reaches it.
