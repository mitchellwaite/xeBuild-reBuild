# mode_client s22 (profile-free), short session -- notes only

Profile build stays. No src/ or build.sh change.

## Try: __builtin_expect with a late-folding value (s21 idea a)
- `v_exp.c`: src/mode_client.c with the case 4/5 `cinfo->hwFlags & 0x20` tests wrapped in
  `__builtin_expect(x, __builtin_constant_p(start|count))`.
- Flags: s19 search.py FLAGS (-O3 -fno-toplevel-reorder -fno-ipa-profile -fno-reorder-functions
  --param builtin-expect-probability=50 -Isrc).
- Result: `tools/wip/mc/mckeys.py` output byte-identical to plain (no frequency/key change);
  fncmp diff 64 lines vs plain 58 (unrelated code change). Reason: profile_estimate runs
  long before dom2 folds bcp, so a non-constant expect argument is simply dropped. Dead end:
  expect cannot carry a late-folded probability.

## Concrete next ideas (not tried)
- Raise predecessor frequency of 112/115 via the send-call blocks 39/41 (s21 idea a, second
  half): check in the s19 injection rows why (39,*) lowers 112 by 1 (inspect the .cfg dump
  for a new merge block from the label placed before the send call).
- s21 idea b: inspect fdo.s order directly for the "missing" 112 rows (analyze.spmap may
  just fail to identify a block with an extra dead pred).
- s21 idea c: re-anneal on the inv-19 history restricted to movable blocks.
- Structural: restructure the case 4/5 source (e.g. hoist the hwFlags test out of the switch,
  or merge the two HDD-error log calls into one shared tail) so that the cold tail block set
  itself differs instead of nudging frequencies.
