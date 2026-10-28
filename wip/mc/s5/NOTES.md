# mode_client, 5th session (2026-10-28): small structural probes, all negative

Harness: `python wip/mc/s5/var.py NAME[+NAME...]` writes `wip/mc/s5/v_NAME.c` from the
draft and prints fncmp's +/- line count; `sh wip/mc/s5/score.sh NAME...` also runs
`wip/mc/mcvar.py` (inv / matching prefix vs WANT).  Draft: inv=23 pre=1 fncmp=56.

Draft frequencies (bbro dump, -O3 param 50): entry 214, switch dispatch 56 with 13
edges (12 x 8% + default 4%), each case 4, the hwFlags test 50/50 -> HDD errors 2,
usage(2) = 4 (2% entry edge + the 13->15 path).

| variant | what | result |
|---|---|---|
| gotoerr | HDD errors reached by goto (2nd label) | identical code (inv 23, 56) |
| u2goto / u2ret | usage(2) via goto / followed by return | identical code |
| shared | case 4/5 share one hwFlags test | inv 15 but xbox block changes, fncmp 98 |
| inv | `!(hw & 0x20)` first | contents change (72) |
| pre | HDD test before the switch | 117 |
| nohdd6 | drop `case 6` (12 edges) | 136, semantic change |
| while / argfirst | while loop / `arg && mode` | same cold order, 65 / 60 |
| dowhile, dw:*, dwe:* | `if (guard) do ... while` | HDD errors land right after -ip (pre=3) but only because usage(2) goes hot (the guard edge is 27%, not the 2% loop floor); hot part breaks (134-300) |

Takeaway: the do-while forms prove usage(2)'s position is driven entirely by the entry
loop-exit edge; any shape that removes the 2% floor makes it hot instead of colder.
Still open: a shape where that edge stays but its 4 units don't reach usage(2)'s block
(angle 1), or HDD cases at >= 8% of a dispatch that stays at 56.
