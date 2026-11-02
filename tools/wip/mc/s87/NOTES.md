# s87 (attempt 68): NO MATCH. New lever: order of the dead `__builtin_constant_p` goto ifs on the `fail:` line

~530 compiled variants: 35 hand variants (rv.sh/rp.sh, log.txt) + 4 hill-climbs (hc.py, ~490 compiles, hc2-5.log; hc1 output lost).

Tools
- gen.py/rv.sh: replace nth occurrence (texts repeat). pf.py/rp.sh: permute the `if (...) goto X;` statements on one
  line (by prefix; perm list / rev / rot:k / sw:a-b). hc.py BASE PREFIX N SEED [start] [inv]: random swap/move climb,
  key fncmp (or inv first).

Results (fncmp/sig2/inv)
| var | base | change | result |
|---|---|---|---|
| a0x..a6y (14) | z3 | swap operand order of the 7 `!argv[i+1] \|\| i+1==argc \|\| *argv[i+1]=='-'` tests | 64-125/6/14 (order never moves) |
| b01-b03,b05,b06 | z3 | invert -s / -i / -p if-else arms, `1==reboot`, `check && mode` | 64/6/14 (no change) |
| b07-b15 | z3 | move case 6 / 2 / 10 / 11 bodies within the switch text | 64/6/14 (no change) |
| b04 (and first b07/b08/b10, wrong switch) | z3 | edits hitting client_usage's switch: invalid | - |
| c01-c112 | z3 | fail-line rev / rot:k / swap | rot2-8: 78/10/7, rot9: 80/10/6, rev 90/15 |
| hc1/hc2 | z3 | climb fail line (fncmp / inv key) | plateaus 64/6/14 and 68/8/6 |
| e01 | z3 | fail perm 0,9,5,3,7,2,1,6,11,10,12,4,8 | 68/8/6: hdd5/hdd4 front diff GONE; left = -ip regalloc (24 lines, same as z3) + back usage(3)/(5) order |
| f*/g10/g11 | e01/z3 | permute ndl (720) line / dsp (910) line | 68/8/6-7, 64/6/14 |
| hc3, h01/h02 | h1 | climb / e01 perm / rot6 | best 64/8/7 (unchanged); e01 perm 96 |
| hc4/hc5, d01-d03 | d2 | climb (inv key, then fncmp from 62) | **62/10/18** (e02.c, perm 0,5,8,10,12,7,1,6,11,3,2,4,9) = lowest fncmp so far, plateau |

Findings
- `||`-operand order, if/else arm inversion and case-body text order do not change bbro order at all.
- The order of the dead constant_p gotos on `fail:` does (they create early CFG edges/bb indices that die before bbro).
  Outcomes are a few discrete classes per base (z3: inv 14/7/6; d2: 9/18). e01 shows the hdd4/hdd5 front can be
  fixed this way; e02 lowers fncmp to 62 but back order gets worse.
- Next: combine — climb other dead-goto lines (rok/dsp/fkbo-front chains, loop-top lines) on e01 with inv key;
  try fail-line perms that also add/remove one dead statement (a goto target change, e.g. ndl<->dtg) to reach new classes.
