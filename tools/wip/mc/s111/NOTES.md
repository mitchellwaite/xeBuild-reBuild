# s111 (attempt 92): NO MATCH. Best stays s102/best.c (f2 24).

Reverse-engineering from the profiled (matching) build.
- fdo.sh: build.sh's fdo compile of src/mode_client.c (-DBUILD_FDO, mode_client.prof,
  align-loop-iterations=100) with -fdump-rtl-bbro-details -> pf/mc.bbro, pf/bbinfo.txt.
  s86/r4sim.py reproduces its round-4 pop order exactly.
- Block map prof->best in wp.py (M). Prof round-4 order, in best's numbering:
  142 96 113 116 119 122 115 129 131 134 141 126 147 49 125 121 108 55 139 138 62 33 29 69 140 127 145 35 42 53 79 81 75 83 88 154 97 155 98 93 95
- Differences in the bb-reorder input:
  * Prof keys form a priority ladder: (prio,freq) 142 (9,10), 113/116 (8,9), 119/122 (8,8),
    115/129 (7,9), 131 (7,8), 134 (7,7), 141 (6,10), 126 (6,9), 147 (6,8), 49 (6,7); the switch edges
    carry almost all of each case block's frequency. best has flat ties: 113/116/119/122 (4,6),
    134 (4,5), 115/129 (4,4), 131 (3,8), 126 (3,5), 147 (2,4), 49 has no priority (-7). So best's round 4
    is mostly tie-breaking (fib-heap shape); prof's is mostly keys.
  * Prof's 141 (BinPatch, f10) goes to round 4 because of count_th (profile counts), not freq.
  * Prof's round-3 events differ too (121/125 are inserted in round 3, 108 is a push, 96 is in round 4,
    105's twin is built in round 2). Putting prof's keys onto best's event stream (wp.py) gives dist 13:
    the keys alone are not enough without prof's insertion structure.
- New lever: the round-3 threshold is exec_th = floor(entry_freq * 50/1000). best's entry is 219 -> th 10,
  so 141 (f10) is built in round 3. With entry >= 220 (th 11) 141 is pushed to round 4 with key (3,10).
  Clean realization v/h2.c: label h0 on the help client_usage(0, NULL) plus a 2-conjunct dead-cp goto h0
  at the loop head. Entry goes to 221 and the only other change is block 5's freq (12->15). But (3,10) pops
  before 131 (3,8) and the extra round-4 node reshuffles the tail (dist 9, f2 64). Same with h1 (1 conj).
  wb3 1-conj (a6) raises entry to 223 but also 29's freq (1->5); a6c4 (+ c11 4 conj) gets the front
  exactly right (...129 131 141 126 147 105 49) but the tail is wrong (29 early, 139 before 108; f2 38).
- Loop exits to post-loop labels (lend before the NO_MODE_ARG test, dtg, ndl; 1-14 conj, v/t*,e*,dtg*,ndl*)
  restructure the code after the loop (e.g. netDisconnect freq 34->112): f2 >= 70. Label alone (l0) = 24.
- ~95 real variants (v/*.c; ev.sh prints f2, entry freq, 141's trace/round). r4sim what-ifs: wi.py
  (141 pushed with key K), wr.py (also dropping one round-4 node: dist 2), srch.py on h2: min 3 with 2 edits.
Conclusion: the matching build's round 4 is decided by a ladder of switch-edge priorities that best's
quantised dead-cp feeds don't produce. The entry-threshold lever (h2) moves 141 to round 4 cleanly at
f10, but its key, like the earlier feed levers, comes with the same tail reshuffle. Floor 24 stands.
Semantics: every variant only adds labels and dead __builtin_constant_p gotos (never taken), or changes
their conjunct counts. Equivalent to src/mode_client.c.
