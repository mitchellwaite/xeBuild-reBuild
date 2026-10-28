# mode_client, 17th session (2026-10-28): NO MATCH (still 15/16)

Best real result unchanged: s10 best.json on s9/sp.c = fncmp 32 / inv 12 (re-verified, slot r0).

## bb_to_key in gcc 6.2 bb-reorder.c (read from the official repo via the built-in browser)
1. `optimize_function_for_size_p` -> key = bb->index (not our case).
2. `BB_PARTITION == COLD || probably_never_executed_bb_p` -> key BB_FREQ_MAX (10000), start last.
3. priority = cached max EDGE_FREQUENCY over preds that are trace ends (src != ENTRY) OR
   EDGE_DFS_BACK edges; key = -(100*BB_FREQ_MAX + 100*priority + freq).  Otherwise -freq.
Quirks the sims do not model: the cache (bbd[].priority, -1 = not computed) is filled once;
when a trace ends, its last block's successors get `priority = max(cached, EDGE_FREQUENCY(e))`
-- for a block whose cache is still -1 that is THIS edge only (earlier trace-end preds and
DFS_BACK preds are not looked at again); a 0 edge gives priority 0 (no priority).  Re-keying
only happens for successors of the new trace end that sit in a heap.  The fibheap replays
(bYr / f40 histories) already carry the real key events, so for fixed shapes this changes
nothing; it only matters for sims that invent new trace ends.  DFS_BACK priority: none of
the round-4 cold blocks has a back-edge predecessor in our CFG (the loop latch is hot).

## The never-executed bucket is dead (closes s10's point 3 for good)
s10 kenum4 found a PERFECT sim key set using the BB_FREQ_MAX bucket (35 42 53 77 79 + the
-c tail never-executed, 127/117/130 at freq 0 but normal).  s10 assumed this needs count 0.
`re/gcda.py --runs=R` sets the summary run count, and probably_never_executed is
`count * 20 < runs`, so in principle any count cutoff.  But gcc 6.2 maybe_hot_count_p has
`if (profile_info->runs >= count) return false;` ("code executed at most once is not hot"),
so never-executed (count < runs/20) always implies not hot -> size-optimised code.
Sweep (runs.py, s10 best.json): R <= 1e5 identical (32/12); 1e6 fncmp 106; 1e7 166; 1e9 234
with the CFG renumbered.  No R keeps contents while moving cold keys.

## Status of the other plan items
- Step 2 (source shapes changing trace ends) was already covered by s5-s8/s11/s15 shape
  batches (~300 variants): every shape either canonicalises to identical GIMPLE or changes
  contents; no new trace-end lever found this session.
- Step 3: no function-level partitioning (-freorder-blocks-and-partition needs named
  sections/BB_PARTITION; the original has no .text.unlikely split and cold blocks are
  interleaved with hot ones in one function), and the original cold blocks are speed code,
  which rules out an FDO profile that put them in the never bucket (same coupling as above).

## Tools
runs.py SLOT design.json R [extra gcda args]   s10 run.py + --runs=R
Compiles this session: 8.

## Next angle
Only remaining non-frequency term is the priority key (trace-end predecessor).  A source
shape that makes e.g. the HDD-error arm's predecessor (case head) end a trace before round 4
would give it a -(1e6+100p+f) key ahead of usage(2); every shape tried so far either keeps
the case-head trace extending into the arm or changes contents.  Otherwise park at 15/16.
