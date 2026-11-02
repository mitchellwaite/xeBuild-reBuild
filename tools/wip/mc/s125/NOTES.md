# s125: composing GIMPLE predictors for 44/48 (NO MATCH, best still s117/best.c f2 18)

Base b18.c (= s117/best.c). gen.py NAME EDITS builds v/NAME.c; run.sh adds f2 + profile_estimate freqs
(pf.py: -s/-keys/-ip block freq + succ probs, msg/shutdown freqs); tr.sh = round-3/4 traces (dd/NAME),
kk.sh = bbro keys. res.txt has all ~85 results. Every edit is a label, a never-taken dead
`__builtin_constant_p(i+N)` goto chain, or a hot label: equivalent to src/mode_client.c.

GIMPLE numbering: RTL 44 = gimple 49 (-s test), RTL 48 = gimple 57 (-keys), 46 = "already set" msg.
predict.def (6.2.0): call 71, hot label 85 (DS, not first-match), opcode nonequal (trees) 72,
pointer 85, early return 61, const return 67, goto 70, cold label / expect / noreturn = first match.

## New lever: break the call heuristic via dominance
PRED_CALL needs e->dest dominated by e->src. A label on the -keys test (`} else { kky: if (...-keys...)`)
fed by a dead cp goto from outside the -s arm (E: in the -eb arm, conj chain 2-5) makes 49 not dominate
57, so the -s branch loses its 71% call prediction: -s alone = 50/50, + hot label on the -s arm = 85/15
(DS of hot alone). Feed size is set by conj count (E n=2: 48 f17, n=3 f14, n=4 f13; T/loop-top feeds
are much bigger). Same trick on "setting shutdown" (label ks2 + feed) leaves only the msg arm's call:
reboot==2 prob 72&71 -> 13.7%; a feed into a label on `if (reboot == 2)` (krb) tunes msg freq.

## Results
- r_2_1 (Lk Ls2 krb E=kky,2 E=ks2,3,30 E=krb,1,60 Hs): 48 f15, msg 14: front issue fixed, f2 48.
- kf_7 / z_1..3 (E=kky,4, krb+ks2 feeds): round 3 == profile exactly (48 [13] alone, 46 [12], 5 [12];
  arm 96 [9] goes to round 4 second, as prof's 94) but f2 144: 48 ending its trace gives 49 (-ip) a
  priority key (-1000404, prio 4) that ties/beats 133/134 (prio 4) and 136/148/130 (prio 3), so 49's trace
  is laid out ~8 traces early. Prof has the same priority on 49 (prio 6) but all those blocks carry
  higher priority there (the r4 ladder s112/s113 showed cannot be built). Lowering 49's prio needs
  48->49 <3.5 (p(-ip) <27% at 48=13, or 48<=12), which conflicts with 46 needing 12..13 and arm <=9.
- Keeping 48+96 in one r3 trace (old equilibrium) with the new freqs: 48-84 (w_2 50, z_6 48); conj-1 kky
  feeds (48 f27) reproduce b18 exactly (18).
Conclusion: composing predictors CAN realise prof's round 3 exactly, but that exposes the round-4
priority ladder; no variant beat 18.
