# net netWritePatches (queue 7)

Tools: `tools/wip/dehint/pwsweep.py <gen.py>` (nssweep.py retargeted: plain -O3, clone renamed, outputs in build/pw/<gen>/; o= other net
functions changed, a= .p2align list same as the attribute build), `wbdump.py <src.c> netWritePatches`, generator `gen_wp1.py`.

## What the attribute did

Same as netWriteBlocks: frequency, not inlining. Plain `!netSendStr` shape: 7 lines, 6 of them the epilogue after netFree (`mov eax,[esp+28]`, then
`jmp` where the reference has add esp/pops/ret).

bb 2's first test probability: `!` .61 (call .71 + early return .39); `<= 0` .367 (adds opcode positive .27). The compare exists only at
profile_estimate: netSendStr is inlined at IPA and returns 0/1, so it folds. At bbro the entry goes from 2486 to 1530 while the free block (old bb 14) stays at 237.
connect_traces duplicates the epilogue (`Connection: 14 23 exit`, `Duplicated bb 23`) in the `<= 0` build: 237 clears 10% of 1530 (153) but not 10% of 2486 (249). The same threshold as
netWriteBlocks' notes give; here it's inferred from the bbro dumps, gcc's source not read.

## gen_wp1 (400; head x check x tail x scope)

Heads: `or`, `orle`, seq, seq with `<= 0`, `< 1`, `!= 1`, `== 0`, `||` of the first two then a separate recv test, `netSendData <= 0`.
Checks: expr, set, nest, if/else. Tails: if, if/else, neg, `return ret`, ternary. rlen block or flat.

- 0 lines, a=1, o=0, 6 shapes: `netSendStr("WBPT\n") <= 0 || !netSendData(...) || !(r = netRecv(&rlen))`, rlen in a block, check `expr` or if/else, tail if, if/else or neg.
- 2 (r=0): the same `<= 0` with seq heads (seqle, seqlt, seqorle), or orle with `ret = 0; if ...`.
- 7 (r=7): the old `!` chain. 9: `!` seq.

Whole .s text of v40 (orle|expr|if|block) vs the attribute build: identical apart from the clone's name.

## State: landed

src/net.c: the attribute removed, `!netSendStr` -> `netSendStr <= 0`. Nothing else changed. Reproduce:
python tools/wip/dehint/pwsweep.py tools/wip/dehint/gen_wp1.py ; python tools/re/fncmp.py src/net.c netWritePatches ; sh build.sh

Borderline, for review: `netSendStr(...) <= 0`, the third in the file (netWriteBlocks, netSendFile, here), all three on the first send of a
multi-step upload; netSendStr only returns 0 or 1, so the compare is redundant. The other tests of netSendStr in net.c use `!` or truth.

Next, if anyone wants `<= 0` gone: not tried, a flag on netSendStr's result might move the predictor as netSendFile's `ok` did, but it reads worse than `<= 0`.

## Review (2026-11-10): approved

`<= 0` approved with netWriteBlocks' and netSendFile's: see net_netWriteBlocks.md, "Review" (no netSendStr body makes
`!` match, 10 lines here; the compare is needed or neutral at every upload and wrong at the command-only senders).
