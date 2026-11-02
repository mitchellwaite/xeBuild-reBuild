# s143: LC114 (clientEraseBlockI einv, bb146) freq levers from s142/front28.c (f2 28)

t.sh NAME (f2 + erase freqs + compiled r4 order), dump.sh, srch.py (r4sim key-override search on the
tail after block 143, target 62 33 29 69 146 128 151 35 42 53 79 81).

## Levers (einv freq / f2)
- a1 uncold einv: 4 / 96 (success drops to 1). a2/a3 extra bcp conjuncts on the dead einv gotos: 2 / 90.
  a4/a5 one conjunct only: 4,3 / 96.
- b1/b5 dead gotos -> cold trampoline inside `if (bcp)`: still 0 / 28 (inert). b3 cold trampoline as
  its own block: 6 / 103. b2 `|| bcp` on `block != -1`: 103. b4 `if (block + 1)`: inert.
- c2 dead gotos -> `einvd: cold; goto einv;` at function end: einv 0 (cold propagates through forwarder).
- c3 dead gotos -> efail: einv 1 but efail gains preds, 96.
- **c1/c4** dead gotos -> separate cold dead duplicate `einvd: cold; log_printf(same string)` after
  `return;`: **einv freq 1 (= P), rest of clientEraseBlockI unchanged (4/3/2/2)**, f2 76: 146 now pops
  at key -1 *before* 33 29 69 (target: right after 69), and the tail becomes 79 75 128 81 83 42 151 35 53.
  Same ordering as s142 q2 - so freq 1 is reachable without touching the front's freqs; the problem is
  purely the round-4 fibheap order of the key -1/0 ties.
## r4sim on c1
srch.py singles/pairs over {146,128,151,35,42,53,79,81,75,83,69} x {0..-3}: floor 6 of 12 tail slots.
146 always pops either before 33 (key -1) or after the tail starts (key 0); no key assignment puts it
between 69 and 128 with the P tail. Matching needs a different heap shape (insertion order / extra
consolidation pops in rounds 1-3), not keys. Goal 3 (gen/climb from front28/c1) not run.
## Semantics
c1: the dead `bcp` gotos now target an unreachable duplicate of the einv message; bcp folds false.
## Conclusion
NO MATCH, best f2 still 16 (s141/best16.c). c1.c is front28 + exact P freqs in clientEraseBlockI.
