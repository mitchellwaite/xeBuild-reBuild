# p1: applyIniOptions profile-free: MATCH

`match.c` is the whole `options` object from one plain compile, with no profile and no `src/options.prof`.

## Verification (real compiler output)

- Flags are build.sh's existing cflags without `prof`: `-O3 --param builtin-expect-probability=83 -fno-ipa-profile -fno-reorder-functions`.
- `sh tools/wip/aio/p1/cmpo.sh tools/wip/aio/p1/match.c`: `.text`, `.data`, `.bss`, `.rdata`, `.text.startup`, `.rdata$zzz`, `.eh_frame` and relocations are all the same as `build/obj/options.o`. Its output dir `build/v/aio_p1/o` is created on demand.
- `sh tools/wip/aio/p1/vlink.sh`: links build.sh's object list with this `options.o`, then stamp and execmp. 0 differing bytes, SHA256 `10dac648...1971c`.

Integration is still open; src/, build.sh and tools/re are untouched. To integrate:

1. Copy `match.c`'s code to `src/options.c`.
2. Drop `prof=...` from the options case in build.sh, and delete `src/options.prof`.
3. Fix the stale comments: the head comment, "compiled with -fbranch-probabilities", "never written", "optIniBool's body", "The block layout comes from the profile", "a dead edge into the remopower test".
4. Remove the unused always_inline copies `parseButtonI`, `macidSetI`, `stripColonsI` and the unused `OPT` body, if they still match when gone. `gen0`/`f2` left them in place.
5. Run `sh build.sh`.

## Why it works: the original is natural source

The earlier work kept option bodies in a macro. The original looks like this instead:

- `OPT(n,s,c)` is `if (!(xb.bootFlags & s)) optIniBool(n, s, c, 0)`, IPA-inlined. PRED_CALL gives 29% on the guard.
- `macidSet()`, `stripColons()` and `parseButton()` are plain calls. This alone gives the reference's freq_max 3716, the whole hot layout and threshold 37.
- `xb.bootFlags &= ~clear; xb.bootFlags |= set;` is two statements, which gives nodvd's `and`/`or` memory forms.

That reduced the difference to the cold part (`n1.c`, 686 lines). The hints below handle that part. Whether the original got the same frequencies from another natural shape of optIniBool is still unknown: variants A to D in `f10.py` all keep the early-return predictor.

What the layout needs, derived from bb-reorder rules (entry 1815; thresholds r1 907, r2 363, r3 90):

- Others: O < 363 and P < 180, so `[O]` ends in r3 and `[P PL S]` forms in r4.
- noecdremap: P in [90,180), so `[P]` is r3 and connect picks `[I W .]` by length.
- S >= 181, so connect_traces copies the next test (`test eax`) after S. That is the "S/jne" pair.
- GU must be 37 (always_inline `optIniIntI`: 15%, not 21.6%).

## Hints in match.c (all zero-byte, never run)

- **optIniBool arms**: `if (flags & set) { if (cp(...)) goto r; return 0; }` and the same for off. The early-return predictor moves into the arm, so bb2 is 50% and off is 29%, giving P = 14.5% of the edge. Label `r:` sits before the S statements, so S is stale-high (the copy threshold).
- **optN (noecdremap)**: one dead exit, plus `expect(!bad, 0)` to put G under nodvd's I.
- **optO (olddvd)**: dead feed into S. This raises the branch edge of L_425c30 above 4x fallthru, the alignment README called impossible. I is 38 and G is 8.
- **parseButtonX (xellbutton)**: dead feeds raise the `!s` block from 29 to 37, and it holds one dummy.
- **gl= copies (smcnoeject, cygnos, nosecurity, nandmu)**: G lowered by expect, to order the G tie groups.
- **Three zero-byte dummy heap entries**, each a `dz` with `asm volatile` and `if (cp) goto back; __builtin_unreachable()`:
  - macid chars warning (key 39..48), `dz1`.
  - Head of xellbutton's else arm (key 48..70), `dx`.
  - dualboot's `xb.dualButton = 0` (key 18 in the real build).
  - dz1 and dz2 are keyed by feeds from the block after sprintf, whose flow only reaches the return.

## Levers learned

- A label in an empty block merges into the next: `dzc: cold; goto dz;` makes the whole block cold. A feed then needs `__builtin_expect(cp, 1)`, because expect beats PRED_COLD_LABEL. This keeps the asm-goto edge at 0.1% (no flow lost) and the feed live.
- `__builtin_unreachable` directly in the target makes the feed edge 0 (PRED_NORETURN). A test `if (cp) goto back;` before it stops that and also returns the flow, so downstream counts don't shift.
- `__builtin_memset(s, 0, cp(x))` before an asm goto keeps PRED_CALL on the block. The size folds to 0 and the call goes.
- `goto back` from a dead block must carry the same value (`b = 0x11`), or threading is lost at the join.
- Feeds out of a block with no join below them lose nothing: downstream counts only change at a join. Anything else shifts every later block.
- PRED_CALL needs the call in `e->dest` and the destination dominated by the source, so a feed into P drops it.
- `connect_traces` picks a successor by edge probability first and then trace length. Trace-end priority keys apply only to a block whose pred ended a trace, and they sort before all frequency keys.

## Tools (run from repo root; outputs go to build/v/aio_p1/, create it first)

- `mkmatch.sh OUT.c`: regenerates `match.c` from `n8c.c` with `mk.py`.
- The chain before that: `gen0.py` -> base, `f2.py int,mac,strip,but` -> n0, `f3.py two` -> n1, `f10.py F`, then always_inline `optIniIntI` -> n8c. Intermediates are deleted.
- `s.sh SRC TAG` (compile, counts), `run.sh`, `ev.py`, `sq2.py`, `cm.py`, `bm.py`, `pe.py`, `hd.sh`.
- `r4.py` and `nm.py`: head order with names. Ids shift once asm gotos split blocks.
- `aldiag.py`, which needs `../alignreq.txt` copied in.
- `sim3.py`: exact fibheap replay of rounds 3 and 4, verified against real dumps.
- `ds7.py`, `ds9.py`, `alt3.py`, `ov.py`, `tail.py`: searches for dummies and keys on the model.

The model found the design and the real build confirmed it, with `ev.py` and `cmpo.sh` as the final check. The ev.py metric keeps padding and string identity, so it was at 0 only when the bytes were.
