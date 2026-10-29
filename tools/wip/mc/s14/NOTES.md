# mode_client, 14th session (2026-10-28): NO MATCH (still 15/16)

Best real result unchanged: s10 best.json on s9/sp.c = fncmp 32 / inv 12.

## Experiment: fake edges from outside the loop INTO the option-loop usage blocks
vW.c = s12 vY.c + labels on the client_usage(3, argv[i]) calls of -ip/-r/-w/-e and those
labels added to vY's out-of-loop asm goto (idea: give 29/33/61/67-type usage blocks
flow directly, bypassing the -ip/-r/-w/-e halving chain, with no asm goto in the loop).
Unprofiled (s12/plain.sh + content.py): vY = 14 unbalanced lines, vW = 24. The extra
predecessors stop the usage(3) blocks being shared/merged (literal `offset l...` x5) and
re-tie the -r/-w RA (`lea edx,[1+eax]` / `[68+esp]` reloads). Negative: targets inside
the loop perturb contents even when the asm goto sits outside it.

Counts: 1 real compile (unprofiled), 0 new simulations.

## Next angle
Not tried yet: a simulator variant where 55/61/67/29/33 frequencies are free variables
(step 2 of the plan) to check whether freeing them reaches 0 inversions at all; then
loop-side source shapes (separate ifs / continue / helper inlining) checked with
plain.sh + content.py before profiling.
