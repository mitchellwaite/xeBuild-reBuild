# s77: mode_client profile-free (attempt 58)

## Key finding: s73..s76 bests are semantically wrong

`best73.c` / `best78b.c` (and gr2.py's `lab` lever) write

    else
        AT(hdd4) { hc4: __attribute__((cold)); } log_printf(0, "...avatar...HDD...");

The `{ hc4: ...; }` block becomes the whole else body, so the log_printf runs
after sendAvatarData too (same for hdd5 / sendCompatData). Our asm then has
`call _sendAvatarData` falling into the hdd4 message. Braced fix
(`else { AT(hdd4) {...} log_printf(...); }`, both sites): `fx.c`, fncmp 98
(was "78"). gr2.py's `lab` lever has the same flaw on any unbraced body: don't use it.
gr3.py drops it.

## How the cold order is made (bb-reorder, from the -fdump-rtl-bbro-details log)

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

## Levers (measured; sig2 = sig2.py +/- token count, fx = 24)

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

## Climb

gr3.py: score (sig2, fncmp); levers: bcp chain del/add/rm, fail-feed (new), rok/fkbo fan
add/del/swap (new); no label lever. 5 x 2400 s from c95.c: see results below.

## Climb result

5 x 2400 s gr3.py from c95.c (16, 222): best (14, 196) = best_s77.c (w4). Logs: w*.log.gz / w*.out.gz.
Semantically correct baselines: fx.c (best78b braced, fncmp 98, sig2 24), best_s77.c (fncmp 196, sig2 14).
Next: give WriteBl (c9) switch-edge priority 4 (find why its case edge is 2), make Info0/CU2
lose fkbo/rok priority, Ferase/-e group levers; then score by fncmp once sig2 reaches 0.
