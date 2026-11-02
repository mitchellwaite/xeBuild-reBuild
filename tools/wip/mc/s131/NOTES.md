# s131 (attempt 112): NO MATCH. Local freq levers work on einv/Info(NULL)/Patches(NULL) but not u2. Best plain 42 (unchanged), b18 18.

Tools: gen.py (s129's, base from $BASE, R edits split on `#|#`), vars.sh / vars18.sh = named edits, g.sh NAME EDIT...
= gen + f2 + dump + fq.py (freq of u2/i0/p0/einv/efail/eout found by source line -> bbro call_insn -> reordered freq;
second number pair = original bb:freq). grid.sh = 216-combo grid (grid_c0.log). ks.py = s129 key search on dd/NAME.
res.txt = all ~270 measured variants.

## Where the f1/f4 come from (dumps: -fdump-tree-all-blocks-details)
- Patches(NULL)/Info(NULL): switch arm 4.46 x pointer-eq 0.3 = 1.34. einv: call site 4 x callee else-arm 0.34.
- A folded test (cp(x) folds at dom2) does NOT lower its target: gimple_merge_blocks keeps the predecessor's
  frequency, so `if (a && !cp(argc)) T` gives T the freq of the cp block again (a1: pe 0, RTL 1).
  Working forms: compute `int k = __builtin_constant_p(argc|block)` earlier (inert alone: c0 42), then
  `if (arg == dummy && !k)` / `} else if (!k) einv` -> the test block becomes an empty forwarder, removed
  without touching the target freq. Also works: forced label (`l: asm("" :: "i"(&&l))`, but blocks inlining
  of clientEraseBlock) or a 2nd predecessor. E4 (all three) = einv/i0/p0 0, eout/efail unchanged.
- u2 (client_usage(2)) is 0 in profile_estimate; its RTL 4 = the dom2 jump-thread of the zero-iteration path
  (entry guard, loop-exit 2% floor x preheader 214 = 4.28) into a forwarder that PRE's cfgcleanup merges with
  u2 (keeps forwarder freq). So u2 = 0.02 x preheader->entry edge: not locally adjustable.
  - asm goto feed into u2 (from a 0-freq block) blocks the merge -> u2 0 (f_FI 48); feeds from f4 blocks add 0
    (noreturn predictor). Extra loop exits/continue raise u2 (2% floor per exit; 188-230).
  - Outer back edge `again:` + `if (k) goto again` to cut entry/preheader: loop-branch 90% predictor; from
    netReboot block u2 -> 2 (m4) but rok/reboot tail reorders (172); other placements 164-289.

## Results (plain): every lever combo >= 42
grid best: MK alone 42, K12 44, K7+K12 44, einv+K12 46, einv+K7+K12+u2feed (all 4 targets at 0) 48, E1-forms 50-52.
With all four targets moved the diff is still only the window (425-563); u2 at 0 lands last (ref has it
right after the first reboot log) and r4sim on that dump with 103=-1..-3 still leaves 55 before 115 and
29/33 swapped (ks.py distance 4-5).  b18: einv k-lever 32, K7/K12/u2 feed inert (18; its p0/i0 already 0, u2 2).
## Conclusion
einv/clientInfo(NULL)/clientPatches(NULL) can be driven to 0 locally and cheaply (pre-computed cp k + `&& !k`),
but u2's 4 is a jump-thread artefact tied to entry/preheader ratio, and even with u2 at the right key the
window's tie order (55/115, 29/33, 77/35 intrusions) does not match. No transferable gain to b18.
