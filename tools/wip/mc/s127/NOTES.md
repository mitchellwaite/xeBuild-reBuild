# s127 (attempt 108): NO MATCH. Floor stays f2 18 (s117/best.c). Best in this family: fb5/fb6 f2 90.

Base = s126 j_dsp_c1 (Li+c1, f2 96); edits in base.edits. Tools copied from s126 (gen0.py with R= now
decoding \n/\t, batch.sh, run0.sh, tr.sh). l1..lf.txt are the batches, res.txt has all ~150 results.
map.txt = s123/map.py on base (note: running map.py rewrote untracked s123/map.txt too).
Every edit is a label, hot/cold label, extra asm-goto label (empty template), extra never-taken
`__asm__ goto("" :::: dsp)`, or a dead __builtin_constant_p goto (chain): equivalent to src/mode_client.c.

## Ladder analysis (base dump)
- Prof r4 order in base numbering: 149 96 113 117 120 123 116 133 136 141 148 130 154 49 ...;
  base: 141 49 96 149 113 117 120 123 116 133 148 136 130 154. r4sim: 49 prio <=2 + 141 prio ~3 +
  149 prio 8 reproduces the front; the case keys themselves only need to beat 49.
- Base keys: 141 prio 31 (140 loop exit), 49/96 prio 7 (48 [13] split 50/50), 149 5, cases 3-4.
- Case blocks' trace-end edges come from 112 = the SWITCH block (f44, ends r2 trace; prof 108 f86) and
  104 = reboot-path netGetInfo + rko asm goto (f20, ends r3). Prof cases are (prio 7-9, freq 7-10):
  nearly all freq via the switch edge. Needs 112 ~105 with case freq < th 10 (entry 219).
## Levers measured
- JMP(fail,cX..) from 159 (netReboot, f39): +13/label, cases >= 10 -> built in r3 (f2 104-202).
- Extra labels in fkbo asm goto (replacing fa19/fa20, 30-operand limit): 120-164.
- Loop exits (T=label,n) raise entry (n1 415, n2 248, n3 223) but restructure (154-242);
  noreturn target h0 barely moves entry (noreturn predictor).
- Hot label on netConnect arm / dsp / else-arm: 96-268. Extra dsp asm gotos in cases: neutral 96-142.
- fkbo dead-cp feed conj count 9 -> 5/6: f2 90 (best); 4: 112 f50 but cases cross th.
- Feeds into dsp / a ksw label on the switch (from NO_MODE_ARG arm or before it): 112 rises to
  70 (n2, cases prio 6) / 104-118 (n1, cases prio 8-9!) but case blocks with extra asm-goto inflows
  (148 c11 via JMP(c11)/case 6, 113 c1 via JMP(dsp,c1), 136, 130, 132) pass th 10 first and go to
  round 3, and the feed steals 104's path (f2 146-204).
- Hk / kipt combos with fb: 96 joins 48's r3 trace as before (120-204).
Conclusion: a prio-8 ladder needs the switch edge to carry ~all of each case block's freq at < 10;
base's extra asm-goto edges into case blocks (rko, fkbo, JMP(c11), JMP(dsp,c1)) add 1-6 each, so the
blocks cross the round-3 threshold before reaching prio 8. Removing those edges is what breaks the rest
of the layout in earlier attempts. Ladder not buildable from this base.
