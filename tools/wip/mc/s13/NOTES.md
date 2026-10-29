# mode_client, 13th session (2026-10-28): second fake source + integration route, NO MATCH (15/16)

Best real result unchanged: s10 best.json on s9/sp.c = fncmp 32 / inv 12.

## Second asm-goto source (angle 2), simulation only
fake5.py = s12 fake4.py + a second fake block X2 (env X2=<block visited just before it>,
TX2=<its targets>; targets pushed into the current heap in round 4, `new` before). Sweep:
X2 in {121,122,107,109,129,110,108,116,119,113,120,128,132,115,112,103,126,125} (blocks outside
the option loop) x TX2 in {117,130 | 117,130,103 | 112,115} (removed from X's TX), 60 hill-climb
rounds each (f5.out, ~44 of 54 runs finished): floor stays **5 inversions** (13 runs), never below.
Remaining inversions are always among the option-loop usage blocks 29/33/61/67 (and 77 vs 42/53),
which sit at freq 0..2 because of the -ip/-r/-w/-e halving chain capped by the round-3 threshold.
Fake targets outside the loop cannot reorder those: a second source does not help.
Tie order (angle 4) is already exact: tools/wip/fibsim.py replays gcc 6's fibonacci_heap, so equal-key
order is modelled, and the sims already explore it.

## Integration route for clientEraseBlock (angle 5)
src/mode_client.c's clientEraseBlock matches unprofiled (fncmp 0) and its body is identical
to sp.c's except extern literal names (sp.c's standalone diff 10 lines = literal/tail shape).
So when a profiled mode_client matches: emit everything from the plain compile and only
mode_client from the FDO compile, like build's loadBlFiles:
  1. tools/wip/mcwhole.py sp.c -> whole C with mc_<addr> arrays (check its .rdata end, 3 bytes short before);
  2. FDO compile of that file (mcfdo prep/score flags, -ftoplevel-reorder per build notes) -> -S;
  3. `tools/re/splice.py --whole <plain -S> <out.s> _mode_client=<FDO -S>` (build.sh line 152 path).
clientEraseBlock is never taken from the profiled compile.

## Next angle
Only a loop-side change that frees 55/61/67 from the halving chain without touching IRA can
get below 5 in simulation; every asm-goto in the loop tried in s12 flipped the -e/-c RA tie.
Otherwise park at 15/16.
