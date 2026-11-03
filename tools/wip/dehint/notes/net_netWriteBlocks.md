# net netWriteBlocks (queue 5)

Tools: `tools/wip/dehint/wbsweep.py <gen.py>` (plain -O3, outputs in build/wb/<gen>/; o= other net functions whose
text changed), `wbdump.py <src.c>` (predictions, optimized GIMPLE, bbro traces, jump2), generators `gen_wb*.py`.

fncmp caveat: on any function that calls netRecv, plain fncmp prints a 2-line diff even when landed
(`call _netrecv` vs `call L`, because gcc calls it `_netRecvVerbose.constprop.1`; src/net.c with its attribute shows that
same diff). wbsweep renames the clone in the asm first (FNCMP_ASM), so its 0 means MATCH.

## What the two attributes did

Attribute off, unscoped rlen: 7 lines (5 + the call). Two separate effects:
- no-crossjumping: jump2's head merge of the two `mov eax,1` after `cmp ebx,netEmpty`. Already known fix: scope `rlen` in a
  block ending before the `if (ret)` tail; its clobber gives the edge its own block. It's needed: in gen_wb3, every shape
  at 0 lines has rlen in a block.
- no-early-inlining: the free block has to reach freq 1000 (connect_traces' freq_threshold, 10% of the entry) for bbro to
  copy the epilogue after it. Early-inlined it's 953, with the attribute 1069. Not really about inlining: inlined at IPA
  the free test keeps netFree's own estimate, .783 (pointer .85, call .29, early return .61), where early-inlined it's
  .698, since the block after it isn't the return block, so no early return.

The free block: F = S * D * N * P = .39 * .39 * .899 * .698 = 953, S the netSendStr test, D the netSendData test,
N `r != 0`, P `r != &netEmpty`. S and D are DS(early return .61, call .29).

## gen_wb1 (640; head x null test x check x tail x scope, all with `!netSendStr`)

Best 5 lines, the epilogue only: `ret = 0; if (...) ret = 1;` or nested ifs, `if (ret) return 1; return 0;`, rlen in a block.
Head form (seq, `||`, `&&`, nested) makes no difference. `ret = expr`, else, neg: 7. `return ret`: 17+.

## gen_wb2: MATCH, the opcode predictor on the netSendStr test

`if (netSendStr(cmd) <= 0) return 0;`: netSendStr is still a call at profile_estimate, so the compare takes PRED_OPCODE_POSITIVE
(`!x` takes nothing, as compares with 0 for equality aren't predicted). S goes to .63, F to 1549; the compare folds once
netSendStr is inlined at IPA (it returns 0/1), so nothing is left in the output. Traces split differently in rounds but connect
to the same order. `< 1`, `<= 0 ||` also match. `!= 1`: wrong way (opcode nonequal), 5. `netSendData(...) <= 0`: real compare
stays (not inlined), 2.

gen_wb3 (640; the same axes with `<= 0`/`> 0`): 16 at 0, all with rlen in a block and `set` or `nest` for the check, any head form. So
it's stable, not a fluke of one shape. o=0 for all.

gen_wb4 (12; `!netSendStr` kept, reply check in a static helper, to get P's .783): helper is early-inlined, best 5, the same miss. Not worth more.

## State: landed

src/net.c: `if (netSendStr(cmd) <= 0)` + scoped rlen, no attribute. drafts/net_netWriteBlocks_best.c.
Reproduce: python tools/wip/dehint/wbsweep.py tools/wip/dehint/gen_wb2.py ; python tools/re/fncmp.py src/net.c netWriteBlocks

Full build: SHA256 10dac648... matches (plain fncmp on src/net.c shows only the `call _netrecv` line pair from the caveat above).

Borderline, for review: the 16 other tests of netSendStr in src/net.c use `!` or truth. This is the only `<= 0`, and netSendStr only
returns 0 or 1, so the compare is redundant. It reads as ordinary socket-style code, but its effect here is the predictor.
For queue 6 (netSendFile), the same scoped rlen + `<= 0` may be worth trying: same OK-reply tail, not tested here.
