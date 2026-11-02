# s128 (attempt 109): NO MATCH. Floor stays f2 18 (s117/best.c). Clean-base family best = 42 (plain).

Clean base c0.c = src/mode_client.c; gen.py builds v/NAME.c from it (P = plain macros with AT labels on,
otherwise BUILD_FDO-style JUMPs active; J1/J2 edit the two FDO JUMP lists; F/Fr/Fu/G dead
__builtin_constant_p feeds (into dsp / any label); E* edits a static clientEraseBlockI copy
(cold/hot labels, dead gotos); Uh hot/cold on u2). run.sh NAME EDITS; l1..l6.txt batches, res.txt ~95 results.
All edits are labels, label attributes, empty asm gotos or dead constant_p gotos: equivalent to src.

## Key finding
- Plain compile (c0 / v/c1, no levers) is f2 42 and ALL 42 lines are in one window (ref lines 420-565):
  the cold blocks placed among the arg-loop arms. The whole switch/case region and everything else
  already matches. b18 (f2 18) differs in exactly the same window. So the "round-4 switch ladder"
  is not where plain/best differ; what is wrong is the order of 4 cold blocks:
  ref: logs(reboot/s) -> u2 ... eout -> efail(ebx) ... u4,u3 ... einv, clientInfo(NULL),
  clientPatches(NULL), u5,u5,u3,u3,u5;  plain: u2 before the two logs, einv right after eout,
  efail after clientPatches(NULL), -r usage(3) (L390) earlier.
## Measured (all worse than 42)
- FDO JUMP lists on: 176; J1 only off 188; both off (labels on) 50; J2 off 90.
- Switch feeds (dead cp into dsp from before NO_MODE_ARG, n=0..6): 48-106 plain, 60-128 FDO.
  Feeds from reboot path 50-60, from u2 arm 184-188, hot dsp 50-60.
- clientEraseBlockI copy alone 42; hot/cold on efail/eout/einv 51-92; dead gotos inside 62-84.
- u2 hot/cold: 42 (inert). Dead feeds from before NO_MODE_ARG into each case/u2/hdd label: 56-126.
Conclusion: the plain compile is a sharp local minimum (every single lever costs >= +6); the profiled
cold-block order (efail next to eout, einv with the NULL calls, u2 after the two logs) needs a
frequency/key change confined to those blocks, which no GIMPLE lever above achieves without
perturbing the loop arms. Next idea: RTL-only levers on the inlined clientEraseBlock branches
(e.g. asm goto from eout to efail with near-zero GIMPLE prob, label placement after inlining).
