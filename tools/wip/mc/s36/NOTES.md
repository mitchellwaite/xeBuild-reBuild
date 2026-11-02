# s36: eb-entry boost, f=0 tie structure, event-changing bases (plain compile, no profile)

Result: NO MATCH. Best unchanged: s35 H5b (5 inv / fncmp 40, content-clean). ~1650 real compiles
(tab_B1 1347 + potscan 274). build/v/mc36 deleted. Tools copied from s35 (mc35 -> mc36; gs2/tab3 take
TP=<tag prefix> env so runs don't share slots).

## 1. B1 = H5b + `k49l keys pp` (49+1, 55+1, event-neutral)
55 now pops before 126/125 (front part right) but the f=0 tail reshuffles:
`... 103 55 126 125 61 33 67 29 53 117 77 127 79 35 42 130` (16 / 108). tab_B1.jsonl (1347 XT=1
candidates, 666 neutral) + fit.py (4 seeds x 30000): floor 5 again (most good entries just revert 55).

## 2. eb entry (idea 1)
`c10` arm gotos raise 121 (case-10 head = eb entry) 4->5/6 but are never neutral (nev 2) and 121 is
one of the tied -1000404 case heads: 121+1 jumps it ahead of 107 in the case order. Raising the eb
entry alone can't work; all eleven tied case heads would have to rise together.

## 3. f=0 tie structure (idea 2) -- insmv.py
Round-4 heap: 35/42/53 are deg-0 roots of the round start heap; 77,79 are inserted during 55's pop,
127 at 121, 117 at 116, 130 at 129. Equal keys resolve by fibheap consolidate (later root becomes
parent on ties; min = lowest-degree slot) -- fibsim replays it exactly. insmv.py relocates one/two
insertion events: best is 77+79 inserted at 61's pop instead of 55's -> 2 (only 126 125 55 left);
with 55+1, 67's insertion moved to 112's pop -> 2. Neither is reachable: bcp dead edges are gone
before bbro (f only), so insertion points are fixed by the real CFG (content).

## 4. How far is 0 in f-space (fpsa3.py, all 35 blocks, f up to 20, P fixed, H5b history)
0 exists, but only with L1 131..181: a strict gradient 49>115>112>103>55=126=125=61>33>29>67>127>
117>130>35=42>=53>77=79 with steps of 1-3, i.e. post-loop freqs x2..3. s16 bounds the loop-exit
scale at <=1.7x, so the plain-compile route through this event history is closed.

## 5. Event-changing bases (potscan.py)
Each nev>0 tab_B1 entry (274, score<=40) realized + hsim f-SA on its own history: best potential
1 at L1 31 (`!rok:pp i0`), 2 at L1 14 (`c7t< p0`), everything else needs L1 >= 27. No base has a
small-L1 zero. ps_B1.jsonl has all.

## Next (if anyone continues)
- The order needs ~2-3x more frequency resolution after the loop than any found source shape gives.
  Remaining untested directions: a source shape that changes the round-4 insertion points of 77/79
  (put them in 61's trace, insmv 77/79@61 -> 2) with identical code; or accept the profiled splice.
Files: st_B1.json, tab_B1.jsonl, ps_B1.jsonl, insmv.py, fpsa3.py, potscan.py.
