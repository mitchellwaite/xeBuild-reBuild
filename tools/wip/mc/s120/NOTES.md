# s120 (attempt 101): NO MATCH. Floor stays 18 (b0.c = s117/best.c).

Model (r4sim/srch.sim on s118/dd/mc.bbro; target = s119's want = sim with {152:1,75:1}, i.e. base with
bb152 moved after bb79):
- h2.py: every single and pair of dummy round-4 heap insertions (key -1/0; all 379 round-4 group
  points + last 60 pre points), every key -1/-2/0 override ("removal") of each round-4 node, and
  dummy+removal and removal+removal pairs: 0 exact hits.
- h3.py: all 3520 single moves of the 22 round-4 'ins' events (any group, any position), and the 117
  neutral moves (layout unchanged) paired with every move of the 152/75/83 insertion: 0 hits.
- h5.py: 600k random sets of 1-4 dummies (keys 1..-8, anywhere in rounds 1-4) plus an optional
  removal: 0 hits (r5_*.txt).
  So within the model no heap shape gives the ref tie order; the ref's round 4 must hold a
  different set of blocks or edges (not just extra or missing zero-byte nodes).
- Issue 1 mapped (bbs.py = post-bbro block list with old bb numbers, b0bbs.txt): u2 usage(2) = bb145
  (inserted from 141, key -2). The two log blocks are the clientEraseBlockI failure logs (LC118 "outside
  system area" / LC117 "Failed to erase" with [8+esp]=ebx). In the ref the ebx-storing LC117 copy is in
  the second group (asm 465), so the difference involves which copy holds `block` in ebx (RA/copy
  identity), not only where the blocks are placed.
Real variants (v1, 90): each of 9 labels (u2,r3x,r5x,w5x,p0,i0,ndl,hc4,hdd5_c) added to each of 10
existing asm gotos. 18 give 18, all byte-identical to b0 (the extra edge has no effect); the JMP(c11) site
gives 19 (an extra jmp); the rest are 24-119. All are equivalent: they only add never-taken empty
asm-goto labels.
