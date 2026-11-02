# s43: register pins on the 77/79@61 movers (plain compile, no profile)

Result: NO MATCH. Best clean is still H5b.c (5 inv / fncmp 40 / cm (0,8)); best moved stays 3 inv / cm (9,8).
Flags as s42. About 1.5k compiles (race-free tt.tid tags). build/v/mc43 and mc42 deleted.

## Tools
- mk.py S T N OUT: write one s42 lever variant (lev.make on s42/H5b.c).
- ps.py VARIANT LINES OUT: 12 empty-asm pin forms x given lines of the -r arm (inv + cm).
- pm.py OUT: 5 pin forms at the -r arm head on all 275 77/79@61 movers from s42 levA/levB2 (movers.json).
  Results: psA.jsonl (599->676), pmA.jsonl.

## Findings
- On 599->676 the -r arm diff is `mov edx,[68+esp]; lea eax,[1+edx]` vs the original `mov eax; lea edx,[1+eax]`.
  Pins `asm("" :: "a"(i))`, `"a"(i),"d"(i+1)`, `"+a"(i)` (and a register-asm j) restore exactly the original
  -r arm code (fncmp diff identical to H5b) -- but EVERY such pin also reverts the order to H5b's 5 inv
  (`... 79 77 53`). Same on all 204 3-inv movers: 816 results at 5 inv, and every 3-inv result has cm >= (9,6).
- So the RA flip and the 77/79@61 insertion are coupled: the allocation change itself (instruction
  size/copy cost seen by bb-reorder after RA) is part of why the layout moves; pinning RA undoes the move.
  A lever that only raises the -r arm frequency cannot be fixed by RA pins.
- `"+d"(i)` at the arm head keeps 3 inv with cm (9,8) (one line better than 10) -- still not clean.

## Next
- Look for levers that move 77/79 via a different block (not -r arm heat): restrict lev.py targets to
  blocks whose frequency change leaves -r arm RA alone, or compare -fdump-rtl-bbro of pinned vs unpinned
  599->676 to see which trace/copy decision the RA change flips, then reproduce that decision elsewhere.
- Profile splice remains the only matching build.
