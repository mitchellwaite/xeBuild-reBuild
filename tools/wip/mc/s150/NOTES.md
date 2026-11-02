# s150 (attempt 131): MATCH, plain compile, no profile

`match.c` builds `mode_client` byte-identical with no profile. Base: `s146/t6.c` (21 changed lines).

## Verification (real compiler output)

- Flags: `-O3 -fno-toplevel-reorder -fno-ipa-profile -fno-reorder-functions --param builtin-expect-probability=50`.
  No `-DBUILD_FDO`, no extra param. `match.c` only mentions BUILD_FDO in its head comment.
- `sh tools/wip/mc/s101/f2.sh <copy of match.c>`: 0.
- `sh tools/wip/mc/s150/cmpo.sh tools/wip/mc/s150/match.c`: `.text`, `.rdata`, `.rdata$zzz` and relocations are
  all the same as `build/obj/mode_client.o`. Its output dir `build/v/mc150/o` is created on demand.
- `sh tools/wip/mc/s150/vlink.sh`: links build.sh's object list with this `mode_client.o`, then stamp and execmp.
  0 differing bytes, SHA256 `10dac648...1971c`, the reference's. Uses `build/obj` from the last build.

Integration is still open: src/, build.sh and tools/re are untouched, and build.sh still uses the profile splice.
To integrate, move `match.c`'s changes into `src/mode_client.c`, drop the fprof/fflags/ffns case and `mode_client.prof`,
then run the full `sh build.sh`. Check whether the old `BUILD_FDO` head comment and macros in the source are still wanted.

## How the residual went from 16 to 0

The model (`s86/r4sim.py`) was exact every time it was compared with a real dump. The search scripts are
`beam2.py` (replaces `beam.py`), `real.py`, `real2.py`, `real3.py`, `dumb.py`, `dumk.py`, `chain*.py`, `ei2.py` and `ext.py`.
`bbs.py` maps a trace bb number to source lines. Those numbers differ from the RTL's, which is compacted through
the "Reordered sequence" table. Older notes misread this: 79/81 are the `-r` usage blocks (asm goto `r3x,r5x`,
cross-jumped), and 144 is the efail log.

Levers, in the order they were found. All are zero-byte and never taken at run time:

1. **Zero-byte dead block**: `if (0) { dz: asm volatile("" ...); __builtin_unreachable(); }` with a `JMP(dz)`. It adds a
   heap entry and a pop, and emits nothing. Identical bodies get cross-jumped, so each needs its own asm, for example a
   `"i"(N)` input or a clobber. A `"#"` template also works but prints /APP lines.
2. **Any key for that block**: a dead `if (__builtin_constant_p(block + K)) goto dy;` feed gives it stale frequency at
   profile_estimate, then folds away. An optional dead `goto` back conserves downstream flow. `dy` (key -2, from efail)
   took f2 from 16 to 10; swapping `r3x,r5x` to `r5x,r3x` took it to 6 (`best6.c`).
3. **`-r` head edges** (`tail_ok.c`). Heap needs 81 and 79 inserted before 62, so:
   - `__builtin_memset(argv, 0, kk); if (!kk) { ac: cold; asm goto("" :: "a"(i) :: r5x, r3x); }` at the head of the `-r` test.
   - The dead memset is a side-effect call in the block, so PRED_CALL still fires on the `-ip` test (without it, 50/50).
   - The cold folded arm keeps the usage blocks at frequency 0.
   - `"a"(i)` matches the reference's first `mov eax,[esp+68]`.
   This gave the exact tail with f2 18.
4. **`-i`/`-p` tie**: those edges renumber the loop PHI, so the i partition's lowest member is anonymous and its pseudo
   gets a high regno (r402, not r91). RTL then uses the copy and `i+1` no longer conflicts. Fixed with
   `({ __asm__ ("" :: "d"(i + 1)); 0; })` in both tests (`p2`). This reached f2 0, but the bytes still differed.
5. **Byte-level residuals**, invisible to f2:
   - Case 6's asm goto cross-jumped into case 8's tail, so its jump table entry was wrong. Removed it. Round 2 then pops
     159 before 161 and the heap shape changes. The model gives one fix: a key -3 entry pushed in round 3. Done with `dv`
     in the rok block's asm label list.
   - Don't use `cp(mode + K)` inside a switch case: VRP knows `mode` there, it folds true, and it became `case 6: c11`.
   - Label alignment rule: `freq > prev_freq * 10` with no fallthrough, so a frequency-0 block before a nonzero block
     aligns the label. Fixed with stale-frequency tail blocks: `efcl` after efail (asm with `"i"(64)`, `-w` label), `c8t`
     (c9 label), `c9t` (c11 label). A zero-byte dummy with frequency there is no help, as the alignment lands on it.
   - Identical `asm goto dsp` tails cross-jumped into jmp-to-jmp. Each now has its own `"i"(N)`, and case 4's asm moved
     into the sendAvatarData arm so hdd4 jumps straight to dtg.

The `mk*.py` scripts are the chain of edits that produced `match.c`. They ran in a scratch dir that is now deleted, so
they are a record and won't rerun as they stand. `best6.c` and `tail_ok.c` are intermediate states.

## Ruled out

- Edges from post-loop code into the arg loop (for example case 3 to the `-w` test, 773-789): liveness wrecks RA.
- Usage edges after the strnicmp call (82-84): eax holds the result, so the usage block gains a reload.
- `s150/beam.py`: its `r3` move can never score, because it emits the block ahead of round 4.
- Model solution "62 first inserted by trace 117": exact in the model but needs a back edge. `real2.py` filters those.
