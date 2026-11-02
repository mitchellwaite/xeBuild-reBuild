# s105 (attempt 86): NO MATCH. Best stays s102/best.c (f2 24); c_w2f3 family floor 34.

base.c = s104/c_w2f3.c (it already has best.c's r3x/fail-chain fix, since it is best.c plus the wb3/wb4 lines).
Tools: gen.py (v_*.c), gen2.py (g/*.c); measured with s104/run.sh (f2 + r4sim pop order).

- v_* (36): the wb4 feed moved off the loop head into other predecessors (after the help usage(0),
  in the -noenter/-reboot/-bp/-rb bodies, after the u2 test), 1-5 conjuncts, plus split feeds
  (a weaker loop-head feed with a second one in -rb). Best is 34 (help_4, noenter_2/3, reboot_2, u2_4).
  Feeds from inside a branch body (bp/rb) give 42: 62 goes ahead of 33, and 79/81 get pulled earlier.
  Split feeds give 50 or 60.
- g/* (120): grid of wb3 conjuncts 1-3 x wb4 conjuncts 2-5 x placement before/after the u2 test
  x an extra k55l (-r) loop-head feed with 0/2-5 conjuncts. Floor is 34 again (10 variants). Every
  k55l feed is worse. Moving 29/33 around (w3f2: 33 early, 29 after 55; w3f3pre: 108 139 29) does
  not lower f2. In all 156, 55 stays after 139/138, which is the same blocker s104 found.
Semantics: only dead __builtin_constant_p gotos to existing labels (wb3/wb4/k55l), as in s104.
Conclusion: the 34 floor holds for any feed placement or weight tried; reaching the target
still needs 139's key >= 55's together with a different heap shape. No realization found.
