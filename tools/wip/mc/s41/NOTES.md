# s41: trace-frequency levers around the shared usage blocks (plain compile, no profile)

Result: NO MATCH. Best unchanged: H5b.c (copy of s40/H5b.c) 5 inv / fncmp 65 diff lines / cm (0,8).
Flags: -Isrc -O3 -fno-toplevel-reorder -fno-ipa-profile -fno-reorder-functions --param builtin-expect-probability=50.
Short session (~20 compiles). gen.py / gen2.py regenerate the variants from H5b.c.

## (a) E()/expect-0 on option-loop tests (-eb/-ip/-keys/-s/-wb), gen.py
| variant | cm | fncmp lines |
|---|---|---|
| -eb E removed | (0,18) | 186 |
| -eb expect(.,0) | (0,8) | 65 (byte-identical to H5b: E is only a tie-breaker at prob 50) |
| -ip E / expect0 | (0,14) | 148 |
| -keys E / expect0 | (2,22) | 340 |
| -s E / expect0 | (0,14) | 324 |
| -ip,-keys,-s E | (4,22) | 501 |
| -wb E removed | (0,18) | 270 |
| -eb plain + -ip expect0 | (0,12) | 150 |
## (b) E() on -r/-w/-e/-c (55/61/67 order), gen2.py
All single toggles (0,10)/78 lines; -r+-w both E (0,10)/90. None beats H5b.

## Conclusion
expect toggles near 53/55/61 only worsen content/order; no lever reached the round-2 trace split.
Untried: (c) switch / flag+break shapes, (d) dx hsim ranking of relocations.
