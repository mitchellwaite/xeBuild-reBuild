# mode_client, 10th session (2026-10-28): split-test crafted profile, NO MATCH (still 15/16)

Best: `best.json` (sp.c from s9, build/mcsp) -> **fncmp 32, mcvar inv 12** (s9: 40 / 18).
Reproduce: prepare build/mcsp as in s9, then `python tools/wip/mc/s10/run.py SLOT tools/wip/mc/s10/best.json`.
~1300 compiles (search10.py: s9 knobs + 17 in-loop usage-edge overrides; probes; exit sweeps).

## Tools
- run.py (one design -> fncmp/inv/order; keys = s9 names or raw `fn:s>d` tree edges)
- probe.py (which bbro blocks an edge override moves), rap.py (parallel variants + RA-swap flag)
- dumpcfg.py (profile-read compgotos CFG = bbro/trace numbering; `-o -` so the -.gcda is found)
- mcsim3.py (mcsim2 + freq -1 = probably-never-executed key 10000), kenum3/4.py (exhaustive
  nonincreasing key sets with realizability), ksearch*.py (random/hill-climb on the sim;
  ksearch4 = real-valued chains capped at 50%), search10.py (compile search).
- Bucket map (tree edge -> bbro block): 16>17,28>29 -> u3cx 29; 19>20,32>33 -> u4cx 33;
  21>22,34>35 -> u5cx 35; 40>41 -> u3dx 53; 42>43 -> u5dx 42. cfg_b40.txt = the s9 best's CFG.

## Why the profile route can't reach inv 0 (sim on the f40 history, all rounds simulated)
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

## Next angle
Not a profile search: something that changes the round-2 competition (104 vs 44/38) or the
erase-chain order (source shape for clientEraseBlock / case 10), e.g. a hint that ends trace
98-99 elsewhere so 104 loses its priority key. Otherwise park (15/16).
