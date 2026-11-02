# s129 (attempt 110): NO MATCH. Floor stays f2 18 (s117/best.c = b18.c here). Plain (c0.c = src) 42.

Tools: hk.py NAME add|del IDX... builds v/NAME.c from the 35 difflib hunks between c0.c and b18.c
(`python hk.py list` names them; 0-3 are the macro block). r.sh = hk.py + f2. gen.py NAME EDIT... (P =
AT labels on; B1..B5 = equivalent restructurings of clientEraseBlock's if/else; R=old|new with @N/@T for
newline/tab). g.sh = gen.py + f2. ks.py/ks2.py = r4sim key-override searches on plain's dump (d_pm/).
res.txt has all ~110 real results.

## 1. best18 lever bisect
- Removing one hunk from b18: only 7 (lu1 label), 32 (cdef constant_p tail) and then 31 are free (18);
  28 costs 1, 6/9/20 cost 6, everything else 32-112 or breaks compile (label dependencies 8/12-16/19/22/24/33).
  Greedy removal: {7,32,31} only. b18 is a tightly coupled equilibrium, not a small lever set plus noise.
- Adding one hunk to plain: inert 4,6,7,8,22 (42); all others 46-133 or need companion hunks.
  So no subset of b18's levers transfers its window gain to plain incrementally.
## 2. Round-4 model of the window (plain dump d_pm, r4sim reproduces exactly)
Window = round-4 traces T32..T51: arms 49(-s..), 55(-r), 61(-w), 67(-e), 73 with single-block cold traces
popped in between. Blocks: 103 u2 (f4), 112/115 reboot logs (f2), 126 eout, 125 efail, 127 einv,
130 clientInfo(NULL), 117 clientPatches(NULL) (all f1), 33 u4, 29 u3, 53 -r usage3.
plain pop: 49 103 112 115 55 126 127 61 130 117 125 33 29 53 67 ...
target (ref): 49 112 115 103 55 126 125 61 33 29 67 127 130 117 ...
=> einv/Info(NULL)/Patches(NULL) must pop after arm 67 (key 0, i.e. freq 0, they are f1 now) and u2 must
drop to <= f2 with the right tie order. r4sim key-override search (1-4 blocks, keys -6..0, 20k random +
exhaustive pairs) never gets closer than distance 4/13 (pairs) - fibheap tie order scrambles everything once
several blocks share a key; setting 127/130/117 = 0 interleaves them with the arms' f0 blocks wrongly.
## 3. RTL/label levers on inlined clientEraseBlock (plain base)
- if/else restructurings B1..B5: 44-62 (B2/B4 move efail into the hot line 300 region).
- asm goto eout->efail 62; Success->efail 116; einv cold/hot label 42 (inert: f1 can't go lower);
  i0/p0 cold labels 44/54; combos 44-62; u2 asm-goto self split 42.
## Conclusion
The window needs three f1 blocks (einv, clientInfo(NULL), clientPatches(NULL)) at f0 plus u2 at <= f2;
labels can't lower them below the predictor floor and key overrides alone can't produce the order.
