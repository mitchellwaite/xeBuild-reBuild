# s109 (attempt 90): NO MATCH. Best stays s102/best.c / s107/h0.c (f2 24).

Joint combination search of the three known lever families on h0.c (hand-inlined erase).
lev.py applies a config: wb3 feed (b=best, 2/1 conj, n=none), wb4 feed conj 0-4 (+ wb4 label),
fail->c11 conj 3-5, k55l conj 0-2, esucc_i->eout_i goto on/off (e), dead-cp feeds to
efail_i/esucc_i/eout_i/einv_i from 8 case sites (pf/ps/po/pv, conj counts pfn/psn).
All levers are dead __builtin_constant_p gotos / labels: semantics identical to src/mode_client.c.

1. g1.py grid: 1584 variants (wb3 x wb4{0,3} x c11{3,4} x k{2,1} x e x efail/esucc site pairs).
   Floor 24 (only the unmodified-feed configs); next 26 (k1 + efail&esucc both from c9),
   30 (24 configs, incl. p_57 family). wb3 alone is inert (b == n). Results g1.out.
2. sa.py simulated annealing (cost f2 + 0.1*dist, T 8.5->0.5, 1-2 lever mutations/step),
   4 chains x 350 from {h0, k1+p55, w2f3, w2f3+k1+e0+p56}, then 4 chains x 450 from a newly
   found second f2-24 layout. ~2500 real evals (logs sa_*.log). Floor 24 in every chain.
   New: a second f2=24 layout c113_e0_k1_pf5_pfn2_po1_ps2_psn1_pv3_wb3n_wb40 (sa_*/) with
   order ...49 139 138 55 108 125 121...: the 145 clientInfo(NULL)/log block moves right, but
   the erase-region blocks swap instead (same 24 count, d=6). Chains seeded there never got <24.
3. Remaining diff of h0 (24): three blocks misplaced - clientBinPatch call (141), a
   log_printf(0,..) block, and a call+jmp near the end; every lever combination fixing one of
   them displaces another by the same amount (quantised feeds).
Conclusion: the lever families do not compose; joint space (grid + SA, ~4000 evals) floors at 24.
