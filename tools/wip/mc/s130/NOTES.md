# s130 (attempt 111): NO MATCH. Global frequency scaling via dead hot loops. Floor stays f2 18 (b18.c = s117/best.c), plain 42.

Tools: mk.sh / mk2.sh / mk4.sh BASE NAME ... insert `if (__builtin_constant_p(argc)[&& ...]) { dead loop(s) }`
after log_set_name in mode_client (mk4: nested known-trip loops T x N, the fine knob); mk3.sh puts it in
clientEraseBlock. dump.sh NAME -> dd/NAME/{mc.pe (profile_estimate-blocks-details), mc.bbro}. fr.py = round-4
trace starts, keys.py = pre-round-4 keys of chosen blocks. res.txt = all ~75 measured variants.

## Mechanism (confirmed)
- profile_estimate: plain's max is the argv-loop body (9800, entry 214; loop predicted ~46x). The dead loop
  survives profile_estimate (constant_p(argc) folds late, ~dom2) and if its body beats 9800 every block is
  rescaled; RTL/bbro keys reflect the scaling (q1: keys x0.93). Asm has no trace of the loop (guard folds to 0).
- Knob: known-trip nested loops give max = preheader*T*N (cap 99% = x100 per unknown loop);
  scale ~ 9157/(100*T*N) with guard constant_p(argc) alone (preheader = entry/2).
- constant_p(sblock) in clientEraseBlock folds early (inert); constant_p(block) there survives but the callee
  is IPA-inlined with ratio scaling -> no rounding effect (c0 111 from size/inlining change only, N-independent).

## Results
- Below the scaling threshold (T*N <~ 85): inert (b18 18, c0 42-50; the extra guard alone costs c0 0-8).
- Any real scaling: monotonically worse. s~0.95: c0 48-52, b18 64; s~0.8: 72-112; s~0.5: 90-120; s<0.3: 120-240.
  Diffs start in the argv loop: IRA costs are frequency-weighted, so rescaling reshuffles register choice
  everywhere, not just the bbro window.
- Window keys vs scale (c0): u4 (33) drops to 0 already at s~0.8, u3 (29) at ~0.55, before u2 (103) reaches
  -2 (s~0.6). The reference order needs 33/29 to stay above the einv/Info(NULL)/Patches(NULL) blocks, so a
  uniform scale can't produce it; scaled pop orders (fr.py c0t13/c0t20) scramble further via ties at 0.
## Conclusion
Global scaling/rounding is not a lever: it can't separate the f1 blocks the way the reference needs, and it
perturbs IRA across the whole function. Dead.
