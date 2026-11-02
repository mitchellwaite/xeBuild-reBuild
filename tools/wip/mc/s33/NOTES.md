# s33: short pass (no new compiles)

Result: NO MATCH. Best remains s29/best_g7b_dup.c (g7b): 7 inversions, fncmp 27.

This pass only reviewed s32's state; the planned work was not run:
- hsim/fany/evedit on the c9>[hdd4,hdd5] history (slots from s18 mkslot/hsim + s32 jT.json design)
- event-neutral bcp injection rescan (s27 injscan/evdiff) on that base
- evdiff of g7b vs c9>[hdd4,hdd5] tail events, to target only the changed round-4 events
- extra `mov [8+esp],ebx` (g7b's only content diff): still unknown whether it is layout-dependent.

Next: do the above in order; start by generating slots for s32's c9>[hdd4,hdd5] design (jT.json)
and running s18/hsim.py + s29/fany.py to find the tail f/P targets.
