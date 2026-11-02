# s99 (attempt 80): NO MATCH. ~1490 measured variants. Best unchanged: s96/best_s96.c (= b0.c) 26/6/5.

Zero-byte blocks (the s98 idea) - findings:
- They exist at bbro. `asm goto` edge to `zd: __asm__ volatile(""); __builtin_unreachable();` (z01) gives a separate
  0-byte bb; an empty asm volatile before a case label (`case 12: asm volatile(""); AT(c12)`, gv.py zb_*b) gives a
  0-byte block on the switch edge that connect_traces places right before the case block (bytes unchanged there).
  An asm volatile after a label inside a block is merged (no new bb). zb_i1b/p1b/s5b: new block, nothing changes.
- But no realisable dummy is freq-neutral: any extra asm-goto target (gz.py, 40 variants, fncmp 108-334) takes
  tree-level flow (e.g. 146 9->4); a forwarder `zf: asm volatile(""); goto L;` on a cold-label edge (z02,
  gf.py 199 variants, 96-300) moves the cold prediction onto the forwarder (Pat 0->3). Block freqs come from the tree
  estimate; RTL asm-goto edges get uniform probs (EDGE_FREQUENCY 143->127 = 3 while bb 127 freq 0).
- Switch-edge dummies (zb_c2b/c3b/c12b/...) do act as heap-shape levers: CU108 moves before Blk, but the zero group
  scrambles (inv 14-25, fncmp 134-318).
- climb.py (inv objective, 104 asm-volatile levers = AT sites + gp.py positions that changed code): inv 3 reached
  (climb1.log); red.py reduces it to 7 levers (rdbest.c: CU108 Blk -r Fer -w ..., Info right after Pat) but
  fncmp 219: the levers also reorder hot/round-1-3 code (extra jmp/je), so not byte-neutral.
- climb2.py (fncmp objective, 450 evals): nothing below 26 (sideways 26 only).
Tools: gz.py/gz2.py (dummy targets), gv.py (asm before/after AT), gp.py (asm at every stmt boundary, p.out),
gf.py (forwarders), cfg.py (pred/succ from -fdump-rtl-cprop_hardreg-blocks-details, cfg/pre.txt), run.sh/run2.sh,
fo.sh, climb.py/climb2.py/red.py. Note: python-written lists are CRLF; strip \r before shell loops.
Next: a combined objective (inv + count of hot-order changes) climb from rdbest, or constrain levers to ones whose
single effect leaves rounds 1-3 untouched (compare trace lists up to round 3).
