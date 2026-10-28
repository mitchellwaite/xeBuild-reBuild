# mode_client, 12th session (2026-10-28): extra-block / fake-edge probes, NO MATCH (still 15/16)

Best real result unchanged: s10 `best.json` on sp.c = fncmp 32 / inv 12.

## Key new tool: zero-byte asm-goto fake edges
`__asm__ goto ("" :::: L1, L2, ...)` emits no bytes but adds real CFG edges that the
crafted profile can load with flow. Placed in its own block (between netConnect's test and
netGetInfo of the switch path, `vX.c`/`vY.c`), mode_client's block *contents* stay identical
(content.py = 0 unbalanced lines; only order changes). This gives direct control over the
frequency (round-4 key) of any register-independent cold block without raising the cases:
- vX: targets = the two HDD errors (hdd4/hdd5 labels). fake 9% -> HDD errors pop before -ip.
- vY: + `c10` (case 10 head; it reloads cinfo from memory, so it is register-safe; cases 4/5
  heads are NOT safe, they use EAX=cinfo).
- vE: + asm goto inside clientEraseBlock after myatoh32 -> Invalid / Failed leaves free
  (mode_client contents identical; ERASE="3>9 4>8 5>7" FAKE="6 7 8 9").
  Outside-range (126) can't be a target (its `[esp+8],ebx` is head-merged into its pred).
- vZ*/vZb/vZc/vZd: asm goto inside the option loop (to free -r/-w/-e from the 50% chain
  halving) flips an RA tie in the -e/-c blocks (`lea edx,[1+eax]; mov eax,edx` ->
  `add eax,1`) at every placement tried -> unusable.
Other register-safe targets (not yet compiled): cases 1,2,3,7,8,9,11,12, default; 117/130
(clientPatches/clientInfo(NULL)); 103 usage(2).

## Simulations (fibheap replay of the real vY bbro history, renumbered to sp bbs: renum.py)
- inject.py: one dummy heap node anywhere in rounds 3/4 (s10 ksearch4 space): baseline 17 ->
  best 2 (dummy pushed in round 3 after case 107/108, key -4). Tie structure is very sensitive.
- fake.py / fake2.py (fake targets free, re-push model slightly wrong for cases) best inv 1
  (only u3cx/u4cx tie at 2 swapped).
- fake3.py / fake4.py (corrected: TX cases keep their priority key when re-pushed; dispatch
  budget <= 86; cases <= 10 to stay round 4; chain 49 >= 2*55 >= 4*61 >= 8*67): best inv 5.
Binding: -ip/-r/-w/-e chain halving (49 <= 10 by the round-3 threshold 10.7, so 61 <= 2,
67 <= 1) leaves ~15 cold blocks on levels 0..2 where only fibheap tie order decides.

## Real compiles
- vX with 0 fake flow: fncmp 64 (order only, case ties reshuffled by the new block).
- search12.py on vY (cases weights + fakes + s11 knobs), ~1000 compiles: best fncmp 48 / inv 16
  (sY1.log.best); case order is not forced well by weights.

## Third angle (thresholds)
STC thresholds are hard-coded arrays in gcc 6.2 bb-reorder.c (branch {400,200,100,0,0},
exec {500,200,50,0,0}) relative to max entry freq/count; no --param moves blocks between
rounds. unlikely-bb-count-fraction only feeds probably_never_executed, which implies
not-hot -> size-optimised code (s10). Not usable.

## Tools
run12.py (variant runner; LOOPX=1 for vZ numbering; fx<sp-bb>=X fake %, cw<tree>=case weight,
ex<n>=erase fake, lx<sp-bb>=loop fake), search12.py, tcfg.py (tree CFG), dumpcfg.py (MCD),
content.py (order-only check), plain.sh (unprofiled fncmp), renum.py, inject.py, fake*.py.
Prep: `export EXTRA='--param builtin-expect-probability=50'; python -c "import sys;sys.path.insert(0,'wip');import mcfdo;mcfdo.prep(r'<abs>\build\mcvY','wip/mc/s12/vY.c')"`.
Note: the standalone clientEraseBlock does not match under any of these profiles (sp too:
its leaves' `add esp; pop; ret` become `jmp`), so integration needs a separate route for it.

## Next angle
Realize a fake-edge design exactly (write a realizer: target integer freqs -> overrides,
iterate against the bbro dump), using more safe targets (case heads 1/2/3/7/8/9/11/12,
117, 130, 103) to break ties by insertion timing; the sim's best (inv 5) is still not 0, so
also look for a register-safe way to free 55/61/67 (a source block in the loop that does
not perturb IRA), or a second X at a different trace time to control tie insertion order.
