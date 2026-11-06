# mode_client de-tricking

Goal: `build/mc/reference.o` (copy of a matching build/obj/mode_client.o) byte-identical with
fewer hints.  141 tricks at the start of attempt 1 (README.md's list: `--param
builtin-expect-probability=50`, 89 `__builtin_constant_p` feeds, 19 asm goto, 10 pins, 7
hot/cold labels, 6 expects, 3 `if (0)`, 3 `__builtin_unreachable`, 2 literal-order asm "i",
clientEraseBlockI inlined by hand).

## State after attempt 4

**88 tricks** by README's categories (94 before), **87 once build.sh drops the param**: all 6
expects gone (the 4 `E()` uses, the macro and its `__builtin_expect`), no new hint.  With no
`__builtin_expect` left, `--param builtin-expect-probability=50` no longer acts: the object
is IDENTICAL BYTES with plain `-O3` too, so build.sh's `mode_client)` case can become
`cflags="-O3"`; the parent dropped the case when landing this (mode_client now uses the default `*` case).  Whole object
IDENTICAL BYTES, full build SHA256 10dac648...1971c, progress 617/617.

| Category | Att. 3 | Now |
|---|---|---|
| `--param builtin-expect-probability=50` | 1 | 0 (inert; dropped from build.sh when attempt 4 landed) |
| `__builtin_constant_p` | 51 | 51 |
| asm goto statements | 16 | 16 |
| pins | 6 | 6 (the -bp `"a"(i + 1)` now inside bpArgs) |
| cold labels | 7 | 7 |
| expects | 6 | 0 |
| `if (0)` / unreachable | 3 / 3 | 3 / 3 |
| hand-inlined clientEraseBlockI | 1 | 1 |

For review: the `-bp`/`-wb`/`-eb` arms call new static helpers bpArgs/wbArgs/oneArg
(getArgs-style, `int *pi`; each keeps its arm's own test order), and the reboot tail calls
`netDisconnect()` in both arms (commented `borderline:`).

## Attempt 4

94 -> 88.  Tools (tools/wip/dehint/, logs in build/mc/, dumps in build/mc4/, not tracked):
- `mc4dump.py FILE.c TAG [flags]`: compile with `-fdump-tree-profile_estimate-details
  -fdump-rtl-bbro-details` into build/mc4/TAG/.  The profile_estimate dump's "Predictions
  for bb N" lists which heuristics set each branch: this is how the expects were understood.
- `mc4v_tail.py`, `mc4v_eb.py`, `mc4v_wb*.py`, `mc4v_bp*.py`, `mc4v_one*.py`: variants for
  mc2try.py (MCBASE = the base named in each file's comment).
- `mc4greedy.py` / `mc4walk.py BASE.c PREFIX`: greedy that also takes count-neutral label
  drops, and a walk that takes count-neutral pairs when stuck.  `mc4groups.py` /
  `mc4gpair.py`: mc1's G_* groups with current slot names (mc1.py's G_* entries carry
  stale indices from attempt 1 and are no-ops on today's base: their "IDENTICAL" in singles
  output means nothing changed), and each group paired with every single.
- `mc4render.py KEY OUT.c`: render a hit from m2_hits.json.

Mechanism (profile_estimate dump): with param 50, `__builtin_expect` is first-match and sets
its branch to exactly 50%.  Without it the branch gets the DS combination of the other
heuristics.  The call heuristic (PRED_CALL, 71%) predicts an edge not taken when its
destination block is dominated by the branch, doesn't post-dominate it, and contains a call
with side effects.  The `-rb` arm is 50% naturally: its first statement is the getArgs call
and the else edge's block calls strnicmp, so both edges are predicted and cancel.  The
-bp/-wb/-eb arms started with argv tests (no call), so only the else edge was predicted
(71% then); E() pinned them to 50%.  Reboot: only the netReboot edge had a call (29%); the
else edge went to `ndl:`, which has many predecessors (not dominated).

What moved:
1. E(reboot): `if (reboot) { netReboot(reboot); JMP(fail); ndl: netDisconnect(); } else
   netDisconnect();` -> IDENTICAL (the else arm's own call is dominated -> both edges
   predicted -> 50%).  `if (!reboot) netDisconnect(); else {... ndl: netDisconnect(); }` also
   IDENTICAL; `ndl:` on the else arm's call: 10 (that arm is no longer dominated).
   Borderline: the duplicated call.
2. E(-eb): the arm as `arg = oneArg(argc, argv, &i, mode);` with a static helper holding the
   arm's checks -> IDENTICAL.  einline does not inline it (too big), ipa-inline does (called
   once), so the call is still there at profile_estimate.  i by value + `i++` at the call is
   also IDENTICAL; took the `int *pi` form like getArgs.
3. E(-wb): wbArgs with `int *pi` -> IDENTICAL for several bodies (j = i + 1, `j++` or the
   scoped `int k = i + 2` for the second argument, `*arg2 = b` before the mode test).  The
   by-value form with `i += 2` at the call: 258+ (the caller's `i` update is a different SSA
   shape).  Note: on a base that still had E(reboot) the same helpers left a 6-line flip of
   the -r/-w arm's `i + 1 == argc || !a` order; it went with the reboot change.
4. E(-bp): bpArgs (`int *pi`, `!a || j == argc` first test, then the arm's `b = argv[i + 2];
   j = i + 2;`), with the `"a"(i + 1)` pin kept inside -> IDENTICAL.  Without the pin every
   shape (36 in mc4v_bp2) is 20: the same eax/edx swap as attempt 2.
5. With all four gone there is no `__builtin_expect`: the param is inert.

Searched with no hit (attempt 4):
- Walk from the reboot base and from the final base: pairs within 100 (501 and 1626
  pairs), only count-neutral label drops (dv's c1 + one fa edge; then c7, fa2-fa4 free).
  Label drops never opened a counted removal.
- Dead-construct groups on the final base: G_dz 60, G_dv 34, G_kk 78, G_dy 225, G_efail
  231, G_hdd 257, G_dsp 263; G_dv/G_dz/G_kk + every single (294): best 28 (G_dz + r_ifkk=4).
- More arms as helpers: -e or -c through their own copy of oneArg: 6 each (flips the -w
  arm's test order); both: the second helper is not inlined (ipa-inline growth limit on the
  large mode_client), 10177.  A shared helper for -bp and -wb (wbArgs twice): not inlined.

### Don't retry (attempt 4)

- bpArgs without the pin (36 shapes, all 20); by-value bpArgs (408).
- More than one extra helper call site for the same helper, or a fourth inlined helper in
  the option loop: ipa-inline stops inlining (mode_client is near large-function-growth).
- Label-only drops in the rok/fkbo lists as stepping stones.

### Ideas for attempt 5

- Read the profile_estimate dump for each remaining feed's target: the cp feeds and asm
  gotos add edges whose probabilities (and the frequencies of their targets) are what
  bb-reorder sees.  Natural code that predicts the same edge the same way (a call in the
  first block of an arm, a dominated block, an early return) may replace a feed; check which
  heuristic the target branch gets with and without the feed before searching.
- Cold labels are PRED_COLD_LABEL (first match, very likely).  The only natural first-match
  predictor with the same weight is a noreturn call (PRED_NORETURN); none of the cold arms
  ends the program, so look instead at whether a cold label can be traded for a feed edge
  pattern, not for plain C.
- The -bp pin: IRA gives i + 1 eax only with the pin; try the caller side (what the call
  passes, `&i` vs a copy) now that the arm is a call, or the -wb helper's shape changed in
  step (the two arms' pseudo numbering interacts, attempt 2).

## State after attempt 3

**94 tricks** by README's categories (96 before): 2 `__builtin_constant_p` gone (the -s k61l
feed's third term and -r's `i + 5555` feed, attempt 2's "k61l pair"), no new hint, no
borderline shape.  Whole object IDENTICAL BYTES, full build SHA256 10dac648...1971c,
progress 617/617.  build.sh unchanged.

| Category | Att. 2 | Now |
|---|---|---|
| `--param builtin-expect-probability=50` | 1 | 1 |
| `__builtin_constant_p` | 53 | 51 (the -s k61l feed has 2 terms, -r has none) |
| asm goto statements | 16 | 16 |
| pins | 6 | 6 |
| cold labels | 7 | 7 |
| expects | 6 | 6 |
| `if (0)` / unreachable | 3 / 3 | 3 / 3 |
| hand-inlined clientEraseBlockI | 1 | 1 |

The source change besides the two feeds: every `arg = argv[++i];` (and `ip = argv[++i];`)
is now `arg = argv[i + 1];` + `i++;` (8 arms).  Plain, consistent style; not a hint.

## Attempt 3

96 -> 94.  Tools (tools/wip/dehint/, logs in build/mc/, dumps in build/mc3/, not tracked):
- `mc3nat.py BASE.c [...] [-r RULE] [-pair]`: natural same-meaning rewrites (pre-increment
  spellings, `!strnicmp` vs `== 0`, `if (mode != 0)`, operand order of `i + 1 == argc`,
  declaration order and initialisers, loop spelling, arm statement order, ...), one
  occurrence or all occurrences of a rule; hits -> build/mc/m3nat_hits.json.
- `mc3nx.py BASE.c [-m 30]`: mc1 singles on the base (cached), then every mc3nat rewrite on
  top of each near miss (hint removal x rewrite).
- `mc3v_tail.py` (E(reboot) with return/duplicate shapes), `mc3v_ga.py` (option arms as
  getArgs calls), `mc3v_ip.py` (attempt 2's -i/-p variants respelled for the new base);
  run with mc2try.py.

What moved:
1. bC.c (attempt 2's k61l pair, 8 lines) is the loop latch compare's operand order
   (`cmp esi,eax; jle` vs `cmp eax,esi; jge`).  Dumps: tree canonicalisation puts the lower
   SSA version first; PRE's latch phi takes a recycled name from the SSA free list (src
   before: prephitmp_228 > argc_69; bC: prephitmp_2 < argc_68).  Which names are free at
   PRE depends on the numbering of the whole function, so any rewrite that changes the
   number of SSA names before PRE can flip it.
2. mc3nat on bC: `arg = argv[i + 1]; i++;` for `arg = argv[++i];` in the -i or -p arm, or
   in all 8 arms -> IDENTICAL.  Took all 8 (consistent).  On the old base the same rewrite
   costs 8 (it flips the same compare the other way), so it only pays together with the
   pair.

Searched with no hit:
- Pairs of bC's near misses within 120 lines (917); case-order moves on bC (144, all 8).
- mc2climb on the new base (singles: no free one; pairs of 67 near misses within 250,
  2167: only label drops that don't count).
- mc3nx on the new base: 22 near misses within 40 x ~110 rewrites (2400): none.
- E(reboot) without the expect: `!reboot ; else`, `!= 0`, a duplicated `netDisconnect();
  return 0;` in the reboot arm, a goto to a shared return: all 10 (two crossjumped
  `client_usage(5, argv[i])` blocks swap; `> 0` 209).  The return lever does not reach it.
- Option arms as getArgs calls (-eb, -bp, -wb, both, all three): gcc does not inline
  getArgs (a constprop clone appears for the NULL-arg calls), 268-10442.  The arms do read
  like getArgs inlined by hand (same test order, `argv[first - 1]` in the usage calls).
- Attempt 2's -bp shapes (mc2v_bpa, bpa2) on the new base: still 20; -i/-p shapes
  (mc3v_ip): still 52.
- Classified the new base's singles up to 800 lines: none differs only in compares/jumps
  or only in register names, so no other near miss is an SSA-order flip of the kind the
  rewrite fixed; the near misses are block-order ties (switch case blocks, the two usage(5)
  blocks) and register allocation.

### Don't retry (attempt 3)

- mc3nat's rewrites alone or on any near miss within 40 lines of the new base.
- getArgs calls for the arms; E(reboot) return/duplicate shapes; -bp/-i/-p shapes from
  attempt 2 on the new base.

### Ideas for attempt 4

- The SSA-free-list lever: look for near misses on other branch points (attempt 2's states
  bA/bB, other pair choices) whose diff is a compare-order or register-only flip, then run
  mc3nat on them; a flip is cheap to fix with a spelling change.
- E(reboot) 10 is a crossjump survivor choice between two identical usage(5) tails (index
  in ecx vs edx); try changing which arms share the `client_usage(5, argv[i])` tail (e.g.
  the -bp/-wb arms' spelling of argv[i] in the usage calls via the shared `j`).
- Switch-case block order near misses (j_dv_26-c1 12, c3 terms 14): case order is free and
  doesn't move them; try the case bodies' shapes (e.g. `case 7` / `case 12` dummy tests as
  `arg != dummy`, calls with the dummy test inside the helpers).

## State after attempt 2

**96 tricks** by README's categories (105 before): both literal-order asms, 4 pins and 3
`__builtin_constant_p` gone, no new hint.  Two borderline shapes (redundant `return;`,
commented `borderline:`).  Whole object IDENTICAL BYTES, full build SHA256
10dac648...1971c.  build.sh unchanged.

| Category | Att. 1 | Now | Where |
|---|---|---|---|
| `--param builtin-expect-probability=50` | 1 | 1 | build.sh |
| `__builtin_constant_p` | 56 | 53 | fail's ndl(205562) feed down to one term (255562), fail's `mode + 260` feed gone; rest as after attempt 1 |
| asm goto statements | 16 | 16 | case 5's former `"a"(cinfo)` asm goto is now `JMP(s4, c12)` |
| pins | 10 | 6 | bp `"a"(i + 1)`, `-i`/`-p` `"d"(i + 1)`, `"a"(i)` in the `-r` head asm goto, fkbo `"X"(&fkv)`, rok `"m"(rko)` |
| cold labels | 7 | 7 | |
| expects | 6 | 6 | |
| `if (0)` / unreachable | 3 / 3 | 3 / 3 | |
| literal-order asm "i" | 2 | 0 | |
| hand-inlined clientEraseBlockI | 1 | 1 | |

## State after attempt 1

**105 tricks** by README's categories (141 before): 33 `__builtin_constant_p` and 3 asm goto
statements gone, no new hint, no borderline shape.  Whole object IDENTICAL BYTES, full build
SHA256 10dac648...1971c, progress 617/617.  build.sh unchanged (the param is still needed).

Remaining, by category:

| Category | Before | Now | Where |
|---|---|---|---|
| `--param builtin-expect-probability=50` | 1 | 1 | build.sh (plain -O3: 736 lines) |
| `__builtin_constant_p` | 89 | 56 | 2 in clientEraseBlockI (dy feed and back edge), `kk` (memset size / `if (!kk)`), u2 at the loop head, the 3-term `(char *)` k61l feed in `-s`, -r's k61l, after the loop (dtg), rok's ndl, dsp's t4 (4), the mode=7/11/9 chain (6+6+5), ndl tail s5 (4) and u2 (1), fail's 10 feeds (4+3+4+1+4+1+1+1+1) |
| asm goto statements (JMP / `__asm__ goto`) | 19 | 16 | rok list now 9 labels (was 26), fkbo list 27 (was 30), c3's JMP(hdd4,hdd5) (s5 gone) |
| pins | 10 | 10 | bp `"a"(i + 1)`, two `"=D"/"D"` blocks + `"r"(count)` in clientBinPatch, `-i`/`-p` `"d"(i + 1)`, `"a"(i)` in the `-r` head asm goto, `"a"(cinfo)` in case 5, fkbo `"X"`, rok `"m"` |
| cold labels | 7 | 7 | efc, einv, ac, rok, hc4, hdd5_c, fail |
| expects | 6 | 6 | E on -bp/-wb/-eb and reboot (+ the macro) |
| `if (0)` / unreachable | 3 / 3 | 3 / 3 | dy, dv, dz |
| literal-order asm "i" | 2 | 2 | clientInfo, clientWriteBlocks |
| hand-inlined clientEraseBlockI | 1 | 1 | |

Also removed, not in README's counts: clientEraseBlockI's `efcl: asm volatile("" : : "i"(64))`,
clientEraseBlock's unused `kk`/`AT(efail)`, rok's dead trampoline sub-block (rk14-rk51), every
trampoline that no list reaches (rk/ork, fa/ofa), and the unused plain labels (eerase, esucc,
eout, lu1, wb3, k55l, k67l, w5x, dvb, fkbo, S761, p0, p0c, i0, i0_c, c8, c8t, c9t).
Labels nothing jumps to never mattered.

## Attempt 2

105 -> 96.  Tools (tools/wip/dehint/, states and logs in build/mc/, not tracked):
- `mc2.py singles|near|pairs|triples [-m DIFF]`: mc1's edits on the current base (MCBASE),
  singles -> build/mc/m2_singles*.json (MC2SINGLES), then pairs / triples over the near
  misses (MC2SKIP regex drops duplicates such as fa3-fa20).  Hits -> build/mc/m2_hits.json.
- `mc2try.py VARIANTS.py [names] [-v name [fn]] [-o name out.c]`: score hand-written
  substitution variants; the variant files are `mc2v_*.py` (ci = clientInfo, wb =
  clientWriteBlocks, bp/bp2-4 = clientBinPatch, bpa/bpa2 = the -bp arm, ip/ip2 = -i/-p,
  misc/misc2 = asm operands).
- `mc2x.py` (term orders of the parser's `||` tests, with removals), `mc2pad.py` (remove a
  cp chain, pad others with fewer terms), `mc2case.py` (move one switch case), `mc2combo.py`
  (cross product of hit files), `mc2climb.py BASE.c` (singles + greedy + pairs within
  diff 250, repeat).
- mc1.py now tolerates the missing clientWriteBlocks asm (template only).

What moved:
1. clientInfo's literal asm (ci_lit 4): success first plus a redundant `return;` at the end
   of the `if (out)` block -> IDENTICAL.  Success first alone flips the branch (6), `if
   (!out) return;` + success first fixes the tail but swaps the jump-threaded copies of the
   bad-block head (xor ebp placement, 4).  Mechanism: the arm bb-reorder leaves out of line
   is the first one expanded unless the return block comes after the forwarder; the extra
   return puts the forwarder (and return block) after the tail.  Borderline.
2. clientWriteBlocks' literal asm (wb_lit 14): nest it `if (start != -1) { buf = ...; if (buf
   && len > 0) { ...; free(buf); return; } read error } else invalid` -> IDENTICAL.  Plain
   nesting without the return 44-60.  Natural (the return skips the read error).
3. clientBinPatch's three pins (bp_D x2, bp_rcount; all three off = 8, a robust esi/edi swap
   in the inlined patchNand tail that no type/order/statement-order sweep moved):
   `if (cinfo->nandSize == 0x3000000) memcpy else patchNand` in place of the switch AND a
   redundant `return;` after the write result -> IDENTICAL.  Either alone 147 / 209.
   Borderline.
4. case 5's `__asm__ goto ("" :: "a"(cinfo) :: s4, c12)`: the operand never mattered ->
   `JMP(s4, c12)` (one pin less).  Also free, not counted: fkbo's `"X"(&fko)` operand and
   `fko`, rok's `"m"(rkv2)` operand and `rkv2`, `rkv0`.  (fkv moved to the outer scope: 358.)
5. Pairs within diff 250 (attempt 1 only went to 80) on the new base: `cp_k61l_3` (-r's
   k61l feed) + any one term of the -s k61l chain, and one term of fail's ndl(205562) chain
   + fail's `mode + 260` feed.  The two pairs don't combine (8).  Took the ndl pair; then
   a second ndl term was free (climb2: greedy), then stuck (2509 pairs within 250, none).
   The k61l pair on that base is an 8-line near miss with no compensating single.

### Don't retry (attempt 2)

- Triples within diff 80 on the 102-state base (4031, none); pairs within 250 on the final
  base (2509, none but label drops).
- Term-order permutations of the parser's `||` tests: each costs a flat 4, also with
  near-miss removals (881 variants).
- Padding cp chains to compensate a removed chain (648 variants): the diffs never move,
  so term counts are not the lever for t5/mode-chain removals.
- Switch case order: free (no byte change) except cases 4/5; with near-miss removals 3024
  variants, none.
- `-i`/`-p` "d" pins: 12x12 test shapes and default-assignment / mode-first shapes all 52.
  The pin makes two pseudos for i + 1 (edx for the test, eax for the latch PHI in the
  arg = dummy paths); every spelling is CSE'd to one.
- `-bp` "a"(i + 1) pin: `j = i + 2; b = argv[j];` gets it to 20 (eax/edx swap of i + 1 and
  argv[i + 2]); 30 first/second-test/end shapes stay at 20 or worse; singles on that base
  no help.  `"r"(i + 1)` 16 (still a pin).
- clientBinPatch: decl splits, int start/count, uint32_t rlen, (int) casts, increment
  order of patchNand's loops: all 8 without the return.

### Ideas for attempt 3

- The redundant-return lever worked twice where bb-reorder picks which arm goes out of
  line; try it on mode_client's tail blocks (the usage(5) / log swaps behind E(reboot) 10,
  fail's t5 feed 8, the k61l pair's 8).
- Pairs on top of the k61l near-miss base (build/mc/bC.c, 8 lines) instead of singles.
- The -bp pin at 20: combine the `j = i + 2; b = argv[j]` shape with the -wb arm's spelling
  changed the same way (allocation order follows pseudo numbering of both arms).
- Climbs from other pair choices (the k61l branch, build/mc/bA.c).  Triples within diff 40
  on the final base were run (1482, none): don't repeat.

## Attempt 1

Tools (tools/wip/dehint/):
- `mc1lib.py <file.c> [-np] [-v [fn]]`: compile as build.sh does (`#line 1 "mode_client.c"`, `-O3
  --param builtin-expect-probability=50`) and compare with build/mc/reference.o (whole file
  bytes, else .text disassembly per function, .rdata/.data/.bss and relocs).  ~0.7 s a compile.
- `mc1.py list|singles|greedy|pairs|climb|show|count`: cuts the source (MCBASE=<file>, default
  src/mode_client.c) into a template of slots.  Manual slots (pins, literal asms, dead blocks,
  the kk construct, the mode chain), automatic ones: every cp feed `if (cp && ...) goto L;` as a
  list of terms (drop terms or all), every asm goto label list (drop labels), cold labels
  (drop, or keep as a plain label), expects.  Post edits: `inline` (call clientEraseBlock),
  `rok_all`, `fk_all`, `-np`; groups (G_dy, G_dz, G_dv, G_efail, G_kk, G_dpin, G_hdd, G_dsp,
  G_cebi, G_E) remove a dead block with every edge into it.  `climb`: greedy, then singles and
  pairs (of edits within `-m` lines) on top, take a pair, repeat.  MCCHAIN=lists makes the
  mode=7/11/9 arms term lists.  Slot names carry a running index, so names differ between
  bases; states (build/mc/*.json) belong to the base they were made on.
- `mc1clean.py in.c out.c`: drops dead trampolines and unused plain labels one at a time,
  keeping each that stays IDENTICAL.

Runs (states and logs in build/mc/, not tracked):
1. singles on the start: 47 of ~210 edits IDENTICAL alone.  Free: clientEraseBlock's kk and
   AT(efail), efcl, rk_dead1, s5 in c3's JMP, rk0-rk13 alone, and any single term of the
   feeds u2(750), ndl(5562..), dtg(7351..), dtg(5569..), ndl(7368..), dtg(6949..).
2. greedy (free edits first, then by single diff): 138 -> 123 in my count (build/mc/g1.json).
3. pairs on g1 (69 near misses, diff <= 60, 2338 pairs): only `j_dsp_36` (default's `"i"(109)`
   asm goto) with one cp term dropped from the dtg/ndl chains.
4. climb -m 24: round 1 took that pair, greedy went on (j_i1, rk1/8/13, dv list's dsp, c7, c8,
   cdef, fa0, fa1, dtg, c3, the `-s` cdef feed, more chain terms) to 109; round 2 took
   `cp_c9_7-ALL + j_c11_27-c11` (dsp's whole c9 feed with c8t's JMP(c11)) and reached 103;
   round 3 no pair.  pairs -m 80 on that state (61 near, 1793 pairs): none.
5. mc1clean on it, then a new base (build/mc/c2.c) with the mode chain arms as term lists:
   one more term (arm 9's first) -> 102.  pairs -m 30 (30 near, 434 pairs): none.
6. Hand tidy (braces and blank lines around removed labels): still IDENTICAL BYTES; full build
   matches.

### What each remaining hint is needed for (singles on the final state)

Diff = differing disassembly lines; sizes from build/mc/singles2.json (final state).
- Near misses (<= 30 lines), all bb-reorder ties between two adjacent cold tail blocks or a
  swapped pair of `client_usage(5, ...)` / log blocks, or the literals' .rdata order:
  ci_lit 4 (clientInfo's .rdata), each wb_lit operand 6-14, the whole fail feed to t5 8,
  E(reboot) 10 (two usage tails swap), bp_rcount 12 (clientBinPatch reload thread), c3 feed
  terms 18, hdd4 in c3's JMP 18, bp_D either block 20, dsp's t4... c9 feed 22, mode chain arm
  11 terms 24, arm 9 terms 28, fail's ndl(205562) feed whole 24, bp_pin 30.
- 35-60: `-p`/`-i` `"d"` pins 35/41 (both 52), rok list's c12 and rk6 44, every fa2-fa20 edge
  44 (each edge into fkN counts; the 19 of them set its frequency), case 5's c12 50,
  hc4 cold 56, JMP(dz) 60.
- 78-150: the `-r` head `if (!kk)` block 78 (G_kk 78), JMP(c10) 92, JMP(dy) 122, rok's dv
  edge 136, the dy feed 144.
- 170+: everything else, up to 736 (-np).  Large ones: E on -bp/-wb 457-597, rok cold 422,
  fail's t5 feed terms 394, cp_dtg_4 (after the loop) 392, fkbo's "X" asm 358, inline 265.
- Compile-only dependencies: dy/dv/dz blocks need their edges gone first; `kk` is used by the
  memset and `if (!kk)`; fail's label is jumped to.

### Mechanisms observed

- Feed chains are not all-or-nothing.  `cp(a) && cp(b) && ...` chains could often lose terms
  one at a time, but which terms can go depends on how many have gone elsewhere: at the start
  any single term of six chains was free, at the end dropping one term of fail's t5 feed costs
  394 lines while dropping the whole feed costs 8.  The removals interact through counts
  (SSA names, blocks, edges into a target), not through the term's constant.
- Pairs work as compensation: removing the default case's `"i"(109)` asm goto alone moved two
  tail blocks (8 lines), and dropping any one cp term in the dtg/ndl/dtg chains put them back.
  Same for the c9 feed + JMP(c11).  So many 8-line near misses are tie flips of a single heap
  key, fixable by another single change of the same weight.
- Edge multiplicity matters: rok's list keeps c12 directly and also rk6 -> ork6 -> c12, and c3
  only through rk10 -> ork10 (the direct c3 went).  The 19 fa edges into fkN each count.
- Unused labels, dead trampolines (labels no list names), and scope braces without
  declarations never changed a byte.

### Don't retry

- Any single removal or single term drop on the final state (all tested, table above);
  pairs within 80 lines on the 103 state, within 30 on the 102 state.
- `-np` (736), all four E's with -np (609), inline clientEraseBlock (265, also with all of
  clientEraseBlockI's hints gone: 265), rok_all (328), dropping the whole fkbo construct.
- Removing a dead `if (0)` block together with its edges (G_dy 225, G_dv 203, G_dz 60 at the
  first greedy state).

### Ideas for attempt 2

- Triples / climb with a wider pair window on the 8-30 line near misses: they are tie flips, so
  two or three paired removals may cancel (e.g. E(reboot) 10 + a term drop; ci_lit 4 is only
  clientInfo's literal order, try the success-first shape with another join).
- Replace the fa2-fa20 edge bundle (19 edges into fkN) by something with the same frequency
  effect: a cp chain feeding fkN, or a loop-free natural construct.
- The literal-order asms (ci_lit 4, wb_lit 6-14) are small and local: try nested/success-first
  shapes and result-variable joins in clientInfo and clientWriteBlocks (options' lever).
- clientBinPatch's pins (bp_D 20, bp_rcount 12): try local types/scoped temporaries for count
  and start (keys' and sendAvatarData's levers) rather than asm.
- Model-based (tools/wip/mc/s86/r4sim.py) recomputation of which heap keys the remaining feeds
  set, then search for natural code that yields the same keys.
