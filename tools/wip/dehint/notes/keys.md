# keys (whole object)

Tools, all in `tools/wip/dehint/` (run from there; `KEYSBASE=<file>` sets the base source,
default `src/keys.c`, and `build/keys/reference.o` must hold a matching build's keys.o):

- `keyslib.py`: compile as build.sh does, whole-object byte compare, per-function diff
- `keysfn.py <fn> <template> [out]`: replace one function and score it
- `keysshow.py`, `keysdump.py <fn> <dump flag> <file>`: diff, or one function's gcc dump
- `keyssubset.py`: all-subsets search over the old hint sites
- `keysfcgrid.py`, `keyskvgrid.py`, `keysdaegrid.py`: shape sweeps per function
  (`keysfc.py`, `keyskvone.py`, `keysdaeone.py`, `keysdae.py`, `keysdaeexp.py` support them)
- `keysalt.py`: spelling checks against `drafts/keys_final.c` at plain -O3

## Attempt 1

**Result: MATCH, 18 tricks -> 1.** `drafts/keys_final.c` at plain `-O3` gives a keys.o
byte-identical to the reference (sha256 e129fe9f...). No expect, label, attribute, pin or param.
The one left is the dead test `if (orig) free(orig);`, which README.md counts as a trick.

What each function needed:

- **fcrtEncrypt** (pure, expect): an else chain down the three checks, with the hash test as
  `if (memcmp(...) == 0) {encrypt} else if (verifyFcrt(...) == 1) {encrypt} else log`. Each of
  the 4 exits needs its own epilogue copy, so each edge must be >= 10% of entry. In the `||`
  form the success block has both preds and takes 1432, the warning gets 875 (below 1000). The
  two-copy form gets all of them over, and crossjumping merges the copies. Found by
  `keysfcgrid.py` (1224 combinations). The size test can't be raised another way: with
  `return`s `size != 0x4000` is 72% and the main path has under 3000 for three >= 1000 exits.
- **kvPrepare** (4 expects, 3 labels): subset search showed everything but the `!alt` expect
  could go, leaving only a [56]/[60] slot swap. The hot labels had no effect. Then
  `if (!alt) kvSet(...); if (alt) kvEncryptAlt(...); else kvEncrypt(...);` gives the rest:
  two tests, threaded together later (profile_estimate runs before threading).
  Plain `if (alt) ... else {kvSet; kvEncrypt}` is 128 lines off.
- **daeEncrypt** (5 expects, cold label, 2 pins): a plain `while (off < size)` with a bad header
  setting `off = size; len = 0;` already gives the original's allocation, including the
  `xor ebx,ebx` / `mov edx,ebx` the pins were forcing. Only the warning's block placement
  was left (91 lines, all from that). In bb-reorder's first round the n != 2 -> log edge must be
  under 50% of entry: 819 x 62.2% = 509 > 450. The 62.2% is opcode 72 + call 29 + early return
  61. The early return applies because the edge's destination is the return block
  (`free(orig); return`) and isn't the next block. `if (orig) free(orig);` puts a test in that
  block, so the predictor doesn't fire: 51.2%, edge 419, trace ends as in the original. vrp
  removes the test later because memcpy's nonnull implies orig != 0.

The `--param` went with the last expect. An intermediate step also matched:
`__builtin_expect(n != 2, 1)` at param 52 or 54 (`keysdaeexp.py`), which is what showed the
window was around the natural 51.2%.

Spellings checked at plain -O3 (`keysalt.py`):
- also match: `len = 0; off = size;` order, `if (orig != NULL)`, `if (!alt) kvEncrypt else
  kvEncryptAlt` for the second alt test
- don't match: `break` at the bad header (533), `off = size + 1` (551), a `goto` past the loop
  (533), plain `free(orig)` (91), a single alt if/else (128)

Failed along the way, not worth repeating:
- `uint32_t off;` uninitialized with no pin (143): not the source of the early zero, and it would
  be an uninitialized read. The zero comes with the plain `while` form.
- `if (size) do ... while` without pins (93) gets the layout but not the allocation. So do
  `if (size) while`, and `do { if (off < size) ... } while`.
- flag forms for the n != 2 test and a switch (172-179); goto tails `Eg`-`Ej` change the
  allocation (172-179).

Borderline shapes, flagged for review:
1. `if (orig) free(orig);` in daeEncrypt is a dead test that steers the predictor. The same file
   has `if (ext->data) free(ext->data);`, though that pointer can really be NULL. Plain `free` is
   91 lines off, and no other form was found.
2. fcrtEncrypt's duplicated encrypt calls in two arms. No shape with one copy matched.
3. kvPrepare's two alt tests, live but redundant.
4. daeEncrypt's `off = size; len = 0;` instead of `break`; the `i = count` pattern, and `break` is
   533 lines off.

Next, if anyone wants to go further: replace `if (orig)` with something that isn't dead, by
getting the same 51.2% on the n != 2 branch. It needs that edge's destination to be something
other than a block ending in the return. A real second `return` elsewhere would split the return
block, but the original has no path for one.
