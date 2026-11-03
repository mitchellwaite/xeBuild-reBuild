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
