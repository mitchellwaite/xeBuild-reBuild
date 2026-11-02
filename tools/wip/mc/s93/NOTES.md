# s93 (attempt 74): NO MATCH. ~62 variants (log.txt; scripts b1-b6.sh, bases e6/e11/b08/b08x).
Best fncmp still e6 (36/10/8). No new best.
- a01-a20: edges in clientEraseBlockI on e6/e11. Any einv edge at eerase (asm goto or constant_p, 1-3 conjuncts)
  gives e11's state (-w before Blk, CU81 early, inv 18). eout/esucc edges to eout: much worse. Removing einv cold: much worse.
- b08 = e11 with wb3 hint reduced to 2 conjuncts (drop `__builtin_constant_p(i + 62)`): fncmp 42 inv 9,
  order -r Fer CU29 CU33 Blk -w -e Inv Pat .. Info -> Inv/Pat/Info now in target order, CU81 back late.
  Remaining for b08: Blk must precede Fer, -w must precede CU29/CU33.
- On b08: esucc/eout/efail edges (d01-d08, g01-g10, separate efail label b08x) all worse or inert;
  r5x position, k55/k67 conjuncts, w5x extras inert or worse; u2 conjunct changes much worse.
- e6 + wb3 2-conj (c01): Blk ok but Info/Inv wrong (inv 11); 1-conj (c03) fncmp 34 inv 18.
Next idea: from b08, find a Blk/Fer lever that doesn't involve the esucc->einv edge (which on b08 hurts, c06).
