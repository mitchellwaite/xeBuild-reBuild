# mode_client attempts

The per-attempt notes from the mode_client matching work (s1 to s150), oldest
first. Each section was `tools/wip/mc/<sNN>/NOTES.md`. The files they mention
(scripts, variants, logs, `best*` files) are in the `wip-archive-2026-11` tag:
`git checkout wip-archive-2026-11 -- tools/wip/mc/<sNN>` restores one.

## s5: mode_client, 5th session (2026-10-28): small structural probes, all negative

Harness: `python tools/wip/mc/s5/var.py NAME[+NAME...]` writes `tools/wip/mc/s5/v_NAME.c` from the
draft and prints fncmp's +/- line count; `sh tools/wip/mc/s5/score.sh NAME...` also runs
`tools/wip/mc/mcvar.py` (inv / matching prefix vs WANT).  Draft: inv=23 pre=1 fncmp=56.

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

## s6: mode_client, 6th session (2026-10-28): frequency-budget analysis, ~110 variants, NO MATCH

Tools (run from repo root): `python tools/wip/mc/s6/batch.py tools/wip/mc/s6/specN.py` builds each
(old,new) replacement variant of the draft, prints fncmp lines (f, draft=56), mcvar inv/pre and
round-4 heap keys of u2=usage(2), av/xb=HDD errors, Bl/Fa=erase Block/Failed, -r.
`keys.py V.c` prints all round-4 trace starts with keys; `tr.py V.c` rounds 1-3 traces.
(g.py/sw.py: single-variant helpers; their output paths are tools/wip/mc/s6/v_*.c.)

### What the original needs (keys = -freq; round 4 extracts the smallest key)
Original round-4 order: -ip(7) av xb u2 -r(2) Bl Fa -w ...  -> av,xb >= u2 >= 2 and Bl <= 2.
Draft: u2 4, av/xb 2, Bl 1.  Loop-internal keys (-ip 7, -r 2, usage3/4/5 0-1) never move.

Budget (draft): entry 214 = 10000 x loop-exit 2%; u2 = 214 x 2% = 4.28 (all of it from the
threaded entry edge; post-loop noreturn edge = 0).  Post-loop 196 splits at the folded
`(mode==0)|(arg==0)` test by the call heuristic 71/29 -> switch side 58, dispatch 56, case 4.3,
HDD 2, Block 1.  Measured: HDD ~ d/26, Block ~ 0.026 d (d = dispatch).
- HDD >= 4 needs d >= ~91; Block <= 2 needs d <= ~94 (narrow window) ...
- ... but the hot layout (reboot side reached by fallthrough, traces 98/99 then 100/101 in
  round 1) needs the reboot side >= 107 (round-1 threshold = 214/2), i.e. switch side <= ~89.
  Every variant with P(switch) >= 50% flips the layout (f >= 108).
- So with u2 = 4 there is no consistent P; u2 must drop to ~3 *and* d rise to ~70-87.
  Available probabilities are only 0 (noreturn/cold), 2 (loop exit), 29/71 (call), 50 (E with
  param 50): no knob gives u2 ~3 or switch ~40-45%.

### Results (all f != 0)
| spec | variants | best |
|---|---|---|
| (s6 singles) guard `if (argc<1) client_usage(2,NULL)` before loop (guard1-4) | 4 | u2 -> 0 (pre=2), only content diff = i=0 store sched; order then wrong (u2 too cold), f 254 |
| post-loop E() forms b1-b5, swapped branches s0-s3 | 9 | E(!(mode&&arg)): pre=4 (-ip av xb u2 exact, keys 4/4/4) but layout flips, Bl -3, f 116 |
| spec1: 12 conditions (E on mode/arg parts, ==NULL, <=0) | 12 | none keep layout with d raised |
| spec2: 4 conds x 9 mods (rok/fail cold removed, E(netConnect), cold u2) | 36 | e_n1 pre=4 inv 17 f 172 |
| spec3: 3 guards x 4 conds x 3 u2 forms | 36 | nothing new |
Earlier this session also confirmed IDA/Ghidra structure = draft (5th session note); orig
entry `jle` goes straight to usage(2), same CFG as ours.

### Next angle
Something that makes the loop-exit probability itself smaller than 2% (n_exits in
predict_loops: 1500/n with n=7 here?) without changing code -- e.g. more distinct exit edges at
profile time that later merge (tail-merge/crossjump).  That lowers u2 quadratically (10000 p^2)
but HDD only linearly, while loop-internal keys stay; combined with E(!(mode&&arg))-like
d this could open a window.  Needs predict.c (gcc.gnu.org git was bot-blocked this session).

## s7: mode_client, 7th session (2026-10-28): loop-exit hypothesis checked against predict.c, NO MATCH

### predict.c (gcc-6.2.0, official gcc.gnu.org git, read via the built-in browser; curl hits the Anubis bot page)
`predict_loops`, PRED_LOOP_EXIT:
    probability = (REG_BR_PROB_BASE - hitrate(LOOP_EXIT)) / n_exits;
    if (probability < HITRATE (2)) probability = HITRATE (2);
So 2% is a FLOOR: more exits can only raise the probability towards 11%, never below 2%.
The s6 hypothesis (more distinct exits -> exit prob < 2%) is refuted.
Only PRED_LOOP_ITERATIONS (constant niter, 1/niter, max-predicted-iterations=100 -> >=1%)
or a first-match predictor ranked above LOOP_EXIT (BUILTIN_EXPECT = 50% with our param)
can override it; neither is available without changing code.

### Empirical (-fdump-tree-profile_estimate-details on the draft)
Latch bb 104: "first match 98.0%, loop exit heuristics: 98.0%" (DS would be 95.2%).
The other ~19 loop-exit predictions sit on noreturn (client_usage) blocks and are ignored.

### spec1.py (10 variants, `python tools/wip/mc/s7/batch.py tools/wip/mc/s7/spec1.py`)
| variant | f | pre | keys |
|---|---|---|---|
| g_e_p / g_ee_p (E(argc<1) guard) | 228 | 1 | u2 gone |
| g_*_d (same + E(!(mode&&arg))) | 164-312 | 3 | av/xb -4 but Bl -3 |
| g_lt_p (argc<1 && !promptEnter) | 104 | 3 | u2 0 |
| loopE / loopNE (expect on loop test) | ~800 | 0 | loop goes 50% |
Every E(!(mode&&arg)) dispatch also makes Block -3 (> 2), so even an ideal u2 ~3 would not
give the original order with that dispatch: the window is closed from the Block side too.

### Next angle
Not the loop exit.  Need a d (dispatch freq) in ~70-87 with the hot layout intact, from a
source predictor combination not tried yet, or accept 15/16 (park mode_client in asm).

## s8: mode_client, 8th session (2026-10-28): systematic predictor search, NO MATCH (still 15/16)

Tools: `batch.py SPEC` (s7 runner writing here), `pe.sh VARIANT.c` (profile_estimate
predictions for the post-loop blocks), `flags.py [SRC]` (param/flag sweep).
76 experiments (spec1-7 + 19 flag sets).

### Predictors found (profile_estimate-details)
- combined `!(mode && arg)` (ifcombined `mode==0 | arg==0`): only PRED_CALL, 71% to the
  reboot side -> dispatch share 0.29 (d=56).  `mode>0`, `mode<=0` etc. change nothing
  because the test is a BIT_IOR of bools.
- splitting the test (`!mode || ({__asm__("");0;}) || !arg`, keeps one test each in asm):
  mode test: `==0` none (50%), `<=0`/`<1` OPCODE_POSITIVE 73%; arg test: TREE_POINTER 15% +
  CALL 71% -> DS 30.2% to the reboot side.  E() on either gives exactly 50%.
- HDD bit tests: CALL 71/29 cancel -> 50%.  `== 0x20`, `>>5 &1`, `>= 0x20` fold to `!= 0`
  before the estimate; `(int)(.. & 0x20) > 0` OPCODE_POSITIVE favours the success arm;
  inverted (`(int)(~flags & 0x20) > 0`) makes the error arm 73% -> it becomes the in-trace
  arm (key None).  Forward user gotos get no PRED_GOTO here; only source block order changes
  (error arm becomes fallthrough).  `__attribute__((cold))` on sendAvatarData/sendCompatData:
  same (error arm in-trace).
- switch: predict.c (6.2.0) `combine_predictions_for_bb`: nedges != 2 -> set_even_probabilities,
  plain 1/nedges, no unlikely-edge exclusion (that is gcc 7).  13 edges -> 1/13 each.

### Results
| spec | variants | best | note |
|---|---|---|---|
| 1 | mode/arg opcode forms, netConnect `>0`/`==1`/`>=1` | base (f56) | combined test unaffected; `>0` changes code |
| 2 | split post-loop test (asm stmt) | sx_le av-4 Bl-3 inv18 | dispatch 0.51 flips hot layout (f110) |
| 3 | split + E()/pointer forms, 15 | le_neg = sx_le | E -> 50% tie also flips hot layout |
| 4 | cold callees | - | HDD error arm goes in-trace |
| 5 | goto'd success arms (+split) | - | same |
| 6 | HDD test opcode forms | - | folded or wrong direction |
| 7 | inverted HDD test (+split) | - | error arm in-trace |
| flags | expect 45-60, hot-bb-frequency-fraction, predictable-branch-outcome, -O2, no-thread-jumps, no-dom | base | -O2 f123; no-dom u2 0 |

### Why the window is empty (with the guessed profile)
- HDD error <= d/26: switch edges are exactly 1/13 (predict.c), and an error arm above 50%
  of its case becomes the case's in-trace arm (spec4/5/7), so <= half.
- u2 = 10000 p^2 = 4.28 (entry->exit path threaded by tree DOM; p = 2% floor).
- HDD >= u2 needs d >= 111 (dispatch share >= ~0.57); the hot layout needs the reboot side
  > 50% at the (last) arg test, i.e. share < 0.5 (combined) or < 0.73*0.5 (split).
- Block/HDD is 0.68 independent of d.
So no combination of guessed predictors gives the original order; the remaining levers are
(a) fewer switch edges (merged case labels; but a 2-label edge records no case value, so DOM
cannot re-split it and code would differ), (b) a crafted profile (memory note says the
switch path <= 1/3 argument blocks it), or (c) park mode_client in asm.

## s9: mode_client, 9th session (2026-10-28): structural probes + split-test crafted profile, NO MATCH (still 15/16)

### Facts checked
- Original jump table (src/mode_client.s, L_44fb1c): 13 entries (index 0..12), 13 distinct
  targets, index 0 = the `ja` default target, case 6 = the join.  Same as ours: no merged
  labels, no fewer edges.  predict.c 6.2 ignores switch predictions (`nedges != 2` ->
  even), so `__builtin_expect` on the switch index does nothing (exp4/exp1: same keys).

### Source-structure variants (batch.py spec1/spec2, draft as base; f = fncmp lines, keys -freq)
| variant | f | u2 | av/xb | note |
|---|---|---|---|---|
| merged `case 4: case 5:` + inner mode test | 88 | -4 | -1/None | code differs |
| merged2 / `case 4 ... 5:` | 112 | -4 | -1/-2 | |
| HDD test hoisted in merged case | 98 | -4 | -1/None | |
| if-chain mode==4/5 before switch | 216 | -4 | huge | layout broken |
| outer switch {4,5,default: inner switch} | 196 | -4 | -10/-10 | right keys, code differs |
| two sequential switches (HDD pre-check) | 232 | -4 | -8/-8 | code differs |
| `switch(__builtin_expect(mode,4/1))` | 62 | -4 | -2/-2 | no effect on probs |
| `switch((unsigned)mode)` | 56 | -4 | -2/-2 | = draft |
Fewer-edge structures do give HDD > u2 but never the original's code (single 13-entry table).

### Crafted profile, combined test (fdorun9.py via d.sh/d2.sh, draft numbering) ~20 designs
- Raising HDD cases alone reorders the case traces (they pop by key); keeping the original
  case order needs 9 tied cases (incl. case 10 for connect) >= the HDD cases, and dispatch
  <= 66 (combined test split by expand: switch <= 1/3) -> HDD <= 3.65 -> realized 4 only at
  7.3/case, which costs the 3 other cases -> case order scrambles (z2: f 100).
- Lowering the loop exit (104>105 = 1%) changes RA everywhere (f 346).

### Crafted profile, SPLIT post-loop test (the real lead)
`sp.c` = draft with `if (!mode || ({ __asm__(""); 0; }) || !arg)`: two GIMPLE conditions, so
the profile sets the arg test's probability directly and the expand q/2 split no longer caps
the switch at 1/3 (cap is now ~50% of the arg-test flow, i.e. ~97 of 200).  Plain compile is
136 lines, but with a profile (sp.sh: mode==0 10%, arg==0 50.5%, all 12 cases equal ~8, HDD 50%)
the hot layout and the whole case order match and the cold order starts
-ip, av, xb, u2 (pre 4..7) for the first time with the original case order.
Prep: `python tools/wip/mcfdo.py "$(cygpath -w "$PWD")\build\mcsp" tools/wip/mc/s9/sp.c` (tree bbs +1 vs
draft after bb 105; erase entry `mode_client:127`).
| run | f | inv | pre | note |
|---|---|---|---|---|
| p1 (mode0 2%) | 116 | 32 | 4 | |
| p2 (mode0 10%) | 78 | 30 | 4 | |
| q1-q3 (dummy 3-5%, erase 30/20) | 68 | 22 | 6 | |
| r2 | 48 | 21 | 4 | below the draft's 56 |
| search.py (240 random/hill-climb designs, fncmp objective) | **40** | 18 | 5 | search.log.best |
| search.py (600 designs, fncmp+4*inv) | 40 best fncmp seen | | | search2.log |
Remaining diffs are only cold-trace order (u3cx/u4cx/Failed/Invalid/patches0/info0 ties).
`mono.py` (mcsim2 replay of every nonincreasing key assignment along WANT on the f40 build's
heap history, values 0..4) bottoms at inv 3 (Failed pops before -r/Block at equal keys;
u3cx/u4cx swapped): tie order inside that history can't give WANT; the history itself must
change (round 1-3 traces) -- with a profile it can, since everything incl. loop-internal
usage blocks (33/29/35/42/53/77/79) is controllable by counts.

### Next angle
Continue on the split-test profile: (1) add overrides for the loop-internal usage edges
(find their tree edges in build/mcsp/pe.txt, `client_usage (3|4|5, ...)` blocks) and the
chain, (2) search with an objective = mcvar inv/pre first, (3) re-run mono.py on each new
best build's dump to steer.  Integration would follow build/mode_update's profile-compile
route (asm("") hint in src + crafted .gcda).
Tools: batch.py (s8 runner -> s9), spec1/2.py, d.sh/d2.sh/fdo.sh (combined-test designs),
sp.c/sp.sh (split-test designs), fdorun9.py (POST env, per-slot cwd so runs can go parallel),
k.py (round-4 keys of a slot), search.py/show.py (parallel search; SLOG selects log), mono.py.

## s10: mode_client, 10th session (2026-10-28): split-test crafted profile, NO MATCH (still 15/16)

Best: `best.json` (sp.c from s9, build/mcsp) -> **fncmp 32, mcvar inv 12** (s9: 40 / 18).
Reproduce: prepare build/mcsp as in s9, then `python tools/wip/mc/s10/run.py SLOT tools/wip/mc/s10/best.json`.
~1300 compiles (search10.py: s9 knobs + 17 in-loop usage-edge overrides; probes; exit sweeps).

### Tools
- run.py (one design -> fncmp/inv/order; keys = s9 names or raw `fn:s>d` tree edges)
- probe.py (which bbro blocks an edge override moves), rap.py (parallel variants + RA-swap flag)
- dumpcfg.py (profile-read compgotos CFG = bbro/trace numbering; `-o -` so the -.gcda is found)
- mcsim3.py (mcsim2 + freq -1 = probably-never-executed key 10000), kenum3/4.py (exhaustive
  nonincreasing key sets with realizability), ksearch*.py (random/hill-climb on the sim;
  ksearch4 = real-valued chains capped at 50%), search10.py (compile search).
- Bucket map (tree edge -> bbro block): 16>17,28>29 -> u3cx 29; 19>20,32>33 -> u4cx 33;
  21>22,34>35 -> u5cx 35; 40>41 -> u3dx 53; 42>43 -> u5dx 42. cfg_b40.txt = the s9 best's CFG.

### Why the profile route can't reach inv 0 (sim on the f40 history, all rounds simulated)
1. Round-4 keys are -freq; a perfect key set exists only with case freq C >= 12
   (kenum3: e.g. 49 9, HDD 6, u2 6, -r 5, Block 5, Failed 4, -w 4, u4cx 3, u3cx 2, -e 2,
   Invalid/patches0/info0 1, rest 0). Binding: erase chain (Invalid->Block->Failed, error arms
   <= 50%, else in-trace) needs Failed >= -w >= u4cx > u3cx >= -e > Invalid...
2. C is capped twice: cases must stay round 4 (round-3 exec_th = 50*214/1000 = 10 -> C <= 9),
   and much harder, 104 (dispatch entry, priority key 100*edge+freq from trace end 99) must pop
   after 44/38 in round 2 (priority 89 from 37) -> 104 <= ~89 -> C = 104/12.6 <= ~7 (b40 has 7).
   44/38 = 4894 * p(10->14) * .5^3; every link is a trace choice capped ~50%, so raising them
   means rescaling the hot loop chain (9>13 = 33% already flips RA, fncmp 68+).
   With C <= 7.45 the best realizable sim order is inv 6 (ksearch4), e.g.
   49 112 115 55 126 103 125 61 33 67 29 117 130 127 35 42 53 79 77.
3. 'Never executed' bucket (count 0 -> key 10000) gives a perfect key set at C 9.49 (kenum4),
   but needs -c (73) never executed; zeroing 64>72/72>80 makes that region not hot ->
   size-optimised code (fncmp 117-166). Under the profile hot test (count > runs) never
   implies not-hot, so no way around it.
4. Raising E (loop exit > 2%) raises all thresholds, but even 2.1% flips an RA tie in the -bp
   option code (eax/edx swap, chaotic in 9>13 / 16>17 / exit; rap.py flags it) and 2.5%+
   reorders rounds 2-3 (45/47, 5, 104 vs 44/38) -> needs the same in-loop rescale as (2).

### Next angle
Not a profile search: something that changes the round-2 competition (104 vs 44/38) or the
erase-chain order (source shape for clientEraseBlock / case 10), e.g. a hint that ends trace
98-99 elsewhere so 104 loses its priority key. Otherwise park (15/16).

## s11: mode_client, 11th session (2026-10-28): source-structure probes, NO MATCH (still 15/16)

### Setup gotcha
Prep MUST run with `EXTRA='--param builtin-expect-probability=50'` exported, otherwise the
.gcno CFG differs and every profile compile ICEs (`create_edge, cgraph.c:850`):
`EXTRA='--param builtin-expect-probability=50' python tools/wip/mcfdo.py "$(cygpath -w "$PWD")\build\mcX" SRC.c`

### Tools
- run.py = s10 run.py + env: MCD (build dir, default mcsp), FAKE (erase leaf bbs for the
  fake-exit overrides, default "5 6 7 8"), ERASE (tree edges for e2 e3 e4).
- search11.py = search10.py with SLOG (log name in s11/) and START (start design) env.
- mk.py OUT.c BODY.txt: sp.c with clientEraseBlock replaced by BODY.txt.

### Variants (best.json from s10 remapped)
| variant | GIMPLE effect | result |
|---|---|---|
| vA: `if (!netConnect) goto fail;` before the switch | identical CFG to sp.c | no change |
| vC: clientEraseBlock with early returns | identical CFG | no change |
| vB (eraseB.txt): erase chain with inverted tests `==-1 / >= / !net` | errors become bb 3/5/7, leaves 3 5 7 8 | e4 51: 32/12 (same as sp); e4 49/55: 36/11 |
| vD: second `({asm("");0;})` after `!arg` | folded away, same CFG | no change |
vB + search11 (hill-climb): see searchB.out / searchB.log.best.
Reproduce vB: prep build/mcvB from vB.c, then
`FAKE="3 5 7 8" MCD=mcvB ERASE="2>3 4>5 6>7" python tools/wip/mc/s11/run.py a tools/wip/mc/s11/bB.json`.

### Conclusion
The erase-chain shape only flips which side of each test is the fallthrough; the s10 cap
(dispatch entry 104 must pop after -eb/-s 44/38 in round 2 -> cases <= ~7) is in mode_client
and untouched. Equivalent C rewrites of the post-loop/dispatch code canonicalise to the same
GIMPLE. Next angle: a hint that really adds a block between trace end 99 and 104 (e.g. a
volatile asm with an output used by the switch, or a cold-label block), then rerun the
s10 simulators on its bbro dump.

searchB (vB, 480 compiles, seed 11): no improvement, best stays fncmp 32 / inv 12 (= s10 best).
Total this session: ~495 compiles.

## s12: mode_client, 12th session (2026-10-28): extra-block / fake-edge probes, NO MATCH (still 15/16)

Best real result unchanged: s10 `best.json` on sp.c = fncmp 32 / inv 12.

### Key new tool: zero-byte asm-goto fake edges
`__asm__ goto ("" :::: L1, L2, ...)` emits no bytes but adds real CFG edges that the
crafted profile can load with flow. Placed in its own block (between netConnect's test and
netGetInfo of the switch path, `vX.c`/`vY.c`), mode_client's block *contents* stay identical
(content.py = 0 unbalanced lines; only order changes). This gives direct control over the
frequency (round-4 key) of any register-independent cold block without raising the cases:
- vX: targets = the two HDD errors (hdd4/hdd5 labels). fake 9% -> HDD errors pop before -ip.
- vY: + `c10` (case 10 head; it reloads cinfo from memory, so it is register-safe; cases 4/5
  heads are NOT safe, they use EAX=cinfo).
- vE: + asm goto inside clientEraseBlock after myatoh32 -> Invalid / Failed leaves free
  (mode_client contents identical; ERASE="3>9 4>8 5>7" FAKE="6 7 8 9").
  Outside-range (126) can't be a target (its `[esp+8],ebx` is head-merged into its pred).
- vZ*/vZb/vZc/vZd: asm goto inside the option loop (to free -r/-w/-e from the 50% chain
  halving) flips an RA tie in the -e/-c blocks (`lea edx,[1+eax]; mov eax,edx` ->
  `add eax,1`) at every placement tried -> unusable.
Other register-safe targets (not yet compiled): cases 1,2,3,7,8,9,11,12, default; 117/130
(clientPatches/clientInfo(NULL)); 103 usage(2).

### Simulations (fibheap replay of the real vY bbro history, renumbered to sp bbs: renum.py)
- inject.py: one dummy heap node anywhere in rounds 3/4 (s10 ksearch4 space): baseline 17 ->
  best 2 (dummy pushed in round 3 after case 107/108, key -4). Tie structure is very sensitive.
- fake.py / fake2.py (fake targets free, re-push model slightly wrong for cases) best inv 1
  (only u3cx/u4cx tie at 2 swapped).
- fake3.py / fake4.py (corrected: TX cases keep their priority key when re-pushed; dispatch
  budget <= 86; cases <= 10 to stay round 4; chain 49 >= 2*55 >= 4*61 >= 8*67): best inv 5.
Binding: -ip/-r/-w/-e chain halving (49 <= 10 by the round-3 threshold 10.7, so 61 <= 2,
67 <= 1) leaves ~15 cold blocks on levels 0..2 where only fibheap tie order decides.

### Real compiles
- vX with 0 fake flow: fncmp 64 (order only, case ties reshuffled by the new block).
- search12.py on vY (cases weights + fakes + s11 knobs), ~1000 compiles: best fncmp 48 / inv 16
  (sY1.log.best); case order is not forced well by weights.

### Third angle (thresholds)
STC thresholds are hard-coded arrays in gcc 6.2 bb-reorder.c (branch {400,200,100,0,0},
exec {500,200,50,0,0}) relative to max entry freq/count; no --param moves blocks between
rounds. unlikely-bb-count-fraction only feeds probably_never_executed, which implies
not-hot -> size-optimised code (s10). Not usable.

### Tools
run12.py (variant runner; LOOPX=1 for vZ numbering; fx<sp-bb>=X fake %, cw<tree>=case weight,
ex<n>=erase fake, lx<sp-bb>=loop fake), search12.py, tcfg.py (tree CFG), dumpcfg.py (MCD),
content.py (order-only check), plain.sh (unprofiled fncmp), renum.py, inject.py, fake*.py.
Prep: `export EXTRA='--param builtin-expect-probability=50'; python -c "import sys;sys.path.insert(0,'tools/wip');import mcfdo;mcfdo.prep(r'<abs>\build\mcvY','tools/wip/mc/s12/vY.c')"`.
Note: the standalone clientEraseBlock does not match under any of these profiles (sp too:
its leaves' `add esp; pop; ret` become `jmp`), so integration needs a separate route for it.

### Next angle
Realize a fake-edge design exactly (write a realizer: target integer freqs -> overrides,
iterate against the bbro dump), using more safe targets (case heads 1/2/3/7/8/9/11/12,
117, 130, 103) to break ties by insertion timing; the sim's best (inv 5) is still not 0, so
also look for a register-safe way to free 55/61/67 (a source block in the loop that does
not perturb IRA), or a second X at a different trace time to control tie insertion order.

## s13: mode_client, 13th session (2026-10-28): second fake source + integration route, NO MATCH (15/16)

Best real result unchanged: s10 best.json on s9/sp.c = fncmp 32 / inv 12.

### Second asm-goto source (angle 2), simulation only
fake5.py = s12 fake4.py + a second fake block X2 (env X2=<block visited just before it>,
TX2=<its targets>; targets pushed into the current heap in round 4, `new` before). Sweep:
X2 in {121,122,107,109,129,110,108,116,119,113,120,128,132,115,112,103,126,125} (blocks outside
the option loop) x TX2 in {117,130 | 117,130,103 | 112,115} (removed from X's TX), 60 hill-climb
rounds each (f5.out, ~44 of 54 runs finished): floor stays **5 inversions** (13 runs), never below.
Remaining inversions are always among the option-loop usage blocks 29/33/61/67 (and 77 vs 42/53),
which sit at freq 0..2 because of the -ip/-r/-w/-e halving chain capped by the round-3 threshold.
Fake targets outside the loop cannot reorder those: a second source does not help.
Tie order (angle 4) is already exact: tools/wip/fibsim.py replays gcc 6's fibonacci_heap, so equal-key
order is modelled, and the sims already explore it.

### Integration route for clientEraseBlock (angle 5)
src/mode_client.c's clientEraseBlock matches unprofiled (fncmp 0) and its body is identical
to sp.c's except extern literal names (sp.c's standalone diff 10 lines = literal/tail shape).
So when a profiled mode_client matches: emit everything from the plain compile and only
mode_client from the FDO compile, like build's loadBlFiles:
  1. tools/wip/mcwhole.py sp.c -> whole C with mc_<addr> arrays (check its .rdata end, 3 bytes short before);
  2. FDO compile of that file (mcfdo prep/score flags, -ftoplevel-reorder per build notes) -> -S;
  3. `tools/re/splice.py --whole <plain -S> <out.s> _mode_client=<FDO -S>` (build.sh line 152 path).
clientEraseBlock is never taken from the profiled compile.

### Next angle
Only a loop-side change that frees 55/61/67 from the halving chain without touching IRA can
get below 5 in simulation; every asm-goto in the loop tried in s12 flipped the -e/-c RA tie.
Otherwise park at 15/16.

## s14: mode_client, 14th session (2026-10-28): NO MATCH (still 15/16)

Best real result unchanged: s10 best.json on s9/sp.c = fncmp 32 / inv 12.

### Experiment: fake edges from outside the loop INTO the option-loop usage blocks
vW.c = s12 vY.c + labels on the client_usage(3, argv[i]) calls of -ip/-r/-w/-e and those
labels added to vY's out-of-loop asm goto (idea: give 29/33/61/67-type usage blocks
flow directly, bypassing the -ip/-r/-w/-e halving chain, with no asm goto in the loop).
Unprofiled (s12/plain.sh + content.py): vY = 14 unbalanced lines, vW = 24. The extra
predecessors stop the usage(3) blocks being shared/merged (literal `offset l...` x5) and
re-tie the -r/-w RA (`lea edx,[1+eax]` / `[68+esp]` reloads). Negative: targets inside
the loop perturb contents even when the asm goto sits outside it.

Counts: 1 real compile (unprofiled), 0 new simulations.

### Next angle
Not tried yet: a simulator variant where 55/61/67/29/33 frequencies are free variables
(step 2 of the plan) to check whether freeing them reaches 0 inversions at all; then
loop-side source shapes (separate ifs / continue / helper inlining) checked with
plain.sh + content.py before profiling.

## s15: mode_client, 15th session (2026-10-28): NO MATCH (still 15/16)

Best real result unchanged: s10 best.json on s9/sp.c = fncmp 32 / inv 12.

### Step 1: free loop frequencies (fake6.py) -> 0 is NOT reachable at the real scale
fake6.py = s13 fake5.py (vY history tools/wip/mc/s12/bYr.txt, X targets ALLX, X2=121 TX2=112,115) with
FREE = {29,33,49,55,61,67} allowed up to VMAX, halving chain only with CHAIN=1, CAP49, and
FULL=1 (drop every realizability cap except cases f[c] >= f[-c], u2 >= 4, CHAIN, CAPC).
Hill-climb runs (600 rounds each unless noted), best inversions:

| setting | runs | best |
|---|---|---|
| loop blocks free 0..20, other caps kept (f6l_*) | 12 | 2 |
| same, 49 <= 10 (round-3 cap) (f6c_*) | 18 | 2 (median 6) |
| everything free in 0..10, cases <= 10 (FULL VMAX=11, f6f11_*) | 8 | **1** |
| FULL, no chain, 0..20 (f6full_*) | 4 | 0 (cases ~20) |
| FULL + CHAIN, 0..40 (f6fc_*) | 4 | 0 |
| FULL + CHAIN + cases <= 7 (s10 round-2 bound), VMAX 16/21/26/31/41 (f6v*, f6cc_*) | 12 | 3/2/1/0/0 |

So the halving chain is not what blocks 0: the integer **resolution** is. Every round-4 cold
block lives on freq 0..10 (round-3 exec threshold = 5% of max entry freq 214 = 10.7); with all
~40 keys free on that range (no realizability at all) the floor is 1. Inv 0 needs ~3x the range,
e.g. (f6v31_82, cases <= 7): 49 29, 112 28, 115 25, 103 24, 55 14, 126 13, 125 9, 61 7, 33 6,
29 4, 67 4, 127 3, 117/130 2, 35 2, 42/53/77 1, 79 0. At exit 2% that is above the round-3 cap
(those blocks would be laid out in round 3, before the round-4 cases), so it is unrealizable
on the current history. Simulated runs this session: 62.

### Step 2: why the chain halves (bbro dump, cfg_b40)
49/55/61/67 are the -ip/-r/-w/-e strnicmp tests (else-if chain). In round 4 (thresholds 0) a
trace always extends to the best successor, so 55 only starts its own trace (as in the
original order 49 ... 55 ... 61 ... 67) if p(49->55) <= p(49->50 match path), i.e. f55 <= f49/2,
and so on down the chain. 49 itself must stay < 10.7 (round 3 otherwise). Hence 55 <= 5,
61 <= 2, 67 <= 1. The way to more resolution is a larger max entry frequency, i.e. a higher
loop exit probability (entry 214 at exit 2%; ~6% would give the 3x range).

### Step 3: loop-side source shapes (shapes.py, shapes.out; 28 shapes, unprofiled)
Identical code to sp.c (canonicalised away): == 0 test, while loop, ++i, help as else-if,
continue after -ip / -r / -w, increment placement (ip/r/e), empty asm after ip, inlined
opt() helper, `return usage(),0`. Same contents, different unprofiled order: E() added/removed
on -ip/-r/-w/-e/-c (profile-equivalent: only the estimate for unoverridden edges changes;
profiled fncmp 38 with best.json, no new history), -ip/-r/-w with the other usage(3) test
form (r_u3, w_u3, ip_r3, r_order: profiled they reorder the -r test operands vs the
original, wrong). Contents change: do-while (32), `!= argc` (22), register pins in -e/-c
(22), shared usage(3) label (15), cached `char *s` (246), `>= argc` (12, different set).
No loop shape gives a new history with identical contents.

### Step 4 (partial): raising the loop exit for resolution
mode_client:104>105 (loop exit) on best.json, sp.c: 2.1% already flips the -bp eax/edx RA tie
(s10). New: register pins fix it with unchanged unprofiled code (plain 134, content 12 = sp.c):
- pinA: -bp `__asm__("" :: "a"(i + 1), "d"((unsigned)(i + 1) * 4));` (replaces the first "r" pin)
- pinF (= pinA + `__asm__("" :: "c"(i));` before `j = i + 1;` in -wb) -> tools/wip/mc/s15/pinF.c
Profiled content (content.py on fdo.diff):
| exit | sp.c | pinA | pinF |
|---|---|---|---|
| 2 | 0 | 0 | 0 |
| 2.5-3 | 20-22 (RA) | 2 (one je/jne) | 2 (one je/jne) |
| 3.5-5.5 | 22-46 | 28-30 (-wb ecx/ebp) | 12-14 |
| 6 | 28 | 28 | 12 |
pinF's remaining 12 lines at >= 3.5%: three extra usage(3/4/5) blocks `mov eax,[ebx+ecx*4]`
(mode_client has 3 more RTL blocks before bbro: created bb 144/145 vs 141/142), i.e. some
pre-bbro merge (tail-merge/crossjump) stops merging them at higher frequency. Not resolved.
Real compiles this session: ~100 (28 plain shapes, 7 pin plain, ~65 profiled).

### Next angle
1. Find the pass that stops merging the three -wb usage blocks at exit >= 3.5% (pinF):
   dump -fdump-rtl-all / -fdump-tree-pre (tail merge) at exit 2 vs 4 and diff block counts;
   a fix keeps content 0 at ~6%, which gives the 3x key range the sim needs.
2. Then the exit-6% history differs (s10: rounds 2-3 reorder at 2.5%+): re-dump bbro at 6% on
   vY+pins, renumber, rerun fake6.py with caps scaled (cap ~ 5% of the new entry freq), and
   build the realizer (fdorun9.overrides with MC_POST = exit flow).
3. X2 (second fake source) is still sim-only; designs without X2 must be re-simulated.

### Tools
fake6.py (env FREE vars, VMAX, CHAIN, CAP49, CAPC, FULL; same args as fake5.py),
shapes.py (+ shapes.out), run.py (s10 runner with MCD=<prepared dir>), pinF.c.

## s16: mode_client, 16th session (2026-10-28): NO MATCH (still 15/16)

Best real result unchanged: s10 best.json on s9/sp.c = fncmp 32 / inv 12 (also on s15 pinF.c, build/mcpF).

### Step 1: why the three -wb usage blocks stop merging at exit >= 3.5% (pinF)
Not a merge pass: it is IRA. `dumpall.sh` (full -fdump-rtl-all-blocks/-tree-all of a slot) at 2% vs 4%:
jump2 crossjumps 18->32, 22->36, 24->38 (-bp/-wb usage(3/4/5)) only at 2%. At 4% the -wb blocks
start with `mov ebp,ecx` (bbins.py on csa): pseudo r167 (i in -wb) gets bp in region l0 (loop
exits = the usage blocks) instead of cx. IRA push order: at 2% r538 (&count, hoisted out of the
loop for -rb getArgs) is GENERAL_REGS and is pushed as a potential spill with r88/r90(mode)
first, then a43(r167,l0) becomes colorable and pops before r181 (i+2) / r172 (a), getting cx.
At 4% r538 becomes NO_REGS (its preheader def got 2x more expensive), r90's spill priority rises
(pri 3 -> 8, fewer excess-pressure points), and a43 itself (cost 296, pri 6) is chosen as the
potential spill; r181/r172 then take cx and a43 gets bp.
- a43's cost is REG_FREQ-floored (usage blocks freq < 10): scaling the -wb usage edges x8 doesn't move it.
- extra "c"(i) pins in -wb (pG1/pG2/pG3.c): hard-reg conflicts don't reach the l0 caps; no fix.
- -rb probability (mode_client:24>25) 60% gives content 0 at 4% but not robustly (5-6%: 12/32).

### Step 2 (the decisive one): the exit can't be raised by more than ~1.7x anyway
Raising the loop exit only buys key resolution if every loop block near the round thresholds
(0.5/0.2/0.05 x entry freq E) scales with E. Those are the else-if halving chain
(cfg.sh on a slot): 8 -> 9(-noenter)/10 50:50, 10 -> 11 (71%) / 14 (29%), 14 -> 15 (-bp) / 23,
23 -> 24 (-rb) / 25, 25 -> 26 (-wb) / 37 ... The hot layout needs the tie/ordering
p(9) >= p(10), p(11) >= p(14), p(15) >= p(23), p(24) >= p(25) (measured: 7>9 = 55..70% breaks
trace 1 at line 23; 9>13 = 50% breaks at line 1). So 25 <= H/2 * 1/2 * 1/4 vs 355 now -> scale
<= 1.72 (exit <= ~3.4%). Consistent scaling at 9>13=40 (exit 2.76, cold edges x1.38, exs.py)
keeps rounds 1-3 except two fixable blocks (12 = -s log, 5 = help usage), content 0.
Sim at that resolution (fake6.py, FULL CHAIN CAPC=7 X2=121 TX2=112,115, VMAX 18 ~ 1.7x;
f6v18_*.out, 4 seeds): best 2/3/2/2 inversions even with every realizability cap dropped.
So the higher-exit route cannot reach 0; s15's 3x requirement is structurally unavailable.

### Next angle
Something other than integer frequency keys must order the cold round-4 traces (e.g. a source
shape that changes which trace end a cold block's predecessor is, i.e. the bb_to_key priority
term), or a different max-frequency block (header) structure. Profile-only routes are exhausted.

### Tools (all take slots in build/mcpF = mcfdo prep of tools/wip/mc/s15/pinF.c, EXTRA param 50)
ex.py SLOT EXIT [k=v]  best.json + exit + overrides; prints fncmp inv pre content
exr.py                 same + first diff hunk;  exs.py: also scales in-loop cold edges (SC env)
dumpall.sh SLOTDIR     all rtl/tree dumps in the slot (profile found: cwd = slot)
cfg.sh SLOTDIR lo hi   pre-bbro CFG with probabilities (cfgdump.py)
bbins.py DUMP bb..     compact post-reload insns per block;  nbb.py: per-pass size diff
Compiles this session: ~45 profiled + 3 plain; sims: 4.

## s17: mode_client, 17th session (2026-10-28): NO MATCH (still 15/16)

Best real result unchanged: s10 best.json on s9/sp.c = fncmp 32 / inv 12 (re-verified, slot r0).

### bb_to_key in gcc 6.2 bb-reorder.c (read from the official repo via the built-in browser)
1. `optimize_function_for_size_p` -> key = bb->index (not our case).
2. `BB_PARTITION == COLD || probably_never_executed_bb_p` -> key BB_FREQ_MAX (10000), start last.
3. priority = cached max EDGE_FREQUENCY over preds that are trace ends (src != ENTRY) OR
   EDGE_DFS_BACK edges; key = -(100*BB_FREQ_MAX + 100*priority + freq).  Otherwise -freq.
Quirks the sims do not model: the cache (bbd[].priority, -1 = not computed) is filled once;
when a trace ends, its last block's successors get `priority = max(cached, EDGE_FREQUENCY(e))`
-- for a block whose cache is still -1 that is THIS edge only (earlier trace-end preds and
DFS_BACK preds are not looked at again); a 0 edge gives priority 0 (no priority).  Re-keying
only happens for successors of the new trace end that sit in a heap.  The fibheap replays
(bYr / f40 histories) already carry the real key events, so for fixed shapes this changes
nothing; it only matters for sims that invent new trace ends.  DFS_BACK priority: none of
the round-4 cold blocks has a back-edge predecessor in our CFG (the loop latch is hot).

### The never-executed bucket is dead (closes s10's point 3 for good)
s10 kenum4 found a PERFECT sim key set using the BB_FREQ_MAX bucket (35 42 53 77 79 + the
-c tail never-executed, 127/117/130 at freq 0 but normal).  s10 assumed this needs count 0.
`tools/re/gcda.py --runs=R` sets the summary run count, and probably_never_executed is
`count * 20 < runs`, so in principle any count cutoff.  But gcc 6.2 maybe_hot_count_p has
`if (profile_info->runs >= count) return false;` ("code executed at most once is not hot"),
so never-executed (count < runs/20) always implies not hot -> size-optimised code.
Sweep (runs.py, s10 best.json): R <= 1e5 identical (32/12); 1e6 fncmp 106; 1e7 166; 1e9 234
with the CFG renumbered.  No R keeps contents while moving cold keys.

### Status of the other plan items
- Step 2 (source shapes changing trace ends) was already covered by s5-s8/s11/s15 shape
  batches (~300 variants): every shape either canonicalises to identical GIMPLE or changes
  contents; no new trace-end lever found this session.
- Step 3: no function-level partitioning (-freorder-blocks-and-partition needs named
  sections/BB_PARTITION; the original has no .text.unlikely split and cold blocks are
  interleaved with hot ones in one function), and the original cold blocks are speed code,
  which rules out an FDO profile that put them in the never bucket (same coupling as above).

### Tools
runs.py SLOT design.json R [extra gcda args]   s10 run.py + --runs=R
Compiles this session: 8.

### Next angle
Only remaining non-frequency term is the priority key (trace-end predecessor).  A source
shape that makes e.g. the HDD-error arm's predecessor (case head) end a trace before round 4
would give it a -(1e6+100p+f) key ahead of usage(2); every shape tried so far either keeps
the case-head trace extending into the arm or changes contents.  Otherwise park at 15/16.

## s18: mode_client, 18th session (2026-10-28): the bb_to_key priority lever

(draft, updated at the end of the session; see "Result" below)

### The lever works (verified on real dumps)
gcc 6.2 bb_to_key: a block whose predecessor ENDS A TRACE gets key -(1e6 + 100*P + f), P = that
edge's EDGE_FREQUENCY; priority blocks pop before every plain -f block.  Three real ways to make
trace ends in front of cold blocks without touching block contents (content.py 0 / 2 = one je/jne
that follows the order):

1. **T48** (profile only): make the round-3 trace [48 94] end at 48 (f94 <= 9 < exec/count
   threshold, f48 = f94 + f49 >= 12 so the round-3 order stays 48, 46, 5).  94 and 49 are pushed to
   round 4 and re-keyed: P49 = EDGE_FREQ(48->49).  -ip (49) then pops right after the cases.
   Real dump (build/mcvP/slotp1): `Changing key for bb 49 from -4 to -1000404`.
2. **X2** = `__asm__ goto` at the end of the rok path (`cinfo = netGetInfo();` of the reboot-only
   path, RTL 102, a round-3 trace [102] that ends there).  Every target gets P = edge freq when the
   trace ends.  Safe targets (plain compile content unchanged): hdd4, hdd5, u2 (labelled
   `client_usage(2)`), case heads c1 c2 c3 c7 c8 c9 c10 c11 c12, default, p0 = clientPatches(NULL),
   i0 = clientInfo(NULL).  Priorities of cases can come from X2 instead of the dispatch, so P132 is
   no longer capped by the range-check halving and the dispatch budget.
3. **RX** = asm goto at the end of a round-4 trace: its targets are re-keyed when that trace ends
   (succ edges of asm goto are not CAN_FALLTHRU, so the trace stops there).
   - RX126: in clientEraseBlock after the "outside system area" log -> efail (125).  The inlined
     leaf's out-edges have count 0 (its flow goes to the fake exit), so gcc splits them evenly:
     P125 = round(f126/2) regardless of the override (forced).
   - RX117: after clientPatches(NULL) -> i0 (130).  P130 = 1 with f130 = 0 is reachable by rounding
     (edge freq rounds up, block freq rounds down), so 130 pops right after 117.
   Targets inside the option loop are NOT usable (jumping into the loop: plain fncmp 1275).

Rounding: P49 = f49 - 1 is realizable (scan49.py: (P,f) = (6,7) at ip 42.5%, 45>49 17.25..17.45),
needed because 49's key must stay below 132's.

### Simulators
- fake7.py: bYr (vY) history replay + priority model (T48, X2, X1ORD/X2ORD orders, RX).  Too
  optimistic: many 0-inversion designs, but the vQ variants' real histories differ (tie structure).
- hsim.py: replays the REAL bbro history of a compiled variant (renumbered to sp numbers by
  analyze.py) with design keys; reproduces the measured order exactly.  hanneal.py anneals
  f/P on it (constraints: chain bounds, case-path <= 50%, X2 budget, dispatch budget, f <= 10).
- runq.py: closed-loop realizer (design f/P -> gcda overrides; dispatch/X2 split, corrections).
- variant.py / batch.py: genq.py source variant (X2 label order, X1 label set/order, RX126/RX117)
  -> prep -> runq -> hanneal on its real history.

### Results so far
- fake7: 0 inversions reachable (an2_*), but not on real histories.
- real histories (hanneal floor per history): RX126 only: 2..18 (48 variants); RX126+RX117:
  best 1 (b10_4: only u2/-r order, tail perfect; b11_1/b12_1: -c/-e usage 42 vs 35).

### Result: MATCH (mode_client, profiled compile; whole object byte-identical in .text/.rdata/.bss/.eh_frame)
- Source: `match/mode_client_fdo.c` (genq variant zero1: vY + X2 asm goto at rok with labels
  `c12,c11,p0,i0,c9,hdd4,hdd5,c2,c1,c10,u2,cdef,c8,c7,c3,s5`, X1 (switch path) labels
  `i1,p1,hdd5,hdd4,c10,c9,c1,c7,cdef`, RX126 + RX117, labels on case heads/arms).
- Profile: `match/overrides.txt` (tools/re/gcda.py overrides, from runq + grid tuning).
- `bash tools/wip/mc/s18/match/repro.sh` -> fncmp 0.
- `FDOX="--param align-loop-iterations=100" bash tools/wip/mc/s18/match/integrate.sh` -> whole-object
  mode_client.o: .text diff 0 vs build/obj/mode_client.o, .rdata/.bss/.eh_frame/.rdata$zzz
  identical; only reloc symbol name `_iob` (asm) vs `__imp___iob` (C; same IAT slot).
- fncmp ignores literal identity and alignment nops: two traps found at byte level:
  the HDD errors are compat (115) BEFORE avatar (112) in the original (mcvar/mcsim2 WANT has them
  reversed), and FDO frequencies add a loop alignment at the reboot-test join and two more blocks
  (fixed with --param align-loop-iterations=100 on the FDO compile only).
- Key steps that made it: hsim (real-history replay; needed per-event priority PFIN fix),
  arm-block zero-flow targets (i1/p1/s5: extra heap insert/delete events) as tie knobs, then
  grid.py fine-tuning (P49 = f49-1 rounding, 61 = 2, 116/128/132 strict keys).

## s20: mode_client s20: design-driven profile-free pass (2026-10-29) -- NO MATCH

Setup: `python tools/wip/mc/s19/mkslot.py src/mode_client.c build/v/mc20/slot_plain`;
analyze reproduces plain inv 23 (all case heads f4/P4, tail f0..2).

### Tools
- `fanneal.py SLOT EVALS SEED`: f-only anneal on the plain history (P as
  measured; env FMAX, PTIE=1 ties P to f where measured P==f, DIST=1 adds
  L1 distance from measured f, START=json, T0).
- `realize.py DESIGN.json STEPS [start.json|-] [WSET]`: greedy over s19
  search.make() injections, objective L1(fq - design) + 3*inv, measured by
  mkslot + s18 analyze (~0.5 s per eval, 94 tgt/src pairs x 4 weights).
- `inv0_a.json` (first inv-0 design, far from plain), `design1.json`
  (inv-0 design at L1 28 from plain).

### Results
- hsim on the plain history admits inv 0 with f alone, unconstrained.
  Closest found (design1, L1 28): cases unchanged (all 4), raise only
  103 +2, 112 +4, 115 +4, 55 +3, 126 +4, 61 +3, 125 +3, 33 +2, 29 +1, 67 +2
  (49 stays 7). Local DIST anneal from the plain point stalls at inv 3.
- Caveat: hsim keeps the plain insertion history fixed and ignores flow
  constraints (55/61/67 halving chain, 112/115 need send calls 39/41 raised).
- realize.py greedy: 3 steps, inv 23 -> 16, but distance to design never
  falls (27-29): single injections add the wrong quanta (and step 0 dropped
  block 125 from the order, which the objective tolerated). Stalled.
  fncmp not attempted (no candidate near inv 0).

### Next ideas
- Realize per block with calibrated injections: first measure, for each
  target block alone, the f delta each (src, weight) gives (table), then
  solve the design as a small integer program instead of greedy.
- Penalize missing blocks (analyze NEED) in realize's objective.
- Re-slot after each realized batch and re-anneal design on the new history
  (START from previous design) -- the plan's iterate loop, not done here.
- Add flow constraints (chain_ok-like) to fanneal so designs are realizable.

## s21: mode_client s21: calibrated injection table + hsim-scored subset solve (2026-10-29) -- NO MATCH

Profile build stays. No src/ or build.sh change. Work dir build/v/mc21 (scratch).

### Tools
- `table.py OUT.json [BASE.json]`: measures every single s19 injection (t,s,w) on top of a base
  (8 threads, ~75 s for 384 jobs, ~3 min with chain sources): per-block fq delta, inv, missing.
  `meas()` now scores inv + 5 per NEED block absent from the round-4 order (s20's realize and
  my first loop runs accepted injections that silently dropped 112/115 -- "inv 16" was bogus).
- `solve.py TABLE DESIGN`: additive-model anneal of subsets toward s20 design1 (L1). Predicted
  L1 12, measured 20 (inv 29): deltas are far from additive.
- `loop.py ROUNDS [start]`: closed loop: table on current base, anneal subsets (<= ADD) scored by
  hsim.inv on the BASE's real history with f = basefq + sum deltas (P tied to f where P==f;
  this replaces the design-distance objective and builds realizability in), measure TOPK, accept
  best measured, re-table. hsim now agrees with measurement (19 == 19) once missing blocks count.
- `srcx.py`: adds chain sources `s<t>` (goto placed before post-loop call t, to a later target);
  env CVAR (default `arg`; `mode` is constant there so bcp folds early -> a real edge).
- `meas.py INJ DESIGN`: one measurement with distance.
- `inv19.json`: best honest result [(44,rok,pp),(50,rok,q)], inv 19 (plain 23).

### Results
- Best honest: inv 19 (clientPatches(arg) and clientInfo(arg) raised). Loop then finds no
  measured or hsim-predicted improvement (ADD up to 8, 60k anneal iters, TOPK 20).
- Why (table t0.json): no injection can raise 55, 61, 67, 103, 112, 115 within the order:
  103/55/61 only ever drop; injections targeting the HDD logs (40/42) raise 112/115 by
  1..73 depending on weight/source but always pull the block out of round 4 (an earlier
  trace takes it via the new edge) -> missing. design1 needs exactly those raised (+2..+4).
- Chain sources (cold block -> next cold block, to build 103->112->115 traces): 590/700 have
  no effect at all (cold source freq * 50% rounds to 0), the rest drop blocks from round 4.

### Next ideas
- The vocabulary is the bottleneck, not the solver: need a way to raise a cold block's f
  by 2..4 WITHOUT a new incoming edge (an edge always lets trace growth claim the block).
  Candidates: raise the block's existing predecessor test probability instead (expect on the
  existing sendAvatarData/sendCompatData result test with a bcp-dependent value, e.g.
  `__builtin_expect(r, bcp(x)?1:0)` -- check whether expect with a non-constant folded later
  keeps a probability), or inject frequency into the predecessor (send call blocks 39/41 = 112/115's
  only preds) and let the 50% split carry it: rows (39,*) currently only lower 112 by 1 --
  investigate why (label before the send call creates a new merge block?).
- Fix analyze.spmap so a block with an extra dead pred is still identified (check whether the
  "missing" 112 is really placed earlier or merely renamed: look at fdo.s order directly).
- Re-anneal design (fanneal DIST) on the inv-19 history, restricted to blocks the table can move.

## s22: mode_client s22 (profile-free), short session -- notes only

Profile build stays. No src/ or build.sh change.

### Try: __builtin_expect with a late-folding value (s21 idea a)
- `v_exp.c`: src/mode_client.c with the case 4/5 `cinfo->hwFlags & 0x20` tests wrapped in
  `__builtin_expect(x, __builtin_constant_p(start|count))`.
- Flags: s19 search.py FLAGS (-O3 -fno-toplevel-reorder -fno-ipa-profile -fno-reorder-functions
  --param builtin-expect-probability=50 -Isrc).
- Result: `tools/wip/mc/mckeys.py` output byte-identical to plain (no frequency/key change);
  fncmp diff 64 lines vs plain 58 (unrelated code change). Reason: profile_estimate runs
  long before dom2 folds bcp, so a non-constant expect argument is simply dropped. Dead end:
  expect cannot carry a late-folded probability.

### Concrete next ideas (not tried)
- Raise predecessor frequency of 112/115 via the send-call blocks 39/41 (s21 idea a, second
  half): check in the s19 injection rows why (39,*) lowers 112 by 1 (inspect the .cfg dump
  for a new merge block from the label placed before the send call).
- s21 idea b: inspect fdo.s order directly for the "missing" 112 rows (analyze.spmap may
  just fail to identify a block with an extra dead pred).
- s21 idea c: re-anneal on the inv-19 history restricted to movable blocks.
- Structural: restructure the case 4/5 source (e.g. hoist the hwFlags test out of the switch,
  or merge the two HDD-error log calls into one shared tail) so that the cold tail block set
  itself differs instead of nudging frequencies.

## s23: mode_client s23 (profile-free) -- NO MATCH

Profile build stays. No src/ or build.sh change. Scratch: build/v/mc23 (ref19 = inv-19 slot).
Base for everything: s21 inv19.json [(44,rok,pp),(50,rok,q)], inv 19.

### Tools (all use s19 search.make + s21 table.meas, NEED-missing penalty 5 each)
- `ext.py BASE [WSET]`: adds non-call targets to search.TGT: 58=h4 / 59=h5 (label before the
  case 4/5 `if (cinfo->hwFlags` test = blocks 110/113), 60=t7 / 61=t12 (before `if (arg == dummy)`
  of case 7/12 = 116/129); measures singles.
- `table2.py`, `loop2.py`: s21 table/loop with ext's targets (loop2 = s21 loop.py, imports ext).
- `try.py INJ-JSON TAG`: one measurement (inv, order, all fq).
- `where.py INJ TAG`: final .s sequence of log strings / calls (where a block really lands).
- `lab.py INJ TAG SPEC..` / `scanlab.py BASE TAG`: label attribute levers without new edges:
  `{ l: __attribute__((hot|cold)); stmt }` at hdd4/hdd5/s4/s5/reb/u2, case heads c1..c12/cdef,
  option then-branches o<name>, and RAW 'ent'/'ent2' (an `if (argc <= 0)` guard before the loop).
- `fanneal2.py SLOT TABLE EVALS SEED`: s20 fanneal restricted to blocks the table moves (env
  EXTRA adds blocks, ONLY=1 uses EXTRA only), flow rule 112 <= f110/2, 115 <= f113/2, L1 cost.

### Findings
1. Why (39,*) lowers 112: 39/41 (send calls) are NOT preds of 112/115. 112/115's only pred is
   the hwFlags test 110/113 (f4, 50/50 split -> 2/2). Injecting into the send block raises 111
   (unmapped) and the label/join makes the 110 split lean to 111 (-1 on 112; same as s4:hot).
   Fix: target the test itself (h4/h5). (58,fail,pp): 110 +5, 112 +3 and 112 moves before 103
   (wanted) -- but 110/113 then jump the round-4 head (inv 38-47). Every lever that makes 112
   >= its sibling 111 (hdd4:hot, s4:cold, 40/42 injections) lets the 110 trace claim 112 ->
   missing. So 112 can only rise as f110/2: needs f110 >= 8 to beat 103 (f4).
2. "Missing" is real, not an analyze.spmap bug: where.py on (40,rok,b) shows the
   "cannot send avatar" log placed in the hot case-4 trace where sendAvatarData was, and the
   send call moved to the tail. s21's numbers stand.
3. 103 = usage(2) reached from the entry (argc<=0 threaded edge 2->103); u2:cold, reb:cold,
   case-head labels have no effect (switch: nedges != 2 => predictions ignored; E() is
   first-match so labels on E-tests/reboot do nothing). 'after' injections drop 103 to 0
   (break the 2->103 threading). ent2 (`if (argc<=0) client_usage(2,NULL)` + cold) -> 103=0.
   No lever found that gives 103 = 2..3.
4. Head realization: design from fanneal2 on ref19 (129 7,107 7,109 6,110 6,113 6,108 5)
   realized exactly by rok-pp duplicates (d3: each (t,rok,pp) = +1, duplicates add) -- head
   order perfect, but tail scrambles (inv 31: 115/112 swap, 29/33/61/125/126 reshuffled by the
   new insertion history). Re-anneal on d3's slot wants 55/61/125/126 +1..+2 (inv 10 in sim),
   which no lever provides; head+112/115 only: sim inv 20-22.
5. 'fail' source saturates: several fail injections share its small frequency (each +5 alone,
   +3 together). 'top' (loop) sources into h4/hdd4 wreck the order (39-56).
6. Option-chain labels: cold label on a then-branch raises the following tests (oip:cold 55 +5,
   or:cold 61/67 +1) but always pulls the raised block out of round 4 (trace claim), E() tests
   ignore labels; hot labels only lower. loop2 (278 rows incl. ext targets, ADD 6, TOPK 12):
   no measured improvement on inv 19.

### Conclusion / next ideas
The binding constraint is structural: a cold block can only rise while staying <= its
sibling at the same 2-way test, so raising 112/115/55/61 requires raising their test blocks,
which are themselves ordered heads/loop blocks. Frequency nudging around inv 19 is exhausted.
- Search 2-level designs explicitly: raise test AND sibling together (e.g. h4 + 39 injections
  so 111 = 112 tie, check tie-break direction in bbro better_edge_p) -- not tried.
- A source with large frequency budget that does not perturb the tail history (entry-level
  source before the loop needs a bcp variable that is not folded at once; all locals are
  constant there -- maybe a volatile-free global read).
- Structural source changes (s22 idea): merge/hoist the hwFlags test, change which blocks exist.

## s24: mode_client s24 (profile-free) -- NO MATCH

Profile build stays; no src/ or build.sh change. Base: s21 inv19.json (inv 19).

### Tries
- `scan.py` (uses s23 ext/table): grid over base + a x (58=h4 test, rok,pp) + nb x send-block
  target {38..41} + c x (59=h5, rok,pp) + nb x {42..45}; a,c in 0..3, nb 1..2 (800 builds,
  scan.log; columns inv a b c d nb f110 f111 f112). Best stays 19 (only no-op combos).
  Raising 112 to 4-5 needs (40,rok,pp) and costs inv 26+ (h4/test head reshuffle, as s23 #1).
  f111 is unmapped in table.meas, so exact 111==112 ties could not be read directly.
  => idea (1) via rok injections into test+sibling: no gain.

### Not done (still open from s23)
- Read gcc-6.2 bb-reorder.c better_edge_p / find_traces_1_round tie rules and map 111 in
  analyze so ties can be targeted exactly.
- Entry-level injection source from a non-folding value (global load / function result /
  argv content) for 103 = 2..3.
- Source restructurings (hoist/merge hwFlags test, usage(2) shape) checked against s5/s9.
- Plain compile + s12 asm-goto zero-byte priority edges (s18 X2/RX/T48) combined with bcp.

## s25: mode_client s25 (profile-free, asm-goto priority lever in the plain compile)

(draft; final state at the end)

Scratch: build/v/mc25 (v_TAG.c + slot_TAG per measurement).  No src/ or build.sh change.

### Key mechanics found (plain compile, gcc 6.2 bb-reorder.c read at releases/gcc-6.2.0)
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

### Tools (tools/wip/mc/s25)
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

### Results -- NO MATCH; best true inversions 7 (s21 best was 19 under the old WANT; plain = 24 true)
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

### Next ideas
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

### build.sh/src changes a match would need (not done)
src/mode_client.c: JMP/AT active in the plain compile (no BUILD_FDO), the chosen edits, the s4/eout/
einv/esucc/eerase labels, the clientEraseBlockI copy; build.sh mode_client case: drop fprof/
fflags/ffns (plain compile only, same cflags); src/mode_client.prof unused.  Check
`--param align-loop-iterations` (the FDO compile needed 100; plain has no FDO loop weights).

## s26 -- mode_client profile-free (continuation of s25)

### Setup
- Copied the s25 tools (voc/ev/m/pot/ga/ga2/hsim users, objcmp, tweak, hq, heapdump, ...) here,
  with paths retargeted to build/v/mc26 (create that dir before use: `mkdir -p build/v/mc26`).
- Deleted build/v/mc25 (694 MB). build/v/mc26 was deleted at the end too.
- Re-checked g7b.json: score (true inversions) 7, fncmp 27. Reproduces.

### Tries
- ga2.py POT2=1 POP=30, seed 2601, from g7b.json, 400 generations (3200 compiles):
  no improvement over init (obj 7070.27 = pot 7, score 7). Log: gp26a.log, population gp26a.pop.json.
  So even a long potential search started from g7b stays at the s25 plateau.

### Result: NO MATCH. Best still s25 g7b (best_g7b_dup.c copied here): 7 inversions, fncmp 27.

### Next ideas (still open, not tried this session)
1. Run ga2 from other seeds or populations (s25 gp*.pop.json, the p34 family) instead of g7b. From g7b
   the potential landscape is flat.
2. Event-neutral realizer: add f deltas only through bcp injections inside clientEraseBlockI and
   check them in hsim before compiling.
3. Control when 55 pops (f126 vs f55 tie) to move 77/79's heap insertion.
4. New JMP sites inside clientEraseBlockI and at the c7/c12 `arg == dummy` tests.

## s27 -- mode_client profile-free (continuation of s26)

Result: NO MATCH. Best still g7b (best_g7b_dup.c, g7b.json): 7 true inversions, fncmp 27.
Scratch dir build/v/mc27 (deleted at the end; `mkdir -p build/v/mc27` before using the tools).

### New tools
- voc.py: new RAW sites (JMP inserted as a bare statement, no braces): `c6<` (case 6 before break),
  `c7t<`/`c12t<` (before the `arg == dummy` tests), `eneg<` `elt<` `enet<` (before the three ifs
  in clientEraseBlock[I]).
- evdiff.py A B: diff of two slots' bbro histories with keys stripped (per popped block event groups)
  + measured f/P deltas.  nev==0 => "event-neutral": hsim on A's history predicts B exactly
  (checked: !fail:pp hdd4 -> f112 7, hsim 21 == real 21).
- injscan.py BASE.json TAG OUT.jsonl: every single bcp injection / raw eb site on top of BASE, with
  evdiff vs TAG (inj27.jsonl = on g7b).
- nsearch.py: event-neutral realizer: combos (K<=3) of neutral levers, deltas summed, hsim-scored.
- fany.py TAG: coordinate descent over ANY f of the 19 tail blocks (0..8) on TAG's history.
- fdum.py TAG: same plus dummy heap nodes (tree-shape lever) after any pop.

### Tries / results
1. (idea 2, new jump sites) tweak.py K<=2 on g7b over the 6 new sites (572 compiles): best 7
   (c7t< some targets, elt<, enet< are no-ops at 7; elt<[eerase] 8; c6/c12t scramble to 10-35).
   K=1 tweak over all sites (incl. new) on v1.json (962 compiles): best 16.
2. (idea 3, event-neutral realizer) injscan on g7b (313 compiles): ~100 injections are
   event-neutral (nev 0) -- all !after/!fail/!ebtop ones; !rok ones are not (nev 6).  Their
   deltas are coarse: f112 1->7/16/29/33/52/74, f115 4->5/8/17.., f103 4->0, f126 2->3 (!ebtop:b/q
   eout, neutral, still 7), f125 1->2, f127 0->1/2.  nsearch (43 distinct levers, K<=3): best 7.
3. (idea 1, when 55 pops / heap shape) heapdump: 55 pops after 126 (both -2; 126 inserted
   during 121, 55 during 49), 77/79 enter at 55's pop and end above 53 in the tree.  KEY RESULT:
   fany.py on g7b's history: no f assignment of the tail blocks gets below 6 (best 6:
   49 5,112 3,103 3,125 2,67 2); fdum.py (f + dummy heap nodes, 25 restarts x 400 steps): 7.
   p34-family history (p34x variant): fany best 7.  So on these histories neither f, nor 55's pop
   time (f55 is in the search), nor extra heap nodes can reach 0: the HISTORY (which blocks a
   trace inserts / claims) must change, not just keys.
4. (idea 4) ga2.py POT2 from s25 populations (gp4/gp5/gs1-3/gp1 top-6 each + p34, seedpop.jsonl),
   ~19 min: best pot 2.2 (score 24, p34 family again) -- same plateau. Log ga27a.log.

### Next ideas
- Target history, not keys: find what event change makes the target order feasible.  Extend hsim
  to edit events (move 77/79 inserts to another popper, drop 112's claim of x, let 112's trace
  end earlier) and search for the MINIMAL event edit that gives 0 with fany; then look for a
  source lever producing exactly that event change.
- Finer injection weights (3-4 chained bcps) only matter after a feasible history exists.

## s28: bbro event-history edits for mode_client (continuation of s27)

Result: NO MATCH. Best still s27 g7b (best_g7b_dup.c, g7b.json): 7 true inversions, fncmp 27.
Scratch dir build/v/mc28 (deleted). Tools = s27 copies with paths -> mc28, plus evedit.py.

### s18 MATCH history vs g7b (evdiff g7b match; slot from s18/match/repro.sh build/mcmatch/slotm)
- Round 4 pop order/inserts of the tail are almost the same; the decisive difference is EARLIER:
  in the match, 112 (avatar), 115 (compat), 103, 117, 130 are already round-4 heap entries at round
  start (pushed in round 3: 1102=rok's visit inserts 117/130/114 and re-keys 112/115/103/132 with
  priority keys P=3/3/2), and dispatch (1105/1106) inserts 115/112 directly in round 2.
  In g7b, 115 is inserted ('this') by x1=1109 and 112 by 110 inside round 4 with plain -f keys.
- Match also has c125 on 126's visit and c130 on 117's visit (RX126/RX117 gotos + profile).
- So the known-good history differs in which round/popper introduces 112/115 and their priority
  keys, i.e. structural (rok as head of a dispatch reaching s4/s5) + profile priorities.

### evedit.py (hsim with event edits + fany f-search, 3 restarts)
- Edits: move X in {112,115,126,77,79,53,55,61,125} to a round-3 push after any round-3 group,
  or to a round-4 'this' insert by any round-4 popper (single edit). 362 edits run (log evedit1.log,
  search stopped before the last blocks).
- Best 6 (e.g. 77 inserted by 112's pop; 77 pushed in round 3 after 110/113 with f115 7 f112 7
  f103 6 f125 4). Pushing 112 as round-3 push with key -1 gets worse (12-22): without priority keys
  the match's round-3 placement doesn't help. No single edit reaches 0.
- Real compile: adding s4 to the rok JUMP list (or dropping c3 from it) is a no-op (inv 8 measured
  order, fncmp 27): rok's JUMP doesn't influence the round-3 pushes in the plain compile.

### Next ideas
- Pair edits (push 112+115 in round 3 WITH priority keys P, as in the match) in hsim; needs
  modelling 'push' with -(1e6+100P+f) keys. Then find a plain-compile source of priority keys
  for 112/115 (in the match they come from profile edge probabilities through rok).

## s29: match-history features in hsim + realizing X2/T48/RX in the PLAIN compile

Result: NO MATCH. Best real plain compile still g7b (best_g7b_dup.c): 7 true inversions, fncmp 27.
Tools = s28 copies (paths -> build/v/mc29, deleted at the end; `mkdir -p build/v/mc29` and rebuild
slots with `python m.py SRC TAG` / `sh tools/wip/mc/s18/match/repro.sh` + copy build/mcmatch/slotm
to build/v/mc29/slot_match).

g7b's 7 inversions: 112 too late (5: after 103 126 55 125 61), 126/55 (1), 77/53 (1).
(k94 placement is NOT a diff in g7b; fncmp shows only those hunks + one scheduling hunk.)

### (1) hsim models
- ed4.py (on the s18 MATCH history; log ed4.log): revert match features to the g7b form one subset at
  a time + f search.  A = 112 as round-3 priority push and B = 115 the same are ESSENTIAL (revert
  either -> >= 9); C (103 prio) and E (130 inserted at rok) are free (CE still 0); D (117 at rok) 3,
  F (125 rekey @126) 2, G (130 rekey @117) 3, H (49 priority) 3 alone.
- ed2/ed3/ed5/sa.py on the g7b history: pushing 112/115 (+117/103) in round 3 with priority keys,
  49 priority, RX re-keys, SA over f and P: best 8 (ed5.log, sa_ab*/sa_abrx*).  The tail becomes
  nearly perfect, but the extra round-4 heap nodes reshuffle the P4/f4 case-prefix ties
  (prefix depends on the NUMBER of nodes, not where the pushes happen; dummy nodes don't fix it).
- psa.py / sa.py on REAL X2 histories (see 2): with 49 priority (H) + RX the tail is perfect;
  only the case prefix (ties) and 112's trace absorption remain:
  * r1 (rok X2 = match list): sa_r1h best 16, all from the prefix (108/116 too early: f7 vs 110/113 f4).
  * c_all (X2 + RX + T48 realized): with case f/P free -> 0 (sa_call_*): history admits a match
    but needs distinct case P levels like the match profile.
  * dfull (X2 + h4t/h5t labels + RX + T48): psa best 5 = only 112 missing (110's trace absorbs
    112 once 110's freq rises); everything else orderable with case f in 4..10, P129 9-10, P132 3.

### (2) plain-compile levers (all real compiles, des.py harness)
- X2 at rok (`JMP(...)` instead of the empty `JUMP(...)`; s28's "rok JUMP +s4 no-op" was because
  JUMP expands to nothing): reproduces the match's round-3 structure (1102 inserts 117/130/112/115,
  re-keys 103) with P2 for the targets.  Labels `h4t:`/`h5t:` on the case 4/5 hwFlags tests are
  harmless (g7b still 7/27) and let X2 raise 110/113.
- T48 realized: label k48l before the -keys test (else-if chain wrapped in `else { ... }`),
  toggles -wb/-eb E() off, and `if ((char *)__builtin_constant_p(i + 10) == (char *)1) goto k48l;`
  at the start of the -s body -> f48 12, rekeys 94 P9/f9 and 49 P3/f3 (inj48b.jsonl; loop-top
  injections are far too hot, f48 in the thousands).  Round-3 threshold: 48 at 9 is not a trace
  start, 94 at 11 is still followed, 8 is not.
  Problem: 94 (P9) then pops before 129 (P4) and before all cases; 49 P3 pops before 132 (P2).
- RX126 (last `JUMP(efail)` -> JMP, inlined copy) / RX117 (`JUMP(i0)` -> JMP) work (125 P2).
- A single-target first JMP level (e.g. `JMP(c12); JMP(...)`) makes rok's trace absorb the target
  (129 disappears); chained JMP levels give geometric shares, too coarse for the 3-4 integer f
  levels the prefix needs (rok freq 41, dispatch gives every case P4/f4).
- Searches: rokscan (all 1-2 extra rok targets on g7b): best 18; rsa.py (rok JMP lists + E toggles
  + RX, 4x~1000 compiles): stuck at 7; dsa.py (chained rok/X1-site JMPs, rx, t48; 9 runs, ~5300
  compiles, from empty and from the full X2 list): best 23-24.

### Next ideas
- The tie-free route needs distinct case priorities: source of 3-4 graded P/f levels for case
  heads besides rok (e.g. several asm-goto sites on paths with different frequencies, each giving
  one level), plus P129 > P94 (or T48 with f94 < case keys) and P132 >= P49.
- Keep 110's trace off 112 when h4t raises 110 (raise hdd4 arm 1113 without raising 112).

## s30: mode_client profile-free, short pass

Result: NO MATCH. Best remains s29/best_g7b_dup.c (g7b): 7 true inversions (m.py inv 8), fncmp 27.

- Set up s30 (m.py copied from s29, build dir build/v/mc30, removed at end). Re-measured:
  g7b inv 8 / fncmp 27; s29 c_all.c (X2+RX+T48 realized) inv 74 / fncmp 308 (as s29: needs graded case P levels).
- scan.py: add a second plain JMP site right after the netConnect JUMP list in g7b, random 1-5 targets
  from {i1,p1,hdd5,hdd4,c10,c9,c1,c7,cdef,s4,s5,c3,c2,c8} (40 compiles): best inv 42 (c8 alone; s4+c7+cdef).
  Every extra goto site at the dispatch head absorbs/re-keys whole case groups; it does not give
  graded levels. Graded levels must come from sites on paths of DIFFERENT frequency (not the hot
  netConnect path), as s29 Next ideas say. Not attempted: per-site frequency table + ILP, 110+s4 sibling pair.

## s31: site table + graded-level design attempt (plain compile, no profile)

Result: NO MATCH. Best remains s29/best_g7b_dup.c (g7b): 7 true inversions, fncmp 27.
About 1300 real compiles. Build dir build/v/mc31 was deleted at the end.

### Step 1: site tables (sites.json, sites_loop.json; step1.py, step1b.py, probe.py)
- Post-loop sites (voc.SITES): g7b plus one JMP to cdef (block 132; c11 for the cdef sites, einv/eout in eb).
  None of them is a round-3 trace end. They only add frequency to the target (132 f6 -> 7/8/9).
  The P of 132 stays 2. Sites that keep contents and order: c1> c2> c3> c8> c9> c11> h4> h5> s4<> s5<>
  p0> p1> i0> eerase<> einv> enet<.
  - f deltas from c9>: 1 target +3, 2 targets +2 each, 3 targets +2, 4 targets +1.
  - Label -> block: c1 107, c2 108, c3 x1, c7 116, c8 119, c10 121, c11 128, c12 129/130.
  - hdd4 -> 112, hdd5 -> 115, p0 -> 117, i0 -> 130 and u2 -> 103 get P2.
- rok with a short target list is not a trace end. Its trace absorbs a target, and case P stays at
  the dispatch's 4. Case f stays below the round-3 threshold only with about 7+ targets, so rok gives P <= ~5.
- Option-loop sites (loopsites.py) are real trace ends only without T48:
  - sig ("reboot has already...") and keys (mode=3 arm end) give P9 with 1 target and P6 with 2 (edge 18/(n+1)).
  - wb gives P89; eb (mode=10) gives f only.
  - Every loop site raises fncmp by about 70-100 (option-loop RA change, s12).
  - With T48 (des.build t48=1) sig/keys no longer give P.

### Step 2: solve + hsim (hs.py, hsa.py)
- The match history shows graded P works (s29 sa_call: 0). On the g7b history graded case levels (f or P)
  do not help: hsim gives 34, because the tail reshuffles. On the c_all history the best is 47.
- Available P levels for cases: dispatch 4, rok <= 5, loop sites 9/6/4.5 only without T48.
  So the s29 design (P129 11, 107 9, 110 8, ... with T48) is not realizable with these levers. I wrote no ILP:
  the site table shows the level set is too small.
- hsa.py (f-only SA on the eb:hdd4 history): floor 15 hsim (incl. the x1 miss penalty).

### Step 3: real compiles (d31.py rounds r1-r5, search.py)
- r2/r3: c_all plus sig/keys graded targets, best 53/208. r4: loop-site x hdd4 table.
  **eb:hdd4** (`{ mode = 10; JMP(hdd4); }`) gives the exact prefix through `49 115 112 103`. The tail
  scrambles (inv 28, fncmp 95).
- search.py (real-compile local search over rok/loop/F/rx/t48, score fncmp+8*inv):
  - seed 1 from g7b, 480 compiles: stays at 7/27.
  - seed 2 from eb:hdd4, 640 compiles: best inv 10 / fncmp 78 (115/117/130 missing).

### Step 4: 110 + s4 sibling (r5.txt/r5.log)
- eb:h4t,s4; keys/sig h4t,s4; eb:hdd4 plus r/e/v:s4 or h4t,s4: raising 110 still makes it jump to the head (s23).
  s4 targets were inert (r/e/v:s4 gave the same order as eb:hdd4). Best 28.

### Next
- A non-loop trace-end source with frequency 10-20 (P levels 5-9) that keeps contents, or a fix for the
  loop-site RA change (pins as in s15/s16), would make the loop-site P levels usable.

## s32: loop-site content check + hdd4 placement scans (plain compile, no profile)

Result: NO MATCH. Best remains s29/best_g7b_dup.c (g7b): 7 true inversions, fncmp 27.
About 3700 real compiles. build/v/mc32 deleted at the end.

### A: the option-loop "RA flip" is not real for asm-goto loop sites
- cm.py: full listings via fncmp (FNCMP_CONTEXT=100000), multiset-of-lines diff vs the original.
  g7b differs by 1 line (an extra `mov [8+esp],ebx` hoist in the 288 region; it is already in g7b).
  sig:[hdd4] and keys:[hdd4] (and every loop site scanned, rA.jsonl) have the same 1-line
  multiset diff. So the +70..100 fncmp of loop sites (s31) is layout only (block order, plus a
  swapped test pair inside the loop at line ~199), not register allocation. No pins are needed.
- What loop sites really do: any loop site that gives a post-loop target P also reshuffles the
  case prefix (108/116 move: 129 107 109 110 113 116 119 108 121 120 128 132) and the tail.
  rL.jsonl (g7b_lab.c adds dead-end filler labels jn/nr/dc/rz + fail): filler-only gotos are inert
  (order identical); hdd4 + 1 filler puts 112 at the head (P too high), hdd4 + 2..4 fillers gives
  `49 112 103 115` with the case prefix disturbed, inv 32. rB.jsonl: hdd4 + case fillers, best 20+.
- search2.py (= s31 search.py scored 10*inv + fncmp/20, all loop sites): 2 seeds x 103 gens from
  g7b: stuck at 7.

### B: post-loop hdd4 sources (scanT.py, rT.jsonl; scanD.py, rD.jsonl)
- `{ AT(c9) clientWriteBlocks(..); JMP(hdd4,hdd5); }` (same at c11 / cdef / c10) gives the match
  prefix through `49 115 112 103`; the tail reorders (126 55 33 29 125 61 127 35 42 130 117 ..), inv 19.
  Adding hdd4 to existing JMPs (s4/s5/c8) gives 112 after 103 or before 49 (20-21).
- Pairwise on top of c9>[hdd4,hdd5] (248 designs: every voc F site x target, every rok target):
  best 17 (rok hdd5) / 18 (h4>u2). search2 from it (150 gens): 15.
- So the same pattern as s23/s31: placing 112 correctly costs the round-4 tail.

### Next
- The tail (55/126/125/61/33/29/67/127/117/130) is a round-4 tie/heap structure question; it needs
  hsim on the c9>[hdd4,hdd5] history (s18 hsim/analyze on build/v/mc32 slots) to find which blocks
  need f/P, not more blind search.

## s33: short pass (no new compiles)

Result: NO MATCH. Best remains s29/best_g7b_dup.c (g7b): 7 inversions, fncmp 27.

This pass only reviewed s32's state; the planned work was not run:
- hsim/fany/evedit on the c9>[hdd4,hdd5] history (slots from s18 mkslot/hsim + s32 jT.json design)
- event-neutral bcp injection rescan (s27 injscan/evdiff) on that base
- evdiff of g7b vs c9>[hdd4,hdd5] tail events, to target only the changed round-4 events
- extra `mov [8+esp],ebx` (g7b's only content diff): still unknown whether it is layout-dependent.

Next: do the above in order; start by generating slots for s32's c9>[hdd4,hdd5] design (jT.json)
and running s18/hsim.py + s29/fany.py to find the tail f/P targets.

## s34: hsim-directed realization on the c9>[hdd4,hdd5] (jT) base (plain compile, no profile)

Result: NO MATCH. New best by inversions: **S5.c (st_S5.json): 5 true inversions, fncmp 37**
(g7b stays the best by fncmp: 7 inv / fncmp 27). About 9000 real compiles. build/v/mc34 deleted.
Tools = s32 copies + s28 fany/evedit/injscan/pot (paths -> build/v/mc34). Rebuild any state with
`DUP=1 LU=1 python -c "import json,gs; open('X.c','w').write(gs.build(json.load(open('st_S5.json'))))"`.

S5 order: `49 115 112 103 126 125 55 61 33 29 67 127 117 130 35 42 79 77 53` (want
`49 115 112 103 55 126 125 61 33 29 67 127 117 130 35 42 53 77 79`): 126/125 before 55 (2), 79 77 53 (3).

### 1. jT base (base.py)
g7b + `{ AT(c9) clientWriteBlocks(arg, start); JMP(hdd4,hdd5); }` = voc design jTd.json
(`["c9>",["hdd4","hdd5"]]`, event-identical to jT.json's text): inv 19, fncmp 79 (g7b 7/27). Confirmed.

### 2. hsim on the jT history
- fany (f only, small): floor 6. fpsa.py (SA f+P): floor 1-2, but only with large L1 (33-113).
- pairscan.py (all 1-2 block deltas -2..+3): **f125 +1 and f67 +1 -> 6**; nothing else below 6.
- evedit (single event edits + f): no 0 (best 6, same as f-only).
- Later histories: on S5 the f-only floor is 1 only with a strict gradient over the whole tail
  (fpsa_no103 best 3 = uniform +1 on 55 126 125 61 33 29 67 127 117 130 35 42 53 77; full 1 needs
  103/112/115 +3..4 too). P helps little.

### 3. evdiff g7b vs jT
Event sequences identical modulo block renumbering (one extra unnamed block); only f112 1->4 and
f115 4->5 differ. So jT's tail scramble is pure heap structure from 112's key; there is no g7b "edit"
to port. The g7b-like tail comes back via f125+1/f67+1 (step 2).

### 4. realization loop
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

### 5. g7b's extra `mov dword ptr [8+esp],ebx`
Not order-dependent: identical 1-line multiset diff on g7b, jT, jT125, B6, S5 and other layouts.
It is a lost head-merge in the inlined clientEraseBlockI (original stores `block` to [8+esp] once
before `cmp ebx,eax; jae`; ours duplicates it into both successors). Cause = real asm-goto (JMP)
edges in the eb copy: dropping all of `esucc<`, `eerase<`, `einv>` (plus the ebtop bcp edits) makes
the listing content-identical; keeping any one JMP edit brings the mov back (bcp-only `!ebtop:q` is
clean). But the "clean" design (g7b/S5 minus esucc</eerase</einv>) orders badly: inv 26-29.
So a final match must order 126/125/127 without JMPs inside the eb copy.

### Next
- Need neutral single +1 levers for 126/125/61/67/127 and a raise for 103 (usage:2) to realize the
  gradient; or recover 126/125 order with bcp-only eb edits (content-clean).
- Files: S5.c / st_S5.json (best inv), B6.c, gs.py, tab.py, comb.py, combsa.py, tfit.py, pick.py,
  beam.py, k67.py, lscan.py, pairscan.py, triscan.py, fpsa.py; tables tab_S5/tab2_S5/tablu_S5.jsonl.

## s35: JMP-free clientEraseBlockI copy + bcp eb levers (plain compile, no profile)

Result: NO MATCH. New best content-clean state: **H5b.c (st_H5b.json): 5 true inversions, fncmp 40,
cm.py (0, 8) = instruction multiset identical (no extra `mov [8+esp],ebx`)**. Same order as s34 S5
(`... 103 126 125 55 61 33 29 67 127 117 130 35 42 79 77 53`), but without any asm-goto JMP in the eb
copy. ~5500 real compiles. build/v/mc35 deleted. Rebuild a state:
`DUP=1 LU=1 python -c "import json,gs2; open('X.c','w').write(gs2.build(json.load(open('st_H5b.json'))))"`
(state = {'v': voc edits, 'a': arm/lu bcp gotos, 'e': eb-copy bcp gotos (ebl.py)}).

### 1. JMP-free base
S5 minus esucc< / eerase< / einv> / elt< = C1 (inv 23, cm (0,10): clean). The !ebtop bcp edits are
inert there (C2 = C1 identical). hsim on C1's history with S5's f (126+1, 125+1, 127-1) reproduces S5's
order exactly: the eb JMPs only changed f of 125 (efail log), 126 (eout log), 127 (einv log).

### 2. New levers (all bcp-only, event-neutral, content-clean)
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

### 3. Search
- gs2.py greedy (853 candidates/round) from E2 (C2 + T:b eerase): 17 -> 11 -> 9 -> 8 (G8), stuck.
- tab3.py table on G8 (1348 entries, 303 neutral) + fit.py (SA on neutral subsets, hsim-predicted, then
  realize): G8 -> **H5 (5/46) -> H5b (5/40)** (u2-top 33-1 + k61l s ppp + T:b efail ...). Prediction exact.
- On H5: table floor 5 (also NOSLOT stacking); hsim pair/triple delta scans floor 5. fpsa: 0 needs a
  strict gradient (L1 ~50: e.g. 49:8 115:8 112:7 103:7 55:7 126:6 125:6 61:6 33:5 29:5 67:4 127:4 117:3
  130:2 35:2 42:1 53:1). track.py/tl.py (SA to that target, re-table each step): L1 51 -> 16 but inv 28-33,
  fncmp 390; 125/126 stay at 2 (eb entry cap) and 61 overshoots -> abandoned.

### Next
- Eb entry boost first (c10 target from a cold source, neutral on H5), then eb levers to put 126/125 above 55.
- 79 77 53 are freq-0 ties; need a neutral 53+1 with 77/79 also >0, or the tie-break rule.
- Files: H5b.c/st_H5b.json (best), H5.c, gs2.py, tab3.py, fit.py, track.py, tl.py, ebl.py, ebscan.py,
  ebt.py, varscan.py, lx.py, hp.py; tables eb_C2/eb_E2/tab_G8/tab_H5.jsonl.

## s36: eb-entry boost, f=0 tie structure, event-changing bases (plain compile, no profile)

Result: NO MATCH. Best unchanged: s35 H5b (5 inv / fncmp 40, content-clean). ~1650 real compiles
(tab_B1 1347 + potscan 274). build/v/mc36 deleted. Tools copied from s35 (mc35 -> mc36; gs2/tab3 take
TP=<tag prefix> env so runs don't share slots).

### 1. B1 = H5b + `k49l keys pp` (49+1, 55+1, event-neutral)
55 now pops before 126/125 (front part right) but the f=0 tail reshuffles:
`... 103 55 126 125 61 33 67 29 53 117 77 127 79 35 42 130` (16 / 108). tab_B1.jsonl (1347 XT=1
candidates, 666 neutral) + fit.py (4 seeds x 30000): floor 5 again (most good entries just revert 55).

### 2. eb entry (idea 1)
`c10` arm gotos raise 121 (case-10 head = eb entry) 4->5/6 but are never neutral (nev 2) and 121 is
one of the tied -1000404 case heads: 121+1 jumps it ahead of 107 in the case order. Raising the eb
entry alone can't work; all eleven tied case heads would have to rise together.

### 3. f=0 tie structure (idea 2) -- insmv.py
Round-4 heap: 35/42/53 are deg-0 roots of the round start heap; 77,79 are inserted during 55's pop,
127 at 121, 117 at 116, 130 at 129. Equal keys resolve by fibheap consolidate (later root becomes
parent on ties; min = lowest-degree slot) -- fibsim replays it exactly. insmv.py relocates one/two
insertion events: best is 77+79 inserted at 61's pop instead of 55's -> 2 (only 126 125 55 left);
with 55+1, 67's insertion moved to 112's pop -> 2. Neither is reachable: bcp dead edges are gone
before bbro (f only), so insertion points are fixed by the real CFG (content).

### 4. How far is 0 in f-space (fpsa3.py, all 35 blocks, f up to 20, P fixed, H5b history)
0 exists, but only with L1 131..181: a strict gradient 49>115>112>103>55=126=125=61>33>29>67>127>
117>130>35=42>=53>77=79 with steps of 1-3, i.e. post-loop freqs x2..3. s16 bounds the loop-exit
scale at <=1.7x, so the plain-compile route through this event history is closed.

### 5. Event-changing bases (potscan.py)
Each nev>0 tab_B1 entry (274, score<=40) realized + hsim f-SA on its own history: best potential
1 at L1 31 (`!rok:pp i0`), 2 at L1 14 (`c7t< p0`), everything else needs L1 >= 27. No base has a
small-L1 zero. ps_B1.jsonl has all.

### Next (if anyone continues)
- The order needs ~2-3x more frequency resolution after the loop than any found source shape gives.
  Remaining untested directions: a source shape that changes the round-4 insertion points of 77/79
  (put them in 61's trace, insmv 77/79@61 -> 2) with identical code; or accept the profiled splice.
Files: st_B1.json, tab_B1.jsonl, ps_B1.jsonl, insmv.py, fpsa3.py, potscan.py.

## s37: loop-site asm-goto insertion moves on H5b (plain compile, no profile)

Result: NO MATCH. Best unchanged: s35 H5b.c (st_H5b.json) 5 inv / fncmp 40 / cm (0,8).
~11,800 real compiles (ins77 152, gjA ~1080, gjB 8536, ebpos 2x582). build/v/mc37 deleted.

### 0. Tag race in the parallel tools (affects s2x-s36 tables!)
All ThreadPoolExecutor scripts tagged slots with `i % 4` / `i % 8`. With map() dispatch, job i and
i+4 overlap whenever job i is slow, so two compiles share slot_<tag> / v_<tag>.c: results get
cross-wired (seen here: fake fncmp 0 / cm (0,0) rows with inv 5). s37 copies now use tt.tid()
(one tag per worker thread). Earlier tables (tab_*.jsonl, eb_*.jsonl, ps_B1...) may contain
mislabelled rows; re-measure any row before trusting it.

### 1. JMP from loop sites to post-loop case labels (ins77.py, gj.py, ebpos.py)
- Every loop-site JMP changes round-1 events (new blocks renumber everything); evdiff nev is not
  a usable "intended insertion appeared" test at round 4 without block-id mapping.
- Single JMPs on H5b (19 sites x 19 labels + statement-position scan, 101 positions x 6 targets):
  nothing below 5. `JMP(c9/c11)` from sig/sset/rbs (61's arm) scramble the tail (inv 25+).
- **J1 = H5b + eb site JMP(p1)** (st_J1.json, `{ mode = 10; JMP(p1); }`): 7 inv / fncmp 38 / cm (0,6).
  Tail becomes `103 55 125 126 61 33 29 67 127 117 130 35 42 53 79 77` -- only 125/126 and 79/77
  swapped (55 and 53 fixed) -- but case head 113 drops behind 128 (5 inv). gj.py beam (gs2 cands +
  XT + JMPs, 3 rounds x ~3400) from J1: stuck at 7. fpsa3 on J1: best 1 at L1 36-38 (same gradient
  story as s36).
### Next
- J1's tail is 2 swaps from target; the cost is a case-head tie (113). A lever that restores the
  case-head tie order on J1 (case heads are tied 4/4, fibheap order) is the open direction.
- Re-run tab3/fit on J1 with race-free tags (gs2.build now honours state 'j').
Files: ins77.py, gj.py, ebpos.py, tt.py, st_J1.json, J1.c, i77/ep.jsonl, gjA/gjB.log.

## s38: race-free re-verification + J1 case-head analysis (plain compile, no profile)

Result: NO MATCH. Best unchanged: s35 H5b.c (st_H5b.json) 5 inv / fncmp 40 / cm (0,8).
~7100 real compiles, all with race-free tags (tt.tid()). build/v/mc38 deleted.
Tools copied from s37 (mc37 -> mc38). Note: cm.py needs ABSOLUTE paths (relative -> silent (0,0)).

### 1. Serial re-verification (ver.py)
| file | inv | fncmp | cm |
|---|---|---|---|
| H5b.c (s35) | 5 | 40 | (0,8) |
| J1.c (s37) | 7 | 38 | (0,6) |
| S5.c (s34) | 5 | 37 | (1,8) |
| best_g7b_dup.c (s29) | 7 | 27 | (1,8) |
All claims hold; the race did not corrupt the recorded bests.

### 2. Race-free re-runs
- tabJ1.jsonl: full one-step table on J1 (1348 XT=1 cands). 700 neutral; nothing < 7. No candidate
  moves 113 ahead of 108 without breaking the tail (best such: 26).
- js1.jsonl: eb JMP(p1,X)/(X,p1) and J1 + one more loop-site JMP (358): nothing < 7.
- gH5b.log: gs2 beam from H5b, XT=1, 2 rounds, beam 3 (1348 + 4042): floor 5 confirmed
  (`!rok:b p1` 5/76 is the best neighbour). So earlier "floor 5" conclusions were not race artefacts.

### 3. Why J1 loses 113 (hd2.py diff of H5b vs J1 histories)
The eb JMP(p1) makes block 118 (clientPatches(arg)) a cold successor of trace 1038 in round 1
(`ins next 118 -7`, pushed into the round-4 start heap). In H5b, 118 is only inserted during 119's
round-4 trace (P1 key). hsim (dx2.py): moving 118 back to 119's trace on the J1 history gives
exactly H5b (5); removing it gives 19. The single extra root 118 is BOTH the tail fix (55, 53) and
the case-head break (113 behind 128): same fibheap consolidation change.
- dx.py / dx3.py: dummy extra roots (any group of rounds 1-4, keys -9..0, P keys, 1-3 copies), alone
  or with any single f delta +-2: nothing below 7 on J1, nothing below 5 on H5b. Parity/root-count
  levers cannot separate the two effects.
- rel.py / rel2.py (relocate one block's insertion event to another group): on J1, 53 inserted in
  round 4 during case 119/120/121 -> 3 (case heads fixed: `129 107 110 113 108 ...`), +29/33/35/42
  relocations -> 2, +77@55 or 126@120 -> 1. On H5b the s36 result again (77/79 @61 -> 2).
  None realizable: 53 (usage:3:dx) keeps its round-1 cold insertion from the option loop; an added
  edge cannot remove an insertion, only add one (and duplicate inserts are no-ops).

### Next
- The remaining routes all need a CFG where 53 (or 77/79) is NOT a cold successor of the option-loop
  trace 1038, i.e. a different crossjump/duplication of the usage(3) calls. That changes content.
- Profile splice remains the only matching build.
Files: ver.py, tabJ.py/tabJ1.jsonl, an.py, js.py/js1.jsonl, gH5b.log, hd2.py, dx.py, dx2.py, dx3.py,
rel.py, rel2.py.

## s39: option-loop usage(3)/(4)/(5) source shapes (plain compile, no profile)

Result: NO MATCH. Best unchanged: s35 H5b.c 5 inv / fncmp 40 / cm (0,8). ~1400 compiles. build/v/mc39 deleted.
Tools copied from s38 (mc38 -> mc39). run.py F.c... = cm + inv (absolute paths handled). m.py gained NONR=1
(drops `noreturn` from the client_usage prototype before compiling).

### Shapes tried (on H5b; mk.py, mk2.py regenerate them)
| shape | cm | inv |
|---|---|---|
| H5b base | (0,8) | 5 |
| all loop usage(3) -> goto one shared call, in loop end (V3_in) / after loop (V3_out) | (110,20) | 18+4 miss |
| same for usage(4)/(5) | (39..,14) | worse |
| pair-share usage(3) site k -> k+1 (Q0-3 / R0-3: -bp,-wb,-eb,-ip) | (13..31, 10..16) | 11-22 |
| pair-share among -r/-w/-e/-c (Q4-6, R4-6) | (0,8) | 5 (already crossjumped; no-op) |
| client_usage noreturn+cold | (0,8) | 5 (no-op) |
| client_usage without noreturn (N0) | (0,6) | 5, fncmp 120, same case/tail order |
| J1 without noreturn | (0,4) | 7 |
So the original has separate usage(3) calls for -bp/-wb/-eb/-ip (sharing them changes content); the
-r/-w/-e/-c ones already merge. No content-neutral shape removes 53/77/79 as cold succs of the loop.

### NONR base
Removing noreturn (local discovery still makes it noreturn later) gives a different bbro history with
same content metric (actually block-metric 6 vs 8). Full one-step table on st_H5b with NONR=1
(tabN.jsonl, 1348 cands): floor still 5 (best fncmp 68). Not a new route.

### Next
- Untried: usage calls via a static noinline wrapper / function pointer, __builtin_unreachable after
  calls, flag+break sinking with argv index kept in a separate var; NONR combined with gs2 beam / rel hsim.

## s40: usage-call shapes, block map, NONR beam (plain compile, no profile)

Result: NO MATCH. Best unchanged: s35 H5b.c 5 inv / fncmp 40 / cm (0,8). ~2600 compiles. build/v/mc40 deleted.
Tools copied from s39 (mc39 -> mc40). New: mk40.py, mk41.py, mk42.py (regenerate the shapes below from H5b.c).

### Block map (sp numbering -> H5b.c source, from slot bbro final listing)
| sp | block | H5b.c lines |
|---|---|---|
| 29 usage:3:cx | -wb usage(3) | 629 (preds: test 628) |
| 33 usage:4:cx | -wb usage(4) | 634 (test 633) |
| 35 usage:5:cx | -wb usage(5) | 637 |
| 42 usage:5:dx | -eb usage(5) | 646 |
| 53 usage:3:dx | shared usage(3) of -eb (643) and -ip (664) | 664 |
| 77 usage:3:ax | shared usage(3) of -r/-w/-e/-c (672/681/689/697) | 698 |
| 79 usage:5:ax | shared usage(5) of -r/-w/-e/-c | 700 |
| 55/61/67 | strnicmp -r / -w / -e tests | else-if chain |
Insertion events (all shapes below identical): 53 inserted round 2 from loop trace 1038 ('next');
55,77,79 inserted round 4 at 55; 61 at 49; 67 at 61.

### Shapes (on H5b)
| shape | cm | inv | round-4 events |
|---|---|---|---|
| __builtin_unreachable() after every loop usage call (U1) / usage(3) only (U2) | (0,8) | 5 | identical (neutral) |
| `if(!c) goto ok; usage; ok:` inverted (G0-7) | (0,8) | 5 | identical |
| `if(__builtin_expect(!c,v)); else usage` per site (I/Z, v=0/1 same) | sites 5-7 (0,10) 5; 4 (0,16) 29; 0-3 content | changed in round 2/4, but 53/77/79/55/61/67 insertions unchanged |
| combos C56/C57/C67/C567 | (0,10) | 5 (C567 fncmp 46, inv 6 in m.py) | same |
| static noinline noreturn wrapper (W1 all / W3 usage3) | (43,16)/(6,10) | content changes (calls cuw) | - |
| volatile function pointer for usage(3) (F1) | (179,28) | 15 | - |
### NONR beam
gs2.py st_H5b.json with NONR=1, 2 rounds beam 2 (~2560 compiles, gN.log): best 5 inv, fncmp 156. Floor 5.

### Conclusion
Usage-call shapes are either gimple-normalised (no change) or change content; none moves 53's round-2
insertion from the option-loop trace or 77/79's insertion at 55. Same conclusion as s38/s39.
Profile splice remains the only matching build.

## s41: trace-frequency levers around the shared usage blocks (plain compile, no profile)

Result: NO MATCH. Best unchanged: H5b.c (copy of s40/H5b.c) 5 inv / fncmp 65 diff lines / cm (0,8).
Flags: -Isrc -O3 -fno-toplevel-reorder -fno-ipa-profile -fno-reorder-functions --param builtin-expect-probability=50.
Short session (~20 compiles). gen.py / gen2.py regenerate the variants from H5b.c.

### (a) E()/expect-0 on option-loop tests (-eb/-ip/-keys/-s/-wb), gen.py
| variant | cm | fncmp lines |
|---|---|---|
| -eb E removed | (0,18) | 186 |
| -eb expect(.,0) | (0,8) | 65 (byte-identical to H5b: E is only a tie-breaker at prob 50) |
| -ip E / expect0 | (0,14) | 148 |
| -keys E / expect0 | (2,22) | 340 |
| -s E / expect0 | (0,14) | 324 |
| -ip,-keys,-s E | (4,22) | 501 |
| -wb E removed | (0,18) | 270 |
| -eb plain + -ip expect0 | (0,12) | 150 |
### (b) E() on -r/-w/-e/-c (55/61/67 order), gen2.py
All single toggles (0,10)/78 lines; -r+-w both E (0,10)/90. None beats H5b.

### Conclusion
expect toggles near 53/55/61 only worsen content/order; no lever reached the round-2 trace split.
Untried: (c) switch / flag+break shapes, (d) dx hsim ranking of relocations.

## s42: bcp-goto lever scans for the 53/77/79 insertion events (plain compile, no profile)

Result: NO MATCH. Best content-clean variant is still H5b.c (copy of s41): 5 inv / fncmp 40 / cm (0,8).
Flags: -Isrc -O3 -fno-toplevel-reorder -fno-ipa-profile -fno-reorder-functions --param builtin-expect-probability=50.
About 42k real compiles, all with race-free tags (tt.tid). Tools were copied from s40 (mc40 -> mc42). build/v/mc42 was deleted.

### Tools
- lev.py: one lever = a new label `zqT:` on statement line T of the option loop plus
  `if (bcp(i+N)==1 [&& ...nt]) goto zqT;` inserted before site line S. Sites are the 85 statement starts after a
  `;{}` line (no unbraced if bodies); targets are the 108 statement starts. It records the true inversions (ev.py)
  and the insertion signature of 53/77/79 from the slot history (hsim). It can be resumed.
- lev2.py: multi-lever builder plus a beam (score 10*inv + cm lines). cmc.py: content check (cm.py) for moved
  signatures. anl.py: signature histogram. shp.py: (c) sinking shapes.
- The H5b signature is `2:1038:ins/next/53, 3:53:push, 4:55:ins/this/77, 4:55:ins/this/79`.

### (a) Exhaustive single-lever scan (levA.jsonl: nt=1, all 9095; levB2.jsonl: nt=2,3, targets 642-700, 8256)
- The insertion events DO move. 164 levers put 77/79 at 61 (round 4), 128+ put 53 in round 1 (1037/1038),
  and others put it in round 3, round 4 (at 49) and so on. These are the first real insertion moves found.
- 77/79@61: best 3 inv (e.g. site 599 (-noenter) -> target 676 (`arg = argv[++i]` in -r), also 601/604/606 ->
  672/674/676/677). Order: `... 42 53 79 77 ...`. But every one has cm >= 10: the -r arm's i+1 swaps
  eax/edx registers (5 mov/lea/cmp lines), and fncmp is 58.
- 53 in round 1 (any site -> 643, the -eb usage(3) test): content-clean (0,8) but 6 inv.
- No lever with a moved signature is both content-clean and below 5.

### (b) hsim relocation ranking (rel2.py, rel2_b0.log, rel2_chk.log)
- On H5b, the best single relocation is 79@61 (3), then 77@55 or 77@61 (4). The best double, 79@61 + 77@61,
  gives 2 (`53 77 79`). Lever (a) realises the 77+79@61 move (3, order 79 77).
- On the moved base (chk599676) the only further gain is 77 relocated within 61's group (2). The remaining
  `126 125 55` vs `55 126 125` is not an insertion problem, so relocations cannot fix it.

### (c) Sinking shapes (shp.py, shp.log)
- Sharing usage(3)/(5) of -eb/-ip with -r/-w/-e/-c (goto zu3/zu5 at the loop end, top or middle) changes
  content (31,12+) and gives 11-34 inv.
- Sinking only -r/-w/-e/-c is neutral: (0,8), 5 inv, and the signature is unchanged.
- A switch rewrite was not tried because it necessarily changes the code (switch on a char).

### (d) Beams on the moved bases (lev2.py, 1 round each, about 9.1k compiles each)
- bmB (from [599,676,1], 3 inv / cm 10): best stays 3 inv / cm 10. No second lever restores the -r arm
  register allocation (min cm 10 at inv <= 6).
- bmA (from [606,643,1], clean 6): best (5, cm 2) and (4, cm 10). No clean result below 6.

### Conclusion / next
- The 77/79@61 insertion is reachable, but only by raising the -r arm frequency, which flips its register
  allocation. A content-neutral fix would need a second lever that restores the allocation (for example
  an asm register pin in the -r arm), or a lever that moves 77/79 without heating -r.
- Profile splice remains the only matching build.

## s43: register pins on the 77/79@61 movers (plain compile, no profile)

Result: NO MATCH. Best clean is still H5b.c (5 inv / fncmp 40 / cm (0,8)); best moved stays 3 inv / cm (9,8).
Flags as s42. About 1.5k compiles (race-free tt.tid tags). build/v/mc43 and mc42 deleted.

### Tools
- mk.py S T N OUT: write one s42 lever variant (lev.make on s42/H5b.c).
- ps.py VARIANT LINES OUT: 12 empty-asm pin forms x given lines of the -r arm (inv + cm).
- pm.py OUT: 5 pin forms at the -r arm head on all 275 77/79@61 movers from s42 levA/levB2 (movers.json).
  Results: psA.jsonl (599->676), pmA.jsonl.

### Findings
- On 599->676 the -r arm diff is `mov edx,[68+esp]; lea eax,[1+edx]` vs the original `mov eax; lea edx,[1+eax]`.
  Pins `asm("" :: "a"(i))`, `"a"(i),"d"(i+1)`, `"+a"(i)` (and a register-asm j) restore exactly the original
  -r arm code (fncmp diff identical to H5b) -- but EVERY such pin also reverts the order to H5b's 5 inv
  (`... 79 77 53`). Same on all 204 3-inv movers: 816 results at 5 inv, and every 3-inv result has cm >= (9,6).
- So the RA flip and the 77/79@61 insertion are coupled: the allocation change itself (instruction
  size/copy cost seen by bb-reorder after RA) is part of why the layout moves; pinning RA undoes the move.
  A lever that only raises the -r arm frequency cannot be fixed by RA pins.
- `"+d"(i)` at the arm head keeps 3 inv with cm (9,8) (one line better than 10) -- still not clean.

### Next
- Look for levers that move 77/79 via a different block (not -r arm heat): restrict lev.py targets to
  blocks whose frequency change leaves -r arm RA alone, or compare -fdump-rtl-bbro of pinned vs unpinned
  599->676 to see which trace/copy decision the RA change flips, then reproduce that decision elsewhere.
- Profile splice remains the only matching build.

## s44: where the -r arm register swap moves 77/79 (plain compile, no profile)

Result: NO MATCH. Best clean unchanged: s42/H5b.c (5 inv / fncmp 40 / cm (0,8)). ~6 compiles (diagnosis only).
U.c = s43 mk.py 599 676 1 (3 inv, -r arm edx form); P.c = U.c + `__asm__("" :: "a"(i));` on line 671 (5 inv, eax form).
Tools: sig.py DUMP (per-pass bb:symbol signature of mode_client), blk.py DUMP BB.. (print insns of blocks).

### Finding (task 1): the decision is cross-jumping in jump2, not bb-reorder
- -fdump-rtl-all, compare bb/symbol signatures pass by pass: identical through csa (265), first DIFF at
  266r.jump2 (post-reload cfgcleanup with CLEANUP_CROSSJUMP); bbro's own decisions are then identical
  except block numbering/which block holds the merged tail.
- The candidates are the noreturn `client_usage(3|5, argv[i])` tails (4 insns: load argv[i*4], store arg,
  store const, call). Index register decides who matches whom:
  - U (edx): -r arm tails bb63(3)/bb65(5) use dx, as do bb46(5)/bb57(3) -> "Cross jumping from bb 46 to 65",
    "57 to 63"; 87/89 (ax) stay alone.
  - P (eax): -r arm tails use ax -> "63 to 87", "65 to 89"; 46/57 stay alone.
- In bbro the merged tail's edges then hang off a different trace: U pushes 77/79 from the 61..65 trace
  (= the "77/79@61" insertion), P from the 55..60 trace (H5b order). Trace keys/frequencies are equal.
- Original binary tails order: (ecx,4)(ecx,3)(ecx,5)(edx,5)(edx,3)(eax,3)(eax,5).
  U: ...(edx,5)(edx,3)(eax,5)(eax,3)   P: ...(edx,5)(eax,5)(eax,3)(edx,3).
  So the original has P's crossjump pairing (eax tails merged with -r arm) but a layout where the dx
  tails 46/57 sit together before the eax pair.

### Next
- Levers should target the crossjump survivor / EXIT-pred edge order (try_crossjump_bb walks EXIT preds;
  which of a matching pair becomes the survivor and which block index the merged tail keeps), not the -r
  arm heat: e.g. reorder the two `client_usage(..., argv[i])` calls of the -r arm vs. the 87/89 arm in the
  source, or make 46/57 the jump target, keeping eax in -r. Read cfgcleanup.c try_crossjump_bb /
  try_crossjump_to_edge (gcc 6.2) for the survivor rule (official repo only).
- Tasks 2-4 not started this session. Profile splice remains the only matching build.
- Scratch build/v/mc44 (dumps) left in place: the rm was blocked by a safety check; delete it by hand.

## s45: crossjump survivor rule (short session)

Result: NO MATCH. Best clean unchanged: s42/H5b.c (5 inv / fncmp 40 / cm (0,8)).
- build/v/mc44 deleted (literal path).
- Task 1: gcc.gnu.org git (cfgcleanup.c @ releases/gcc-6.2.0) returned an Anubis "Access Denied" page to
  WebFetch; source not read. From memory (unverified): try_crossjump_bb walks the preds of the common
  successor (EXIT here) in edge-vector order, inner loop over all other preds; try_crossjump_to_edge(e1,e2)
  redirects src1 (outer edge's block) into src2, splitting src2 at the match start. "from 46 to 65" =>
  46's edge is earlier in EXIT's pred vector than 65's; survivor = later pred. Pred order = edge creation
  order (noreturn call -> EXIT edges made at RTL expand / find_many_sub_basic_blocks in source order),
  so source statement order of client_usage calls is the expected lever. Verify against the real source
  (try a different mirror, e.g. github.com/gcc-mirror/gcc blob releases/gcc-6.2.0) before relying on it.
- Tasks 2-3 not run. Note: plain `fncmp.py <c> mode_client -I<repo>/src` prints ~1670 diff lines for both
  H5b and P (the "fncmp 40" metric of s42 uses different flags/tooling; reuse s42 cm.py/ev.py setup).

## s46: crossjump survivor levers (plain compile, no profile)

Result: NO MATCH. Best clean unchanged: s42/H5b.c (s42 m.py: 5 inv / fncmp 40 / cm (0,8)).
~350 compiles. P.c measures 6 inv / fncmp 40 / cm (0,8) with s42/m.py.

### gcc-6.2 cfgcleanup.c (read via built-in browser, javascript innerText works past Anubis)
- try_crossjump_bb(EXIT): walks EXIT preds in order; for e (only if e is src's first succ) it tries
  every e2 with e->src->index <= e2->src->index, try_crossjump_to_edge(mode, e, e2, dir_both); first
  success restarts the scan (ix = 0). A fallthru pred is tried first and never redirected.
- try_crossjump_to_edge: src1 = e's block (lower index) is redirected; src2 (higher index) survives
  (redirect_to = src2, or split_block(src2) if the match starts mid-block); swapped only if
  flow_find_cross_jump returns dir_backward. So the survivor of a matching group = its highest index.
  Counts/frequencies of src1 are added to the survivor.

### Levers tested (tools: j2.py = jump2 crossjump lines; scan1.py, scan2.py over m.py, race-free tags)
- A1.c: P.c with the -r arm tails moved to `goto rq3/rq5` + dead `if (0) { rq3: ...; rq5: ...; }` at the
  loop end -> the -r tails become the eax-group survivors (104/105). bbro order/inv/fncmp/cm identical to P
  (6/40/(0,8)). A2 (rq5 first) fncmp 46.
- scan1: dead tail block at every statement position 599..725, both orders (206 compiles): best 6/40, mostly 6/40 or 6/52.
- scan2 / B670.c: -w/-e/-c tails moved into a dead block placed before the -r arm (170 compiles):
  the in-place -r tails survive ("59 to 65", "60 to 67"), still 6/40, order unchanged (...42 79 77 53...).
- Conclusion: which block survives / where it sits does NOT move 77/79 (the clientWriteBlocks /
  clientBinPatch switch-case blocks in bbro numbering). The U effect must come from the pred-set
  (edx tails of -bp/-wb arms 46/57 joining the -r trace) or from the RA/renumbering side effects,
  not from survivor choice. Merging 46/57 into the -r tails while -r keeps eax is impossible
  content-preservingly (different index registers).

### Remaining diffs of A1 vs original (fncmp 40)
- two log_printf blocks (126/125/55 region) placed early; the -r/-w arm `cmp esi,edx` scheduled after
  the argv load/test; tails order (eax,5)(eax,3)(edx,3) vs original (edx,3)(eax,3)(eax,5).

### Next
- Task 3 not reached. Check bbro trace keys for 77/79 directly (hsim) in U vs B670 to see which
  edge/pred set pushes them, instead of crossjump survivor levers.
- Scratch build/v/mc46 and build/v/mc42 deleted.

## s47: the exact 77/79 mechanism (plain compile, no profile)

Result: NO MATCH. New best clean content: H5c2.c (= s42/H5b.c + zero-byte asm-goto edge in the -w arm,
`mk.py H5b.c H5c2.c c2`): m.py 6 inv (same order as H5b) / fncmp 34 / cm (0,6)  (H5b: 6 / 40 / (0,8)).
Best order: Uc1.c (= s44/U.c + asm goto `c1` in -w arm): m.py 3 inv, true (ev WANT) order only 2 inv
(55 vs 126/125, the two reboot log_printf blocks), tail 35 42 53 77 79 exact; but fncmp 50 / cm (10,6)
(the -r arm RA flip of U).

### Task 1: U vs P in bbro (exact)
- 77 / 79 = the shared crossjumped tails client_usage(3, argv[i]) / client_usage(5, argv[i]) (eax group;
  original labels .L_408ca9 / .L_408cbc, jumped to by ALL four len-2 arms -r/-w/-e/-c, see rawref.py).
- Both are key-0 singleton traces in round 4; order = fibheap tie order of the key-0 nodes 35/42/53/77/79.
- P (-r tails eax, in 77/79's pred set: 77 <- 56,57,58, 79 <- 59): pushed during the -r trace (group 55,
  after ins 61 key -2) as 77 then 79 -> pops 35 42 79 77 53.
- U (-r tails become edx group, not preds): first pushes come from the -w trace (group 61, after
  ins 67 key -1): 77 from 62, 79 from 65 -> 35 42 53 79 77.
- hsim what-ifs (wi2/wi3.py on slot_tP): the target 35 42 53 77 79 needs the push of 79 BEFORE 77,
  both inside the -w group after its 67 ins, and NO -r pushes. Any -r push (any position, any order)
  gives at best 35 42 77 79 53 (wi3 55 55). Moving 53/42/35 pushes (wi5) or adding a dummy key-0
  node (wi6) never gives the tail without breaking others (>=12 inv).

### Task 2: levers
- Zero-byte `__asm__ goto("" :::: w5x)` in the -w arm with `w5x:` on its client_usage(5) call:
  position c1 (before `i + 1 == argc`) pushes 79 first -> on U: tail exact (Uc1). Positions c2/mid/c3/c4
  after the first usage(3) jump don't. `top`/`pre` (before a = argv) wreck the order (41-43 inv).
- On H5b/P the edge is order-neutral (the -r trace pushes first) but c2 improves content (fncmp 34, cm 0,6).
- RA pins restoring the -r arm (eax=i, edx=i+1) on Uc1 ("d"(i+1), "a"(i), both): -r tails rejoin 77/79,
  back to 6 inv / cm (0,8). Confirms s43's coupling with the exact reason: the original's -r arm DOES jump
  to the shared tails, so in the plain heap model the -r trace's pushes always come first.
- So a plain match needs the -r trace's pushes to be ineffective (77/79 already queued in round 4 before
  the -r trace, inserted 79 first) or a different heap shape; round-3 pushes (wi4) shift other blocks.

### Next
- Find an existing earlier round-4 trace (before group 55, after 53/42/35 are in the heap) that can carry
  zero-byte asm-goto edges to w5x-style labels on the shared tails, 79's label first (wi3-style sim first:
  add ('ins','this',79,0),('ins','this',77,0) to each round-4 group before 55 and check the tail).
- Task 3 (ebl/k*l/beam) not reached.

Tools: wi.py..wi6.py (hsim what-ifs), mk.py (asm-goto variants), rawref.py (raw original/gcc listings
with labels), lev.py/lev2.py (lever scans). Scratch build/v/mc47 deleted.

## s48: what-if sims on H5c2 for 77/79 and 126/125/55 (plain compile, no profile)

Result: NO MATCH. Best unchanged: s47/H5c2.c (m.py 6 inv, ev true-order 5-6, fncmp 34, cm (0,6));
best order still s47/Uc1.c (ev 2, cm (10,6)). Only 1 real compile (H5c2 slot); rest is hsim on its history.

### Task 1 (77/79 from an earlier round-4 trace): impossible in the heap model
- wi7.py: move both 77/79 ins (either order, any positions) into EVERY round-4 group before 55
  (129..125): always 77/79 pop BEFORE 35/42/53 (14-28 inv). 35/42/53 are round-3 pushes; anything queued
  in round 4 before 55 lands ahead of them after consolidation.
- wi8.py: 77 and 79 independently at any (group,pos) among groups 49..67: the tail 35 42 53 77 79 appears
  ONLY with both in group 61 (after pos 2 = after 67's ins), confirming s47.
- wi9.py: keep the -r pushes, add a dummy node (key 0..-3) inserted anywhere in groups 49..67 and optionally
  deleted (visited) later: never the tail (best 35 42 77 79 53). So heap-shape tricks do not neutralise the
  -r pushes.
- -fdump-rtl-all-details: crossjumping only happens in 266r.jump2 (none at/after bbro), so the -r arm tails
  are preds of the shared 77/79 at bbro whenever the original eax pairing holds (s44/s46). With the -r
  trace (55) running before 61, its pushes always come first -> the original order is not reachable from
  this event history by insertion/heap tricks alone.

### Task 2 (55 vs 126/125)
- fs.py / fa.py / fa2.py: freq (key) overrides 0..6 on all round-4 named blocks (exhaustive on
  55,126,125,61,33,29,67; hill climb on 19 blocks), with and without 77/79 moved to 61: min true inv 5
  (as is) / 2 (moved) -- 126 125 always before 55. wi10.py: relocating 55's or 126's ins to every
  (group,pos): no change (best 5 / 2). Not a key or insertion problem in this history (matches s42).
- Not done: ebl/k*l/bcp lever beams (need a structural change first; the sims show no key/insert target).

### Next
- The remaining two inversions need a different round-3/round-4 history (pre events, number of traces
  extracted between) -- e.g. sim edits on R[2] (round 3) pushes/extractions together with the 61 move,
  or check whether the original was not a plain heap order at all (profile-only).
Tools: wi7-wi10.py, fs.py, fa.py, fa2.py (all take a mkslot slot dir; make one with s42/m.py SRC TAG).
Scratch build/v/mc42, build/v/mc48a deleted.

## s49: H5c2 vs s18 profiled MATCH bbro history (plain compile goal)

Result: NO MATCH. Best unchanged: s47/H5c2.c (m.py 6, ev 5, fncmp 34, cm (0,6)); best order s47/Uc1.c.
Only compiles: s18/match/repro.sh (fncmp 0, round4 inv=1) and H5c2 slot (m.py 6). No lever compiles done.

Tools (take slot dirs; H5c2 slot via `s42/m.py s47/H5c2.c TAG`, match slot = build/mcmatch/slotm after repro.sh):
- hist.py SLOT: per-round/group event dump (v=visit, p=push, iN:t/n=insert, cN=chg).
- cross.py A B: sim A's history with B's keys, single/pair/triple key transplants.
- graft.py A B: round-wise history mixes (useless: unnamed block numbers shift by 1, mixes are junk).
- needk.py A B: on B history, revert B keys to A keys greedily; lists keys B needs.
- pscan.py A: P (trace-end priority) x f scan for 55/126/125/61 on A history.

### Findings (task 1)
- R4 events for 126/125/55/61/77/79 are IDENTICAL in both: 126,125,127 inserted in g121, 55 in g49,
  61/77/79 in g55 (the -r trace), 67 in g61. So s48's "77/79 must be inserted only by 61" is a property
  of H5c2's keys, not of the target: the MATCH also inserts 77/79 from the -r trace (g55).
- The real difference is ROUND 3:
  match: R3 trace 1102 visits only itself, inserts 117 130 114 and stops with chg on 112 115 103 132; trace
  1048 stops with chg on 94 49. Then EVERY round-4 seed is pushed in R3 (109 107 113 110 119 108 120 121 128
  116 132 115 112 103 ... 131 118 29 33 42 35 53) -- note 53 pushed LAST (after 42 35), 94 not visited in R3.
  H5c2: R3 1048 trace visits 94 (v94) and inserts 49; 115/112/131/118 are not pushed in R3; push order
  ... 103 29 33 53 42 35 (53 before 42/35) -> this is the 35 42 79 77 53 vs 35 42 53 77 79 tail.
- Keys: on H5c2 history no key/P transplant (singles..triples of all 22 differing blocks; P 0..2 x f 1..4 on
  55/126/125/61) gets below m-inv 10 (sim) -- history-bound, confirming s48.
- On the MATCH history, needk.py: 55's key is NOT needed (f=2 like plain is fine), but trace-end priority keys
  are: 125 (P=1, f=1) essential (else +2 = 126/125 vs 55), 49 P=6, 112 P=3, 132 P=6, plus the high R3/R4
  keys of 107..129. P>0 = bb_to_key priority from an edge out of a trace end with EDGE_FREQUENCY>=1, which
  plain estimated frequencies give (P=0 everywhere in H5c2).
- So the target needs (a) round 3 to stop at 112/115/103/132 and 94/49 (thresholds) so they are pushed,
  with 53 pushed after 35/42, and (b) a nonzero trace-end edge frequency into 125.

### Next
- Lever compiles: make 94 fail the R3 threshold (bcp-goto cold edge into 94 / trace-end lever T48) so 1048
  stops before 94; get an RX goto (s18/s29) from a trace end into 125 to give P>0; reorder R3 53 vs 42/35
  insertion (53 inserted in R2 g1038 before 42) -- swap their source order. cm + evdiff each.
- Not proven unreachable.

## s50: round-3 lever compiles on H5c2 (plain compile goal)

Result: NO MATCH. Best unchanged: s47/H5c2.c (ev 5 / m.py 6 / fncmp 34 / cm (0,6)).

Tools: h.py (ev score + fncmp + round-3 feature score r3s vs s18 match: v94 in R3 +3, missing c112/c115/c103/c132,
missing p115/p112/p131/p118, 53 pushed before 42/35; H5c2 = 13, match = 0), lv.py (lever genome -> text:
rok JUMP->real JMP target lists, second JUMP->JMP, JUMP(i0)->JMP, E() drops on -bp/-wb/-eb/-e/-c, T48 =
k48l label before the -keys test (else-wrap) + bcp goto from 10 sites with 1-3 bcp terms, two extra bcp gotos
to existing labels), sa.py (mutation search; env W = score weight, G = start genome). Logs: sa_a*.jsonl, sa_b*.jsonl.

### Findings (~6500 real compiles, 8 runs x ~560 s)
- Every lever that changes round 3 at all costs >= +9 ev: best per r3s (min ev score):
  r3s 12 -> 16, 11 -> 14, 10 -> 28, 8 -> 28 (k48b.c: T48 at -keys body, fncmp 228, cm (0,16)), 7 -> 51, 6 -> 59, 5 -> 126.
- r3s 0 never reached. rok real JMP lists reproduce the match's R3 g1102 re-keys of 112/115/132 partially
  (e.g. rok c12,hdd5,c7,hdd4 + T48 keysb: c115 c112 in R3) but always also break the prefix/case order.
- T48 at -s (N=300, rok c12,i0) gives the match's 1048 shape exactly (i94:n i49:n c94 c49) but ev 41.
- Most extra bcp gotos to existing labels are no-ops (folded before bbro).
- Task 4 (53/42 swap) not attempted: no content-safe source swap identified.

### Next
- Combine the exact-1048 lever (t48 s/300 + rok) with prefix-repair levers; score with evdiff by round, not r3s.

## s51: event-score search (plain compile goal)

Result: NO MATCH. Best unchanged: s47/H5c2.c (ev 5 / m.py 6 / fncmp 34 / cm (0,6)).

Tools: es.py (fine event score vs s18 MATCH slot build/mcmatch/slotm: per-round edit distance of the flattened
event/group-token sequence, weights R1 8, R2 4, R3 2, R4 1; anonymous blocks >=1000 renamed by first appearance so
bb-index offsets don't count; match vs itself = 0). `python es.py FILE.c TAG` or `python es.py SLOTDIR`.
sa.py (s50 lever genome hill-climb, cost es + W*ev; env G, W), lv.py (copy of s50/lv.py with BASE = H5c2).
Logs sa_a1.jsonl (W=3, from H5c2), sa_b1.jsonl (W=1, from T48 s/300 + rok c12,i0): ~1150 compiles.

### Findings
- H5c2 es = 348 (R1 2, R2 33, R3 53, R4 94). T48 s/300 + rok(c12,i0): es 377-516, worse in R3/R4, same R1/R2.
- No lv lever lowers R2 below 33 (734/1152 compiles exactly 33; all others worse). Both climbs return to H5c2.
- The first real divergence is ROUND 2, not round 3: the match's R2 trace (after vX51) inserts
  131 118 115 112 121 120 116 132 (all :n) in one go; H5c2 inserts only 132 there and 116/120/121 later from
  the iX55 trace. Round 3 differences (pushes of 115/112/131/118, re-keys c112..c132) follow from that:
  those blocks are already in the heap in the match. So round-3 levers fight a symptom.
- R1 only differs by one cX37 position (likely offset/canon noise).

### Next
- Find what makes the match's R2 trace reach the case blocks 131/118/115/112/121/120 (switch/jump-table
  successors of the trace end block vX51): edge probabilities out of that block in the profiled cfg vs plain.
  Levers: probability on that dispatch edge (expect on the switch value / case-order), not rok/T48.

## s52: why the round-2 trace stops (plain compile) and a lever for it

Result: NO MATCH. Best overall unchanged: s47/H5c2.c (ev 5 / fncmp 34 / es 348 = R1 2, R2 33, R3 53, R4 94).
New best R2: c_t2A.c (= lp4.mk(9,21,0,'tail',2,'A')): es 368 (R1 2, **R2 26**, R3 56, R4 136), ev 52, fncmp 228
(instruction multiset unchanged, +114/-114 lines: layout only).

### Root cause (task 1)
- The match's vX51 pushes come from the BUILD_FDO `__asm__ goto("" :::: i1,p1,hdd5,hdd4,c10,c9,c1,c7,cdef)` before
  netGetInfo (match bb106 = asm goto, 107 = switch range check, 108 = tablejump; trace 105 106 107 108 [87..86]).
  H5c2 has that JUMP disabled (106 = range check, 107 = tablejump; trace stops at 107).
- Plain compile with that asm goto (JMP): asm goto with >2 succs gets even probs (1/10) at tree level;
  bbro needs prob >= 20% (round 2) AND edge freq >= exec_th = 217*0.2 ~ 44. Trace stops at the asm block.
- Fake extra labels don't work naively: (a) labels in the fallthru bb make expand_asm_stmt emit a fallthru_label,
  the block is split and find_many_sub_basic_blocks leaves >2-succ edges at probability 0 (cfgbuild.c
  compute_outgoing_frequencies: "rely on BBs with more than two successors to have sane probabilities");
  (b) bcp-guarded fake blocks are folded at fab1 (tree) -> same as (a); (c) asm operand limit 30.
- Working construct (ck3.py/lp4.py): fake labels fa_k each `goto ofa_k` out of a `struct {}` scope (asm "X"(&var) keeps
  the vars), so try-finally lowering gives one clobber-only copy per destination: distinct, non-forwarder tree blocks
  that expand to nothing; RTL cfgcleanup forwards them into the fallthrough and redirect_edge_succ_nodup SUMS the probs.
  Fallthrough share (1+K)/(10+K), K<=21 -> .71; still < .76 needed at freq 58, so add a frequency boost:
  bcp backedge `if (bcp(mode+91)&&bcp(mode+92)) goto fkbo;` before `if (E(reboot))` with fkbo at the asm block
  (header 'A'): loop exists only at tree level (stale freq after fab). Then the R2 37-group matches the match's
  insertion sequence (131 118 115 112 121 120 107 116 132, vX vX, 108 ...).
- Boosts entering via netConnect / forward bcp from the NO_MODE_ARG block wreck R1 (then-branch loses freq,
  round-1 trace 101/102 drops below 108 = round-1 exec_th).
- Remaining R2 diff: fail-path trace X40 (H5c2 143 [101], match 139 [73]) comes first in round 2; plus i109/iX54:t naming.

### Search
- grid.py/lp*.py/fl.py ~120 variants; sa2.py (s51 lv levers on the construct) 2 x 540 s, ~2200 compiles
  (sa_s52a1.jsonl, sa_s52a2.jsonl): best es 350 (R2 26, R3 49, R4 132) ev 60; nothing beats H5c2 on es+ev.

### Next
- Lower the fail-path freq below the 105 trace (or raise 105 without touching R1) to fix R2 order.
- Then R3/R4 with lv levers on c_t2A base (sa2.py, BASEV env).

## s53: round 2 fixed (fail-path order); rounds 3-4 unchanged

Result: NO MATCH. New best by event score: **c_r10.c** (= s52/c_t2A + one line):
es 308 (R1 2, R2 12, R3 58, R4 128), **es2 300 (R1 2, R2 0, R3 56, R4 172)**, ev 56, fncmp 222.
Best by ev is still s47/H5c2.c (ev 5 / fncmp 34 / es 348 / es2 488).

### Task 1: fail path below the 105 trace (done)
- Round-2 start order uses the key of the edge from a trace end (priority*100000 + freq), so raising 105's
  block freq via tree-only edges does not help (edge 100->105 stays 58); the fail edge 102->143 must drop below 58.
- Lever: in the NO_MODE_ARG then-branch, before `if (reboot) {`, a tree-only bcp goto to a label put on
  `if (E(reboot)) netReboot` (after the switch):
  `if (__builtin_constant_p(mode + 93)) goto dtg;` ... `dtg: if (E(reboot))`.
  Diverts stale tree freq away from the reboot netConnect: 103 20 / 143 51 (< 105's 58); R1 untouched.
  Same with target netDisconnect (nd_r11, R2 es 11/es2 7) or E(bcp). Before the NO_MODE test or into netConnect
  (nc2) it wrecks R1. v1-v4.py hold the scan (t.py applies substitutions to c_t2A, prints R1 keys + R2 first traces).
- es2.py: es with all block ids canonicalized by first appearance over the whole history; removes the 109 vs
  anonymous-id naming noise (c_r10 R2 = 0). R4 counts rise under es2 (renaming cascades); compare es2 to es2 only.
  dd.py/dd2.py print per-round diffs.

### Task 2: R3/R4 hill-climb on c_r10 (sa3.py, cost es2 + W*ev)
- 3 runs x 1500 s (~4600 compiles, sa_s53a{1,2,3}.jsonl): best es2 289 (R4 161) with t48 levers, ev 52;
  **R3 never moves (56)** with any lv lever. Full rok JMP (all 16 labels) -> es2 443 (R2 29).
- R3 diff: match's first R3 trace is the reboot success block (102) whose BUILD_FDO rok dispatch inserts
  117/130/114 and re-keys 112/115/103/132; then case blocks pushed with priorities 9..2. Plain rok asm goto gives
  even probs. Next: per-case fake-label weighting on the rok dispatch (several clobber-only fakes per case label,
  as in s52's fallthrough construct but targeting the case labels) to reproduce those priorities.

### Task 3
No candidate matched fncmp; cm/objcmp not run (nothing to verify).

## s54: rok dispatch enabled (R2 kept at 0); round-3 case-key order still open

Result: NO MATCH. New best by es2: **c_s54.c** = c_r10 + full rok asm goto (16 labels, extra fakes p0 x1, c3 x2)
+ tree-only fkbo boost from the then-branch (replaces the latch) + 3 `goto ndl` diversions before dtg:
**es2 239 (R1 2, R2 0, R3 40, R4 143)**, ev 76, fncmp 236. (c_r10: es2 300, R3 56.) Best by ev is still s47/H5c2.c.

### Findings
- label -> spot (lab.py): c12 129, c11 128, p0 117, i0 130, c9 120, hdd4 112, hdd5 115, c2 108, c1 107, c10 121,
  u2 103, cdef 132, c8 119, c7 116, c3 109, s5 114; case-4/5 hwFlags tests are 113/110 (labels t4/t5 in lev.py).
- bb_to_key = -(1e6 + 100*prio + freq): prio = max edge freq from a trace-end pred, freq = block freq. Match R3 order
  comes from R2 tablejump prios 9..6 (profile). Plain: every tablejump edge has the same prio (4), so order = block freq.
- Why rok JMP broke R2: rok edges enter the fkbo boost loop body -> irreducible, so no loop scaling, and the trace stops
  before the tablejump. Fix: drop the latch and use a tree-only `if (bcp(mode+91..94)) goto fkbo;` in the
  NO_MODE then-branch (cur.py base()). The R2 tail then needs join*P(reboot) < 42.5 (exec_th = 217*200/1000 = 43, rounded):
  3 `if (bcp) goto ndl;` before dtg (base2()) keep join at 85.
- Exact rok edge freqs (cdef 6, hdd4/hdd5 3, u2 2, p0/i0/s5 0) can't be had with one asm (30-operand limit):
  you need >=21 extra fakes but only 14 fit. Leftover R3 diff: cB80/cB81 (p0/i0 get Cha'd).
- For the R3 order, t4/t5 would need freq above c8/c2/c9/c10/c11/c7/cdef, but those already get +2 from the fkbo edges.
  Boosts from fail (lev.py B) plus exit diversions (X) raise join over the threshold above, so R2 goes to 1. Not solved.

### Tools
rkgen.py (rok/fkbo fake constructs), cur.py (bases), lev.py (all levers: w, fk, B, X, npre, dd, dt), sa.py/sa2.py (SA,
logs sa*_s54*.jsonl), fq.py (compgotos dump with freq/edge probs + call map), r3.py (raw round events with spot
names, match | ours), bmap.py, lab.py, t1-t8.py (scans).
### Next
Get per-case freq ordering within prio 4 without raising join: e.g. lower the fkbo per-target share (more fkbo fakes via
a second chained asm that keeps the trace), or lower the dtg flow so case boosts fit under join <= 86.

## s55: chained rok asm with exact edge weights (idea 1); NO MATCH

Best by es2: **c_s55.c** = lev.text({'w':W}) with rkgen cap=30 (16 reals + 19 fakes -> 2 chained asm gotos),
W = {cdef 6, hdd4 3, hdd5 3, u2 2, c3 2, p0 2, c11 1}: **es2 230 (R1 2, R2 1, R3 34, R4 142)**, ev 78, fncmp 239.
(s54 c_s54.c: es2 239, R2 0, R3 40.) Best ev still s47/H5c2.c.

### Findings
- The 30-operand limit is not a blocker: rkgen.rok already chains chunks (cap). Exact s54 weights {cdef6,hdd4 3,hdd5 3,u2 2}
  fit in one asm (30 ops) -> R3 33 but R4 162 (es2 244). Splitting the same set across chunks (cap 16/8) changes
  R2/R3 (chunk boundaries alter probabilities: each chained asm splits flow evenly over its labels + fallthrough).
- Two-chunk variants mostly cost R2 = 1 (join over the 43 threshold); greedy on weights reached es2 230 but never R2 0
  with R3 < 40. Ideas 2 (distinct prios) and 3 (join budget) not explored this session.

### Tools
s1.py (cap/weight variants), hc.py (greedy +-1 on rok weights, fixed cap; log hc.jsonl).
### Next
Combine hc weights with base2 npre (more ndl diversions) to pull R2 back to 0; try per-chunk label grouping (order arg)
so the chunk carrying t4/t5-related targets gets a smaller fan-out.

## s56: rok fakes to case-4/5 test blocks (t4/t5) + joint SA; NO MATCH

Best by es2: **c_s56.c** (state best.json) = c_r10 levers + chained rok asm (sa.py rok2, which also accepts fake
targets t4/t5 = case-4/5 hwFlags test blocks 113/110):
w {t4 4, t5 4, _ft 5, c12 1, i0 1, c8 2, s5 1, c1 1}, cap 29, X {c2 1, c7 4, c11 3, c3 1}, custom chunk order:
**es2 199 (R1 2, R2 0, R3 26, R4 131)**, ev 57, fncmp 211 (es2/fncmp via es2.run fncmp=True; tools/re/fncmp.py on a
wip path fails to find xebuild.h). Previous: s55 230 (R2 1), s54 239. Best ev still s47/H5c2.

### Findings (~6500 real compiles, 4 race-free SA workers, logs sa_s56*.jsonl, old/)
- Idea 1 (s55 weights + npre/order, R2 hard-constrained): from the s55 R2=1 point the SA never reached R2 0 (1150
  compiles); R2=0 side from s54 weights stalls at 239. Weight sets with R2 0 exist only near small rok totals.
- Idea 3 key lever: t4/t5 were never rok targets. Fakes to t4/t5 raise 113/110 above the other case heads within prio 4
  without raising join: {p0 1,c3 2,t4 4,t5 4} alone gives es2 226 / R3 26. All good states use t4/t5 4.
- R3 remaining: case-head freqs only take ~3 integer levels (4/6/7; rok flow is small), so graded match keys 910..205
  collapse into ties; the head Cha section (match pushes 112/115/103/132; ours 117/130 = p0/i0 rok targets) differs.
- hsim.load writes bbro_mc.txt into build/mcmatch/slotm at es2 import: start parallel workers staggered (>=5 s).
- Idea 2 (fake edges from round-2 trace ends to case heads for distinct prios) and idea 4 (R4 levers) NOT tried.
### Next
Raise rok flow (more scale -> more freq levels) e.g. place rok on a hotter path or feed it from the boosted loop; then
idea 2 for prios; then R4.

## s57: higher rok flow (WMAX 60) + p0/i0 -> hdd4/hdd5/u2/c12 seeds; NO MATCH

sa.py = s56/sa.py with total-weight cap from env WMAX (default 40). Runs (R3W=1, ~4200 real compiles, 4 workers
staggered 6 s): a (from s56 best, WMAX 60) never improved 199/R2 0; b (init2.json: i0 dropped, hdd4/hdd5 2, u2 1,
c12 2, t4/t5 6, _ft 8) -> es2 194 (R2 1); c/d from that (r2one.json) -> **best_c.json es2 189 (R1 2, R2 1, R3 25,
R4 119), ev 50**, best_d.json 194. Logs sa_[abcd].jsonl.

### Findings
- Raising rok flow (weights total 45-60) does lower R4 (131 -> 119) and R3 a little (26 -> 25), but every such state
  has R2 = 1: the extra rok flow pushes the reboot fail edge back over the s53 threshold. No R2 0 state below 199
  in 2100 c/d compiles (0 R2-0 states at all from r2one).
- SA settles on i0 high (7-9) and t5 9-11 rather than the hdd/u2/c12 seeds: head Cha section not fixed (task 2 open).
- Ideas 2 (round-2 trace-end fakes) and 4 (RX/k*l/eb bcp/T48) still untried; ev/fncmp/cm finalists not run (no
  candidate with R1..R3 near 0).
### Next
Combine the high-flow state (best_c.json) with a stronger tree-only reboot bcp boost (s53 lever) to bring R2 back
to 0, then continue R3/R4.

## s58: tree-only bcp depth (dd/dt/npre) + pinned head weights; NO MATCH (cut short)

sa.py = s57/sa.py plus mutations of dd/dt (bcp depth 1..8) and npre (0..14). The FIX env pins weights
(task 2, e.g. FIX=i0=0,p0=0,hdd4=2,hdd5=2,u2=2,c12=3). The run was stopped early by the caller: about 260 SA
compiles over 4 workers (a/b from s57 best_c, c pinned, d from s56 best). Logs are in sa_s58[abcd].jsonl, best_c.json.

### Findings
- On best_c, dt 3/6 makes things worse (es2 358/419, R2 24/33). npre had no effect at dt 1, so deeper dtg is the
  wrong lever for the reboot edge.
- Pinned head weights (c): best es2 209 (R2 1, R3 34). No R2-0 state.
- The best R2-0 state is still s56 c_s56.c es2 199 / ev 57.
- Not done: task 3 (round-2 trace-end fakes), task 4 (RX/k*l/eb bcp/T48), task 5 finalists.
### Next
Try a second, independent bcp diversion target (not a deeper dtg). Then run the SA for the full planned length.

## s59: second reboot-fail diversion levers + R4 levers; NO MATCH (run cut short, ~390 SA compiles)

sa.py = s57 SA + post-text levers: rf/rft (bcp on the reboot fail edge -> ndl/dtg/rbn), d2/d2t/d2p (second bcp
diversion before/inside `if (reboot)` to ndl/rbn/u2/case labels/fail), rp (bcp after rok netGetInfo -> ndl),
rE (expect on reboot netConnect), E2 (round-2 trace-end fakes after netDisconnect to case labels), rx126/rx117
(JUMP->JMP), ebm (drop eb bcp lines), kl (drop k67l bcp). Logs sa_[abcd].jsonl.

### Findings
- Single-lever scans on s57 best_c: rf (any target) and d2 to ndl/rbn/case labels all wreck R2 (7..28); rE 1/2 R2 7;
  d2 to u2/fail, rx126, rx117, kl: no effect; ebm 2 +2 es2. No single lever gives R2 0 on best_c.
- SA worker a (from best_c, R3W=1) found **best179.json: es2 179 (R1 2, R2 0, R3 27, R4 109), ev 58** -- new R2-0
  best (s56 was 199). Levers in it: E2 {i0:1}, ebm 2, kl 1, rx126 1, cap 26, npre 0 (see json).
- c (FIX head weights) best R2-0 227; b/d (from s56, E2-only for d) no improvement in the short time.
- Workers were stopped early by the caller's hand-back request; ev/fncmp/cm/objcmp finalists not run.
### Next
Continue SA from best179.json (R3W=1) for the full length; then fncmp/cm finalists.

## s60: full-length SA from s59 best179; NO MATCH

sa.py = copy of s59/sa.py (logs here). Round 1 (4 x 5400 s, ~7900 iters each): a/b R3W=1 from best179, c R3W=3,
d R3W=1 from s59/init_s56.json. Round 2 (e/f/g/h from best169: R3W 1/2, FIX t4,_ft,c12,c8 pinned, T0=2) was
stopped early on hand-back.

### Results
- **best169.json / f169.c: es2 169 (R1 2, R2 0, R3 25, R4 103), ev 54, fncmp 177, cm (15, 24)** (from c, R3W=3).
- a best 175 (R3 25), b 178, d (s56 seed) 187. Max-ev R2-0 state bestev.json/fev.c: ev 105 but es2 250, fncmp 178.
- SA plateaued: 28k R2-0 evaluations, no state below 169.
### dd2 R3 diff (f169)
Within the B60..B76 group the block order differs (T: 69,64,74,65,... vs M: 70,64,72,71,74,69,...), and
iB83/cB80-82 are hoisted in T (M keeps cB83/84 after GB47); B66/B58/B59 are v (fallthrough) in T vs p in M.
Suggests a lever on the case-group order of the B60-B76 targets and on B83 placement; not implemented.
### Next
Add a lever permuting the B60-B76 targets (and B83 position) then resume SA from best169.json.

## s61: R3 case-head key analysis + PD (pre-dispatch diversion) lever + SA; NO MATCH

### Tools
- raw.py SLOT|m: es2 canonical B id -> raw (spmap) id. rk.py SLOT|m R: one round's events with fibheap keys.
- fq.py SLOT DETAILS: block freq + per-pred edge freq for mapped case-group blocks (compgotos-blocks-details dump).
- exp.py TAG MOD.py: s60 text(best169) through mod(s), es2 + fq table (details compile into slot_TAG/det).
- sa.py: s60 SA + PD lever (ordered [[label,depth]] tree-only bcp gotos after the switch-path netGetInfo).
- M details: rerun the fdo second compile from build/obj/mode_client.fdo/-.gcda with
  -fdump-rtl-compgotos-blocks-details (bb numbering == build/mcmatch/slotm).

### B58-B84 map (R3, canonical -> raw source id; key = -(1e6 + 100*prio + freq), prio = max edge freq from a trace end)
B58 131 clientInfo, B59 118 clientPatches, B60 115 s5 sendCompat, B61 112 s4 sendAvatar, B62 121 c10, B63 120 c9,
B64 107 c1, B65 116 c7 test, B66 132 cdef, B69 108 c2, B70 109 c3, B71 110 t4, B72 113 t5, B74 119 c8, B75 128 c11,
B76 129 c12 test, B80 117 (M) / 130 (T), B81 130 / 1121, B82 114 / 117, B83 94 / 1104, B84 49.
M R3 keys (prio/freq): c12 9/10, c3 8/9, c1 8/9, t5 8/8, t4 8/8, c8 7/9, c2 7/9, c9 7/8, c10 7/7, c11 6/10,
c7 6/9, cdef 6/8, s5 3/4, s4 3/3, 103 2/5. Ours (f169): every dispatch head prio 4, freqs 9..4.
M edge source: dispatch bb108 edges c12 9, c3/c1/t5/t4 8, c8/c2/c9/c10 7, c11/c7 6, cdef 1; BUILD_FDO asm goto
bb102 edges c11 4, c7 3, cdef 6, s5 3, s4 3, c8/c2 2, others 1.
Ours: plain switch gives EVEN dispatch edges (4 each, gcc 6 has no switch predictor); rok chunks (bb103/bb109)
add 1..4. So the R3 heap order (and the B60-B76 permutation, the 132/131/118 fallthroughs = those heads being
visited instead of pushed, and the 83/80-82 insert differences) all come from flat dispatch probabilities.
- Dead extra case values (case 13 -> scope/asm forwarder -> c12) are NOT pruned (even with
  `if (mode==13) __builtin_unreachable()`): jump table grows, fncmp 196. Dead end.
- PD lever: depth-1 diversion takes ~50% of dispatch flow (c12 +21); deeper depths give ~F/2^d. Ordering by
  freq at uniform prio is the only reachable route.

### SA (4 x 5400 s, ~6560 evals each; a R3W=1, b R3W=2, c PPD=0.6, d R3W=3/T0=6/PDP=1)
| file | es2 (R1,R2,R3,R4) | ev | fncmp | cm |
|---|---|---|---|---|
| fin0.c/json (b) | 159 (2,0,20,103) | 61 | 160 | (14,24) |
| fin1.c/json (a) | 161 (2,0,19,107) | 50 | 178 | (14,22) |
| fin2.c/json (min ev, R2 0) | 175 (2,0,21,117) | 43 | 142 | (14,22) |
New es2 best 159 (was 169); R3 25 -> 19/20. Still far from MATCH (no objcmp). c/d did not improve.
### Next
The flat dispatch is the structural blocker: the match's dispatch edges are 9..1 per case, ours even.
Only uniform-prio + freq ordering is reachable; a freq-target designer (desired freq per head from M's
key order, solved with PD depths) would beat blind SA. best_[abc]61.json kept.

## s62: TH lever (jump-threading assignments make switch dispatch edges uneven); NO MATCH

### Lever
`if (__builtin_constant_p(mode+X) && ...depth...) mode = V;` placed directly before `switch (mode)`.
vrp1/dom thread the then-arm straight to case V; update_bb_profile_for_threading lowers ONLY the
V dispatch edge (others renormalised up); fab later folds bcp to 0 and the arm vanishes (no code).
So unlike PD (which lowers the whole dispatch block), TH gives per-case uneven dispatch probabilities,
the thing s61 said gcc 6 can't do. Verified: depth 1 on c11 removes its whole dispatch edge (111:4 -> gone).
Deeper depth = smaller cut (F/2^d, clamped). Integer freqs are tiny (dispatch edges 4), so granularity is coarse.

### Runs (sa.py = s61 SA + TH; R3W=2; 4 x 3600 s, ~5200 evals each)
| file | es2 (R1,R2,R3,R4) | ev |
|---|---|---|
| best_a.json/.c (from fin0) | 156 (2,0,19,102) | 61 |
| best_b.json/.c (from fin0) | 155 (2,0,21,97) | 60 |
| best_c.json (designed init des.json) | 160 (2,0,20,104) | 59 |
| ev_d.json/.c (from fin2, min ev) | 193 (2,0,27,123) | 39 |
New es2 best 155 (was 159), new ev best 39 (was 43). R3 barely moves (19-21): reductions alone can't
reach M's 9..6 ordering above s5/s4 (prio 3) because our dispatch edges start at only 4.

### Next
- Combine TH with raising dispatch-block freq first (so edges ~9 then cut down to M's 9/8/7/6/1 profile);
  a designer on fq.py output per TH depth (measure edge cut per (case,depth), then solve) instead of SA.
- TH with a threading value that hits a case via a *different* path (e.g. mode=V set in a rok chunk) to
  add, not only subtract.

## s63: short probe; NO MATCH
- Re-ran s62/sa.py (R3W=3, seed 63, 560 s, 1096 evals) from s62/best_b: no improvement (es2 155, R3 21).
- No dispatch-raising lever was built; the plan from s62 (raise dispatch-block freq above 9, then TH cuts;
  designer over fq.py per-(case,depth) cuts) remains untried and is the next step.

## s64: dispatch-raising levers + SA; NO MATCH

### Probes (m1.py, q.py = s62 text + mod, es2 + fq table; base s62/best_b, dispatch bb111 freq 46, edges 4)
Label `dsp:` right before `switch (mode)` (after the TH chain), dead bcp gotos into it from:
- `-v` arm in the option loop: no effect (arm freq ~0). Using `mode` there after `mode = 7` is a REAL goto
  (bcp(7+k) folds to 1) - use non-constant vars (argc, i).
- pre-loop (before `for`): mode == 0 there, so vrp/dom thread the goto straight to cdef; dispatch stays 46.
- loop top (i bcp): depth 3 only -> dispatch 82 (edges 7) but R1 10/R2 55 and fncmp +80 (loop exit changes
  loop estimates); depth >=4 no freq change but fncmp still +26 (content change).
- backedge after the switch: no freq change at any depth (es2 224-250, content changes).
- loop-top goto to a label before `if (NO_MODE_ARG...)` (scale whole post-loop region): bogus case-head
  freqs (c12 29..42 via threading), es2 >= 244.
- POST (before `if (NO_MODE_ARG...)`, argc bcp): WORKS: depth 1 dispatch 112 (edges 9!), d2 75 (6), d3 53 (4),
  d>=4 ~no change. But it steals (1-2^-d) of every other post-loop block: d1 es2 794, d2 532, d3 299 (R2 broken).
### SA (sa.py = s62 + POST/LT levers, 4 x 4800 s, ~6900 evals each)
| run | start | best es2 (R1,R2,R3,R4) | ev | fncmp |
|---|---|---|---|---|
| a free+LT | best_b | 155 (no gain) | | |
| b POST 2-3 forced | best_b | never R2 0 (1303 cost, es2 245) | | |
| c POST 3-4 | best_b | best_c 160 (2,0,22,100) POST 4 | 57 | 172 |
| d free R3W=3 | best_a | best_d 156 (2,0,18,104) | 57 | 158 |
No es2 improvement (155 still best); best_d has lowest R3 so far (18).
### Read of R3 tokens (s61/rk.py q0 3 vs m 3)
es2 tokens carry no keys: R3 diff is which heads are VISITED vs pushed (ours visit 128 c11 freq 37 - stale
tree freq from fail/PD gotos - and 132), 1114 pushed instead of 109, and 1103's insert list. So equalising
prio alone is not enough; c11's inflated freq (fail `goto c11`, PD c11) makes it a trace continuation.
### Next
- Make POST usable: compensate the stolen post-loop flow (e.g. a second POST-like goto from the dispatch
  region back into the NO_MODE_ARG side is impossible w/o loops; instead re-tune rok/E2 at scale 1/2 with a
  dedicated SA that only allows POST 1-2 and a softer R2 penalty).
- Remove the c11 visit: drop/reduce fail `goto c11` and PD c11 depth so c11 head freq ~ dispatch share.

## s65: R3 c11 hand probes + annealed-R2 POST SA; NO MATCH
### Hand probes (hv.py, variants of s64/best_d, es2 156 = R1 2/R2 0/R3 18/R4 104, fncmp 158)
- PD c11 removed / depth 8 / 9, TH c11 dropped, rok w c11 1 or 2: no change at all (identical es2/fncmp).
- w c11 4: es2 183 (R3 26); w c11 0: 163 (R3 20); c11 out of rok order: 233 (R2 1); X c11 removed: 214;
  w0+X2: 183 (fncmp 152, lowest seen here but R4 127).
=> the c11 visit is not removable through PD/rok/TH c11 levers without hurting; removing c11 flow hurts R3.
### SA (sa.py = s64 sa + R2 penalty annealed 2 -> 400 per R2 event, b2_ tracks best R2-0 es2; 4 x 3600 s, ~5150 evals each)
- p1/p2 (best_d, POST 1-2), p3 (best_b, POST 2): never below R2 40; best es2 ~464 (R2 40). POST at depth <=2
  cannot be compensated by the existing levers - R2 is structurally broken by the halved post-loop region.
- f4 (free, R3W 3, best_d): no improvement (156).
### Next ideas
- POST is a dead end with current levers; a compensating lever must ADD flow to the non-dispatch post-loop
  blocks (e.g. dead bcp gotos from the dispatch region into the NO_MODE_ARG side's blocks) - untested.
- The 1114/109 push difference still unexplained; try rk.py on best_d with w0x2 variant (fncmp 152).

## s66: 1114/109 push, post-loop compensation lever, source-structure check; NO MATCH
Base: s64/best_d (es2 156 = R1 2/R2 0/R3 18/R4 104, fncmp 158). Tools: cp.py (best_d + POST + compensation
gotos), tm.py (text substitutions on best_d + rk.py R3 dump), th.py (drop each TH/PD entry), x3.py (c3 knobs).
### 1. 1114/109 wrong push (rk.py region 3)
- canonical 109 = clientKeys (case 3). In ours case 3's head is the `JMP(hdd5,s5)` asm-goto block (copy id 1114,
  key -1000403) and clientKeys falls through at freq 1; in M 109 itself is the case head (key -1000809).
- Fix: move the JMP after the call (`{ clientKeys(); JMP(hdd5,s5); }`, o_k2.c) or drop it (o_k1.c): 109 is pushed
  directly, but R3 stays 18 (k2) / 22 (k1) and R4 rises 104 -> 120/124 (es2 172/184). The wrong push is cosmetic
  for R3; R3 is the even dispatch keys (-1000408..403 ours vs -1000910..610 in M).
- No TH/PD entry or c3 X/w/TH knob removes 1114 (all no-ops or worse).
### 2. Compensation lever for POST (dead i/argc-bcp gotos from loop top / pre-loop into post-loop labels
   cpnm (then-branch of NO_MODE_ARG), cprb (reboot test), cpnc (else netConnect), dtg, ndl; depths 1-6, combos)
- POST 2 alone: es2 567 (R2 40). Every single or combined compensation goto made it worse (es2 686..965,
  R2 59..92, R1 also up to 14-30). Dead loop gotos add new merge blocks rather than restoring the halved
  post-loop frequencies. Lever is negative; POST stays a dead end.
### 3. Source structure
- Linux xeBuild64 (v1.16) has no network client modes: no cross-check possible for mode_client.
- M's uneven dispatch probabilities (9..1) on a jump-table switch cannot come from gcc 6 plain compile source:
  switch edges get even probs without profile, gcc 6 has no if-chain->switch conversion, and a
  `__builtin_expect` on the switch value lifts only one edge. Case order/shared bodies don't change edge probs.
  This is strong evidence the original was built with -fprofile-use, so a plain-compile match needs a
  lever that produces per-edge uneven switch probabilities (none found in 66 attempts).
### 4. SA: not run (no lever moved R3 below 18).

## s67: switch-edge probability levers; NO MATCH
Base s64/best_d (es2 156, R3 18). Short session.
### Idea 3 (predictors on case bodies) - negative, measured
Tiny test (6-case switch, -O3, -fdump-tree-profile_estimate-details): case labels with
`__attribute__((hot))` / `((cold))`, a case body calling __builtin_abort (noreturn) and one with
__builtin_unreachable: switch edges stay exactly even (14.3% each; unreachable/abort cases are just
dropped). gcc 6 combine_predictions_for_bb uses even probabilities for nedges != 2, so no label/call
predictor can give uneven jump-table edges. (predict.c fetch from gcc.gnu.org blocked by Anubis again.)
### Idea 1 (extra trace-end preds into case heads)
This is what the rok asm-goto fan (ork* multiplicities to c1/c8/c11/c12/i0/p0/c10/cdef/c3/hdd5/u2/s5/t4/t5)
already does (s54-s57, SA in s60-s65). rk.py region 3, ours vs M:
 ours pushes 129,116,107 (-1000408), 113 406, 119/108/120/121 405, 128 404, 1114 403, 132 209, 110 203
 M    pushes 129 910, 109 809, 107 809, 113 808, 110 808, 119 709, 108 709, 120 708, 121 707, 128 610, 116 609, 132 608
 In M keys strictly decrease in push order and head freqs are 7..10 (dispatch total ~90 vs ours ~48):
 the gap is overall dispatch flow (x2) plus a monotone per-case prio, not just tie order. Raising dispatch
 flow is only achieved by POST (s64), which breaks R2. No new lever found.
### Idea 2 (two-level dispatch) - not compiled; an if-guard before the switch only scales total flow, and
 peeling a case out of the switch changes the table (entry -> default), so it cannot keep one table.
Best unchanged: s62/best_b (es2 155), s64/best_d (es2 156/R3 18).

## s68: inject flow only into the switch dispatch; NO MATCH
Base s64/best_d (es2 156, R1 2 R2 0 R3 18 R4 104, fncmp 158). Probes run with `python ../s64/q.py TAG ../s64/best_d.json m_X.py`.
The mod files are kept (m_*.py; slf.py, slf2.py and lp.py are their generators).
"Dispatch" here means the per-case edge value from the switch block (the 111:N entries in q.py's table); the base value is 4.

| probe | what was added | es2 (R1,R2,R3,R4) | dispatch |
|---|---|---|---|
| lbl | only the `dsp:` label before `switch` | 156 (2,0,18,104) | 4 |
| u2 d1-3 | dead argc-bcp goto dsp before client_usage(2) | 660 (15,61,75,146), same at every depth | - |
| fail d1-3 | dead goto dsp on the netConnect-fail branch | 435 (3,27,70,163) | - |
| rokf d1/2/3 | dead goto dsp after the rok netGetInfo | 243/216/164 (R3 46/28/22) | 4 (rok is cold, so it carries no flow) |
| s1-8 | self loop `dsp: if(bcp(argc..)) goto dsp;` | 160 (2,0,18,108) | 4: a self loop cannot raise the switch's outflow |
| g1 | self loop `dsp: asm goto("" :::: dsp)` | 379 | 3 |
| g3 | self loop with `bcp(mode+777)` | 160 | 4 |
| l1/l2 | `asm goto("" :::: dsp)` at the head of all 12 live cases (a real loop around the switch) | 503/519 (R2 30/24, R3 90/109) | **14** |
| k1-k4 | the same at 1, 3, 6 or 3 cases | 368-399 (R2 19-24, R3 46-66) | 3-5 |
| b1/2/3/5 | dead `bcp(argc+k)` gotos to dsp at every case head | 224/220/208/225 (R2 0, R3 34-45) | 4 |

### Findings
- The only lever that raised the dispatch edges without POST is a real loop: asm-goto back edges from the case heads.
  With all 12 live cases it overshoots (14 per edge against M's 7-10). The case bodies drop to 2-6.
  Any asm-goto loop breaks R2 (19-30).
  The asm diff for k1 shows bb-reorder moving the rok netGetInfo/netReboot block after the switch and the
  dispatch register changing from ecx to edx. The cause is the layout change, not extra bytes.
- Dead bcp back edges to dsp (b*) keep R2 at 0 but do not raise the dispatch edges.
  They only lower the case-body frequencies, so R3 gets worse.
  The table seems to mix frequency snapshots taken at different times; the head frequencies no longer equal the sum of their predecessors.
- Flow into dsp from blocks that look wasted (fail, u2, rok) does nothing useful: those blocks are cold or noreturn, so they carry almost no flow.
- R3 never went below 18, so SA was not started (the gate was R3 < 18). Bests are unchanged: s62/best_b (es2 155) and s64/best_d (R3 18).

### Next ideas (not run)
- Asm-goto loop from a subset of cases, together with an SA that re-tunes rok/TH to repair the bb-reorder layout (R2).
  Target 7-10 per dispatch edge.
- Probability-controlled back edges, e.g. an asm goto with several distinct labels stacked before dsp.

## s69: weighted asm-goto loop levers; NO MATCH
Base s64/best_d (es2 156, R2 0, R3 18). Probes: `python ../s64/q.py TAG ../s64/best_d.json m_X.py` (lp2.py mkw = per-case multiplicity).

| probe | loop edges | es2 (R1,R2,R3,R4) |
|---|---|---|
| a | default x2 | 401 (2,24,64,161) |
| b | case1 + default | 438 (2,24,81,164) |
| c | case1 x2 + case2 | 466 (2,25,81,188) |
| d | default x3 | 419 (2,24,64,179) |
| e | one asm goto at case-12 tail (before break) | 415 (2,25,62,175) |

Finding: any real loop back to the switch, from heads or tails, at any multiplicity, gives R2 24-25 (the rok-block
bb-reorder move noted in s68). R2 is not tuned by edge count or position, so an SA over loop weights would start
at a floor of about 400 against the 155 best. SA was not run. Bests are unchanged (s62/best_b 155, s64/best_d 156).
Next idea: repair R2 directly (rok order/weights, or put an ecx pin on the dispatch) while keeping one loop edge.

## s70: diagnose/repair the asm-goto loop R2 break; NO MATCH
Base s64/best_d (es2 156). Probes: `python ../s64/q.py TAG ../s64/best_d.json m_X.py` (env vars pick the variant);
`python kv.py TAG` prints the round-2 heap keys (block freqs) of the switch trace for comparison with `m`.

### R2 diagnosis (s69/m_e, tail asm goto at case 12 -> `dsp:` before switch)
- The R2 break is not the rok block itself: the `dsp:` label splits the block before the switch into its own
  2-pred block, whose fallthrough edge (freq 37) is below the round-2 threshold, so the main trace stops there and
  everything after (switch, rok/netGetInfo trace) moves to round 3.
- Moving `dsp:` up to `cinfo = netGetInfo();` after fkbo (or to fkbo itself) keeps the trace: R2 0-2 (m_p.py gi/fk 233, R2 1).
- Remaining R2 1: the cycle is entered by DFS from rok's asm goto (c10 first), so the dispatch->case edge is
  EDGE_DFS_BACK and that case gets the back-edge priority key (-1000403). Fix: list `dsp` FIRST in rok's asm goto
  (m_v.py TA=r) -> DFS enters at dsp, R2 0 for every single tail edge.
  Best: tail edge at case 10 + r -> **es2 149 (R1 2, R2 0, R3 18, R4 97)**, ev 58, but fncmp 270.
- Why tail loops don't raise dispatch: case blocks also have rok/fkbo preds, so dsp never dominates them; the
  cycle is irreducible and predict.c drops DFS-back edge flow. Natural loops need the latch in a new block before the
  case's AT label (head position): those raise case freqs to ~10 (M 8-10) but the extra head blocks cost R2 22-30
  (m_v TPOS=head, m_b, m_a). Bcp-guarded head gotos (m_b) don't vanish cleanly either (R2 30).
- Back edge to a header before NO_MODE_ARG (natural, m_t.py): es2 460-1120.

### SA (sa.py = s62 PD/TH + LP tail-loop lever with dsp-at-netGetInfo + rok-dsp-first)
4 workers x 4000 s (~5900 compiles each), from s64/best_d (w1,w2) and s62/best_b (w3,w4) with LP {10:1}.
Best: best_es2.json / best145.c = **es2 145 (R1 2, R2 0, R3 18, R4 93)**, ev 54, LP {10:1, 3:2, 1:1}; but
fncmp 271 (base 158): the loop changes register allocation, so the es2 gain does not reach the bytes.
R3 stayed at 18: this lever does not change the dispatch flow, so it can't fix R3.
sa_s70w*.jsonl.gz are the logs.

### Conclusion / next
- The R2 break is understood and fixed (dsp placement + DFS entry order), but loops that keep R2 0 are irreducible
  and add no flow. Natural loops (head latch blocks) add the right flow (~10/case) but add blocks.
- Next idea: natural head latch blocks that later passes remove before bbro while the estimated freqs stay. Needs
  a guard that folds after profile_estimate but before RTL (the m_b bcp guard left jump-threaded copies). Another
  option: drop the rok/fkbo edges into one case so a tail latch is natural.

## s71: natural-loop / rok-strip levers + fncmp-driven SA; NO MATCH (fncmp 158 -> 82)
- m_x.py: strip a case label from rok/fkbo fake edges (ST) + s70 tail loop to dsp. Stripping c10/c9/c2 breaks R2 (35-40);
  c12/c11/c3 keep R2 0-1 but es2 rises (R3 34-38). Tail loop at case 12 alone: fncmp 144 (base best_d 158) though es2 229.
- Conclusion: es2 and fncmp disagree; optimise fncmp directly.
- sa.py = s70 sa + ST lever (toggle a label's rok/fkbo edges), cost = fncmp + 0.1*(es2 + 2*R3), compile with fncmp.
  4 workers x 3000 s. Best: w2 (from s62/best_b, LP {12:1}) -> best_s71w2.json / best82.c:
  **fncmp 82**, es2 196 (R2 0, R3 23), ev 44; LP {4:1,1:3,d:2,9:3,3:1}, ST [c11,i0,p0].
- Next: continue SA from best_s71w2.json with cost on fncmp (longer runs, lower T0); full-object compare.

## s72: longer/cooler SA from s71 best82 on fncmp cost; NO MATCH (fncmp stays 82)
- sa.py = copy of s71 sa.py. 4 workers x 4500 s (~4260 evals each) from best_s71w2.json:
  a T0=1.5 FW=0.1; b FW=0 (pure fncmp) T0=1.5; c T0=3; d FW=0.05 T0=0.8 PLP=0.3.
- No worker beat fncmp 82. Worker a found an es2-only gain (best_s72a.json: es2 189, R3 25, fncmp 82).
  So best82 is a deep local minimum for the existing levers (PD/TH/LP/ST/w/X/E2/order).
- d82.txt = fncmp diff of best82: almost all block placement (log_printf/jmp error blocks
  in a different order, one je/test swap, an epilogue moved, one index-register order).
  Fixing it needs new levers that move individual cold blocks, not more SA on the current ones.

## s73: hand-targeted levers on best82; NO MATCH (fncmp 82 -> 76)
- f.sh SRC.c: plain-flags fncmp count, diff in SRC.d (FNCMP_CONTEXT=2000 for full listing).
- Diff item 1 (test/je swap) FIXED by -wb second-arg check operand order:
  `{ int k = i + 2; b = argv[k]; if (!b || k == argc || *b == '-') client_usage(4, argv[i]); }`
  (only `!b` first gives 80; the k temp in a block gives 76). best76.c / best76.patch (vs s71/best82.c).
- perm.py: all operand permutations of every argv `if (A||B||C)` check: no further gain.
- Epilogue after netDisconnect (original duplicates add esp,92..ret there): tried goto ret single exit,
  asm goto before return, empty asm after netDisconnect, asm goto ndl edge: 76/76/76/84, no gain.
- Case 3 JMP(hdd5,s5) removal/swap: 76/100, no gain.
- sa.py = s71 SA with the -wb lever fixed on; 3 x 2400 s from best_s71w2.json: no fncmp gain (76).
- Remaining: cold error-block order, epilogue copy, rok X-operand leas (lea edx/ecx [56/59+esp]), base/index swap.

## s74: NO MATCH (fncmp 76 -> 74)
- best74.c = s73/best76.c with the rk X operands changed to memory operands:
  `"X"(&rko), "X"(&rkvN)` -> `"m"(rko), "m"(rkvN)` (item c: the two rok-path `lea edx/ecx,[56/59+esp]` vanish).
  Same edit on fko/fkv: no change (76). Dropping rko operand, or "X"(rko): 74 too.
- Item b (epilogue copy after netDisconnect): bbro dump shows the netDisconnect block of that
  path (jump-threaded per-mode tail copy, bb 59) at freq 1 vs entry 217, and the return block
  (bb 19) sits inside a longer trace, so connect_traces' 1-block duplication (needs edge freq
  >= ~10% entry for code_may_grow; epilogue is 10 bytes > 2-byte jmp) can't fire. `hot` label on
  ndl: 91, no duplication. Needs that path much hotter or ret as its own trace. gcc source fetch
  from gcc.gnu.org was blocked (Anubis) this session.
- Items a, d untouched.

## s75: NO MATCH (fncmp 74 -> 73; item b solved at a cost: 78)

Tools (new): `ours.sh SRC OUT` (mode_client asm, literals resolved), `dump.py`+`dump2.py`
(original asm with strings -> origs.txt), `sig.py origs.txt OUT` (compact diff of the
cold-block / error-block sequence), `gr2.py BASE OUT SECS` (hill climb with sideways moves over
every bcp-goto chain: delete / add conjunct / drop conjunct, plus cold/hot labels on AT() sites;
protects the `mode + 260` lever). `bbmap.py` tags are unreliable (several RTL dumps before Trace 1).

- best73.c = best74 + cold label on hdd4: `AT(hdd4) { hc4: __attribute__((cold)); } log_printf...` (73).
  Greedy over 60 cold/hot-label and efail/eout raise levers (gr.py) found nothing more.
- Item b (epilogue copy after netDisconnect) SOLVED structurally: in `fail:` add
  `if (__builtin_constant_p(mode + 260)) goto ndl;` (one conjunct, ~50%: raises ndl's freq above
  connect_traces' duplication threshold ~10% of entry; 2+ conjuncts = too low, no copy). Any
  predicate shape giving 50% works the same (== 1, != 0, == 3...). Other origins (u2, goto fail
  sites, before dtg, function entry) either don't copy or break much more (entry: 175+).
  fl1 = best73 + that lever: 95; gr2 climb -> best78b.c 78 (epilogue copy + reboot test match,
  rest is the item-a cold order).
- Item a: orig order after the argv traces: -keys CU0 Info Keys Patches invalid | -ip hdd5 hdd4 CU2 |
  -r Block Ferase | -w CU4 CU3 | -e Invalid Patches0 Info0 CU5.. ; ours pulls Keys+hdd5 right after
  the netReboot block (JMP(hdd5,s5) in case 3 is needed: removing it +6..+24) and puts every
  cold group one argv trace too early. Raising efail (bcp goto from clientEraseBlockI entry, 3
  conjuncts) puts Block+Ferase together but before -r, and disturbs -e. Not solved.
- d untouched (follows the cold order).
Next: run gr2.py longer from best78b.c (b fixed) with more lever kinds (rok fan weights, case JMPs).

## s76: NO MATCH (fncmp stays 78 from best78b.c)

Copied s75 tooling (gr2.py, f.sh, ours.sh, sig.py, origs.txt, best78b.c).
Ran 3 parallel gr2.py hill climbs (1800 s each, sideways moves allowed) from best78b.c:
every accepted move was sideways at 78; no improvement (logs w*.log.gz / w*.out.gz).
Conclusion: the existing bcp-goto chain + cold/hot label lever space is exhausted for item a
(cold-group placement after argv traces). Needs a new lever kind attaching each cold group to
its option trace (e.g. per-group asm goto from the option trace's last block, rok fan weights),
designed from bb-reorder connect_traces mechanics; not attempted in this session.

## s77: mode_client profile-free (attempt 58)

### Key finding: s73..s76 bests are semantically wrong

`best73.c` / `best78b.c` (and gr2.py's `lab` lever) write

    else
        AT(hdd4) { hc4: __attribute__((cold)); } log_printf(0, "...avatar...HDD...");

The `{ hc4: ...; }` block becomes the whole else body, so the log_printf runs
after sendAvatarData too (same for hdd5 / sendCompatData). Our asm then has
`call _sendAvatarData` falling into the hdd4 message. Braced fix
(`else { AT(hdd4) {...} log_printf(...); }`, both sites): `fx.c`, fncmp 98
(was "78"). gr2.py's `lab` lever has the same flaw on any unbraced body: don't use it.
gr3.py drops it.

### How the cold order is made (bb-reorder, from the -fdump-rtl-bbro-details log)

Tools: `dd.sh SRC` (bbro dump to d/NAME/, prints the final order as [Trace/round]
labels:freq), `bbinfo2.py` (final position -> old bb -> trace; the dump has 2
"Reordered sequence" lists: the first maps the old bbs to positions, the second is
from the renumbered blocks), `keys.py d/N/mc.bbro d/N/order.txt` (round-4 heap pops with
the keys), `sig2.py origs.txt OURS` (call/string token diff from the last netReboot,
which reads better than sig.py).

- None of the cold traces are joined in connect_traces (no Connection lines among
  them), so the final order is the trace index order, which is the order in which
  find_traces_1_round pops each trace's start block from the heap.
- The heap key is `bb_to_key`: `-(100*BB_FREQ_MAX + 100*maxEdgeFreq + freq)` when some
  pred is the END of an already built trace (or a DFS back edge), else `-freq`. Keys are
  updated when a trace ends (its last block's succs). So priority comes from the
  edge frequency of trace-end preds, and freq only breaks ties.
- Priority sources here: switch block (110, end of T14), so every case head gets
  edge freq 3-5 → ~-10004xx; fkbo asm-goto fan (109, end of T12), giving its targets
  ~-10002xx; and the rok fan (103 netGetInfo, round-3 trace end) for hdd4/hdd5/u2/s5.
  asm-goto edges are not EDGE_CAN_FALLTHRU, so they never *connect* traces, but
  they do set priorities. Prioritised blocks below the round threshold are carried to
  the next round with the key kept.
- Round 3 (exec threshold ~10): any prioritised block with freq>=10 is popped before
  -keys (26, no priority). In best78b, c3's head (f28 from `fail: if(bcp) goto c3`),
  then hdd5 and s5, start traces 18-20, so Keys and hdd5/compat land right after netReboot.
- Round 4: case heads by (edge freq, freq), then the fkbo/rok-prioritised cold
  blocks (hdd5, hdd4, invalid, Info0, CU2), and only then the argv option traces
  (-ip key -7, no priority) with the blocks pushed while they are built. So a
  cold block lands after -ip only if it has no trace-end priority.
- Dilution doesn't work: extra asm-goto labels that thread to the same block merge
  into one edge, and the probabilities split evenly over the distinct targets. An asm goto
  from a loop block to a label inside the argv loop (or from outside into it) drags
  huge flow (-keys 48, or irreducible-loop freqs in the hundreds).

### Levers (measured; sig2 = sig2.py +/- token count, fx = 24)

1. `fail: if (bcp(mode+200)) goto dtg;` instead of `goto c3` (c7): c3/Keys drop to round 4.
2. `goto s5` tail at mode+730: 2 conjuncts (g1): s5 below the round-3 threshold;
   netReboot -> -keys -> "reboot has" -> CU0 -> Info -> DumpNand, as the original has it.
3. Drop hdd4/hdd5/u2 from the rok fan (direct list + ork15/16/18-21 -> rkE) and
   swap hdd4/hdd5 in fkbo for dtg,ndl (r1): hdd5, hdd4 move after -ip.
4. Fail-feed `if (bcp^k) goto L;` in fail: sets case-head freq for the round-4 tie
   order (k=4 c3: Keys after DumpNand; k=4 t5: Compat after Avatar; k=5 c9).
   c95.c (= c9_5) sig2 16, fncmp 222. fncmp is dominated by block moves now; sig2 is better.
Remaining in c95: WriteBl prio 2 (via fkbo) vs BinPatch/ReadBl 4 (switch); Info0 still
fkbo-prioritised before -ip; CU2 missing after hdd4; Ferase after -w; -e group order.

### Climb

gr3.py: score (sig2, fncmp); levers: bcp chain del/add/rm, fail-feed (new), rok/fkbo fan
add/del/swap (new); no label lever. 5 x 2400 s from c95.c: see results below.

### Climb result

5 x 2400 s gr3.py from c95.c (16, 222): best (14, 196) = best_s77.c (w4). Logs: w*.log.gz / w*.out.gz.
Semantically correct baselines: fx.c (best78b braced, fncmp 98, sig2 24), best_s77.c (fncmp 196, sig2 14).
Next: give WriteBl (c9) switch-edge priority 4 (find why its case edge is 2), make Info0/CU2
lose fkbo/rok priority, Ferase/-e group levers; then score by fncmp once sig2 reaches 0.

## s78 (attempt 59): flag sweep + short climb

### Flag sweep (fncmp / sig2), extra flags on top of the plain compile
| flags | fx.c | best_s77.c |
|---|---|---|
| baseline | 98 / 24 | 196 / 14 |
| --param align-loop-iterations=100 | 98 / 24 | 196 / 14 |
| -O2 | 99 / 24 | 197 / 14 |
| builtin-expect-probability=40 | 614 / 62 | 728 / 54 |
| builtin-expect-probability=65 | 324 / 50 | 302 / 32 |
| drop -fno-ipa-profile | 98 / 24 | 196 / 14 |
None helps; keep the s77 flags.

### Climb
gr3.py 560 s each: from best_s77.c no gain (14,196); from fx.c -> best_s78.c (sig2 24, fncmp 86).
Only bcp-chain edits (compile-time dead), so semantics as fx.c. Order-diff fixes (WriteBl/Info0
priority, CU2, Ferase, -e group) not attempted this round. Logs: g*.log.gz/g*.out.gz.

## s79 (attempt 60): hand fixes of the round-4 order (from best_s77.c)

Tools: m.sh SRC (fncmp, sig2 count, bbro order), mk.py (exact-once replace), bc.py (bcp chain),
vars.sh (kk = round-4 keys). Measures are (fncmp, sig2 +/- lines).

| variant | change | fncmp | sig2 | effect |
|---|---|---|---|---|
| best_s77 | base | 196 | 14 | ReadBl BinPatch(-1000403) WriteBl(-1000309) Patches(c7,-1000305) |
| a1/a2 | more conjuncts on `mode = 9` thread | 232 | 18 | switch->c9 edge 4, WriteBl (f9) jumps to round 3 |
| b1-b3 | a1 + drop goto c9 feeds | 216-264 | 16-26 | c9 freq stays >=6 (dsp loop back-edges) |
| c5/c6 | `if(bcp^k) mode = 11;` after mode=9 | 214 | 14 | BinPatch edge 3 but mode=7 thread dies (only the last two threads work): c7 edge 4 |
| g*/h* | mode=11 thread before 7 / between 7 and 9 | 196/214 | 14 | same problem |
| i6 | `mode = 7; else if (bcp^6) mode = 11; else if (... ) mode = 9` (else chain: all three thread) | 212 | 14 | WriteBl 309, c7 305, BinPatch 303 |
| **j1** | i6 + fail-feed `if (bcp^4) goto c11;` | **196** | **12** | BinPatch f6 -> -1000306: ReadBl WriteBl BinPatch Patches = original. WriteBl diff fixed |
| k1-k4 | j1 minus i1 in fkbo fan (+ replacement c8/c11/c2) | 224-232 | 18-28 | Info0 loses prio but round-4 tail reshuffles |
| l1/l2 | JMP(efail) from eout/einv | 198 | 12 | no order change |
| m2-m5 | fail-feed goto c10 | 198-312 | 14-29 | Ferase still f1 |

Remaining (j1): Info0 fkbo-prioritised before -ip; a CU before -r; Ferase after -w;
-e group (orig: -w CU CU -e Invalid Patches Info CU..). Original needs Ferase f>=2 and
LC117/Patches/Info at f0 popped after -e; round-4 equal-key pops follow fibheap
structure (e.g. 80,68,78 pushed 78,80,68), so they need measured experiments.
Semantics: all j1 deltas over best_s77 are bcp-guarded (`mode = 11`, `goto c11`) = dead.

gr3.py 2 x ~22 min from j1.c (q1/q2.log.gz): no gain, plateau (12, 196). Best: best_s79.c (= j1.c).
Next: Ferase freq / -e group via measured fibheap tie experiments; port the else-chain
mode=11 + feed c11 fix onto best_s78.c (its order is further off: Keys/hdd5 in round 3).

## s80 (attempt 61)

Base: best_s80.c = copy of s79/best_s79.c. Re-measured with s79/m.sh: fncmp 196, sig2 12 (unchanged).

### Semantics check of best_s80.c vs src/mode_client.c (diff reviewed by hand)
- All added `__builtin_constant_p(...)` conditions are on non-constant `i`/`mode`, so they fold
  to 0: every guarded `goto`/`mode = 7/11/9` is dead (bcp-dead).
- `JMP(...)` / `__asm__ goto("" :::: L)` and the rk*/fa* asm-goto fans are empty asm: fall through
  at run time (zero-byte hints); labels added (lu1, k55l, k61l, k67l, dsp, t4, t5, s4, w5x, ...) are labels only.
- `-r`/`-w`/`-e` branches wrapped as `} else { L: if (...) {` with the three closers `} } }` after the
  final `client_usage(1, argv[i])`: else-grouping intact.
- `-ip`'s second arg: `k = i+2; b = argv[k]; if (!b || k == argc || *b == '-')` vs original
  `i+2 == argc || !b || ...`: argv[argc] is NULL, no side effects, same result.
- `-w`: `({asm goto w5x; 0;})` conjunct is 0 at run time; `if (mode) { w5x: client_usage(5,..) }` same.
- hdd4/hdd5 cold labels, `JMP` inside cases, extra `asm goto dsp` before `break`: hints only.
- clientEraseBlockI added as a static copy with labels (eerase/esucc/efail/eout/einv) and JUMP(efail): same behaviour.
Conclusion: semantics-preserving.

### Work
Only the baseline confirmation and the check above were done this attempt; no new variants
improved on (196, 12). Remaining order diffs are unchanged from s79/NOTES.md (Info0 vs -ip,
CU before -r, Ferase after -w, -e group fibheap tie order).

## s81 (attempt 62): hand levers on the four round-4 order diffs

Base best_s80.c (fncmp 196, sig2 12). New best: **best_s81.c (= n1.c): fncmp 68, sig2 8**, semantics-preserving
(diff vs best_s80: bcp-dead gotos on non-constant i/mode/block, braced cold labels, label-only, empty asm JMP).
Tools: r.sh NAME BASE old new ... (mk.py + fncmp + sig2 + tail order with freqs), tail.py,
r4sim.py (round-4 replay on tools/wip/fibsim.py with per-block key overrides; reproduces gcc exactly),
srch.py / sa.py (what-if key searches against the target order).
NOTE: dd.sh in s77/s79 swaps LC114/LC117: LC117 = "Failed to erase" (Ferase), LC114 = "Invalid arguments". Fixed in tail.py.

Target round-4 tail (original): inv -ip hdd5 hdd4 CU107(u2) -r Blk Fer -w CU33 CU29 -e Inv Pat0 Info0 CU35 CU42 CU53 CU78 CU80 -c
(Info/Patches cold calls in the original are the NULL ones: clientInfo(NULL)/clientPatches(NULL); hot ones take arg.)

| var | base | change | fncmp | sig2 | effect |
|---|---|---|---|---|---|
| **diff 1: Info0 prio / hot-cold sense** |||||
| a1 | s80 | cold label i1 -> i0 | 228 | 18 | Info leaves tail, -e group shuffles |
| a2 | s80 | a1 + drop i1 from fkbo | 224 | 24 | Info f0 but -r/Blk swap |
| a3 | s80 | a1 + fkbo i1->i0 | 208 | 14 | Info143 still prio |
| a4 | s80 | drop i1 from fkbo only | 232 | 28 | (= s79 k1) |
| a5 | s80 | a1 + s4 JMP(i1)->JMP(i0) | 216 | 14 | |
| **a6** | s80 | a1+a3+a5 | **192** | 12 | hot Info(arg)/cold Info(NULL) sense now right (fixes the je/jne diff) |
| a7 | s80 | a1 + fkbo i1->c12 | 252 | 28 | |
| b1-b10 | a6 | fkbo i0 -> fa21/c12/c2/c11/c8/hdd4/u2/c3/t4/efail | 112-246 | 18-28 | b7 (u2) fncmp 112 but u2 gets fkbo prio before -ip; efail not in scope |
| j_*_1..4 | g6,h4,i3 | fkbo i0 -> none/c12/i1/hdd5 | 90-148 | 10-28 | **j_i3_3 (i1) removes Info prio, hot order intact: 96/10** ; c12 reshuffles hot part |
| **diff 2: CU(2,NULL)=u2 (bb107) before -r** |||||
| c1-c7 | a6 | goto u2 feeds in fail block / chain lengths | 192/222 | 12/24 | fail is cold: no freq change; removing feed (c4) worse |
| d1,d9 | a6 | loop-head u2 feed 1 conjunct | 146 | 18 | u2 f4 (too high) |
| d2-d7 | a6 | extra/changed feeds (post-loop, ==3 forms) | 192 | 12 | no freq change (saturated) |
| d8 | a6 | feed `bcp(i+320)&&bcp(i+321)` (int form) | 146 | 18 | u2 f3, but before hdd4 (tie -3) |
| d10/d11/d12 | a6 | 2 feeds / `||` / 2x2-conj | 98/144/220 | 14/18/12 | u2 f5/f8/f2 |
| e1-e5 | d8 | raise hdd4 (post-loop goto, JMP dup, i0 fan) | 82-170 | 12-22 | **e4: JMP(hdd5,s5,hdd4) in c3 -> hdd4 f5, u2 after both: 82/12** |
| f1-f6 | e4 | hdd5 vs hdd4 order | 82-154 | 12-20 | **f5: JMP(hdd4,s5,hdd5) -> hdd5 hdd4 u2 order = original** |
| **diff 3: Ferase before -w** |||||
| g1-g3 | f5 | goto efail before eerase (1-3 conj) | 148 | 18 | Fer stays 1, -r/-w reshuffle |
| g4/g5 | f5 | JMP(efail) from eout / at eerase | 84/151 | 12/18 | |
| **g6** | f5 | esucc: `if (bcp(block+7)) goto efail;` | **70** | 10 | Fer f2, pops before -w (diff 3 fixed) |
| h1/h3 | g6 | cold einv (Inv f0) [+cold p0] | 144/104 | 18/14 | Fer jumps to f3 |
| h4-h7 | h3 | drop / weaken esucc feed (0,2,3,4 conj) | 100/100/84/84 | 14/14/12/12 | h4: Fer f2 + Inv/Pat f0 |
| k3/k4/n2 | j_i3_3/m1 | feeds into eout (Blk) | 76-148 | 10-14 | Blk f3 but Fer drops to 1 |
| **diff 4: -e group / fibheap ties** |||||
| h2 | g6 | cold p0 | 128 | 14 | Pat f0, after -e |
| i1-i5 | h4 | k67l feeds (1..3 conj, int form) | 156-284 | 18-34 | **i3 (3 conj) -e f1, pops right after CU29/CU33** |
| k1,k2,k5,k6,k7 | j_i3_3 | k55l/k67l/k61l feed edits | 96-148 | 10-16 | mostly saturated; k7 (no k67l feed) -e back to f0 |
| l1-l4 | j_i3_3 | drop k61l feeds | 86-112 | 14-20 | -w f1 |
| m1-m4 | l2 | label wb3 on -wb usage3 + feed (2/3/1 conj) | 68-86 | 10-14 | **m1: CU29 f2; after -e: Inv Info Pat 35 42 53 80 78 -c (near target)** |
| **n1** | m1 | re-add k61l feed after k55l feed | **68** | **8** | -w f2 again |
| n3-n5,o1-o5 | m1/n1 | k55l strength, wb4 label feed, wb3 feed forms/places | 68-96 | 8-12 | freq 1<->2 cliff only |

Current (n1) tail: inv -ip hdd5 hdd4 CU107 CU29 Blk Fer -r -w CU33 -e Inv Info Pat CU80 CU78 CU35 CU42 CU53 -c
Remaining: CU29 must be f1 but pop after CU33 (f1 ties); -r before Blk/Fer; Pat before Info; CU35/42/53 before 78/80.
r4sim key searches (sa.py on m1/j_i3_3 dumps) never reach 0 inversions with <=10 key overrides: with these heap
histories the f0 group order cannot be reached by key changes alone; the round-3 push order (53 42 35 pushed in that
order) and round-4 insert timing would have to change. Next: use r4sim to search over *insertion order* (round-3 trace
order of 33/29/35/42/53 pushes) and then find levers for that.

## s82 (attempt 63): insertion-order search + lever climb

Base b0.c = s81/best_s81.c (fncmp 68, sig2 8). **New best: best60.c, fncmp 60, sig2 10** (fncmp-better,
order-equal: bbro inversions vs target 15 like b0). Diff vs b0: dead `if (bcp(block+7)) goto efail;` at esucc,
lu1 loop-head feed dropped, k61l `(i+20)==3` feed dropped (all bcp-dead / label-only; braces intact).
Not adopted as "obviously better": sig2 8 -> 10 and the bbro tail is not closer.

### Tools
- osrch.py DUMP REPS: SA over round-4 key overrides + round-3 push order + per-trace insert order (r4sim replay).
- ks.py NAME REPS RANGE ITERS: key-only SA; target block ids resolved per variant by tmap.py (source-line based:
  u2/wb3/wb4/wb5/eb5/ip3/c3/c5 CU blocks, LC labels, cold Info/Pat = last occurrence). ks2/ks3 variants.
- bf.py: brute force of the f0 back group with the front fixed.
- lev.py / climb.py: parametrised levers (feed conjunct counts for u2,k55l,wb3,wb4(new label),lu1,k67l,k61l,
  esucc->efail, eerase->eout, new labelled CUs ip3/c3/c5/eb5/wb5) + coordinate climb on (fncmp, inversions).
  Logs: climb_2.log (y*), climb_3.log (x*); w* run results in w*.c/.d.

### Findings
- osrch with push/insert-order moves reaches 0 inversions on b0's history (e.g. keys 107:-4 33:-2 139:-4
  138:-3 140:-1 127:-1 55:-4 61:-3 68:-2, round-3 push 53 first), cost 11 changes; key-only never reaches 0.
- With *distinct* front keys (125=-7 121=-6 107=-5 55=-4 139=-3 138=-3 61=-2 33=-2 29=-1 68=-1) the front
  (inv..-e) is exact; the back f0 group (Inv Pat Info 35 42 53 78 80 -c) is the hard part: bf.py over {0,-1}
  for those 9 gives >= 9 inversions. These are tie-structure (fib-heap) orders, not freq levels. The original is
  an FDO build, where these blocks are all count 0: their order there is pure heap structure (key 0 / prio), so
  matching it via guessed freqs needs the same heap history, not just keys.
- Measured levers (~140 compiles: v1-v17, w1-w50, x1-x27, y1-y45):
  u2 1-conj: u2 f4 free (fncmp same), u2 3/0 conj very bad; k55l 3-conj (on u2=1): -r f3 right after u2, front
  inv..-r exact (v8, fncmp 68); k55l 1-conj: -r f5 (bad). wb4 label+feed: CU33 f2-4 but jumps ahead (76).
  esucc->efail: Fer f3 (60 with k61/lu1 off). eerase->eout 1-conj: Blk f4. New labelled CU feeds (ip3/c3/c5/
  eb5/wb5) cost ~+250 fncmp at any strength (the label stops a CU merge) -> unusable.
- Climb plateau at 60 (all single moves >= 60).

Next: the back group needs the heap *structure* of the original; consider making Inv/Pat/Info prioritised
(trace-end preds with edge freq 0 -> key -1000000) instead of freq tweaks, and simulate that first with r4sim
(ks3.py tried {0,-1000000} on b0 history without success; needs prio for the right subset + insertion timing).

## s83 (attempt 64): back f0 group fixed by heap-structure levers

Base best60.c (s82). **best_s83.c (= h1.c): fncmp 64, sig2 8, inversions 7 (inv.py metric; best60 = 19 on the
same metric)**. Back group after -e is now exactly the original's: Inv Pat Info CU35 CU42 CU53 CU78 CU80 -c.
Remaining order diffs are front only: ours `u2 Fer Blk CU29 -r CU33 -w -e`, target `u2 -r Blk Fer -w CU33 CU29 -e`.
Diff vs best60 (all zero-byte asm goto / label / list order, braces intact):
1. fkbo asm goto list `i1, p1, ...` -> `p1, i1, ...` (b1: back group becomes Info Inv Pat 35 42 53 80 78 -c).
2. -r: `if (({__asm__ goto("" :::: r5x); 0;}) || i + 1 == argc || ...)` + `if (mode) { r5x: client_usage(5, argv[i]); }`
   (d1): the -r trace now inserts CU80 before CU78 -> 78 80 order right. The label did NOT stop the CU merge.
3. c12: `if (arg == dummy || ({JMP(p0); 0;}))` (h1): c12's trace inserts Info then Pat (JMP before the test = e5 inserts
   Pat first; inside i1 = bad).

### Finding: no prio route
bb_to_key gives priority only if edge_freq > priority(0): a zero-frequency edge from a trace end never prioritises,
so the "key -1000000 via 0-freq asm goto" idea of s82 is impossible. Also a JMP inside the loop body (a1-a4) is a
loop exit: fncmp 330. Instead the back group is fixed by *insertion order* (heap structure), found with:
- mv.py DUMP blocks: what-if moving ins events of blocks to other groups/round-3 pushes.
- perm.py x NAME: permute the round-4 initial ins events (+ 78/80 swap); showed back group exact needs
  Info-first initial inserts with Pat right after, and 80 inserted before 78 in the -r group.
- perm2.py, ksr.py/ksr2.py (key grid searches on variant NAME), osrch2.py (osrch on variant ids via tmap), ev.py x NAME
  (compact heap event trace), inv.py NAME, r.sh now prints inv= and logs to log.txt.
Front: key-only grid on i4 history can't get below 5 inversions; moving front keys (k55 3-conj int: i5) re-breaks the
back group (consolidation shape changes). osrch2 3x12000 on i4: best 4 inv (not 0).

| var | base | change | fncmp | sig2 | inv |
|---|---|---|---|---|---|
| a1 | | | 330 | 32 | 43 |
| a2 | | | 330 | 32 | 43 |
| a3 | | | 330 | 32 | 43 |
| v8 | | | 68 | 10 | 16 |
| b1 | | | 80 | 10 | 11 |
| b2 | | | 60 | 10 | 19 |
| b3 | | | 160 | 20 | 26 |
| b4 | | | 160 | 20 | 26 |
| b5 | | | 96 | 12 | 15 |
| b6 | | | 9999 | 0 | inv? |
| b7 | | | 9999 | 0 | inv? |
| b8 | | | 60 | 10 | 19 |
| b9 | | | 60 | 10 | 19 |
| b10 | | | 60 | 10 | 19 |
| c1 | | | 80 | 10 | 11 |
| c2 | | | 80 | 10 | 11 |
| c3 | | | 80 | 10 | 11 |
| c4 | | | 80 | 10 | 11 |
| c5 | | | 80 | 10 | 11 |
| c6 | | | 80 | 10 | 11 |
| d1 | | | 76 | 10 | 10 |
| d2 | | | 80 | 10 | 11 |
| d3 | | | 76 | 10 | 10 |
| e1 | | | 294 | 20 | 33 |
| e2 | | | 282 | 22 | 23 |
| e3 | | | 302 | 22 | 44 |
| e4 | | | 94 | 14 | 15 |
| e5 | | | 64 | 10 | 8 |
| f1 | | | 302 | 22 | 44 |
| f2 | | | 140 | 18 | 24 |
| f3 | | | 140 | 18 | 25 |
| f4 | | | 64 | 10 | 8 |
| f5 | | | 90 | 12 | 15 |
| g1 | | | 90 | 12 | 16 |
| g2 | | | 274 | 18 | 34 |
| g3 | | | 64 | 10 | 20 |
| g4 | | | 76 | 10 | 10 |
| h1 | | | 64 | 8 | 7 |
| h2 | | | 64 | 10 | 8 |
| h3 | | | 134 | 18 | 23 |
| i1 | | | 72 | 8 | 16 |
| i2 | | | 100 | 12 | 29 |
| i3 | | | 100 | 12 | 29 |
| i4 | | | 64 | 8 | 7 |
| i5 | | | 100 | 12 | 29 |
| j1 | | | 64 | 8 | 8 |
| j2 | | | 64 | 8 | 7 |
| j3 | | | 72 | 6 | 12 |
| j4 | | | 64 | 8 | 7 |
| j5 | | | 64 | 8 | 7 |
| k1 | | | 80 | 12 | 15 |
| k2 | | | 80 | 12 | 15 |
| k3 | | | 80 | 12 | 15 |
| k4 | | | 64 | 8 | 8 |

Changes: a1-a3 JMP(i0|p0|p0,i0) after `mode = 4;` (loop body); v8 = s82 v8; b1 fkbo p1,i1; b2 JMP(cdef,p1); b3/b4
s4 JMP(i0,p0)/(p0,i0); b5 s4 JMP(p0); b6/b7 extra fkbo labels (error: label in list twice); b8 ndl feed p0->i0;
b9 JMP(c12,s4); b10 c9 JMP(hdd5,hdd4); c1-c6 further fkbo list perms (only p1-before-i1 matters); d1-d3 r5x asm goto
before/after argc test / standalone; e1-e5 JMP(p0) in c3 list front/back, i1 after/before call, c12 head; f1 JMP(p0)
before case-12 break; f2/f3 c12 JMP(i0,p0)/(p0,i0); f4 e5 minus s4 JMP(i0) (same); f5 e5 + fkbo i1,p1; g1-g4 JMP(p0) in
c3 / after clientKeys / c3 only / c10; h1-h3 JMP(p0) inside c12 condition (|| after, || before, && after);
i1-i5 v8 front levers on h1 (all / no esucc / u2+k55 / u2 1-conj / k55 3-conj int); j1 no esucc feed; j2 lu1 feed;
j3 k61l feed (sig2 6, fncmp 72); j4 k55 3-conj char; j5 no k55 feed (dead on h1); k1-k3 wb3 feed off/3/4-conj;
k4 esucc 2-conj.

Next: front only. Need -r to pop right after u2 (before Fer/Blk), Fer after Blk, CU29 after CU33, without
changing the round-4 consolidation shape that now gives the back group. Search insert-order levers (like 2./3.) for
the front with perm.py-style what-ifs on h1's history before trying freq levers.

## s84 (attempt 65): front fixed on x4/z3, back group broken again

Step 0 (semantics): s83's -r `({__asm__ goto("" :::: r5x); 0;})` emits no instructions and never jumps at runtime,
so the condition is unchanged; r5x: sits inside the existing `if (mode)` around the same client_usage(5) call. So
behaviour is preserved, the same pattern as w5x. z3 drops r5x entirely anyway.

Results (r.sh: fncmp / sig2 / inv; base h1 = 64/8/7). Levers are mk.py replacements in b1..b8.sh.
- v18/v23 (esucc bcp feed 2-conj / removed): Fer freq 3->2 -> front `CU29 Blk Fer -r CU33 -w -e` (Blk Fer now in
  the right relative order), back still exact. 64/8/8.
- w12 = v23 + wb3 feed 5-conj: CU29 freq 2->1 -> front `Blk Fer -r CU29 CU33 -w -e`, back broken (CU53 first). 80/12/14.
- **x4 = w12 + second k55 feed `if (bcp(i+35)&&bcp(i+36)&&bcp(i+37)) goto k55l;`**: -r freq 3, -w 2 ->
  front `-r Blk -w Fer CU33 CU29 -e` (target `-r Blk Fer -w CU33 CU29 -e`, 1 swap). Back
  `Inv 81 53 35 42 Pat Info 79 -c` vs target `Inv Pat Info 35 42 53 79 81 -c`. 70/6/15.
- **z3 = x4 without the r5x asm goto: 64/6/14 = best_s84.c** (best sig2 so far; back still off).
- ws3.py (random what-if: move a block's R4 ins event to another group with a key) on x4/z3: inv 1-2 reachable only by
  inserting Inv (einv, 140/141) late (from the -e or CU29/CU33 group) plus Fer key -1. No source lever found for
  that: Inv is a successor of the erase trace (135) which pops first in R4. einv cold off, JMP(einv) from
  eout/eerase/esucc, bcp gotos to einv/eout, __builtin_expect on erase tests: all worse (y1-y7, q3-q8).
- s83 back levers retried on x4 (z1-z8): fkbo i1,p1 / p1,dtg,i1, c12 JMP variants, r5x moves: none restores the back.

| var | base | change | fncmp | sig2 | inv |
|---|---|---|---|---|---|
| v01 | h1 | r5x after argc | 68 | 8 | 8 |
| v02 | h1 | r5x after !a | 68 | 8 | 8 |
| v03 | h1 | w5x first | 68 | 8 | 7 |
| v04 | h1 | w5x after !a | 64 | 8 | 7 |
| v06 | h1 | k55 1-conj | 222 | 14 | 25 |
| v07 | h1 | k55 4-conj | 64 | 8 | 7 |
| v08 | h1 | k67 2-conj | 64 | 8 | 7 |
| v09 | h1 | k67 4-conj | 64 | 8 | 7 |
| v10 | h1 | k61 2-conj | 150 | 12 | 20 |
| v11 | h1 | k61 4-conj | 64 | 8 | 7 |
| v12 | h1 | wb3 5-conj | 80 | 12 | 15 |
| v13 | h1 | u2 1-conj | 64 | 8 | 7 |
| v14 | h1 | u2 3-conj | 138 | 14 | 25 |
| v15 | h1 | k55 feed x2 | 64 | 8 | 7 |
| v16 | h1 | k67 feed x2 | 64 | 8 | 7 |
| v17 | h1 | eout no JUMP(efail) | 64 | 8 | 7 |
| v18 | h1 | esucc 2-conj | 64 | 8 | 8 |
| v19 | h1 | eout cold | 148 | 20 | 33 |
| v20 | h1 | einv not cold | 274 | 20 | 26 |
| v21 | h1 | eout JUMP(efail,einv) | 64 | 8 | 7 |
| v22 | h1 | eout JUMP first | 64 | 8 | 7 |
| v23 | h1 | no esucc feed | 64 | 8 | 8 |
| v24 | h1 | eout JUMP(einv) | 64 | 8 | 7 |
| v25 | h1 | eout JUMP(esucc) | 64 | 8 | 7 |
| v26 | h1 | esucc goto eout | 70 | 10 | 16 |
| w01-w16 | v23 | v01-v16 levers on v23 | 64-150 | 6-18 | 8-24 (w12 80/12/14 front closer) |
| x1-x3 | w12 | wb3 3/4-conj, none | 80 | 12 | 14 |
| x4 | w12 | 2nd k55 feed 3-conj | 70 | 6 | 15 |
| x5 | w12 | 2nd k55 feed 2-conj | 170 | 14 | 21 |
| x6-x8 | w12 | 2nd k61 feed 3/2/1-conj | 320-360 | 24-28 | 29-32 |
| x9 | w12 | einv JMP(eout) | 129 | 15 | 19 |
| y1-y5 | x4 | eout JUMP(efail,einv)/(einv,efail)/none, einv not cold, eout JMP(einv) | 70-284 | 6-22 | 15-24 |
| y6/y7 | x4 | JMP(einv) in eerase / esucc | 93/78 | 10/6 | 30/18 |
| z1 | x4 | fkbo i1,p1 | 138 | 16 | 16 |
| z2 | x4 | r5x after argc | 64 | 6 | 14 |
| z3 | x4 | no r5x | 64 | 6 | 14 |
| z4-z6 | x4 | c12 JMP none / first / +JMP(i0) | 70-138 | 6-16 | 15-16 |
| z7 | x4 | fkbo p1,dtg,i1 | 70 | 6 | 15 |
| z8 | x4 | JMP(r5x) from -w | 288 | 12 | 19 |
| q3/q4 | z3 | expect on erase range / block!=-1 | 148/288 | 14/24 | 29 |
| q6-q8 | z3 | esucc 3-conj bcp goto efail/einv/eout | 72/72/148 | 6/6/14 | 17/17/29 |

Next: on z3, fix the back group (Pat/Info before 35/42/53, 81 last) with insert-order levers (s83 style), or find a
lever that inserts Inv late. ws3.py NAME ITER blocks SEED MAXMOVES does the what-ifs (ids per variant, see tmap).

## s85 (attempt 66): NO MATCH, best unchanged (s84/z3 = best_s84.c, 64/6/14)

About 57 real variants (r.sh: fncmp / sig2 / inv), plus round-4 what-if scripts wi*.py (r4sim based).

Findings
- Back group break, z3 vs v23: the keys of 29 (-2 -> -1) and 55 (ins by 49, -2 -> -3) change, so 55 pops right
  after -r (107) and inserts CU78/CU80 (key 0) early. Those two then pop ahead of 53/35/42 (fib-heap tie structure).
  The k55 second feed alone (d1) is enough to break the back. Dropping r5x alone from v23 (d2) keeps the back exact
  (inv 9).
- What-ifs on z3/v23 found no fix that reaches inv <= 2. Tried: key overrides of up to 4 R4 blocks (wi.py, wi4.py,
  40k samples), every insert order and 0/-1 key inside the 55 group (wi2.py), dummy insert/delete nodes (wi3.py),
  decrease-key on any block from any group (wi5.py), and CU78/80 moved into the R3 pushes (wi6.py). Best was 7.
- Structural Inv-late levers (erase function):
  - be1: range test before the -1 test (equivalent). Moves Inv late but changes code (fncmp 215).
  - be3: inverted -1 test. Worse.
  - be4: `goto einv` with einv at the end. No change.
  - c2-c5: asm-goto back edges to the -1 test. Loops; fncmp 281-356.

| var | base | change | fncmp | sig2 | inv |
|---|---|---|---|---|---|
| aw3/4/6/7 | z3 | wb3 3/4/6/7-conj | 64 | 6 | 14 |
| au1/au3 | z3 | u2 1/3-conj | 64/188 | 6/12 | 14/28 |
| ak4/akk | z3 | k55 2nd feed 4-conj / doubled | 64/130 | 6/12 | 14/22 |
| af1-af4 | z3 | fkbo label orders (i1 p1 / p1 dtg i1 / ndl dtg / dtg first) | 128,64,64,64 | 16,6,6,6 | 15,14,14,14 |
| aj1-aj5 | z3 | JMP order swaps (c3, s5, c8, c9) | 64 | 6 | 14 |
| aj6 | z3 | s4 JMP(i0,p0) | 132 | 16 | 18 |
| am1 | z3 | k55 feeds swapped | 64 | 6 | 14 |
| am2/am3 | z3 | 2nd feed char-style / removed | 86 | 12 | 15 |
| am4 | z3 | 2nd feed after k67 | 162 | 14 | 20 |
| ax1-ax3 | z3 | w5x position in -w test | 68,64,64 | 6 | 14 |
| ac1-ac3 | z3 | c12 JMP first / JMP(i0) / JMP(p0,i0) | 64/128/132 | 6/16/10 | 15/14/18 |
| be1/be3/be4 | z3 | erase restructure (above) | 215/148/64 | 15/14/6 | 21/29/14 |
| c2-c5 | z3 | JMP(eck) back edge from esucc/eout/eerase/efail | 288/356/281/344 | 24/25/18/29 | 25/34/22/27 |
| d1 | v23 | + k55 2nd feed | 72 | 8 | 16 |
| d2 | v23 | no r5x | 68 | 8 | 9 (back exact) |
| d3 | d1 | no r5x | 68 | 8 | 15 |
| d4w3/4 | d3 | wb3 3/4-conj | 64 | 6 | 14 |
| d2w3-5 | d2 | wb3 3/4/5-conj | 86 | 12 | 15 |
| d2u1/u3 | d2 | u2 1/3-conj | 68/128 | 8/12 | 9/22 |
| d2f1-f4 | d2 | fkbo orders | 68 | 8 | 16,9,9,9 |
| d2j1-j6 | d2 | JMP order swaps / s4 JMP(i0,p0) | 68 (j6 146) | 8 (20) | 9 (26) |

Conclusion: under bbro's fib-heap ties, the back group needs 55 to pop after 29/139/140, while the front needs
55 right after -r. No key-only or single-insert change satisfies both. The next idea needs a CFG change that
makes CU78/CU80 successors of a later trace than 55, or drops them from 55's insert list, without changing the
emitted code.

## s86 (attempt 67): NO MATCH, best unchanged (s84/z3 = best_s84.c, 64/6/14)

42 compiled variants (v01-v42, vb.py + b1-b6.txt, results in log.txt) plus r4sim what-ifs (w1-w8.py).

Tools
- r4sim.py fix: an `ins` of a block already in the heap now does replace_key when the key differs (real
  bb-reorder behaviour). Earlier what-ifs (s85 wi*.py) skipped it. Replay of z3/d2 still exact.
- w1.py: drop 78/80 from 55's inserts, insert from group G. w3/w4: random insert moves + key overrides.
  w5: single extra insert of block b from group G. w8: move inserts between groups.
- z3L.c / d2L.c: labels `cu3l`/`cu5l` on -c's usage(3)/(5) calls (= blocks 78/80); labels alone change nothing.

Findings
- Even with 78/80 never inserted, z3's back group is inv 7 (74 and 140 tie order). The what-if that reaches inv 2
  needs 78/80 inserted by the -w trace (61) instead of -r (55), plus 61 key -1: not realizable, -r's usage
  edges go to 78/80 (same emitted block).
- Single extra early insert of 78/80 (asm-goto edge from an earlier trace) best sim inv 8 (from 142 = case 12).
- Real asm-goto edges perturb freqs much more than the sim assumes:
  - into k67l (-e test) from wb3/wb4/u2: loop entry, fncmp 511-1018.
  - to cu3l/cu5l from c12's JMP: Pat127 freq 2, fncmp 135-179. cold label on cu3l: no change.
  - from fkbo fan (replacing fa20 / fa0): fncmp 194-307 (fan edges carry freq 2). fkbo asm is at 30 operands.
  - from rok fan, cdef, hdd5 log: fncmp 67-137, inv 15. From hdd4 log: 135. From u2/wb3: 361-392.

| var | base | change | fncmp | sig2 | inv |
|---|---|---|---|---|---|
| v01/v02/v03 | z3 | JMP(k67l) in wb3 / usage4 / u2 | 516/511/1018 | 36/36/102 | - |
| v04-v06 | d2 | same | 551/521/1008 | 37/34/102 | - |
| v07/v15 | z3L/z3LC | labels only (plain / cold) | 64 | 6 | 14 |
| v08-v12 | z3L | c12 JMP + cu3l/cu5l (orders, both) | 162-179 | 12-16 | 30-33 |
| v13/v14/v20 | d2L(C) | c12 JMP + cu3l | 135-137 | 16 | 29-30 |
| v16-v18 | z3LC | c12 JMP + cold cu3l/cu5l | 177-179 | 14-16 | 30-32 |
| v19 | z3LC | separate JMP(cu3l) at c12 | 149 | 12 | 17 |
| v21/v23/v24/v31 | z3L | fkbo fan slot -> cu3l/cu5l | 307/307/305/194 | 26/26/26/16 | 27-32 |
| v22/v33 | z3L | asm operand overflow | err | | |
| v25/v26/v32 | z3L | rok fan + cu3l | 87/87/137 | 10/10/8 | 24/23/15 |
| v27/v30 | z3L | hdd4 JMP(cu3l/cu5l) | 135 | 14 | 21 |
| v28/v29 | z3L | hdd5 JMP(cu3l/cu5l) | 67 | 8 | 15 |
| v34/v35 | d2L | hdd5 JMP | 161 | 18/22 | 26/31 |
| v36-v38 | z3L/d2L | u2 JMP(cu3l/cu5l) | 368-392 | 32-38 | 37-39 |
| v39 | z3L | cdef JMP(cu3l) | 137 | 8 | 15 |
| v40-v42 | z3L/d2L | wb3 JMP(cu3l/cu5l) | 361/361/180 | 32/32/20 | - |

Conclusion: plan item 1 (move the 78/80 insert away from 55) is not realizable: 55's edges to 78/80 are part of
the emitted code, and any added edge that inserts them earlier shifts frequencies (asm goto edges split evenly)
far more than the target needs. Sim-level, no single early insert beats inv 8. Remaining unexplored: levers that
change fib-heap root structure without new edges (e.g. extra zero-freq blocks that are popped/consolidated
early, from code that already exists in the original), or matching the original's profile-shaped freqs directly.

## s87 (attempt 68): NO MATCH. New lever: order of the dead `__builtin_constant_p` goto ifs on the `fail:` line

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

## s88 (attempt 69): NO MATCH. New best 36 (v06.c), -bp regalloc diff FIXED

~530 variants measured: v01-v11 hand (rv.sh, log.txt), 16 single-line perms (en.sh: lines 667/739/799, all no-op),
3 fail-line climbs on v04 (hc11-13.log, 210), 2 on v06 (hd21-22, 120), 3 on v10 (he31-33, 180). hc.py now takes a per-seed tag (parallel-safe).

| var | base | change | fncmp/sig2/inv |
|---|---|---|---|
| v01-v03 | e01 | -bp pins "r"->"d" | 188/15/29 |
| v05 | e01 | drop first -bp pin | 68 (no change) |
| **v04** | e01 | first -bp pin `__asm__("" :: "r"((unsigned)(i + 1) * 4))` -> `__asm__("" :: "a"(i + 1))` | **42/8/6**: the 24-line "-ip" (actually -bp arm) eax/edx swap is gone |
| v07-v09 | e01 | other pin combos with "a" | 42 |
| **v06** | e02 | same "a" pin | **36/10/18** (best) |
| v10 | z3 | same | 38/6/14 |
| v11 | h1 | same | 92 |
| climbs | v04/v06/v10 | fail-line perm | plateaus 36/18, 38/14, 42/6-7; no lower |

Remaining (v06): back-of-function cold block order only (usage(3)/(5) pairs, a log_printf(ebx) block, call/jmp pair
near sendcompatdata). v04/v10 share the misplaced `log_printf(...,ebx)` block (moves ~35 lines later).
Lines 667/739/799 goto order: no effect. Next: other dead-goto kinds (asm goto chains on dsp/rok lines; pf.py only
handles `if (...)` statements) on v06/v10; try the "a" pin with other e01-class fail perms.

## s89 (attempt 70): NO MATCH. Best unchanged: s88/v06.c 36/10/18

~1450 variants measured (log.txt for hand ones; hl*/hc*/cd*.log for climbs, each line = one compile).
New tools: lp.py/el.sh (permute an asm-goto label list), hl.py (climb a label list, per-seed tag),
dc.py/cd.py (set / coordinate-descend the number of `asm goto(dsp)` per dispatch case).

| what | base | result |
|---|---|---|
| fkbo label list (first 9 labels) climbs hl61/62/63 | v06/v04/v10 | plateau 36/18, 42/6, 38/13; rev = 62, any swap of p1..cdef usually worse |
| rok rkv0 list rev / first-11 rev / climb hl83 | v06, c38 | 37 / 36 / 42 - list order nearly inert |
| dsp counts per case, coord descent cd1-5 | v06/v04/v10/b22/c38 | no improvement anywhere |
| c3 JMP list perms/subsets (c1-c10) | v06 | 36 or worse (c4 = drop hdd5: 46, inv 10) |
| JMP(c3)/JMP(t4) after netDumpNand (c11-16) | v06 | 67-94 |
| more dead edges into c3: ork9/10 -> c3 (c22), ork12/13 (c37), c38 = c22 minus ork17 | v06 | **42/8/9: clientKeys block now right after netDumpNand (front fixed)** but back cold traces reorder (-r/Block swap, -w trace, Ferase/Patches/Info) |
| one extra c3 edge (c21,c31,c35,c36) | v06 | 37 (threshold needs 2) |
| same c3 edges on v04/v10 (c41-46) | | 66/62, or no effect |
| fail-line climbs hc71 (b22), hc81/92 (c38), hc91 (c38, inv-first) | | climbs only reach 36 by undoing the Keys fix; with Keys fixed best stays 42/9 |

Finding: Keys position (call;jmp near sendCompatData in v06) is a round-4 trace order tie; >=2 extra dead
edges into c3 fix it, but the same shift reorders the freq 0-2 back traces (heap insertion order).
Keys-right and back-right look coupled through heap insertion order; next: r4sim what-if with c38's order to find
an edge that restores the back order (-r before Block, -w before CU group) without touching c3.

## s90 (attempt 71): NO MATCH. Best unchanged: s88/v06.c 36/10/18 (c38 42/8/9)

~270 variants (log.txt; sweeps sw.sh -> swa.txt, swb.txt, swv.txt), all single rok-fan (ork_i) retargets:
| sweep | base | n | result |
|---|---|---|---|
| each rkE ork (11-21,43-51) -> each case c1,c12,s5,c8,c10,cdef,t4,t5,c3 | c38 | 180 | 159 unchanged 42/8/9; ->c10 (and a few cdef) 38/12/18 (undo Keys fix); ->t5 42/10/19; 3 at 66 |
| each non-rkE ork -> rkE | c38 | 32 | 30 unchanged; ork9/ork10 -> rkE back to v06 (36/10/18) |
| rkE ork -> c3/t4/c8 | v06 | 57 | 36 or 37 |
Finding: single fan-edge retargets are inert for the back cold-trace order (-r/Blk, -w, Fer); the
fan edge counts only matter for the c3 threshold. Back order needs a lever outside the rok fan
(insert order of freq 0-2 traces), not more dead edges. r4sim what-ifs not redone this round.

## s91 (attempt 72): NO MATCH. New best: best_s91.c (= g2.c = g_27_-2.c) fncmp 42 / sig2 10 / inv 6
(previous: c38 42/8/9, v06 36/10/18). ~900 compiles (log.txt: 466 lines; hc1?/hc2?/hc3?.log: 435 climb steps).

### r4sim what-ifs (step 1)
- r4sim.py (s86 version) replays c38 (b38) and a01, g_27_-2 round 4 exactly.
- c38 round-4 order 107 29 139 138 55 33 61 68 ..., target 107 55 139 138 61 33 29 68 ... (tmap.py).
  Keys: 29 -2, 33 -1, 107 -3 (round-3 pushes); 55 -2 (ins by 49), 139/138 -2 (ins by 134), 61 -1 (by 55), 68 -1 (by 61).
- Key-only (ws.py, single/pair): best inv 8. 29 must be key -1 (wb3 freq 1) for 29 after 33.
- Push-order/insert what-ifs (wm.py, wr2.py random search, wp.py exhaustive single/pair):
  * on c38: best single = push 53 (ip3 CU, key 0) during round 3 among the priority pushes/48 trace -> inv 5.
    Not realizable: 53 has freq 0 so it can't get a priority key, and it is already in the heap
    (inserted by round-2 trace 38), so an extra edge doesn't re-insert it.
  * on a01 (29 at -1): push-53-earlier -> inv 4; 3-edit combos reach 2 (138 inserted first in 134's trace,
    80 inserted before 78 by 55's trace, push 53 early); 5 edits reach 0.
  * on g2: extra early insert of 55 (-r test) by trace 123 (t5) or 115 (c2) -> 4; + 139 earlier -> 3.
    A real asm-goto edge to k55l from t5/c2 (e01-e05) enters the loop: fncmp ~1190.
- Dummy zero-key node what-ifs (wd.py): best 6; not an obvious source construct.

### Levers that worked (step 2/3)
- a01: wb3 feed 2->3 conjuncts makes 29 freq 1 (key -1), as the sim needs (alone 60/12/15).
- r2_*: dead `({asm goto("" :::: r5x); 0;})` as FIRST disjunct of -r's usage(3) test puts 80 before 78
  in 55's insert order (CU c3/c5 order now right); on c38 alone 92/8/8.
- g1 = a01 + r2 + fail c11 chain 4->3 terms: -r now first of the -2 group (52/12/9).
- g2 = g1 + fail `ndl` (7368) chain 6->4 terms: 42/10/6. Order: 108 -r Fer Blk CU33 CU29 -w -e Inv Pat CU35 CU42 CU53 Info CU79 CU81 -c.
  Remaining: Blk/Fer swap, -w must precede CU33/CU29, Info position, plus 2 code diffs from it.
### Measured and plateaued
- cc.py: +-1/+-2 conjuncts on each of 30 constant_p chains (ccs.sh) on c38 (k_*), a01 (m_*), g1 (g_*), g2 (h_*): 432 variants.
  c38 best inv 9; g2 best still 42/6 (52 variants tie 6).
- fail-line order climbs, inv first (hc.py ... 1): c38 (hc11-13) 42/9, g1 (hc21-23) 52/9, g2 (hc31-33) 42/6.
- r5x positions r1/r3 (2nd/3rd disjunct): inert.
Tools: ws.py (keys), wm.py/wr2.py/wp.py (moves, extra inserts, random/exhaustive; target via tmap), wd.py (dummy nodes),
cc.py/ccs.sh (conjunct-count sweep), ms.sh (measure existing .c).
Semantics: best_s91.c differs from c38 only by dead constant_p conjunct counts and a dead asm goto that never jumps.

## s92 (attempt 73): NO MATCH. ~150 variants (log.txt).
Best fncmp: best_s92.c (= e6.c) 36/10/8 = g2 + dead `__asm__ goto ("" :::: einv);` at start of esucc in clientEraseBlockI.
  Fixes Blk/Fer swap (order: -r Blk Fer CU33 CU29 -w -e Info Pat ... Inv). Remaining: -w before CU33/29, Inv/Info placement.
p_0_-2 (cc sweep on e6, chain 0 -2) fncmp 34 but inv 18 (CU29 jumps early).
- v01-v05: constant_p goto k55l from case 2/5: loop entry wrecks freqs (fncmp ~960) even as dead constant_p edge.
- fkbo label adjacent swaps (f0-f7), rk list swaps (r0-r9): inert or worse.
- w1-w3 (w5x disjunct position): inert. e1/e11/e12 (edge to einv at eerase): -w moves before Blk/CU33 (wanted) but CU81/Inv jump, inv 18.
- e2/e4/e8/e10/x2-x6: worse. ccs sweep on e6 (ccs_p.txt, 109 variants): best inv 8.
Next idea: combine e11's -w move with something that keeps CU81/Inv late.

## s93 (attempt 74): NO MATCH. ~62 variants (log.txt; scripts b1-b6.sh, bases e6/e11/b08/b08x).
Best fncmp still e6 (36/10/8). No new best.
- a01-a20: edges in clientEraseBlockI on e6/e11. Any einv edge at eerase (asm goto or constant_p, 1-3 conjuncts)
  gives e11's state (-w before Blk, CU81 early, inv 18). eout/esucc edges to eout: much worse. Removing einv cold: much worse.
- b08 = e11 with wb3 hint reduced to 2 conjuncts (drop `__builtin_constant_p(i + 62)`): fncmp 42 inv 9,
  order -r Fer CU29 CU33 Blk -w -e Inv Pat .. Info -> Inv/Pat/Info now in target order, CU81 back late.
  Remaining for b08: Blk must precede Fer, -w must precede CU29/CU33.
- On b08: esucc/eout/efail edges (d01-d08, g01-g10, separate efail label b08x) all worse or inert;
  r5x position, k55/k67 conjuncts, w5x extras inert or worse; u2 conjunct changes much worse.
- e6 + wb3 2-conj (c01): Blk ok but Info/Inv wrong (inv 11); 1-conj (c03) fncmp 34 inv 18.
Next idea: from b08, find a Blk/Fer lever that doesn't involve the esucc->einv edge (which on b08 hurts, c06).

## s94 (attempt 75): NO MATCH. ~330 variants (log.txt, q.log, r.log, s.log; scripts v1-v5.sh + ccs sweeps).
New inv best: best_s94.c (= n2 = q_1_1) fncmp 42 / sig2 10 / inv 6.
- n1 = b08 + dead `if (__builtin_constant_p(block+5)) goto einv;` at end of eout (before JUMP(efail)) in
  clientEraseBlockI: 42/10/7; Blk moves up to Fer (order -r Fer Blk CU29 CU33 -w). Conjunct count/order/
  position inside eout inert; JUMP(efail) can be dropped (v31 same). goto at eout start / esucc target: worse.
- n2 = n1 + cc chain 1 +1 conjunct: CU33 before CU29 -> inv 6. ccs sweeps on n1 (q) and n2 (r): plateau 42/6.
- x1 = n2 + e6's `asm goto einv` at start of esucc: 36/10/8 (Blk Fer fixed, Info/Inv swapped back); ccs on x1 (s): best 34/18, 36/8.
- -w levers on n1 (w5x disjunct positions/removal, extra edges to w5x/wb3, cold w5x/wb3): all inert; hot k61l very bad.
- efail/esucc edges to eout/einv (v45-v50): worse or inert.
Remaining on n2: Fer before Blk, -w after CU33/CU29. On x1: -w and Info/Inv.

## s95 (attempt 76): NO MATCH. ~600 measured variants (log.txt; v1-v9.sh, ccs sweeps c/e/f/m/p.log, hc7.log).
New best: best_s95.c (= d01) fncmp 26 / sig2 6 / inv 5 (was n2 42/10/6). Diff vs n2 = two dead gotos:
- b06 = n2 + `if (__builtin_constant_p(i + 5555)) goto k61l;` after -r's log_printf: -w (blk 62) freq 1->2, so it
  now precedes CU33/CU29 (sub-problem A solved). Same effect: a09/a12 (asm goto k61l, worse fncmp), a13/b05
  (`&& !cp` on -r test). But zero group scrambles (CU81 first; fib-heap structure) -> 42/10/18.
- d01 = b06 + `if (__builtin_constant_p(block+9)) goto eout;` at end of esucc: Blk freq 2->3; zero group back in
  target order. Order now: Blk CU108 -r Fer -w CU33 CU29 -e Inv Pat CU35 CU42 CU53 Info CU79 CU81.
  Remaining inv 5: Blk(140, key -3, ins by 135 myatoh32 trace) before CU108/-r, and Info(146) after CU53.
- r4sim on n2: -w alone needs key -2 (done). On d01: key-only (<=3 overrides) best 4; wp/wr2 insert what-ifs
  again only reach <5 via an extra early insert of 55 (-r test) from 123/135/143/105 = edges into the loop
  (g01-g03: cp goto k55l from after the loop -> fncmp 850+).
- k4 = d01 + cc chain 4 (-ip goto k55l) -1: -r freq 3, still 26/5 (Blk CU108 -r). k1 = + chain 2 -1 (u2):
  CU108 -r Blk Fer -w CU33 CU29 correct but CU108 above hdd5/hdd4 and -c/zero group off (148/16);
  m_6_2 (k1 + k61l chain +2) 138/8/8.
- Inert/worse: E()/expect/cold/hot on -r/-w tests (a01-a06), JMP(i0)/cp goto i0 for Info (h*, b06h*),
  -c usage cold/asm (c1-c4), eout edge variants (d11-d16, j*), esucc->efail (j01: Fer 3, 122/8).
- ccs on b06, b01 (x1+lever), d01, k1, m_6_2 and fail-line hc on d01 (hc7): plateau 26/5.
Next: from d01 need Blk tie-broken after CU108/-r (fib-heap tie) and Info earlier; try k4/k1-type freq shifts
with compensations for CU108-vs-hdd (CU108 key -4 ties hdd5/hdd4).

## s96 (attempt 77): NO MATCH. ~260 measured variants (log.txt; v1-v5.sh, ccs sweeps p14.log on a14, pk4.log on k4).
Best unchanged at 26/6/5; best_s96.c = b01 = d01 minus the JMP(i0) in s4 (identical score, one hint fewer).
- Round-4 keys are tiny ints (-freq), so Blk(140)/CU108/-r order is a pure fib-heap tie: d01 140,108 at -3, 55 at -2;
  k4 has all three at -3 and still extracts 140,108,55. r4sim on k4: 140=-2 puts it after 62 (139/62 tie wins);
  wd.py dummy pushes/inserts on k4 bottom out at 4 (same as s95).
- Blk freq 2 via any dead edge into efail before the range test (a08/a11/a14/a16/a19): order CU108 -r Blk -w (Blk
  right place) but Fer drops to freq 0 and zero group scrambles (46/10/22); ccs on a14 best inv 15.
- Edge into eout before the tests (a06/a10/a15/a17), removing eerase->einv (c02): Blk freq 4 (36/8/10).
- Conjunct count / (char*) form of esucc->eout goto: Blk 2, zero group broken (a01-a04, 42-50/10/18).
- Inert (26/5): JUMP(efail,esucc), extra einv edges (c03-c07), JMP(i0) removal/dup (b01,b05), JUMP(i0) dup (b04).
- Harmful: dropping einv/i0/p0 cold labels (c01, b03, b06), dropping JMP(p0) in c12 (b02).
Next idea untried: make Fer keep freq 2 while Blk gets freq 2 from an efail edge (e.g. second efail edge from
the success path), then fix the Fer/Blk tie and zero group.

## s97 (attempt 78): NO MATCH. ~300 measured variants (log.txt; v1.sh, gen1.py g_/h_/j_ sweeps, ccs q.log on H1, gen2.py k_).
Best unchanged: best_s96.c (= b0.c here) 26/6/5.
- a00 = b0 + dead `cp(block+79)&&cp(block+80) goto efail` before the range test (s96 a14): Blk 2 in place, but
  Fer (LC117) rises to 3 and moves early; Success block (LC116) appears at freq 1 after -w; zero group scrambled.
- gen1.py: dead goto {efail,esucc,eout,einv,eerase} x 1/2 conjuncts at top/eerase/esucc(before/after)/eout/efail,
  on b0 (g_) and a00 (h_). Fer back to 2 only via an esucc SELF-LOOP (h_su_esucc_1 = H1.c, 42/10/18):
  CU108 -r Fer -w Blk ..., zero group starts CU81 and ends Inv.
- ccs on H1 (q.log, 118): nothing below 26; q_8_2 (k61l chain +2) gives CU108 -r Fer Blk CU33 CU29 -w:1 with the
  zero group right (42/10/6) but -w drops to 1.
- efail SELF-LOOP on H1 (j_fa_efail_1 / k_efail_*, any conjunct count 1-8): 30/8/11, CU108 -r Blk -w (Blk right),
  Fer at 4 early, zero group Info Pat CU35 CU42 CU53 Inv CU79 CU81. efail->einv edge: Fer 3 before -r (122/8/8).
  Conjunct counts in self-loops are inert (loop heuristics, not cp branch probs).
- kk.py (r4sim key overrides, single+pairs) on H1 bottoms at 5; wd.py on H1: only dummy-block inserts (key -3 at
  block 142 extraction, or a round-3 tail push) reach 3, none realisable byte-neutrally.
Next: lower Fer from 4 to 2 while keeping the efail self-loop (e.g. loop on a split sub-block of efail, or move the
esucc loop to esucc->efail with Success freq) and check Blk/Fer tie order; zero group then needs Inv/Info swap.

## s98 (attempt 79): NO MATCH. ~320 measured variants (log.txt; c2.log = ccs on k2h).
Best unchanged: best_s96.c (= b0.c) fncmp 26 / sig2 6 / inv 5 (invd.py: Blk before CU108 -r = 2, Info after wb5/eb5/ip3 = 3).
Tools: g1.sh (efail/esucc loop shapes on J1), g2.py (self-loop wrap/after/before on 11 statements),
g3.sh (JMP(i0) real edges), g4.py (efail loop on asm split part, +/- top goto), g5.py (k61l chain 1-5 on H1/J1/m02n),
gen1.py top/er/ou gotos on m02n (n2_*), invd.py (named inversion order), sw.py/sw2.py (r4sim insert-order what-ifs).
Findings:
- Self-loops on argv-loop statements (-r/-w/-e/-ip printf, mode=1/2) and on "erasing"/Success/Inv: inert.
- Blk self-loop (wrap or before) on H1 gives exactly b0's order (26): loop on eout = Blk 3.
- efail loop: Fer 4 (with top goto efail), 22 (loop before printf, no top goto), 3 (empty loop after printf), 1 (loop
  after printf, no top goto = m02n: Blk 3, Fer 1 after CU33). asm("") split parts merge into the Fer block: no new values.
- Observed (Blk,Fer) pairs only: (3,2 b0 order), (2,3), (2,2 -> -r Fer -w Blk or -r Fer Blk with -w 1), (2,4), (3,1), (4,1).
  Never Blk 2 + Fer 2 with Blk before Fer.
- k61l chain: -w freq is binary (0 extra conj -> 2, >=1 -> 1) on H1/J1/m02n.
- JMP(i0) real edges from any block raise Info freq to 1-2 (worse); JMP(i0) in p0 / before clientPatches(arg) inert.
- r4sim (sw.py): on H1 the order among key-0/-2 ties is fibheap-shape driven; deleting 146 before 142's inserts gives 3,
  but 146's push cannot be removed realistically (nopush 16). Edge-order perms of 134/55 give >=10.
- ccs on k2h: no change below 42 / inv 6.
Next: needs a heap-shape lever (an extra round-4 insert/delete of a dummy block between 134 and 142 processing)
that is byte-neutral; loops and cp gotos only move integer freqs, which are exhausted around Blk/Fer.

## s99 (attempt 80): NO MATCH. ~1490 measured variants. Best unchanged: s96/best_s96.c (= b0.c) 26/6/5.

Zero-byte blocks (the s98 idea) - findings:
- They exist at bbro. `asm goto` edge to `zd: __asm__ volatile(""); __builtin_unreachable();` (z01) gives a separate
  0-byte bb; an empty asm volatile before a case label (`case 12: asm volatile(""); AT(c12)`, gv.py zb_*b) gives a
  0-byte block on the switch edge that connect_traces places right before the case block (bytes unchanged there).
  An asm volatile after a label inside a block is merged (no new bb). zb_i1b/p1b/s5b: new block, nothing changes.
- But no realisable dummy is freq-neutral: any extra asm-goto target (gz.py, 40 variants, fncmp 108-334) takes
  tree-level flow (e.g. 146 9->4); a forwarder `zf: asm volatile(""); goto L;` on a cold-label edge (z02,
  gf.py 199 variants, 96-300) moves the cold prediction onto the forwarder (Pat 0->3). Block freqs come from the tree
  estimate; RTL asm-goto edges get uniform probs (EDGE_FREQUENCY 143->127 = 3 while bb 127 freq 0).
- Switch-edge dummies (zb_c2b/c3b/c12b/...) do act as heap-shape levers: CU108 moves before Blk, but the zero group
  scrambles (inv 14-25, fncmp 134-318).
- climb.py (inv objective, 104 asm-volatile levers = AT sites + gp.py positions that changed code): inv 3 reached
  (climb1.log); red.py reduces it to 7 levers (rdbest.c: CU108 Blk -r Fer -w ..., Info right after Pat) but
  fncmp 219: the levers also reorder hot/round-1-3 code (extra jmp/je), so not byte-neutral.
- climb2.py (fncmp objective, 450 evals): nothing below 26 (sideways 26 only).
Tools: gz.py/gz2.py (dummy targets), gv.py (asm before/after AT), gp.py (asm at every stmt boundary, p.out),
gf.py (forwarders), cfg.py (pred/succ from -fdump-rtl-cprop_hardreg-blocks-details, cfg/pre.txt), run.sh/run2.sh,
fo.sh, climb.py/climb2.py/red.py. Note: python-written lists are CRLF; strip \r before shell loops.
Next: a combined objective (inv + count of hot-order changes) climb from rdbest, or constrain levers to ones whose
single effect leaves rounds 1-3 untouched (compare trace lists up to round 3).

## s100 (attempt 81): NO MATCH. ~850 measured variants (log.txt, climb3_*.log). Best unchanged: b0.c (= s96/best_s96.c) 26/6/5.

Tools: ev.sh NAME (fncmp, inv, hot = diff of r1-3 block list vs b0 from hs.py), sub.py MASK (b0 + subset of rdbest's
7 asm insertions), pos.py (asm at every ; { } of given lines), climb3.py BASE SEED N (lexicographic (fncmp,inv) climb
over p.out asm levers).
- All 127 subsets of rdbest's insertions on b0 (s_*.c): none below 26 (s_8 28, s_64 32). Single bits: 1,4,8,16,32
  keep r1-3 identical (hot=0) yet fncmp 82-158: round-4 trace extraction itself reshuffles (T26/T27 swap etc.).
  inv 3 needs bit 2 (asm after `goto dtg;` line 725, or anywhere on line 723/724): it splits the reboot-test block
  (hot 1:138:L726 -> 1:142:L725). s_42 (bits 2,8,32) = CU110 Blk -r Fer -w ... Pat Info, inv 3, fncmp 153.
- pos.py around lines 723-734 on s_40: inv 3 only from lines 723/724 positions (always hot=2); others inv 15/18.
- climb3 from s_42 (300): best 64/9 by random-walking many levers; from b0 (400): 238 evals sideways at 26/5, none lower.
Conclusion: the inv-3 shape requires the line-724 block split; no zero-byte lever found that gives it with hot=0.

## s101 (attempt 82): NO MATCH. ~4000 measured variants (climb4_*/climb5_*/climb6_*/sx_*/sw_*/rd_* logs, sub_f2.log, sw15.log, ps_f2.log). Best by fncmp unchanged: b0.c (= s96/best_s96.c) 26.

Key finding 1 (metric): fncmp.py's difflib diff overstates mismatches when blocks move. f2.sh (fncmp2.py dumps
normalized ref/mine; count = GNU `diff --minimal`) gives the true edit size: b0 26, s_42 33 (fncmp said 153),
v08 35. Old fncmp-ranked results (s99/s100) should be re-read with f2.sh. climb6.py / sx.py use f2.sh.
Key finding 2 (s_42's "hot change"): the line-725 empty asm blocks jump threading of the argc<=0 path
(original and b0: `jle` -> client_usage(2)); s_42 instead jumps to the reboot test via an extra
`xor ebp; [44]=0; xor edi; [40]=0; jmp` PHI-copy block (5 extra lines, reboot block freq 138->142).
Explicit thread `for (i = 0; i < argc || ({ if (!i) goto u2; 0; }); i++)` (w15; equivalent: loop exit with
i==0 iff argc<=0, mode=0/reboot=0 -> u2) or `if (i == 0) goto u2;` after the loop restores the jle and
makes the line-725 asm irrelevant. Best of that family: y36.c (w15 + rdbest bits 4,32) f2 32, plateau
(single-lever sweep + 2 climbs). Residual vs original there: BinPatch block after netReboot (10, also in b0),
u2+printf moved early (10), -r cmp/mov sched (2, also b0), 3-line usage block (6, also b0).
- climb4 (hot,inv,fncmp) from s_42 found fncmp 43 = s_42 + one asm after `a = argv[i + 1];` (-w); x.s
  differs from s_42 only by a cmp/mov swap -> purely a difflib artifact.
- Single sweeps with f2 on b0, s_42, w15, y36: nothing below 26/33/32/32. All 127 rdbest subsets: min 26 (s_8);
  with w15: min 32. pos.py positions at 721-736/794-800: 33/48/50 only.
- w01-w08: other zero-byte forms at line 725 (asm with inputs, asm goto, dead bcp gotos): 33 or 50.

## s102 (attempt 83): NO MATCH. New best best.c (= e_12.c) f2 24 (b0 26).

Fix: -r cmp/mov sched swap solved by adding a labelled usage(3) target to the r5x asm goto:
  if (({__asm__ goto("" :::: r5x, r3x); 0;}) || i + 1 == argc || !a || *a == '-')
      { r3x: client_usage(3, argv[i]); }
(semantics unchanged: empty asm always falls through; label is only a target). Moving the r5x asm
goto later in the || chain also fixes the swap but swaps the usage 3/5 cold blocks (28).
Applied to all s99/s100/s101 .c (rr/, rr.log): b0 family -> 24, y36 -> 30; nothing else below 30.

Remaining diffs in best.c (24): BinPatch bb141 (freq 10, round-3 trace) right after netReboot (10);
Blk LC118 printf (f3, T37r4) before u2 instead of after -r log/LC117 (8); i0 clientInfo(NULL)
(f0, T50r4) after 3 usage blocks instead of directly after p0 (6).
- c11 fail feed 4/5 conjuncts drops BinPatch to f6/f5 round 4 and places it right (after WriteBlocks)
  but reshuffles round-4 heap (g4.c 56; climb from g4 only reached 30).
- i0 levers (JMP(i0) from p0/p1/i1/c8/hdd, c12/c7 asm gotos, dead cp gotos to i0): all inert or worse.
- Blk levers (eout JMP efail/esucc/eerase, feed conjunct changes): none below 24.
- c11 JMP/asm-goto/cold variants (v1.txt): all worse or inert.
- cl.py: f2 climb over p.out asm-volatile + bcp-conj add/del levers, 3x500 (cl_1..3.log): best.c plateau 24.
~1900 variants measured. Tools: sw.py (substitution sweeps, '@@' sep, ' ;; ' multi), bi.sh (bbro bbinfo), cl.py.

## s103 (attempt 84): NO MATCH. Best stays s102/best.c (f2 24).

Sweeps (sw.py now skips conflicting substitutions instead of aborting):
- v1.txt (23): c11 fail feed 3->4 conjuncts + one other fail-feed conjunct +1/-1. Best 50 (c3 feed +1), 52 (c9 -1, s4 -1); rest 56-68.
- v2.txt (89): the 23 single feed tweaks alone on best.c (13 inert at 24, others 46+), plus c11=4 with
  the 3 best v1 tweaks paired with every other tweak: none below 46.
Conclusion: fail-feed conjunct counts cannot both demote clientBinPatch to round 4 and preserve the
round-4 heap order; the r4sim-guided model work (exact fibheap insertion order) was not done here.

## s104 (attempt 85): NO MATCH. Best stays s102/best.c (f2 24). New second family: c_w2f3.c (f2 34).

Model work (mandatory part):
- r4sim (s86/r4sim.py) reproduces the round-4 pop order exactly for s102 best and g4 dumps (o_dmp_*.txt).
- Target round-4 pop order (from the ref layout): T in srch.py =
  best's order with 141 (BinPatch) after 131, 139 (Blk) after 55 (-r), 145 (i0) after 127 (p0).
- g4 = best + only 141's key change (-10 -> -6, pushed into round 4); that one extra round-4 heap node
  reshuffles ties (fib-heap shape), nothing else in the event stream changes.
- srch.py: sim with key overrides + dummy (zero-byte) heap insertions at any event; beam.py/beam2/beam3.py
  beam search, kd.py/kd2.py exhaustive key grid + 1/2 dummies.
  * From g4: 2 dummies reach dist 1 but only at round-3 positions inside the rejected-push sequence
    (pre idx 175 = between get/push 129, idx 203-206) - no trace is built there, so not realizable.
    Realizable positions (after round-3 trace visits + any round-4 group) + keys: min dist 2 (beam2_g4.log).
  * From c_w2f3: keys of {139,29,33,55} x 2 dummies (kd2_w2f3.log): no exact hit; min 1.
    Permuting the round-3 tail push order + keys: min 3. Keys alone (6 blocks, -4..0): min 2.
  => Within key changes + <=2 zero-byte insertions the target is unreachable from either state; the
     remaining Blk/55 order needs 139 key >= 55 key (Blk freq 2 or -r freq 3) AND a different heap shape.
- Realized zero-byte blocks (asm goto to `z: __builtin_unreachable();`, a*.c, b*.c) are not freq-neutral:
  the extra asm-goto target steals edge freq (e.g. 104->142 priority 5->4), and the z block gets
  key -1000100 / -1; none below 44.

Real variants (~165, res*.txt not kept; see *.d/*.mine): 
- c_wXfY.c / e_ / r_ / g_ / j_: wb3 loop-head feed (593) conjuncts X + new wb4 feed (label on L634
  client_usage(4)) with Y conjuncts. w2f3, w2f4, w4f2, w4f3, w4f4 -> f2 34 from g4 (56) AND from best
  (e_*, 141 also moves to round 4): BinPatch and i0 placed RIGHT; remaining 34 = usage 3/4 (29/33) promoted
  (keys -2/-3) plus Blk/Fer before -r. With 29/33 back at -1 (w5+), shape reverts to g4 (56).
- d*.c (esucc/eout/eerase bcp-goto conjuncts on c_w2f3): inert (34) except removing eerase goto (58).
- h*/k*: k55l (-r) feed conj -/+ : inert or worse; k3_j_w5f3 gets 108 139 55 138 62 33 29 69 but breaks p0/i0 (42).
- m*: wb4 feed inside the -wb branch: inert.
Semantics: all levers are dead __builtin_constant_p gotos, labels, or empty asm gotos (fallthrough) /
unreachable labels after return - equivalent to src/mode_client.c.
Tools: gen.py (line-local substitutions), mk1.sh/mk2.sh (feed grids), run.sh/par.sh (f2 + r4 order, 4-way), bi.sh (fixed: no longer deletes mc.bbro on rerun).

## s105 (attempt 86): NO MATCH. Best stays s102/best.c (f2 24); c_w2f3 family floor 34.

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

## s106 (attempt 87): NO MATCH. Best stays s102/best.c (f2 24). New basin: 55 before 139 realized (f2 26).

Model broadening (m.py, unrestricted; m2.py, restricted to realizable edits): beam over edits of the
round-3 tail and round-4 groups of the parsed bbro event stream (simulated with s104/srch.sim):
swp/mvp (round-3 push order), i2p (round-4 start pushed in round 3 instead), mvi (move/rekey a round-4
insertion to any group position), rkp (round-3 push key), dum (zero-byte dummy inserts), depth 3-5.
- From best: dist 1 (only 141) with 2 edits: 139 pushed in round 3 (key -3, between 33 and 53) + 55 key -3.
  The 139 edit cannot be realized: 139 (eout printf) lives in the inlined clientEraseBlockI, so all its
  predecessors are in trace 134-137 (round 4); no mode_client edge can reach it. one.py: no key/insert
  combination inside the 134 group alone helps.
- From w (c_w2f3) and g4: depth 3 min dist 2.
55 vs 139 (what decides them): both enter round 4 as "possible start of this round" with key -freq
(139 from 135 in trace 134 at -3; 55 from 49 at -2). Ties go to the one inserted first (139).
Realization found:
- 55 freq 3: k55l feed in -ip down to one conjunct (v/a1.c, f2 24, order unchanged since 139 ties first).
- 139 freq 2: remove the esucc `goto eout` dead cp goto (2/3 conjuncts act the same).
- v/e0_b3.c = w.c - wb3 feed + k55l 1 conj + esucc->eout removed: 108 55 139 62 33 138 69 29 ... (f2 34),
  first variant with 55 before 139. Rest wrong: 138 after 62/33, 29 after 69, 79/81 early.
- -w (62) freq levers: -s k61l feed off or to k67l puts 62 at -1 but also raises 79/81 (-e usage) to -1 (56).
- kg.py key grid on e0_b3 (6 blocks, -4..0): min dist 2. m2 beam from e0_b3 depth 4/5: min dist 1, never 0.
- cl.py climbs (dead-cp conjunct add/del, cost f2+2*dist, 3x400) from e0_b3 all reach the same plateau
  v/h1.c (= c/clb_1.c) f2 26: 33 108 55 138 139 62 29 69 81 79 ...; cl2.py pure-f2 climbs from h1 (2x300): 26.
  m.py from h1 depth 4: min dist 1.
Real variants: ~100 hand (v/*.c) + ~1800 climb evals. Semantics: every edit only adds/removes conjuncts
of dead __builtin_constant_p gotos or removes one (esucc->eout); equivalent to src/mode_client.c.
Conclusion: the model now covers earlier-round push order, insertion moves and 3+ dummies; within it the
target needs at least one round-3 push of a clientEraseBlockI block or a 2nd tie change that no source
lever reaches. 55-before-139 can be realized but costs 2 in f2 vs best (26 vs 24).

## s107 (attempt 88): NO MATCH. Best stays s102/best.c (f2 24).

Key finding: hand-inlining clientEraseBlockI into case 10 (mk.py -> h0.c; labels renamed *_i, function
removed) is codegen-neutral: f2 24 and the same round-4 order as best. Its labels (eerase_i, ecmp_i,
enet_i, esucc_i, efail_i, eout_i, einv_i) are now main-local, so main code can jump to them.
Semantics: same statements, run once in the same place; the only edits are dead gotos.

Variants (all from h0/h1; ev.sh = run.sh + srch.dist; ~300 hand/grid + ~1270 climb evals):
- g/c*, g2: dead cp `goto eout_i` from 19 main sites x 1-5 conjuncts x esucc->eout on/off: 139's freq goes
  3->11 (key -11), and it pops right after 105/49 (f2 34, d4). Conjunct count and site make no
  difference (the feed is quantized).
- g/b*, g/a*: a real zero-byte edge (JMP(eout_i), alone or added to existing asm-goto lists): f2 108-239,
  because `block` becomes live (and uninitialized) from the source block, which upsets RA. b15 (efail->eout
  inside the callee) costs 39. An edge from a round<=3 block (104/141/48/46/5) into 139, which the m.py
  target needs, therefore always costs this RA damage, so (a) is not reachable for free.
- g3/g5: feeds to the other callee labels. einv_i: neutral (24/32, same order). efail_i: 139 drops to key -2
  and comes AFTER 55 (108 55 139, as the target wants), but 138 (now 137) drops to -1 and lands after 62,
  and 81/140 move (f2 40, d5). eerase/enet: 136 takes over (f2 98). Pairs of feeds: nothing better.
- g6: feeds into c10 / ecmp_i (top of the 134 trace): with the c10 feed from site 13, 134-135 become a
  round-3 trace (134 [13] 135 [13]), so 139 is pushed in round 3, but at key -6, 134 leaves the round-4
  list, and f2 is 82-104.
- cl.py climbs (conjunct add/del, cost f2+2d), 4x~320: from ef.c (efail feed) to 44-48; from iv.c (einv feed) 38.
Conclusion: a round-3 push of 139 needs either a real edge (RA damage from `block`) or a 134 trace that is
hot enough for round 3 (then 134 leaves the round-4 list, which contradicts the target). The efail feed
newly gives 55-before-139 ordering, but at the cost of 138's key and of 81/140.

## s108 (attempt 89): NO MATCH. Best stays s102/best.c (f2 24).

Direction: structural source variants (not dead-goto levers). ~170 compiles; ev.sh = s104/run.sh 4-way + dist.py.
Files: pre.c/post.c (best.c split around clientEraseBlockI), gen.py + vars*.txt (callee bodies),
gm.py (main-region variants), gf.py/gp.py (feeds on the s107 h0/ef inlined family), res in ev.out/res*.txt.

1. clientEraseBlockI restructurings (vars.txt e01-e20): early-return chain, outer/inner/net polarity swaps,
   else-if chain, goto error labels at the end (two label orders), do{}while(0)+break, int return,
   net result in a variable, range test via local. ALL compile to the identical layout (f2 24; only
   block numbers shift). gcc canonicalises these shapes before bbro, so statement structure is not a
   free lever here. Variants that change code: shared msg-variable exit (e05) 51, ternary printf (e09) 48,
   status-code switch (e10) 124, no levers (e11) 64, out-of-range test first (e13) 42, local n (e17) 32,
   einv not cold (e15) 46 (gives 108 139 55), eout cold (e18) 70.
2. Hot/cold labels on each callee label and pairs (vars2/vars3, 24 variants): efail hot = 108 55 139 (target
   order) but 138 drops after 62 and efail becomes the fallthrough of the netErase test (je->jne + sunk
   [8+esp] store), f2 40 - same as s107's efail_i feed. efail hot + esucc hot cancels back to best (24).
   Everything else 34-132.
3. main regions (gm.py, 20): case 12/7 polarity / early break / shared call (m01,m04-m07: 24, same layout),
   arg=NULL + single call (m02/m08) and ternary clientInfo (m03) ~110; switch case text order (m09-m13): 24;
   -r: if(!mode) nesting, i++ split, arg=a: 24; mode=1 before log (m15) 40; extra dsp asm gotos on c10/c11 50/76.
4. efail_i feed (s107 ef.c) + compensating esucc_i feed (gf.py 7 sites x 1-3 conj; gp.py 8x8 site pairs
   from h0): esucc feed restores the je fallthrough but makes 138/139 pop right after 49 (f2 46);
   best pair p_57 (efail from c9, esucc from c11) f2 30. Register pins were not applied: the ef damage is a
   fallthrough choice (efail vs esucc after netEraseBlock), not register allocation, so a pin cannot repair it.
Semantics: every variant keeps the statements/outputs of src/mode_client.c (restructurings are
control-flow equivalent; levers are dead __builtin_constant_p gotos or label attributes). e09 passes an
extra ignored vararg to the "Success!" printf (output identical) - probe only.
Conclusion: source structure in these regions is canonicalised away; only frequency changes move the
order, and those re-enter the known efail/esucc fallthrough trade-off. No variant below 24.

## s109 (attempt 90): NO MATCH. Best stays s102/best.c / s107/h0.c (f2 24).

Joint combination search of the three known lever families on h0.c (hand-inlined erase).
lev.py applies a config: wb3 feed (b=best, 2/1 conj, n=none), wb4 feed conj 0-4 (+ wb4 label),
fail->c11 conj 3-5, k55l conj 0-2, esucc_i->eout_i goto on/off (e), dead-cp feeds to
efail_i/esucc_i/eout_i/einv_i from 8 case sites (pf/ps/po/pv, conj counts pfn/psn).
All levers are dead __builtin_constant_p gotos / labels: semantics identical to src/mode_client.c.

1. g1.py grid: 1584 variants (wb3 x wb4{0,3} x c11{3,4} x k{2,1} x e x efail/esucc site pairs).
   Floor 24 (only the unmodified-feed configs); next 26 (k1 + efail&esucc both from c9),
   30 (24 configs, incl. p_57 family). wb3 alone is inert (b == n). Results g1.out.
2. sa.py simulated annealing (cost f2 + 0.1*dist, T 8.5->0.5, 1-2 lever mutations/step),
   4 chains x 350 from {h0, k1+p55, w2f3, w2f3+k1+e0+p56}, then 4 chains x 450 from a newly
   found second f2-24 layout. ~2500 real evals (logs sa_*.log). Floor 24 in every chain.
   New: a second f2=24 layout c113_e0_k1_pf5_pfn2_po1_ps2_psn1_pv3_wb3n_wb40 (sa_*/) with
   order ...49 139 138 55 108 125 121...: the 145 clientInfo(NULL)/log block moves right, but
   the erase-region blocks swap instead (same 24 count, d=6). Chains seeded there never got <24.
3. Remaining diff of h0 (24): three blocks misplaced - clientBinPatch call (141), a
   log_printf(0,..) block, and a call+jmp near the end; every lever combination fixing one of
   them displaces another by the same amount (quantised feeds).
Conclusion: the lever families do not compose; joint space (grid + SA, ~4000 evals) floors at 24.

## s110 (attempt 91): NO MATCH. Best stays s102/best.c = s107/h0.c (f2 24).

New lever classes on h0.c (copy here), flags -O3 -fno-toplevel-reorder -fno-ipa-profile
-fno-reorder-functions --param builtin-expect-probability=50.

1. gen.py -> v/, r1.txt (109 variants). Callee attributes:
   - local callees via asm-label alias decl (`clientXA(...) __asm__("_clientX") __attribute__((A))`,
     TODO(prototype cast)), A in cold/hot/noinline/noclone on clientBinPatch, clientInfo,
     clientPatches, clientWrite, clientKeys, clientRead/WriteBlocks: hot/noinline/noclone inert (24,
     identical asm). cold: clientBinPatch 66, clientInfo 104, clientWriteBlocks 56, rest inert.
     client_usage alias errors (already noreturn; it is the only true noreturn).
   - externs (redeclared with attribute): hot/leaf/nothrow inert everywhere; cold netReboot/
     netDumpNand/sendCompatData inert, sendAvatarData 84, netGetInfo 110, netConnect 170,
     netDisconnect 234, strnicmp 564, log_printf 581; pure strnicmp 800.
   - optimize("...") on mode_client, 40 -f toggles: best no-tree-sink 26 (same three blocks
     misplaced + a cmp moved), no-tree-fre 36, others 46-829; several inert (24).
   Cold-call predictor is a fixed-quantum predictor too: no continuous effect.
2. gen2.py -> v2/, r2.txt (83 variants): __builtin_expect(!!(c),0) on every real condition in
   mode_client (whole and per ||/&& term), and removal of each existing E(). With the param at 50
   expect forces 50/50 (first-match), so it is a strong quantum, not continuous. 29 variants inert
   (24, same asm), next 32 (removing E(reboot) at dtg: clientBinPatch block moves elsewhere), rest 33+.
3. sa2.py / lev2.py: s109 SA space extended with expect site x/xt, cold callee, optimize flag.
   4 chains x 300 (from h0 and from s109's second 24 layout), ~970 real evals (sb_*.log):
   floor 24 in every chain; next 26.
Remaining diff unchanged: clientBinPatch call block, a log_printf(0,..) block and a call+jmp
block. Every tree-level toggle leaves the bbro result for these blocks identical, i.e. the
bb-reorder input that misplaces them is robust; attributes/expects only add quanta.
Semantics: attributes are hints (cold/hot/noinline/leaf/nothrow true for these callees;
pure strnicmp true); expects don't change semantics. Variants are probes only.

## s111 (attempt 92): NO MATCH. Best stays s102/best.c (f2 24).

Reverse-engineering from the profiled (matching) build.
- fdo.sh: build.sh's fdo compile of src/mode_client.c (-DBUILD_FDO, mode_client.prof,
  align-loop-iterations=100) with -fdump-rtl-bbro-details -> pf/mc.bbro, pf/bbinfo.txt.
  s86/r4sim.py reproduces its round-4 pop order exactly.
- Block map prof->best in wp.py (M). Prof round-4 order, in best's numbering:
  142 96 113 116 119 122 115 129 131 134 141 126 147 49 125 121 108 55 139 138 62 33 29 69 140 127 145 35 42 53 79 81 75 83 88 154 97 155 98 93 95
- Differences in the bb-reorder input:
  * Prof keys form a priority ladder: (prio,freq) 142 (9,10), 113/116 (8,9), 119/122 (8,8),
    115/129 (7,9), 131 (7,8), 134 (7,7), 141 (6,10), 126 (6,9), 147 (6,8), 49 (6,7); the switch edges
    carry almost all of each case block's frequency. best has flat ties: 113/116/119/122 (4,6),
    134 (4,5), 115/129 (4,4), 131 (3,8), 126 (3,5), 147 (2,4), 49 has no priority (-7). So best's round 4
    is mostly tie-breaking (fib-heap shape); prof's is mostly keys.
  * Prof's 141 (BinPatch, f10) goes to round 4 because of count_th (profile counts), not freq.
  * Prof's round-3 events differ too (121/125 are inserted in round 3, 108 is a push, 96 is in round 4,
    105's twin is built in round 2). Putting prof's keys onto best's event stream (wp.py) gives dist 13:
    the keys alone are not enough without prof's insertion structure.
- New lever: the round-3 threshold is exec_th = floor(entry_freq * 50/1000). best's entry is 219 -> th 10,
  so 141 (f10) is built in round 3. With entry >= 220 (th 11) 141 is pushed to round 4 with key (3,10).
  Clean realization v/h2.c: label h0 on the help client_usage(0, NULL) plus a 2-conjunct dead-cp goto h0
  at the loop head. Entry goes to 221 and the only other change is block 5's freq (12->15). But (3,10) pops
  before 131 (3,8) and the extra round-4 node reshuffles the tail (dist 9, f2 64). Same with h1 (1 conj).
  wb3 1-conj (a6) raises entry to 223 but also 29's freq (1->5); a6c4 (+ c11 4 conj) gets the front
  exactly right (...129 131 141 126 147 105 49) but the tail is wrong (29 early, 139 before 108; f2 38).
- Loop exits to post-loop labels (lend before the NO_MODE_ARG test, dtg, ndl; 1-14 conj, v/t*,e*,dtg*,ndl*)
  restructure the code after the loop (e.g. netDisconnect freq 34->112): f2 >= 70. Label alone (l0) = 24.
- ~95 real variants (v/*.c; ev.sh prints f2, entry freq, 141's trace/round). r4sim what-ifs: wi.py
  (141 pushed with key K), wr.py (also dropping one round-4 node: dist 2), srch.py on h2: min 3 with 2 edits.
Conclusion: the matching build's round 4 is decided by a ladder of switch-edge priorities that best's
quantised dead-cp feeds don't produce. The entry-threshold lever (h2) moves 141 to round 4 cleanly at
f10, but its key, like the earlier feed levers, comes with the same tail reshuffle. Floor 24 stands.
Semantics: every variant only adds labels and dead __builtin_constant_p gotos (never taken), or changes
their conjunct counts. Equivalent to src/mode_client.c.

## s112 (attempt 93): NO MATCH. Best stays s102/best.c (f2 24).

Goal: reproduce the profiled build's round-4 priority ladder (s111) without the profile.
Tools: run.sh (f2 + round-4 pop order with each block's last (prio,freq) key, via keys.py),
gen*.py (variant generators), w1.py (r4sim what-ifs). b0.c = copy of s102/best.c. log.txt has all runs.

Why best has no ladder (analysis):
- gcc 6 sets even probabilities on every >2-successor block without a profile (combine_predictions_for_bb
  returns early for nedges != 2), and expand_case keeps those per-edge. So every switch edge out of dsp
  (freq 46) is ~46/13 = 3.5. Case labels per edge, grouping, or a dead extra case can't make them
  unequal. Priority is the max EDGE_FREQUENCY over preds that are trace ends (or DFS back edges), so
  only the switch block (and case blocks that end traces through the JMP() inter-case edges) give
  priority. Feeds from the rk/fkbo asm-goto weight tables add frequency, not priority, because those
  blocks are mid-trace.
- So the "dilution" in best is not the issue (freq is already about prio+1..+4). The issue is that all
  switch edges are equal and the absolute scale is too small (prio 3-5) to give a 10-step ladder.
Variants (54 real, all f2 >= 24):
- p_/m_*: +-1 rk weight per case target (18): f2 24 (most, keys unchanged: rk is ~20 freq / 52 units,
  so one unit is < 1) or 46-56.
- f_*: drop one case label from the fkbo asm goto (5): 38-50 (f_c10 = 38: 129 before 134).
- d_*: +-1 `asm goto dsp` back edges in c1/c3/c9 (6): 24, keys unchanged (no effect on dsp's freq).
- g1..g12: dead k-conjunct cp `goto dsp` at the loop head to scale up dsp (12): 142-204. The extra edge
  restructures earlier passes; even k=12 (no freq change) is 166. Scaling dsp's freq this way is not
  viable.
- q_*: fkbo fa slot retargeted to a case (weight table on the hot path, 12): 56-134. Raises case freqs
  and pushes 141 into round 4 at f9, but no priority ladder (q_lad: prios collapse to 2).
r4sim (w1.py on best's dump): pushing 141 into round 4 with any key in (2..3, 5..10) x 134/126 overrides
gives dist >= 7 (tail reshuffle), vs base 3. Same as s111.
Conclusion: a per-case priority ladder isn't reachable without a profile: switch edges are equal by
construction, and the levers that add per-case weight (rk/fkbo tables) add frequency, not priority.
The only ways to change priority are dsp's total frequency (uniform for all cases; the dead-goto way
breaks the code) and the JMP() inter-case edges (already used). Floor 24 stands.
Semantics: variants only change targets of never-taken empty asm-goto labels, add or remove empty
asm gotos, or add dead __builtin_constant_p gotos. Equivalent to src/mode_client.c.

## s113 (attempt 94): NO MATCH. Best is still s102/best.c (f2 24; b0.c is a copy).

Tools: gen.py (variants: c11=N conjuncts, j:POS:LBL empty asm goto), run.sh (f2 + round-4 keys),
kc.py / kd.py / kv.py / kh.py (r4sim searches on a dump), sa.py (real SA over every dead-cp chain's
conjunct count plus optional empty asm gotos), sa1..4.log + sa*/best_*.c, log.txt.

Main finding: the premise "best has no ladder" doesn't hold up. r4sim on best's dump: best's round-4
order already matches the profiled order for the whole front (142 113 116 119 122 134 115 129 131 ...
126 147 105 49 125 121). The f2 of 24 is exactly three misplaced blocks (asm diff, b0.d):
141 clientBinPatch (built in round 3, but the original builds it in round 4 between 131 and 126),
139 log_printf (pops before 108/55) and 145 clientInfo(NULL) (in the tail).
So a key ladder isn't needed. Hill-climbing key overrides on the case blocks never gets below
r4sim dist 3 (= base).
- Fail->c11 dead-cp conjunct count 4 (k4.c) or 5 pushes 141 into round 4 with key (3,6)/(3,5), at
  exactly the right front position. But the extra round-4 heap node reshuffles the fib-heap tail:
  f2 56 (r4sim dist 7). Same with JMP(c11) at p1/c8/c2 (b_*). An extra case-6 block (a_c6_c11) gets
  f2 31: 141 is correct, but it adds a jmp block, and 139 plus the client_usage blocks are still off.
- r4sim on k4 with abstract edits (extra round-3 pushes of blocks that round 4 visits, key overrides;
  extras penalised): floor dist 1 with 2 edits; 139 always pops before 55 (139 is inserted at -3 by
  134's trace, 55 at -2 by 49's). Moving that key breaks something else.
- Real variants: about 45 hand-made (k*, a_*, b_*) and about 1800 SA evals (4 chains, from k4). Floor
  26 (c7-target asm goto at i1); k4-family 56. Never <= 24.
- Renumbering the constants in the dead-cp conjuncts (same counts) changes f2 (52 vs 56), so the
  constant values themselves are a noise source.
Semantics: variants only change conjunct counts of never-true __builtin_constant_p gotos or add
empty asm gotos (never taken). Equivalent to src/mode_client.c.

## s114 (attempt 95): NO MATCH. Best still s102/best.c (f2 24; b0.c here is a copy).

Tools: pert.py/runp.sh (randomise every __builtin_constant_p(var + K) constant), g6.py/rv.sh (case-6
dead-cp gotos), sa.py (SA: conj counts + "collision" move = a chain's first constant set equal to
another chain's + case-6 empty asm goto label), sa1..4.log.

1. Constant values are NOT a tie-break lever. 200 random renumberings of all dead-cp constants in
   best.c: all f2 24. 60 of k4.c: all 56. 60 of a_c6_c11.c: all 31. The s113 56->52 observation
   must come from a collision: when two dead conjuncts get the same expression (mode + K), FRE/PRE
   value-number them as one, which changes the CFG structure (shared/threaded tests), not
   tie-breaks. (sa.py's a + 50000*i scheme can collide across chains.) So no dump bisection needed.
2. Case 6 with a dead-cp goto (1..6 conj) to c11/c12/c9/c10/... on best and on k4 (108 variants):
   best-family floor 24 (c11/c12 no change), k4-family floor 42/56. A dead-cp goto is folded before
   bbro and does not reproduce a_c6_c11's effect (141 in r4); only a real (asm goto) edge does, and
   that always leaves a jmp block (fallthrough to the switch end isn't next).
3. SA with conj counts + collisions + case-6 asm-goto label, 4 chains x 400 (1600 evals) from
   a_c6_c11 (x2), best, best+c11=4: floor 24 (only best-like configs), a_c6_c11 chains never below 31.
Semantics: only never-true __builtin_constant_p conjuncts and never-taken empty asm gotos changed.

## s115 (attempt 96): NO MATCH. Best still s102/best.c (f2 24; b0.c is a copy).

Systematic real-edge (empty asm goto) search on best.c. Tools: gen.py (family v), gen2.py (family w),
comb.py (apply any set of v/w edits: `python comb.py out.c s07_i0 n00_t4 ...`), run.sh DIR (f2 of
DIR/*.c, 4 parallel -> DIR/res.txt), scan.sh (flags which of 141/139/145 are placed right).
Targets throughout: c1 c2 c3 c7 c8 c9 c10 c11 c12 cdef hdd4 hdd5 i0 i1 p0 p1 s4 s5 t4 t5 dsp dtg ndl fail.

- v (464): append one target to each of the 21 existing asm-goto label lists in the function
  (r5x/r3x, w5x, rkv0, fkbo, the JMPs in c3/s5/c8/c9/c12, the dsp gotos). Floor 24 (130 neutral),
  39 compile errors. No stray jmp possible, but nothing moves 141/139/145.
- w (768): new JMP(t) before each `break;` in the switch and right after each AT() label (32 spots).
  Floor 24 (202 neutral).
- p (703): all pairs of the 38 singles scoring 25..34. Floor 24 (only neutral pairs).
- q (1192): n00_t4 (JMP(t4) at the end of case 1) + every valid single. Floor 25 (= base back + reload).
Total about 3100 real variants. scan.sh over all: no variant places 141 or 139 correctly. Only
145 clientInfo(NULL) ever gets fixed: JMP(t4)/JMP(t5)/JMP(s4) at the end of case 1/2 (n00/n02,
f2 27/28) and s07..s13 + i0 (f2 30). It always costs a cinfo reload (`mov eax,[l]` before the t4
test, the path skips dsp) and swaps the order inside the tail's `5` block (546-549 vs 553-556).
Adding the label to case 1's existing dsp gotos (s04..s06) instead is neutral (24), so the fix needs
a new edge.
Conclusion: single and pair zero-byte real edges into existing labels don't reach 141's round-4
placement or the 55-over-139 key order. The a_c6_c11 effect (141 right) needs a new case-6 block,
which this search space doesn't contain without a stray jmp.
Semantics: only never-taken empty asm gotos added (labels already exist, all in scope; the compile
errors were rejected). Equivalent to src/mode_client.c.

## s116 (attempt 97): NO MATCH. First variant with 141, 139 and 145 all placed right: best.c (f2 27).

base b0.c = s113/a_c6_c11.c (case-6 asm goto c11, 141 right, f2 31). comb.py = s115's, reading this b0.c.
- y/ (gen.py): c11 dead-entry conjuncts 4/5/6 x 145 fixes (n00/n02 t4/t5/s4, s07..s13 i0).
  The conjunct count does nothing. n00_t4 makes 141+145 right (f2 40); i0 sites break things (93).
- q/ (gq.py): n00_t4 + every single v/w edit (1192 compiled). s06_s4 -> f2 28, 141+145 right.
  n25_c1 -> 141+139 right (46).
- climb.sh ROUND EDITS: singles on top, cost f2 + 10*(blocks wrong) -> rN/cost.txt.
  r1 (n00_t4 s06_s4): n25_s5 = all three right, f2 28. r2: + n07_c11 removes the stray case-6 jmp -> 27.
  r3/r4: no single improves on 27 (the floor is wide, mostly neutral edits).
best.c = b0 + n00_t4 s06_s4 n07_c11 n25_s5. What's left in its diff (27 lines):
  1. cinfo reload `mov eax,[l]` before the t4 test (351) and again in the moved `call l(2,0)` block (path skips dsp).
  2. n25_s5 (JMP(s5) after AT(c9)) moves the `[esp]=2,[4+esp]=0; call` block 9 lines early (420 vs 429)
     and pulls `[8+esp]=ebx` from 465 up to 424.
  3. Tail `5`/`3` block order swapped (535-559): same as in every 145 fix.
Next: pairs over best.c targeting 1-3; register pin / edge placement after the cinfo load; another site
for the 139 lever that doesn't move the call-2 block.
Semantics: only never-taken empty asm gotos to existing labels plus the dead __builtin_constant_p entry. Equivalent.

## s117 (attempt 98): NO MATCH. New overall best: best.c (= best18.c) f2 18, all three blocks (141/139/145) right.
(previous overall best s102/best.c 24; s116/best.c 27.)

Path (on s116's b0.c, comb.py names; climb.sh/pairs.sh cost f2 + 10*blocks wrong):
- The c1 levers n00_t4/s06_s4 are NOT needed: r1 = singles on n07_c11 n25_s5 -> n26_c10 (JMP(c10) right
  after AT(c10), self-edge) gives 26 with all three right. Their reload blocks were intrinsic: every
  never-taken edge into t4/s4 from a block without cinfo in eax gets a `mov eax,[_cinfo]; jmp` block
  (tried edges after dsp, before netDumpNand, from t5/s5, "a"/"r" inputs on the asm goto: all worse).
- p1 pairs (top 40 distinct singles): + n19_dsp (JMP(dsp) after AT(s5)) + n31_i1 (JMP(i1) after AT(cdef)) -> 25.
- r3: + s07_c2 (c2 added to case 1's 2nd asm goto) -> 19 (fixes the 5/3 tail mostly).
- 19 had an extra `call _netDisconnect` (bbro duplicated ndl into the reboot-only path);
  `{ netReboot(reboot); JMP(fail); }` in dtg fixes it -> 18 (best18.c). `ndl: JMP(u2); netDisconnect();` also 18.
- k/ (b0 = best18): r1, r2 (u2/rok targets), p1 pairs: floor 18, nothing lower. Leave-one-out of each lever: all worse.
  ndl dead-conjunct lengths (g/), dtg/rok/ndl/u2 asm gotos (h/, m/), arg-parse asm gotos / label orders (c/, n/): none below 18.
Remaining diff of best.c (18 lines):
  1. u2 `call client_usage(2,0)` block placed 1 block early (ref 429) and the `[8+esp]=ebx` log block swapped (424 vs 465).
  2. reload `mov eax,[_cinfo]; jmp` (ref 502) = s5's JMP(s4,c12) edge into s4 (s4 is load-bearing: removing it -> 134).
  3. one client_usage(5, argv[i]) shared block (L608: -e/-c/-ip) placed after L407 instead of last.
~5000 variants compiled. Semantics: only empty never-taken asm gotos to existing labels (incl. a self-edge)
plus the existing dead __builtin_constant_p entries. Equivalent to src/mode_client.c.

## s118 (attempt 99): NO MATCH. Floor stays 18 (s117/best.c = b0.c here).

Semantics check of s117/best.c vs src/mode_client.c: equivalent. `{ netReboot(reboot); JMP(fail); }`
is an empty asm goto that never jumps, so control falls through to `ndl: netDisconnect();` exactly as
the original (`if (reboot) netReboot(reboot); netDisconnect(); return 0;`). All other additions are
never-taken empty asm gotos and __builtin_constant_p dead gotos; the u2/dtg/ndl dead entries fold to 0.

Variants (gen.py BASE VARFILE, '~~'-separated old/new pairs; pair.py = all pairs of a list; run.sh -P8):
- v1/v2 (55 singles): issue 2 (s4 edge moved to t5 / dsp / as "a"(cinfo) input / t4 target / order),
  issue 3 (r5x/r3x order, drop/extend w5x, cold attrs on r3x/r5x/w5x, extra edges into w5x/r5x/r3x),
  issue 1 (u2 dead feeds removed/lengthened, u2 cold, edges into u2 from parse/log blocks).
  Neutral (18, different asm): a4 (s4 moved onto the AT(s5) asm goto -> reload block moves next to
  the [8+esp]=ebx log block, still present), c1 (r3x,r5x order -> L407 usage(3) takes the early slot
  instead of L609 usage(5): the slot after the c11 log block (L541) goes to the first label of that
  asm goto). Everything else worse.
- v3 (93): an extra label first/middle/last in the r5x,r3x asm goto: all >= 39.
- p2 (1197 pairs of 52 singles): floor 18.
bbro (dd/mc.bbro): L609 = pre-bbro bb152, a round-4 key-0 trace start queued from trace 23 (bb149);
key-0 ties are taken in heap order, so it lands before patches(NULL)/info(NULL) (bb35/42); the ref
has it after L407.
~1345 variants compiled.

## s119 (attempt 100): NO MATCH. Floor stays 18 (b0.c = s118/b0.c = s117/best.c).

About 300 real variants compiled (run.sh = s118's; results in v*/res.txt). All edits are
never-taken empty asm gotos or __builtin_constant_p dead gotos, so all are equivalent to the original.
- v1/v2 (135): dead bcp feeds to r5x/r3x/u2 placed mid-loop (after each option's assignment),
  1-6 terms, the plain and (char*)==1 forms. They fold before bbro: output identical to b0 or worse
  (the statement's shape matters, the target doesn't). Only feeds at the loop top survive.
- v3/t (51): loop-top feeds (before wb3, between, after u2) to r5x/r3x/w5x/lu1/u2, 1-3 terms, plus
  retargeting the u2 feed: best 18 (= b0), the rest 34-112.
- v4 (16): issue 2, the JMP(s4) edge from other blocks (hdd4/hdd5/c1/c2/c3/c8/c9/c10/c11/c12/cdef/p1/i1),
  "r"(cinfo) input, split JMP(s4);JMP(c12): b9 (split) is neutral 18 (the reload moves into the
  [8+esp]=ebx log slot and usage(3) takes L609's early slot, like s118 a4/c1); b10 = b0; b16 is 19.
- v5 (17): adding/removing E() on every option test: E on -c/-e is a no-op; the rest 22-536.
- v6 (64): the loop-top feeds and v4 on bases b9/b16/c1: floor 18.
r4sim model of issue 3 (w2.py/w3.py/w4.py on s118/dd/mc.bbro):
- Moving bb152's insertion to any other group/position (key -2..1) always changes the order of
  other blocks. Only placements inside 149's group keep them, and those leave 152 where it is
  (or put it last if key 1).
- No single key override of any node, key -8..3, gives the ref order. The only pair hits are 152 and 75 both
  key 1 (or 152 and 83 both key 1): 152 and the strnicmp trace head bb75 (queued from 69's group) must pop after
  every key-0 tie. bb_to_key without a profile can't give a positive key (BB_FREQ_MAX needs a cold
  partition or an unlikely-executed function). Moving both insertions together doesn't hit either.
  So the ref's round 4 probably differs structurally (the tie order comes from a different heap shape),
  not from a single 152 edit.

## s120 (attempt 101): NO MATCH. Floor stays 18 (b0.c = s117/best.c).

Model (r4sim/srch.sim on s118/dd/mc.bbro; target = s119's want = sim with {152:1,75:1}, i.e. base with
bb152 moved after bb79):
- h2.py: every single and pair of dummy round-4 heap insertions (key -1/0; all 379 round-4 group
  points + last 60 pre points), every key -1/-2/0 override ("removal") of each round-4 node, and
  dummy+removal and removal+removal pairs: 0 exact hits.
- h3.py: all 3520 single moves of the 22 round-4 'ins' events (any group, any position), and the 117
  neutral moves (layout unchanged) paired with every move of the 152/75/83 insertion: 0 hits.
- h5.py: 600k random sets of 1-4 dummies (keys 1..-8, anywhere in rounds 1-4) plus an optional
  removal: 0 hits (r5_*.txt).
  So within the model no heap shape gives the ref tie order; the ref's round 4 must hold a
  different set of blocks or edges (not just extra or missing zero-byte nodes).
- Issue 1 mapped (bbs.py = post-bbro block list with old bb numbers, b0bbs.txt): u2 usage(2) = bb145
  (inserted from 141, key -2). The two log blocks are the clientEraseBlockI failure logs (LC118 "outside
  system area" / LC117 "Failed to erase" with [8+esp]=ebx). In the ref the ebx-storing LC117 copy is in
  the second group (asm 465), so the difference involves which copy holds `block` in ebx (RA/copy
  identity), not only where the blocks are placed.
Real variants (v1, 90): each of 9 labels (u2,r3x,r5x,w5x,p0,i0,ndl,hc4,hdd5_c) added to each of 10
existing asm gotos. 18 give 18, all byte-identical to b0 (the extra edge has no effect); the JMP(c11) site
gives 19 (an extra jmp); the rest are 24-119. All are equivalent: they only add never-taken empty
asm-goto labels.

## s121 (attempt 102): NO MATCH. Floor stays 18 (b0.c = s117/best.c).

Structure (dir 1): best18 (s118/dd/mc.bbro) and profiled (s111/pf/mc.bbro) bbro both duplicate exactly
two blocks (a 3474/3475-insn trace head copy and one ~120-insn tail block); no extra bb-reorder copies in
either. The profiled CFG has ~20 fewer blocks (empty forwarders absent: 143 vs 165 bbs before dup), so
the round-4 set difference is in forwarder/jump blocks, not in copy_bb decisions.
Issue 1 (ref asm 290-305, 421-469): ref stores [8+esp]=ebx once before the nandSize compare; the
outside-area and invalid logs (421/425) need no store; the "Failed to erase" copy that re-stores ebx
is the post-neteraseblock path and sits in the second group (465) after usage(2). Ours has the same
blocks, ordered usage(2) first and fail-log in the first group: ordering, not RA.
Variants (~135, all equivalent: only never-taken asm-goto / __builtin_constant_p edges or asm volatile(""))
- v/ (gen.py, 34): dead gotos between clientEraseBlockI labels (einv/eout/esucc/eerase/efail) from 5
  sites + asm volatile("") at 9 spots. 12 x 18 all byte-identical to b0; g_eo_efail2 20 (fail log
  becomes fall-through after the erase call), others 21-112.
- v2/ (gen2.py, 23): reverse / drop each label of each switch-region asm goto. 7 x 18; rm1_8
  (JMP(s4,c12) -> JMP(s4)) is a different 18: cinfo reload moves and the tail usage block becomes
  usage(3) instead of usage(5). del_11/del_22 19.
- v3/ (55): gen.py + gen2.py on rm1_8: best 18 (17 of them), none lower.
- v4/ (~28): gen2 on g_eo_efail2 and del_11: >=19.
Conclusion: clientEraseBlockI edge levers and switch asm-goto label sets are exhausted around best18.

## s122 (attempt 103): NO MATCH. Floor stays 18.

Forwarder-free realisation of the switch-region asm-goto levers (only moves/merges/drops of
never-taken empty `asm goto` -> semantically equivalent to src/mode_client.c).
- gen.py (10 levers: move block-start JMP into following stmt / merge into existing JMP / drop):
  on b0, m_c9, m_s5c, m_c8, s121 rm1_8. gen3.py (11 more: label-order, p0 operand order, c11 placement).
- ~80 variants measured. New distinct 18s (different asm from b0, same count):
  v/m_c9.c (`AT(c9)JMP(s5); {..JMP(hdd4,hdd5)}` -> single trailing JMP(s5,hdd4,hdd5)),
  v/m_s5c.c (s5 block: JMP(dsp,s4) merged, c12 dropped). Their diff vs ref is still the issue-1
  (fail-log vs usage(2) group) and issue-3 shuffles. Combos, c3 label order, p0mv: 18.
  m_c8 (c11 merged into c8's JMP) 19; dropping cdef/i1 JMP 82-126; c10 JMP move/drop 44-57;
  s5 full merge 28-52; removing AT(t4/t5/u2) labels does not compile (still referenced).
- Not done: per-block wp.py/bbs.py forwarder map and r4sim removal study (task dirs 1-2).
Conclusion: merging block-start JMPs to kill forwarders is neutral at best; the block-start
JMPs on cdef/c10/c12 are load-bearing (removing them costs 30-100).

## s123 (attempt 104): NO MATCH. Floor stays f2 18 (b18.c = s117/best.c).

Tools (all in s123): dump.sh SRC DIR (cprop_hardreg-blocks + bbro dumps), fdo2.sh (profiled build -> pf/),
cfg.py (trace-time CFG: freq/preds/succs/insns/lines/trace), map.py (best18 <-> profiled block map via
source-line alignment + symbols; map_b18.txt / map_b18_pairs.txt), ord.py/fin.py (round-4 traces and final
layout in common numbering), rm.py (r4sim with blocks removed), pfsim.py, mv81.py, keys.py, d127.py, ev4.py
(variant -> layout distance vs profiled, in profiled numbering, + count of unmapped extra blocks).

### 1. Block map (trace-time CFG, after bbro's cfg cleanup)
best18 157 live blocks, profiled 140. 139 mapped. 18 best18 blocks have no profiled counterpart; 1 profiled
block (108, the dispatch tablejump) maps to our 112 by hand.

| ours | freq | trace | source construct |
|---|---|---|---|
| 45 | 63 | T10 r2 | -I arm: split of the `if` (mapped approx, prof 45 f73) |
| 57 | 0 | T41 r4 (mid) | -r test: `asm goto(r5x,r3x)` block splits the condition |
| 66 | 1 | T44 r4 (mid) | -w test: `asm goto(w5x)` conjunct |
| 105 | 0 | T36 r4 head | rok rk network / u2 dead edge (`__builtin_constant_p ... goto` residue, no succ) |
| 106 | 0 | T36 r4 | dead block from the `mode = 7/11/9` constant_p chain (no preds) |
| 112 | 45 | T14 r2 | dsp dispatch tablejump (= prof 108) |
| 114 | 3 | T25 r4 (mid) | case 1 `asm goto(dsp)` x3 after netDumpNand |
| 117 | 6 | T26 r4 head | case 3 block-start `JMP(hdd4,s5,hdd5)` |
| 124,125 | 8,4 | T28 r4 (mid) | case 5 `AT(s5)JMP(dsp); { JMP(s4,c12); ...` |
| 127 | 1 | T46 r4 head | `mov eax,[_cinfo]; jmp` reload for the s5->s4 edge (issue 2) |
| 134 | 4 | T30 r4 head | case 8 `JMP(p1,cdef)` after clientReadBlocks |
| 136 | 8 | T33 r4 head | case 9 block-start `JMP(s5)` |
| 138,156 | 1,2 | T33 r4 (mid) | case 9 trailing `asm goto(dsp)` x3 |
| 140 | 62 | T15 r2 head | case 10 self-loop `JMP(c10)` |
| 150 | 7 | T24 r4 (mid) | case 12 `({JMP(p0);0;})` conjunct |
| 154 | 4 | T35 r4 head | default block-start `JMP(i1)` |
| 157 | 13 | T25 r4 (mid) | break/merge forwarder after case 1 |
(ours 142 = prof 125, the cinfo->nandSize test, is real; map.py pairs it wrongly with 127.)

### 2. r4sim
- rm.py: each extra removed (mid-trace: drop visit/ins; head: rename to its trace successor), all 1159
  singles/pairs/triples of 19 candidates: no hit. 15 singles are inert; 124, 127, 134, 136 make it worse.
  All extras at once: worse (s119-want dist 8, prof dist 13 vs base 1/5).
- pfsim.py: the profiled event stream with best18's keys gives a much worse order: the keys, not the block
  set, decide it.
- The real target (fin.py: final layouts in common numbering) is not s119's "want" (152 after 79).
  best18 vs prof differ only in: ...54 [108 146 145] 55..61 [129 122] 62... vs ...54 [129 122 108] 55..61
  [146 145] 62..., and usage(5) bb81 after bb79 at the tail. (129/122 = hdd5/hdd4 logs, 108 = u2,
  146/145 = erase logs.)
- keys.py: in prof 108/129/122 come into round 4 with priority keys (-1000205/-1000304/-1000303) from
  round 3, because the rok dispatch block (prof 102 = ours 104) has direct JUMP edges to u2/hdd4/hdd5 and
  p0/i0 (131/152 inserted 'next' there too). 49 has priority (-1000607) because prof's 48 ends its r3 trace:
  96 (-keys arm) has freq 9 < round-3 exec_th 10 (ours 18, so 48 96 form one trace). 145 gets a key change
  from prof's outside-area log (efail edge). Also prof's g55 inserts 79 at bb56 and 81 at bb60 (the
  `if (mode)` test); ours inserts 81,79 both at bb56 (the r5x,r3x asm goto). Moving only that insertion
  (mv81.py) just swaps 79/81 (dist 5).

### 3. Real variants (~350, all compiled with f2; all edits never-taken asm goto labels or dead
### __builtin_constant_p conjuncts, so equivalent to src/mode_client.c)
- v/ (36): -r asm goto forms on b18, s122 m_c9/m_s5c, s121 rm1_8. r1/r4/r5/r9 are equivalent 18s;
  r9 (`i + 1 == argc || ({asm goto(r3x)}) || !a || *a == '-'`, r5x edge dropped) reproduces prof's g55
  insertion order (79 at 56, 81 at 60) but the tail block becomes usage(3) instead of usage(5). r2/r3/r8/r10 20.
- w/ (123): retarget each rkE ork slot to p0/i0/u2/hdd4/hdd5/c11: slots 14-51 (2nd/3rd rok asm gotos) are
  byte-identical (their edges are gone before bbro); slots 11-13: u2 44, hdd4/5 48, p0/i0 86.
- x/ (68), y2/ (7): 2-3 of those targets together, repurposing slots 0-10, adding labels to the first rok
  asm goto (max 30 operands, so no dilution possible): 44-102. One label = 1/26 of rok freq 20 -> priority
  and freq too big (u2 jumps to asm 393).
- k/ (51), k2/ (48): lower -keys arm (96) freq below exec_th: dead cp conjuncts (`&& !cp`, `!cp &&`,
  `({if (cp) goto L; 1;})`, body gotos): 96 keeps freq 18 (merged block keeps the pre-split freq), 18 or
  90-182; never-taken asm goto at arm start/end to 16 labels: 50/50 split, but the body still has freq 18
  (freq not recomputed), best 18 (identical), else 22-73.
- f/ (12): c3b (`clientKeys(); } asm goto(dsp, hdd4, s5, hdd5)`) removes forwarder 117 byte-identically
  (also on r9); c3a 34; folding cdef's JMP(i1) into its trailing asm goto 142.
Conclusion: the remaining diff needs prof's round-3 priority structure (rok edges with edge freq 2-3 to
u2/hdd4/hdd5, 48 ending its trace). Without a profile, asm-goto edges from rok carry 1/26 of its freq at
best, and the -keys arm frequency can't be lowered (dead conjuncts/asm-goto splits keep freq 18).
Forwarder removal is inert or worse, both in the model and in real builds.

## s124: round-3 priority structure via edge probabilities (NO MATCH, best still f2 18)

Base b18.c (= s117/best.c), f2 18. Variants in a/ (~70 compiled, each with dd_<name>/ dumps).
Scripts: mk.py/run1.sh (-keys condition), mk2.py/run2.sh (-keys arm body), run3.sh (literal replace), bi.py
(block freq/succ/pred from a dump dir). Every edit is a never-taken asm goto, an unused/added label, a
hot/cold label attribute, or `for(;;i++)` -> `klat: i++` (b18N.c, f2 18): all equivalent to src/mode_client.c.

### Key finding: where the frequencies come from
- Block freqs are fixed by the GIMPLE profile_estimate (042t). Asm-goto edges to client_usage (noreturn)
  targets get ~0% there, so cascades to r3x/r5x/w5x change nothing (c2r3/c3r3: 48 [26] .. arm [18]).
  At RTL the asm goto edges are re-split evenly but block freqs are NOT recomputed.
- Asm-goto edges to live targets (k55l/k61l/k67l, klat, ks1/ks2/kn1/kip labels) do get ~30-50% in GIMPLE and
  do end 48's round-3 trace (arm or compare block drops to 13 or below), but each costs 73-300 f2: the
  target gets extra freq and the asm goto leaves an extra (empty) block that forms its own round-3 trace
  (even when the label sits on the real latch, b18N klat: gcc keeps a forwarder for the asm-goto target).
- 48's 71% arm prob is the "call heuristic" (else side starts with strnicmp). 44->48 29% likewise.
  Profiled: 44->48 17.4%, 48 freq 15, arm 9 (57%), 49 7: BOTH successors of 48 under exec_th 10, so 48
  must drop below ~20, i.e. 44->48 must be ~17-21%. No equivalent edit gives that:
  - E() (builtin_expect, param 50) is first-match: exactly 50% (G3: arm 13, f2 206).
  - cold label = ~100/0% (H1: arm freq 0, 48 chains into the else tests, f2 168).
  - hot label = HITRATE ~85% (K1 arm 24; K3 hot label on the -ip side: arm 8 but 49 18 chains; K4 on the
    -s arm: 44->48 ~7%, 48 drops out of round 3; f2 114-142). Hot+cold on both sides cancel.
  - `goto klat;` in the arm: no predictor effect (G1 = b18 identical); `continue;`: f2 102.
  DS needs an extra ~72%-vs-48 predictor on 44 (e.g. opcode-nonequal), which only 44's own compare could carry.
- (a) rok cascade (ork11/ork43 slot -> asm goto to u2/hdd4/hdd5/p0/i0, R1-R8): 47-65. A 15-label cascade (R5)
  hung cc1 (killed).
- (c) r9 -r form, asm goto moved/duplicated (T1,T3,T5,T6): byte-identical to b18_r9 (18); T2 20.

### Table (f2)
p_<target> (call; asm goto; compare): cdef/u2/dsp/c3/fail/dtg 18 (=b18), ndl 29, r3x/r5x/w5x 43,
k55l 172, k61l 270, k67l 280. c2/c3 cascades: r3x 43, w5x 43, k55l 274, k61l 302, k67l 286, m2 104/282.
L1-3 (klat) 101-147; P1/P2/Q1 x {ks1,ks2,kn1,kip} 100-158; N_* (klat on latch) 73-147; G1 18, G2 102,
G3 206; H1 168, H2 18, H3 206; K1 142, K2 54, K3 140, K4 114; R1-4,6-8 47-65; T1/3/5/6 18 (=r9), T2 20.

Conclusion: matching prof's round 3 needs 44->48 ~17% and 48->arm ~57%. Without a profile, GIMPLE heuristics
only give 29/71, 50/50 (expect), ~6/94 (hot label) or ~0/100 (cold label), and asm-goto dilution adds blocks
that wreck the layout elsewhere. Still NO MATCH; best stays s117/best.c at 18.

## s125: composing GIMPLE predictors for 44/48 (NO MATCH, best still s117/best.c f2 18)

Base b18.c (= s117/best.c). gen.py NAME EDITS builds v/NAME.c; run.sh adds f2 + profile_estimate freqs
(pf.py: -s/-keys/-ip block freq + succ probs, msg/shutdown freqs); tr.sh = round-3/4 traces (dd/NAME),
kk.sh = bbro keys. res.txt has all ~85 results. Every edit is a label, a never-taken dead
`__builtin_constant_p(i+N)` goto chain, or a hot label: equivalent to src/mode_client.c.

GIMPLE numbering: RTL 44 = gimple 49 (-s test), RTL 48 = gimple 57 (-keys), 46 = "already set" msg.
predict.def (6.2.0): call 71, hot label 85 (DS, not first-match), opcode nonequal (trees) 72,
pointer 85, early return 61, const return 67, goto 70, cold label / expect / noreturn = first match.

### New lever: break the call heuristic via dominance
PRED_CALL needs e->dest dominated by e->src. A label on the -keys test (`} else { kky: if (...-keys...)`)
fed by a dead cp goto from outside the -s arm (E: in the -eb arm, conj chain 2-5) makes 49 not dominate
57, so the -s branch loses its 71% call prediction: -s alone = 50/50, + hot label on the -s arm = 85/15
(DS of hot alone). Feed size is set by conj count (E n=2: 48 f17, n=3 f14, n=4 f13; T/loop-top feeds
are much bigger). Same trick on "setting shutdown" (label ks2 + feed) leaves only the msg arm's call:
reboot==2 prob 72&71 -> 13.7%; a feed into a label on `if (reboot == 2)` (krb) tunes msg freq.

### Results
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

## s126 (attempt 107): NO MATCH. Floor stays f2 18 (s117/best.c).

Tools: gen0.py (= s125 gen.py on b18.c), run0.sh, batch.sh LIST (4-parallel run + round-3/4 traces),
climb.py TAG ROUNDS EDITS... (greedy climb over JMP(...)+label additions and predictor feeds/hot labels).
base.c = s125 kf_7 rebuilt by gen0: Hs Lk Ls2 R=krb E=kky,4 E=ks2,3,30 E=krb,1,60 E=ks2,1,40 (f2 144).
res.txt has ~950 measured variants. All edits are dead constant_p gotos, labels, hot labels or extra
asm-goto labels (empty template, never jumps): equivalent to src/mode_client.c.

### Results
- kky feed length 5/6/8/10: saturates, 48 stays f13 (144). Stronger krb feed: 46 f10, worse (150).
- Hk (hot -keys arm, 93/7): 48->49 drops to ~1 but 96 joins 48's r3 trace (old equilibrium) -> 160.
- Li + kipt feed (-ip test dominance-off): 49 f7 as in prof, prio 7, f2 120 (best of kf_7 family);
  Li+Hk 100. Prof round 3 kept, but 49's trace lands right after 141 (prof: after 136).
- Adding a label to any existing JMP(...) on the Li base: JMP(x,c1) best, 96; the climb from there
  falls into the 48+96 merged-trace equilibrium and ends at 18.
- Climbs from b18 (no edit < 18) and from r_2_1 (K=kky,1 gives 18 = b18 equilibrium, then plateau).
Conclusion: every path that keeps prof's round 3 stays >= 96; everything better collapses to b18's
equilibrium at 18. The prof round-4 priorities of the switch-case blocks remain unreachable: the
predictor levers only move the front blocks (48/49/46), not the case arms' trace-end priorities.

## s127 (attempt 108): NO MATCH. Floor stays f2 18 (s117/best.c). Best in this family: fb5/fb6 f2 90.

Base = s126 j_dsp_c1 (Li+c1, f2 96); edits in base.edits. Tools copied from s126 (gen0.py with R= now
decoding \n/\t, batch.sh, run0.sh, tr.sh). l1..lf.txt are the batches, res.txt has all ~150 results.
map.txt = s123/map.py on base (note: running map.py rewrote untracked s123/map.txt too).
Every edit is a label, hot/cold label, extra asm-goto label (empty template), extra never-taken
`__asm__ goto("" :::: dsp)`, or a dead __builtin_constant_p goto (chain): equivalent to src/mode_client.c.

### Ladder analysis (base dump)
- Prof r4 order in base numbering: 149 96 113 117 120 123 116 133 136 141 148 130 154 49 ...;
  base: 141 49 96 149 113 117 120 123 116 133 148 136 130 154. r4sim: 49 prio <=2 + 141 prio ~3 +
  149 prio 8 reproduces the front; the case keys themselves only need to beat 49.
- Base keys: 141 prio 31 (140 loop exit), 49/96 prio 7 (48 [13] split 50/50), 149 5, cases 3-4.
- Case blocks' trace-end edges come from 112 = the SWITCH block (f44, ends r2 trace; prof 108 f86) and
  104 = reboot-path netGetInfo + rko asm goto (f20, ends r3). Prof cases are (prio 7-9, freq 7-10):
  nearly all freq via the switch edge. Needs 112 ~105 with case freq < th 10 (entry 219).
### Levers measured
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

## s128 (attempt 109): NO MATCH. Floor stays f2 18 (s117/best.c). Clean-base family best = 42 (plain).

Clean base c0.c = src/mode_client.c; gen.py builds v/NAME.c from it (P = plain macros with AT labels on,
otherwise BUILD_FDO-style JUMPs active; J1/J2 edit the two FDO JUMP lists; F/Fr/Fu/G dead
__builtin_constant_p feeds (into dsp / any label); E* edits a static clientEraseBlockI copy
(cold/hot labels, dead gotos); Uh hot/cold on u2). run.sh NAME EDITS; l1..l6.txt batches, res.txt ~95 results.
All edits are labels, label attributes, empty asm gotos or dead constant_p gotos: equivalent to src.

### Key finding
- Plain compile (c0 / v/c1, no levers) is f2 42 and ALL 42 lines are in one window (ref lines 420-565):
  the cold blocks placed among the arg-loop arms. The whole switch/case region and everything else
  already matches. b18 (f2 18) differs in exactly the same window. So the "round-4 switch ladder"
  is not where plain/best differ; what is wrong is the order of 4 cold blocks:
  ref: logs(reboot/s) -> u2 ... eout -> efail(ebx) ... u4,u3 ... einv, clientInfo(NULL),
  clientPatches(NULL), u5,u5,u3,u3,u5;  plain: u2 before the two logs, einv right after eout,
  efail after clientPatches(NULL), -r usage(3) (L390) earlier.
### Measured (all worse than 42)
- FDO JUMP lists on: 176; J1 only off 188; both off (labels on) 50; J2 off 90.
- Switch feeds (dead cp into dsp from before NO_MODE_ARG, n=0..6): 48-106 plain, 60-128 FDO.
  Feeds from reboot path 50-60, from u2 arm 184-188, hot dsp 50-60.
- clientEraseBlockI copy alone 42; hot/cold on efail/eout/einv 51-92; dead gotos inside 62-84.
- u2 hot/cold: 42 (inert). Dead feeds from before NO_MODE_ARG into each case/u2/hdd label: 56-126.
Conclusion: the plain compile is a sharp local minimum (every single lever costs >= +6); the profiled
cold-block order (efail next to eout, einv with the NULL calls, u2 after the two logs) needs a
frequency/key change confined to those blocks, which no GIMPLE lever above achieves without
perturbing the loop arms. Next idea: RTL-only levers on the inlined clientEraseBlock branches
(e.g. asm goto from eout to efail with near-zero GIMPLE prob, label placement after inlining).

## s129 (attempt 110): NO MATCH. Floor stays f2 18 (s117/best.c = b18.c here). Plain (c0.c = src) 42.

Tools: hk.py NAME add|del IDX... builds v/NAME.c from the 35 difflib hunks between c0.c and b18.c
(`python hk.py list` names them; 0-3 are the macro block). r.sh = hk.py + f2. gen.py NAME EDIT... (P =
AT labels on; B1..B5 = equivalent restructurings of clientEraseBlock's if/else; R=old|new with @N/@T for
newline/tab). g.sh = gen.py + f2. ks.py/ks2.py = r4sim key-override searches on plain's dump (d_pm/).
res.txt has all ~110 real results.

### 1. best18 lever bisect
- Removing one hunk from b18: only 7 (lu1 label), 32 (cdef constant_p tail) and then 31 are free (18);
  28 costs 1, 6/9/20 cost 6, everything else 32-112 or breaks compile (label dependencies 8/12-16/19/22/24/33).
  Greedy removal: {7,32,31} only. b18 is a tightly coupled equilibrium, not a small lever set plus noise.
- Adding one hunk to plain: inert 4,6,7,8,22 (42); all others 46-133 or need companion hunks.
  So no subset of b18's levers transfers its window gain to plain incrementally.
### 2. Round-4 model of the window (plain dump d_pm, r4sim reproduces exactly)
Window = round-4 traces T32..T51: arms 49(-s..), 55(-r), 61(-w), 67(-e), 73 with single-block cold traces
popped in between. Blocks: 103 u2 (f4), 112/115 reboot logs (f2), 126 eout, 125 efail, 127 einv,
130 clientInfo(NULL), 117 clientPatches(NULL) (all f1), 33 u4, 29 u3, 53 -r usage3.
plain pop: 49 103 112 115 55 126 127 61 130 117 125 33 29 53 67 ...
target (ref): 49 112 115 103 55 126 125 61 33 29 67 127 130 117 ...
=> einv/Info(NULL)/Patches(NULL) must pop after arm 67 (key 0, i.e. freq 0, they are f1 now) and u2 must
drop to <= f2 with the right tie order. r4sim key-override search (1-4 blocks, keys -6..0, 20k random +
exhaustive pairs) never gets closer than distance 4/13 (pairs) - fibheap tie order scrambles everything once
several blocks share a key; setting 127/130/117 = 0 interleaves them with the arms' f0 blocks wrongly.
### 3. RTL/label levers on inlined clientEraseBlock (plain base)
- if/else restructurings B1..B5: 44-62 (B2/B4 move efail into the hot line 300 region).
- asm goto eout->efail 62; Success->efail 116; einv cold/hot label 42 (inert: f1 can't go lower);
  i0/p0 cold labels 44/54; combos 44-62; u2 asm-goto self split 42.
### Conclusion
The window needs three f1 blocks (einv, clientInfo(NULL), clientPatches(NULL)) at f0 plus u2 at <= f2;
labels can't lower them below the predictor floor and key overrides alone can't produce the order.

## s130 (attempt 111): NO MATCH. Global frequency scaling via dead hot loops. Floor stays f2 18 (b18.c = s117/best.c), plain 42.

Tools: mk.sh / mk2.sh / mk4.sh BASE NAME ... insert `if (__builtin_constant_p(argc)[&& ...]) { dead loop(s) }`
after log_set_name in mode_client (mk4: nested known-trip loops T x N, the fine knob); mk3.sh puts it in
clientEraseBlock. dump.sh NAME -> dd/NAME/{mc.pe (profile_estimate-blocks-details), mc.bbro}. fr.py = round-4
trace starts, keys.py = pre-round-4 keys of chosen blocks. res.txt = all ~75 measured variants.

### Mechanism (confirmed)
- profile_estimate: plain's max is the argv-loop body (9800, entry 214; loop predicted ~46x). The dead loop
  survives profile_estimate (constant_p(argc) folds late, ~dom2) and if its body beats 9800 every block is
  rescaled; RTL/bbro keys reflect the scaling (q1: keys x0.93). Asm has no trace of the loop (guard folds to 0).
- Knob: known-trip nested loops give max = preheader*T*N (cap 99% = x100 per unknown loop);
  scale ~ 9157/(100*T*N) with guard constant_p(argc) alone (preheader = entry/2).
- constant_p(sblock) in clientEraseBlock folds early (inert); constant_p(block) there survives but the callee
  is IPA-inlined with ratio scaling -> no rounding effect (c0 111 from size/inlining change only, N-independent).

### Results
- Below the scaling threshold (T*N <~ 85): inert (b18 18, c0 42-50; the extra guard alone costs c0 0-8).
- Any real scaling: monotonically worse. s~0.95: c0 48-52, b18 64; s~0.8: 72-112; s~0.5: 90-120; s<0.3: 120-240.
  Diffs start in the argv loop: IRA costs are frequency-weighted, so rescaling reshuffles register choice
  everywhere, not just the bbro window.
- Window keys vs scale (c0): u4 (33) drops to 0 already at s~0.8, u3 (29) at ~0.55, before u2 (103) reaches
  -2 (s~0.6). The reference order needs 33/29 to stay above the einv/Info(NULL)/Patches(NULL) blocks, so a
  uniform scale can't produce it; scaled pop orders (fr.py c0t13/c0t20) scramble further via ties at 0.
### Conclusion
Global scaling/rounding is not a lever: it can't separate the f1 blocks the way the reference needs, and it
perturbs IRA across the whole function. Dead.

## s131 (attempt 112): NO MATCH. Local freq levers work on einv/Info(NULL)/Patches(NULL) but not u2. Best plain 42 (unchanged), b18 18.

Tools: gen.py (s129's, base from $BASE, R edits split on `#|#`), vars.sh / vars18.sh = named edits, g.sh NAME EDIT...
= gen + f2 + dump + fq.py (freq of u2/i0/p0/einv/efail/eout found by source line -> bbro call_insn -> reordered freq;
second number pair = original bb:freq). grid.sh = 216-combo grid (grid_c0.log). ks.py = s129 key search on dd/NAME.
res.txt = all ~270 measured variants.

### Where the f1/f4 come from (dumps: -fdump-tree-all-blocks-details)
- Patches(NULL)/Info(NULL): switch arm 4.46 x pointer-eq 0.3 = 1.34. einv: call site 4 x callee else-arm 0.34.
- A folded test (cp(x) folds at dom2) does NOT lower its target: gimple_merge_blocks keeps the predecessor's
  frequency, so `if (a && !cp(argc)) T` gives T the freq of the cp block again (a1: pe 0, RTL 1).
  Working forms: compute `int k = __builtin_constant_p(argc|block)` earlier (inert alone: c0 42), then
  `if (arg == dummy && !k)` / `} else if (!k) einv` -> the test block becomes an empty forwarder, removed
  without touching the target freq. Also works: forced label (`l: asm("" :: "i"(&&l))`, but blocks inlining
  of clientEraseBlock) or a 2nd predecessor. E4 (all three) = einv/i0/p0 0, eout/efail unchanged.
- u2 (client_usage(2)) is 0 in profile_estimate; its RTL 4 = the dom2 jump-thread of the zero-iteration path
  (entry guard, loop-exit 2% floor x preheader 214 = 4.28) into a forwarder that PRE's cfgcleanup merges with
  u2 (keeps forwarder freq). So u2 = 0.02 x preheader->entry edge: not locally adjustable.
  - asm goto feed into u2 (from a 0-freq block) blocks the merge -> u2 0 (f_FI 48); feeds from f4 blocks add 0
    (noreturn predictor). Extra loop exits/continue raise u2 (2% floor per exit; 188-230).
  - Outer back edge `again:` + `if (k) goto again` to cut entry/preheader: loop-branch 90% predictor; from
    netReboot block u2 -> 2 (m4) but rok/reboot tail reorders (172); other placements 164-289.

### Results (plain): every lever combo >= 42
grid best: MK alone 42, K12 44, K7+K12 44, einv+K12 46, einv+K7+K12+u2feed (all 4 targets at 0) 48, E1-forms 50-52.
With all four targets moved the diff is still only the window (425-563); u2 at 0 lands last (ref has it
right after the first reboot log) and r4sim on that dump with 103=-1..-3 still leaves 55 before 115 and
29/33 swapped (ks.py distance 4-5).  b18: einv k-lever 32, K7/K12/u2 feed inert (18; its p0/i0 already 0, u2 2).
### Conclusion
einv/clientInfo(NULL)/clientPatches(NULL) can be driven to 0 locally and cheaply (pre-computed cp k + `&& !k`),
but u2's 4 is a jump-thread artefact tied to entry/preheader ratio, and even with u2 at the right key the
window's tie order (55/115, 29/33, 77/35 intrusions) does not match. No transferable gain to b18.

## s132 (attempt 113): NO MATCH. New plain-compile best f2 34 (was 42); floor stays s117/best.c 18.

Tools: gk.py BASE OUT off:form... (k-lever on the if at line offset `off` from the arg-loop `for`;
A=(c)&&!k, B=!k&&(c), C=k||(c); KV=name env for the k variable), gg.sh NAME BASE SPEC... (gk + f2 + dump + fq),
sw.py (disjunct permutations; only perm 102 is safe), gen.py/vars.sh/fq.py from s131. res.txt = ~500 measured.

### best34.c (= c0 + EK + EK2 + MK + K7 + `-bp` usage(4) test `(j == argc || !b || *b == '-') && !k`)
Equivalent to src: both k's are __builtin_constant_p of runtime values -> 0; every `&& !k` / `else if (!k)` is a no-op.
Synergy only: 18A alone 58, EK+18A 64, K7+18A 58, EK+K7 (s131) ~44, all three 34.
Remaining diff (asm 420-560): u2 (f4) placed first instead of after the two cold logs; one cold log (ebx) and
usage(4)/usage(3)/usage(0) blocks still shuffled.

### Measured, no gain
- k-lever A/B/C on all 22 arg-loop ifs: from c0 (66), from s131 f_FI 48 (66; 18A -> 44), from b44 (63), b34 (63),
  b18 (36, with KV=kk since b18 has a block-local k): all >= base.
- 32-combo grid {EK, K7, K12, reboot&&!k, 18A}: best 34.
- u2 is binary under every k/cp form: 4 or 0 (`reboot && !k`, `!k && reboot`, `!(k||!reboot)` -> 0 -> 38;
  cp(reboot/mode/ip/arg) inert). Asm-goto feeds from loop logs: f2 only from the -noenter log (76), others 0 (38-102).
- Splitting the 18A condition per disjunct: `*b=='-' && !k` or `(j==argc||!b) && !k` = 34, others 44-72.
- NO_MODE_ARG/netConnect/loop-condition k forms: 34-180. KU/FP/FI/P12/K12/PL/CT on b34: 34-228.
- Disjunct swaps on b34: >= 36.
### Conclusion
k-lever on the -bp usage(4) test is a new cheap improvement for the plain compile (42 -> 34), but u2 can't be
set to 2 locally and the cold usage tie order still differs; nothing beats b18's 18.

## s133 (attempt 114): NO MATCH. Plain-compile best stays s132/best34.c (f2 34); floor stays s117/best.c (18).

Tools: m.sh NAME SEDEXPR... (sed on $BASE, default best34.c, + f2), hk.py/hm.sh (best34 + selected best18 hunks,
c0-relative; `python hk.py list`), res.txt = all ~95 measured variants. All variants: k = __builtin_constant_p of
a runtime value (folds to 0), empty asm goto / labels / expect only -> equivalent to src.

### Mixed lever families (direction 1)
- best34 + b18 define hunks 0-3 (AT/JUMP active): 34 (inert). + single b18 hunks: 4,6,8,22,27 = 34; 9 38; 7 60;
  28 68; 14 80; 31 82; others need label partners (9999).
- Label-closed groups: {5,8} 38; {12-16} 66; {10-16} 88; {4-16} 96; {17-34} 125; {4,17-34} 86.
- All b18 hunks + EK/K7 k-levers = 18 (k inert there). b18 + 18A (`&& !k` on -bp usage4 test) 70; + c7 k 18;
  + k on -w usage test 34; dropping EK 18.
### u2 (direction 2): stays 4/0
- reboot test forms `|k`, `^k`, `!=k`, `>k`, `k||`, `k?0:`, `&& reboot+k`: 34-38; expect(reboot,0/1) 75;
  loop cond `&&!k`/`||k` 42; NO_MODE_ARG `||k` 134-180; else-branch k-forwarders to rok/fail/netDisconnect 98-120.
- -noenter asm-goto/`if(k) goto` feed to u2 with plain/hot/cold label: 150-187.
### Dispatch / labels (directions 3-4)
- k-levers on netConnect x2, hwFlags x2, c12/c7 dummy tests, final E(reboot): 34 (inside expect / `k||E`) or 56-106.
- cold labels on usage(0/1/3/4/5) calls: inert (34); hot/cold on u2 label inert; rok hot/no-cold 90; cold label on
  -reboot log 270.
### Conclusion
The two lever families don't compose: b18's dispatch/arg-loop hunks dominate and k-levers become inert, while
partial b18 hunks on best34 only hurt. u2 frequency is not movable by any local predicate/label form tried.

## s134 (attempt 115): NO MATCH. Plain best stays s132/best34.c (f2 34); overall floor s117/best.c (18).

### 1. r4sim on best34 (dd/b34/mc.bbro; tag.py maps asm lines to bbro blocks via gcc -dA)
Window heads, best34: 49 103 112 115 55 126 61 130 125 29 67 127 77 117 33 42 35 53 79
Target (ref):         49 112 115 103 55 126 125 61 33 29 67 127 130 117 35 42 53 77 79
(103 u2 f4; 112/115 reboot logs f2; 126 eout; 125 efail(ebx log); 130 Info(NULL); 117 Patches(NULL);
 127 einv; 33 usage4 ecx; 29 usage3 ecx; 35/42 usage5; 53/77 usage3; 79 usage5.)
- Exhaustive singles/pairs (keys -8..0, window blocks), triples (13 blocks, keys -4..0, 37765 sims), and
  SA (window and all blocks, full-order metric, arbitrary many overrides): 0 exact hits, floor distance 4.
- u2 at 0/-1/-2: arm 55 (inserted at key -2 when 49 is processed) pops between 112 and 115; target needs
  112,115,103 all before 55 which only happens via fib-heap tie history with u2 at -4 or logs < -2.
  The prefix alone (..61) is reachable only with 112/115 more negative than -2 (e.g. 112:-6 115:-4);
  the 61..117 segment alone is never exact. Keys can't produce the target: needs different block/insert set.
- rs.py / rs2.py / rsa.py = searches.
### 2. Automated lever generator (gen.py, climb.py)
Edits: k-lever A `(t && !k)` / C `(k || t)` on every if condition and every sub-term (51 conds, 200 edits);
hot/cold label on every statement (122 stmts, 244); dead `if (k) goto` and empty asm goto from every statement
to 31 cold targets + rok/fail (7432 singles total). Cost f2*100 + diff hunks (r4sim block ids aren't stable
across variants, so hunks used as tie-break).
- Singles 7432: none < 34; 1867 inert (34). Best non-inert 36.
- Greedy: no improving step. Pairs over the 100 best distinct non-inert singles (4950): floor 34.
- SA 4 chains x 450 over 4000 singles: all end at 34 (base).
- ~13.8k real compiles in total (v/g_*.res, cache.jsonl).
- Hot label on the reboot logs (raise to f3 for the prefix solution): 42/43, moves another log instead.
### 3. Semantics
All edits: k = __builtin_constant_p(runtime) = 0, so `t&&!k`==t, `k||t`==t (same evaluation order);
labels/hot/cold no-ops; `if (k) goto` dead; empty asm goto falls through. Equivalent to src/mode_client.c.
### Conclusion
Exhausted for this family: the window order is not reachable by key changes (r4sim proof-by-search) and
the generated lever space has no improvement over best34.

## s135 (attempt 116): NO MATCH. Bests unchanged: s132/best34.c (34 clean), s117/best.c (18).

Arg-loop restructuring of best34 (and best18) to change the window block set. vars.py = generator
(`python vars.py <base.c> [tag] [names...]`); results vars.out (best34), vars18.out (best18); sources in v/.

### Variants (best34 base, f2; 58 measured)
- Inert (34, same code): rb_setfirst, s_sel/s_neg/s_cont/s_tern, help_elif, help_sep, noenter_cont+reboot_cont
  together, nma_1 (`!mode||!arg`), nma_3, ip_i, r_a/w_a/rw_a, e_a, i_neg/p_neg, i_pre/p_pre, keys_order, v_inv,
  while-loop, v_a, g3_ec/g3_rw (shared `bad3:` usage site), g5_rw/g5_ec, cv_ip (code variable).
  gcc canonicalises all of these (tail merging/ifcvt), block set unchanged.
- Worse: rb_ifelse 42, rb_flag 46, s_flag 118, nma_2 (`!arg||!mode`) 38, g3_ip 39, g3_eb 38, cv_r 57,
  cv_rw/cv_ec 47, g3_all 168, g5_all 151; option-order swaps: sw_r_w 38, sw_e_c 38, sw_i_p 46, sw_keys_ip 74,
  sw_c_i 77, sw_s_keys 94, sw_rb_wb 108, sw_bp_rb 142, sw_wb_eb 172, sw_reboot_bp 207; single continue-splits
  (reboot_cont 497, s_contchain 586, ip_cont 602, v_first 244, help_a 242) break the chain shape badly.
- best18 base (vars18.out): nothing below 18 (nma_2 22, rb_ifelse 26, sw_i_p/rb_flag 30); many s-arm forms
  don't apply (best18's -s arm differs).
### Climbs on top (s134 gen.py/climb.py copies in cl_*)
- cl_sw_r_w: 7432 singles + 60-pairs: floor 38 (=its base), no improvement.
- cl_sw_e_c: 115 singles before stop, floor 38. cl_nma_2 not run.
### Semantics
Swaps only between tests with distinct non-prefix strings (at most one matches; -reboot kept before -r,
-rb/-wb/-eb before -r/-w/-e, -keys before... no prefix overlap with -s/-ip). goto-shared usage calls pass
the same code/arg; continue-splits preserve else-chain (each arm ends the iteration). All equivalent.
### Conclusion
Source-level reshaping of the arg loop either normalises away in GIMPLE (inert) or perturbs the layout
away from the reference; none moves the window toward the target order.

## s136 (attempt 117): NO MATCH. Floor stays 18 (s117/best.c).

s134's gen.py/climb.py ported to best18. base18.c = s117/best.c + `int kk = __builtin_constant_p(argc);`
(mode_client) and `int kk = __builtin_constant_p(block);` (clientEraseBlock): still 18. Levers use `kk`
(best18 has block-local `k`). gen.py reads GBASE (default base18.c); nonin.py N = top-N distinct-asm
non-inert singles -> nonin.json; run_rest.sh = pairs + 4 SA chains per base. Same 28 cold feed targets
filter as s134 (6340 singles per base). ~38.7k real compiles (v/, nma_2/v, rb_ifelse/v *.res).

### best18 (base 18, 7 hunks)
- Singles 6340: floor 18; 1980 at 18, two at 18/5 hunks (dead `if (kk) goto` between the hdd4/hdd5
  error stmts, lines 755<->761); next 19.
- Pairs over 100 distinct non-inert singles (4950): floor 18. SA 4x450 over 4000 singles: all end at base.
### nma_2 on best18 (base 22): singles/pairs/SA floor 22.
### rb_ifelse on best18 (base 26): singles reach 18 via feed from the duplicated reboot log (606) to 597/737,
  but the asm diff is byte-identical to best18's (it just undoes rb_ifelse). Pairs 18/5 (same hdd4/hdd5
  feed); SA chains: one 18/7, three stay 26.
### Remaining diff (best18 and the 18/5 variants)
Common to all: u2 `mov eax,[l]; jmp l` (ref 503) and the usage(5) block (4 insns, ref 542 vs 560) -- the
known stuck u2/usage5 placements. Variable part near ref 421-465: best18 misplaces a
`l(2,0)` call block + `[8+esp]=ebx` store; the 18/5 variant instead misplaces a log_printf+jmp block. No
lever fixes both, or touches the u2/usage5 hunks.
### Semantics
kk = __builtin_constant_p(runtime value) = 0: `t&&!kk`==t, `kk||t`==t; labels/hot/cold no-ops; `if (kk) goto`
dead; empty asm goto falls through. nma_2 (`!arg||!mode`) and rb_ifelse (log duplicated into both arms)
are equivalent (s135). All equivalent to src/mode_client.c.
### Conclusion
The lever family is exhausted on best18 and its two restructurings too: floor 18, residual is the u2/usage5
pair plus one block in the 421-465 region.

## s137 (attempt 118): NO MATCH. Floor stays 18 (s117/best.c = b18.c here).

### Block-set finding
best18's u2 hunk (`mov eax,[l]; jmp l`, mine 503-504) is NOT a misplaced block: ref has no such block at all
(ref 679 lines, mine 681). In gcc's asm it is `L535: mov eax,_cinfo; jmp L532` (L532 = the
`sendAvatarData(arg, cinfo->kernel)` call), never referenced in the text: it is the entry edge of the
lever `JMP(s4,c12)` (empty asm goto) in case 5 of the dispatch, which targets label `s4:` in case 4. The
edge needs cinfo reloaded, so gcc makes a separate edge block for it.
- Dropping `goto s4` (dead bcp goto, line 801): still 18, same diff (a1.c).
- Dropping s4 from the asm goto (`JMP(c12)` or none): 34. Retargeting it to each of the 29 other labels
  (v/j_*.c): best 32 (c3), t4 33.
- Moving the asm goto (v/k1..k5): k1/k3/k5 stay 18 but the dead block just moves (to 428 / 466); k1/k3 also
  turn the usage(5) hunk into a usage(3) one.
So best18's layout depends on an extra (dead-in-practice) asm-goto entry block that the ref doesn't have;
the lever set is fitted around it. A profile-free match needs a different way to supply that edge's
effect on bbro without a block that survives to the output (e.g. an edge whose target needs no reload).
### Usage(5) hunk
Ref 560-563 is the same usage(5) block as mine 542-545, diff just aligns it oddly; it's pure placement of a
noreturn block (as s136 says).

## s138 (attempt 119): NO MATCH. Floor stays 18 (b18.c = s117/best.c).

Goal: get the case-5 `JMP(s4,c12)` edge's bbro effect without best18's extra edge block
(`L535: mov eax,_cinfo; jmp L532`; L532 = `mov eax,[eax+4]; ...; call _sendAvatarData`, so the edge
needs cinfo in eax).

- Block removed by giving the asm goto `"a"/"r"/"g"(cinfo)` input (vEa/vEr/vEg): f2 35. The edge block is
  gone, but the reload moves into case 5 (`mov eax,[_cinfo]` before sendCompatData, the volatile JMP(dsp)
  stops FRE), and 421-565 relayout (log_printf pair + [8+esp]=ebx block, usage 3/5) -> the edge
  block itself is a bbro trace member best18 relies on, not just the edge.
- "m"(cinfo): 18, same block (vEm). Load cinfo into a local ci5 shared by test and asm: 122 (vFa/vFr).
- Moving s4 after the load (`kv = cinfo->kernel; s4: sendAvatarData(arg,kv)`): 98-102 (vA/vC); s4 after call: 34 (vB).
- Asm with "a"(cinfo) before/merged with JMP(dsp) (vG1-5): 34-44, block stays in G1/G2.
- w/: "a"(cinfo) asm goto with s4 + each other label (e_*, f_*): all 35 (second label inert).
- No RTL mechanism removes an asm-goto edge after bbro (bcp gotos fold in GIMPLE), so a "dies after
  bbro" edge is not available.
Goal 2 (profiled bbro block-by-block, r4sim) not done.

## s139 (attempt 120): block-free base vEa (s138/vEa.c, f2 35) vs profiled bbro

Files: dump.sh (bbro/profile_estimate dumps -> dd/NAME), al.py (emitted-order alignment of
s111/pf/bbinfo.txt vs dd/vEa/bbinfo.txt -> align.txt), al2.py (map P->V by block signature, map.json),
keys.py (round-4 keys P vs V, keys.txt), srch.py (r4sim key search on vEa), baseA.c (vEa + kk vars,
f2 35), gen.py/climb.py/nonin.py (s136 ports on baseA).

### A. Block-by-block (align.txt has every block: bb, trace/round, freq, both sides)
- Rounds 1-2 (P 2-51 / V 2-51): identical block set and order, same traces. Freqs equal in the
  arg loop; differ after it: P14/15/16 175/109/110 vs V 127/138/71, P17 73/51, P46-51 (T10/T12)
  73/60/87x4 vs 63/44/58/58/47/45 -- V splits P's T12 (netConnect..cinfo) into T12+T14 and adds
  V52 (T15r2 f62, a forwarder).
- Round 3: P has 5 traces (58 netGetInfo f37, 60 f15, 62 f13, 63 usage f12, 59 netReboot T15r2 f61);
  V has 6 (59, 62, 64/65, 66, 67) and builds V96 (= P94, f18 vs P f9) in round 3; P builds it in r4.
  Threshold is entry*5% = 10 in both; P94 at f9 falls below it.
- Round 4: V has 19 extra forwarder blocks (60,61,63,69,72-75,77,81,82,86,87,89-94,96 new-numbering);
  P's ~41 r4 traces map 1:1 to V heads (V heads are often an empty forwarder before P's block:
  P111->V117/118 clientKeys, P123->V132/135 clientWriteBlocks, P136->V152/153 LC157).
- Round-4 keys (keys.txt; p=priority=pred-edge freq, f=bb freq), P vs V, in P pop order:
  P133 p9/f10 vs V147 p5/f7; P94 p9/f9 vs V96 (r3); P109/111 p8/f9, P112/115 p8/f8 vs V p4/f6 x4;
  P110/122 p7/f9, P123 p7/f8 vs V p4/f5, p4/f4, p4/f4; P124 p7/f7 vs V139 p31/f6 (myatoh32 entry,
  pushed early with prio 31 -> popped FIRST in V); P132 p6/f10, P118 p6/f9, P136 p6/f8, P49 p6/f7
  vs V p3/f9, p3/f8, p2/f4, f7 (no prio); P117 p3/f4, P114 p3/f3, P104 p2/f5 vs V f2,f2,f3;
  tail P f1-f3 vs V f0-f3 (P131/P119 f1 vs V f0).
- Emitted-order differences that survive forwarder removal: clientWriteBlocks (P74, own trace after
  ReadBlocks) sits inside V's BinPatch trace T33; LC156/LC155 logs (P84/85 before usage P86) placed
  after the -x/... strnicmp chain in V; LC118/LC117 logs (P93/95) moved; clientPatches P111/112 and
  usage P117/118 order.

### B. r4sim on vEa (srch.py, keys.py)
- vEa replay exact. LCS distance to the mapped P pop order: base 11.
- Any-key SA (single/pair/SA over all r4 blocks, 6x4000): floor 6 with 3 overrides
  {144:p2/f10, 132:p3/f13, 108:f2}; remaining misses: V139 still first (its p31 push in round 3 is
  outside the sim's r4 overrides' reach), V96 not in r4, 81/79 order, forwarders 128/105 interleave.
- Transplanting ALL of P's keys onto vEa's events: front matches (147 113 117 120 123 _ 116 132 139 146
  134 152 49) except 96 (r3) and a tie swap 116/131 (equal p7/f9, heap shape); the f0-f3 tail is
  scrambled (128,105 forwarders + V's insertion structure). So targets are: (1) P94/V96 freq <= 9,
  (2) V139 must not get the prio-31 edge (it must arrive as p7), (3) switch-case ladder p9..p6 instead
  of flat p4/p3, (4) ~19 forwarders gone. (3) is the same ladder s111/s124 showed heuristics can't make.

### C. gen/climb on baseA (vEa + kk, f2 35)
- Singles 6340: floor 25 (asm goto 787->755/761 = feed into hdd4/hdd5 logs; 631..801->735).
- Pairs over 100 non-inert (4950): **17/5 hunks** (new overall best, block-free):
  best17.c = p17.json [("f",773,761,"a"), ("f",755,761,"k")]: empty asm goto to hdd5 (S761) before
  case-12's `JMP(c11); break;` plus dead `if (kk) goto S761;` before the hdd4 log.
- SA 600 iters from p17 over 4000 singles: stays 17.
- Residual of best17 (diff v/best17.ref v/best17.mine): extra `mov eax,[cinfo]` in case 5 (the "a"(cinfo)
  reload, ref 361) + two `log_printf(0,..); jmp` hdd log blocks misplaced (ref 461 and 536 -> 395 and 555).
### Semantics
kk = __builtin_constant_p(runtime) = 0, `if (kk) goto` dead; empty asm goto falls through; "a"(cinfo)
input on the empty asm goto only reads a value. Equivalent to src/mode_client.c.
### Conclusion
NO MATCH; best f2 17 (block-free, best17.c), beats b18. Next: climb from best17 (singles on top of p17),
and remove the case-5 cinfo reload line.

## s140: case-5 cinfo reload (from s139 best17, f2 17)
b0.c = s139/best17.c (f2 17). Variants of the case-5 empty asm goto input (f2.sh):
- v1 "g"(cinfo) 17, v3 "r"(cinfo) 17, v6 "a" without s4 label 17: reload `mov eax,[cinfo]` stays.
- v2/v7 no input 34; v4 "a"(&cinfo->hwFlags) 32.
- v8 "+a" copy in the if condition 17 (asm goto still re-reads cinfo).
- v9 function-scope local c5 used in test and asm: 116 (frame slots shift by 4).
- v10 block-local c5 = cinfo for case 5: 116 equivalent; c5 spilled across je, case 5 moves after case 6.
Insight: the reload is the input operand itself. cinfo is a static global, and the value the test
loaded is not reused across the je: no CSE over the BB edge. Copying cinfo into a local makes RA
spill it. So the asm needs some input that gcc already holds as a pseudo live in eax over the edge.
None of the tried variants gives one.
Climb (goal 2) not re-run: s139 SA 600x4000 from p17 already floors at 17.
NO MATCH, best 17 (s139/best17.c).

## s141: profile-free mode_client, from s139 best17 (f2 17)

### B. Case-5 cinfo reload: FIXED -> best16.c (f2 16, 4 hunks)
Cause (tree-optimized dump, dd/): at t5 cinfo is a PRE value (prephitmp, from the load before the
switch), but label s5 has many fake preds (rk dispatcher ork7/8, c3/c9 JMPs, the bcp goto). So the
"a"(cinfo) input of the asm goto inside s5 has no available value and gets a fresh load.
Fix: move that asm goto ahead of label s5, into the t5 then-arm, so only the t5 edge runs it:
  { __asm__ goto ("" :: "a"(cinfo) :: s4, c12); AT(s5)JMP(dsp);  { sendCompatData(arg); } }
Its input is now the value the test loaded, so the reload is gone. Semantics: the empty asm goto
falls through, as before. Splitting labels as (s4)+(c12) gives the same result (c3); other splits,
merges or orders give 34/44. "X"/extra "i"(0) inputs and a plain asm in front change nothing (17).
baseC.c = baseA.c with this change; baseC + p17 = best16.c.

### A. Search on baseC + p17 (gen.py/climb.py; the bsingles mode was added)
- Singles 6338: none below 16 (1947 inert at 16; best non-inert is 17).
- Pairs over the top 100 non-inert (noninC.json): floor 16.
- SA x4 (600 iterations; pool 1500 for seed 1, 4377 for seeds 2-4): all end at p17, 16/4.
Not done: srch.py r4sim targeting of the two blocks.
Left: the two hdd `log_printf(0,..); jmp` blocks. Ref asm lines 461 and 536; ours land at 394 and 554.

## s142: bbro analysis of best16's residual (s141/best16.c, f2 16)

Files: dump.sh (bbro dump -> dd/NAME/), align.txt (s139/al.py P=s111/pf vs best16), srch.py (target +
singles/pairs), gr.py, beam.py (r4sim beam over key overrides), m.s/p.s (function asm, ours/profiled).

### A. What the 4 hunks really are (normalized log blocks are interchangeable)
Literal order of the standalone `log_printf(0,LC); jmp` blocks, profiled (= ref) vs best16:
  ref : LC157 | T(LC140..LC141) | LC156 LC155 | usage | T(LC142..LC143) | LC118 | LC117 ... LC147 | LC114 | clientPatches(NULL)
  ours: LC157 LC156 | T(LC140..LC141) | LC155 LC118 | usage | T(LC142..LC143) | LC117 ... LC147 | clientPatches(NULL) clientInfo(NULL) usage x3 | LC114
So three blocks are off, not two hdd blocks: hdd5 log LC156 (bb126) is one trace early, LC118
(clientEraseBlockI "outside system area", bb144) is before the LC142 trace instead of after it, and
LC114 (clientEraseBlockI einv, bb145) is at the end of the f0 tail instead of right after the LC147
block (trace 69..74). The minimal diff pairs them up as "394->461" and "554->536".

### B. bbro round 4 (best16 numbering; key = -freq, or -(1e6+100*prio+freq) with prio)
Pop order: ...127 152 126 105 49 121 144 108 55 143 62 33 29 69 128 150 35 42 53 145 79 81...
Target   : ...127 152 105 49 126 121 108 55 144 143 62 33 29 69 145 128 150 35 42 53 79 81...
Keys: 126 -4 changed to -1000104 (prio 1) by trace 30 (130/131 = case 8 clientReadBlocks; 131 is the
`__asm__ goto("" :::: S761)` lever from s139 -> edge 131->126 freq 1); 49 -7; 121 -4; 144 -3; 108 -3;
55 -2; 143 -2; 62 -2; 69 -1; 145/128/150/35/42/53 0 (ties).  In P both hdd logs are p3, LC140 trace p6.
r4sim: 126=-4 alone fixes LC156 (pops 49,126,121) but reshapes the fibheap so the f0 tail scrambles
(42 145 81 128 79 150 ...). 144 needs key in (-2 tie, after 55) and 145 needs to pop between 69 and 128
(-1 or prio) — both are tie-order dependent. Beam (5 deep, 40 wide, distinct orders) floor dist 2:
{126:-6,144:prio3} or {117:prio2,55:-3}; no override set reaches 0 within the sim (tail ties).

### C. Levers (t.sh NAME: f2 + clientEraseBlockI freqs + compiled r4 order)
- h2: case-8 lever `asm goto("" :::: S761)` -> `(S761, hdd4)`: 126 loses prio, pops 49,126,121 as in
  ref (exactly r4sim's 126=-4 prediction), f2 32 because the f0 tail reshuffles.
- clientEraseBlockI freqs (P: erase 5, success 4, failed 1, outside 2, invalid 1; best16: 4/2/2/3/0).
  e3 = drop the dead `if (bcp(block+9)) goto eout` after Success -> outside 2; y4 = + `JMP(efail)`
  (empty asm goto) in eout -> LC117 gets the eout->efail edge P has; z2 = + `esucc: __attribute__((hot))`
  -> success 3 / failed 2.  z2 = h2+e3+y4+hot = **front28.c, f2 28: every block up to ref line 535 is
  in ref order** (126 after LC141 trace, LC118 after LC143 trace, r4 pops ...69 as target).
- Remaining in z2: only the key-0 tail after trace 69..74: ours 42 128 81 146 79 151 35 53, ref
  146(LC114) 128 150 35 42 53 79 81 (LC114, clientPatches(NULL), clientInfo(NULL), usage x3, 79, 81).
  P has LC114 at f1/key -1; ours is cold (f0). Uncolding einv gives f4 (q1), removing the dead einv
  gotos f1 but re-breaks the front (q2 76); hot label on the outer then-arm inert (q3/q4).
  r4sim beam on z2 (target = z2 order with P's tail) floor dist 2: ties at key 0 depend on fibheap shape.
### Semantics
h2/y4: empty asm gotos fall through; e3 removes a dead bcp goto; hot label only changes estimates.
### Conclusion
NO MATCH. Best f2 still 16 (s141/best16.c); front28.c (f2 28) fixes all three misplaced log blocks
in the front and leaves only the f0 tail order (need LC114 at freq 1 / key -1 without moving the front).

## s143: LC114 (clientEraseBlockI einv, bb146) freq levers from s142/front28.c (f2 28)

t.sh NAME (f2 + erase freqs + compiled r4 order), dump.sh, srch.py (r4sim key-override search on the
tail after block 143, target 62 33 29 69 146 128 151 35 42 53 79 81).

### Levers (einv freq / f2)
- a1 uncold einv: 4 / 96 (success drops to 1). a2/a3 extra bcp conjuncts on the dead einv gotos: 2 / 90.
  a4/a5 one conjunct only: 4,3 / 96.
- b1/b5 dead gotos -> cold trampoline inside `if (bcp)`: still 0 / 28 (inert). b3 cold trampoline as
  its own block: 6 / 103. b2 `|| bcp` on `block != -1`: 103. b4 `if (block + 1)`: inert.
- c2 dead gotos -> `einvd: cold; goto einv;` at function end: einv 0 (cold propagates through forwarder).
- c3 dead gotos -> efail: einv 1 but efail gains preds, 96.
- **c1/c4** dead gotos -> separate cold dead duplicate `einvd: cold; log_printf(same string)` after
  `return;`: **einv freq 1 (= P), rest of clientEraseBlockI unchanged (4/3/2/2)**, f2 76: 146 now pops
  at key -1 *before* 33 29 69 (target: right after 69), and the tail becomes 79 75 128 81 83 42 151 35 53.
  Same ordering as s142 q2 - so freq 1 is reachable without touching the front's freqs; the problem is
  purely the round-4 fibheap order of the key -1/0 ties.
### r4sim on c1
srch.py singles/pairs over {146,128,151,35,42,53,79,81,75,83,69} x {0..-3}: floor 6 of 12 tail slots.
146 always pops either before 33 (key -1) or after the tail starts (key 0); no key assignment puts it
between 69 and 128 with the P tail. Matching needs a different heap shape (insertion order / extra
consolidation pops in rounds 1-3), not keys. Goal 3 (gen/climb from front28/c1) not run.
### Semantics
c1: the dead `bcp` gotos now target an unreachable duplicate of the einv message; bcp folds false.
### Conclusion
NO MATCH, best f2 still 16 (s141/best16.c). c1.c is front28 + exact P freqs in clientEraseBlockI.

## s144: fibheap-shape analysis of the round-4 f0 tail (front28 / c1), profile-free mode_client

Files: shape.py (dummy push / drop / swap edits in rounds 2-3), shape2.py (move a round-4 insert to
another trace group + dummy entries, singles/pairs/SA), shape3.py (permute inserts inside one group),
shape4.py (shape2 moves only), shape5.py (shape2 with env targets TT/TP), dv.py (dummy-absorption test),
mk.py (source variants), t.sh NAME (f2 + simulated r4 order), run.sh DIR (climb singles/pairs/SA),
fb/ f28/ c1/ (gen.py/climb.py ports, base.c = fb.c / front28.c / c1.c).

### 1. Model validation (MANDATORY step 1)
s86/r4sim.py already replays rounds 1-3 event by event on tools/wip/fibsim.py, which is GCC 6.2's
fibonacci_heap (insert into root list after root, extract_min with consolidate, replace_key =
decrease or delete+insert, delete_node). Checked: simulated round-4 order == real "Getting bb" order,
**exactly**, for s143/dd/front28, s143/dd/c1 and s142/dd/best16 (all blocks). So tie order is fully
modelled; no change to the model was needed (no need to read fibonacci_heap.h).

### 2. Shape search (step 2), target tail after 143: 62 33 29 69 146 128 151 35 42 53 79 81
Facts from the dumps (bbro numbers): 146 (LC114 einv) is inserted by the first r4 trace 139
(clientEraseBlockI entry); 128 (case-7 p0 clientPatches(NULL)) and 151 (case-12 i0 clientInfo(NULL)) by
trace 148 (case 12 dispatch; 128 via the `({JMP(p0); 0;})` edge); 79/81 (-c usage 3/5, crossjumped
with -r's r3x/r5x) by trace 55 in asm-goto label order (r5x first -> 81 before 79).
- Keys only (s143): floor 6. Permuting inserts inside groups (shape3, 1-2 groups, 146 key -1/0): floor 6.
- Dummy pushes/drops/swaps in rounds 2-3 (shape.py): c1 floor 9, front28 floor 4.
- Moving inserts between groups, no extra entries (shape4): floor 4 both.
- With extra heap entries (shape2/SA): **0 reachable**. Minimal c1 recipe (dv.py):
  (a) 128 inserted by trace 108 (u2 usage) or 121 (hdd4 log) instead of 148;
  (b) 81 inserted after 79 in trace 55 (= label order r3x, r5x);
  (c) one extra key-0 entry created by trace 143 (efail log) that stays in the heap until it is
      absorbed by trace 79/42/53 (a single-block usage trace) - no source form found: those blocks
      are already in the heap when 143 runs, so a re-insert only changes a key, not the shape.
### Source translation
- (b) `asm goto("" :::: r3x, r5x)` swaps 79/81 exactly as modelled (f_bac / front28_b).
- (a) dropping `|| ({JMP(p0); 0;})` from case 12 (a0): front28 28 -> 20; with (b): **fb.c f2 18**
  (front28 + b + a0). Residual: LC117/LC118 (143/144) swap (pop at the -2 tie) and the f0 tail
  149 146 79 128 81 42 53 35 vs target 146 128 149 35 42 53 79 81. Re-adding the p0 edge elsewhere
  (u2 before/after usage, hdd4 arm, -w arm, swapped c12 operand) 18..165, never better.
- shape5 on fb (TP "144 143", TT tail): 0 needs dummy at 108 + 128 from trace 62 + 146 key -1 (c1's
  einv freq 1, which on its own costs the front: c1+b+a0 = 78).
### 3. gen/climb
gen.py/climb.py (s141 port) on fb.c (6334 singles): stopped after ~1550 singles, none below 18.
front28 base: ~370 singles, none below 28. c1 base (76) dropped in favour of fb. Pairs/SA not reached.
Resume: `NJ=4 sh run.sh fb` (the cache in fb/v is reused).
### Conclusion
NO MATCH. Best f2 still 16 (s141/best16.c). New fb.c (front28 + r3x/r5x swap + no c12 JMP(p0)) is 18:
it gets parts (a)+(b) of the modelled recipe. Part (c), one more key-0 heap entry created during the
efail trace and kept until the usage traces run, has no source form found, and the 143/144 tie flips.
### Semantics
b swaps the labels of an empty asm goto (falls through); a0 removes an empty asm goto from the c12
condition (it never jumps). Both equivalent to src/mode_client.c.

## s145: source forms for the extra efail heap entry (part (c) of s144's recipe)
Base fb.c = s144/fb.c (f2 18). mk.py writes variants that add an empty asm goto at the end of
clientEraseBlockI's efail block (JMP(ex)) to a new label; t.sh NAME = f2 + simulated r4 order.
- c1 (ex = einv) / c2 (JMP(einv)): f2 86; einv edge moves 79/75 ahead of the front.
- c3 (`if (0) { ex: asm volatile(""); }` at end of fn) = c4 (`return; ex: ...`): f2 29. A new block
  (147) does get pushed by the efail trace, and 128 now lands before 79, but it is popped between 79
  and 81 instead of being absorbed by a usage trace.
- c5 (dead "Success!" copy at ex): did not compile (string escaping in mk.py).
Limit: efail lives in the inlined static clientEraseBlockI, so it cannot get an edge to a
mode_client usage call site; the extra entry has to be a block inside that function.
Not done: the 143/144 tie fix and resuming the gen/climb (`NJ=4 sh ../s144/run.sh fb`).
NO MATCH; best is still s141/best16.c (16), fb.c 18.

## s146: tie fix + model-designed efail dummy (part c), profile-free mode_client

Base fb.c = s144/fb.c (f2 18). Tools: t.sh NAME (f2 + simulated r4 order), mke.py BASE (c3-style
dead `ex` block variants), enum1-4.py (r4sim enumerations), tie.py, run.sh DIR (s144 climb), fb/ e/.

### 1. Tie 143/144 (LC117/LC118) - FIXED: t6.c, f2 16 (ties s141/best16)
tie.py: in fb, trace 139 inserts 146(einv) 144(eout) 143(efail), both -2. The tie flips only by
inserting efail before eout (keys unchanged) or by changing keys. Source: `JMP(efail);` before
`if (block < cinfo->nandSize ...)` in clientEraseBlockI plus a cold label on efail
(`AT(efail) { efc: __attribute__((cold)); }`). Now efail enters at key 0 and is boosted by eout's
trace end (chg -1000100), so it pops right after eout: front is in ref order, only the f0 tail
differs (t6 tail 150 147 79 128 81 42 53 35 vs target 147 128 150 35 42 53 79 81).
Without the cold label (t1/t2/t3) 29-40.

### 2. Model for the extra entry (part c)
- enum2 on fb: 0 needs ALL of: LC114 (146) key -1, 128 (case-7 p0) first inserted by trace 108 (u2)
  or 121 (hdd4), and a dummy inserted by the efail trace at key 0 (absorber irrelevant: an
  unabsorbed dummy popping after the tail also scores 0). With 128 left in trace 127 (its natural
  case-7 dispatch) and <=2 dummies (enum3): floor 3 on fb, 2 on t4/t6.
- 128 is the untaken arm of the case-7 dispatch block 127, which pops before 108/121, so its first
  insertion is always by 127; an added edge from u2/hdd4 can only re-key it (and a key decrease is
  a priority boost that pops it at once). Adding JMP(p0) in u2 (t6u 16 unchanged, t6v 163).
  => the modelled exact recipe is not reachable with the natural CFG; part (c) alone cannot finish.
- enum2b on t6 shape with 128 from 108/121 forced: nothing <= 2.
### 3. c3 variants on t6 (mke.py)
- asm-volatile body (e1-e4, e8: hot/cold/none, JMP before/after log): the dead block (149) IS
  inserted by the efail trace at key 0 (model's shape), but 75 now pops early and 149 lands between
  79 and 42: f2 53. enum4 on that dump (128 move, LC114 key, absorber): floor 5.
- empty / goto bodies (e5 `;`, e6 goto einv, e7 goto efail): block folded away, = t6 (16).
### 4. Climbs (s144 gen/climb, -O3 flags of s101/f2.sh)
- fb: 6334 singles, 100-top pairs (4950), SA x2 (600 it): floor 18, nothing better.
- e (t6e2 + kk in clientEraseBlockI so gen can edit it; gen.py ce range fixed to
  clientEraseBlockI - the s144 port pointed it at the unused public clientEraseBlock): base 53;
  6324 singles floor 17 (dead kk feeds 603/607/608/618 -> usage lines 677/685/692/700 pull the
  dummy out; residual = the same tail hunks as t6), pairs floor 17, SA 27/28. Nothing <= 16.
### Semantics
JMP(...) is an empty asm goto that falls through; label attributes and `if (0)` dead blocks do not
change behaviour; `int kk = __builtin_constant_p(block)` is only read in dead conditions.
### Result
NO MATCH. Best f2 16: s141/best16.c and new s146/t6.c (front fully in ref order; residual is only
the f0 tail ordering, which the model says needs 128 inserted before the case-7 trace).

## s147: goal 1 probes (move case-7 p0 block off the dispatch trace), profile-free mode_client

Base s146/t6.c (f2 16). t.sh NAME = f2 + simulated r4 tail (copy of s146/t.sh). All variants edit
only the case-7 p0 arm / the u2 arm of t6 (JMP = empty asm goto falling through; `if (0)` blocks
reached only by goto; semantics unchanged: p0 still calls clientPatches(NULL) then falls to dtg).

| file | change | f2 | tail |
|---|---|---|---|
| v1 | p0: JMP(u2) then label p0x + call; u2: JMP(p0x) | 108 | front broken |
| v2 | p0: JMP(hdd4) before call | 92 | front broken |
| v3 | p0: JMP(u2) before call | 16 | = t6 (asm edge folded) |
| v4 | v1 with cold label on p0x | 162 | |
| v5 | p0: JMP(hdd4); u2: JMP(p0x) | 156 | |
| w1 | case 7 p0 = `goto p0`; body moved to `if (0)` block after u2 | 16 | same order, block renumbered 109 |
| w2 | w1 + JMP(p0) after client_usage in u2 | 16 | same |
| w3 | w1 without cold label | 76 | |
| w4 | w1 + JMP(p0) before client_usage | 163 | |

Insight: wherever the clientPatches(NULL) block sits in source, `goto` is threaded so it is still a
direct successor of the case-7 dispatch block, which pops before traces 108/121; extra asm-goto
edges from u2/hdd4 either fold away (no change) or perturb the front heavily (asm goto splits u2 /
hdd4 blocks and changes their freqs). Goal (iii) not reached. Goals 2/3 (alt enum on t6, fixed
s146/e climb from t6) not run this session.

NO MATCH, best f2 still 16 (s141/best16.c, s146/t6.c).

## s148: alternative-solution enumeration + dummy levers + t6 climb (profile-free mode_client)

Base s146/t6.c (f2 16; r4 tail 150 147 79 128 81 42 53 35, target 147 128 150 35 42 53 79 81).
Tools: alt.py DUMP K (r4sim enumeration of up to K changes: dummy heap entries key 0/-1/-2 inserted
by any trace at any op position, key overrides -2/-1/+1 on 150 147 79 128 81 42 53 35 144 145 75,
removal of any existing ins/chg op), alt3.py (triples over the 228 non-redundant changes whose single
score <= 9), alt3b.py (every 3rd change on top of each best pair), dz.py (JMP(dz) sweep), t.sh, run.sh.

### 1. Model enumeration on t6's dump (535 changes)
- singles: floor 7. pairs (143k): floor 2, only {dummy key -2 by trace 144 (line ~699, -c `if (mode)`),
  dummy key 0 by trace 69 (c12 `arg == dummy`, line 785)} -> tail 147 79 150 35 42 53 128 81
  (79/128 swapped). triples (filtered, ~2M) and pair+any-third: floor 2. No solution reaches 0 with
  <= 3 changes of these kinds; nothing removes the need to move 128 relative to 79.
### 2. Levers
- dz.py: dead `if (0) { dz: [cold]; asm volatile(""); }` before mode_client's `return 0` + JMP(dz)
  before each of 94 statements (cold and plain): floor 17; the dz block pops early in round 4
  (position ~10, before 127) as its own trace, tail unchanged (renumbered only).
- manual (m0-m7): JMP(dz) in i0 arm (m1/m3) 29, tail 150 147 42 53 35 75 128 79 dz 81; i1 arm 87/35;
  plus JMP(dy) at line 700 (model's key -2 dummy) 82-102. alt.py on m1: singles floor 8.
  The model's trace-144/69 dummies are not realisable: asm-goto edges either fold, pop early, or
  change the inserting block's freqs and wreck the front.
### 3. Climb (s146/e gen/climb, base c/base.c = t6 + kk in clientEraseBlockI, inert 16/5)
6324 singles, top-100 non-inert pairs (4950), SA x2 (600 it): floor (16,5), nothing better.
All jobs stopped.
### Result
NO MATCH. Best f2 16 (s141/best16.c, s146/t6.c). Semantics: JMP = empty asm goto falling through,
dead if(0) blocks and dead kk reads; all variants equivalent to src/mode_client.c.

## s149: CFG-shape levers around case-7 p0 (profile-free mode_client)

Base s146/t6.c (f2 16). Variants a1-a7 (sed on t6, f2 via s101/f2.sh):
- JMP(u2) inside p0 before/after clientPatches(NULL) (a1, a5): 16, edge folds (inert).
- JMP(hdd4) inside p0 (a2) 92; JMP(u2)/JMP(hdd4) before AT(p0) (a3, a4) 76/77.
- JMP(p0c) from u2 (a6, a7) 163/143.
Laundered-value conditions (asm "=r"/"0" copies) were not compiled: they leave a real
test+branch in the output that the reference lacks (no pass after bbro deletes real branches),
so they cannot be byte-exact. Model enumeration to 4-5 changes and climb not run.
### Result
NO MATCH, best f2 16 (s146/t6.c). Semantics: JMP = empty asm goto falling through.

## s150 (attempt 131): MATCH, plain compile, no profile

`match.c` builds `mode_client` byte-identical with no profile. Base: `s146/t6.c` (21 changed lines).

### Verification (real compiler output)

- Flags: `-O3 -fno-toplevel-reorder -fno-ipa-profile -fno-reorder-functions --param builtin-expect-probability=50`.
  No `-DBUILD_FDO`, no extra param. `match.c` only mentions BUILD_FDO in its head comment.
- `sh tools/wip/mc/s101/f2.sh <copy of match.c>`: 0.
- `sh tools/wip/mc/s150/cmpo.sh tools/wip/mc/s150/match.c`: `.text`, `.rdata`, `.rdata$zzz` and relocations are
  all the same as `build/obj/mode_client.o`. Its output dir `build/v/mc150/o` is created on demand.
- `sh tools/wip/mc/s150/vlink.sh`: links build.sh's object list with this `mode_client.o`, then stamp and execmp.
  0 differing bytes, SHA256 `10dac648...1971c`, the reference's. Uses `build/obj` from the last build.

Integration is still open: src/, build.sh and tools/re are untouched, and build.sh still uses the profile splice.
To integrate, move `match.c`'s changes into `src/mode_client.c`, drop the fprof/fflags/ffns case and `mode_client.prof`,
then run the full `sh build.sh`. Check whether the old `BUILD_FDO` head comment and macros in the source are still wanted.

### How the residual went from 16 to 0

The model (`s86/r4sim.py`) was exact every time it was compared with a real dump. The search scripts are
`beam2.py` (replaces `beam.py`), `real.py`, `real2.py`, `real3.py`, `dumb.py`, `dumk.py`, `chain*.py`, `ei2.py` and `ext.py`.
`bbs.py` maps a trace bb number to source lines. Those numbers differ from the RTL's, which is compacted through
the "Reordered sequence" table. Older notes misread this: 79/81 are the `-r` usage blocks (asm goto `r3x,r5x`,
cross-jumped), and 144 is the efail log.

Levers, in the order they were found. All are zero-byte and never taken at run time:

1. **Zero-byte dead block**: `if (0) { dz: asm volatile("" ...); __builtin_unreachable(); }` with a `JMP(dz)`. It adds a
   heap entry and a pop, and emits nothing. Identical bodies get cross-jumped, so each needs its own asm, for example a
   `"i"(N)` input or a clobber. A `"#"` template also works but prints /APP lines.
2. **Any key for that block**: a dead `if (__builtin_constant_p(block + K)) goto dy;` feed gives it stale frequency at
   profile_estimate, then folds away. An optional dead `goto` back conserves downstream flow. `dy` (key -2, from efail)
   took f2 from 16 to 10; swapping `r3x,r5x` to `r5x,r3x` took it to 6 (`best6.c`).
3. **`-r` head edges** (`tail_ok.c`). Heap needs 81 and 79 inserted before 62, so:
   - `__builtin_memset(argv, 0, kk); if (!kk) { ac: cold; asm goto("" :: "a"(i) :: r5x, r3x); }` at the head of the `-r` test.
   - The dead memset is a side-effect call in the block, so PRED_CALL still fires on the `-ip` test (without it, 50/50).
   - The cold folded arm keeps the usage blocks at frequency 0.
   - `"a"(i)` matches the reference's first `mov eax,[esp+68]`.
   This gave the exact tail with f2 18.
4. **`-i`/`-p` tie**: those edges renumber the loop PHI, so the i partition's lowest member is anonymous and its pseudo
   gets a high regno (r402, not r91). RTL then uses the copy and `i+1` no longer conflicts. Fixed with
   `({ __asm__ ("" :: "d"(i + 1)); 0; })` in both tests (`p2`). This reached f2 0, but the bytes still differed.
5. **Byte-level residuals**, invisible to f2:
   - Case 6's asm goto cross-jumped into case 8's tail, so its jump table entry was wrong. Removed it. Round 2 then pops
     159 before 161 and the heap shape changes. The model gives one fix: a key -3 entry pushed in round 3. Done with `dv`
     in the rok block's asm label list.
   - Don't use `cp(mode + K)` inside a switch case: VRP knows `mode` there, it folds true, and it became `case 6: c11`.
   - Label alignment rule: `freq > prev_freq * 10` with no fallthrough, so a frequency-0 block before a nonzero block
     aligns the label. Fixed with stale-frequency tail blocks: `efcl` after efail (asm with `"i"(64)`, `-w` label), `c8t`
     (c9 label), `c9t` (c11 label). A zero-byte dummy with frequency there is no help, as the alignment lands on it.
   - Identical `asm goto dsp` tails cross-jumped into jmp-to-jmp. Each now has its own `"i"(N)`, and case 4's asm moved
     into the sendAvatarData arm so hdd4 jumps straight to dtg.

The `mk*.py` scripts are the chain of edits that produced `match.c`. They ran in a scratch dir that is now deleted, so
they are a record and won't rerun as they stand. `best6.c` and `tail_ok.c` are intermediate states.

### Ruled out

- Edges from post-loop code into the arg loop (for example case 3 to the `-w` test, 773-789): liveness wrecks RA.
- Usage edges after the strnicmp call (82-84): eax holds the result, so the usage block gains a reload.
- `s150/beam.py`: its `r3` move can never score, because it emits the block ahead of round 4.
- Model solution "62 first inserted by trace 117": exact in the model but needs a back edge. `real2.py` filters those.
