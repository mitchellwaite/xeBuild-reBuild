# s110 (attempt 91): NO MATCH. Best stays s102/best.c = s107/h0.c (f2 24).

New lever classes on h0.c (copy here), flags -O3 -fno-toplevel-reorder -fno-ipa-profile
-fno-reorder-functions --param builtin-expect-probability=50.

1. gen.py -> v/, r1.txt (109 variants). Callee attributes:
   - local callees via asm-label alias decl (`clientXA(...) __asm__("_clientX") __attribute__((A))`,
     TODO(prototype cast)), A in cold/hot/noinline/noclone on clientBinPatch, clientInfo,
     clientPatches, clientWrite, clientKeys, clientRead/WriteBlocks: hot/noinline/noclone inert (24,
     identical asm). cold: clientBinPatch 66, clientInfo 104, clientWriteBlocks 56, rest inert.
     client_usage alias errors (already noreturn; it is the only true noreturn).
   - externs (redeclared with attribute): hot/leaf/nothrow inert everywhere; cold netReboot/
     netDumpNand/sendCompatData inert, sendAvatarData 84, netGetInfo 110, netConnect 170,
     netDisconnect 234, strnicmp 564, log_printf 581; pure strnicmp 800.
   - optimize("...") on mode_client, 40 -f toggles: best no-tree-sink 26 (same three blocks
     misplaced + a cmp moved), no-tree-fre 36, others 46-829; several inert (24).
   Cold-call predictor is a fixed-quantum predictor too: no continuous effect.
2. gen2.py -> v2/, r2.txt (83 variants): __builtin_expect(!!(c),0) on every real condition in
   mode_client (whole and per ||/&& term), and removal of each existing E(). With the param at 50
   expect forces 50/50 (first-match), so it is a strong quantum, not continuous. 29 variants inert
   (24, same asm), next 32 (removing E(reboot) at dtg: clientBinPatch block moves elsewhere), rest 33+.
3. sa2.py / lev2.py: s109 SA space extended with expect site x/xt, cold callee, optimize flag.
   4 chains x 300 (from h0 and from s109's second 24 layout), ~970 real evals (sb_*.log):
   floor 24 in every chain; next 26.
Remaining diff unchanged: clientBinPatch call block, a log_printf(0,..) block and a call+jmp
block. Every tree-level toggle leaves the bbro result for these blocks identical, i.e. the
bb-reorder input that misplaces them is robust; attributes/expects only add quanta.
Semantics: attributes are hints (cold/hot/noinline/leaf/nothrow true for these callees;
pure strnicmp true); expects don't change semantics. Variants are probes only.
