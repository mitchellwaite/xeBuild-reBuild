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

## Attempt 2

**Result: MATCH, 1 trick -> 0.** `drafts/keys_daeloop.c` at plain `-O3`, compiled through stdin
as build.sh does (`keyslib.py`), gives a keys.o byte-identical to the reference (sha256
e129fe9f..., same as `build/obj/keys.o`). `src/keys.c` still reproduces the reference, so the
reference was current. `sh build.sh` was not run: src/ is the orchestrator's to change.

The shape: the warning moves into the loop's exit arm, and the dead test goes.

```c
for (;; off += len) {
	if (off >= size) {
		if (n != 2)
			log_printf(0, "...WARNING...");
		break;
	}
	...   /* `goto next` became `continue`; the label is gone */
}
free(orig);
```

Why it works (from `-fdump-tree-profile_estimate-details`):

- The early-return predictor fires in two ways, and attempt 1's notes only had one. Say `e` goes to
  the block ending in `return`, and isn't `bb`'s next block. If `bb` has two successors, `e` is
  predicted not taken. If `bb` has one successor, `bb`'s incoming edges are predicted not taken.
- With the warning right after the test and right before free (the plain form), only the first
  fires: free edge not taken, warning 62.2%.
- In the exit arm, the body's blocks sit between the warning and free, so both fire. The dump shows
  early return 39% and 61% on the same branch; they cancel, leaving 72 + 29 = 51.2%, the
  number the dead test gave. The form with the warning after the free block (`E9`) only fires
  the second: 40.2%.
- The real window: bb-reorder sees edge frequencies after the size == 0 path is threaded off the
  warning edge, so the warning edge is `900p - 81`, not `819p` as attempt 1 wrote, and the free
  edge is `900(1-p)`. Dead test: 380 and 439, both under 450, so the trace ends and the warning
  goes out of line. Plain form: 479, so the trace takes the warning. The window for p is about
  50-59%. Below 50 the trace takes free directly, which should also leave the warning out of line
  (`E9`'s 179 lines are its allocation, see next point; that wasn't separated out further).
- The allocation needs the warning's block ordered before the loop (`.optimized` shows it as bb 3).
  The block moves there in the `pre` dump. Likely mechanism, inferred and not traced: PRE splits
  the critical edges, the forwarders are tail-merged, and the warning merges into the one placed
  after bb 2. That only seems to happen when the block before the warning has an edge to it.
  `E1`, `E2`, `E9` (warning not right after the test) keep it late, and that's where their
  172-179 lines come from: `xor ebx,ebx` is lost and buf/size change registers.

Scores at plain -O3 (`KEYSBASE=drafts/keys_final.c python keysend.py keysend_forms.py`):

| Form | Lines | |
|------|-------|---|
| `for (;; off += len)` with `continue` (the draft, `f3V1`) | 0 | no goto, no label |
| same plus `continue` after the bad header's `len = 0` (`f3V4`) | 0 | |
| `for (;;)` keeping `next:` (`T1`), `while (1)` (`T2`), `do ... while (1)` (`f3V8`) | 0 | |
| `size <= off` (`f3V7`), `if (n == 2) break; log; break;` (`T5`), `goto out` in the arm (`T4`) | 0 | |
| bad header `off = size; continue;` with no `len = 0`, `for (;;)` form (`f3V3`) | 0 | keeps `goto next` for the other two |
| warning kept after the loop, with the bad-header block moved between warning and free, reached by `goto bad` (`Z1`) | 0 | same predictor effect, worse to read |
| exit arm with `free(orig); return;` in it (`T3`) | 91 | warning falls into free again |
| plain, and folded spellings (`E0`, `E3`, `E4`, `E5`, `E6`, `E7`, `Ed`, `Ee`) | 91 | |
| free in the `n == 2` arm or warning last (`E1`, `E2`, `Eb`, `Ec`) | 172 | |
| flags and goto tails (`E8`, `E9`, `Ea`) | 179 | |
| free before the warning (`Ef`, `Eg`) | 214 | |

Borderline, for review: the warning in the loop's exit arm is unusual but live. Nothing in it
is dead or redundant, it behaves the same as before (same bytes), and it needs no goto. The
shape does steer the predictor, as any loop form does. It's a source shape, not a disguised
hint, so it counts as 0. The remaining borderline shapes from attempt 1 (fcrtEncrypt's two
encrypt calls, kvPrepare's two alt tests, `off = size; len = 0`) are unchanged.

Not tried: dropping daeEncrypt's duplicated first-key encrypt copy under the new loop form, or
`break` at the bad header (it would skip the warning test, so no).

Tools: `keysend.py` + `keysend_forms.py` (forms), `keysshowdae.py` (reference listing or diff).
`keyslib.py`'s default `FLAGS` still carries the old `--param`; pass `-O3` (keysend and keysshowdae do).

Next: nothing left to remove in keys. To land: copy the draft to `src/keys.c`, run `sh build.sh`,
drop keys from README.md's trick list (renumber, update the count), run `tools/re/progress.py`.

## Review (2026-11-10): all three borderline shapes approved, no code change

The user asked for the three keys borderline items to be reviewed and settled. All three
stay as they are, with `(approved)` added to their tags and the reason in each comment.
Scored at plain `-O3` against `build/keys/reference.o` (`keyslib.fndiff` lines; a scratch
`v.py` replaced one function of src/keys.c per `//== tag` block, not kept).

### fcrtEncrypt's two encrypt copies

| Form | Lines |
|------|-------|
| `memcmp(..) == 0 \|\| verifyFcrt(..) == 1`, one copy | 25 |
| helper taking the computed hash (`return 1` first, `\|\| `, `!= 0` first, both tests returning, `== 1` at the call), or doing the SHA too with `hash` from the caller | 50 |
| the same with the arms swapped (`if (!ok) warn else encrypt`) | 75 |
| helper with its own `hash` (shares a slot with `aes`, frame 0x22c) | 77-100 |
| encrypt helper called once or twice (not inlined: `aes` is too large a frame) | 93-97 |

Why, from `-fdump-tree-profile_estimate-details`: each of the four exits needs its own
epilogue copy, so each exit edge must be at least 1000 (10% of entry). The call heuristic
applies to an edge only when its test dominates the destination. The memcmp test dominates
the shared encrypt block, but the verifyFcrt test doesn't, so in the `||` form that test
gets the call heuristic on the warning edge alone (with early return and opcode, 62.2%).
The warning is 1407 x 62.2% = 875 and gets a `jmp` to the shared epilogue, which is the whole
25-line diff. With two copies each encrypt block is dominated by its test, the call
heuristics cancel, and the warning has 1127. The helper forms do get all four epilogues, but
the helper's own profile puts memcmp == 0 at 61% (call 71 against early return 39, dumped
for the first helper form), so the success path falls through after memcmp (the original
has 39%). keysfcgrid.py had already tried the flag forms (h6, h7) and the `||` forms with
every size and offset shape.

### kvPrepare's two alt tests

| Form | Lines |
|------|-------|
| `if (alt) kvEncryptAlt; else { kvSet; kvEncrypt; }`, with or without braces or a trailing `return` | 128 |
| the alt arm returning early, `kvSet; kvEncrypt` after it | 129 |
| `if (!alt) { kvSet; kvEncrypt; } else kvEncryptAlt` | 231 |
| `free(buf)` before a single if/else | 372 |
| `if (!alt) kvSet;` then `(alt ? kvEncryptAlt : kvEncrypt)(..)` | 383 |
| a function pointer set next to `file`/`name` | 398 |

Why: `if (!alt) kvSet(..)` is the only test with a call on one arm and none on the other, so
the call heuristic gives `!alt` 29% (bb 17 in the dump). After threading, the joined branch
keeps those probabilities. Every single if/else has calls on both arms (kvEncryptAlt against
kvSet + kvEncrypt), so its heuristics cancel at 50%. Reading the two tests as two concerns
(set the reference keyvault for the main kv; pick the salt for both) is plausible author code.

### daeEncrypt's `off = size; len = 0;` and the warning in the exit arm

| Bad-header arm | Lines |
|---|---|
| `off = size; len = 0;` (landed), or the same plus `continue` | 0 |
| `len = size - off;`, with or without `continue` | 551 |
| the same in the failed-decrypt arm too | 550 |

| Failed-decrypt arm | Lines |
|---|---|
| `n = 0; off = size + 1; continue;` (landed) | 0 |
| `off = size` | 35 |
| `len = size - off` | 43 |
| `off = size; len = 0;` | 332 |

The evidence that settles it: the binary's failed-decrypt arm loads `size + 1` (`lea
edx,[ebp+0x1]`) and jumps to the latch's `add edx,[esp+0x28]` (`off += len`) and the exit
compare. So the original computes `size + 1 + len`, and no `break` can produce that: the
author ended this loop by setting `off`, and the bad header doing the same with `off = size;
len = 0;` (which gcc threads straight to the `n != 2` test, as in the binary) is the same
idiom. Given the warning in the exit arm (attempt 2, needed for the 51% branch), a `break` at
the bad header would skip the warning, which the binary prints after a bad header. Same
call as console_hdd's approved `i = consoleManifest.count`.
