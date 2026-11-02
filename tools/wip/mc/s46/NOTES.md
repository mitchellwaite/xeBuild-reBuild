# s46: crossjump survivor levers (plain compile, no profile)

Result: NO MATCH. Best clean unchanged: s42/H5b.c (s42 m.py: 5 inv / fncmp 40 / cm (0,8)).
~350 compiles. P.c measures 6 inv / fncmp 40 / cm (0,8) with s42/m.py.

## gcc-6.2 cfgcleanup.c (read via built-in browser, javascript innerText works past Anubis)
- try_crossjump_bb(EXIT): walks EXIT preds in order; for e (only if e is src's first succ) it tries
  every e2 with e->src->index <= e2->src->index, try_crossjump_to_edge(mode, e, e2, dir_both); first
  success restarts the scan (ix = 0). A fallthru pred is tried first and never redirected.
- try_crossjump_to_edge: src1 = e's block (lower index) is redirected; src2 (higher index) survives
  (redirect_to = src2, or split_block(src2) if the match starts mid-block); swapped only if
  flow_find_cross_jump returns dir_backward. So the survivor of a matching group = its highest index.
  Counts/frequencies of src1 are added to the survivor.

## Levers tested (tools: j2.py = jump2 crossjump lines; scan1.py, scan2.py over m.py, race-free tags)
- A1.c: P.c with the -r arm tails moved to `goto rq3/rq5` + dead `if (0) { rq3: ...; rq5: ...; }` at the
  loop end -> the -r tails become the eax-group survivors (104/105). bbro order/inv/fncmp/cm identical to P
  (6/40/(0,8)). A2 (rq5 first) fncmp 46.
- scan1: dead tail block at every statement position 599..725, both orders (206 compiles): best 6/40, mostly 6/40 or 6/52.
- scan2 / B670.c: -w/-e/-c tails moved into a dead block placed before the -r arm (170 compiles):
  the in-place -r tails survive ("59 to 65", "60 to 67"), still 6/40, order unchanged (...42 79 77 53...).
- Conclusion: which block survives / where it sits does NOT move 77/79 (the clientWriteBlocks /
  clientBinPatch switch-case blocks in bbro numbering). The U effect must come from the pred-set
  (edx tails of -bp/-wb arms 46/57 joining the -r trace) or from the RA/renumbering side effects,
  not from survivor choice. Merging 46/57 into the -r tails while -r keeps eax is impossible
  content-preservingly (different index registers).

## Remaining diffs of A1 vs original (fncmp 40)
- two log_printf blocks (126/125/55 region) placed early; the -r/-w arm `cmp esi,edx` scheduled after
  the argv load/test; tails order (eax,5)(eax,3)(edx,3) vs original (edx,3)(eax,3)(eax,5).

## Next
- Task 3 not reached. Check bbro trace keys for 77/79 directly (hsim) in U vs B670 to see which
  edge/pred set pushes them, instead of crossjump survivor levers.
- Scratch build/v/mc46 and build/v/mc42 deleted.
