# s37: loop-site asm-goto insertion moves on H5b (plain compile, no profile)

Result: NO MATCH. Best unchanged: s35 H5b.c (st_H5b.json) 5 inv / fncmp 40 / cm (0,8).
~11,800 real compiles (ins77 152, gjA ~1080, gjB 8536, ebpos 2x582). build/v/mc37 deleted.

## 0. Tag race in the parallel tools (affects s2x-s36 tables!)
All ThreadPoolExecutor scripts tagged slots with `i % 4` / `i % 8`. With map() dispatch, job i and
i+4 overlap whenever job i is slow, so two compiles share slot_<tag> / v_<tag>.c: results get
cross-wired (seen here: fake fncmp 0 / cm (0,0) rows with inv 5). s37 copies now use tt.tid()
(one tag per worker thread). Earlier tables (tab_*.jsonl, eb_*.jsonl, ps_B1...) may contain
mislabelled rows; re-measure any row before trusting it.

## 1. JMP from loop sites to post-loop case labels (ins77.py, gj.py, ebpos.py)
- Every loop-site JMP changes round-1 events (new blocks renumber everything); evdiff nev is not
  a usable "intended insertion appeared" test at round 4 without block-id mapping.
- Single JMPs on H5b (19 sites x 19 labels + statement-position scan, 101 positions x 6 targets):
  nothing below 5. `JMP(c9/c11)` from sig/sset/rbs (61's arm) scramble the tail (inv 25+).
- **J1 = H5b + eb site JMP(p1)** (st_J1.json, `{ mode = 10; JMP(p1); }`): 7 inv / fncmp 38 / cm (0,6).
  Tail becomes `103 55 125 126 61 33 29 67 127 117 130 35 42 53 79 77` -- only 125/126 and 79/77
  swapped (55 and 53 fixed) -- but case head 113 drops behind 128 (5 inv). gj.py beam (gs2 cands +
  XT + JMPs, 3 rounds x ~3400) from J1: stuck at 7. fpsa3 on J1: best 1 at L1 36-38 (same gradient
  story as s36).
## Next
- J1's tail is 2 swaps from target; the cost is a case-head tie (113). A lever that restores the
  case-head tie order on J1 (case heads are tied 4/4, fibheap order) is the open direction.
- Re-run tab3/fit on J1 with race-free tags (gs2.build now honours state 'j').
Files: ins77.py, gj.py, ebpos.py, tt.py, st_J1.json, J1.c, i77/ep.jsonl, gjA/gjB.log.
