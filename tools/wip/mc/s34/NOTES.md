# s34: hsim-directed realization on the c9>[hdd4,hdd5] (jT) base (plain compile, no profile)

Result: NO MATCH. New best by inversions: **S5.c (st_S5.json): 5 true inversions, fncmp 37**
(g7b stays the best by fncmp: 7 inv / fncmp 27). About 9000 real compiles. build/v/mc34 deleted.
Tools = s32 copies + s28 fany/evedit/injscan/pot (paths -> build/v/mc34). Rebuild any state with
`DUP=1 LU=1 python -c "import json,gs; open('X.c','w').write(gs.build(json.load(open('st_S5.json'))))"`.

S5 order: `49 115 112 103 126 125 55 61 33 29 67 127 117 130 35 42 79 77 53` (want
`49 115 112 103 55 126 125 61 33 29 67 127 117 130 35 42 53 77 79`): 126/125 before 55 (2), 79 77 53 (3).

## 1. jT base (base.py)
g7b + `{ AT(c9) clientWriteBlocks(arg, start); JMP(hdd4,hdd5); }` = voc design jTd.json
(`["c9>",["hdd4","hdd5"]]`, event-identical to jT.json's text): inv 19, fncmp 79 (g7b 7/27). Confirmed.

## 2. hsim on the jT history
- fany (f only, small): floor 6. fpsa.py (SA f+P): floor 1-2, but only with large L1 (33-113).
- pairscan.py (all 1-2 block deltas -2..+3): **f125 +1 and f67 +1 -> 6**; nothing else below 6.
- evedit (single event edits + f): no 0 (best 6, same as f-only).
- Later histories: on S5 the f-only floor is 1 only with a strict gradient over the whole tail
  (fpsa_no103 best 3 = uniform +1 on 55 126 125 61 33 29 67 127 117 130 35 42 53 77; full 1 needs
  103/112/115 +3..4 too). P helps little.

## 3. evdiff g7b vs jT
Event sequences identical modulo block renumbering (one extra unnamed block); only f112 1->4 and
f115 4->5 differ. So jT's tail scramble is pure heap structure from 112's key; there is no g7b "edit"
to port. The g7b-like tail comes back via f125+1/f67+1 (step 2).

## 4. realization loop
- injscan on jT base: `!ebtop:b [efail]` = f125 +1, event-neutral -> real inv 14 (jT125.json).
- f67 (`-e` strnicmp test, end of the -ip/-r/-w/-e halving chain) is now steerable: label `k67l` before
  the -e test (else-if tail wrapped in `else { }`, inert) + bcp goto from an earlier arm
  (k67.py): `-ip` arm `pp` form -> f67 +1 event-neutral -> **real inv 6, fncmp 45** (B6.c).
  Same trick: k55l/k61l/k49l labels before -r/-w/-ip; and `luN:` labels on the option-loop
  `client_usage(k, argv[i])` calls + loop-top bcp gotos raise 33/29/35/42/53/77 by +1..+5, all
  event-neutral (tablu). Plain asm-goto JMPs into usage labels / k67l are not neutral (nev 40-80).
- gs.py greedy (real compiles, candidates = voc injections/RAW + arm bcp gotos): B6 -> `elt<[eerase]`
  inv 5 / 45 -> `k61l ip pq` inv 5 / 37 (= S5), then stuck.
- Effect table on S5 (tab2_S5.jsonl, 787 compiles, 261 neutral with df). hsim prediction of a sum of
  neutral deltas matched the real compile exactly (pick.py: pred 28 / real 28).
  comb.py (all <=3 subsets): floor 5. combsa/tfit (SA subsets, target fitting to the fpsa gradient):
  floor 8 — deltas are quantized: no neutral +1 for 126/125/61/67/127 alone (they come in pairs/
  chains), 103 can only drop (-4), 112 only +4 or more.
- beam.py: 6 plateau states x 787 candidates = 4702 real compiles: best still 5 (587 at 5).

## 5. g7b's extra `mov dword ptr [8+esp],ebx`
Not order-dependent: identical 1-line multiset diff on g7b, jT, jT125, B6, S5 and other layouts.
It is a lost head-merge in the inlined clientEraseBlockI (original stores `block` to [8+esp] once
before `cmp ebx,eax; jae`; ours duplicates it into both successors). Cause = real asm-goto (JMP)
edges in the eb copy: dropping all of `esucc<`, `eerase<`, `einv>` (plus the ebtop bcp edits) makes
the listing content-identical; keeping any one JMP edit brings the mov back (bcp-only `!ebtop:q` is
clean). But the "clean" design (g7b/S5 minus esucc</eerase</einv>) orders badly: inv 26-29.
So a final match must order 126/125/127 without JMPs inside the eb copy.

## Next
- Need neutral single +1 levers for 126/125/61/67/127 and a raise for 103 (usage:2) to realize the
  gradient; or recover 126/125 order with bcp-only eb edits (content-clean).
- Files: S5.c / st_S5.json (best inv), B6.c, gs.py, tab.py, comb.py, combsa.py, tfit.py, pick.py,
  beam.py, k67.py, lscan.py, pairscan.py, triscan.py, fpsa.py; tables tab_S5/tab2_S5/tablu_S5.jsonl.
