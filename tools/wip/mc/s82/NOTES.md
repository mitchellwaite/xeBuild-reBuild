# s82 (attempt 63): insertion-order search + lever climb

Base b0.c = s81/best_s81.c (fncmp 68, sig2 8). **New best: best60.c, fncmp 60, sig2 10** (fncmp-better,
order-equal: bbro inversions vs target 15 like b0). Diff vs b0: dead `if (bcp(block+7)) goto efail;` at esucc,
lu1 loop-head feed dropped, k61l `(i+20)==3` feed dropped (all bcp-dead / label-only; braces intact).
Not adopted as "obviously better": sig2 8 -> 10 and the bbro tail is not closer.

## Tools
- osrch.py DUMP REPS: SA over round-4 key overrides + round-3 push order + per-trace insert order (r4sim replay).
- ks.py NAME REPS RANGE ITERS: key-only SA; target block ids resolved per variant by tmap.py (source-line based:
  u2/wb3/wb4/wb5/eb5/ip3/c3/c5 CU blocks, LC labels, cold Info/Pat = last occurrence). ks2/ks3 variants.
- bf.py: brute force of the f0 back group with the front fixed.
- lev.py / climb.py: parametrised levers (feed conjunct counts for u2,k55l,wb3,wb4(new label),lu1,k67l,k61l,
  esucc->efail, eerase->eout, new labelled CUs ip3/c3/c5/eb5/wb5) + coordinate climb on (fncmp, inversions).
  Logs: climb_2.log (y*), climb_3.log (x*); w* run results in w*.c/.d.

## Findings
- osrch with push/insert-order moves reaches 0 inversions on b0's history (e.g. keys 107:-4 33:-2 139:-4
  138:-3 140:-1 127:-1 55:-4 61:-3 68:-2, round-3 push 53 first), cost 11 changes; key-only never reaches 0.
- With *distinct* front keys (125=-7 121=-6 107=-5 55=-4 139=-3 138=-3 61=-2 33=-2 29=-1 68=-1) the front
  (inv..-e) is exact; the back f0 group (Inv Pat Info 35 42 53 78 80 -c) is the hard part: bf.py over {0,-1}
  for those 9 gives >= 9 inversions. These are tie-structure (fib-heap) orders, not freq levels. The original is
  an FDO build, where these blocks are all count 0: their order there is pure heap structure (key 0 / prio), so
  matching it via guessed freqs needs the same heap history, not just keys.
- Measured levers (~140 compiles: v1-v17, w1-w50, x1-x27, y1-y45):
  u2 1-conj: u2 f4 free (fncmp same), u2 3/0 conj very bad; k55l 3-conj (on u2=1): -r f3 right after u2, front
  inv..-r exact (v8, fncmp 68); k55l 1-conj: -r f5 (bad). wb4 label+feed: CU33 f2-4 but jumps ahead (76).
  esucc->efail: Fer f3 (60 with k61/lu1 off). eerase->eout 1-conj: Blk f4. New labelled CU feeds (ip3/c3/c5/
  eb5/wb5) cost ~+250 fncmp at any strength (the label stops a CU merge) -> unusable.
- Climb plateau at 60 (all single moves >= 60).

Next: the back group needs the heap *structure* of the original; consider making Inv/Pat/Info prioritised
(trace-end preds with edge freq 0 -> key -1000000) instead of freq tweaks, and simulate that first with r4sim
(ks3.py tried {0,-1000000} on b0 history without success; needs prio for the right subset + insertion timing).
