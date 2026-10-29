# mode_client, 16th session (2026-10-28): NO MATCH (still 15/16)

Best real result unchanged: s10 best.json on s9/sp.c = fncmp 32 / inv 12 (also on s15 pinF.c, build/mcpF).

## Step 1: why the three -wb usage blocks stop merging at exit >= 3.5% (pinF)
Not a merge pass: it is IRA. `dumpall.sh` (full -fdump-rtl-all-blocks/-tree-all of a slot) at 2% vs 4%:
jump2 crossjumps 18->32, 22->36, 24->38 (-bp/-wb usage(3/4/5)) only at 2%. At 4% the -wb blocks
start with `mov ebp,ecx` (bbins.py on csa): pseudo r167 (i in -wb) gets bp in region l0 (loop
exits = the usage blocks) instead of cx. IRA push order: at 2% r538 (&count, hoisted out of the
loop for -rb getArgs) is GENERAL_REGS and is pushed as a potential spill with r88/r90(mode)
first, then a43(r167,l0) becomes colorable and pops before r181 (i+2) / r172 (a), getting cx.
At 4% r538 becomes NO_REGS (its preheader def got 2x more expensive), r90's spill priority rises
(pri 3 -> 8, fewer excess-pressure points), and a43 itself (cost 296, pri 6) is chosen as the
potential spill; r181/r172 then take cx and a43 gets bp.
- a43's cost is REG_FREQ-floored (usage blocks freq < 10): scaling the -wb usage edges x8 doesn't move it.
- extra "c"(i) pins in -wb (pG1/pG2/pG3.c): hard-reg conflicts don't reach the l0 caps; no fix.
- -rb probability (mode_client:24>25) 60% gives content 0 at 4% but not robustly (5-6%: 12/32).

## Step 2 (the decisive one): the exit can't be raised by more than ~1.7x anyway
Raising the loop exit only buys key resolution if every loop block near the round thresholds
(0.5/0.2/0.05 x entry freq E) scales with E. Those are the else-if halving chain
(cfg.sh on a slot): 8 -> 9(-noenter)/10 50:50, 10 -> 11 (71%) / 14 (29%), 14 -> 15 (-bp) / 23,
23 -> 24 (-rb) / 25, 25 -> 26 (-wb) / 37 ... The hot layout needs the tie/ordering
p(9) >= p(10), p(11) >= p(14), p(15) >= p(23), p(24) >= p(25) (measured: 7>9 = 55..70% breaks
trace 1 at line 23; 9>13 = 50% breaks at line 1). So 25 <= H/2 * 1/2 * 1/4 vs 355 now -> scale
<= 1.72 (exit <= ~3.4%). Consistent scaling at 9>13=40 (exit 2.76, cold edges x1.38, exs.py)
keeps rounds 1-3 except two fixable blocks (12 = -s log, 5 = help usage), content 0.
Sim at that resolution (fake6.py, FULL CHAIN CAPC=7 X2=121 TX2=112,115, VMAX 18 ~ 1.7x;
f6v18_*.out, 4 seeds): best 2/3/2/2 inversions even with every realizability cap dropped.
So the higher-exit route cannot reach 0; s15's 3x requirement is structurally unavailable.

## Next angle
Something other than integer frequency keys must order the cold round-4 traces (e.g. a source
shape that changes which trace end a cold block's predecessor is, i.e. the bb_to_key priority
term), or a different max-frequency block (header) structure. Profile-only routes are exhausted.

## Tools (all take slots in build/mcpF = mcfdo prep of tools/wip/mc/s15/pinF.c, EXTRA param 50)
ex.py SLOT EXIT [k=v]  best.json + exit + overrides; prints fncmp inv pre content
exr.py                 same + first diff hunk;  exs.py: also scales in-loop cold edges (SC env)
dumpall.sh SLOTDIR     all rtl/tree dumps in the slot (profile found: cwd = slot)
cfg.sh SLOTDIR lo hi   pre-bbro CFG with probabilities (cfgdump.py)
bbins.py DUMP bb..     compact post-reload insns per block;  nbb.py: per-pass size diff
Compiles this session: ~45 profiled + 3 plain; sims: 4.
