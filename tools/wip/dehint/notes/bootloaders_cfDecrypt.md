# bootloaders cfDecrypt (queue 8)

Tools: `tools/wip/dehint/cfsweep.py <gen.py>` (plain -O3, outputs in build/cf/<gen>/; o= other bootloaders functions whose
text changed, a=1 whole .s text of cfDecrypt, labels and .p2align included, equals src/bootloaders.c's), generators `gen_cf*.py`.

## The reference

The difference isn't what the queue's brief said: cfDecrypt has no calloc and no `xor ebx,ebx` (that's cb/cd/ceDecrypt, with buf).
Without its attribute the diff is 5 lines, at the end:

    call _checkZeros            call _checkZeros
    mov edx,1                   test eax,eax
    test eax,eax                setne al
    cmovne eax,edx              movzx eax,al
    jmp L                       jmp L

So the original's final PHI is `PHI <ok, 1>` at RTL, not `PHI <0, 1>`.

## The mechanism (general part, measured from the -fdump-tree-* dumps)

Three passes decide it, and DOM and VRP were never the real cause: the attribute only worked because stopping them stopped the 0 appearing before phiopt.

1. DOM/VRP replace `ok` on the false edge with 0 (the attribute stopped this). Any source spelling gets `PHI <0, 1>`; it's unavoidable and harmless.
2. phiopt's conditional_replacement turns `if (x != 0) PHI <1, 0>` into `_ = x != 0` (the setne), **but only if the block between the test and the join is empty**.
   Flat `key` with `if (ok) ok = 1` (gen_cf1 v16): the dump already has `_30 = ok_22 != 0` at phiopt1, and it stays. `return ok != 0` (gen_cf1 v0) has that compare from the source; PRE only moves it into the checkZeros block. Either way it's a setne.
   That phiopt's empty-block test is what stops it is inferred: gcc's source wasn't read, but with clobbers on the arms phiopt1, 2 and 3 all leave `PHI <1, 0, ...>` and the `if` alone (dumps below).
3. uncprop, late, walks the dominator tree and turns a constant PHI argument back into an SSA name known equal to it on that edge (`0` -> `_20`), if the types agree.
   This is what produces the `ok` the reference has; the 0 only needs to survive to here as a PHI argument. Expand then has `if (_20) eax = 1`, and ce1 makes the cmov.

So the job is to keep the arms non-empty until phiopt3, and the natural way is a **scope clobber**. A `return` from inside the block declaring `key` makes tree-eh copy the clobber to both exits
(two destinations: the return and the fallthrough), so `-fdump-tree-eh` has `key = {CLOBBER}` on each arm:

    if (_20 != 0) goto <bb 7>; else goto <bb 8>;
    <bb 7>: key ={v} {CLOBBER}; goto <bb 9>;
    <bb 8>: key ={v} {CLOBBER};
    <bb 9>: # _1 = PHI <1(7), _20(8), 0(3)>      (uncprop1; phiopt3 still had 0(8))

Clobbers produce no code at expand, so both arms are empty at RTL, and the if-conversion sees a simple `if`.

Conditions, from gen_cf2:
- The `return` must have two destinations out of the scope: `if (test) return 1;` falling out of the block. `return x != 0;`, `return x ? 1 : 0;`, `if (x) return 1; else return 0;` have only the return destination,
  so tree-eh sets the value first and has a single clobber after the join: arms empty, setne (4).
  Dumped for `return x != 0` and the if/else: one `key = {CLOBBER}` after the value's set.
- The scope must hold the test directly. `key` one block further out, in the magic block (gen_cf2 v2): the two clobbers are still there and phiopt still leaves it, but the false arm's clobber is in a block shared with `len > size` (bb7, two preds).
  The 0 for it isn't dominated by the test's false edge, so uncprop leaves `0(7)`: `je L; mov eax,1` instead of the cmov, and the fail path gets `xor eax,eax` before the magic test. **uncprop only reuses a value on a block the test's edge dominates.** 16 lines.

For cb/cd/ceDecrypt (untested; their hints left alone as asked): same family, opposite direction. Their reference has a literal `xor ebx,ebx` where gcc would reuse a known zero, and they have `key` at function level and
`return buf` from inside `if (buf)`. Worth checking first: whether their `xor ebx,ebx` is uncprop not firing. gen_cf2 v2 shows the lever in the wanted direction: the fail path's 0 keeps its `xor` when its block has another predecessor, so the test's edge doesn't dominate it, and here that came from which block `key` is declared in.
So: move `key` (or `len`) between the blocks in those functions and see which block the failure path's clobber lands in. Their attributes also include no-cse-follow-jumps, and the comment above cbDecrypt blames CSE and postreload too, so a scope move may fix only part of it.

## Shapes

gen_cf1 (192; head nest/guard/nestret/and x 12 tails normalising after a join x ok's type; key at function level): nothing under 4 (always setne). Moving the normalising past a join doesn't help: PRE does it.
gen_cf2 (28; test form x key's scope x len's scope):
- 8 MATCH, all a=1, o=0: key in the `len <= size` block, with `if (checkZeros(...)) return 1;`, `if (... != 0) return 1;`, or via `ok` (function-level or block-level); len at function level or in the magic block. Stable, not a fluke of one spelling.
- 4 lines: `return x != 0`, `return x ? 1 : 0`, if/else returns (one clobber after the join).
- 16 and 24: key in the magic block (see above).

## State: landed

src/bootloaders.c, gen_cf2's `ifret|inner|fn`, no attribute. Full build: SHA256 10dac648... matches.
Reproduce: python tools/wip/dehint/cfsweep.py tools/wip/dehint/gen_cf2.py ; python tools/re/fncmp.py src/bootloaders.c cfDecrypt ; sh build.sh
drafts/bootloaders_cfDecrypt_best.c is the landed src/bootloaders.c.

Nothing borderline: no flag, no redundant test; `key` in the innermost block that uses it, and the file's usual `return 0` at the end.
The tie to `len` is free: `len` could be scoped too, and matches the same.
