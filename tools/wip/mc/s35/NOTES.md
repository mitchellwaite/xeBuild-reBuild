# s35: JMP-free clientEraseBlockI copy + bcp eb levers (plain compile, no profile)

Result: NO MATCH. New best content-clean state: **H5b.c (st_H5b.json): 5 true inversions, fncmp 40,
cm.py (0, 8) = instruction multiset identical (no extra `mov [8+esp],ebx`)**. Same order as s34 S5
(`... 103 126 125 55 61 33 29 67 127 117 130 35 42 79 77 53`), but without any asm-goto JMP in the eb
copy. ~5500 real compiles. build/v/mc35 deleted. Rebuild a state:
`DUP=1 LU=1 python -c "import json,gs2; open('X.c','w').write(gs2.build(json.load(open('st_H5b.json'))))"`
(state = {'v': voc edits, 'a': arm/lu bcp gotos, 'e': eb-copy bcp gotos (ebl.py)}).

## 1. JMP-free base
S5 minus esucc< / eerase< / einv> / elt< = C1 (inv 23, cm (0,10): clean). The !ebtop bcp edits are
inert there (C2 = C1 identical). hsim on C1's history with S5's f (126+1, 125+1, 127-1) reproduces S5's
order exactly: the eb JMPs only changed f of 125 (efail log), 126 (eout log), 127 (einv log).

## 2. New levers (all bcp-only, event-neutral, content-clean)
- ebl.py: bcp gotos inside clientEraseBlockI from sources T (after myatoh32), A (in block!=-1), B (in
  block<n), S (before esucc), F (efail arm), E (eout arm) to forward labels. eb_C2.jsonl (299): T:b eerase =
  125+1/127-1; S:* eout = 126+1(+2 with b)/125-1; B:q eout = 126+1; *:einv = 127+1..+3; T:b esucc = 127-1.
  Not additive within one source (second T goto inert); the three eb logs sum to ~3 (entry 121 = 4):
  can't get 126=125=2,127=0 without raising the eb entry (`!fail:qqq c10`: 121 4->8, not neutral on C2).
- XT arm gotos (gs2.py XT=1) from option-loop arms to post-loop labels: `u2 top pp` = **33-1 alone**;
  `i1|p1 rbt pp` = **103+1** (first raise of 103 ever); `hdd4 s` = 112+1; `hdd5 s|keys` = 115+1;
  `c12 s` = 129+1; `cdef s` = 132+1. Gotos to u2 from ip/r/w arms are inert.
- Loop-exit dead edge (lx.py, `lx:` label after the loop, goto from loop top): scales only the post-loop
  region (ppp/pppp neutral-ish 5/74, pp/qq/b scramble). Root cause of all ties: mode_client's option loop
  runs ~45x estimated (header 9800, entry 216), post-loop blocks end up at freq 0..8.

## 3. Search
- gs2.py greedy (853 candidates/round) from E2 (C2 + T:b eerase): 17 -> 11 -> 9 -> 8 (G8), stuck.
- tab3.py table on G8 (1348 entries, 303 neutral) + fit.py (SA on neutral subsets, hsim-predicted, then
  realize): G8 -> **H5 (5/46) -> H5b (5/40)** (u2-top 33-1 + k61l s ppp + T:b efail ...). Prediction exact.
- On H5: table floor 5 (also NOSLOT stacking); hsim pair/triple delta scans floor 5. fpsa: 0 needs a
  strict gradient (L1 ~50: e.g. 49:8 115:8 112:7 103:7 55:7 126:6 125:6 61:6 33:5 29:5 67:4 127:4 117:3
  130:2 35:2 42:1 53:1). track.py/tl.py (SA to that target, re-table each step): L1 51 -> 16 but inv 28-33,
  fncmp 390; 125/126 stay at 2 (eb entry cap) and 61 overshoots -> abandoned.

## Next
- Eb entry boost first (c10 target from a cold source, neutral on H5), then eb levers to put 126/125 above 55.
- 79 77 53 are freq-0 ties; need a neutral 53+1 with 77/79 also >0, or the tie-break rule.
- Files: H5b.c/st_H5b.json (best), H5.c, gs2.py, tab3.py, fit.py, track.py, tl.py, ebl.py, ebscan.py,
  ebt.py, varscan.py, lx.py, hp.py; tables eb_C2/eb_E2/tab_G8/tab_H5.jsonl.
