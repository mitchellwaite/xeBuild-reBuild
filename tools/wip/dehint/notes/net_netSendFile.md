# net netSendFile (queue 6)

Tools: `tools/wip/dehint/nssweep.py <gen.py>` (plain -O3, clone renamed, outputs in build/ns/<gen>/; o= other net functions changed,
a= .p2align list same as the hinted build, which fncmp can't see), `nstab.py <file.c|gen.py>` (lines, aligns, buf's MEM cost, trace freqs;
NS_N="..." sweeps the expect param, diagnostic only), `nsira.py <src.c>`, `wbdump.py <src.c> netSendFile`, generators `gen_ns*.py`.

## The reference (build/obj/net.o)

Order: name test, buf test (`mov ecx,[buf]; test ecx,ecx`: buf has no register), init, strcpy, inline strlen, send, `cmp; je L_ok`, shared ret0 block
(aligned), L_ok aligned: log_get_verbose, netSendData...

## Mechanics (measured)

- `!name || !buf` folds to one test. At expand it's split in two: T (buf test block) = 1 - P/2, pass = 1 - P. Predicted P = .61 (call .71 + early return .39).
- `if (!name) ...; if (!buf) ...` (P1 .101, P2 .216) is ifcombine'd later: T = 1 - P2/2 = 8918 whatever P1 is, pass = (1-P1)(1-P2) keeps the estimate. So src/net.c's
  expect alone leaves buf in a register. The asm pin's real job: buf is addressable, so its load stays in the second block and ifcombine can't merge the tests (T = 1-P1).
- buf out of a register: MEM cost = .4*(T + U) - 4006 (fits 8 points), U = netSendData's block, must be <= 0: T + U <= 10015. With U = .378-.39 pass.
- Layout: the strlen expansion halves the frequency: f7 (the block with `cmp ebx,eax`) = pass/2. It must start in round 2 (f7 >= 2000) or the 6->15 edge (.378 f7 >= 500) extends the trace in
  round 3, and ret0 falls to after the whole tail (that's `or` head's 12 lines). So pass >= 4000. `or` has 3898.
- Upper: bb13 (`xor eax,eax; cmp ebx,netEmpty`) gets an extra .p2align once >= ~500 (pass about 5240), fncmp doesn't see this.
- 6->15's edge probability is inner netSendStr's estimate after threading: .622 fail for `!`, `!= 1`, `== 0`; .475 for `<= 0`. Outer predictors don't lower it, `!= 1` only lowers what comes after 15.
- Window for one test: P(ret) in about [.43,.60], .47 from the bb13 limit unless later tests lower bb13. DS of natural predictors: .61 (.71+.39), .71 (.71), .39 (.39), .5 (none), .488 (.71+.28), .475 (.71+.27).

## Shapes

gen_ns1 (288; head x netSendStr test x send form x scope x check x tail). Best 12, r=2: or|le, or `!` with function-level cmd (gen_ns2 v80): only ret0's position. seq family 13, r=7: layout right, buf in esi.
gen_ns2 (320; nesting of head and send, cmd fn or block, rlen block or flat): same two families. Tail must be `if (ret) return 1; return 0;`, rlen in a block.
gen_ns3 (640; `!`, `!= 1`, `== 0`, `<= 0`, `< 1` on both sends): nothing under 12.

### The flag head: first shape to pass all of it

gen_ns4 (72): `int ok = 0; if (name && buf) ok = 1; if (!ok) return 0;`: the first test has no predictor (the block it guards only sets a flag), P = .5, and the flag test threads away. T = 7500, pass = 5000, f7 = 2500,
MEM(buf) -396. 2 lines left: the sense of `cmp ebx,netEmpty` (edge probs after threading: reference 0/100, this 100/0).
gen_ns5 (180; scope ends x tail x check): `ret = rlen == 2 && getBeU16(r) == OK_REPLY` (as netEraseBlock and netFormatSysex write it) or an if/else: 0 lines in fncmp. `ret = 0; if ...` is the 2 lines.
gen_ns6: all flag spellings the same, `if (!name || !buf) return 0;` 14, `if (name && buf) {` 16.

### fncmp's 0 isn't the end here

fncmp ignores .p2align and jump targets. nssweep's a= now compares the whole .s with the hinted build (labels renamed): that's what counts.
- The ret0 block: compute_alignments aligns a block with a fallthrough only if branch freq > 4 * fallthrough freq (align-loop-iterations; final.c from memory, consistent with nsmargin.py's numbers). `nsmargin.py <gen dir>` prints branch - 4*fall.
  okif + `!netSendStr`: b 6124, f 1555, margin -95. oknest (`if (ok) {`) + `!`: -53. Only `netSendStr(cmd) <= 0` lifts it (U 2046-2469, margin +450..+640).
- The netEmpty test's je must go to `xor eax,eax`, not past it; cmd's scope ending after the tail's `xor` sends it to the epilogue label (visible with a=, not fncmp).
gen_ns7 (42): a=1 for oknest|le|recv (build/ns/gen_ns7/v35.c), oknest|le|str, oknest|le|cmdin, okif|le|cmdin, badif|le|cmdin. So exact text exists: flag + `<= 0`.
gen_ns8 (432; flag head x `!`/`<= 0`/`== 0` x check x tail x where rlen's block starts): all 0 in fncmp, 48 at a=1, every one with `<= 0`. So `<= 0` is needed for the alignment, and it's stable: if/else or expr, 3 tail spellings, several scopes.

## State: landed

src/net.c: flag + `<= 0` + scoped rlen, no attribute, no expect, no asm, laid out like netMkdir (`if (ok) { char cmd[264] = ...; ... } return 0;`).
Full build: SHA256 10dac648... matches. Plain fncmp on src/net.c shows only the `call _netrecv` pair.
Reproduce: python tools/wip/dehint/nssweep.py tools/wip/dehint/gen_ns8.py ; python tools/re/fncmp.py src/net.c netSendFile ; sh build.sh. drafts/net_netSendFile_best.c is src/net.c.

Which trick each piece replaced:
- no-crossjumping: rlen's block ending before the tail (as netWriteBlocks).
- expect and the `buf` pin: the flag. Both only existed to move the head's frequencies: the pin stopped ifcombine (T = 1-P1), the expect set P1.
- the alignment: `<= 0`. Margin +452 against -53 with `!`.

Borderline, for review:
- `int ok = 0; if (name && buf) ok = 1; if (ok) {`: the flag is redundant (`if (name && buf) {` is the same logic, and gives 16 lines). Same form as myatou32's `hex`. Its effect is the predictor: the setting `if` guards no call, so it's 50/50.
- `netSendStr(cmd) <= 0`: netSendStr only returns 0 or 1, as in netWriteBlocks. It's the file's second `<= 0`; the other tests use `!`.
- `ret = rlen == 2 && ...` matches netEraseBlock and netFormatSysex; `if (ret) return 1; return 0; } return 0;` is netMkdir's. Neither is new.

build.sh's comment at line 75 ("netSendFile's !name hint (55-65)") is stale now; left for the user, as build.sh was out of scope.

Next, if anyone wants the `<= 0` gone: margin -53 (oknest + `!`) needs U up by about 90, or P(send fails) down from .622. A second flag on netSendStr would likely do it (its test would guard no call), not tried, as `<= 0` is simpler. Not worth retrying: `||`/`&&` heads without a flag (pass 3898 < 4000), seq heads (T 8918 keeps buf in a register), `!= 1` (lowers only what's after netSendData's block).

## Review (2026-11-10): flag and `<= 0` approved

The user asked for net's four borderline items to be reviewed and settled. gen_nb3 (20; `tools/wip/dehint/nbsweep.py`,
whole object against build/obj/net.o) tried heads without the flag, nested ifs first (the author seems to have favoured
them), each with `<= 0` or `!`:

| Head | `<= 0` | `!` |
|------|--------|-----|
| flag (`if (name && buf) ok = 1; if (ok) {`) | 0 | 2 |
| `if (name && buf) {`, `!= NULL` spelled out, `ok = name && buf;` | 19 | 26 |
| `if (buf) { if (name) {`, `if (name) { if (!buf) return 0;` | 21 | 30 |
| `if (name) { if (buf) {` (with or without `else return 0`), `if (!name) return 0; if (buf) {`, nested with `return ret` | 23 | 32 |

`ok = name && buf;` missing by as much as `&&` confirms the mechanism above: what matters is that the flag is set by
an `if` whose arm holds no call (50%, no call heuristic). Approved: it is the form of myatou32's `hex` and prepSysex's
`r`, both approved. The `<= 0` as netWriteBlocks' review.
