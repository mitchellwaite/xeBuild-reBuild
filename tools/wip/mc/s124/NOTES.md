# s124: round-3 priority structure via edge probabilities (NO MATCH, best still f2 18)

Base b18.c (= s117/best.c), f2 18. Variants in a/ (~70 compiled, each with dd_<name>/ dumps).
Scripts: mk.py/run1.sh (-keys condition), mk2.py/run2.sh (-keys arm body), run3.sh (literal replace), bi.py
(block freq/succ/pred from a dump dir). Every edit is a never-taken asm goto, an unused/added label, a
hot/cold label attribute, or `for(;;i++)` -> `klat: i++` (b18N.c, f2 18): all equivalent to src/mode_client.c.

## Key finding: where the frequencies come from
- Block freqs are fixed by the GIMPLE profile_estimate (042t). Asm-goto edges to client_usage (noreturn)
  targets get ~0% there, so cascades to r3x/r5x/w5x change nothing (c2r3/c3r3: 48 [26] .. arm [18]).
  At RTL the asm goto edges are re-split evenly but block freqs are NOT recomputed.
- Asm-goto edges to live targets (k55l/k61l/k67l, klat, ks1/ks2/kn1/kip labels) do get ~30-50% in GIMPLE and
  do end 48's round-3 trace (arm or compare block drops to 13 or below), but each costs 73-300 f2: the
  target gets extra freq and the asm goto leaves an extra (empty) block that forms its own round-3 trace
  (even when the label sits on the real latch, b18N klat: gcc keeps a forwarder for the asm-goto target).
- 48's 71% arm prob is the "call heuristic" (else side starts with strnicmp). 44->48 29% likewise.
  Profiled: 44->48 17.4%, 48 freq 15, arm 9 (57%), 49 7: BOTH successors of 48 under exec_th 10, so 48
  must drop below ~20, i.e. 44->48 must be ~17-21%. No equivalent edit gives that:
  - E() (builtin_expect, param 50) is first-match: exactly 50% (G3: arm 13, f2 206).
  - cold label = ~100/0% (H1: arm freq 0, 48 chains into the else tests, f2 168).
  - hot label = HITRATE ~85% (K1 arm 24; K3 hot label on the -ip side: arm 8 but 49 18 chains; K4 on the
    -s arm: 44->48 ~7%, 48 drops out of round 3; f2 114-142). Hot+cold on both sides cancel.
  - `goto klat;` in the arm: no predictor effect (G1 = b18 identical); `continue;`: f2 102.
  DS needs an extra ~72%-vs-48 predictor on 44 (e.g. opcode-nonequal), which only 44's own compare could carry.
- (a) rok cascade (ork11/ork43 slot -> asm goto to u2/hdd4/hdd5/p0/i0, R1-R8): 47-65. A 15-label cascade (R5)
  hung cc1 (killed).
- (c) r9 -r form, asm goto moved/duplicated (T1,T3,T5,T6): byte-identical to b18_r9 (18); T2 20.

## Table (f2)
p_<target> (call; asm goto; compare): cdef/u2/dsp/c3/fail/dtg 18 (=b18), ndl 29, r3x/r5x/w5x 43,
k55l 172, k61l 270, k67l 280. c2/c3 cascades: r3x 43, w5x 43, k55l 274, k61l 302, k67l 286, m2 104/282.
L1-3 (klat) 101-147; P1/P2/Q1 x {ks1,ks2,kn1,kip} 100-158; N_* (klat on latch) 73-147; G1 18, G2 102,
G3 206; H1 168, H2 18, H3 206; K1 142, K2 54, K3 140, K4 114; R1-4,6-8 47-65; T1/3/5/6 18 (=r9), T2 20.

Conclusion: matching prof's round 3 needs 44->48 ~17% and 48->arm ~57%. Without a profile, GIMPLE heuristics
only give 29/71, 50/50 (expect), ~6/94 (hot label) or ~0/100 (cold label), and asm-goto dilution adds blocks
that wreck the layout elsewhere. Still NO MATCH; best stays s117/best.c at 18.
