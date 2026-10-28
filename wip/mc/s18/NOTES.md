# mode_client, 18th session (2026-10-28): the bb_to_key priority lever

(draft, updated at the end of the session; see "Result" below)

## The lever works (verified on real dumps)
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

## Simulators
- fake7.py: bYr (vY) history replay + priority model (T48, X2, X1ORD/X2ORD orders, RX).  Too
  optimistic: many 0-inversion designs, but the vQ variants' real histories differ (tie structure).
- hsim.py: replays the REAL bbro history of a compiled variant (renumbered to sp numbers by
  analyze.py) with design keys; reproduces the measured order exactly.  hanneal.py anneals
  f/P on it (constraints: chain bounds, case-path <= 50%, X2 budget, dispatch budget, f <= 10).
- runq.py: closed-loop realizer (design f/P -> gcda overrides; dispatch/X2 split, corrections).
- variant.py / batch.py: genq.py source variant (X2 label order, X1 label set/order, RX126/RX117)
  -> prep -> runq -> hanneal on its real history.

## Results so far
- fake7: 0 inversions reachable (an2_*), but not on real histories.
- real histories (hanneal floor per history): RX126 only: 2..18 (48 variants); RX126+RX117:
  best 1 (b10_4: only u2/-r order, tail perfect; b11_1/b12_1: -c/-e usage 42 vs 35).
