# mode_client s25 (profile-free, asm-goto priority lever in the plain compile)

(draft; final state at the end)

Scratch: build/v/mc25 (v_TAG.c + slot_TAG per measurement).  No src/ or build.sh change.

## Key mechanics found (plain compile, gcc 6.2 bb-reorder.c read at releases/gcc-6.2.0)
- bb_to_key priority is cached per block (bbd.priority, computed at first key) and raised only
  when a trace ENDS: for succ edges of trace->last, priority = max(EDGE_FREQUENCY).  Then keys of
  those succs in the heap are recomputed ("Changing key").  Key = -(1e6 + 100P + f) if P else -f.
- An asm goto only confers priority if its block is the LAST block of a trace: its fallthrough must
  go to an already visited (or copyable multi-pred) block.  Case arms / HDD-log arms / p0 etc. end
  in `break` -> the visited join, so `{ stmt; JMP(x); }` there makes x pop right after that arm's
  trace (P = f_arm / (n+1), rounded; f_arm = 2 gives P1).
- Inside the option loop the arm ends fall through to the shared `i++` block, which becomes a
  fresh block (copy shared with -v) once the arm has an asm goto -> the trace continues, no
  priority (e3).  `JMP(cont,...); __builtin_unreachable(); cont:;` ends the trace but RTL then has
  ALL asm-goto edge probabilities 0 ("Invalid sum of outgoing probabilities 0.0%") -> P = 0 (e5/e6).
  In-loop forward jumps between option tests (labels `else lr: if (...)`) wreck contents (fncmp
  160-445).  So loop blocks (55 61 33 29 67 35 42 53 77 79) can't be steered directly.
- An extra pred on one arm of a 2-way test flips gcc's PRED_CALL (71%) toward that arm: the arm
  is then claimed by the test's trace ("missing" in analyze).  Keep both arms symmetric:
  JMP(hdd4, s4) / JMP(hdd5, s5) (s4 = new label before sendAvatarData).
- A JMP placed BEFORE a statement (case head 'cX<') is not a trace end: pure frequency source
  (target += f_src/(n+1)) with no priority (the case head becomes the asm block: analyze calls it
  'x1'; ev.py maps it back).
- `{ hdd4 log; JMP(u2); }` (h4>u2): 103 = usage(2) loses the threaded 2->103 entry edge (f 4 -> 0)
  and gets P1 when 112's trace ends -> prefix 49 115 112 103 55 solved with
  [h4> u2] + [c3< hdd5,s5] (v1.json, fncmp 46 = best content so far at that point).
- Edits inside clientEraseBlock change the standalone clientEraseBlock too (objcmp: 66 lines).
  Fix: voc.dup() keeps the standalone function plain and gives mode_client a `static
  clientEraseBlockI` copy (with the edits) defined right after it; literals are shared, .rdata
  identical, standalone clientEraseBlock identical, mode_client identical to the non-dup variant.
- The tail (after 55) is tie-order luck (f 0/1 everywhere, fibheap ties); it changes
  chaotically with any key/event change (hsim what-ifs on 112/103 scramble it).

## Tools (tools/wip/mc/s25)
- gen.py: plain src with AT labels always on, the old JUMP() sites off, JMP() = active asm goto.
- voc.py: edit vocabulary: sites `X<`/`X>` (before/after statement X, wrapped in braces) for case
  calls c1..c11, h4 h5 s4 s5 p0 p1 i0 i1 cdef rok, and clientEraseBlock statements etop eerase esucc
  efail eout einv; targets = labels not on the path to the site (no cycles); bcp injections
  `!SRC:W` (after/rok/fail/ebtop x b/p/q/pp, s19 style).  make(edits), dup().
- m.py (compile+analyze), ev.py (true WANT: 115 before 112; x1 mapping), tr.py (round-3/4 traces
  with names), cfgp.py, objcmp.py (whole object vs build/obj/mode_client.o, per function).
- ls.py (stochastic local search), samp.py (random sampling), ga.py (GA on real score), ga2.py
  (GA on hsim 'potential': pot.py enumerates/descends f of non-loop tail blocks on the variant's
  real history), tweak.py (all single-site changes), hq.py / tenum*.py / hann2.py (hsim what-ifs),
  etog.py (E() toggles on option tests: -r..-v no effect, hot ones wreck).

## Results -- NO MATCH; best true inversions 7 (s21 best was 19 under the old WANT; plain = 24 true)
All counts here use the TRUE original order (ev.WANT: compat 115 before avatar 112).
- Plain src (JUMP off): inv 24, fncmp 56.
- v1.json `[h4> u2] [c3< hdd5,s5]`: prefix exact through `49 115 112 103 55`, inv 23
  (tail scrambled), fncmp 46.
- **g7b.json** (from ga2 potential search + ga): inv 7, fncmp 27 (best content so far), all
  blocks present.  Order `... 132 49 115 103 126 55 125 61 112 33 29 67 127 117 130 35 42 77 53 79`.
  Remaining errors: 112 after 103/126/55/125/61 (5), 126 before 55 (1), 77 before 53 (1).
  Edits: `c3<[hdd5,s5] esucc<[efail,eout] s5<[s4,c12] !ebtop:q[eerase,einv] c8>[p1,cdef]
  eerase<[esucc,eout] !ebtop:b[eout,esucc] einv>[eerase] s4<[i1]`.  best_g7b_dup.c is the
  DUP=1 source; objcmp: all other functions, .rdata, .rdata$zzz identical (eh_frame differs only
  through mode_client's size).
- Every single-site change around g7b (tweak.py, 1200 + 900 jobs) and GA restarts (ga.py on real
  score) stay at 7: strict local optimum on a neutral plateau.  Moving 112 (hq.py: f112 3..5) or
  adding the 115->112 chain (h5> hdd4) scrambles the tail (inv 14..34).
- ga2 'potential' (hsim f-descent over 112 103 115 126 125 127 117 130 on the real history,
  RX126/RX117 chains): best 2.2 (p34 family: `[c3< hdd5,s5] [h4> u2] [c9< i1,p1] [h5> u2,s4,cdef]
  [eerase< eout,esucc,efail] ...`, needs f112 +1, f103 +1, f127 -2) -- but realizing those f
  deltas with bcp injections (tweak.py over the 16 injection sites, K=2) only reaches 20: the old
  s19-s24 realization problem (injections move several blocks and the history).
- dummy.py: one or two extra heap insert/extract events (zero-flow arm targets) at any trace end
  never change g7b's tail order (ties there are robust to consolidation timing; they follow keys
  and insertion times).  heapdump.py shows why 77 pops before 53: 77/79 are inserted during 55's
  trace and 77's tree ends up parent of 53 (equal keys: the later-processed tree becomes parent).

## Next ideas
1. Closed-loop realizer for the potential designs: per-block f deltas with EVENT-NEUTRAL levers
   only (bcp injections from sources whose continuation loses frequency in blocks that are
   already popped or irrelevant, e.g. inside clientEraseBlockI only), scored by hsim on the
   current history + real compile check; s21 loop.py on top of a ga2 history (p34) instead of inv19.
2. Order of 53/77 and 126/55: target the insertion times (55's trace inserts 77/79; 61's inserts
   67) -- a chain into 55 is impossible (loop), but changing WHEN 55 pops (f126 vs f55 tie) moves
   77/79's insertion; enumerate in hsim with f126 in {1,2} plus chains 126->125.
3. More vocabulary: JMP sites inside clientEraseBlockI after myatoh32 test/blocks, labels on the
   `if (arg == dummy)` tests (c7/c12 arms) for 117/130 levels; targets with 4+ labels to dilute P.
4. Run ga2 (POT2=1) much longer from several seeds (each run converged in ~1 h to pot 2-7;
   worker crashes 0xC0000005 under Python 3.15 -> ga2 now recreates the pool).
5. The DUP trick (static clientEraseBlockI copy) is required whenever eb-internal edits are
   used; .rdata is unaffected because the literals are shared with the standalone function.

## build.sh/src changes a match would need (not done)
src/mode_client.c: JMP/AT active in the plain compile (no BUILD_FDO), the chosen edits, the s4/eout/
einv/esucc/eerase labels, the clientEraseBlockI copy; build.sh mode_client case: drop fprof/
fflags/ffns (plain compile only, same cflags); src/mode_client.prof unused.  Check
`--param align-loop-iterations` (the FDO compile needed 100; plain has no FDO loop weights).
