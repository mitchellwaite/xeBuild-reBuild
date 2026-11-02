# s44: where the -r arm register swap moves 77/79 (plain compile, no profile)

Result: NO MATCH. Best clean unchanged: s42/H5b.c (5 inv / fncmp 40 / cm (0,8)). ~6 compiles (diagnosis only).
U.c = s43 mk.py 599 676 1 (3 inv, -r arm edx form); P.c = U.c + `__asm__("" :: "a"(i));` on line 671 (5 inv, eax form).
Tools: sig.py DUMP (per-pass bb:symbol signature of mode_client), blk.py DUMP BB.. (print insns of blocks).

## Finding (task 1): the decision is cross-jumping in jump2, not bb-reorder
- -fdump-rtl-all, compare bb/symbol signatures pass by pass: identical through csa (265), first DIFF at
  266r.jump2 (post-reload cfgcleanup with CLEANUP_CROSSJUMP); bbro's own decisions are then identical
  except block numbering/which block holds the merged tail.
- The candidates are the noreturn `client_usage(3|5, argv[i])` tails (4 insns: load argv[i*4], store arg,
  store const, call). Index register decides who matches whom:
  - U (edx): -r arm tails bb63(3)/bb65(5) use dx, as do bb46(5)/bb57(3) -> "Cross jumping from bb 46 to 65",
    "57 to 63"; 87/89 (ax) stay alone.
  - P (eax): -r arm tails use ax -> "63 to 87", "65 to 89"; 46/57 stay alone.
- In bbro the merged tail's edges then hang off a different trace: U pushes 77/79 from the 61..65 trace
  (= the "77/79@61" insertion), P from the 55..60 trace (H5b order). Trace keys/frequencies are equal.
- Original binary tails order: (ecx,4)(ecx,3)(ecx,5)(edx,5)(edx,3)(eax,3)(eax,5).
  U: ...(edx,5)(edx,3)(eax,5)(eax,3)   P: ...(edx,5)(eax,5)(eax,3)(edx,3).
  So the original has P's crossjump pairing (eax tails merged with -r arm) but a layout where the dx
  tails 46/57 sit together before the eax pair.

## Next
- Levers should target the crossjump survivor / EXIT-pred edge order (try_crossjump_bb walks EXIT preds;
  which of a matching pair becomes the survivor and which block index the merged tail keeps), not the -r
  arm heat: e.g. reorder the two `client_usage(..., argv[i])` calls of the -r arm vs. the 87/89 arm in the
  source, or make 46/57 the jump target, keeping eax in -r. Read cfgcleanup.c try_crossjump_bb /
  try_crossjump_to_edge (gcc 6.2) for the survivor rule (official repo only).
- Tasks 2-4 not started this session. Profile splice remains the only matching build.
- Scratch build/v/mc44 (dumps) left in place: the rm was blocked by a safety check; delete it by hand.
