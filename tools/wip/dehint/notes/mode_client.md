# mode_client de-tricking

Goal: `build/mc/reference.o` (copy of a matching build/obj/mode_client.o) byte-identical with
fewer hints.  141 tricks at the start of attempt 1 (README.md's list: `--param
builtin-expect-probability=50`, 89 `__builtin_constant_p` feeds, 19 asm goto, 10 pins, 7
hot/cold labels, 6 expects, 3 `if (0)`, 3 `__builtin_unreachable`, 2 literal-order asm "i",
clientEraseBlockI inlined by hand).

## State after attempt 12

**51 tricks** (MATCH, 52 before): clientEraseBlockI's `JMP(dy)` (erase-failed block) gone,
`dv` added to case 3's list (`JMP(hdd4, hdd5, c3, dv)`).  Per category: asm goto 11 -> 10;
cp 24, pins 6, cold labels 4, `if (0)` 3, unreachable 3, clientEraseBlockI 1 unchanged.
List labels 47 -> 48.  Whole object IDENTICAL BYTES, full build SHA256 10dac648...1971c,
progress 617/617.  No borderline shape.  n49 (49, 10 lines) still the best near miss; the
mechanism that ties the cebi removals to the case region is the vrp1 jump-thread hash
order (below).  build.sh unchanged.

## Attempt 12

52 -> 51 (item 6).  Tools (tools/wip/dehint/, states and logs in build/mc/w12/, dumps build/mc4/b12_*):
- `mc12keys.py A.c ...`: RTL (bbro) frequency, trace and final position of the blocks that
  hold named labels (label -> bb from rtl_dce, the numbering bbro's trace lines use).  The
  case heads: c9 127, c11 140 (138 on n49), c7 123, p1 125.
- `mc12vrp.py A.c ...`: vrp1's jump threads through the mode-chain switch in execution order
  with the target block index mod 13.
- `mc12filt.py BASE -g GEN,...`: count-neutral variants (cebifeed, dyblock, failperm,
  reloc[:T], rep:<mc9rep gen>, rep:at) filtered by the reference thread order before scoring.
- `mc12rm.py BASE`: every single trick removal with its thread order and score.
- `mc12cebi.py BASE`: the two JMP(efail) lists x the cebi feed's spelling and target (576).
- `mc12arms.py BASE`: mode-chain terms redistributed between arms 9/11/7 (total kept).
- `mc12heads.py`, `mc12bb.py`: early profile freqs per callee; named bbro traces (the call
  naming of mc12bb uses the post-bbro listing and is wrong for the high bbs: use mc12keys).

What was found:
1. **n49's 10 lines are the c11 head's frequency.**  bbro round 4 pops the case heads by
   key -(100*BB_FREQ_MAX + 100*priority + freq): priority 3 for all (the switch edge),
   c9 7, c11 7, c7 6 in the reference; on n49 c11 is 4 (fail's c11 feed gave +3), so c7/p1
   pop before c11.  Need c11 >= 7 (or c7 <= 3).  The case heads' block freqs are fixed at
   the early profile_estimate (switch shares 4 each + feeds/list edges); the mode-chain
   arms don't change them (mc12arms: 1/4/5 136, all others 257+).
2. **Why the c11 feed can't come back on n49 (n49c11 = n49 + the feed, 50 tricks, 320
   lines): vrp1's thread order.**  vrp1 threads the arms mode = 11 / 7 / 9 through the switch
   (sources 139/144/134).  thread_block walks a redirection_data hash table whose hash is the
   target block's index, table size 13.  The targets are the ASSERT blocks VRP creates on
   switch edges whose case head has several preds (c7 = x, c9 = x+1, c11 = x+3, all
   last_basic_block + k), so the walk order is set by the *total block count* at vrp1.
   Reference x = 205 (slots c11 0, c7 10, c9 11: order c11, c7, c9).  The threading order
   changes the switch's case probabilities after the update: reference 8.7% each, c7 6.3%;
   n49c11 (x = 204: c7, c9, c11) 8.9% / c7 4.2%, so the c7 edge freq rounds 3 -> 2, c7 loses
   its priority (key -1000206) and c7/p1 go late: the 320 lines.  n49 has c11 with one pred
   (no split, target 176), so its order and probabilities are the reference's.
   Good x: x mod 13 in {10, 11}, i.e. **one or two blocks more** than n49c11.
3. Block-count shifts of single edits (relative to the state): cebi's dyj alone 0 (nodyj,
   51 tricks, 122 lines but only ~24 real: a few cold blocks reordered), ybk alone -1
   (225), dyj+ybk -1, merging `if (0) { dv: } if (0) { dz: }` into one -1 (base 300, a
   removal waiting for a +1).  Cebi feed moved anywhere in cebi: 0, -1 or -2, never +;
   dy block moved: 0.  mc12rm on n49c11: no single removal is +1.
4. No count-neutral +1 found on n49c11: reloc of every feed (1883, 314 with the right order,
   best 10 = the c11 feed moved somewhere dead, i.e. n49 again), lists/at/less/retarget/
   default (2144, 108 right order, best 10 = c11 retargeted, then 24+, lists 130+), fail
   perms (6 right order: feeds before the log call, 261+, the probabilities move to 9.0/5.0
   because fail's flow changes too), cebi lists x spelling x target (217+).  On n49 the cebi
   sweep is 10 everywhere (the cebi side does not reach c11's frequency).
6. **52 -> 51**: nodyj (JMP(dy) removed: shift 0, right order, 122) + the filtered repair set
   (mc12filt -g rep:perm,default,less,at,retarget,cebifeed,lists: 2189, 1905 right order):
   `dv` added to case 3's list (either end) or to case 5's `JMP(s4, c12, ork6)` front:
   IDENTICAL (4 hits; landed `JMP(hdd4, hdd5, c3, dv)`).  An extra edge to the dv
   unreachable block from the cold area gives back the cold-tail layout JMP(dy)'s edge gave.
   Next best: c11 retargets 10, at 18.
5. Asm goto edges into c11 (self JMP(c11) 248, JMP(c10, c11) 284, subs into c11 175+, fkv
   list drops of c7/p1 209+) are not gentle: the edges live into RTL.

### Don't retry (attempt 12)

- On n49: any c11 feed position (it brings the split and the bad thread order), mode-chain
  term redistribution, cebi lists/spelling/target, asm goto edges into c11, fkv drops.
- On n49c11: single feed relocations, single list/at/less/retarget/default edits, fail
  perms, cebi sweeps (all checked against the thread order, build/mc/w12/*.log).

### Ideas for attempt 13

- The lever is the block count at vrp1 (mc12vrp, mod 13).  Look for a gentle **+1 block**
  that vanishes before RTL: candidates not tried are shapes that GIMPLE lowers to an extra
  block but that fold away (a second `return 0;` path, a split `if (a) if (b)` of a 2-term
  feed such as k61l's, a feed written with `else`, a label kept by `&&label`-free code), and
  pairs (one count-neutral -1 elsewhere + the dyj/ybk/merge removals).  Each removal with
  shift -1 (ybk, dyj+ybk, dv/dz merge) becomes a candidate once one such +1 exists.
- On the new 51 state (mc12rm, build/mc/w12/rm51): c11 feed 18, u2 feed 206, einv cold
  243, first JMP(efail) 246, ybk feed 320 (shift -1: needs a +1), the rest 260+.  Re-run the
  filtered repairs (mc12filt rep:lists,at,less,retarget,perm,default) on each of those.
- Run mc12filt's repair set on every shift-0 removal: that is how 52 -> 51 came.
- Other hash-order spots: any vrp/dom thread_block with 2+ paths is order-sensitive the same
  way; mc12vrp prints only the switch's.

## State after attempt 11

**52 tricks, unchanged** (NO MATCH; src/mode_client.c untouched, still IDENTICAL BYTES).
List labels 47 before and after.  Best near miss: **drafts/mode_client_a11_n49.c, 49
tricks, 10 lines** (fail's c11 feed, cebi's `JMP(dy)` and the dy block's ybk feed gone, one
`less` toggle; the only difference is the c11 block, clientBinPatch, laid out after
c7/p1's clientPatches instead of between c9 and c7).  build.sh unchanged.

## Attempt 11

No match.  Tools (tools/wip/dehint/, states and logs in build/mc/w11/, dumps build/mc4/a11*):
- `mc8comp.labels` fixed (idea 1): string literals and comments blanked (no more 'ERROR',
  '1', 'borderline' junk) and AT(x) labels included.  mc8comp.edits on 52: 1236 edits (all
  older generators that use it, mc7comp / mc8comp -two / mc9rep lists / mc10pairs, now see
  the case labels).
- `mc11arm.py BASE -arm N -t L -k ...`: a whole mode-chain arm dropped and replaced by one
  k-term `goto L` feed at every position (idea 2).
- `mc11armjmp.py`: arm dropped + list edits / one new JMP(L) anywhere / less / perm (written,
  not run: the arm 11 drop alone is 371, see below).
- `mc11sub.py BASE -t L`: list substitutions (one label replaced by L, list length kept).
- `mc11norm.py A.c [-v]`: diff with jump/call targets blanked (a moved block counts its own
  lines, not every jump into it; useful to see what a 300-line score really is).

What was found:
1. mc10loop on 52 (loop.log, stopped after c11's repairs): alone, fail's **c11 feed is 10**
   (was 26-34 in attempts 7-9); pdpin 35, idpin 41, dyj 122, ybk 225, dy 233, the rest
   240+.  Every 1-term feed other than c11 is 300+ now (t4 315, t5 324, s5 362, rok's ndl
   341, dtg 388, fail's ndl 418; mc11norm: t4's 315 is ~96 real lines, several case blocks
   move).  The arm 11 terms are 300 (were 22 on 54).
2. The c11 near miss (drafts/mode_client_a11_c11.c, 51): the c11 block is placed after
   c7/p1's in the same bbro trace (layout c9 c11 c7 p1 -> c9 c7 p1 c11).  rtl dumps
   (build/mc4/a11r_*): the block order and every call's relative order are the same in
   every pass up to rtl_dce; **bbro alone** makes the difference.  profile_estimate: c11
   head 7 -> 4 (c12 3, i1 5, c9 7, c7 6, p1 8).  Repairs on it: at 276, default 2, perm 6,
   less 20, default+at 552, lists 1218, retarget 552, substitutions 47: all 10 (subs 266+).
   One arm 11 term removed on top: 22; 2-4 terms 257.
3. **dyj and ybk ride on the c11 removal.**  On the c11 state, removals: dyj 18 (= the c11
   10 + the latch flip 8; any of 20 `less` toggles fixes the flip -> 10), arm 11 terms 22,
   pdpin 45, idpin 51, efail1 56.  On that state (rm_c11_dyj_less, 50) the ybk feed is free
   (10) -> n49 (49 tricks, 10 lines).  On 52 itself dyj is 122 (dyj+ybk 320, with any less
   122): the cebi edges and the c11 feed interact (the c10 block, clientEraseBlockI, sits
   between c9 and c11).  On n49 the whole dy block (feed + if (0) + unreachable, 46 tricks)
   is 230, efail1 146.
4. On n49: perm 266+, default 10, less 10, lists (fixed labels, 1228) 10, retarget 552 10,
   reloc 2144 10, the cebi dy feed moved anywhere in clientEraseBlockI (mc7reloc -fn,
   with `block + N` spelling) 230+, and the c11 feed put back as a 1-term feed at every position
   (mc10ins, 269): **10 everywhere**, including the original position.  So the c11 block's
   placement on n49 is no longer about the c11 feed: it is the cebi change (dyj/ybk) that
   keeps c11 late, and c11's frequency alone cannot bring it back.
5. Arm 11 (5 terms) dropped and replaced by a 1-4 term `goto c11` feed anywhere (mc11arm,
   1076): best 194 (1 term in the rok list block).  The arm is the case head's flow; no
   position replaces it.  Arm 7 (-> c7/p1) was started and stopped (same pattern expected).

### Don't retry (attempt 11)

- Arms as goto feeds (mc11arm) on 52: 194+.  List substitutions toward c11: 266+.
- On the c11 state and on n49: single at/lists/less/default/perm/retarget repairs, a new
  c11 feed anywhere (all 10).
- 1-term feed removals on 52 other than c11 (300+, several case blocks move).

### Ideas for attempt 12

- n49's 10 lines are a bbro layout choice in the case region (c9, c10 = clientEraseBlockI,
  c11, c7, p1).  Look at the bbro-details traces of base52 vs n49 (build/mc4/a11_base52,
  a11_n49, mc.bb: trace 58 is c9 c11 c7 p1 vs c9 c7 p1 c11) and find which edge
  probability / frequency in the cebi blocks changed; then aim count-neutral moves at cebi
  (efail list labels, `cp(block)` vs `cp(block + N)` on the dy feed, efc/einv positions,
  ybk label position) rather than at c11.
- Pairs of edits on n49 restricted to cebi labels/lists plus c9/c10/c11/c7/p1 (mc10pairs
  -labs with the fixed labels).
- On n49, the latch-flip toggle set (less) for the cebi feed spelling `cp(block)` vs
  `cp(block + N)` together with the dy feed's position (mc7reloc gave 230+ with `block + N`).
- If n49 lands, the dy block (if (0) + unreachable + its feed) may follow: on n49 it is 230,
  re-check after.

## State after attempt 10

**52 tricks** (MATCH, 55 before), three `__builtin_constant_p` gone: the default case's c3
feed (`cp(mode + 1085650)`), fail's ndl feed `cp(mode + 255562)`, and one term of the t4
feed (2 terms in the rok block -> 1 term at the end of the connected branch, after
`} else goto fail;`: a relocation with one term fewer).  Per category: cp 27 -> 24; asm goto
11, pins 6, cold labels 4, `if (0)` 3, unreachable 3, clientEraseBlockI 1 unchanged.  List
labels 46 -> 47 (`c3` added to case 3's own `JMP(hdd4, hdd5, c3)`).  Count-neutral moves
that came with it: the t5 feed after the default case's log call (attempt 9's c3t5 draft),
fail's other ndl feed `cp(mode + 157368)` moved *before* fail's log call (call heuristic
71%), the mode = 7 arm's terms spelled 907000/907002/907003/907004 (still 4).  Whole object
IDENTICAL BYTES, full build SHA256 10dac648...1971c (checked at 54 and at 52), progress
617/617.  build.sh unchanged.  No new hint kind, no borderline shape.

## Attempt 10

55 -> 54 -> 52.  Tools (tools/wip/dehint/, states and logs in build/mc/w10/):
- `mc10edits.py BASE.c ... [-pairs]`: asm goto list adds of the **AT(x) labels**.  The lever.
  mc8comp.labels only matches `name:` labels, so c1, c2, c3, t4, hdd4, t5, s5, hdd5, c7, p1,
  c9, c10, c11, c12, i1, cdef, u2 (and cebi's efail) were never added to any list by
  mc7comp/mc8comp/mc9loop/mc9rep (their label list also holds junk from string literals:
  '1', 'ERROR', 'borderline', which only make compile errors).  278 edits on the 55 state.
- `mc10loop.py BASE OUTDIR [-skip RX]`: mc9loop with the AT edits as a repair, plus the
  default-case perms, and two-step default+at / less+at.
- `mc10pairs.py BASE -labs L,...`: pairs of mc8comp list edits restricted to some labels.
- `mc10ins.py BASE -t L [-k N]`: one new k-term feed to L at every position.  Found t4.
- `mc10self.py BASE`: subsets of the three ndl feeds removed x ndl in the dtg arm's JMP(fail)
  list / a new JMP(ndl), each with fail's perms.  Found fail's ndl feed.
- `mc10jmp.py BASE -rm RX -t L`: a 2-term feed replaced by L in a list or one new JMP(L)
  at every position.  `mc10two.py BASE EDIT|none -r ...`: all count-neutral repairs of one
  near miss (mc9rep's plus `at`).

What was found:
1. c3t5 (attempt 9's draft: c3 feed gone, t5 after the default log, 8 lines: the clientKeys
   block placed after case 5's instead of after c1's) + `c3` added to c3's own
   `JMP(hdd4, hdd5)` -> IDENTICAL.  An edge from the case 3 block back to its own head
   raises the head's frequency (the block's flow split three ways, one share re-entering),
   which is what the removed default feed gave it.  The earlier repairs could not reach it:
   c3 is an AT label.
2. On c3t5 before that: every 1-term feed relocated (2430): 8 everywhere; pairs of list
   edits restricted to rk10/ork10 (676; hdd4/hdd5/c3 are AT labels so were missing): 8.
3. AT edits on the 55 state's near misses: c3 alone 12 -> 8 (`c9` or `t5` into c3's list);
   arm 11 terms 22 -> 14 (`i1` into case 5's `JMP(s4, c12, ork6)`); ch16 (chain-16 draft,
   51 tricks) 16 everywhere.  On 55 also: c3 removal + reloc 8, c11 removal + reloc 20
   (alone 297), c11 + default perms 34.
4. mc10loop on the 54 state (build/mc/w10/loop*.log): stuck at 54.  Alone: t5 22, arm 11
   terms 22 (all four the same), ndl (rok's feed) 24, pdpin 35, idpin 41, dz 60, kk2 78,
   the rest 120+ (c11 now 270+: with c3's self-edge the case-11 head no longer needs only
   fail's feed).  Repairs:
   - t5: AT 12 (`hdd5` into case 5's list), perm/less 22, lists 22, less x AT (6072) 12.
     t5 + hdd5 then: AT, less, perm, lists, retarget all 12 (mc10two, two_t5.log).
   - arm 11 term: perm **10** (fail's four feeds all *before* the log call, c11's last, so
     c11's feed takes the call heuristic's 71%), default 18, AT 22.  On that perm
     (arm11perm0.c): AT, default, less, retarget, lists all 10.  The 10 lines: the c11 block
     (clientBinPatch) placed after c12's instead of before; mc9freq: c11 head 8 vs 7 in the
     reference.  The term removal alone leaves every case head's frequency as is (c11 7) and
     moves the chain itself: arm 7's first test 22 -> 21 (arm 11 takes one unit more).
   - ndl: AT 22, default+at 22, the rest 24.  pdpin: 35 everywhere.
   - Two removals with the arm 11 term (+ perms, combo.log, 1780): best 22 (with an ndl
     feed of fail).
5. ch16 on the 54 state (ch16_54.c: 50 tricks, 16 lines): AT 16, perm/default/less 16.
6. **54 -> 53, two ways** (each IDENTICAL on the 54 state, not together: 113+):
   - mc10self: fail's `cp(mode + 255562)` ndl feed removed and the other ndl feed moved
     before the log call (fail's perms; with or without `ndl` in the dtg arm's JMP(fail)).
     The ndl block gets back what the removed feed gave through the call heuristic.
   - mc10jmp: the rok block's 2-term t4 feed replaced by `case 8: JMP(t4);` (2 cp -> 1 asm
     goto).  Kept as an alternative only (drafts/mode_client_a10_t4jmp53.c, full build checked).
7. **53 -> 52**: on the ndl state, the t4 feed removed and a 1-term t4 feed put at every
   position (mc10ins): one hit, after the connected branch's `} else goto fail;` (the
   switch's join, colder than the rok block, so one term is enough: attempt 6's mechanism).
8. On 52: mc10self (the remaining ndl feeds) 275+; k61l as a 1-term feed anywhere 190+.
   On 53/54: k61l replaced by a JMP or a list label 204+; ch16 + JMP(c7) anywhere 16.

### Don't retry (attempt 10)

- Reloc of 1-term feeds on c3t5 (floor 8); rk10/ork10 list pairs on c3t5.
- AT edits alone on ch16 / ch16_54 (16 floor); less x AT on removals (6000 each, nothing).
- k61l as a JMP / list label (54) or a 1-term feed (52): 190+.  The other ndl feeds on 52.
- On the 54 state: single repairs (AT, perm, default, less, lists, retarget) of t5, the
  arm 11 terms, ndl, pdpin; repairs of t5+hdd5 and of the arm 11 perm-10 state.

### Ideas for attempt 11

- **Self-edges.**  c3's feed was replaced by the case 3 block's own label in its own asm
  goto list.  Look for other feeds whose target block (or a block it dominates) already has
  an asm goto statement, and try the target's label in that statement: t5/s5 into case 5's
  JMP(s4, c12, ork6) and JMP(dsp) (single AT adds were tried on t5's removal: 12), c10 into
  JMP(c10) (already there), the efail/dy lists in clientEraseBlockI for the dy feed.  And
  blocks with no asm goto: a *new* `JMP(L)` inside the target block costs one asm goto per
  feed removed, so it only pays where it replaces a 2+-term feed (t4's 2 terms, k61l's 2) or
  two feeds at once (fail's two ndl feeds: one JMP(ndl) in the ndl block).
- Arm 11 term perm-10 (c11 head 8 vs 7): c11 needs a share between fail's 50% and 71%;
  try the c11 feed's position relative to *other* calls (reloc ran only on the 55-state
  near misses; mc10two with -r reloc on build/mc/w10/arm11perm0.c, see two_ap0.log), or
  the chain's arm 7 first test given back its unit (arm 7 tests before arm 11 with the
  same terms).
- mc10ins / mc10jmp for the other multi-term feeds and arms after each bank (t4 only hit
  once the ndl state existed): the mode = 11 / 7 arm terms as 1-term `goto c11` / `goto c7`
  feeds at the switch join (attempt 6 tried goto feeds for arms only before the c3/t5
  moves), and re-run mc10self / mc10ins t4 on every new state.
- Fix mc8comp.labels (AT labels, no string-literal junk) so every older generator
  (mc7comp, mc8comp -two, mc9rep lists) includes them; re-run mc8comp -two on the 54
  state's t5 (12) and arm 11 (10) near misses with AT labels in the pair space.

## State after attempt 9

**55 tricks** (MATCH, 58 before), all three `__builtin_constant_p`: fail's dtg(156949)
feed, the mode = 9 chain arm's second term (now 1 term) and one of the mode = 7 arm's
terms (now 4).  Per category: cp 30 -> 27; asm goto 11, pins 6, cold labels 4, `if (0)` 3,
unreachable 3, clientEraseBlockI 1 unchanged.  List labels 46 before and after (no list
edit).  Whole object IDENTICAL BYTES, full build SHA256 10dac648...1971c, progress
617/617.  build.sh unchanged.  No new hint kind, no borderline shape.  Count-neutral
moves that came with it: fail's four remaining feeds now sit after its log call (one per
line), and two feeds are spelled `cp(V)` instead of `cp(V + N)` (clientEraseBlockI's dy
feed, the after-tail u2 feed: attempt 8's latch-flip repair, still needed: reverting
either costs 8).

## Attempt 9

58 -> 55.  Tools (tools/wip/dehint/, states and logs in build/mc/w9/, dumps build/mc4/a9*,
f9a/f9b):
- `mc9fail.py BASE.c [-o OUT]`: fail's feeds in every order, each before or after the log
  call (both layouts are read).  The lever.
- `mc9loop.py BASE OUTDIR [-m 40] [-k 1] [-ml 14]`: greedy over removals generated from
  the text (every 1-term feed, every `&& cp` term, a 1-term chain arm, mc8comp's named
  non-cp removals), each alone, then repaired with mc9fail perms, `less` singles, and
  (within -ml) single list edits and `less` pairs.
- `mc9rep.py BASE.c -r perm,default,less,lists,reloc,retarget`: every count-neutral repair
  of one near miss (default = the default case's feeds before/after its log call; retarget
  = a feed's goto target changed to any other label).
- `mc9freq.py A.c B.c`: profile_estimate block frequencies of two sources side by side.
- `mc9chain.py BASE.c [-lt N]`: mc6chain restricted to fewer than N terms, else-chained.
- `mc9flog.py`: a new label on fail's log call added to one asm goto list (dead end).

What was found:
1. **The 4-line c9/c11 swap was the call heuristic.**  bbro dumps of the 4 state vs the
   58 state: the c11 head (bb 140, clientBinPatch) has frequency 8 instead of 7, the c9 head
   (bb 127) 7 in both, so c11 wins the tie.  profile_estimate: with dtg2 gone, c11's feed
   is the last one before fail's `log_printf`; its else edge enters a block it dominates
   that makes a call, so PRED_CALL gives the c11 edge 71% instead of the 50% "no
   prediction" of the other feeds (in the 58 state that 71% went to dtg2's feed).  Moving
   all four remaining feeds after the log call (mc9fail, cut 0) gives each 50% of the log
   block's flow: IDENTICAL -> 57.  Other orders after the log (ndl s5 c11 ndl, ndl first
   before the log) also hit; feeds before the log in any order: 4+.  A second predecessor of
   the log block (mc9flog: `flog:` in JMP(fail, flog) etc.) undoes the dominance but moves
   the return blocks: 26+.
2. On the 57 state the arm 9 chain's second term was free alone (mc8alone), and after it
   one arm 7 term (any of four, mc9loop) -> 55 (full build checked).
3. Stuck at 55 (mc9loop, then mc9rep): c3 12 (its own block moves, plus the c9/c11 swap
   again), arm 11 terms 22 (list edits 14, less pairs 16), c11 26, t5 28, pins 35/41, dz 60,
   kk2 78, the rest 120+.  The c3 removal + the t5 feed moved after the default case's log
   call (same call-heuristic mechanism) is 8: only the c3 (clientKeys) block's position
   (its frequency 6 -> 4); less singles/pairs, list edits (1217), fail perms, retargets
   (599): 8.  Draft: drafts/mode_client_a9_c3t5.c.
4. Chain sweep on 55 (mc9chain, < 10 terms, 685 variants): best 16 with 51 tricks, arm 7
   dropped entirely, order 9, 11 with 2 + 4 terms (or 11, 9 with 5 + 1).  The 16 lines are
   the c7 block (the dummy test before clientPatches) placed after c1 instead of near the
   end: c7 loses the arm's threaded flow.  Repairs on both (lists 1217, retarget 666, less,
   perms, default): 16 everywhere.  Draft: drafts/mode_client_a9_chain16.c.

### Don't retry (attempt 9)

- New labels on fail's log reached from asm goto lists (mc9flog: 26+).
- On c3t5 (c3 gone, t5 after the default log, 8): less, list edits, retargets, perms.
- On the chain-16 states (arm 7 gone): single list edits, retargets, less, perms, default.
- Single repairs from 55 for arm 11 terms (14 best with list edits).

### Ideas for attempt 10

- Look for every other feed that sits right before a call block it dominates (the call
  heuristic gives it 71%): the t5 feed before the cdef log, the rok block's feeds after
  netGetInfo, the -noenter feed.  Each is a count-neutral 71%/50% switch, i.e. a new
  frequency knob; sweep before/after-call positions for each together with the removals
  (c3, arm 11 terms, c11, t5).
- Chain-16: c7 needs the frequency the threaded arm gave it; try c7 in two lists at once
  (pairs of list adds restricted to c7), or a 1-term feed to c7 placed after a call (one
  feed for four chain terms would still be -3).
- c3t5 (8 lines, 54 tricks): the clientKeys block needs ~+2 frequency: pairs of list adds
  restricted to c3/rk10/ork10, or c3's JMP(hdd4, hdd5) with one label fewer (each list
  label splits the block's flow).
- Re-run mc8alone + mc9loop with -ml 22 on every banked state: arm9 only became free after
  the fail move, so a change anywhere can free terms elsewhere.

## State after attempt 8

**58 tricks, unchanged** (NO MATCH; src/mode_client.c untouched, still IDENTICAL BYTES).
List labels 46 before and after (efail, dy, efail, -r head 3, dz, rok 7, fkbo 24, hdd4/5 2,
s4/c12/ork6 3, dsp, c10, fail).  Best near miss: drafts/mode_client_a8_near4.c, 57 tricks,
4 lines (dtg2 feed removed + two count-neutral `cp(mode)` toggles; c9/c11 call blocks
swapped).  The latch flip itself is now solvable by count-neutral means (Attempt 8, 2).

## Attempt 8

NO MATCH, 58.  Tools (tools/wip/dehint/, states and logs in build/mc/w8/, dumps
build/mc4/m8b (58 base), m8d (dtg2 removed)):
- `mc8comp.py NAME|none [-base F] [-two [TOP]]`: mc7comp with clientEraseBlockI's labels
  and lists in the edit set (cebi labels into cebi lists), new removals (efc, einv, dyfeed,
  ybkfeed, efail1/2, dyj, hdd45, pinX, pinm, s4c12o, kk2, and groups dyall, efall), `a+b`
  combined removals, and pairs of edits from the TOP best singles.
- `mc8loop.py BASE OUTDIR [-names] [-two N]`: mc7loop over mc8comp.  `mc8alone.py BASE`:
  every removal alone (quick triage).
- `mc8tmp.py BASE [-pairs]`: count-neutral toggles of one cp argument's temporaries:
  `cp(V + N)` -> `cp(V)` (less) or `cp(V * 3 + N)` (more).
- `mc8less.py BASE OUTDIR NAME[,a+b...] [-k 2]`: a removal + every single/pair of `less`.

What was found:
1. Removals alone on the 58 state (mc8alone): dtg2 12, c3 20, arm11 22, c11 34, pdpin 35,
   t5 36, idpin 41, t4 52, dz 60, kk2 86 (2 tricks), dyj 130, dyfeed/ybkfeed 152,
   efail1 174, dyall 216 (5 tricks), hdd45 216, efall 274, efc 286, pinm 295, einv 314,
   pinX 357; the rest 200+.  The new cebi removals are not close.
2. **The latch flip mechanism.**  PRE takes all 20 of its new names from the free list
   (max version unchanged).  The latch phi is prephitmp_582 in the base (> argc_71(D): the
   compare is `argc > i`, `cmp esi,eax; jle`), prephitmp_4 after the dtg2 removal (< 71:
   swapped).  What the free list holds at PRE comes from dce3 (115t) releasing the folded
   cp feeds' `mode + N` temporaries (the c3 feed's _448/_449 in the base; cp is folded to 0
   by dom2) and earlier releases (name 4 at cplxlower).  Toggle: `cp(mode + N)` -> `cp(mode)`
   (one temporary fewer, same count).  On the base one `less` flips the latch (8 lines) at
   most sites; on removal bases a PAIR of `less` repairs it: dtg2 12 -> 4 (any less + the
   after-tail u2 feed `cp(mode)`), c3 20 -> 12, t5 36 -> 20, c11 34 -> 26, t4 52 -> 44.
   `more` (+1 or +2 or +3 temporaries) never changes a removal base.  So the flip is no
   longer the wall; what remains is the case-head order.
3. What remains after the flip fix: dtg2 -> c9/c11 call blocks (clientWriteBlocks /
   clientBinPatch) swapped, 4 lines (drafts/mode_client_a8_near4.c).  c3 and t5 leave the
   same swap plus their own case block moves.  On the 4 state: every single list edit
   incl. cebi (960): 4; every 1-term feed relocated (mc7relocall, 9 feeds; the `cp(mode)`
   ones are not matched by its pattern): 4; less singles/pairs (314+): 4; more singles: 4.
4. mc8loop with single and pair edits (pairs from the 60 best singles): dtg2 12, c3 20,
   arm11 14 (`add dtg>4.e + drop c12@8`), c11 18, t5 22.  The 60 best singles are mostly
   no-op edits (score = alone), so these pairs are weak; a better pair space would take
   singles that change the output.
5. Removal pairs + less pairs (mc8less): dtg2+c3 12, dtg2+t5 24, dtg2+arm11 22, c3+t5 28,
   c11+t5 30, t5+arm11 34, dtg2+c11 250, c3+c11 96.  No hit.

### Don't retry (attempt 8)

- cebi removals (efc, einv, dy/ybk feeds, efail/dy JMPs, groups) with list edits: 130+.
- `more` toggles; less singles/pairs on the d2l 4 state; list edits / 1-term relocation
  on the d2l 4 state.
- Pairs of edits drawn from the best-scoring singles (they are no-ops).

### Ideas for attempt 9

- The c9/c11 swap on the 4 state is a case-head frequency tie (attempt 5): look at the bbro
  keys of the c9/c11 heads in a profile_estimate/bbro dump of the 4 state vs the reference
  and find which feed/list moves one of them by one unit; then try the counted-neutral
  moves aimed at that (relocate the t4 2-term feed, chain arm terms, list labels into
  c9/c11 specifically).
- Apply the `less` toggle as a standard repair in mc7comp/mc8loop: removal + list edit +
  less pair (three steps) for c3, t5, c11, arm11.
- Extend mc7relocall's pattern to `cp(mode)` feeds, and relocate on the 4 state with
  `less` kept on the relocated feed.
- `less` is count-neutral and simpler than `cp(mode + N)`; if a match needs it, it lands
  as is (no new kind).

## State after attempt 7

**58 tricks** by README's categories (63 before).  Whole object IDENTICAL BYTES, full build
SHA256 10dac648...1971c.  build.sh unchanged.  No new hint kind, no borderline shape.

| Category | Att. 6 | Now | What went |
|---|---|---|---|
| `__builtin_constant_p` | 31 | 30 | fail's c9 feed (its edge now rides in case 5's list as `ork6`) |
| asm goto | 13 | 11 | case 9's `JMP(hdd4,hdd5)` and its `"i"(107)` dsp asm goto |
| cold labels | 6 | 4 | `hc4` (case 4's no-HDD block), `ac` (the -r head's kk block) |
| pins, `if (0)`, unreachable, clientEraseBlockI | 6, 3, 3, 1 | same | |

Real removals vs relocation: all 5 are real removals of a counted item.  One count-neutral
relocation came with them (the loop-head u2 feed `cp(i + 321)` now sits after `promptEnter =
0;` in the -noenter arm, still 1 term), and the compensations are uncounted asm goto list
labels: `rk6` added to the -r head's `"a"(i)` asm goto, `ork6` (a trampoline to c12) to case
5's `JMP(s4, c12, ork6)`.

Steps (each IDENTICAL, states in build/mc/w7/):
1. c9's `JMP(hdd4,hdd5)` dropped and hdd4 put in case 5's list (n14: 14 lines, an hdd4-log /
   u2 tail swap) + the loop-head u2 feed relocated to the -noenter arm (mc7relocall) -> 62.
2. hc4's cold label dropped, hdd4 taken back out of case 5's list (mc7comp hc4) -> 61.
   (On the 63 base, hc4 alone + one of several list adds, e.g. `dtg` into c3's JMP, was
   also IDENTICAL: 62.)
3. Case 9's `"i"(107)` dsp asm goto free on that base (mc1 greedy) -> 60.
4. fail's c9 feed dropped + `ork6` in case 5's list (mc7comp c9) -> 59 (full build checked).
5. `ac`'s cold label dropped + `rk6` in the -r head's asm goto (mc7loop) -> 58 (full build).

## Attempt 7

58 (MATCH).  Tools (tools/wip/dehint/, logs/states in build/mc/w7/, dumps build/mc4/m7*, p_*):
- `mc7loop.py BASE OUTDIR [-names]`: greedy over mc7comp's removals, each alone or with one
  free list edit; takes the first IDENTICAL one and starts over.  The lever of this attempt.
- `mc7reloc.py -rm RX ... -ins TEMPLATE [-k] [-fn] [-var]`: generic relocation (remove one or
  more constructs, insert one templated statement at every position of mode_client or
  clientEraseBlockI).  `mc7relocall.py BASE.c`: every 1-term feed relocated (count-neutral).
- `mc7pairs.sh`: two/three feeds into one target (ndl x3, dtg x2, u2 x2) -> one 1-term feed.
- `mc7j2l.py`: an asm goto statement removed and its labels moved into other asm goto lists
  (list labels are uncounted).  `mc7dead.py`: dz/dv dead blocks merged or retargeted.
- `mc7comp.py NAME|none [-save KEY OUT]`: a counted removal compensated by one free list edit
  (any mode_client label added at either end of any asm goto list, or one label dropped).
- `mc7nsingles.sh BASE TAG`: mc1 singles on a near-miss base (= pairs with that near miss).
- `mc7flip.py`, `mc7rev.py`, `mc7revsub.py`, `mc7sub.py`: the latch-flip toggles (below).

What was found:
1. Chain arms, k61l, dy: no shorter position.  k61l 1-term at all 279 positions: best 174;
   the dy feed / ybk back edge (1 term each, not 2) have no other position in
   clientEraseBlockI (122+).  Chain arms 7/11/9 removed from the chain and placed as
   `if (cp..) mode = X;` anywhere with 1-4 terms (arm 9: 1): best 14 (arm 11 after arm 7 =
   mc6chain's order space), 28, 30.  Arms are positional.
2. Same-target pairs -> one feed (ndl, dtg, u2): all ~290-340.  Not close.
3. asm goto statement -> labels into other lists (mc7j2l, every single/2-label statement):
   none.  Near: c9's JMP(hdd4,hdd5) -> hdd4 into case 5's JMP(s4,c12), hdd5 dropped: 14 (two
   adjacent tail blocks swap: the hdd4 log and u2's usage(2)); JMP(s4,c12) -> s4 dropped, c12
   elsewhere 22.  JMP(c10) -> c10 into the rok list 116.  dz->dv merge: 60 (= dropping the
   edge; the second dead block itself matters, not where the edge goes).
4. Counted removal + one free list edit (mc7comp, 22 removals x ~1500 edits): the c9 fail
   feed + `hc4` added to `JMP(s4, c12)` -> **8**, and that 8 is purely the loop latch compare
   flip (`cmp esi,eax; jle` -> `cmp eax,esi; jge`, attempt 3's mechanism).  dtg(156949) + many
   adds -> 8 (the same flip).  t5 16, s4c12 14, c3 22, t4 30, c11 32, pins 35/41: no gain.
5. **The latch flip is the common wall.**  Removing almost any case-head feed (c9, t5, dtg2,
   c11 ...) flips the latch compare.  PRE dumps: the latch phi is the third prephitmp PRE
   allocates; in the reference state it is a fresh name (prephitmp_580 > argc_69), after a
   case-feed removal it takes a recycled low name (prephitmp_4 / _7 / _9) -> operands swap.
   So the removal frees one more SSA name before PRE (a CFG change around the case head,
   not the feed's own names: re-inserting a 1-term feed anywhere never repairs it, mc7relocall
   on the c9 base, 11 feeds x 280 positions, floor 8).
   Toggles tried: mc5nat's rules and oneArg/wbArgs/bpArgs body respellings (mc7flip, 196
   each): none flips it.  Reverting attempt 3's `x = argv[i + 1]; i++;` to `x = argv[++i];`
   in all 7 arms (mc7rev) flips it back **only** on the c9 + dtg(156949) base (12 -> 4); every
   subset of arms on the pure-flip bases c9 / dtg2 (mc7revsub, 127 each): none.  Singles and
   pairs (within 100) of the near misses on the all-reverted base: none.
6. (Before the steps above, a dead end on the 63 base.)  l4 =
   drafts/mode_client_a7_near4.c, 61 tricks, 4 lines (fail's c9 and dtg(156949) feeds gone,
   hc4 into case 5's list, all arms `x = argv[++i]`): case 9 / case 11 call blocks swapped.
   Singles, pairs within 60, list edits, feed relocation, chain term counts: none.  Superseded
   by the 58 state, which got c9 without the latch flip.
7. What made the steps work: the latch flip of finding 5 depends on the state; after steps
   1-3 the c9 removal no longer flipped it (comp on the 60 state: c9 + `ork6` and dtg2 +
   `ork6` both IDENTICAL alone; together 12).  So re-running mc7comp after every banked
   change matters more than toggles.  Two levers alternate: a counted removal + one free list
   label (mc7comp / mc7loop), and a near miss + one count-neutral feed relocation
   (mc7relocall).
8. mc7loop's full pass on the 59 state found only `ac` (step 5); before it, nothing for dtg2
   12, arm11 14, c11 18, c3 20, t5 26, t4a 28, dz 28, pins 35/41, kk 76, the rest 100+.  On
   the 58 state only dtg2 (12), c11 (18), t5 (22) and the rok/fail cold labels (315/285) were
   re-run with list edits (no hit; the rest of that pass was stopped, its numbers should be
   close to the 59 pass).  Every 1-term feed relocated on the 58 near misses dtg2 (12), c11
   (18), t5 (22) and arm11 (22): none (build/mc/w7/ra_m_*.log).

### Don't retry (attempt 7)

- 1-term positions for k61l, dy, ybk, chain arms (as `mode = X` statements anywhere).
- Merging same-target feeds; asm goto statements into other lists; dz/dv merges/retargets.
- Relocation on the 58 state's near misses dtg2/c11/t5/arm11 (item 8).  (mc7loop on the 58
  state is worth one full pass, since only part of it ran.)
- mc5nat / helper-body respellings as latch-flip toggles; argv[++i] subsets on c9 / dtg2.

### Ideas for attempt 8

- Two list edits with one removal (mc7comp has only one; pairs of adds for the 12-22 line
  near misses dtg2, arm11, c11, c3 on the 58 state, restricted to labels within the case
  region and lists 0, 2, 3, 5).
- Near miss + relocation + list edit (three-step), starting from the dtg2 (12) and arm11
  near misses; a relocation hit at step 1 came from a near miss that list edits alone could
  not fix.
- The latch flip mechanism (finding 5): dump -fdump-tree-all for a flipped / unflipped pair
  and find which release frees the extra name; a natural toggle would reopen t5/c11/dtg2.
- The cebi JMPs (efail x2, dy) were not in mc7comp's edit set (mode_client lists only): add
  clientEraseBlockI's labels and lists.

## State after attempt 6

**63 tricks** by README's categories (84 before): 20 `__builtin_constant_p` and one cold
label (`hdd5_c`) gone, no new hint kind, no borderline shape.  Whole object IDENTICAL BYTES,
full build SHA256 10dac648...1971c, progress 617/617.  build.sh unchanged.  mc1.count now
uses README's mapping (it prints 63, the same as README's categories).

| Category | Att. 5 | Now | Where |
|---|---|---|---|
| `__builtin_constant_p` | 51 | 31 | relocated with fewer terms: t5 4->1 and c3 4->1 (default case), c11 4->1 (fail), t4 4->2 (rok block), s5 4->1 (from after the reboot tail to fail); mode chain 17->12 (2+5+5 in the order 9, 11, 7); fail's dtg(205569) dropped |
| asm goto | 13 | 13 | (rok list lost c1/c10, fkbo list fa2-fa4: free label drops) |
| pins | 6 | 6 | |
| cold labels | 7 | 6 | hdd5_c gone |
| `if (0)` / unreachable | 3 / 3 | 3 / 3 | |
| hand-inlined clientEraseBlockI | 1 | 1 | |

Not a plain removal everywhere: five feeds were *relocated* with fewer terms (same target,
another source block).  The count drops because a feed's job is a frequency, and a colder
source needs fewer terms for it; reported as such to the user.

## State after attempt 5

**84 tricks** by README's categories (87 before): the three empty `asm volatile` barriers in
the dead blocks (`dy:` in clientEraseBlockI, `dv:` and `dz:` at the end of mode_client) are
gone; the blocks are now `if (0) { L: __builtin_unreachable(); }` (dy keeps its ybk feed).
No new hint, no borderline shape.  Whole object IDENTICAL BYTES, full build SHA256
10dac648...1971c.  build.sh unchanged.

How README's categories map onto the source (mc1.count misses some of these, see below):
- "asm goto" 16 -> 13 = the 13 `asm goto` statements (JMP uses + `__asm__ goto`) other than
  the `-r` head's `"a"(i)` one, plus the 3 barriers (now 0).
- pins 6 = bpArgs `"a"(i + 1)`, the -i/-p `"d"(i + 1)`, the `-r` head's asm goto `"a"(i)`,
  fkbo's `"X"(&fkv)`, rok's `"m"(rko)`.
- mc1.count (83 before, 83 now) counts the `"a"(i)` asm goto in both columns and neither the
  barriers nor X/m: README total = mc1 total + 1 (X, m minus the double count) + barriers.

| Category | Att. 4 | Now |
|---|---|---|
| `__builtin_constant_p` | 51 | 51 |
| asm goto + barriers | 16 | 13 |
| pins | 6 | 6 |
| cold labels | 7 | 7 |
| `if (0)` / unreachable | 3 / 3 | 3 / 3 |
| hand-inlined clientEraseBlockI | 1 | 1 |

## Attempt 6

84 -> 63.  Tools (tools/wip/dehint/, logs and states in build/mc/w6/, dumps build/mc4/m6*):
- `mc6short.py BASE.c OUT.c [-auto]`: the lever.  For each multi-term feed: remove it, put a
  1-term (then 2-, 3-term ...) feed into the same target after every `;` / label of
  mode_client (`mc6feedpos.py` positions; ~240), take the IDENTICAL hit nearest the old feed,
  go on.  `-auto` finds the feeds by pattern (pass 2+).  `mc6feedpos.py FEED_RX TARGET`: the
  same for one feed, prints all hits.
- `mc6chain.py BASE.c`: the mode = 7/11/9 chain with 0..6 terms per arm, every arm order,
  `else`-chained or separate ifs (4116 variants at -max 6).
- `mc6f2l.py`: each feed replaced by its target added to an existing asm goto list (none).
- `mc6dead.py BASE.c dz|dv`: dead block + its edge replaced by a feed near it (none).
- `mc6walk.py` / `mc6walk2.py`: walks over list label drops/adds (+ new feeds) from the base
  with all case feeds stripped (`mc6case_order.py` strips them and prints the case order).
- `mc6v_one.py` (oneArg bodies x -e / -c / -w call sites), `mc6v_case.py` (shared case 4/5
  and 7/12 bodies), `mc6v_ceb.py` (clientEraseBlockI natural / a real call): for mc2try.py.
- `mc6keys.py TAG`: case heads' bbro keys from an mc4dump (rough bb->call mapping).
- mc1.count follows README now: asm goto with an operand is a pin, `"X"`/`"m"` asms are pins,
  empty asm barriers count with the asm gotos.

What moved:
1. Feed relocation (mc6short pass 1, 84 -> 71): a feed sends 1/2^k of its source block's
   flow (attempt 5), so the frequency a 4-term feed from `fail` adds can come from a colder
   or smaller block with 1 term.  t5 (default case head, 1 term), c11 (fail, 1), c3 (end of
   the default case, 1), t4 (inside the rok block, 2; no 1-term hit), s5 (fail, 2 in pass 1,
   1 in pass 2).  Many positions hit for t5 (7 1-term) and c11 (17); c3 had exactly one.
2. Free singles then (mc4greedy): fail's dtg(205569) feed, rok list c1/c10, fkbo fa2-fa4
   (-> 70); MCCHAIN=lists greedy: 4 of the 9 arm's 5 terms (-> 66); pass 2: s5 2 -> 1 (65).
3. mc6chain on that base: arms in the order 9, 11, 7 with 2, 5, 5 terms (12 for 13) -> 64.
4. Greedy: cold label hdd5_c free (-> 63).  Pass 3 shortening, mc6f2l, chain sweep again
   (-max 5): nothing more.

Mechanism notes:
- Removing every case-head feed (34 cp: chain, t4, t5, c11, c3, c9) costs only 72 lines:
  the case blocks come out 10, 9, 12, 1, 7, 3, 2, 5, 4, 8, 11 against the reference's 10,
  12, 1, 3, 4, 5, 2, 8, 9, 11, 7.  The case bodies' source order does not change it (12
  permutations, same order), so ties are not broken by bb index.  Greedy walks over list
  label drops/adds (and new 1-3 term feeds) from there stall at 56-58: the order needs the
  fine-grained per-head amounts, which the relocated short feeds supply more cheaply.
- Chain arms are not goto feeds: an arm `mode = 7` is threaded through the switch, and
  replacing an arm with a `goto c7` feed of any length from any position never matched
  (best 12/4/22 lines for arms 7/11/9).

Searched with no hit:
- oneArg bodies (DECL x TEST x TAIL x mode-test position, 62 bodies) with -e or -c calling
  it: best 6 (the -w flip stays); with -w calling it: best 4 (then -eb's own test order
  flips: the two inlined copies take the same ifcombine order).  mc5nat -only on both bases:
  no change (all 6 / 4).
- Shared case bodies: `case 4: case 5:` with one HDD test and a mode test (3 shapes): 258+;
  gcc does not thread the inner `mode == 4` test (the reference has two separate HDD tests
  and no mode compare), so 4 and 5 were separate cases.  7/12 sharing the dummy test (`arg
  = NULL` or `?:`): 251+.
- clientEraseBlockI as a natural static function or a call to clientEraseBlock: 273; with
  einv kept cold: 198.
- The Linux v1.16 build has no client mode (no client strings), so it can't tell the
  original switch shape.
- Per feed (63 state): its target added to any asm goto list instead (mc6f2l): best 8
  (dtg 156949, c9); dz block + JMP(dz) replaced by a 1/2-term feed within 300 chars: 60.

### Don't retry (attempt 6)

- Shared case bodies for 4/5 or 7/12; case body source order (also without the feeds).
- oneArg body spellings for the -e/-c/-w bases (6 / 4 lines, see above).
- Feed -> list label replacements; dz/dv dead blocks -> nearby feeds.
- mc6short / mc6chain again on the 63 state without another change first (pass 3: none).

### Ideas for attempt 7

- Relocation for the other hint kinds: an asm goto list's edges (e.g. JMP(s4, c12) 44, the
  j_s4-s4 drop is 8) might be replaced by short feeds from a cold block; only a gain where
  one statement is replaced by fewer counted items (or the list goes with a dead block).
- Relocation with 2 changes at once: remove two 1-term feeds and search one new 1-term
  feed (pairs of positions are too many; restrict to the removed feeds' targets).
- t4 is still 2 terms (no 1-term position); the chain arms 11 and 7 still 5 each: try
  splitting the chain (`if (...) mode = 7;` placed before netGetInfo / at fkN, only for
  arms that need fewer terms there), or the arm values in other order with the 9 arm first.
- The k61l feed (2 terms, `(char *)` form) and the dy feed in clientEraseBlockI (2 terms)
  were not in mc6short's patterns: extend it to `i`-based and clientEraseBlockI feeds.

## Attempt 5

87 -> 84.  Tools (tools/wip/dehint/, logs in build/mc/, dumps in build/mc4/m5*):
- `mc5v_dead.py` (dead-block contents: hit `all_ur`), `mc5v_one.py` (-e/-c through oneArg,
  `static inline`), `mc5v_ip.py` (-i/-p through an optArg helper), `mc5v_bp.py` (bpArgs
  caller side: out-params, index returned): all for mc2try.py.
- `mc5nat.py BASE.c [-only]`: mc3nat's rules plus new ones for attempt 4's shapes (helpers,
  reboot tail, case bodies, -keys/-ip spellings), on the base alone or crossed with its near
  misses.  `mc5drift.py RULE@K ...`: singles and pairs of near misses on drift bases.
  `mc5combo.py KEY ...`: score one combination of mc1 keys.
- mc1.py's template knows the new dead-block spellings and has slots `fk_X1` / `rk_m1` for the
  X and m asms (old spellings kept for old bases).  Singles on the new base:
  build/mc/m5_singles2.json (same numbers as before the barrier removal).

What moved:
1. The barriers: `dv:`/`dz:`'s `asm volatile("" ::: "memory"/"cc")` and dy's `asm
   volatile("")` dropped, each alone and all three together IDENTICAL BYTES.  The blocks are
   dead (`if (0)`), reached only by asm goto edges and dy's feed; what the edges need is a
   block that ends in `__builtin_unreachable()`, not its contents.  Replacing the
   unreachable with `return 0;`, `goto fail;`, `goto dtg;` or nothing: 60-356.

Profile_estimate findings (build/mc4/m5base/pe_mc.txt, the parsed dump):
- A cp feed's branch is "no prediction heuristics: 50%" at profile_estimate (cp is folded
  later), so each `&&` term halves the flow sent to the target: a k-term feed sends 1/2^k of
  its block's flow.  Feeds whose target ends in a noreturn call (u2) get the noreturn
  heuristic (~0%) instead.  asm goto edges are "predicted to even probabilities".
- The switch region is tiny in frequency (the option loop holds the maximum): case heads
  have frequencies 3-7 of 10000.  Their bbro keys are the priority form
  -(1000000 + 100 * edge_freq + bb_freq), so a feed decides the order by a unit or two
  (removing t5's feed: bb 118 from 5 to 3, key -1000405 -> -1000403, after c2's -1000404:
  the 8-line near miss).  All switch edges are even (13 targets), so natural code gives the
  case heads equal keys; feeds or extra real predecessors are the only way to order them.
  That is why the case-order near misses (t5 8, c11 10, rok's c1 12, ...) have no natural
  compensation: nothing natural changes one case head's frequency by one unit.
- The -w arm's 6-line test-order flip (also in attempt 4): ifcombine builds
  `_x = a == 0; _y = argc == i + 1; _z = _x | _y`, and the expander tests the lower SSA
  version first.  In the base ifcombine gets fresh names (argc compare 636 < 637), in a base
  where -e calls oneArg it pops recycled names from the free list (157 / 146: flipped).
  The free list at ifcombine holds names released after release_ssa (045t), i.e. by the
  passes after ipa-inline, so the spelling of an inlined helper's body is the lever, not
  the spelling of mode_client (all mc3nat rules left it at 6).

Searched with no hit:
- Triples of the base's near misses within 35 lines (MC2SKIP fa*, ~1100): none.
- mc5nat on the base: 30 count-neutral IDENTICAL rewrites (eqarg, keys, ipinc, tail, oa_i,
  oa_ret, usage0, nma2, help, cinfo, ...); near: decl_ip / decl_reboot / wb_arg2 2,
  argvi1 4.  Crossed with the 20 near misses within 40 (2018): none.  mc5drift (12 drift
  rewrites x the 14 near misses within 22, singles and pairs, 1260): none.
- -e or -c through the shared oneArg (two call sites): 6 (the -w flip above), with or
  without `static inline`; -e and -c both (three call sites): oneArg is not inlined (10177):
  oneArg's size is 31 and max-inline-insns-auto is 30, so only the called-once rule (overall
  growth negative) inlines it; `inline` doesn't help with three sites.  mc3nat on the -e
  and -c bases: all 6.
- -i/-p through `optArg(argc, argv, &i, dummy)` (+ `if (arg != dummy) log`, or the message
  as an argument), shared or one arm, plain or `static inline`: 37-78; the `arg != dummy`
  test is not threaded into the helper's branch.  Worse than dropping the pins (35/41).
- bpArgs without the pin, caller side: void with both out-params, the new index returned:
  410-459 (the out-param/`&arg` forms change the arms' predictions); plain removal 30.
- Pair compensations by hand: t5 + rok's c2 edge 60, t5 + c11 26, t5 + c3 245, t5 + s4 16.
- The X / m asms (fk_X1 358, rk_m1 235, both 385) are needed.  The hinted clientEraseBlockI
  body moved into the global clientEraseBlock (gcc inlines it): 78 (the out-of-line copy
  changes).

### Don't retry (attempt 5)

- Dead-block contents other than `__builtin_unreachable()`.
- More call sites for oneArg (3 do not inline); -i/-p helpers with a dummy-test after the
  call; bpArgs out-param / index-return forms.
- Natural compensation of the case-head feeds (t5, c11, c3, c9, t4, rok's c-edges): their
  job is a one-unit frequency difference between switch targets with even edges.

### Ideas for attempt 6

- The case-order feeds can only go with a real structural change of the switch: a case head
  with a second real predecessor (a case body shared by a goto or a fall-through the
  original may have had), or a different dispatch (the reference's jump-table order is
  fixed, but which blocks feed which case is not).  Look at the Linux v1.16 build's
  mode_client for how the cases are laid out.
- The -w flip with -e through oneArg: vary oneArg's body (locals, statement order, the
  `*pi` update) to change how many names it releases before ifcombine; a base with -e and
  -c as calls predicts those arms evenly and may free feeds in the option loop (u2's loop
  head feed, k61l, the kk construct) -- run singles on it once it is IDENTICAL.
- mc1.count could learn README's mapping (barriers, X/m, the double-counted "a"(i)).

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
