# mode_client, 9th session (2026-10-28): structural probes + split-test crafted profile, NO MATCH (still 15/16)

## Facts checked
- Original jump table (src/app/mode_client.s, L_44fb1c): 13 entries (index 0..12), 13 distinct
  targets, index 0 = the `ja` default target, case 6 = the join.  Same as ours: no merged
  labels, no fewer edges.  predict.c 6.2 ignores switch predictions (`nedges != 2` ->
  even), so `__builtin_expect` on the switch index does nothing (exp4/exp1: same keys).

## Source-structure variants (batch.py spec1/spec2, draft as base; f = fncmp lines, keys -freq)
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

## Crafted profile, combined test (fdorun9.py via d.sh/d2.sh, draft numbering) ~20 designs
- Raising HDD cases alone reorders the case traces (they pop by key); keeping the original
  case order needs 9 tied cases (incl. case 10 for connect) >= the HDD cases, and dispatch
  <= 66 (combined test split by expand: switch <= 1/3) -> HDD <= 3.65 -> realized 4 only at
  7.3/case, which costs the 3 other cases -> case order scrambles (z2: f 100).
- Lowering the loop exit (104>105 = 1%) changes RA everywhere (f 346).

## Crafted profile, SPLIT post-loop test (the real lead)
`sp.c` = draft with `if (!mode || ({ __asm__(""); 0; }) || !arg)`: two GIMPLE conditions, so
the profile sets the arg test's probability directly and the expand q/2 split no longer caps
the switch at 1/3 (cap is now ~50% of the arg-test flow, i.e. ~97 of 200).  Plain compile is
136 lines, but with a profile (sp.sh: mode==0 10%, arg==0 50.5%, all 12 cases equal ~8, HDD 50%)
the hot layout and the whole case order match and the cold order starts
-ip, av, xb, u2 (pre 4..7) for the first time with the original case order.
Prep: `python wip/mcfdo.py "$(cygpath -w "$PWD")\build\mcsp" wip/mc/s9/sp.c` (tree bbs +1 vs
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

## Next angle
Continue on the split-test profile: (1) add overrides for the loop-internal usage edges
(find their tree edges in build/mcsp/pe.txt, `client_usage (3|4|5, ...)` blocks) and the
chain, (2) search with an objective = mcvar inv/pre first, (3) re-run mono.py on each new
best build's dump to steer.  Integration would follow build/mode_update's profile-compile
route (asm("") hint in src + crafted .gcda).
Tools: batch.py (s8 runner -> s9), spec1/2.py, d.sh/d2.sh/fdo.sh (combined-test designs),
sp.c/sp.sh (split-test designs), fdorun9.py (POST env, per-slot cwd so runs can go parallel),
k.py (round-4 keys of a slot), search.py/show.py (parallel search; SLOG selects log), mono.py.
