# stfs stfsGetFile

Tools: `tools/wip/dehint/sfsweep.py <gen.py> [-v N]` (parallel fncmp at plain -O3; outputs in build/sf/<gen>/; source replaces
stfsGetFile), generator `gen_sf1.py`.

## Background (earlier sessions, no notes or generators kept)

Tricks to remove, on the loop guard: `if (__builtin_expect(n != 0, 1)) __asm__("" : : "S"(fb));`. Natural C reached 24 lines, swapping esi and ecx. Over 900 shapes failed
(loop forms, local types and scopes, helpers, copy inside the scan loop, types, signature, struct types, decl order, LE24 forms, raw offsets, dead-code SSA perturbation,
expect sweeps). The earlier explanation (n and fb tie at spill priority 2, so fb pops before blocks and takes ecx) was right as far as it went, but "needs something that makes ecx
unavailable to fb" wasn't the way: the fix makes the `blocks` pseudo pop first, and it takes ecx itself.

## Attempt 1: MATCH, both tricks removed

Shape (drafts/stfs_stfsGetFile_match.c, same as _best.c):

    for (j = 0; j < n; j++) {
        uint32_t off = c->blocks[j + fb];
        memcpy(buf + j * 0x1000, c->data + off, 0x1000);
    }

Verified: fncmp MATCH with no flags from src/stfs.c; build/obj/stfs.o byte-identical (cmp) to the previous build's object; `sh build.sh` SHA256 10dac648...971c. src/stfs.c restored
afterwards, so it still has the hints until landed. No __builtin or asm is left in the file, and build.sh has no stfs flags. Nothing about the shape needs a review flag: `off` is an ordinary temporary, and the same match holds with it declared at function
scope (gen_sf1 `off2`).

How it was found: reading ira.txt's push order for natural C.

- Natural: push a19 n (pri 2, cost 15), and that makes a16 `blocks` colorable, so it's pushed before a18 fb (pri 2, cost 23). Stack order means fb pops first, takes the first free reg (ecx),
  and blocks gets esi. The a16 conflict list is a8 a14 a20 a21 a23 a17 a19 a18. **a22 `c` is missing**, because c dies at the blocks load, the last load in the preheader.
- With `off`, `c->blocks` is evaluated before `c->data` in the loop body, so PRE's preheader order is `pretmp = blocks; pretmp = data`. c stays live over blocks' def, so blocks
  has one more conflict and isn't colorable until fb has been pushed (dump: "Pushing a18 ... Making a16(r131) colorable"). Pop order is then a16 (ecx), a18 (esi), the original's allocation.
- The final asm still loads data before blocks, as the original does: sched2 reorders them, which is why the instruction order gave no clue that the RTL order differs.

So the deciding pass is PRE's insertion order feeding IRA's colorability, not costs or frequencies. The earlier sweeps never moved the evaluation order of the two loads.

gen_sf1 (20: load order forms x n/fb order):

| Shape | Lines |
|---|---|
| nf, `off` in the body, or `off` at function scope | 0 |
| nf, plain, `c->blocks[..] + c->data` | 24 |
| ptr `b = c->blocks + fb` | 51 |
| locals data then blocks | 54 |
| locals blocks then data | 60 |
| fn (fb computed before n), any form | 51+ |

Don't retry: anything further on this function, unless the shape is rejected.

Lesson for other register-swap ties: list the a-number conflict list of the pseudo that pops too late, and ask what source order would extend a neighbour across its def. Spill priorities
may be unreachable when colorability isn't.
