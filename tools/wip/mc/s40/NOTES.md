# s40: usage-call shapes, block map, NONR beam (plain compile, no profile)

Result: NO MATCH. Best unchanged: s35 H5b.c 5 inv / fncmp 40 / cm (0,8). ~2600 compiles. build/v/mc40 deleted.
Tools copied from s39 (mc39 -> mc40). New: mk40.py, mk41.py, mk42.py (regenerate the shapes below from H5b.c).

## Block map (sp numbering -> H5b.c source, from slot bbro final listing)
| sp | block | H5b.c lines |
|---|---|---|
| 29 usage:3:cx | -wb usage(3) | 629 (preds: test 628) |
| 33 usage:4:cx | -wb usage(4) | 634 (test 633) |
| 35 usage:5:cx | -wb usage(5) | 637 |
| 42 usage:5:dx | -eb usage(5) | 646 |
| 53 usage:3:dx | shared usage(3) of -eb (643) and -ip (664) | 664 |
| 77 usage:3:ax | shared usage(3) of -r/-w/-e/-c (672/681/689/697) | 698 |
| 79 usage:5:ax | shared usage(5) of -r/-w/-e/-c | 700 |
| 55/61/67 | strnicmp -r / -w / -e tests | else-if chain |
Insertion events (all shapes below identical): 53 inserted round 2 from loop trace 1038 ('next');
55,77,79 inserted round 4 at 55; 61 at 49; 67 at 61.

## Shapes (on H5b)
| shape | cm | inv | round-4 events |
|---|---|---|---|
| __builtin_unreachable() after every loop usage call (U1) / usage(3) only (U2) | (0,8) | 5 | identical (neutral) |
| `if(!c) goto ok; usage; ok:` inverted (G0-7) | (0,8) | 5 | identical |
| `if(__builtin_expect(!c,v)); else usage` per site (I/Z, v=0/1 same) | sites 5-7 (0,10) 5; 4 (0,16) 29; 0-3 content | changed in round 2/4, but 53/77/79/55/61/67 insertions unchanged |
| combos C56/C57/C67/C567 | (0,10) | 5 (C567 fncmp 46, inv 6 in m.py) | same |
| static noinline noreturn wrapper (W1 all / W3 usage3) | (43,16)/(6,10) | content changes (calls cuw) | - |
| volatile function pointer for usage(3) (F1) | (179,28) | 15 | - |
## NONR beam
gs2.py st_H5b.json with NONR=1, 2 rounds beam 2 (~2560 compiles, gN.log): best 5 inv, fncmp 156. Floor 5.

## Conclusion
Usage-call shapes are either gimple-normalised (no change) or change content; none moves 53's round-2
insertion from the option-loop trace or 77/79's insertion at 55. Same conclusion as s38/s39.
Profile splice remains the only matching build.
