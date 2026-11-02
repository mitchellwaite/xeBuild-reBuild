# s135 (attempt 116): NO MATCH. Bests unchanged: s132/best34.c (34 clean), s117/best.c (18).

Arg-loop restructuring of best34 (and best18) to change the window block set. vars.py = generator
(`python vars.py <base.c> [tag] [names...]`); results vars.out (best34), vars18.out (best18); sources in v/.

## Variants (best34 base, f2; 58 measured)
- Inert (34, same code): rb_setfirst, s_sel/s_neg/s_cont/s_tern, help_elif, help_sep, noenter_cont+reboot_cont
  together, nma_1 (`!mode||!arg`), nma_3, ip_i, r_a/w_a/rw_a, e_a, i_neg/p_neg, i_pre/p_pre, keys_order, v_inv,
  while-loop, v_a, g3_ec/g3_rw (shared `bad3:` usage site), g5_rw/g5_ec, cv_ip (code variable).
  gcc canonicalises all of these (tail merging/ifcvt), block set unchanged.
- Worse: rb_ifelse 42, rb_flag 46, s_flag 118, nma_2 (`!arg||!mode`) 38, g3_ip 39, g3_eb 38, cv_r 57,
  cv_rw/cv_ec 47, g3_all 168, g5_all 151; option-order swaps: sw_r_w 38, sw_e_c 38, sw_i_p 46, sw_keys_ip 74,
  sw_c_i 77, sw_s_keys 94, sw_rb_wb 108, sw_bp_rb 142, sw_wb_eb 172, sw_reboot_bp 207; single continue-splits
  (reboot_cont 497, s_contchain 586, ip_cont 602, v_first 244, help_a 242) break the chain shape badly.
- best18 base (vars18.out): nothing below 18 (nma_2 22, rb_ifelse 26, sw_i_p/rb_flag 30); many s-arm forms
  don't apply (best18's -s arm differs).
## Climbs on top (s134 gen.py/climb.py copies in cl_*)
- cl_sw_r_w: 7432 singles + 60-pairs: floor 38 (=its base), no improvement.
- cl_sw_e_c: 115 singles before stop, floor 38. cl_nma_2 not run.
## Semantics
Swaps only between tests with distinct non-prefix strings (at most one matches; -reboot kept before -r,
-rb/-wb/-eb before -r/-w/-e, -keys before... no prefix overlap with -s/-ip). goto-shared usage calls pass
the same code/arg; continue-splits preserve else-chain (each arm ends the iteration). All equivalent.
## Conclusion
Source-level reshaping of the arg loop either normalises away in GIMPLE (inert) or perturbs the layout
away from the reference; none moves the window toward the target order.
