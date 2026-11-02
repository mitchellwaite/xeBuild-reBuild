# p1: mode_update profile-free: MATCH

`match.c` is the whole `mode_update` object from one plain compile, with no profile, no `prof=` and no `NOPROF`.

## Verification (real compiler output)

- Flags: `-O3 -fno-toplevel-reorder --param builtin-expect-probability=68`. `-fno-ipa-profile -fno-reorder-functions` are no longer needed, and neither is NOPROF. Without a profile, getConsoleFiles is not inlined anyway.
- `sh tools/wip/mu/p1/cmpo.sh tools/wip/mu/p1/match.c`: `.text`, `.data`, `.bss`, `.rdata`, `.rdata$zzz`, `.eh_frame` and relocations are all the same as `build/obj/mode_update.o`.
- `sh tools/wip/mu/p1/vlink.sh`: links build.sh's object list with this `mode_update.o`, then stamp and execmp. 0 differing bytes, SHA256 `10dac648...1971c`. It also reports section sizes and symbols the same, and `cmp` of the whole `.o` file against `build/obj/mode_update.o` is identical.
- Both scripts compile as build.sh does: `#line 1 "mode_update.c"` + source on stdin, `gcc -c $FL -Isrc -x c -`. Output goes to `build/v/mu_p1/`, created on demand. They use `build/obj` from the last build.

## Integration (not done; src/, build.sh, tools/re untouched)

1. Copy `match.c` to `src/mode_update.c`. `diff base.c match.c` is the whole change (`base.c` is src at the start of this attempt).
2. build.sh's mode_update case: `cflags="-O3 -fno-toplevel-reorder --param builtin-expect-probability=68"`. Drop `prof=` and the comment above it about the crafted profile (lines 77-83, 86-89). The `fdo` helper and `prof` handling can go if nothing else uses them (options and mode_client no longer do; check).
3. Remove `NOPROF` from `src/xebuild.h` (lines 78-82) if nothing else uses it. `match.c` no longer uses it.
4. Stale text in `match.c`: the head comment points at this file; replace it with a short explanation of the hints. Add comments at the hints (labels `werr`, `wok`, `hu`, `iperr`, `dn`), since they have none. getBadBlocks' success-first shape was for align-threshold under the profile; it still matches, so leave it unless you re-test.
5. Run `sh build.sh`, then `python tools/re/progress.py`, and update the docs that describe the profile (tools/wip/README.md's mode_update section, tools/wip/mufdo.sh and friends are now history).

## Why it works

The plain compile of the existing src differs only in cold-block order in the last STC round (42 ev lines, no RA changes). So no source rewrite was needed. The natural-source idea from options was not pursued, because the frequencies above round 4 already agree. Whether the original had a more natural shape is still unknown.

The old conclusion, "9 key changes", assumed key changes only. Adding one dummy heap entry cuts that to 3 keys:

`fast.c` (annealing on an exact heap model, about 200k sims/s) found: **122 (WARNING) -2 -> -3, 125 (writeImage error) -2 -> -1, 13 (-ip error) -3 -> -4, plus one zero-byte dummy entered when bb 43 (the -noava log block) is visited, key <= -7.** Numbers are bbro's for the base compile.

The dummy alone fixes the 46/112 tie and the 38/30 tie, because its pop changes the heap's consolidate shape right after 43.

## The hints in match.c (all zero bytes, never run)

- **WARNING to 3**: `__builtin_expect(!noReboot, 1)`. The block `if (!ret)` goes from 4.5 to 6.4, so both arms are 3. A feed into the arm does not work: the arm is then not dominated, PRED_CALL drops, and the trace flips to WARNING.
- **writeImage error to 1**: `wok: __attribute__((hot, unused));` on the join gives 15%, but with PRED_CALL DS combines to 6.7% and the key is 0. A dead `if (cp(r+1) && .. cp(r+4)) goto werr;` removes the dominance (so PRED_CALL drops, leaving 15%) and adds a small feed. Result: 1.
- **-ip error to 4**: one more edge into the noreturn block, `if (cp(i + 101)) goto iperr;`. Each edge into a noreturn block adds 0.04% of its source.
- **Dummy `dn`** in the -noava arm: asm goto to a block holding `asm volatile("" :: "r"(i))`, `if (cp(argc+103)) continue;` and `__builtin_unreachable()`. Two `if (cp(argc+K)) goto dn;` feeds lift it to freq 8.
  - The cp must use `argc`, not `i`.
  - The `"r"(i)` keeps i_1 live on the dn edge. cp folds right after IPA, before sink, and without a real use sink moves `add ebx,1` past the call.
- **-noreeb trace lengthened**: asm goto splits 43's jump into a second block, so trace [43, jmp] has length 2, and connect_traces ties by length and took 42->43 instead of 42->noreeb test. Fixed with `__builtin_memset(argv, 0, cp(i+106)); asm goto("" :::: hu);` at the head of the -noreeb arm, making that trace length 3.
  - `hu` is the help block's `update_usage()`. The edge into a noreturn block has frequency ~0 and the block is already in the heap, so nothing else moves.
  - The memset keeps PRED_CALL on the -noreeb test.
  - An edge to the -nowrite arm instead pulled that arm out of its r3 trace.

## Levers learned

- `cp(pointer)` folds to 0 in the front end at once; cast to int (`(int)p + K`) or use an int.
- Before writing hints, ask the model which key/dummy set is cheapest; lowering a key is possible by a stronger predictor plus a small feed.
- better_edge_p: with equal probability, the lower-frequency destination wins. A stale raise of one arm can flip the trace.
- A dummy from a block that ends a trace adds a jump block to that trace and changes connect_traces' length tie.

## Tools (run from repo root unless noted)

- `sh tools/wip/mu/p1/run.sh SRC TAG [width]`: compile with dumps to `build/v/mu_p1/TAG`, show traces, ev counts, string-order diff count.
- `python ev.py SRC -t TAG -v _mode_update` (in this dir): per-function diff vs `build/obj/mode_update.o`.
- `python refseq.py O`: string order diff; `python tr.py DIR -a`: named traces.
- `dsim.py` (model, checked: r3 and r4 same as every dump compared), `ds1.py` (single dummy brute force), `expev.py` + `fast.c` (`gcc -O2 fast.c -o build/v/mu_p1/fast.exe`; `fast EV SEED SECS cl cr cd NODES..`, env `EXCL=",43,44,"` to forbid dummy hosts).
- `dsim.WANT` is in base bb numbering (asm gotos shift it). The model does not cover connect_traces.

## Ruled out or not needed

- Raising 117 and 20 instead of lowering 125 (first model solution): a feed into 117 drops PRED_CALL on 115 and the trace flips.
- Single dummies at other blocks: none works with these keys. 2-3 dummies in the updateNand trace do work in the model (for example two at 113 and one at 105), but were not needed.
