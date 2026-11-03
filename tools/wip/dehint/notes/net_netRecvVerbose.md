# net netRecvVerbose (queue 4)

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
