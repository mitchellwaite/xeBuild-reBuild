# s150 (attempt 131): interrupted, no result

The session ended before this attempt reported. Only `beam.py` survives, unverified.
Its brief is still open, starting from `s146/t6.c`:

1. Extend s148's model enumeration (`alt*.py`) to 4-5 changes by beam from the
   best 2/3 combinations. Add change types: a tail block built in round 3, any
   trace first inserting block 128, insertion order within a trace.
2. Implement any 0 solution that maps to known levers on t6, then compare the dump
   with the model.
3. Run the fixed gen/climb (`s146/e/gen.py`) on any new base at f2 <= 20.

## Current state

- Best f2 16: `s146/t6.c` (front in reference order; only the freq-0 tail differs:
  150 147 79 128 81 42 53 35, target 147 128 150 35 42 53 79 81) and `s141/best16.c`.
- Metric `s101/f2.sh`; flags -O3 -fno-toplevel-reorder -fno-ipa-profile
  -fno-reorder-functions --param builtin-expect-probability=50.
- Validated round-4 model: `s86/r4sim.py` + `tools/wip/fibsim.py`.
- Model floor on t6 within 3 changes is 2 (79/128 swapped). The known 0 needs block
  128 first inserted by trace 108/121, which source moves can't do (s147, s149).

## Cleanup (2026-11-02)

To free disk, generated files were deleted from every untracked attempt directory:
gcc dumps, .s/.o/.ref/.mine, files over 1 MB, and .c variants below an attempt's top
level unless named base*/best*. Notes, scripts, json and top-level .c were kept.
Rerun the attempt's scripts to regenerate dumps and climb caches (`s144/fb/v` etc.).
`build/v` was also removed.
