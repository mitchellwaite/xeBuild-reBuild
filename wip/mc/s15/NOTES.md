# mode_client, 15th session (2026-10-28): NO MATCH (still 15/16)

Best real result unchanged: s10 best.json on s9/sp.c = fncmp 32 / inv 12.

## Step 1: free loop frequencies (fake6.py) -> 0 is NOT reachable at the real scale
fake6.py = s13 fake5.py (vY history wip/mc/s12/bYr.txt, X targets ALLX, X2=121 TX2=112,115) with
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

## Step 2: why the chain halves (bbro dump, cfg_b40)
49/55/61/67 are the -ip/-r/-w/-e strnicmp tests (else-if chain). In round 4 (thresholds 0) a
trace always extends to the best successor, so 55 only starts its own trace (as in the
original order 49 ... 55 ... 61 ... 67) if p(49->55) <= p(49->50 match path), i.e. f55 <= f49/2,
and so on down the chain. 49 itself must stay < 10.7 (round 3 otherwise). Hence 55 <= 5,
61 <= 2, 67 <= 1. The way to more resolution is a larger max entry frequency, i.e. a higher
loop exit probability (entry 214 at exit 2%; ~6% would give the 3x range).

## Step 3: loop-side source shapes (shapes.py, shapes.out; 28 shapes, unprofiled)
Identical code to sp.c (canonicalised away): == 0 test, while loop, ++i, help as else-if,
continue after -ip / -r / -w, increment placement (ip/r/e), empty asm after ip, inlined
opt() helper, `return usage(),0`. Same contents, different unprofiled order: E() added/removed
on -ip/-r/-w/-e/-c (profile-equivalent: only the estimate for unoverridden edges changes;
profiled fncmp 38 with best.json, no new history), -ip/-r/-w with the other usage(3) test
form (r_u3, w_u3, ip_r3, r_order: profiled they reorder the -r test operands vs the
original, wrong). Contents change: do-while (32), `!= argc` (22), register pins in -e/-c
(22), shared usage(3) label (15), cached `char *s` (246), `>= argc` (12, different set).
No loop shape gives a new history with identical contents.

## Step 4 (partial): raising the loop exit for resolution
mode_client:104>105 (loop exit) on best.json, sp.c: 2.1% already flips the -bp eax/edx RA tie
(s10). New: register pins fix it with unchanged unprofiled code (plain 134, content 12 = sp.c):
- pinA: -bp `__asm__("" :: "a"(i + 1), "d"((unsigned)(i + 1) * 4));` (replaces the first "r" pin)
- pinF (= pinA + `__asm__("" :: "c"(i));` before `j = i + 1;` in -wb) -> wip/mc/s15/pinF.c
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

## Next angle
1. Find the pass that stops merging the three -wb usage blocks at exit >= 3.5% (pinF):
   dump -fdump-rtl-all / -fdump-tree-pre (tail merge) at exit 2 vs 4 and diff block counts;
   a fix keeps content 0 at ~6%, which gives the 3x key range the sim needs.
2. Then the exit-6% history differs (s10: rounds 2-3 reorder at 2.5%+): re-dump bbro at 6% on
   vY+pins, renumber, rerun fake6.py with caps scaled (cap ~ 5% of the new entry freq), and
   build the realizer (fdorun9.overrides with MC_POST = exit flow).
3. X2 (second fake source) is still sim-only; designs without X2 must be re-simulated.

## Tools
fake6.py (env FREE vars, VMAX, CHAIN, CAP49, CAPC, FULL; same args as fake5.py),
shapes.py (+ shapes.out), run.py (s10 runner with MCD=<prepared dir>), pinF.c.
