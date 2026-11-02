# fileutil myatou32 (queue 2)

Tools: `tools/wip/dehint/musweep.py <gen.py>` (parallel fncmp, plain -O3 -Isrc; outputs in build/mu32/<gen>/),
generators `gen_mu*.py`. `mufn.py <dump> <fn>` cuts one function out of a dump, `mustubs.py <bbro.txt>` lists
bb-reorder's pop order with frequencies (needs -fdump-rtl-bbro-details-blocks).

## Upstream evidence

cOzInABox/XeBuild tools/opt_idx/opt_idx/util.cpp (both refs main and master, same file) has, line 209-222:
`if(((dat[0]&0xFF) == '0')&&(myatol(dat[1]&0xFF) == 'x'))` with one comparison, no 'X' test, and the same if/else
and returns as src/fileutil.c. su_check's util.c has myatol but no myatou32. So the only upstream text available
does NOT have the second comparison; that source (single test) gives 120 differing lines, see below. opt_idx is a
different tool from xeBuild, so this doesn't prove what xeBuild.exe's own copy said, in either direction.

## What the dead test changes

Single test: 116 lines differ, all in the tail of cold stubs (block order only, same instructions).
profile_estimate: dead 'X' block adds a second .28 (bb6), so P(hex) = .28 * (.28 + .72*.28) = .1348 vs .28*.28 = .0784.
VRP removes the test, the frequencies stay. Hex arm's stubs get about 1.7x the frequency, which changes the order
bb-reorder pops them in (mustubs: round 4 of the hinted run has no bb 7, plain pops it first; order of 39/38, 120...).

Diagnostic (expect + --param builtin-expect-probability=N on the x test, not a candidate):
N=49 and 50 MATCH; 48 and 51 don't (116/126 lines). So the target: P(x test) around 48.2..50% with P(first test) = 28%,
i.e. the x test is effectively UNPREDICTED. gcc's opcode heuristic skips `!= 0` comparisons, so a flag test or
a switch would give 50%.

## Sweeps

- gen_mu1 (143): flags around the whole test, gotos, early returns, helpers. `if (c0 && cx)` family 116-120; flag around both tests 140-724.
  `if (c0) switch (myatol(..)) { case 'x': ... }` 4 lines: layout right (50% with no prediction), only two loop `cmp` orders wrong.
- gen_mu2 (840): switch shape x spellings of tails and temp: always 4 (or 18 with the switch on dat[0]).
- Why 4: a switch's default edge is first in succs, so DFS finishes dec before hex, so the loop numbers swap and ivopts does dec first.
  The first loop processed gets `ivtmp != bound` (121/336), the second `bound != ivtmp` (298/318), so both cmps flip.
  Checked by gen_mu6: a switch whose default arm is hex (`switch (cx) { case 0: break; default: hex }`) MATCHes. That form isn't natural.
- gen_mu3 (241), flag at the join after the '0' test: 217+. gen_mu4 (55), x flag with two uses: forwprop folds it anyway (match.pd follows multi-use), 116+.
- gen_mu5 (112): switch x spellings of validateString and myatol: no change to the cmp order.
- gen_mu7: `int base` at the join 700+. BUT a flag set and tested inside the '0' test MATCHes: `ifl`, `ifb`:
  `if (c0) { int skip = 0; if (cx) skip = 2; if (skip) { hex } } dec`.
- gen_mu8 (26): flag spellings. MATCH: `int`/`BOOL` set by an `if` (`hex = 1`, `skip = 2`, `base = 16`), also `if/else` set, and `skip = cx ? 2 : 0`.
  116 (flag folded before the estimate): `hex = cx`, `hex = cx ? 1 : 0`, `BOOL hex = cx ? TRUE : FALSE`.
  6 lines (dec's strlen/test order): `skip` actually used, `&dat[skip]` or `dat += skip`. That would have given the flag a second job, but doesn't match.

## Why the flag matches

The `if (hex)` compare with 0 gets no opcode prediction: bb7 50%, so its true edge is .28 * .5 = .14 of the function, inside the diagnostic window
(.1348 to .14). vrp1 threads both arms of the x test through it and the frequency stays. It's an `if`, so the true edge comes first and the loop order and cmp order are right.
At the join after the '0' test (gen_mu3) the same flag fails: 50% of the whole function instead of 50% of the '0' arm.

## Result: MATCH, landed in src/fileutil.c, not committed

    if((dat[0]&0xFF) == '0') {
        BOOL hex = FALSE;
        if(myatol(dat[1]&0xFF) == 'x')
            hex = TRUE;
        if(hex) { if(validateString(&dat[2])) return myatox32(&dat[2], defValue); return defValue; }
    }
    if(validateString(dat)) return atoi((const char*)dat);
    return defValue;

fncmp with no flags: MATCH, also myatoh32, myatol, myatox32, validateString. `sh build.sh`: 10dac648...971c.
drafts/fileutil_myatou32_best.c is a copy of the landed file; drafts/fileutil_myatou32_switch4.c is the 4-line switch shape.

Caveat: `if (hex)` is live (it goes both ways) but redundant with the test above it, and it matches because it adds a 50% branch estimate. That's the same lever
as the dead test, in a form that reads as an ordinary flag. Whether that's source shape or a disguised hint is a judgement call for the user.
No upstream source has this flag. The binary can't tell the flag from the 'X' test: both produce the same bytes.
