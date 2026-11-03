# net netRecvVerbose (queue 4)

**Current state:** matched, landed with no dead test and no asm (attempt 12, at the end of this file; SHA256 matches,
not committed). The loop's two failure arms assign and rejoin, and a test after each leaves the loop: `size = got;`
then `if (got >= size) return NULL;`, and `status = 0;` then `if (status != 1) break;`, with `if (status != 1) return NULL;`
after the loop. Every test is live, but `size = got` and `status != 1` are there for the bytes, so it's flagged for
the user's review. Attempt 10's `if (!len)` is gone. Older sections' "current" descriptions of `src/net.c` are out of date.

Tools: `tools/wip/dehint/nrsweep.py <gen.py>` (compiles the file, compares netRecvVerbose and the
clone; outputs in build/nr/<gen>/), generators `gen_nr*.py`. NR_DIAG="--param ..." for diagnostics only.

The clone's symbol in the current source is `_netRecvVerbose.constprop.1` (the number varies; not always .0).

## Baseline

src/net.c with hints: `python tools/re/fncmp.py src/net.c netRecvVerbose -O3 --param builtin-expect-probability=65` MATCH.
With no flags (expect at 90): 76 lines, the verbose block trace moved.

## Findings, attempt 1

Tools added: nrdump.py <dir> <src> (dumps + IRA/bbro summary), nrbb.py <dir> (bbro traces with freqs), nrshow.py <dir> est|opt|got, nrwin.py (expect window diagnostic).

Plain source, no hints (gen_nr1): V=22 (verbose block trace after the recv-fail block), C=48 (all registers, size/buf/got = esi/edi/ebx instead of ebx/esi/edi); r=0 on both.

V cause (bb-reorder, round 3 heap): verbose "waiting" block f=253 (29% of 873, PRED_CALL) must beat recv-fail block f=282. The loop freqs are stale and don't follow the first test. Expect diagnostic (nrwin.py): lines match for P(verbose) >= 33% (N<=67); alignment same as reference only at N=64..67 (33-36%), N<=63 adds a .p2align on the verbose size<=0 putchar block.

V fix (gen_nr2): don't raise P, lower the block: PRED_LOOP_EXIT = 9%/n_exits. `r == SOCKET_ERROR || r == 0` folds to one range test in GENERIC (3 loop exits, 3% each); `if ((r = select(...)) == SOCKET_ERROR || r == 0)` has a side effect so it can't fold, stays 2 tests at profile_estimate (4 exits, 2.25%), ifcombine merges them later. **V=0 with no flags, no expect.** Only on the loop's select; on the head select / hdr recv it gives V=26/46+.

C cause (IRA, clone): got must be "6 avail" (caller-saved regs profitable at l0) so it goes in the colorable bucket and pops after size/buf. ira_tune adds call_freq*8 for crossing select+recv in the loop: (f1+f2)/10*8. Test: total MEM - class cost(.2*f2, the `size-got` 2-address tie) > (f1+f2)*.8. Plain: 15237 vs 15287 (asm adds 72, passes). Side select (V=0): 15175 vs 15292, deficit 117: exits before recv lower f2,f3 relative to f1, so the side select hurts C. gen_nr4 asm site diagnostic: `log`/`okstore`/`free` not enough on side, `body` C=0, `afterloop` C=11.
gen_nr3 (324): compare spellings, *len=got, init place, while/for/forinc, r scope: C always 48 when V=0.

gen_nr5 (sign axes, 20): uint32 size/got with casts add copies but break V (100+) and leave an extra cmp in C (5). gen_nr6 (do-while + guard; `if (size > 0) do {...} while`): clone registers RIGHT (log block f up), but log block f=426 pops before recv-fail: V=50, C=24, r=0. gen_nr7 (4th exit): `if (got >= size) break;` at the loop bottom plus the while: C registers right, V=30/C=10 r=0, exit block f doubles (17[415] > 14[215]). `size > 0 && got < size` folds to a single test (no exit added), adds cmov in C.
Layout constraints seen in both functions: select-fail >= verbose block > recv-fail >= short-count join (17), and log (19) must stay below 14 and 17 or it pops early. So raising the log block's frequency can't pay the deficit.

gen_nr8 (`n = got + r; ...; got = n`, `r += got; got = r`): coalesced at SSA, no change.
gen_nr9 (450, sign casts at uses, locals stay int, side select): V=0 always. `(uint32_t)got` in log + unsigned add: C=13, r=5, allocation order right (size ebx, buf esi, got edi) but got's log/exit value becomes its own unsigned pseudo in eax.

gen_nr5's `uint32_t got, int size` (plain select, `(int)got < size`, `got == (uint32_t)size`): clone registers RIGHT with no asm. Extra `cmp ebx,edi` survives (compare not merged by cse_cc, which is also the extra ref of got at IRA), and V is 121. gen_nr10 sweeps cast spellings on uint32_t got.
gen_nr10 (1728, uint32_t got with casts): V never below 109 (signed compare on a cast name defeats loop header copying/threading). Drop it.

gen_nr11 (14): `if (got > size) break;` at the bottom: registers right, C=25 (extra jl), V=32. `if (r == SOCKET_ERROR) break;` with the recv failure after the loop: same bytes as base, the post-loop test is 50%, R block f=291; R and the short-count join share the exit frequency: they sum to 556, and clone order needs R >= 17 with V needing R < 253, so with one select test (3%) this can't satisfy V. `continue` form: no clone.

## State at the end of attempt 1: NO MATCH, best 13 lines

- drafts/net_netRecvVerbose_best.c (gen_nr9): V MATCH, clone 13 lines, no expect, no asm. Allocation order right (size ebx, buf esi, got edi). `if ((r = select(...)) == SOCKET_ERROR || r == 0)`, `got += (uint32_t)r;`, `log_printf(..., (uint32_t)got, size)`. Left: the add result is a separate unsigned pseudo in eax (`add eax,edi; cmp ebx,eax; mov edi,eax`), so xor and log arg differ. That pseudo's back-edge copy is what passes the threshold, and r's eax preference (call return) stops IRA coalescing it. In V it crosses printf, so it isn't eax and V matches.
- drafts/net_netRecvVerbose_side.c (gen_nr2): plain types, only the side-effect select. V MATCH, clone 48 lines (only registers).
Check: python tools/re/fncmp.py <draft> netRecvVerbose -O3 -Isrc ; FNCMP_GCCSYM=_netRecvVerbose.constprop.N python tools/re/fncmp.py <draft> netRecv -O3 -Isrc (N from the .s, not always 0).

The asm can't just be kept with the side select: at the log site it's +72 and the deficit is 117 (gen_nr4).

Next ideas, untested:
- A way to keep the add's unsigned pseudo out of eax in the clone (best draft), e.g. its other tie being stronger: why does tmp thread with r not got? Read ira dump of build/nr/d/v91.
- Any natural ref of got at IRA that is coalesced or dies before output, f>=~290 total on l0 or any one ref in the loop. Types and copies through other variables were tried (gen_nr5/8/9/10).
- Lowering the tied-sub class cost (.2*f2=1868): it applies because `(minus size got)` isn't tied to its dest. Removing it would pay the deficit many times over. No spelling found; `want = size; want -= got` is the same SSA.
- P(verbose) >= 33% instead of side select only moves the deficit from 117 to 50; no predictor combination for 33-36% natural (call 29 needs a 55-58% partner; early return 61 gives 39%, right lines, wrong alignment).
Don't retry: uint32_t got (gen_nr10), do-while + guard (log block pops early, gen_nr6), extra exit at the bottom (join doubles, gen_nr7/11), tail compare spellings/init place/for forms/r scope (gen_nr3).

## Attempt 2

Model of the clone's threshold, from the dumps: refs cost .4f each (add .6f), so with a = exit share before recv, b = recv's
exit, F = f1: deficit ~ F*(.8a + b - ab) - .4*f_pre - .4*f_log. Plain 3 exits a=b=.03; side select a=.045, b=.0225.
Checked: no cmpelim pass exists in this build (-fdump-rtl-all lists none), so a compare left at IRA stays in the output.
best draft's eax: r108 (_25) is live on the exit (log's (uint32_t)got is value-numbered to _25), so it conflicts with got's
pseudo (no non-conflicting-copy logic in 6.2) and no copy forms. `got += (uint32_t)r` alone (log uncast): TER folds it away, C=48.

gen_nr12 (`if (!verbose) continue;` in the loop, PRED_CONTINUE): no effect, only the first verbose test matters. `(uint32_t)got` in the log alone: TER, no ref, C=48.
gen_nr13 (80, do/while x guard spelling x 4 tails x shared fail): in the while form the tail spelling changes nothing (V=0 for all 4); shared `goto fail` is wrong (V=10, C=58, r=6: the reference has 3 separate buf compares). Do forms stay V=50, C=24.
gen_nr14 (10, err/ok flags): errbreak|plain has registers RIGHT with plain select and no cast (C=22, r=6, shared compare again; stale 50% post-loop test raises J/log). okcond: no.
Layout rule, refined from the do form's traces: order is R, then J+log, so log < R and J <= R. In do>0: log = .8*(J+else) = 485 (threader doesn't lower log), else = 323 (guard 73%), f_pre = 1196, V block = 347 > R, D well below 0. So only log is wrong there: lowering P(fail) at `got == size` below ~.48 would fix it.
gen_nr15 (60, do>0 / while x flags, gotos, return variable): `ok = got == size` and `if (!ok) goto` are forwprop'd back to the EQ before profile_estimate, same result. Flags set by an `if` (badflag, flag2): log 436 instead of 485, but V=134 in the do form, V=13-15 in the while form.
gen_nr16 (48, `left = size - got` tests, `got > size`): left-* fold to the EQ (nonequal 72% stays); gt/le leave an extra jump. P(fail) can't go below .72 with a natural test.
gen_nr17 (8, MODEL CHECK ONLY, dead tests, not a shape to land): `got >= size` in the body folds before profile_estimate (no effect). `size - got <= 0` before recv survives to the output in the clone (not dead there), so no use.

### Why the families fail (arithmetic, using the measured freqs)

Needs: V block .29*f_pre > R; log = P(fail)*(J+else) < R; J <= R; deficit <= 0.
- while form, plain: else ~26, f_pre 873: V 253 < R 282. Deficit 50.
- while form, side: V OK, deficit 117. Refs available: log is .4*180 = 72 and log can't rise above R (+19 at most), f_pre is fixed by the exits (conservation), so no natural frequency pays 117.
- do + guard, plain, P(guard) = p: else = 873(1/p-1). V > R needs else > 130; log < R with P(fail) .72 needs else < 122. An 8 gap. p would have to be about .87 (opcode 73 + call 71 = .869, but the else edge's first block isn't a call: both verbose putchars must stay on that path, as the original does them). p = .73 is the only predictor seen on a natural guard.
- Reaching the deficit through a ref: any ref in the exit block (f 921) pays .4*921 = 368, but it must exist at IRA and be gone in the output. Compares can't (no cmpelim, cse_cc merges before IRA), so only a coalesced copy can, and every cast I found is TER'd, or sunk to the log block, or live on the exit and conflicting (best draft).
- Removing the class cost needs size to die at the sub (the alt_cost test in ira-costs is REG_DEAD on the operand, from memory, not re-read); size is live round the loop.

## State at the end of attempt 2: NO MATCH, best still 13 lines

drafts/net_netRecvVerbose_best.c unchanged (V MATCH, clone 13). Closest other shape: plain|do>0 (build/nr/gen_nr6/v1.c): C=24, registers right, r=0, only log+J placed before R; V=50 for the same reason. Reproduce by `python tools/wip/dehint/nrsweep.py tools/wip/dehint/gen_nr6.py`.
nrsweep.py: NR_TOP=n prints n rows (default 20).

Next ideas, untested, low odds:
- A natural guard at P ~ .87 for the do form: closes the 8 gap. Would need else's first block to hold a call without changing V's two putchars.
- A 33-36% first verbose test: partner 55-58% is PRED_CONTINUE's range (hitrate from memory, 56, not re-read). `continue` needs an enclosing loop around the first test; nothing natural found, and it only moves to the plain deficit of 50, which then still needs +50.
- If either lands: a coalesced copy in the log block (+72) would also be needed for the plain while form.
Don't retry (adds to attempt 1's list): tail spellings in the while form (no effect), `(uint32_t)got` alone (TER), `continue` in the loop, shared fail label (3 compares in the original), err/ok flags in the loop, repairing the best draft's eax (r108 conflict is structural).

## Attempt 3: is netRecv its own source function?

Tools: nrsplit.py <gen.py> (netRecv before netFree, no macro, V from drafts/_side.c; N/V lines, r= regs erased), gen_nrs*.py.
No FNCMP_GCCSYM. V stays MATCH in every case: no constant caller left, so no clone, V's code doesn't depend on it.

gen_nrs1: V's text with the verbose tests removed, `static`: N=52, r=0 (registers size/buf/got esi/edi/ebx again, plus store block `*len=size` before the two head-failure blocks instead of last). Non-static: N=67, r=9 (IPA-RA call-clobber differences in callers don't matter here; N differs through inline/frame).
gen_nrs2 (744; loop form x select x recv x tail x decl): best doguard `if (size > 0) do {...} while`: N=22, r=2 registers RIGHT; `u` (uint32_t got): 19, r=3.
gen_nrs3 (384; head select/recv spellings): `r<=0` and side-effect head tests change code (r=5..16). `!r ||` same as plain. Not useful.
gen_nrs4 (24; wrappers over one helper): `inline` helper is inlined EARLY, verbose 0 folds before profile_estimate, so same as gen_nrs1 (N=52). `static inline` helper is not inlined at all (recvReply + its own constprop clone, 144+).
gen_nrs5 (size <= 0 skips the got == size test: nested `if (size > 0) { do..while; if (got == size) {store; return buf;} } log; free; return NULL`, or goto): N=24, r=0, registers RIGHT. J (got == size) P(eq) 19.9% (call heuristic gone: log block has 2 preds, as in the clone) and guard 86.9% (opcode 73 + call 71). Left: log block f 358 > R 291, J 282, pops early.
gen_nrs6: `if (size > 0) do..while; if (size <= 0 || got != size) {log...; return NULL;} store`: N=14, r=0 registers right. Non-short-circuit OR: P(fail) 29% (call only), J falls through to store rather than log. Polarity is the problem. goto_ok form: N=24, P(eq) 28%, log 335.
Layout model (own function), order R, J+log, W, W, store needs: log < J and log < R; J->log edge >= 5% entry (exec_th, round 3); store < W (~.04 entry). Registers need f_pre + f_log >= ~.1325*F (deficit = .053F - .4(f_pre+f_log)). While form: else 26, f_pre 873 too low (deficit 74). Nested do: f_pre 1005 OK if log <= 282, needs else <= ~52 i.e. guard >= 95% (have 86.9).
gen_nrs7 (24; store inside loop, nested while, redundant `size > 0 &&`): best do_and|side, saved as drafts/net_netRecv_own_best.c: `if (size > 0) do {...} while (got < size); if (size > 0 && got == size) {store; return buf;} log...`, side select: N=8, r=2, registers right, J falls through to store instead of log (P(store) 61%). `if (got && got == size)` while form: N=9 but a real extra test stays. Store inside the loop: extra je in the loop, N=24.
gen_nrs8 (48; ret variable, goto out, nested): no better than 22.

### Evidence: clone or separate function? Clone.

For a clone:
- Every other function in the object is public (`T` in nm), even those used only here (netCheckOk, netSendStr, netOpenSocket, netReadInfo, netClose...): the author doesn't write `static` in net.c. netRecv alone uses the local-function convention: `len` in eax (`lea eax,[esp+28]; call 41e800`, `mov edx,eax` on entry), 13 call sites. V takes stack args. A public own netRecv can't match (gen_nrs1: N=67, r=9). A hand-written netRecv would have to be the file's only `static`; a gcc clone is local by construction.
- Position: netRecv is first in .text, at 0x41e800, before netFree, with V in the middle at 0x41ee30. gcc emits the clone first with no help; a source function would have to be the file's first, far from its twin.
- Layout: the clone's frequencies give the reference's block order with no help in the plain form (r=0, only registers). store 45 < W 96 because V's `if (verbose) putchar` block between J and log removes the call heuristic and the else share. An own function has to reproduce those stale numbers from nothing, and the model below says it can't.
Neutral: .rdata (shared strings at netRecv's position, V-only ones at V's): same for both. Both verbose callers pass `log_get_verbose() != 0`, all 13 netRecv calls are in net.
Linux xeBuild64: no net strings ("waiting for 0x", "timeout waiting for data" both 0 hits; no such code in v1.16), no cross-check possible. Upstream cOzInABox/XeBuild tree (read in full via the GitHub API): no net/recv/socket/client path, no xeBuild app source. tmp/dashlaunch: no match.
Task's other ideas refuted by the binary: verbose as global/static: callers pass it as stack arg (`movzx eax,al; mov [esp+4],eax`). V as thin wrapper: V at 41ee30 holds the whole body, no call. Wrappers over a helper: gen_nrs4 (`inline` folds early, `static inline` isn't inlined).

### Why the own-function family fails (nested do, the best family; F=10000)
Let p = guard, P(eq) at J. f_pre = 873/p, else = 873(1-p)/p, J 282, R 291, W ~115. Need log = (1-P(eq))*282 + else <= 282, store = P(eq)*282 < 115, f_pre + log >= 1325 (registers). From store: P(eq) < .41, so log's J share >= 167, so else <= 115, so p >= .884, so f_pre + log <= 987 + 282 = 1269: short by 56 refs freq, .4*56 = 22 cost. Natural predictor values miss by more: p=.869,P(eq)=.378: log 307 > J by 25; p=.912 (no such guard found): registers short by 44. While form: f_pre 873 + log <= 274 against 1285: short by 55 in cost, always.

## State at the end of attempt 3: NO MATCH
Clone best still 13 (drafts/net_netRecvVerbose_best.c). Own-function best 8 (drafts/net_netRecv_own_best.c, plain types but side select and a redundant `size > 0 &&`), though the evidence says the original isn't that shape.
Reproduce: python tools/wip/dehint/nrsplit.py tools/wip/dehint/gen_nrs7.py ; python tools/re/fncmp.py tools/wip/dehint/drafts/net_netRecv_own_best.c netRecv -O3 -Isrc . nrtr.py <src.c> prints traces and predictions.
Next (low odds): a natural got ref in the log block, worth .4*f_log (~110), would close either family; nothing found that isn't TER'd or left in the output. Otherwise this needs the user's ruling: keep expect+asm (hints) in src/net.c.
Don't retry: public netRecv, wrappers over helper, global verbose, head spellings (gen_nrs3), single-return styles (gen_nrs8), store in the loop.

## Attempt 4

Tools: nrtpl.py (template with one axis per piece of C, DEF has the side select), nrcost.py <src.c>... (clone's MEM/class cost and disposition per pseudo), nrhead.txt/nrbody.txt (function head and loop body for gen_nr23). Generators gen_nr20-.

How the reference's registers come about, read from the hinted build's IRA dump (not a guess; `Spilling a7r137 for a1r109` in the dump): got is pushed early because 6 regs are profitable, is popped last, is given edx (reg 1) by colouring, then improve_allocation spills r137 (&tv, rematerialised as `lea eax,[esp+52]`) and gives got its edi. Pop order is then size ebx, buf esi, r137 edi, r138 (&fds) ebp. In the colorable bucket the order is ascending thread freq, and got (~4700) always beats size and buf, so only the caller-save profitability test can change it. No hard-reg preference is available in plain C to steer got off ebx directly.

The test, exact: got's MEM - class > 8*call_freq. Side draft: MEM 17043, class 1868 (= 2*f2/10, alt_cost on the `sub`, because size doesn't die there; it's charged to all the insn's operands), threshold .8(f1+f2) = 15292. Deficit 117. (alt_cost's mechanism is from memory of ira-costs.c, not re-read; predict.def fetch got HTTP 429, predictor rates here are from the dumps.)

### New: the flip fixes V with no side select (real progress)

gen_nr25 (16): `if (size) { calloc...; loop...; if (got == size) {store; return buf;} log...; return NULL; } *len = 0; return &netEmpty;`: **V MATCH with the plain select**, no side effect in the condition, no cast. drafts/net_netRecvVerbose_flip.c; clone 48, registers only (r=0). So the side select isn't needed, and the clone's deficit goes from 117 back to plain's 50 (MEM 17117, class 1880, threshold 15287).
Why, from the traces (V's: `nrbb.py <dir> 'netRecvVerbose ('`; note plain `netRecvVerbose` matches the clone first, because it's a prefix): `if (size)` loses the early-return prediction (61%) and takes the call heuristic (29%), so bb 7's successor keeps its freq but the entry freq goes 2533 -> 3405. bbro's round thresholds scale with the entry freq, so the block before the verbose test no longer extends into a trace in round 2; the non-verbose loop and the verbose loop start in round 3 in the right order. So the earlier "f_pre is fixed, so upstream exits don't matter" is true for the IRA deficit (clone freqs in the loop are identical) but **wrong for bbro**: the entry freq is a separate lever on layout. The other flips (one shared `*len = size` with buf defaulting to &netEmpty: share_ne, share_eq, else) are V=26, C=51: separate store blocks are in the reference, so it isn't one shared store. `flip|side` is C=52, V=0.
gen_nr26 (216; flip x loop form x tail x outer spelling x zero arm x select): only `while` keeps V=0. Tail, `if (size)` vs `if (size != 0)`, `*len = 0` vs `*len = size` change nothing. Dropping the zero store is wrong (no `mov [eax],0`). do>0 is worse with the flip (V=52, C=44, r=2; see gen_nr28), bottom `got >= size` V=137, C=10, `got > size` V=36, C=29 and only without the zero store.
gen_nr28 (30; head shapes moving the entry freq x while/do>0/nested while x tail): flip and `if (size != -1) { if (size) {...} zero } return NULL` give V=0, C=48. `if (size == 0) {zero} else {...}` is the same as base (V=22; do>0 V=50, C=24): an else arm doesn't take the call heuristic the way `if (size)` does, so entry freq alone decides V. Others are worse. No shape moved log or J in the do family.
gen_nr27 (144; flip, plain select x gen_nr9's cast axes): V=0 with C=13 for the cast pair `got += (uint32_t)r` + `(uint32_t)got` in the log, same 13 lines as before, no side select needed. Saved as the new drafts/net_netRecvVerbose_best.c. Other casts C=48.

### The task's ideas, tested

gen_nr24 (1080; select x tail x remainder/pointer local x advance x head):
- Tails with got (`*len = got`, `size = got; *len = size`): no change to C.
- `left` (body-scoped or not), `p`, both: V and C unchanged, so no new ref at IRA. Not run: the same locals computed before the select. It would pay (refs at f1, about .6*a*F), but I expect the tree sink pass to move them back, and if it didn't, the output would differ from the reference, which computes them after the select.
- `if (r != 0) got += r`, `got = got + r`: same as base. `if (r > 0) got += r`: C=4 (registers RIGHT, `lea ecx,[eax+edi]; test eax,eax; cmovg edi,ecx` instead of `add edi,eax`), V=96. A real test that can't fold, and it's what pays the threshold, so not usable.
- `r < 0`, `r <= 0` for the recv failure: real compare differs, V=28 (side) or 50 (plain), C=52.
- Head (side / plain, one-axis rows from nr24check.py): `if (!size) *len = size`, `buf = &netEmpty` default before the zero test: no change. Combined `size == -1 || size == 0`: V=68/86, C=86/42 with r=8/6. Zero-first: V=28, C=77/73. calloc check: V=2/24, C=50, r=2: the reference has none (`call _calloc; test ebx,ebx`), a real test stays.
- `if (got != size)` log first: gen_nr23 and gen_nr26, no effect in the while form.

### Other families

gen_nr20 (16; int vs long splits, `n = got + r; got = n` with n another type): got's init becomes its own pseudo (r111, `got_32 = PHI <0>`), got keeps the rest, MEM falls. C=48, V=3..23. Plain `long` anywhere: no effect.
gen_nr21 (60; a carrier `total` of another type into the log block): the copy just replaces log's ref of got at the same freq, so it pays nothing (MEM 17011, down from 17043), and V is 62+ with the unsigned types. `long` is propagated away. Every carrier has this problem: a copy only pays if got also keeps its own ref there.
gen_nr22 (84; `if (verbose) putchar` as a static or static inline helper at any of the 3 sites, while/do, select): the helper is early-inlined, results same as no helper. So no call in the guard's else block at profile_estimate; p=.869 isn't reachable this way.
gen_nr23 (64; do family with `if (size <= 0) goto done;` and other guards x tails): C has no goto predictor (guard still 73%), do-family V=50+, C=24.

### Arithmetic for what's left (flip, while, plain; F=9700)

Pay 50: f_pre + f_log must go up by 125. Log can rise only from 240 to R=282 (+17 cost). With else raised by a guard, while P(fail) .72 (`got != size`-style tail isn't lower, the dump shows 72 at best): the window is else in about [113,117], guard p about .883. Available guards: .73 (opcode positive), .869 (needs a call in the else block, which can't exist, see gen_nr22), .97 (while). At .869: log 298 > R 291, 7 over. So the do family misses again, narrowly, even though the flip removes its V > R constraint.

## State at the end of attempt 4: NO MATCH, best 13 lines

drafts/net_netRecvVerbose_best.c: flip + plain select + cast pair. V MATCH, clone 13 lines, the same eax difference as before.
drafts/net_netRecvVerbose_flip.c: flip + plain select, no casts. V MATCH, clone 48 lines, registers only. The most natural source so far, and short by 50 cost.
Reproduce: python tools/wip/dehint/nrsweep.py tools/wip/dehint/gen_nr27.py ; python tools/re/fncmp.py tools/wip/dehint/drafts/net_netRecvVerbose_best.c netRecvVerbose -O3 -Isrc ; FNCMP_GCCSYM=_netRecvVerbose.constprop.1 python tools/re/fncmp.py tools/wip/dehint/drafts/net_netRecvVerbose_best.c netRecv -O3 -Isrc
Next, in order of odds:
1. A guard between .86 and .885, or a tail with P(fail) under .70, for the do family. Note the flip itself pushes do>0 to C=44, so this also needs a flip that keeps the base do's C=24 layout while still fixing V; flip4 keeps C=24 but loses the V fix.
2. Any natural got ref worth 50 in the plain flip: this is the same open question as before, but it's now 50 and not 117.
3. The user's ruling: the flip with the existing `__asm__ ("" : : "g"(got));` before the log call gives MATCH on both V and the clone with no flags, and no expect, no --param and no side select (checked with fncmp; not landed, no full build). It keeps a hint, so it isn't a queue MATCH, but it does cut this function's hints to that one asm. To rebuild it: add that line above the log call in drafts/net_netRecvVerbose_flip.c.
Don't retry: carriers into the log block (gen_nr21), int/long splits (gen_nr20), newline helpers (gen_nr22), goto guards (gen_nr23), remainder/pointer locals, tails in the while form, `if (r > 0)` (real test).

## Attempt 5

Tools: nrdef.py <gen.py> (V, C and the clone's measured margin per variant, grouped by result), nrflip.py (base text: src/net.c minus the asm, plus the strings generators replace), nrrtl.py <src.c> [regex] (the clone's GIMPLE and got's insns at expand, fwprop1, IRA, with costs). Generators gen_nr30-34.

Deficit measured, not estimated: flip MEM 17117, class 1880, f1 9700, f2 9409, threshold .8(f1+f2) = 15287, margin -50. With the asm MEM is 17189, margin +22. The asm is worth 72, not 96: a "g" operand allows memory, and ira-costs takes 1 off the move cost for that, so .3f at log's 240. A plain (set mem got) is .4f. Own (non-loop) MEM of got: 440, the rest (16677) is the l1 region. got's refs: inits 847 + 26 (.4 each, two PHI edges), lea and sub at f2, add and cmp at f3, store 60 and log 240. The store uses got, not size (DOM swaps it after `got == size`), so P(eq) is irrelevant to MEM: log + store = J + else whatever the split.

### The task's angles, tested

Angle 2 (verbose-only structure, gen_nr31, 168): tail spellings (block, nested, `got != size` first, printf newlines, else), loop printf (block, `!verbose continue`, block + continue), waiting printf (got first, block), recv-fail newline (block). **108 of them are V=0 with MEM exactly 17117**, frequencies unchanged. `!verbose continue` V=16, MEM same. `nested` V=15, C=52, MEM 17093 (lower). Why: a verbose test that isn't a loop exit rejoins, so flow is conserved at every block the clone keeps. Non-exit verbose structure can't move the clone's costs.

**The stale lever is real, but only for exits** (gen_nr33, model check, not natural): `if (verbose) { printf(...); if (got >= size) break; }` adds an exit edge only on the verbose path. n_exits goes to 4 (e = .0225), the clone loses the edge but keeps the frequencies: MEM 17373, class 1910, f 9775/9555, margin -1, and the clone's **registers are all right**, C=10, only the J+log trace before R (J 270 > R 215, the verbose exit lands in J). V=67 though (`r=9`). gen_nr34 gave the exit its own destination (`goto check` past the first newline, `goto nl`, `nl-break`, own tail, each with plain and side select): V=67..130, C=10 at best. Even with J fixed, log stays above R (229 > 215 in the trace), because the verbose exit's flow still reaches it. A redundant `got >= size` test inside `if (verbose)` isn't something anyone would write, and V is far off, so no candidate came of this.

Angle 1 (log block, gen_nr32): scoped int copy, `const char *fmt`, `(int)(uint32_t)got`, `(long)`, carrier across the newline: MEM 17117, no ref added (carrier V=2). Scoped `uint32_t n`, `(uint32_t)got`, `(unsigned long)got`: MEM 17076, 41 lower. The nrrtl.py dump of `(uint32_t)got` shows why: PRE makes `prephitmp = PHI <(uint)got, 0>`, so the log uses its own pseudo, got's log ref becomes a copy on the J edge (insn 166), and got loses the else init. The copy replaces refs and adds none. Attempt 1's "single cast" vs "pair": the pair only differs because the add's unsigned temp then has two uses (add's conversion + log, value-numbered together), so TER can't fold it. That's what pays 809 in the best draft, and that same log use keeps it live on the exit and conflicting, so it can't share got's register.

Angle 3 (exits): the sum is what matters. With F0 = 10000, deficit is about .6e*F0 when a=b=x=e, so lowering loop frequency relative to the pre-loop refs means more exits or a higher x, and layout needs a >= b >= x. Exit forms in gen_nr32: `!r ||`, `r == 0 ||` same as base; `r <= 0` a real compare (V=30, C=53). Re-measured: no natural exit form changes f1 or f2 from 9700/9409. A higher else (guard) only pays .72 per unit; needs guard about .90 (else 90) and log <= R, predictors available .73, .869 (needs a call in the else block, gen_nr22), .97. Null return (.90) combines with opcode positive to .96. So attempt 4's arithmetic stands after the flip.

Angle 4 (class cost, gen_nr30, gen_nr32): `uint32_t want = size; want -= got;` and `uint32_t n = got; n += r; got = n;` do what they were meant to at expand: a same-root name (`want_1` used by a stmt defining `want_2`) isn't TER'd, and a two-use conversion (`off`, `got.9_20` for buf+ and size-) stays as a real (set r got). But **fwprop1 and cprop remove them all before IRA**: nrrtl.py on build/nr/gen_nr30/v6.c shows insn 128 (set r103 got) at expand and gone at fwprop1, with (minus size got) back. All variants: V=0, C=48, MEM 17117, class 1880. So size can't be made to die at the sub with a same-mode copy, and got can't get an extra read through one either.

### Why a natural ref can't exist (the mechanism)

To pay 50 without changing the output, IRA must see an extra got ref that's gone in the output. What can do that:
- A copy that fwprop/cprop can't propagate: only if the destination keeps a value got no longer holds, i.e. the back-edge form (tmp = got + r; got = (int)tmp). TER folds that unless tmp has a second use. The second use has to be before the copy and in the clone. The only such use in the code is the verbose printf, which the clone removes, so TER folds it in the clone. A use after the copy (log, store, the J compare) is live on the exit, and IRA 6.2 has no non-conflicting-copy logic, so tmp conflicts with got (best draft, 13 lines).
- TER kills: same_root_var needs one variable on both sides, which a type change rules out; kill_expr needs r or got redefined between the add and the copy, nothing natural does that. (Both from memory of tree-ssa-ter.c, consistent with the dumps, not re-read.)
- A second compare removed after IRA: no cmpelim here; reload-cse's no-op set test needs same CC mode and no label, and cse_cc would have merged that case before IRA anyway.
- Lower spill priority for got so it pops after size and buf with 3 avail: needs got's cost (15237) under buf's (6911) scale. No.

## State at the end of attempt 5: NO MATCH without the asm

src/net.c unchanged (flip + asm: both MATCH, SHA matches, one hint left). Best with no hint: drafts/net_netRecvVerbose_best.c, V MATCH, clone 13 lines. Most natural: drafts/net_netRecvVerbose_flip.c, V MATCH, clone 48, margin -50.
Reproduce: python tools/wip/dehint/nrdef.py tools/wip/dehint/gen_nr32.py ; python tools/wip/dehint/nrdef.py tools/wip/dehint/gen_nr33.py ; python tools/wip/dehint/nrrtl.py build/nr/gen_nr30/v6.c 'got|want|_12'
Next, low odds: a natural exit that exists at profile_estimate and later goes away in both versions (stale exit sum, the one lever that moved the margin). It has to land away from J and log, or the clone's R order breaks. Nothing natural known. Otherwise this is the user's call: keep the asm.
Don't retry: verbose tests that aren't exits (no effect, gen_nr31), named or two-use conversions at the sub or add (fwprop, gen_nr30), log-block copies and casts (gen_nr32), verbose-only exits as written (gen_nr33/34: V=67+).

## Attempt 6: reuse of one C variable

Partition map (`-fdump-rtl-expand-details`, the clone of the flip): r_3, r_8, r_15, r_24 are all separate partitions, and the "Coalesce list" has only PHI/copy pairs (got_26/34/32/79; _27/_31/buf_14). So in this gcc, with -ftree-coalesce-vars on, sharing a base variable alone does NOT merge SSA names; the same-base merge is what -fno-tree-coalesce-vars does. A plain reuse needs a PHI or a copy connecting the names.
gen_nr40 (300; hs/hr/ls/lr roles over r, got, size, n, m, k, decl order, `got = 0` at the declaration with/without the later set): **all V=0 C=48 r=0**. Where got holds a head result, that's its own pseudo and got's margin line in nrdef reads that first pseudo (MEM 2289/2380), the loop's pseudo is unchanged. `int got = 0` is const-propped: same.
gen_nr41 (20; got read in a shared exit, flags on the flip): `got = 0; buf = &netEmpty; if (size) {...; if (got != size) {fail}} *len = got; return buf;` V=6 (r=2), C=51 (r=3), MEM 17105 (-62): one shared store is real in the output (the reference has `mov [eax],0` and a separate store of size/got), zero path's got=0 is constant-propagated, no ref. `nest` (only the zero arm's `got = 0; *len = got`), `head-got`: same bytes as the flip, cprop. Flags on the flip: break-tail|err V=26 C=22 margin -6: shared compare (reference has 3); cont-cond V=215+.
gen_nr42 (100; size through r: `r = getBeU32(hdr); ...; size = r` and others, buf through ret/ptr locals, r on verbose paths: `r = got; printf(.., r, ..)`, `r += got; got = r`, `r = got` before the log): 80 are V=0 C=48 MEM 17117, identical to the flip. `void *p = calloc(); buf = p` V=130, C=68, same MEM. Copies are propagated, so no pseudo changes.
Not swept: scope and parameter forms for merging. They were only to be tried if reuse showed promise. It can't: a nested `int r` is just another base variable, and gen_nr40's distinct-name rows already give identical bytes.

**General note for the queue:** reusing a C variable doesn't change the code in gcc 6.2 at -O3, unless the names are joined by a PHI or a surviving copy. Only those pairs are on the coalesce list. Unconnected webs of one variable stay separate pseudos, so a reuse sweep isn't worth running to change allocation. Check with `-fdump-rtl-expand-details` ("Coalesce list", "Partition map"; the map is printed per function, so find the clone's section).

### The margin, as a formula, and what it rules out

With H the loop header (10000) and exit shares a (select), b (recv), x (tail): margin/H is about .8x + .4*else/H - .4a - .6b. Plain a=b=x=.03 gives -60 + 10 = -50, as measured. So tail exits pay and recv exits cost most, but a second tail exit doubles J (J > R breaks the clone's layout, gen_nr7/11), and with x <= b the best natural mix would be a=e, b=2e, x=2e, n=5, which needs tests no one writes and comes to about 0. else pays .4 per unit, but log then passes R (attempt 4's window). PRED_LOOP_EXIT is first match on all 3 exits (profile_estimate dump: "first match heuristics: 3.0%", others ignored), so no other predictor on the exit blocks can shift a or b; only n_exits can.

### Another way to the same registers, looked at and dropped

IRA dump of the flip's clone: r111, r136, r139, r137 are pushed as potential spills, then r138, buf, size, got go colorable together and are pushed in ascending cost, so got pops first (ebx). If got went colorable alone, one step before size and buf, it would pop later: that needs got to have one conflict fewer than they do, or one more profitable reg.
- Conflicts: got's are the same long-lived set as size's and buf's (len, the recv and select pointers, &tv, &fds), all live over the whole loop. A pseudo that conflicts with size and buf but not got would have to cross a call outside the loop, and the output has no such pseudo (its only stack slots are 0x24, 0x28, 0x2c, already these).
- Profitable reg: a hard-reg preference on got (eax, from `(set got eax)`) could add one, but head results in got are their own pseudo (gen_nr40), so nothing natural gives got that copy.
- Thread freq order (from memory of the bucket sort; the dump only shows the push order): got would have to rank below size and buf, and it has 5 refs in the loop against size's 2.

### What can't reach IRA as a got ref, added to attempt 5's list

- J's compare (insn 163, +113 if it lived) is at expand and gone at IRA, removed by cse_cc. Nothing after IRA could remove it instead (no cmpelim, as attempt 2 found).
- A PHI-joined carrier with a type change needs its second use on the path in the clone before the copy; with a signed `got < size` compare the conversion comes first, so the name is shared and TER folds. Not compiled: reasoned from attempt 5's TER findings.

## State at the end of attempt 6: NO MATCH without the asm

src/net.c unchanged (flip + asm). Best with no hint is still drafts/net_netRecvVerbose_best.c (V MATCH, clone 13 lines). Most natural is still drafts/net_netRecvVerbose_flip.c (V MATCH, clone 48, margin -50). No new candidate.
Reproduce: python tools/wip/dehint/nrdef.py tools/wip/dehint/gen_nr40.py (also gen_nr41.py, gen_nr42.py).
Next: nothing with real odds. This is the user's call: keep the one asm, or accept the 13-line or 48-line state. If anyone retries, the only unexplored kind of source is one that changes loop exits at profile_estimate and then folds away in both V and the clone, with x <= b.
Don't retry: variable reuse in any role (gen_nr40, gen_nr42), got in a shared exit (gen_nr41: real extra store merge, or cprop), flags on the flip (shared compare), `void *p` calloc carrier.

## Attempt 7: helpers that inline late

Tools: gen_nr50-, nrpass.py <src.c> (the clone's select/recv/R/log/add block freqs after each GIMPLE pass).

**The margin moved for the first time with plain code.** gen_nr50 `none|both|logeq` (build/nr/gen_nr50/v3.c): `static int netRecvSome(char *p, int n, uint32_t verbose)` holding recv, the test, the newline and the log, `return SOCKET_ERROR` on failure, `return r` otherwise; caller `r = netRecvSome(...); if (r == SOCKET_ERROR) { free; return NULL; }`. Not early-inlined (growth 14 > early-inlining-insns divided by calls), inlined at IPA. Margin +58 (MEM 17225), **clone registers right, C=10** (r=0), V=22 (r=0). Left: only R's position; R's block 150 < J 274, so J+log come first. Why: the helper's `return -1` gives negative return 4%, with opcode .28 it's 1.6%, and that's the helper's estimate: after inlining R's block starts with the helper's fail block (150) and the ok block (9259 instead of 9127) merges with the add. A merged block keeps the first block's freq, so the stale values survive. margin = f3 - .2f2 - .8f1 + .4(f_pre + f_log) + ~20.

Mechanism, read from nrpass.py and the dumps (`a.c.082t.fixup_cfg4` for the clone after IPA):
- Whether a helper is early-inlined: `-fdump-tree-einline-details`, "will not early inline ... growth N exceeds --param early-inlining-insns divided by number of calls". recv + test + newline: growth 9, not inlined, but small forms taken at 56's size are (then the caller's estimate sees opcode .28 on the helper's test, plus X's exit 3%).
- After inlining, freqs are propagated from the edge probabilities (the helper's and the caller's stay as they were estimated). Then vrp1 threads the fail and ok edges through the caller's test X. R's block merges with what's before it and keeps the first freq, so R = P(helper fail) * f2 and f3 = (1 - P) * f2 (if the add is in the ok path's first block). X's own 3% is gone. So exit shares can be set by the helper's predictors. That's why log-in-caller doesn't keep R at 282: R merges with X's threaded copy, at the threaded edge's freq.
- P values available for `r == -1`: opcode .28 always; with `return -1`/SOCKET_ERROR negative return .04: **.016**; with a call first in the fail block .29 too; without the negative return .131. phiopt folds PHI<0,1> and PHI<-1,r> where the fail block is empty (verbose 0 helper clone: `return -1` with `return r` is a no-op, so log has to be in the helper for the branch to survive in the clone). PHI<-1,0> isn't folded but needs a status return and a pointer; `int *got` makes got memory at estimate, and the two latches then become nested loops (n = 4 at e = 2.25%, entry 2573 so the flip's V fix is lost: gen_nr54, V=138, C=10, margin +13).

gen_nr58: fail helper `netRecvFail(buf)`: early-inlined, no effect. Side select + recv helper: margin -63, V=16, C=64. `static` whole `if (size)` arm: not inlined once V and the clone both call it. `static inline` arm: inlined, margin -50 as plain, V=72, C=50.
gen_nr59: loop in a helper returning got or -1: `got < 0` stays as a real test (js), V=61, C=27.
**gen_nr60: loop in `static int netRecvBody(buf, size, verbose, fds, tv, int *total)`, frees in the helper, returns a status, `if (!netRecvBody(...)) return NULL;`: inlined at IPA, every status test threads away, r=(0,0) with the clone's registers RIGHT, margin +102, frequencies in the loop as plain, V=16, C=44.** Only layout left. Why the margin moved: after threading the empty copies of the status test X are removed as forwarders, so J keeps its own freq, which is P(ok at X) * X and X is the sum of all exit flows (847+): J 760, log 629 instead of 274/240, worth .4 per unit on got's log ref. Why layout breaks: J 760 is round 2, so it comes before R 282. Needs J <= R (282), which means P(ok at X) <= .33; log can stay high only if it has flow not through J.

gen_nr61: `status = netRecvBody(...); if (status == 1 && got == size) {store; return buf;} if (status != 1) return NULL; newline; log; free; return NULL;` (newline after the loop inside the helper; v16): r=0, registers right, margin +110, and **J 274 <= R 282 as the reference wants**. Log own freq 641 pops before R. C=24, V=38. The else edge goes straight to log, as in the reference (`jmp 0x41e9e2`, past the `je`), which fncmp's label erasure can't show; so log is in the heap as soon as the loop's trace is done, and must be < R.
Exact: margin = -50 + .4*(log + store - 300) in this family. Layout: log <= R (282), store <= 129 (the reference puts it after the head failures 134, 129). So at most log + store = 411, 14 short of the 425 needed: 5.6 cost short, with R at 282.

gen_nr62 (82; two status conventions x spellings x 5 tail orders x recv helper): best no-recv-helper shapes V=16, C=24, r=(0,0), registers right. All the status family have margin +30..+262 with no real extra test (tail `e` adds real tests, r=8).
Family numbers (clone, block freqs): `c` (nested `if (status == 1) { if (got == size) {...} newline; log; free } return NULL;`, v32, the most natural): J 653, log 544, R 282, store 135. `a` with `status == 1 &&` (v28): J 274, log 641, R 282, store 49. `a` with `status &&` (v50): J 411, log 612, store 87. With the recv helper R is 150 and everything else is the same. J keeps its own freq because the threaded copy of X is a forwarder there (same loop depth). For R the copy is on a loop exit, so it's kept and R merges into it: that's why R can't keep its own freq.

### Where it stands (why I stopped)

The margin is no longer the problem: helpers move it from -73 to +262 with no extra test in the output (+581 with a real one), and both the recv helper and the loop helper put got in edi. What's left in every one is the order of R, J and log, and these are now tied together:
- Reference order is R, J+log. log is in the heap as soon as the loop's trace is done (the else edge jumps straight to it), so log <= J <= R, all below 681 (round 2) and R >= 170 for round 3; store must stay under the head failures (<= 129).
- No helper on recv: R = 282, so log + store <= 282 + 129 = 411. Needed: ~415 (shape a, margin = -46 + .4*(log + store - 300)). Short by about 2 cost even at the extremes, and in practice store = .2*J, so log + store is about 330 (margin about -34). Stale log (the only thing that pays here) is what breaks the order.
- With the recv helper: margin is paid by f3 (+58), R = 150, so J and log must be <= 150. J's own freq is P(X->J)*X with X about 740: needs P <= .2. Seen on natural status tests: .33, .5, .77. J in the plain shape is 274 (tail exit), R 150: gap 124.
- R's share can't be chosen: for `r == -1`, opcode .28 is always there, so P is .016 (negative return), .28 (none) or .131 (a call first in the fail block, but the verbose test is first). The window needs .029..0.072 with f3 not lowered; nothing gives it.

Not hints but borderline: `return 2` from netWait (gen_nr57 `0,2|hlog|both|logeq`, v51, V=12, C=8): the head and loop fail paths through one helper, r=0, swaps R and the head's failure. A status of 2 with nothing else meaning anything is there only because phiopt folds 0/1. Not saved as a candidate: not a match anyway.

## State at the end of attempt 7: NO MATCH without the asm

src/net.c unchanged (flip + asm). Line counts, no flags (V, clone):
- drafts/net_netRecvVerbose_best.c (flip + cast pair): 0, 13. Still the lowest total. Clone registers off in one pseudo.
- drafts/net_netRecvVerbose_recvhelper.c (gen_nr50 v3, netRecvSome with recv, newline, log): 22, 10. All registers right, in both; only R's position.
- drafts/net_netRecvVerbose_loophelper.c (gen_nr62 v32, netRecvBody + status): 16, 24. All registers right; only J+log vs R and store.
- drafts/net_netRecvVerbose_flip.c: 0, 48.
Reproduce: python tools/re/fncmp.py <draft> netRecvVerbose -O3 -Isrc ; FNCMP_GCCSYM=_netRecvVerbose.constprop.1 python tools/re/fncmp.py <draft> netRecv -O3 -Isrc ; python tools/wip/dehint/nrdef.py tools/wip/dehint/gen_nr50.py (also 57, 58, 59, 60, 61, 62); python tools/wip/dehint/nrpass.py <src.c>; python tools/wip/dehint/nrbb.py build/nr/tr/<dir> 'netRecvVerbose.constprop'.
Next: only with a new way to set R, J, log independently. Candidates, low odds: a natural predictor giving P(X->J) <= .2 on the status test for the recv-helper + loop-helper combination; anything that keeps the else edge off log until J is placed. Otherwise the user's call: keep the one asm.
Don't retry: fail helper (early-inlined), whole-arm helper (static: not inlined; static inline: same freqs as plain), `got < 0` return from a loop helper (real js stays), pointer to got in a recv helper (nested loops, entry 2573, V=138), status with out param for recv only (phiopt or early inline, margin -50), netWait in any spelling (f2 up, f3 fixed: margin -73, loop rotates).

## Attempt 8: constraints re-read from the source, then a tail helper

Read from the official repo at releases/gcc-6.2.0: ira-color.c. (Saved in the session's scratchpad only.)

### The constraints themselves

bbro (hinted src/net.c vs recv helper, `nrbb.py build/nr/tr/<dir> 'netRecvVerbose.constprop'`). The first decision that differs is in round 3: the hinted build gets bb 14 (R 282) then 17 (J 274) + 19 (log 240); the recv helper gets 10, then 15 (J) + 17 (log), and R (150) is below round 3's threshold (5% of 3405 = 170), so it goes to round 4.
- `log <= J` is NOT required. If log > J, log starts its own trace, J gets a later one, and connect_traces' predecessor search still places J before log, so the output is the same. Required is only R >= J and R >= log (R has to start its trace first), and store <= the lower head failure. Attempt 7's "log <= J <= R" was too strong, though its margin arithmetic used log <= R anyway.
- A block whose predecessor ends a trace gets priority in the heap (bb_to_key, from memory of bb-reorder.c, consistent with 10 being popped first). R's and J's predecessors are mid-trace (recv, add) in the reference's loop rotation, so R has no way to jump the queue.

IRA (ira-color.c bucket_allocno_compare_func): the colorable bucket sorts by thread_freq first, and threads form over any copy (including `shuffle`, an operand dying into an output). Popping size, buf, got, r138 in that order would also give the reference's registers without passing the caller-save test. That needs thread(size) > thread(buf) > thread(got) (got's freq about 4700, size about 2100, buf about 1400): a loop-frequency partner for size and buf through a copy. None exists: their operands don't die in the loop, and head copies are low frequency. Dropped.

### New family: a shared tail after the transfer (gen_nr70)

`buf = &netEmpty; got = 0; if (size) {...loop...; newline} if (got == size) {store; return buf;} newline; log; free; return NULL` explains why buf != &netEmpty exists at all, and has margin +634 with registers right, but it isn't the reference: one shared store (no `mov [eax],0`), and J 1953 stale from the zero path. V=28, C=47. Don't retry; the separate `*len = 0` store is real.

### New family: tail in a helper above the early-inline limit, do form (gen_nr71-74)

`if (size > 0) do {...} while (got < size); return netRecvDone(buf, got, size, len, verbose);`, with netRecvDone holding the newline, the got == size test, the second newline, the log and the free. Not early-inlined, inlined at IPA. **V MATCH with the do form** for the first time (attempt 2 to 4's do family was V=50), and the guard takes the call heuristic the notes wanted (attempt 4's "p = .869 can't exist": it can, through a call in the else block at profile_estimate).
Why it works: at estimate the else edge and the loop's exit both reach the helper's got == size; after inlining VRP threads the else edge past it. Threading doesn't lower log or store, so log = (1-P)*S and store = P*S, with S = J + else and P = P(eq) in the helper (J 282 itself is corrected).
Measured (do form; f [10000, 9700], R 291, J 282, head failures scale with f_pre):
- `ne|ret` (gen_nr72 v10; `if (got != size) {...; return NULL;} *len = size; return buf;`, guard .912, P .28): **V=0, C=52, r=(0,0)**, margin -26. log 264, store 103. Layout right in both; only the registers.
- `eqs|ifnot` (gen_nr73 v16; guard .869, P .378): V=0, C=54, r=(0,2), margin -10. log 257, store 157 > head 155 (that's the r=2).
- `ne|ifnot` (gen_nr73 v10; `if (netRecvDone(...)) return buf; return NULL;`, guard .869, P .28): V=16, C=24, r=(0,0), margin +6. Registers right. log 298 > R 291, that's all the 16 and 24 are.
- `eq|ret` (gen_nr71 v9, guard .912, P .199): V=16, C=62, margin -14, log 294.
Exact model: margin = .4*(f_pre + log) - 515; f_pre = 874/g, else = 874(1/g - 1), S = 282 + else. Needs log <= 291, store <= second head failure (149 at g .869), margin > 0.
- g predictors: .912 (opcode + call + early return, `return helper()`), .869 (opcode + call, a test on the helper's result), .73 (no call first).
- P(eq) in the helper: .199 (eq layout), .28 (ne layout, the return block is next so no early return), .378 (eq + call first in the fail block via a nested static helper), .402/.598 (`nes`), .488 (nesv).
- At g = .869 the window is P in [.297, .316]. At P = .28, g would need to be about .877 and the window is empty by one freq unit. .33 misses by 2.4 cost. Nothing natural gives .30 (only opcode + call + const return, `return 2` on the ok path).
- gen_nr74 (63; `if (size > 0) { while ... }`, `for`, with the helper): the while's first test folds late; V=81+, C=37+. Do only.
- gen_nr75 (15; recv helper with a status and `int *` out for r, log in the caller, to keep R's own freq): early-inlined whatever the status convention, and r stays in memory (V=72, C=44+). Don't retry.
- gen_nr76 (40; helper returning 1/0 with the store in the caller): every test spelling and the eq/ne layout give the same bytes (phiopt folds PHI<1,0>; only two results, `eq`: V=16, C=24, margin +22, log 332, store 373; `eqs`: V=0, C=54, r=(0,2), margin -10). store here is P(X ok)*S with the null return's .90, so it decouples from log but can't get under the head failures.

Other windows worked out, none reachable:
- Direct form (else bypasses the helper's test, log = (1-P)J + else, store = PJ): at g .869, P in [.443, .468]. Have .488 (2.4 cost short); `return 2` on the fail path would give .464. And the else block can't start with a call, because the reference's else path has its own newline first.
- g .73 (margin to spare, S 605): log <= R needs P >= .519, then store 314 against head 177; also f_pre 1197 > the free-test block, so its trace starts in the wrong order.
- Pointer heuristic: a pointer compare at J has P(eq) .15, and with the call on the fail block that's .30, in the window. It would need `buf + got == end`-style pointers that survive to profile_estimate and go through a helper's parameters: a parameter that exists only to change the prediction, so not worth writing. Not compiled.
- Four exits, one dead (a = b = x = .0225): model gives R 220, log 215, store 131, margin about +100 at g .869, P .378, the clearest window of all. It needs a loop exit present at profile_estimate that is gone after IPA and doesn't land in J or log. Nothing natural known (attempt 6 reached the same wish from another side). A test in a helper would do it mechanically, but that helper has no reason to exist other than the count, so it would be a candidate at best. Not compiled.

## State at the end of attempt 8: NO MATCH without the asm

src/net.c and build.sh unchanged (flip + asm). Line counts, no flags (V, clone):
- drafts/net_netRecvVerbose_best.c (flip + cast pair): 0, 13. Still lowest total.
- drafts/net_netRecvVerbose_tailifnot.c (gen_nr73 v10, do form, tail helper, `if (netRecvDone(...)) return buf; return NULL;`): 16, 24. Registers right, margin +6, only log 298 > R 291, 7 over. The test on a pointer that is then ignored isn't how anyone would write it; the status form with the same layout (gen_nr76) isn't quite the same (eq: log 332).
- drafts/net_netRecvVerbose_tailhelper.c (gen_nr72 v10, `return netRecvDone(...)`): 0, 52. V MATCH, layout right in both, only the clone's registers, margin -26. The most natural of the three. The do + guard + tail helper reads like normal code.
- drafts/net_netRecvVerbose_tailshort.c (gen_nr73 v16): 0, 54. margin -10, store 157 against head 155.
Reproduce: python tools/wip/dehint/nrdef.py tools/wip/dehint/gen_nr72.py (also 70, 71, 73, 74, 75, 76); NR_TAGS=1 lists every tag per group. python tools/re/fncmp.py <draft> netRecvVerbose -O3 -Isrc ; FNCMP_GCCSYM=_netRecvVerbose.constprop.1 python tools/re/fncmp.py <draft> netRecv -O3 -Isrc ; python tools/wip/dehint/nrtr.py <src.c> netRecvVerbose (predictions) ; python tools/wip/dehint/nrbb.py build/nr/tr/<dir> 'netRecvVerbose.constprop' (traces).
Next: a natural P(eq) of about .30 at the helper's test, or a natural dead exit (four-exit model). If neither, keep the asm: this family only shows other ways to miss by a few units.
Don't retry: shared tail after the transfer (gen_nr70, shared store), guard + while (gen_nr74), recv helper with an out parameter (gen_nr75), caller test spellings on a status helper (gen_nr76, same bytes), thread_freq route to the same registers.

## Attempt 9: scoping locals (clobbers)

Reference first (0x41ee30): fds at esp+0x3c and tv at esp+0x34 in both the head's select and the loop's (`lea eax,[esp+0x3c]`, `mov [esp+0x10],ebp` with ebp = &tv), no second FD_ZERO, no second tv write. So there's one fds and one tv, live from the head through the loop: a second `fd_set`/`timeval` for the loop isn't the original (it would need its own init). Their scope can only be function level, or a block holding head and transfer, ending before what's outside it (zero arm or tail).

gen_nr80 (223 plain+while, 892 with do and side; hn neg/pos/rpos x hdr fn/blk/blk1/rest x fds fn/blk/tailout x head flip/old/else/nest x tail ret/fall/ne/var; invalid tailout+fall-through dropped): **f stays [9700, 9409] in every while+plain row**, MEM never rises above 17117 (-62, -122 where it changes). hdr's own block changes nothing (x50 rows have the flip's numbers; `blk1`, with the -1 test in the block, is V=20, C=48, same margin).
gen_nr82 (64; r per use and in the loop body, got and buf in if (size), size at its getBeU32, hdr at its recv, plain/side): every row is the flip or side result, margin -50 / -117. Scalars have no clobbers, so this was expected.

### Where the clobbers land, and what they change (drafts built from gen_nr80.src; dumps build/nr/n9/{flip,fb})

Flip at uncprop1: `_27 = PHI <0B(3), 0B(5), 0B(7), &netEmpty(22), 0B(13), 0B(21), 0B(16), buf_14(19)>`, then fds, tv, hdr clobbers and `return _27` in that one block. All 0B args are already direct, so there's no cb-style uncprop effect to gain here: nothing reuses a known 0, and the reference keeps its `xor edi,edi`.

fds/tv block with the zero arm outside it (`neg|fn|blk|flip|ret`): a clobber copy with an inner `_30 = PHI <0B..., buf_14>`, then `_27 = PHI <&netEmpty(21), _30(23)>`, then hdr's clobber and the return. Profile_estimate shows what that costs:
- every null-return prediction goes (cb's item 4): head tests 4.0% -> 27.0%, size == -1 95.9 -> 72, so the head failures are far too hot. V=113, C=107, r=17. The reference has them last, so **the head's returns reach the real return's PHI: fds/tv aren't in a block that excludes the zero arm.**
- J's early return goes: P(eq) .199 -> .28 (like the `ne` tail).
- the loop's exits don't change: first match, 3% each.
Nested head with fall-out, or a zero arm inside the block: x50 no-ops when all paths share one clobber copy; V=28+, C=66+ when not, and some fall-out rows lose the clone altogether (`neg|fn|blk|old|fall`, V=130, no clone). Tail outside the block (`tailout`, valid only with the old head): V=130, C=92, r=(46,42), margin -50.
`pos|rest|blk|old|ret` V=0, C=70, r=(0,8), margin -62: another V fix without the flip, worse in the clone, no margin.

### Why it can't pay the margin (while form)

margin needs f_pre, log+store, else or the exit shares to move. LOOP_EXIT is first match on all 3 exits and n_exits counts edges, so a clobber can't move f1/f2/f3 or f_pre. log + store = J + else whatever J's prediction is, and scope doesn't touch else (the 97% guard). So the only scoping effect on got's MEM is losing a ref (-12, -72). Measured, not just argued: no row in 223 is above -50.

### Do family: one real effect, not enough

gen_nr81 (210; attempt 8's tail helper x 3 callers x 10 scope shapes). **Scope does change the guard:** `return netRecvDone(...)` is g .912 at function level because of the early return; with fds/tv round it the return is two blocks, no early return, g .869. So `if (netRecvDone(...)) return buf;`, the odd spelling attempt 8 needed for .869, isn't needed: `eq|ret|posfb` (g .869, P .199) margin +22, log 332; `ne|ret|posfb` (P .28) margin +6, log 298.
But those are the same numbers as `eq|ifnot|base`, `ne|ifnot|base`: the window needs P(eq) in [.297, .319] at g .869, and the helper's P is estimated in the helper, which has no aggregate, so scope can't touch it. Also the shapes that get this are worse: posfb V=50, C=22, r=(8,8); fb V=92, C=74, because the head failures lose their shared return path or their null return. Rows unchanged from attempt 8: `eq|ifnot|base` and `ne|ifnot|base` V=16, C=24; `ne|ret|base` V=0, C=52, margin -26; `eqs|ifnot|base` V=0, C=54, margin -10.
Raising the head failures to free `store <= head` (the idea behind gen_nr81, for g .73, P >= .52) fails on arithmetic, not compiled at g .73: store 362 would pass R 291 too, and a P(eq) over .5 makes store J's fallthrough.
Direct do form (gen_nr80, no helper): flip|do V=52, C=44; old|do V=50, C=24, margin +158, log far over R; side|do V=26, C=43, r=(0,3), margin +91; `pos|rest|fn|flip|ret|side|do` V=59, C=20, r=(1,2). None beats the existing drafts.

## State at the end of attempt 9: NO MATCH without the asm. Scoping doesn't move it.

src/net.c and build.sh unchanged (flip + asm). No new best: drafts/net_netRecvVerbose_best.c still 0, 13; drafts/net_netRecvVerbose_flip.c 0, 48, margin -50. No candidate.
Reproduce: python tools/wip/dehint/nrdef.py tools/wip/dehint/gen_nr80.py (NR80_LOOP=do NR80_SIDE=1 for the 892); also gen_nr81.py, gen_nr82.py; NR_TAGS=1 lists tags.
Next: nothing from scoping. Still open from attempt 8, and not scoping: a natural P(eq) of about .30 in the helper (pointer compare + call would be .30, needs odd helper parameters; still not compiled, as this attempt was limited to scoping), or a natural dead loop exit.
Don't retry: any scope of fds, tv, hdr or the scalars for the margin; a second fd_set/timeval (the reference doesn't re-init); fds/tv blocks excluding the zero arm (head goes hot); tail outside the fds block.

## Attempt 10: declarations, then a test folded after profile_estimate. Bytes match with no asm; it's a dead test, so a candidate

### The families asked for (nrdef.py margin; flip base, -50)

- Log call (gen_nr92 `proto|*`, plus gen_nr32's forms from attempt 5): no macro form exists in `src/` (grep), `log.h` has one prototype. int return, K&R, `int level`, `char *fmt`, format attribute, do-while macro wrapper: all V=0, C=48, margin -50. So the asm's memory-capable operand has no natural equivalent here.
- Declaration (gen_nr90, 61): len as int/uint/long/ulong/size_t/u32/void/char pointer, return u8/uchar/void/char/int/u32, verbose u32/uint/ulong/size_t/DWORD/BOOL/long/int: **margin -50 in every row with a clone, MEM 17117.** Non-int len: V=2 for the unsigned ones. Return other than u8/uchar: V=130, C=68 (cause not looked at). verbose int: V=31 (known). Narrow verbose (u8, char, schar, u16, short, _Bool): V=10, **no clone** (why not looked at), so they're out.
- size and getBeU32 (gen_nr91, 154): long, int32_t, INT, LONG, ssize_t and `(int)`, inline test, `uint32_t` temp, `!~size`, `size + 1 == 0`, static helper: margin -50, V=0, C=48. Unsigned size with no casts: V=121+, class 0 only because got is another pseudo (margin -3887). `uint32_t size` with `got < (int)size`: **V=126, C=5, margin +31, registers right**, the same extra compare as `uint32_t got` (gen_nr5): the J compare survives cse_cc and that compare is the ref that pays, so it stays in the output.
- FD_SET (gen_nr92 `fd|*`): hand-written, reversed, winsock.h's old macro, pointer, helper, local SOCKET, written-out loop: margin -50, V=0, C=48, so the macro's loop changes nothing. tv after fds: V=2. memset: V=26, C=62, r=(8,4).
- Globals (gen_nr92 `glob|*`): volatile netEmpty, int/char[4]/u8[4] netEmpty, int netSock: margin -50, V=0, C=48. volatile netSock: V=24, C=58.

None of these moves got's costs, except by adding a real instruction.

### The lever: a stale block before the loop

The one odd row in gen_nr91, `int|u-temp3` (`n` unsigned, `if (!n) {zero}`, `size = n; if (size) {...}`), had margin +801. nrtr.py on it: block 8 (calloc, guard) is 3011 where the flip has 873. The inner `if (size)` is on the converted name, FRE can't fold it, so it's still there at profile_estimate, and VRP folds it after IPA. The folded test's block merges with what follows and keeps its own freq. The loop's freq was estimated with that exit taken out, so the sum no longer holds: this is the stale pre-loop frequency that attempts 4 to 9's conservation arithmetic ruled out (their "f_pre is fixed by the exits" is only true without an exit that later goes away).

Why it pays: got's two inits sit on the guard's edges, so MEM goes up .36 per unit of f_pre and nothing else in the loop changes (f stays [9700, 9409]).

The window (measured, gen_nr94-96; a test placed after the calloc, so the outer `if` keeps its .29 call heuristic):
- margin > 0: f_pre >= about 1010, so P(stay) <= .864.
- bbro: edge 10->11 (R's free test, .7 * 291 = 204) must reach round 3's threshold, 5% of the entry freq (threshold from memory of bb-reorder.c; fits entry 4251 failing, 212 > 204, and 4006 passing, 200 < 204), or 10 and 11 are separate traces and 12 isn't copied (`xor reg,reg` shared rather than copied: V=6, C=12). Entry = 3.89 * f_pre, so f_pre <= about 1048, P(stay) >= .833.
- So P(stay) in about [.833, .864], margin about 0 to +13.
- This also corrects attempt 8: f_pre above block 12 (1030 vs 966) is fine, connect_traces gives the same order. What it blamed on that is this threshold.

Results: gen_nr94/95, one test on the converted name, P is the wrong size: m1-empty .80 (+29, V=6, C=12), z-empty .61 (+165, V=34, C=6), z-null .911 (-19), before the calloc V=44 (outer `if` loses the call heuristic, entry falls). gen_nr96: two tests, `!size` + `size == -1`, each `return NULL`: **V=0, C=0, margin +1**, the first asm-free match.

### The candidate: gen_nr97/98, a test on len

`*len = 0` at the top lets VRP infer len != NULL, later than profile_estimate; nothing folds it earlier. So no conversions are needed and the types stay plain. Arm x test (gen_nr98): `if (!len) { netFree(buf); return NULL; }` right after the calloc gives **V=0, C=0, margin +5**, P(stay) .848, f_pre 1030, entry 4006. Same result for `len == NULL`, `len == 0`, and with the arm written `if (buf != &netEmpty) free(buf); return NULL;`. Other arms miss: plain `return NULL` -51, `return buf` -19, `free(buf)` alone -43/-55.
drafts/net_netRecvVerbose_candidate.c, patch drafts/net_netRecvVerbose_candidate.patch. fncmp MATCH on both with no flags. Its object is byte-identical (cmp) to build/obj/net.o from the matching build, built as build.sh does, so the link can't differ. The full build itself wasn't run with it (src/ unchanged).

Why it isn't a queue MATCH: README's list has dead tests, and this one is dead: len was dereferenced 16 lines earlier. It reads as ordinary defensive code (a null check after a deref is a common pattern) but it has no reason to be right there, and it does nothing except move a frequency. Behaviour is the same, since a NULL len would already have faulted at the top. The user's ruling: this, or the existing asm. It's the same class as the dead hints mode_client and mode_update carry, but with no asm or builtin.

The margin is thin: +5, in a window 13 wide, so it depends on this exact arm.

Other rows, not better: `r == SOCKET_ERROR` (r known from the head's test) with the log + free arm V=0, C=0, margin +1, but it's a re-test of a stale r. Rejoining tests (`if (len) *len = size`): no lever, as expected, flow is conserved (margin -62, or -50 for the zero arm's). `size == 0 || size == -1` on the plain name: -46, V=53+ (not looked at).

## State at the end of attempt 10: CANDIDATE, bytes match with no asm, needs the user's ruling

src/net.c and build.sh unchanged (flip + asm).
Reproduce: python tools/re/fncmp.py tools/wip/dehint/drafts/net_netRecvVerbose_candidate.c netRecvVerbose -O3 -Isrc ; FNCMP_GCCSYM=_netRecvVerbose.constprop.1 python tools/re/fncmp.py tools/wip/dehint/drafts/net_netRecvVerbose_candidate.c netRecv -O3 -Isrc ; python tools/wip/dehint/nrdef.py tools/wip/dehint/gen_nr98.py (also 90-97); python tools/wip/dehint/nrtr.py tools/wip/dehint/drafts/net_netRecvVerbose_candidate.c netRecvVerbose.constprop
Next: a test with the same effect and a reason to be there. Anything that exits between the calloc and the loop at profile_estimate and is gone by the output must be false at compile time, so it is dead in some sense; the only question left is which spelling the user accepts. A loop exit that folds (attempt 8's four-exit model) now looks doable with the same VRP trick, but it can't read better than this.
Don't retry: declaration types, log prototypes, FD_SET forms and global declarations for the margin (all -50); narrow verbose (no clone); tests before the calloc (outer `if` loses the call heuristic, V=44); `uint32_t size` (real compare stays).

## Attempt 11: the author's out-parameter guard (`if (len) *len = ...`)

Reference: `*len = 0` at the head is unconditional (0x41ee66, `mov eax,[esp+0x160]; mov [eax],0`, no test), so a later guard would fold. It also counts against the idea: bootloaders and fileutil guard every store of an out-parameter, and here the first store isn't guarded.

gen_nr100 (224; flip/else/old/not x tail eq/ne/first newline inside/`got == size && len`/`len && got == size` x store plain/`if (len)`/`!= NULL`/`*len = got` x zero arm plain/guards): no row above -50.
- Zero arm's guard: no change, as it isn't on the clone's path to got.
- Success store's guard: -62 (V=0, C=48). It rejoins, so flow is conserved and f_pre doesn't move; only the store block falls.
- `got == size && len`: -74, V=15. The false edge reaches the log, so log + store stays J + else.

gen_nr101 (241; `size && len` and spellings x `size == -1 || !len` and splits x zero arm x store): -50/-62 for everything natural. Why: on x86 `a && b` of two side-effect-free tests is one non-short-circuit `&` at GENERIC, so there's no exit edge at profile_estimate; VRP then only removes an operand. `size != -1 && size && len` has +40, but V=74+, r=14+. Control `if (!len) { netFree(buf); return NULL; }` is V=0, C=0, +5, so the tooling agrees with attempt 10.

gen_nr102 (384; no zero arm: buf from tern/if-else/default, verbose output skipped by `verbose && size` etc., one store, zero path left to threading; this would explain why buf != &netEmpty exists at the frees): margin -290/-302, V=65+, C=51, r=3. got's own refs fall (MEM 16865), and the threaded zero path doesn't get its own `mov [eax],0`. gen_nr93's `tern-if` etc. (rerun): second `if (size)` is gone before profile_estimate, V=22, -50. `buf != &netEmpty` as the second test: +167, but a real compare stays (r=17).

gen_nr107: `!tv.tv_sec`, `tv.tv_sec != 15`, `!fds.fd_count`, `!FD_ISSET(...)` after the calloc are real (V=157+, and gcc makes no clone). `!hdr`, `!&fds` fold in the front end: V=0, C=48, -50. `while (got < size && r != SOCKET_ERROR)` and spellings (a dead exit VRP should fold): V=134, C=48, -50, no lever. With `r != 0` too: V=222, C=31.

### In a tail helper the guard has a reason to exist (gen_nr103-108)

Attempt 8's do form with netRecvDone: the helper can't see the head's `*len = 0`, and the test folds after IPA.

Ordinary rejoining guard (gen_nr103): same frequencies as attempt 8 apart from the store. `eq-g|ret`: V=0, C=48, -26. `eq-g|ifnot`: V=16, C=24, +6, log 298. No match.

A `!len` test that leaves the helper before the compare, at P(stay) .85, lowers log without changing J, which is what attempt 8 lacked. **gen_nr104 `nolen|inl|ifnot`, gen_nr105 `free|not|afternl|eq|ifnot2` (build/nr/gen_nr105/v48.c, saved as drafts/net_netRecvVerbose_helperlen.c): V MATCH, C=6, r=0, margin +2, all registers right.** What's left is one block: the store (18) comes before the two head failures rather than after them.

Why, from the bbro dump: log 282 = J 282. log enters the heap first (the guard's else edge, trace 3), so on the tie it pops first and J is a one-block trace. That makes the store's predecessor a trace end, so bb_to_key gives the store priority over 3 and 5, whatever its frequency (70). If J pops first it extends into log, its trace doesn't end at J, and the store has to wait.

The window, exact:
- log < J = 282 (J is fixed by the 3% exit), so log <= 281.
- REG_FREQ truncates frequency to tens (`freq * 1000 / 10000`), so got's MEM moves in steps of 4 per 10 of log: log 280-289 is +2, 270-279 is -2 (C=52, registers lost).
- So log must be 280 or 281. log = Q(len) * (1 - P(eq)) * 414, so eq tail (.801) needs Q .845-.848, ne tail (.72) needs Q .940-.943.

The bb_to_key and J-extends-into-log steps are from memory of bb-reorder.c plus the hinted build's traces (J + log in one trace, store last); the dump shows the tie and "Changing key for bb 18 from -70 to -1008270". Not tested with a log of 280-281, because no source gave one. The window itself is therefore a prediction.

Measured (gen_nr105/107/108; about 115 arm x tail rows at ifnot2): all fall one side or the other. Upper side, margin +2 and C=6: eq tail with free, dup, vput (log 282), netFree + const, netFree + buf = NULL (not read individually), ne tail `log-const` (285). Lower side, margin -2 and C=52: ne tail `dup0`, `logfree`, `log-net-null`. No row is C=0. No predictor combination seen lands in the window, and I don't see one to try (hitrates from dumps: pointer .7, call .71, null return, const return, early return .61).

gen_nr106 (198; `*len = got` in the helper): V=2, margin unchanged, so no got ref is added.

Not landable even if the window were hit: `!len` here is still a dead test, in a helper that exists for the frequencies, with a caller `if (!netRecvDone(...)) return NULL; return buf;` that ignores the pointer. Attempt 10's single `!len` is simpler and already matches.

## State at the end of attempt 11: NO MATCH with the idiom

src/net.c and build.sh unchanged (flip + asm). The `if (len) *len = ...` idiom has no effect beyond lowering got's cost, since a test that rejoins conserves flow (attempt 10 had said so from one row; now it's measured over every shape). The evidence also says the author didn't guard len in this function: the head's store has no test.

Line counts, no flags (V, clone):
- drafts/net_netRecvVerbose_helperlen.c: 0, 6, margin +2. Lowest yet, but it has a dead `!len` and a helper, so this is a measure of the family, not a shape to land.
- drafts/net_netRecvVerbose_best.c: 0, 13. Still the lowest with no dead test.
- drafts/net_netRecvVerbose_flip.c with `if (len)` on the success store: 0, 48, margin -62, the idiom's best.
- drafts/net_netRecvVerbose_candidate.patch (attempt 10): 0, 0, margin +5, still awaiting the user's ruling.

Reproduce: python tools/wip/dehint/nrdef.py tools/wip/dehint/gen_nr100.py (also 101-108; NR_TAGS=1 lists tags); python tools/re/fncmp.py tools/wip/dehint/drafts/net_netRecvVerbose_helperlen.c netRecvVerbose -O3 -Isrc ; FNCMP_GCCSYM=_netRecvVerbose.constprop.1 python tools/re/fncmp.py tools/wip/dehint/drafts/net_netRecvVerbose_helperlen.c netRecv -O3 -Isrc ; python tools/wip/dehint/nrtr.py build/nr/gen_nr105/v48.c netRecvVerbose.constprop

Next: the user's ruling on attempt 10's candidate or the asm. Otherwise, any natural source that lowers log alone by 1-2 units in helperlen's shape, though that only swaps one dead test for another.
Don't retry: `if (len)` on any store in any shape (gen_nr100, 103); `size && len`, `size == -1 || !len` (one test at GENERIC, gen_nr101); no zero arm with threading (gen_nr102); tests of fds/tv (real, gen_nr107); `r != SOCKET_ERROR` in the loop condition (gen_nr107); `*len = got` in the helper (gen_nr106); more `!len` arms (gen_nr105, 108).

## Attempt 12: loop ended by assignment. MATCH, landed, no dead test

Tools: nrobj.py <file.c>... (text and data against build/obj/net.o; needed, see below), nrobjbest.py <gen> [N] (nrobj on rows of build/nr/<gen>.txt, written from `NR_TAGS=1 NR_TOP=300 nrdef.py`), generators gen_nr110-120. `-fdump-rtl-alignments-details` prints compute_alignments' freq, fall and branch per block.

src/net.c: fncmp MATCH for netRecvVerbose and the clone with no flags, nrobj text 0 data 0, `sh build.sh` SHA256 10dac648...971c. drafts/net_netRecvVerbose_best.c is a copy.

    int status = 1;
    ...
    while (got < size) {
        r = select(...);
        if (r == SOCKET_ERROR || r == 0) { log; free; size = got; }
        if (got >= size)
            return NULL;
        r = recv(...);
        if (r == SOCKET_ERROR) { newline; log; free; status = 0; }
        if (status != 1)
            break;
        got += r;
        if (verbose) printf(...);
    }
    if (status != 1)
        return NULL;
    (tail as before)

### How it was found

- gen_nr110 (504; the idea as given: arms assign, `else` or `continue` skips the rest, marker tested after the loop): V+C 173 at best. Arms no longer exit, so PRED_LOOP_EXIT doesn't apply and the opcode's 27% does: f [9100, 6643], margin -3012. A positive margin only came with `got = size + 1`, where a real compare stays. margin = f3 - .2f2 - .8f1 + ..., so f2/f1 must be near .97. Don't retry: an arm whose only way out is the head.
- gen_nr111 (162): the arm assigns and rejoins, and a separate test right after it leaves the loop. The exit keeps its 3%, so f is the plain [9700, 9409], but the arm has its own edge at estimate and R is 847, not 282. **That frees the old R >= J, R >= log constraint**, which is what capped the margin in attempts 4-11. `ok|sr|return|bot` V=4, C=0, margin +111; bot is `if (got >= size) break;` at the bottom, a 4th exit.
- gen_nr112 (700): `int ok = 1` in the loop body fixes the last V difference: fncmp V=0, C=0. **Not a match:** nrobj text 53. BB27 (V's tail newline) loses its .p2align: the 4 exits make it 2.25% * 2720 = 61, under V's freq_max/100 = 69 (the reference needs 3%: 79). fncmp can't see this. So 3 exits.
- gen_nr114 (108): 3 exits, one arm `break`, one arm `return`, post-loop `if (!ok) return NULL;`: V=4, C=0, margin +22. The break's flow reaches the post-loop test, and J's stale frequency pays the margin that the 4th exit did. Both arms `break`: V=8, C=6 (J stale too high, store 156 passes the head failures).
- V=4 is the verbose latch `cmp`. From the dumps: unswitch's copy gives the add a name off the free list, got_7, below size_46, so dom3 swaps to `got_7 < size_46`. The top of the free list is the flag PHIs that vrp1's threads create and dce2 kills. gen_nr115 (1728; locals, decl order, cast spellings) moves none of this: all V=4. Don't retry those. gen_nr116 (143; a different stop per arm): `size = got` on the select arm with `if (got >= size) return NULL;` is V=0, because no PHI of the flag is threaded there. Only `size|ok|rb` and `size|failed|rb` get it; that's the user's idea landing on one arm.
- nrobj on that: text 13, one .p2align on the clone's store block: 104, over freq_max/100 = 97. gen_nr117, 118: post-loop spellings, free or log moved after the loop: no effect, or worse (margin -14 to -54, C=60+).
- gen_nr119 (108): store = .199 * (stale J + else) = .199 * 523. Needs under 487, and margin needs about 400. `!ok` gets only the null return's 10%; `ok != 1` adds the opcode's 72% against it, P(stay) .78 by DS, stale J + else 452. **Store 90, text 0 data 0.** The prediction came first and the row agreed. `ok < 1` isn't enough. Comparisons with 0 getting no opcode prediction is from memory of predict.c and fits: `!ok` had a pure 10%.
- gen_nr120 (240): scope and init of the flag, loop-side test (`!= 1`, `!`, `== 0`), select test (`>=`, `==`, `<=`, `!(<)`), `while` or `for`: all text 0 data 0, so the shape isn't fragile in spelling. Only the post-loop `!= 1` is needed; I used it in the loop too so the two read alike. Margin reads -2 in nrdef, yet the registers are right: its formula truncates, so -2 here is not a failure.

### Clone, measured (trace order 2, 17 / 8, 19, 20, 9 / 10, 16 / 12 / 21, 15 / 3 / 5 / 14)

R 847, J 427, log 363, store 90, heads 134 and 129. f [9700, 9409], MEM 17165, class 1880.

### What each part does, and how far it can be defended

- `status = 0;` then `if (status != 1) break;`: same pattern as myatou32's approved `hex` flag, one `if` sets and the next tests. Needed: recv arm plain `return` is C=48 (margin -50, gen_nr116 `size|none|rr`) or V=92, C=36 with the select arm plain.
- `if (status != 1) return NULL;` after the loop: live. `!= 1` rather than `!`: **borderline**, reads fine, but it's there for the prediction. `!status` is one .p2align off (text 13).
- `size = got;` then `if (got >= size) return NULL;`: **borderline**. Live, but it's an odd way to write a return. Its job is the free list (V's latch cmp): a flag here is V=4, text 4. It's the part most likely to get a reviewer's question.
- `int status = 1` beside the other locals: fine.

Behaviour: same. Select failure: log, free, NULL, and `size` is only overwritten on that path. Recv failure: newline, log, free, NULL. `*len` stays 0 on both, as before. recv returning 0 still loops.

### Evidence

Frequencies, predictions, chains, SSA names and alignment numbers are from dumps. Alignment's freq_max/100 threshold is inferred from the dumps' `jump alignment added` lines and rows on both sides. The free list's order is inferred from names across passes (ok_7, ok_3, ok_111.. at vrp1, gone at dce2, reused in order at unswitch), and I didn't dump the free list itself. Why the `size` arm avoids the problem is inferred from V=0 and is not traced further.

Note for later generators: gen_nr110-120 cut src/net.c around `buf = calloc` and still build, but gen_nr1-108 expect the text before this attempt (commit b8d48e6's src/net.c); nrflip's strings won't all be found now.

Reproduce: python tools/re/fncmp.py src/net.c netRecvVerbose ; FNCMP_GCCSYM=_netRecvVerbose.constprop.1 python tools/re/fncmp.py src/net.c netRecv ; python tools/wip/dehint/nrobj.py src/net.c ; sh build.sh ; NR_TAGS=1 NR_TOP=300 python tools/wip/dehint/nrdef.py tools/wip/dehint/gen_nr119.py > build/nr/gen_nr119.txt ; python tools/wip/dehint/nrobjbest.py gen_nr119 8

If `size = got` is rejected, try next: another way to change what's on the free list at unswitch with a plain select arm or a flag on it, starting from gen_nr119's `ok-ret|!|!=1|brk|ret` (text 4, only V's latch cmp).
Don't retry: arms that only leave through the head (gen_nr110); a bottom `got >= size` exit (4 exits lose V's .p2align, gen_nr112); locals and casts for the free list (gen_nr115); moving the free or the log after the loop (gen_nr118). Check every fncmp MATCH with nrobj: two in this attempt were .p2align off.
