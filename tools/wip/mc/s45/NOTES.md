# s45: crossjump survivor rule (short session)

Result: NO MATCH. Best clean unchanged: s42/H5b.c (5 inv / fncmp 40 / cm (0,8)).
- build/v/mc44 deleted (literal path).
- Task 1: gcc.gnu.org git (cfgcleanup.c @ releases/gcc-6.2.0) returned an Anubis "Access Denied" page to
  WebFetch; source not read. From memory (unverified): try_crossjump_bb walks the preds of the common
  successor (EXIT here) in edge-vector order, inner loop over all other preds; try_crossjump_to_edge(e1,e2)
  redirects src1 (outer edge's block) into src2, splitting src2 at the match start. "from 46 to 65" =>
  46's edge is earlier in EXIT's pred vector than 65's; survivor = later pred. Pred order = edge creation
  order (noreturn call -> EXIT edges made at RTL expand / find_many_sub_basic_blocks in source order),
  so source statement order of client_usage calls is the expected lever. Verify against the real source
  (try a different mirror, e.g. github.com/gcc-mirror/gcc blob releases/gcc-6.2.0) before relying on it.
- Tasks 2-3 not run. Note: plain `fncmp.py <c> mode_client -I<repo>/src` prints ~1670 diff lines for both
  H5b and P (the "fncmp 40" metric of s42 uses different flags/tooling; reuse s42 cm.py/ev.py setup).
