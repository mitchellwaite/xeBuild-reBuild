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
