# options de-tricking

Goal: `build/op/reference.o` (copy of a matching build/obj/options.o) byte-identical with fewer
hints.  69 tricks at the start of attempt 1 (README.md's list).

## State after attempt 30

**0 tricks** (15 before), plain `-O3`, and three borderline shapes fewer.  The closures of
attempts 13-29 held two counts fixed that were ours, not the original's: the int options'
getIniU32 blocks at 37 (the INI_INT macro's 15%) and, read off the layout against them,
xellbutton's constant-0 block at "exactly 37".  With optIniInt returning early on the *good*
path (`if (!bad) return getIniU32(name, def);`, then the warning) gcc predicts the call at
10.1%, the eleven blocks are 25, a natural parseButton's constant-0 block (29) pops ahead of
them with no tie, and the natural heap gives every other tie order of the reference.  Gone:
parseButtonX and its three dead tests, the macid memset and asm goto, dualboot's asm goto,
the rev feeds and dead sprintf, dz1/dz2; and with them the INI_INT macro (optIniInt is
called), parseButtonPart (parseButton is one else-if chain, split by gcc) and optIniBoolG
(one optIniBool whose warning arm sets `on = 0`).  Full build SHA256 10dac648...1971c.  See
"## Attempt 30".

## State after attempt 29

**15 tricks** (16 before), and **plain `-O3`**: the `--param builtin-expect-probability=83` and
parseButtonX's power expect are gone; three dead `__builtin_constant_p` tests in parseButtonX
(one more than before) take their place.  Attempt 28's "the power edge needs 82.13-83.09%"
holds only while the power block stays at 103: bbro never keys that block, so its count is
free, and at 52 the constant-return heuristic alone (67%) gives the else edge its 17.  See
"## Attempt 29".

## State after attempt 28

**16 tricks** (17 before).  The user accepted attempt 23's dead-sprintf candidate
(drafts/options_applyIniOptions_candidate.patch, now in src): the rev feeds' last two expects
are gone and a dead `sprintf` in dz2's arm takes their place (counted as one dead block).
parseButtonX's power expect is the only reader of the --param left; attempt 28 found no
spelling that frees it (see "## Attempt 28").

## State after attempt 27

**17 tricks, unchanged** (no match; src/ untouched).  Audit of attempts 24-26's closures:
op25map.py's maps are unsafe (unmatched TAG ids keep their own id and collide; a TAG head
mapped to a REFTAG non-head never compares), and of the files it wrote m_dzall.txt,
m_nodz2a.txt, m_xa.txt (and m_nodz1c.txt) fail a positive control (the known answer
injected: no hit).  Fixed generator op27map.py (gap pairs, head fix, drop list, collision
check) and op27ctl.py (controls).  Every attempt-25/26 replay re-run with a map that passes
its control: **no verdict changes** (dzall: -ext 0, drop 0, move 0, swaps 0/0, op15sim
singles 0 and pairs +-4 0, deleted-entry hits = attempt 25's window; xa/xb/xc joint dz1 x
dz2 keys 0 with the control passing; attempt 26's a26m map passes).  Attempt 24's dominance
argument confirmed in profile_estimate dumps (op27dom.py: a live call block the test doesn't
dominate gets no call heuristic; the opposite, dominated edge does).  Attempt 26's untried
private parseButton copy for xellbutton2 (op27y.py, 57 feed shapes x 2 copy positions): the dummy needs its own
asm goto to survive (a feed-only dummy is gone by bbro), and a dummy fed mid-function drains
its flow from every later block (rev 554 -> 546-550): best 304, 850-1000 with dz2 in its
window.  See "## Attempt 27".

## State after attempt 26

**17 tricks, unchanged** (no match; src/ untouched).  Attempt 25's last lead (dz2 pushed
from xellbutton's trace after the bootFlags reload) is closed by the CFG: the reload block
193 joins the parseButtonPart-nonzero path (191's ne edge) and the default arm (192), and an
asm goto can only push after 193's deletion from a block that is on those paths and *not*
on the matched-name paths (262, the jump-threaded store copy).  Every test gcc can decide
on those paths is `v != 0`, which the matched constants and an unknown nonzero part result
share, so no source shape separates them (else arm, end of block, nested ifs, re-tests,
local flags copy all put the asm goto on 262's paths too, which moves 262's reload: `xk`).
Full replay map (op26inj.py, every position of every r3/r4 event group, extracted dummy):
the only pushes that work are 188 after `visit 193` (-8..-19), anywhere in 198's trace
(xellbutton2's inlined parseButton: -6..-8, -12..-19) and inside dualboot's parseButton
(244/245, -8..-19), plus today's 251 (-6..-8).  The wide windows are all in parseButton's
inlined body, where no applyIniOptions statement can sit.  See "## Attempt 26".

## State after attempt 25

**17 tricks, unchanged** (no match; src/ untouched).  The whole dummy group (dzall, 11
tricks, 304 lines) can't go: every block count is the same with and without it, and the
p1/sim3 replay of the dzall heap finds no real-key fix (singles, pairs +-4, any one insert
dropped or moved, one or two push-order swaps, all 8192 OPT/G assignments: best 280).  The
only single operation that reproduces the reference order is an entry pushed in the macid
chars warning's trace (149, dz1's push point) and visited by xellbutton2's or dualboot's
trace, and 149's trace has no other successor.  dz1's push point is unique in every
replay; dz2 could also be pushed from xellbutton's trace (keys -8..-19, wide enough for the
rev feeds to lose both expects), but only after the threaded bootFlags-reload copy that ends
that trace, which no statement maps to (`xa`-`xc` 191 lines, joint key replay 0 hits; `xk`
changes code).  See "## Attempt 25".

## State after attempt 24

**17 tricks, unchanged** (no match).  The rev feeds' last two expects (e2, e3) can't be
replaced by a *live* call: gcc 6's call heuristic predicts an edge only when its source
dominates the call block, and a dead test's edge dominates only dead blocks, so a call that
helps a dummy's edge is always a dead call (attempt 23's candidate).  Without a call, every
split (both arms to dummies) gives dz2 >= 20% of its flow (DS rounding k = 1; unrounded 27%
with the labels swapped), so dz2 <= 8 with dz1 >= 39 needs a call, an expect or a
loop-iteration predictor; nothing else exists in gcc 6 (no PRED_GOTO from the C front end:
measured).  Two-label asm gotos get even probabilities (a third each) and wreck the live
flow (887-1092 lines).  New fact: the live rev code as early returns (`if (xb.blSuffix[0])
return; s = getIniValue("rev"); if (!s) return; sprintf ..`) with the feeds after it is
IDENTICAL, not landed (nested ifs read as the author's).  src/ change: parseButtonX's
comment now gives the z feed's measured numbers (45% of the else arm: 71% and 63.4%; the old
text said 3/8: 50% and 75%); bytes identical, full build SHA256 10dac648...1971c.  See
"## Attempt 24".

## State after attempt 23

**17 tricks** (18 before).  Removed (1): the rev feeds' e1 `__builtin_expect` (dz1's inner
test).  New fact: a test whose two arms both go to dummies gets PRED_NORETURN on both edges,
so first match ignores it and the test keeps its own (natural) prediction; dz2's inner test
now sends its other arm to dz1 (`if (expect(cp(+15), 0)) { if (expect(cp(+16), 0)) goto
dz2; goto dz1; }`), which gives dz1 its count (39, window 39..79), so dz1's own test needs no
expect (it gets no flow; it only keeps that return from being an early return).  Windows
(heap replay, one key at a time): dz1 39..79, dz2 7..8 only; e2/e3 each [13.8%, 18.05%) with
the other at 17%; bxe (82.13%, 83.09%], and its natural value can never fit (the 0x11 join
and remopower scale together: P <= 83.17% for any call-site count; natural 83.25%).  Full
build SHA256 10dac648...1971c; progress 617/617.  Candidate (not landed, for review):
drafts/options_applyIniOptions_candidate.patch, the rev feeds with no expect at all (a dead
`sprintf` in dz2's arm for the call heuristic, the dummies' labels swapped so gcc doesn't
round the split's probability; full build matches).  See "## Attempt 23".

Remaining (17 by README's count): `--param builtin-expect-probability=83`; 7
`__builtin_constant_p` (parseButtonX's z feed 2, the macid memset 1, the rev feeds 4); 3
`__builtin_expect` (parseButtonX's power, the rev feeds' two); 2 `asm goto` and 2
`__builtin_unreachable` (dz1, dz2).

## State after attempt 22

**18 tricks** (19 before).  Removed (1): parseOption's setBool `__builtin_expect` (po1).
Attempt 21's "one knife edge" was wrong: the binding constraint is the "\n" block's own
epilogue copy (its count must reach 57, 10% of the entry 570; the natural 9.22% gives 41,
and no entry scaling helps: 570 x 0.789 x 9.22% < 57 always), so the setBool edge needs
>= ~12.7%, i.e. no early-return prediction (13.7% = call + `== 1`).  The "\n" block can't
simply move to the end (`goto done` after bad: same .text, but the "\n" literal is then
first expanded in macid's block and .rdata moves).  The shape that works keeps it early
and sends it to a join: `ok = 0; if (setBoolOption(opt, val) == 1) { log "\n"; ok = 1; }
else if (val) { ..value options.. }  if (ok) return 1;`, with attempt 21's macid helper
(`macidRest(&xb.macid[1], val, 5)`, trip count unknown at profile_estimate).  `val &&
vlen` stays (still needed), vvn isn't needed.  Full build SHA256 10dac648...1971c;
progress 617/617.  See "## Attempt 22".

| Where | Shape | Why it's worth a look |
|---|---|---|
| parseOption, the bool option | `ok = 1` in the setBoolOption arm, the value options in its `else`, `if (ok) return 1;` after them | Borderline: live but redundant (a `return 1` in the arm would do).  The join takes the early-return prediction off the setBool edge (13.7% instead of 9.2%); VRP1 threads it away.  A new `set` flag, `set = setBoolOption() == 1` or `== 1` re-tests all give the same bytes |
| parseOption, macid | `static void macidRest(uint8_t *mac, const char *val, int n)`, called once with 5 | Borderline: a helper that exists to match, with a constant argument.  Its loop exit is 9% (unknown trip count) instead of 1/6.  A never-written `static int macidRestLen = 5` bound (sp5) gives the same bytes but reads as a dead hint, so the helper landed |

Remaining (18 by README's count): `--param builtin-expect-probability=83`; 7
`__builtin_constant_p` (parseButtonX's z feed 2, the macid memset 1, the rev feeds 4); 4
`__builtin_expect` (parseButtonX's power, the rev feeds' three); 2 `asm goto` and 2
`__builtin_unreachable` (dz1, dz2).

## State after attempt 21

**19 tricks, unchanged** (no match; src/ untouched).  Table loops that gcc unrolls don't
reach bxe/bxz: strnicmp isn't pure, so a name loop unrolls only with 2 entries (cunroll's
size rule), and loop predictors predict *no* match where power needs 83%.  New facts: cunroll
(late, after VRP1/dom2/PRE) unrolls loops whose calls are off the hot path, so a guard that
folds only after unrolling is a natural count lever (nodvd/olddvd as a table loop: same code,
other layout); macidSet's loop header sets applyIniOptions' whole scale (do-while: x1.125,
inert crossed).  po1 is down to one knife edge: with parseOption's macid loop trip count
unknown at profile_estimate (helper or never-written static bound, pointer store: exit 9%)
and nested `if (val) { if (vlen)` (unknown 34), both IDENTICAL with the expect kept, the
natural setBool 9.22% fails only because cputemp's head is 285 against exec_th 285 (needs
P(setBool) >= 9.26%, P(val) <= 69.56% or the '=' loop's normal exit <= 78.7%).  See
"## Attempt 21".

## State after attempt 20

**19 tricks, unchanged** (no match; src/ untouched).  Attempt 19's lever (a live,
redundant re-test that VRP1 threads) only moves counts onto thread *targets*: an original
block keeps the share its estimate gave it after the threader reroutes its real inflow.
Jump-thread *copies* get only real incoming-edge counts.  bxz's constant-0 block is a copy (the
null path's copy of the store-and-test block; its 37 is the null edge's 28.5 plus the z
feed's dead edge), so a live test can't lift it.  Its only real flow is G x P(null), pinned
by power = 103.  For bxe, retention adds a whole predictor split (remopower 34-63 where 18 is
needed).  The rev/dz group's blocks are unreachable (no live flow), and the memset and
setBool expects set edge probabilities.  See "## Attempt 20".

## State after attempt 19

**19 tricks** (20 before).  Removed (1): parseOption's vlen `__builtin_expect` (po2).  The
unknown-with-value test is now `if (val && vlen)`: the `val` test lets VRP1 thread the
val-null path straight to the incomplete message, and after PRE's tail merge that block has
the path's whole frequency (113, threshold 57; with `vlen` alone it keeps half, 56) and owns its epilogue
copy; it keeps a second pred, so it stays in place and its literal stays between the
unknown and bad messages.  Full build SHA256 10dac648...1971c; progress 617/617.  po1 (the
setBool expect) is pinned to (16.67%, 18%) by two bb-reorder comparisons; the natural 9.2%
fails both, and only a non-0/1 constant return gives a value in range.  See "## Attempt 19".

| Where | Shape | Why it's worth a look |
|---|---|---|
| parseOption, the unknown-with-value test | `if (val && vlen)` where `vlen` alone decides (vlen is 0 whenever val is NULL) | Borderline: live but redundant, and it matches because the `val` test gives VRP1 a path to thread.  It reads naturally (the message prints val with %s).  `if (val) { if (vlen) ... }` (nested) and `vlen && val` give the same bytes |

Remaining (19 by README's count): `--param builtin-expect-probability=83`; 7
`__builtin_constant_p` (parseButtonX's z feed 2, the macid memset 1, the rev feeds 4); 5
`__builtin_expect` (parseButtonX's power, parseOption's setBool, the rev feeds' three); 2
`asm goto` and 2 `__builtin_unreachable` (dz1, dz2).

## State after attempt 18

**20 tricks, unchanged** (no match; src/ untouched).  Attempt 17's constant-argument lever
doesn't reach the rest: a test on a constant argument folds when ipa-cp or the inliner copies
the body, so its edge is gone before the caller's frequencies are rebuilt (parseButtonX with
`if (def) goto z;` gives exactly the no-feed bytes, 90), and a value-only argument is inert
(predictors don't see values).  Removal costs are unchanged by attempt 17 (rv2 44 ... po1
811).  The macid memset exists only because dz1's asm goto ends the validateString false
edge's first block (gcc 6's call heuristic scans that block alone: 71% with the memset, 50%
without); moving the asm goto behind a real call loses the crossjump of the two macid
warnings.  The z feed can't be one cp test (9 forms x 3 places), and parseButtonX at more
sites is split again.  See "## Attempt 18".

## State after attempt 17

**20 tricks** (22 before).  Removed (2): the hand-written `_parseButton.part.0` (its `cold`,
`section(".text.startup")`, `regparm(1)` and asm label) and parseButton's winbutton
`__builtin_expect`.  The part is now `static int parseButtonPart(const char *s, int def)`
(`int b = def;`), called as `parseButtonPart(s, 0)` from parseButton and parseButtonX.  The
always-0 argument does two jobs: the bigger call lets fnsplit split parseButton at the call
alone (split size 4 > call overhead), so ipa-profile sees only zero-frequency calls and
promotes the part to unlikely executed (size optimised, .text.unlikely), and ipa-cp's
`.constprop` clone is created after baseFileExists' split part, so it is expanded (FDE)
second as in the original.  Without `cold` the winbutton edge needs no expect.  Full build
SHA256 10dac648...1971c; progress 617/617.  build/op/reference.o is now this build's
options.o (the old one is reference_a16.o); optlib also normalises `.constprop.N`.

| Where | Shape | Why it's worth a look |
|---|---|---|
| parseButtonPart (and its two calls) | a static helper for the names after winbutton with a `def` result parameter that every caller passes as 0 | Borderline: live but redundant (the helper could return 0 itself), and it exists to match: the argument is what makes gcc split parseButton at the call (zero-frequency edge -> unlikely helper) and clone the helper late (emission order).  The helper itself is the original's ipa-split part written out by hand |

Remaining (20 by README's count): `--param builtin-expect-probability=83`; 7
`__builtin_constant_p` (parseButtonX's z feed 2, the macid memset 1, the rev feeds 4); 6
`__builtin_expect` (parseButtonX's power, parseOption's two, the rev feeds' three); 2 `asm
goto` and 2 `__builtin_unreachable` (dz1, dz2).  See "## Attempt 17".

## State after attempt 16

**22 tricks, unchanged** (no match; src/ untouched).  The natural parseButton split (7 tricks
gone at once) is 321 on today's source, and the fibheap replay shows only two keys differ,
both in the xellbutton site's inlined split header: its `!s` block must be exactly 37 (is
29) and its remopower block's key <= -1001718 (is -1001717); the old extra dx entry is no
longer needed.  Both are closed by arithmetic: the header's ratios are parseButton's own
(shared with xellbutton2 and dualboot, whatever the spelling), `!s` = G x 21.6% needs G >=
169 while the call block (<= 146) and the constant-store join (power-success edge <= 86) pin
G <= 132.6, and the remopower edge needs a power probability <= 83.0%.  OPT/G site flips
(5506 assignments) can't move those blocks (best 311).  Hints moved into the shared
parseButton: a two-test feed changes the split (header size limit), single-test feeds give
61%/80.9% where ~48% is needed, and xellbutton2 then ties.  See "## Attempt 16".

## State after attempt 15

**22 tricks, unchanged** (no match; src/ untouched).  The cheapest removals are closed by
mechanism: rv2 (dz2's feed) needs dz2 extracted at key -7/-8, and dz2's count can only come
from a dead feed (its asm goto edge is 0% under PRED_NORETURN); no real key change (singles
over all entries, pairs within 3, joint +-1 over the 13 getIniBool blocks) and no OPT/G
assignment of the 14 boolean sites (all 16384, best 20 lines from 44) replaces it.  bxz's
constant-0 block must be 37 to pop ahead of the key-37 getIniU32 blocks; naturally it's 29.
pbe is forced by the hand-written part's `cold` (PRED_COLD_FUNCTION outranks every natural
predictor).  See "## Attempt 15".

## State after attempt 14

**22 tricks, unchanged** (no match; src/ untouched).  No natural zero-byte block reaches bbro:
a census of every object (op14scan.py, 617 functions, 9777 blocks) finds empty blocks only at
the hinted asm gotos, because bbro's own CLEANUP_EXPENSIVE removes every empty block with a
successor, and empty no-successor blocks come only from __builtin_unreachable.  The push
points (149, 251) have no branch in the reference, so only a zero-byte jump (asm goto) can
give them the extra successor.  Return-register clobbers (int applyIniOptions), a shared macid
warning tail and dualboot spellings change code or are inert.  See "## Attempt 14".

## State after attempt 13

**22 tricks, unchanged** (no match; src/ untouched).  applyIniOptions' stretches as static
helpers (rev, macid, dualboot, dvdkey, cfldv, xellbutton2) are inert or change code; all 12
dz tricks together cost 304 (= dz2 alone), but a fibheap replay (op13sim.py) shows no key
change of any real block within 6 (pairs within 1) does a dummy's job: dz2's key must be 7-8,
and the dummies stand for extra heap operations only a zero-byte block gives.  parseButtonX
isn't split by gcc (called once); called twice it splits at winbutton and ICF doesn't merge.
See "## Attempt 13".

## State after attempt 12

**22 tricks, unchanged** (no match; src/ untouched).  build's late levers (attempts 46-70)
tried on options: helpers with their own IPA-inlined profile for parseOption's setBool test
and vlen tail, int/uint32_t/_Bool/void types of the inlined helpers, non-PHI return
statements (`on & 1`, `on != 0`, ...), nested ifs for every `&&` in applyIniOptions, `i = 6`
loop ends, moving the static helpers in the file.  Everything that keeps the code is inert:
each removal scores exactly what it scores alone (rv2 44, po2 62, bxz 90, pbe 190, dz2 304,
ms 373, rv1 508, po1 811, bxe 818).  Measured gcc 6 predictor values rule out a natural 17%
for setBool unless its success path returns a constant other than 0/1.  See "## Attempt 12".

## State after attempt 11

**22 tricks, unchanged** (no match; src/ untouched).  The vlen near miss is stuck by
mechanism: every join form threads in VRP1, and the copy for the vlen==0 edge carries a
degenerate virtual PHI (the unknown arm's call is on the other edge), so it isn't a
forwarder and cleanup merges the incomplete block into it at the end of the chain.  Without
a join, FRE1 folds any re-test of vlen before profile_estimate, and every natural predictor
points the wrong way.  Named arrays go to the end of .rdata.  See "## Attempt 11".

## State after attempt 10

**22 tricks, unchanged** (no match; src/ untouched).  parseOption's vlen expect has a
near miss: `if (vlen) unk; if (!vlen) inc;` (or an `ok` join) gives identical .text, but
VRP1's threading merges the incomplete block into a copy at the end of the block chain, so
its literal follows bad's (.rdata only; drafts/options_parseOption_vlen_nearmiss.patch).
The rest (setBool's 17%, the power and winbutton expects, the rev feeds and dz dummies) has
no join lever: see "## Attempt 10".

## State after attempt 9

**22 tricks** (25 before, the parent's count).  Removed (3): both `po_hint()` calls (and the
po_hint function and its `dead` local) and parseOption's `optimize("no-early-inlining")`.
cputemp's and gpufan's arms now set an `ok` flag in the log's `if` and `goto bad` on it after
(src comment: borderline).  Full build SHA256 10dac648...1971c; progress 617/617.

Remaining: `--param builtin-expect-probability=83`; 7 `__builtin_expect` (parseButtonX's power,
parseButton's winbutton, parseOption's two, the rev feeds' three); 7 `__builtin_constant_p`
(parseButtonX's z feed 2, the macid memset 1, the rev feeds 4); 2 `asm goto`, 2
`__builtin_unreachable` (dz1, dz2); the hand-written `_parseButton.part.0`.  See "## Attempt 9".

| Where | Shape | Why it's worth a look |
|---|---|---|
| parseOption, cputemp and gpufan | `ok = 0; if (x != -1) { log; ok = 1; } if (!ok) goto bad; return 1;` where the other value arms do `if (x == -1) goto bad; log; return 1;` | Borderline: live, redundant flag (myatou32's `hex` pattern), only in those two arms.  It exists to match: the log block no longer goes straight to the return, so their success edge loses the early-return prediction.  Every myatou32 arm but edramtemp in this form also matches (op9rv.py, ARMS=-edramTemp) |

## State after attempt 8

**16 tricks by kind** (23 by the same count before; the parent's list said 25).  Removed (7): 5
`__builtin_constant_p` and 2 `__builtin_expect`.  The dead feeds now test one shared value per
function: applyIniOptions' `dead = __builtin_constant_p(xb.blSuffix[1])` (macid memset size and
the rev feeds) with `rare = __builtin_expect(dead, 0)` for the rev feeds' 17% tests, and
parseButtonX's z feed tests one cp twice.  Full build SHA256 10dac648...1971c; progress 617/617.

Remaining: `--param builtin-expect-probability=83`; 5 `__builtin_expect` (parseButtonX's power,
parseButton's winbutton, parseOption's two, `rare`); 2 `__builtin_constant_p` (applyIniOptions'
`dead`, parseButtonX's z feed); 2 `asm goto`, 2 `__builtin_unreachable` (dz1, dz2); 2
`po_hint()` + no-early-inlining; the hand-written `_parseButton.part.0`.  No new borderline
shape (the feeds are still counted hints).  See "## Attempt 8".

## State after attempt 7

**26 tricks** (34 before).  Removed (8): every hint in the optIniBool helpers.  optIniBool
and optIniBoolG are now plain result-variable functions (`on` set on every path, one
`if (on)` at the end); optN is merged into optIniBoolG.  Gone: optIniBool's 2 cp arms,
optIniBoolG's 2 cp arms and `!bad` expect, optN's entry cp (`== 1`), off-arm cp and expect.
Full build SHA256 10dac648...1971c; progress 617/617.  See "## Attempt 7".

Remaining: `--param builtin-expect-probability=83`; 7 `__builtin_expect` (parseButtonX's
power, parseButton's winbutton, parseOption's two, the rev feeds' three); the dead cp feeds
(parseButtonX's z feed 2, the macid memset 1, the rev feeds 4: 7 in the source, README counted
14 before, so 8 by its count); 2 `asm goto`, 2 `__builtin_unreachable` (dz1, dz2); 2
`po_hint()` + no-early-inlining; the hand-written `_parseButton.part.0`.

| Where | Shape | Why it's worth a look |
|---|---|---|
| optIniBoolG (noecdremap, nandmu, nosecurity, cygnos, smcnoeject) | a second copy of optIniBool that differs in one statement: the warning arm sets `on = 0` where optIniBool does `return 0` | Borderline: it exists to match.  The G sites need `!bad` at 15% (no early-return prediction), the OPT sites 21.6%; one function for all sites is 120, the G sites unguarded 1789 |
| optIniBool | result variable `on`, `||` flag test (Linux's), `return 0` only after the bad-value warning | Natural; the one return is what gives the OPT sites their profile, flagged only because the mix of `on` and an early return is a choice that steers |

## State after attempt 6

**34 tricks, unchanged** (no match; src/ untouched).  Structural attempt: read the Linux
v1.16 build (tools/ref/xeBuild64) for optIniBool, parseButton, parseOption and applyIniOptions;
tried whole-body shapes of the helpers, live "already on" arms, and the G/N sites written out
in applyIniOptions.  Nothing came near (best 81 lines, everything else 400+).  The Linux build
has the same structure as src, so it gives no new shape to try.  See "## Attempt 6".

## State after attempt 5

**34 tricks** (35 before).  Removed (1): one `__builtin_constant_p` of parseButtonX's z feed;
the feed is now `if (cp) { if (cp > 0) goto z; }` (the opcode heuristic's 75% on `> 0` does
what the second and third 50% tests did).  Full build SHA256 10dac648...1971c.

Remaining: as after attempt 4 with 14 `__builtin_constant_p` (README's count), i.e.
`--param builtin-expect-probability=83`; optIniBool's 2 arms; optN's entry, off arm + expect;
optIniBoolG's 2 arms + expect; parseButtonX's power expect and its 2-cp z feed; parseButton's
winbutton expect; the rev feeds; the macid memset; parseOption's two expects; 2 `asm goto`, 2
`__builtin_unreachable`; 2 `po_hint()` + no-early-inlining; the hand-written
`_parseButton.part.0`.  No new borderline shape (the `> 0` is a counted dead cp test).

## State after attempt 4

**35 tricks** (42 before).  Removed (7): optN's first cp arm (now a plain `return 0`), and
parseButtonX's dx dummy (feed cp + expect, asm goto, cold label, tail cp, unreachable: 6),
replaced by nothing: dz1's rev feed got a `return;` in its (already counted) dead arm.  Full
build SHA256 10dac648...1971c.

Remaining: `--param builtin-expect-probability=83`; 15 `__builtin_constant_p` and 9
`__builtin_expect` (README's count; optIniBool's 2 arms; optN's entry, off arm + expect;
optIniBoolG's 2 arms + expect; parseButtonX's power expect and z feeds; parseButton's winbutton
expect; the rev feeds; the macid memset; parseOption's two); 2 `asm goto`, 2
`__builtin_unreachable` (dz1, dz2); 2 `po_hint()` + no-early-inlining; the hand-written
`_parseButton.part.0`.  No cold label left.

| Where | Shape | Why it's worth a look |
|---|---|---|
| applyIniOptions' rev block, dz1's feed | `if (cp) { if (expect(cp, 0)) goto dz1; return; }` | The `return;` is new, inside an existing dead arm (no builtin added); it does the dx dummy's job (the demon/patchsmc getIniBool tie) through the feed's flow |
| optN | first arm `if (xb.bootFlags & set) return 0;` | Plain optIniBool form, not borderline |

## State after attempt 3

**42 tricks** (44 before).  Removed (2): always_inline on optIniIntI (the copy is gone; the
int options use an `INI_INT(var, name, def)` macro of optIniInt's body, see the review table),
and optN's entry `__builtin_expect` (the dead test is now `__builtin_constant_p(...) == 1`,
whose opcode heuristic does what the expect did).  Full build SHA256 10dac648...1971c.

Remaining: `--param builtin-expect-probability=83`; 18 `__builtin_constant_p` and 10
`__builtin_expect` (optIniBool's 2 arms; optIniBoolG's 2 arms + expect; optN's entry, 2 arms
+ expect; parseButtonX's power expect, dx feed, z feeds and dx tail; parseButton's winbutton
expect; the rev feeds; the macid memset; parseOption's two); 3 `asm goto`, 3
`__builtin_unreachable`; 2 `po_hint()` + no-early-inlining on parseOption; the hand-written
`_parseButton.part.0`; 1 cold label (dx).

| Where | Shape | Why it's worth a look |
|---|---|---|
| applyIniOptions' int options | `INI_INT(var, name, def)` macro, a copy of optIniInt's body with a temporary for the result | Replaces the always_inline copy optIniIntI.  optIniInt can't be early-inlined (3 calls), and the profile needs the body in applyIniOptions before profile_estimate, so the original most likely had the code written out or in a macro; storing var in both arms instead of the temporary gives other code (258) |
| optN | dead entry test spelled `__builtin_constant_p(xb.bootFlags + 2) == 1` | Still a counted dead cp test; `== 1` replaces the expect (opcode heuristic) |
| parseOption, parseCmdOptions, olddvd | unchanged from attempt 1's table | |

## State after attempt 2

**44 tricks** (63 before).  Removed (19): the 3 asm "i" pins (dx's, dz1's, dz2's), both
`if (0)` blocks (the dz labels now follow a `return;` at the end of applyIniOptions), the
dxc/dzc1/dzc2 indirections (not counted: the cold label sits on dx itself, the asm gotos
target dz1/dz2 directly), 4 `__builtin_constant_p` + 1 `__builtin_expect` from the rev
feeds (dz1: `cp { expect(cp, 0) }`, dz2: `expect(cp, 0) { expect(cp, 0) }`), and 6
`__builtin_constant_p` + 3 `__builtin_expect` by merging the four identical optIniBool copies
optC/optE/optS/optU into one, `optIniBoolG`.  Full build SHA256 10dac648...1971c.

Remaining: `--param builtin-expect-probability=83`; 18 `__builtin_constant_p` and 11
`__builtin_expect` (optIniBool's 2 arms; optIniBoolG and optN; parseButtonX's power expect,
dx feed, z feeds and dx tail; parseButton's winbutton expect; the rev feeds; the macid
memset; parseOption's two); 3 `asm goto`, 3 `__builtin_unreachable`; 2 `po_hint()` +
no-early-inlining on parseOption; the hand-written `_parseButton.part.0`; 1 cold label (dx);
always_inline on optIniIntI.

Review table: unchanged from attempt 1 (no new borderline shapes; everything changed in
attempt 2 is still a counted hint, only fewer of them).

## State after attempt 1

**63 tricks** (69 before; README's way of counting).  Removed: optO's copy (its 2
`__builtin_constant_p` and 1 `__builtin_expect`), the `parseOptionInt` asm-label prototype,
the literal-order asm and the `__asm__("")` barrier in applyIniOptions' macid block.
Full build SHA256 10dac648...1971c.

Remaining: `--param builtin-expect-probability=83`; about 28 `__builtin_constant_p` and 15
`__builtin_expect` (optIniBool's 2 arms; the optN/optU/optS/optC/optE copies; parseButtonX;
the rev feeds; the macid memset; parseButton's winbutton expect; parseOption's two); 3 `asm
goto`, 3 `__builtin_unreachable`, 2 `if (0)` dummy blocks; 2 `po_hint()` + no-early-inlining
on parseOption; the hand-written `_parseButton.part.0`; 1 cold label (dxc); 3 asm "i" pins
in the dummies; always_inline on optIniIntI.

| Where | Shape | Why it's worth a look |
|---|---|---|
| parseOption, parseCmdOptions (and options.h) | both return `uint32_t` | Natural, but it steers: the 0/1 result type is what keeps uncprop from returning macid's stricmp result (parseOption) and lets it reuse the call's 0 (parseCmdOptions). mode_build's `if (!parseCmdOptions(...))` is unchanged |
| applyIniOptions, olddvd | `optIniBool("olddvd", 0, 4, 0)` called directly, not through `OPT` | OPT's guard would be `!(xb.bootFlags & 0)`, always true; both forms are identical bytes, the direct call reads better |

Not borderline: macid's nested ifs (success first) in applyIniOptions.

## Attempt 1

Tools (tools/wip/dehint/):
- `optlib.py <file.c> [-v [fn]] [-L] [-np|-p N]`: bdlib for options (reference
  build/op/reference.o, default --param 83, also compares .text.startup and relocs).
- `optricks.py singles|pairs|greedy|show` with each trick as a named edit; groups `po`
  (parseOption) and `aio` (the rest); pseudo-edit `param` drops the --param.  OPBASE=<file>.
- `oppco.py` (parseCmdOptions call forms), `oppo.py` (parseOption with int return, local types).

### Singles (from the starting source)

Only `m_O` (olddvd through `OPT`/optIniBool instead of the optO copy, which takes its 2
`__builtin_constant_p` and 1 expect) is IDENTICAL.  Nearest misses: lit_mac 6 (only the
.rdata order), po_int2 30 (parseCmdOptions), E_exp/C_exp/m_C/m_E 38, O_e1 56, S_exp/m_S 62,
U_exp/m_U/rev2 64, po_exp2 62.  Everything else 100+; `param` 1183, ib_cp1 1187.
`part` (parseButtonPart folded back into parseButton) gives gcc's own split as
`.part.1`s and moves baseFileExists' split too: 40k.

### Landed: m_O, and parseCmdOptions returns uint32_t (asm-label prototype gone)

- `parseOptionInt` existed because parseCmdOptions needs to see the callee's return type
  equal to its own: `if (!parseOption(opt)) return 0;` becomes "return the call's 0" by
  uncprop only when the types agree.  With an int parseOption, uncprop instead turns macid's
  two `return 0` into `return _140` (_140 = stricmp(opt, "macid"), known 0 there), which
  keeps the return value in esi (dump: uncprop1's return PHI has `_140(67), _140(68)`).
  So parseOption stays uint32_t and parseCmdOptions is now uint32_t too (options.h changed;
  mode_build's caller is unchanged in bytes).  `int r = parseOption(); if (!r) return r;`
  doesn't help (forwprop folds the conversion): 30 lines.
- Local types for vlen/len/i don't matter for the int-return problem (it's macid's stricmp).

### Landed: macid's tests nested, success first (literal-order asm and barrier gone)

`opmac.py`: `if (strlen(s) == 12) { if (validateString(s)) { loop } else { chars warning } } else
{ length warning }` gives the original's .rdata order (chars warning first) with no literal
asm, and with the loop first the `__asm__("")` barrier against if-conversion isn't needed
either (IDENTICAL BYTES).  `if (!validateString(s))` first (bad arm first) also fixes .rdata
but needs the barrier (479).  The memset/asm goto dummy in the chars arm still matters
(315 without it, any order).

### parseButtonPart (the hand-written cold global in .text.startup)

- optlib now maps `.part.N` names and `.text.unlikely` to the reference's: ld's script
  puts both `.text.startup` and `.text.unlikely` under `*(.text.*)` in file order, so the
  name of the section doesn't matter for the exe.
- gcc's own split of a natural parseButton (`part` edit, the else-if chain folded back in)
  gives the same part bytes (.text.unlikely == the reference's .text.startup), and with
  `m_bx` IPA inlines the split header into applyIniOptions' 3 calls as the reference has.
  So `part` is free once parseButtonX goes (`part+m_bx` = 335 = `m_bx` alone).
- A plain `static __attribute__((cold)) int parseButtonPart` helper (no section, no
  regparm, no asm label) gives identical code but its FDE comes first in .eh_frame
  (51 bytes differ in the full build) wherever its definition is placed (`oppart.py`, 8
  positions): static functions are expanded before gcc's split parts.  Without `cold` it
  stays in .text.  Not landed.

### parseOption's po_hint / no-early-inlining group

- po1, po2 and po_nei are one unit: without both po_hint calls no-early-inlining changes
  nothing (po1+po2+po_nei = po1+po2 = 231).
- Natural replacement tried (`opbad.py`): cputemp's and gpufan's arms print the bad-value
  error themselves (copy of `bad:`) instead of `goto bad`.  The code is then identical
  (crossjump merges the copies; the call gives PRED_CALL on the edge as po_hint did), but
  the bad string is now expanded first in cputemp's arm, so .rdata order differs
  (158 lines, all string offsets).  Every other subset of arms with copies is worse.
  The original's bad string is parseOption's last: the message was at `bad:` only.

### parseOption's two expects

`opend.py`: 3 setBoolOption test forms x 6 tail forms (`if (vlen)`, `if (val)`, message
inside `if (val) {}`, if/else).  Only the current expects match; `if (vlen)` plain or as
if/else is 62, `if (setBoolOption())` without `== 1` but with the vlen expect is 217.
Draft: `drafts/options_parseOption_badcopies_nearmiss.patch` (code identical, .rdata order off).

### applyIniOptions' copies and dummies (heap ties)

- Every single removal other than m_O moves cold blocks; the nearest (m_C, m_E, C_exp,
  E_exp: 38) swap two `iniBoolInvalid`/`getIniBool` cold blocks (the G tie groups of
  p1/NOTES.md).  `opsub.py` over subsets of m_C, m_E, m_S, m_U, m_N, rev1, rev2, pb_exp:
  nothing IDENTICAL; best 38 (m_C+m_E, m_U+rev2).
- N's five tricks (N_entry, N_cp1, N_cp2, N_exp, m_N) all give the same 172: one unit.
- Copy-internal tricks are subsumed by merging the copy (m_X+X_cp1 = m_X).
- Both dz dummies together with their feeds and asm gotos (7 edits) = 304, the same as
  dz2's alone: optIniIntI's cold `getIniU32` blocks and two optIniBool blocks move.
- All of applyIniOptions natural (copies merged, gcc's own parseButton split, optIniInt,
  no dummies): 1220 lines (662 loose).
- optIniIntI: `inline`/`extern inline` on optIniInt itself instead of the always_inline
  copy: 562, same as plain optIniInt (it isn't early-inlined either way; the 15% vs 21.6%
  of p1/NOTES.md needs early inlining).

### Don't retry

- parseCmdOptions forms with an int temporary (`r = parseOption(); if (!r) return r;`, casts,
  `== 0`): forwprop folds them, 30 lines.  Return-type agreement is the lever.
- vlen/len/i types for an int parseOption.
- The macid block's other orders (opmac.py's table).
- parseButtonPart as a static (cold or not) helper at any source position (FDE order).
- f10.py's optIniBool variants A-D (p1, still in force).

### Next ideas

- parseButtonX is what keeps `part` (and so the hand-written split) alive: with
  `m_bx` + gcc's own split the only cost is the xellbutton dummies' layout (335).  A
  natural shape that rebuilds the `dx`/`!s` frequencies from parseButton's real split would
  remove ~12 tricks at once.  Use p1/sim3.py with dumps of `part+m_bx` to see which heap
  keys move.
- The po_hint pair: a natural call on cputemp's/gpufan's bad edge that vanishes after
  profile_estimate and doesn't expand the bad string early.  The copies draft shows the
  layout side is solved by a real call; only the string order is left.

## Attempt 2

Tools (tools/wip/dehint/): `opxb.py` (natural xellbutton-site forms and wrappers on top of
`part+m_bx`), `opms.py file.c [fn]` (instruction multiset vs the reference, jump targets
dropped: empty = layout-only difference), `optr4.py REFTAG TAG sf sh` (bbro trace lists side
by side, TAG's ids >= sf shifted by sh), `opsim.py` (p1/sim3 replay of TAG with key overrides
and extra round-4 dummy entries, compared with REFTAG's real extraction order), `opds.py`
(search for one dummy entry).  Dumps: `sh tools/wip/aio/p1/run.sh SRC TAG`
(build/v/aio_p1/TAG); `cur` = src at 7afad6c2, `pm` = optricks part+m_bx.

### Starting point

- singles and all pairs (optricks, 780 pairs) from 7afad6c2: nothing IDENTICAL.  Nearest
  `part` 14 (not real: it only calls an undefined `_parseButtonPart`), then 38s as before.

### parseButtonX -> natural parseButton (gcc's own split): 335, not solved

- `part+m_bx` (draft `drafts/options_parseButton_natural_nearmiss.patch`, against the
  attempt-2 source): only the cold layout of applyIniOptions differs; the instruction
  multiset is identical (opms.py).  Traces (optr4.py cur pm 194 3): the xellbutton site's
  remopower block is 17 (edge 103*16.8%) where the reference has 18, so its trace-end key
  -1001717 ties with xellbutton2's and loses; the `!s` block is 29 where the reference needs
  exactly 37 (the goto z feeds); and dx's zero-byte entry (key -71) is missing.
- opsim.py on pm's dump: r3/r4 equal the reference's only with all three: 188=-1001818,
  263=-37 (36 and 38 both fail) and one extra round-4 entry with key 40..72 in the
  xellbutton trace.  opds.py: no single dummy anywhere fixes it without the first two.
- The xellbutton site's probabilities come from the inlined header (parseButton's own
  profile: 83.2% = call 71% + const return 67%), the same for all three sites, so no
  call-site spelling can make the remopower block 18.  Tried (opxb.py), all no better than
  335: assignment-in-if, `== 0`, empty-then/else, `s = getIniValue(); xb.xellButton = s ?
  parseButton(s) : 0` (pointer heuristic 69.8%: 844), `if (s) ...` forms (code changes),
  wrappers `iniButton(name)` (one site or all three) and a void `xellButtonIni()` (all early
  inlined: 335 exactly), `if (!s) return 0` wrapper (745/884).
- Mechanism for a future try: the xellbutton site needs its own profile (a separately
  estimated function that is IPA-inlined, like parseButtonX) or a call-block frequency >= 133
  at IPA-inline time; parseButton isn't early-inlined (it's split first).

### Trimming parseButtonX (opbx.py)

- `nodx` (dx, its feed, the asm goto and the cold label all gone): 38 lines, one getIniBool
  tie swap; opsim says only the dx-like entry (key 39..78 in the xellbutton trace, or the
  other positions opds lists) is missing.
- IDENTICAL: dx's `"i"(3)` pin removed; the cold label put on dx itself (no dxc + goto).
- Not: the feed without expect (312); asm goto out of the power arm instead of the else arm
  (656+: the power arm becomes a real block, hot layout moves); dx's tail as a plain
  `goto bx` (388); fewer/other z feeds (opfeed.py z: every linear nest is 90 or worse, the
  branching 3/8 form is the only one).  dx feed forms (opfeed.py dx): only `e1`/`e1e1`.

### dz1/dz2 (opdz.py, oprev.py)

- Both pins removable, and the dzc indirections, and the `if (0)` wrappers: `return;` then
  `dz1: __builtin_unreachable(); dz2: __builtin_unreachable();` (IDENTICAL; one shared label
  for both is 304, so they stay two entries, in that order or reversed).
- opsim key ranges on the matching dump: dz1 39..71, dz2 12..18, dx 39..78.
- oprev.py sweeps nested cp/expect forms: dz1 `ce0` (cp, then expect(cp,0)) and dz2
  `e0e0` are the cheapest IDENTICAL ones; single conditions and plain cp nests fail
  (plain cp nests act like no feed at all: 352/64).

### optIniBool copies (opmerge.py, opn.py)

- optC/optE/optS/optU were identical: any merge is IDENTICAL; landed as `optIniBoolG`.
- optN can't join: its dead entry test moved to the call site (4 spellings) is 684; it has
  to be inside the inlined body (it shapes the copy's own profile).  optIniBoolG's own cp
  arms and expect are all needed (1108/708/100).

### Don't retry (attempt 2)

- Call-site spellings and early-inlined wrappers for xellbutton with a natural parseButton.
- Linear nests for parseButtonX's z feeds; dx feed without expect; asm goto in the power arm.
- optN's entry outside the copy.
- One label for both dz dummies.

### Next ideas

- Natural parseButton still needs the xellbutton site to have its own profile.  A static
  helper that IPA (not early) inlines, e.g. one too big to early-inline that holds the
  xellbutton default handling and the log, might give that without hints; measure the
  remopower block's frequency in its dump first (needs 18, and `!s` 37).
- nodx + one cheaper zero-byte entry: opds.py lists other positions (group 198 key 80..147,
  group 244, cputemp's getIniU32 group key 17..19, nosusecurity's group 6..10); an existing
  asm goto edge (macid's, dualboot's) could perhaps also feed dx and drop dx's own feed.
- parseOption's po_hint group (3 tricks): the copies draft from attempt 1 still only misses
  the .rdata order of the bad-value string.

## Attempt 3

New tools (tools/wip/dehint/): `opp3.py` (parseOption bad-value copies with the message as a
static array / pointer / helper), `opbtn.py` (parseButton's own shape on top of part+m_bx),
`ophelp.py` (non-early-inlined helpers around the xellbutton site), `opvl.py` (parseOption's
two expects: operators, vlen's type and computation), `opint.py` (optIniIntI written out /
macros), `opmac3.py` (macid's memset feed replaced by a real call before the asm goto).

### Landed: optIniIntI's always_inline -> an `INI_INT(var, name, def)` macro (IDENTICAL BYTES)

- Why always_inline was needed: gcc 6's early inliner refuses any callee whose growth *
  (calls in it + 1) exceeds early-inlining-insns; optIniInt has 3 calls, so no spelling of a
  function gets early-inlined.  The 15% GU profile needs the body in applyIniOptions before
  profile_estimate, i.e. the original had the code there: written out or as a macro.
- opint.py: IDENTICAL with a temporary for the result (do-while macro `m_tv`, statement
  expression `m_se`, or written out `w_v`); storing the field in both arms (`m_st`, `w_def`)
  is 258, dropping the bad arm's store (`m_st2`, `w_nodef`) 1090.  Landed `m_tv`, flagged
  borderline (it is a macro copy of optIniInt).

### parseOption po_hint group: still the .rdata order

- The literal is emitted when its first use is expanded (BB chain order), so cputemp's copy
  puts the bad string before "Using CPUTEMP" (0x6f8).  A `static const char[]` message: code
  identical, but the array goes after all literals (0xe80; 42 lines of offsets).  A
  `const char *const` to the literal folds back (158, same as copies).  A helper
  `badValue(opt, val)` for all three: 684.
- Tree tail-merge doesn't merge the copies (pre dump: cluster {cputemp, gpufan} has no
  duplicate): each copy's vuse is its arm's store (xb.cpuTemp / xb.gpuFan) and the call's vdef
  escapes to the return block's .MEM PHI.  If it merged into bad: the order would be right.

### parseOption's two expects (opvl.py): no match

- vlen test: `!= 0`, size_t/uint32_t vlen, ternary/if-ne/init forms of vlen: all 62 (the
  incomplete block loses its epilogue copy); `> 0`, `>= 1`, `0 < vlen`: 79; `vlen = 0; if
  (val) vlen = strlen(val)`: 483; `len != strlen(opt)` directly: 469.
- setBoolOption test: `!= 0`/nonzero 217, `> 0`/`>= 1` 403, `== 1` 811.  Pairs: >= 156.

### parseButton's shape (opbtn.py, on part+m_bx): the winbutton expect is free there

- With gcc's own split, removing parseButton's winbutton expect changes nothing: `noexp` =
  `cur` = 335 (only applyIniOptions; parseButton and its .part identical).  Every other natural
  shape (returns, `if (s) {}` around the chain, `b` assigned in an else, mixes) is also 335:
  the split part and the header profile don't depend on the spelling.  uint8_t/uint32_t `b`:
  far worse.
- So the natural-split route costs: parseButtonX's ~10 + the hand-written part + pb_exp, all
  at once, for the 335 xellbutton-site layout.

### xellbutton-site helpers (ophelp.py)

- A helper that holds the whole `if (!xb.xellButton && (xb.bootFlags & 4)) {...}` block is
  not early-inlined (unlike attempt 2's wrappers) and gets its own profile: 1161 (void), the
  same with xellbutton2's block too 834, `int xellButtonIni()` with the log inside 607, the
  whole JTAG-range block as a helper 1653.  All change the entry frequencies (the helper's
  conditions are estimated with entry 10000: the call block is 216, not 132).
- Mechanism (profile_estimate dump of noexp): the call block is 907 * 50% (xellButton == 0,
  no heuristic) * 29% (bootFlags & 4, PRED_CALL) = 132; the header's `!s` is 21.6% (pointer
  15% + call 71% + early return 39%), power-fail 16.8%.  The reference layout needs `!s` 37
  and remopower 18 together: call block >= ~141 with p(!s) ~26%, so neither the call-site
  frequency nor the header's own estimate alone can do it.

### macid memset feed (opmac3.py)

- Dropping the memset: 496.  The asm goto after the first log_printf (a real call before it,
  no memset): 427; after showHexPairs 431; after the last log 437.  The memset also keeps the
  asm goto at the head of the arm.

### Landed: optN's entry expect -> `__builtin_constant_p(xb.bootFlags + 2) == 1` (IDENTICAL)

- opcmp.py: every `__builtin_expect(cp, 0|1)` respelled as a comparison of the cp result that
  folds false.  Only optN's entry matches (`== 1`, `== 2`, `== -1`, `< 0`, `<= -1` all
  IDENTICAL; `> 1`/`>= 2` 989; dropping the test 172, plain cp 797), so one builtin fewer.
  The expect(cp, 1) dx feed: every `>`/`>=`/`!=` form is 312 (= no expect: no taken-heuristic
  folds false).  The rev feeds' expects and dz2's: no form matches.
- oprev3.py: rev feed nests with levels cp / `cp == 1` / expect(cp, 0), depth 1-3: only the
  landed `ce` (dz1, 3 builtins) and `ee` (dz2, 4) or costlier (`qqe` 4, `qee`/`eqe` 5).
- optN's entry as a natural parameter test (`!name`, `name == NULL`, `!set`, `set == clear`,
  `def < 0`, ...): 172 = dropping it, i.e. folded before profile_estimate; `!*name`: 696.
- dx's tail `if (cp == 1) goto bx` and the z feed's outer `cp == 1`: IDENTICAL/90, no saving.

### Other probes (no match)

- optIniBoolG/optN's `!bad` expect (opg3.py): `bad == NULL`, nested getIniBool, assignment in
  the if: 100 (G) / 172 (N); bad arm first: 221 / 690.
- optIniBoolG/optN sites as a statement-expression macro of optIniBool (opgm.py, like
  INI_INT): 1300+ (their profiles must be estimated separately; the copies stay).
- parseButtonPart without `cold`: parseButton and applyIniOptions then match even without the
  winbutton expect, but the part is no longer optimized for size (102 lines in .part).  So the
  hand-written part needs cold, and cold needs the expect.
- parseButtonX's power expect: `== 0` 925, arms swapped (`if (strnicmp(...))`) 898.
- dx without the cold label 281; dx ending in `return b` instead of unreachable 331.
- Experiment (opF.py, hints): a dead feed into the xellbutton call block from the block after
  patchsmc: 1049+ (it takes flow from the xellButton tests below the join; not informative).

### Don't retry (attempt 3)

- The bad-value message as a static array or pointer, or a helper for all bad arms.
- Natural parseButton spellings (they all give the same split and profile).
- Helpers around the xellbutton site that hold its conditions (own profile, wrong entry
  frequencies); written-out/macro optIniBool for the G/N sites.
- Comparison respellings of the expect(cp, 1) feed and the rev feeds.
- parseButtonPart without cold.

### Next ideas

- The natural-split route (opbtn noexp, 335) is now ~13 tricks for one region: it needs the
  xellbutton call block near 171 (so `!s` = 37 with parseButton's own 21.6% and remopower
  >= 18) plus one dummy entry.  A natural reason for that frequency: the call block is
  907 * 50% (xellButton == 0) * 29% (PRED_CALL); a shape where one of those two tests gets
  ~65% or ~38% instead (e.g. a test with an opcode heuristic, or no call in the dominated
  block) without changing the code.  Model it with p1/sim3 before compiling.
- po_hint: make tree tail-merge merge the copies into bad: (the arms' stores before the copy
  stop it today); any form where the copy's vuse equals bad:'s would put the string last.

## Attempt 4

New tools (tools/wip/dehint/): optricks.py has edits for the attempt-3 source (`G_*`, `mG_*`,
`N_entry4`, `mac_*4`, `dual_goto4`, `rev*_4`, `bx_*`); `opfq.py` (a block's frequency at
profile_estimate), `opxs4.py` (xellbutton-site condition forms on the natural parseButton base,
build/op/nat.c), `oppo4.py` (parseOption bad-arm variants), `opnodx4.py` (writes build/op/nodx.c:
src without the dx dummy), `opdx4*.py` (dx replacements), `opret4.py`/`opret4b.py` (control
flow inside the existing dead feeds, alone and with removals).

### Landed: optN's first cp arm (singles, IDENTICAL BYTES)

Re-running singles on the attempt-3 source: `N_cp1` (optN's `if (xb.bootFlags & set) { if (cp)
goto r; return 0; }` -> `if (xb.bootFlags & set) return 0;`) is IDENTICAL.  Its `goto r` lost its
job once the entry test became `== 1` in attempt 3.  Nothing else is free alone; pairs on top of
it: none IDENTICAL (best 14 `pb_exp+part`, then 38s).

### Landed: the dx dummy goes, dz1's dead arm returns (IDENTICAL BYTES, 6 tricks)

- nodx (dx, its feed, asm goto, cold label, tail test, unreachable all gone) = 38: only the demon
  and patchsmc getIniBool blocks swap (a G tie).  opsim a4ref a4nodx 192 3: r3 same, r4 swaps
  169/179.  opds: one dummy entry fixes it at groups 188/207 (key 47..78), 198 (80..147) etc.
- opdx4.py: one asm goto from applyIniOptions' xellbutton code to dz1/dz2 (no change) or a new
  dz3 (312: key wrong).  opdx4c.py: an asm goto (no feed) before every statement: nothing.
- opdx4b.py: dz3 + asm goto from the xellbutton log block + a rev feed: IDENTICAL with 3-builtin
  feeds (`ce0`, `e1e0`, `e0e1`), 5 tricks.  opdx4d.py: no 1-2 builtin feed anywhere works.
- opdx4e.py: dz3's feed inside dz1's outer arm, `if (C1) { if (E0 C2) goto dz1; goto dz3; }`:
  IDENTICAL, and then without the asm goto too, and with `return;` (or `__builtin_unreachable()`)
  in place of `goto dz3`: IDENTICAL.  So the tie is settled by the flow of dz1's dead outer arm
  (it no longer falls through to dz2's feed), not by a dummy entry.  Landed `return;`.
- Borderline: it is the existing dz1 feed (still counted) with one more statement; no builtin
  added.
- Full build after both: SHA256 10dac648...1971c.

### Flow in the dead feeds as a lever (opret4.py, opret4b.py, opdz4.py): nothing more

- dz2's feed with `return;`: IDENTICAL but saves nothing; dropping either inner/outer test of
  dz2's feed (with or without return): 44 / 279 / 304.  dz1's feed simplified (one test, cp
  inner): 333-532.
- Every M edit x every single removal (mG_*, G_*, N_*, ib_*, bx_z, bx_exp, pb_exp, mac_*,
  dual_goto4, po_exp2, part): nothing IDENTICAL.  Rev feed arms rewritten with
  return/goto dz1/goto dz2 at both ends (16 x 16 forms) for mG_cygnos/mG_smcne/mG_nosec/
  mG_nandmu/G_exp/bx_z: best 38 (unchanged tie swaps).
- A whole dummy (dz1 or dz2 with its feed, asm goto, memset) dropped, the other feed carrying
  return/goto instead: 304+.  Both dummies stay.

### xellbutton site frequency (opfq.py, opxs4.py): stuck

- Natural base build/op/nat.c (part+m_bx+pb_exp, parseButtonX deleted): 335; on the attempt-4
  source 321 (nat2.c), and the rev-feed flow forms don't move it.
- profile_estimate (opfq): call block 132 = 907 x 50% (`_243 == 0`: no heuristic, gcc skips
  comparisons with 0) x 29% (PRED_CALL on getIniValue).  Forms tried, all 132: nested ifs, test
  order `bootFlags & 4 && !xellButton` (code changes: 1251), `== 0 && != 0`, negated, empty-then
  else, and `goto` skips (`if (xb.xellButton || !(xb.bootFlags & 4)) goto alt;`, goto on either
  test): gcc 6's C front end adds no goto predictor here, frequencies identical (code 931).
- Needed 0.186..0.191 overall; the only per-test values that give it are 65-66% on the
  xellButton test (PRED_OPCODE_NONEQUAL needs a nonzero constant: different code) or a DS
  combination with a ~60% taken predictor on the bootFlags test (none applies to `x & 4`).
  Judged stuck.

### parseOption po_hint group: stuck

- Confirmed the .rdata mechanism (po4_copies.c -S): literals get LC numbers in expand order and
  .rdata is written in label order, so cputemp's copy numbers the bad string first (LC86, before
  "Using CPUTEMP" LC87) even though crossjump later merges the code.  A natural shape needs
  cputemp's/gpufan's arms to reach `bad:` at expand time while carrying a call at
  profile_estimate that vanishes afterwards; only a guarded hint call does that.

### Don't retry (attempt 4)

- Asm goto (no feed) to dz1/dz2/new dz3 from any statement of applyIniOptions.
- One-dummy replacements for the tie (dz3): the flow fix needs none.
- Rev feed control-flow rewrites for the mG_*/G_exp/bx_z ties; dropping dz1 or dz2.
- xellbutton-site condition spellings and goto skips (frequency is fixed at 132).

### Next ideas

- The lever that worked: control flow inside an already-dead arm changes the profile without a
  builtin.  Other dead arms reached from applyIniOptions are inside inlined helpers (optIniBool's
  and optIniBoolG's `goto r` arms, optN's off arm, parseButtonX's z feed): try `return`/goto
  rewrites there together with removing a neighbouring builtin (the z feed's 3 cp, G's expect).
- Otherwise the rest looks stuck: the G/N copies need their own profiles, the dz dummies need
  asm-goto edges at bbro, parseOption's group needs a vanishing call.

## Attempt 5

New tools (tools/wip/dehint/): `op5.py FN` (optIniBool / optN / optIniBoolG regenerated from a
template: each dead arm `{ if (cp) <stmt>; return 0; }` with <stmt> a goto to any label in the
body (L0 before the off test, L1 before perbox, L2 perbox log, L3 else head, L4 !bad head, L5 ini
log, L6 bad warning, r, L8 before `return 1`) or `return 1`; arms plain; optN's entry likewise;
the `!bad` expect on/off), `op5x.py FN` (those forms x every optricks single removal),
`op5bx.py` (parseButtonX's z feed as 1-2 cp feeds at four positions in the else arm with
gotos/returns to any label of the copy, power expect on/off).

### Singles on the 5d05a77e source

Nothing IDENTICAL.  Nearest: part 14 (not real), mG_cygnos/mG_smcne 38, rev2_4 44 (its text is
stale: dz2's feed), po_exp2 62, mG_nosec 62, mG_nandmu 64, bx_z 90, po2 102, G_exp 112.

### Helper dead-arm flow alone (op5.py)

- G (130 forms with fewer builtins): none IDENTICAL.  Best: off arm `goto L6` (into the bad
  warning) without the expect, 76 (G_exp alone 112); every on-arm target but r is 358+.
- N (361 fewer forms): none; everything with the expect gone is 146 (= N_exp), whatever the arms.
- ib: off arm `goto L5`/`goto L8`/`return 1` = `goto r` (IDENTICAL, no saving); any other on-arm
  target 333+.

### Helper flow forms x single removals (op5x.py; results in build/op/op5x_{G,ib,N}.txt)

- G 4475, ib 2314, N 7175 combinations: none IDENTICAL.  The flow forms are inert: every removal
  scores what it scores alone (mG_cygnos/mG_smcne 38, rev2_4 44, ...), except that G's
  no-expect off->L6 form moves with mG_nandmu: 48 (n=2, both gone would be -2).
- So control flow in the helpers' cp arms only matters where it lands at bbro, and with the
  helpers inlined 4-8 times the arms are all copies of one shape: there is no per-site lever.

### parseButtonX's z feed as flow (op5bx.py, 1372 forms)

- Only the current 3-cp branching feed is IDENTICAL.  `return 0;`, `return b;` (b is 0 there)
  and `goto z` are the same block, so every 1-2 cp feed with any targets is 90 (= no feed) at
  positions 1/3, 546 at position 0 (z gets 50% of the else arm; it needs 37.5%) and 795 at 2.
  0.375 = 1/2 x 3/4 needs three 50% tests, which is why the branching form is the only one.

### MATCH: parseButtonX's z feed with 2 cp (op5z.py, IDENTICAL BYTES)

- op5z.py: 1-2 tests from a menu of cp comparisons (`== 1`, `> 0`, `< 0`, `!= 0`, ...) and
  expect(cp, 0|1).  `if (cp1) { if (cp2 > 0) goto z; }` is IDENTICAL (also `>= 1`, `> 1`, and
  any 50% outer spelling: `!cp`, `cp == 0`, `cp != 0`): PRED_TREE_OPCODE_POSITIVE gives the
  inner test the 75% that the old pair of 50% tests (1/2 + 1/4) gave.  One cp fewer.
- No single test works (no menu condition gives 37.5%): 1[...] is 90 at best; sequential
  pairs `if (a) goto z; if (b) goto z;` 29 at best (`cp < 0` twice).
- Landed (src: parseButtonX), comment updated.

### Rev feeds with the comparison menu (op5rev.py): nothing

- dz1 (3 builtins now) with 1-2 builtins: best 333 (one expect level), plain-cp pairs 403.
- dz2 (4) with 1-3: best 38 (`cp == -1`/`cp < 1`/`cp < 2` outer + expect inner, 3 builtins);
  the 17%-of-17% the two expects give has no opcode-heuristic equivalent.

### ib arms as comparisons (op5cmp.py ib): nothing (one arm gone is 852+ whatever the other)

### G and N arms as comparisons (op5cmp.py G/N, 4223 + 4351 forms): nothing

- The arm's cp spelling (`> 0`, `== 1`, `< 0`, ...) never changes the score: the arms' own
  frequency comes from the live `x & set` test, and the dead branch only adds flow below the
  G block (r, the warning).  G without the expect stays 76 (off -> L6) / 112; N without it 146.
- N's entry test with the comparison menu and other targets, off arm gone: 290+.
- dz2's feed as 3 one-builtin levels (343 forms): 44 = no feed (plain cp nests act like none).

### Pairs on the new source: nothing IDENTICAL (best pb_exp+part 14, mG_cygnos+mG_smcne 38).

Full build with the z feed change: SHA256 10dac648...1971c; progress 617/617.

### Mechanisms (why the rest is stuck)

- G expect (and N's): it sets p(!bad) on a live test; dead flow can only add counts below the
  G block, never lower it, and the 4 G sites are copies of one profile (no per-site lever).
- optIniBool/G/N cp arms: needed for the 50%/29% split of the live tests (early-return
  predictor); comparison spellings and other targets are inert or 300+.
- parseButtonX power expect: 83% on a live strnicmp test; `== 0`/swapped arms change code.
- Rev feeds: their 8.5% / 2.9% come from expect's 17%; no opcode heuristic gives that, and
  plain cp nests vanish as feeds.
- dz1/dz2 asm gotos + unreachable, macid memset, po_hint group, hand-written part: unchanged
  from attempt 4's analysis.

### Don't retry (attempt 5)

- Goto/return targets in the helpers' cp arms (any label, with any single removal).
- Comparison spellings of the helpers' arms, N's entry, the rev feeds (1-3 levels).
- z feed: 1 test of any spelling; flow targets in parseButtonX (return 0/b are z).

### Next ideas

- The opcode-heuristic lever (a comparison of a cp result gives 66%/75%/... instead of 50%)
  only removes builtins where two or more 50% tests combine into one of those values; no other
  site has that.  Otherwise options looks stuck at 34 by these routes; the natural-split
  parseButton route (attempt 2-4) remains the one big lever, and it needs the xellbutton call
  block's frequency (132 -> ~171), which no spelling found so far gives.

## Attempt 6

Structural, not spelling.  New tools (tools/wip/dehint/): `op6x64.py` (iw13x64.py with options'
strings: function extents in tools/ref/xeBuild64), `op6dis.py ADDR` (one Linux function with string
immediates and guessed callee names resolved; outputs were tmp/strs/aio64.txt and po64.txt, deleted 2026-11-11),
`op6pe.py file.c [pattern]` (applyIniOptions' profile_estimate blocks around a pattern),
`op6ib.py ib|G|N|all` (whole-body helper shapes), `op6on.py [-fn ib,G,N]` (live on/off arm
forms x expect x optN entry), `op6w.py` (G/N sites written out in applyIniOptions).

### The Linux build (v1.16, gcc 4.9.2): same structure as src

- optIniBool (40c9b0, 189 bytes, not inlined there): `if ((bootFlags & set) || (bootFlagsOff
  & set)) return 0;`, then perbox, iniBoolInvalid (bad: warning, return 0), getIniBool(name,
  def), the ini log, `bootFlags = (bootFlags & ~clear) | set; return 1`.  This is src's
  logic, and in source it can't be told apart from two separate tests.
- applyIniOptions (40d9c0) has optIniBool's body at every site (gcc 4.9 inlined it), in
  src's order: nomobile, noremap, noecdremap, nandmu, nosecurity, nosusecurity, smcnocheck,
  cfldv and the int options, macid (macidSet inlined), then the JTAG range block: cygnos,
  demon, patchsmc, xellbutton (`!xellButton`, then `bootFlags & 4`, then
  `xellButton = parseButton(getIniValue(..)); if (!xellButton) { log; = 0x12 }`),
  xellbutton2 (with the same `if (!xb.xellButton)` test as src), smcnoeject, smcnoblink;
  type == 2: nodvd, olddvd, dualboot; dvdkey; rev.  Nothing marks the G sites (nandmu,
  nosecurity, cygnos, smcnoeject) or noecdremap as different from the other options.
- The int options pass the field's current value as the default (`getIniU32(name, ebx)`, with
  ebx loaded before the -1 test), i.e. `xb.cpuFan = optIniInt("cpufan", xb.cpuFan)`.
  gcc 6 would propagate the -1.  It doesn't help here: INI_INT isn't counted.
- parseButton (40cac0) is one flat else-if chain in the same order (wiredx nested).
  parseOption (40d200) has the same arms as src, each `goto bad` style (one shared bad
  message block), and no extra code in cputemp's or gpufan's arms.  So the po_hint
  asymmetry (only those two arms) has no source in the older code.

### Helper shapes (op6ib.py): nothing

All builtins of optIniBool gone, whole body replaced: result variable / `ok` flag 917,
`a || b` exit, nested ifs, `&&`, `out:` exit 1001, bad-first / else-if 1054, early
`return 1` in each arm 1217, `(a | b) & set` 1493.  The standalone `_optIniBool` itself
differs by 8 lines (the order of `or`/`mov eax,1` in the set block: the cp arms make `r:`
a join with its own frequency), so its two arms aren't just for applyIniOptions.

### Live "already on" arm (op6on.py): nothing

Every caller guards with `!(xb.bootFlags & set)` (olddvd's set is 0), so the on arm is dead
at every site.  A real `if (on) goto r;` (already on: re-apply) or `return 1;` would be
natural code that still changes the callee's own profile.  Results: ib on `goto r` 445
(and `_optIniBool` 37 lines: the standalone body changes); G on `goto r` 81 (G's cp arm
alone, removed, is 112); N's on arm `goto`/`return 1`/`return 0` are all IDENTICAL with
the entry kept (no saving: N's on arm is already plain).  Off arms must stay `return 0`
(they are live).  G x N together (`-fn G,N`, 800 forms): best cheaper form is still 81.

### G/N sites written out (op6w.py): nothing

Plain nested ifs at the site (no helper, no return, flag set in each arm, a flag variable,
`goto` past the block, `else if` chains), for each site, the four G sites and noecdremap:
821 (smcnoeject alone) and up, 1234 for noecdremap.  The inlined copies with their own
profiles stay the only way.

### xellbutton call block (profile_estimate, nat2.c)

bb98 `xellButton == 0` has no prediction (50%), bb99 `bootFlags & 4` call heuristic 29%,
call block 907 x 0.5 x 0.29 = 132.  To get ~171 one of the two tests needs another
heuristic: 65% on bb98 (only PRED_OPCODE_NONEQUAL, a nonzero constant: other code;
`xellButton` is int, so `< 1`/`<= 0` give jle) or ~60% to combine with bb99's 29%
(early-return at 61% would need a `return` on the false edge, which changes behaviour:
907 x 0.5 x DS(29%, 61%) = 177 even then).  The Linux build has the same two tests in the
same order, and the reference loads `xellButton` first, so `if (bootFlags & 4) { if
(!xellButton) ..; if (!xellAltButton) ..; }` is other code.  Still stuck.

### Don't retry (attempt 6)

- Whole-body shapes of optIniBool/G/N with their builtins gone (op6ib's 12 shapes).
- Live on arms (`goto r`, `return 1`) in place of the cp arms.
- Writing the G/N sites out in applyIniOptions as plain C.
- Looking in the Linux build for a different helper set or option order: there isn't one.

### Next ideas

Nothing with real odds is left by these routes.  Each remaining group needs something that
changes a profile and vanishes before RTL: the G/N copies need a callee profile of their own
(the same code from a different function), parseButtonX needs a call block of ~171 that
plain C can't give, and po_hint needs a call that goes away after profile_estimate.  If
options is retried, start from a new fact about the original (another build of v1.21 or
a newer source), not from a new spelling.

## Attempt 7

Hypothesis (from attempt 6's diagnosis): the G/N copies are real functions whose own,
unhinted profile gives what the expects force.  New tools (tools/wip/dehint/): `op7pe.py
file.c fn...` (a helper's own profile_estimate predictions), `op7g.py G|N|GN` (natural lower
halves, perbox/ini/bad, for optIniBoolG/optN with their `!bad` expect gone).

### The `!bad` expects: a result variable does their job (IDENTICAL BYTES)

- Read off op7pe: optIniBool's `!bad` test is 21.6% (pointer 15 & early return 61, the call
  heuristics cancel); G's and N's expect force 17%.
- op7g `on2`: `if (!bad) on = getIniBool(name, def); else { warning; on = 0; } if (!on)
  return 0; log ini` is IDENTICAL for G, for N, and for both (also N `on5`).  The warning
  block no longer goes straight to the return block at profile_estimate, so the bad arm loses
  the early-return prediction; the `on` join is threaded away after inlining (DOM/VRP), so the
  code is the same and the blocks keep the stale counts.  `on1`/`on3` (bad arm first) 31 (G) /
  731 (N); `noexp` 112/146.
- op7arms.py (arms x entry x lower per helper): with on2, optN's sites take optIniBoolG's
  shape exactly (`cp cp none on2`), so optN merges into optIniBoolG (its entry cp, off-arm cp
  and expect go).  ib must keep its own lower (`noexp`/`out2`; on2 for ib: 194, its standalone
  4 lines + .rdata).  At this step: 4 removed (G's and optN's expects, optN's entry and
  off-arm cp); the arms follow below.

### Param tests in the arms: the inline-time rebuild (mechanism)

- G's off-arm cp can be any parameter test (`if (clear)`, `if (def)`, `set == clear`, ...):
  IDENTICAL.  G's on-arm cp only with a two-step test (`set & clear`, `(set & clear) != 0`):
  a direct parameter test (`clear`, `def`, `def > 0`, `set == clear`) is 321.  So the inliner
  folds conditions on substituted parameters at inline time and then rebuilds frequencies
  (TODO_rebuild_frequencies): no stale flow survives.  A condition one statement away from the
  parameter (`_1 = set & clear; if (_1 != 0)`) is only folded by the next ccp, after the rebuild,
  so its flow into r stays stale like a cp arm's.  The off arm only needs to not be a plain
  `return 0` at profile_estimate (no early-return prediction on the off test); the on arm needs
  its stale flow into r.  Memory tests (`xb.bootFlags & clear`) make the body too big to inline.

### optIniBoolG as a result-variable function: no builtins at all (IDENTICAL BYTES)

op7w.py: tops (T1 `on = 0` for each flag test, T2 Linux's `||` sets `on = 0`, T5/T6 `on = 0`
then `if (!a && !b)` / nested ifs) x lowers (L1 on2-like without the return, L2 on2, L3 bad
first, L4-L6 ini log before the warning) x tails (R1 `if (!on) return 0; set; return 1`, R2 `if
(on) set; return on`, R3).  Every T1/T2/T5/T6 with L1/L2/L4/L5/L6 is IDENTICAL for G; L3 733;
T3/T4 (one flag test still returning) 943-1724.  Mechanism: no arm returns, so no early-return
prediction anywhere; the on/off and bad paths reach `if (on)` with on = 0 and are threaded to
the exit after inlining, leaving the stale counts the cp arms and the expect used to make.
Landed T2 L1 R2 (src: optIniBoolG).  optIniBoolG now has 0 builtins: removed 6 since attempt 6
(optN's entry cp, off-arm cp and expect; G's 2 cp arms and expect).  34 -> 28.

### optIniBool (ib) with result variables

- ib's standalone `_optIniBool` is IDENTICAL with T1/T2/T5/T6/T3 x L4/L5/L6 (the ini log
  must come before the warning in source, or .rdata order and the standalone change: L1/L2
  188, standalone 16 lines).  Only applyIniOptions' OPT sites differ: 114 (T1/T2/T5/T6), 764
  (T3), 1230 (T4).  So the standalone no longer needs the cp arms; the OPT sites' profile does.
- op7pe on ib (cp source vs result variable): the result-variable body gives `!bad` 15%
  (pointer only), the getIniBool test 29/71 and set 6100, where the OPT sites need 21.6%
  (pointer & early return), 61/39 and 6002.  op7ib.py: the same result-variable body with
  `return 0` after the warning (and only there) is IDENTICAL, standalone included, for every
  top T1/T2/T5 and ini form a/c/d, either tail; with `on = 0` there it's 114.  Landed T2 a
  ret R2 for optIniBool: its 2 cp arms go (28 -> 26), and optIniBoolG now differs from it in
  that one statement (src comment: borderline).
- One function for all sites: 120 (the G sites need the warning arm's `on = 0`); the G sites
  as unguarded `optIniBool(...)` calls (like olddvd): 1789.
- Landed: optIniBool T2 a ret R2 and optIniBoolG the same with `on = 0` in the warning arm
  (op7ib.py's L4 order; op7w T2 L4 R2 is IDENTICAL for G too).  Full build SHA256
  10dac648...1971c; progress 617/617.  Singles (optricks) on the new source: nothing free
  (part 14 not real, mG_cygnos/mG_smcne 38, rev2_4 44, po_exp2 62, mG_nosec 62, mG_nandmu 64).

### parseButtonX (xellbutton) as a real second reader: no match

Read off the dumps (run.sh, a7cur vs natural): the hinted copy differs from a natural reader
only in the cold xellbutton blocks: `!s` (store 0) 37 vs 29, the constant-store join 95 vs
102, the remopower head 18 vs 17, the part call 0 vs 1.  The power expect only turns 83.2%
(const return 67 & call 71) into 83.0%, which rounds the remopower head (103.5 x 0.17) to 18;
the z feed moves ~45% of the else head (71% x 63.4%) to `!s`.
- op7bx.py, natural bodies (b with `if (s)` / `if (!s) return 0`, returns, `if (s != NULL)`,
  `if (!s) b = 0; else ...`): all 321 (90 with the power expect kept); default handled in the
  reader (`d_b`, `d_ret`) 675/749; reader that stores the field itself 741.
- op7bx2.py (24 forms: the reader stores xb.xellButton and logs the default, b or field,
  `if (s)`/else/init, with or without the ini read inside): 741-994 (the default's log then
  gets the reader's profile).
- op7bx3.py, defensive `s &&` on any subset of the chain (192 forms): with an `if (!s) return
  0;` head they are inert (folded before profile_estimate: 90 = expect only); without the head
  the null flow cascades down the guards: 392+.
- Arithmetic: with no feed the natural constraints are P(!s) = 37/132 = 28% and P(power) =
  81%; the available predictor mixes give 21.6% / 30.2% / 10.1% for `!s` and 83.2% / 71% /
  79.3% / 76% for power.  A feed is needed, and in the reader there's nothing that folds late
  (its only parameter is the ini string; a parameter test folds at inline time, see above).

### parseOption (po_hint) under the new mechanism: not retried

The dominated call po_hint gives cputemp's/gpufan's bad edges has to exist at
profile_estimate and vanish after it; a natural static helper there would be early-inlined
(that is what no-early-inlining stops), and the copies draft still has the .rdata order.

### Mechanisms (attempt 7)

- **Result variables are a profile lever.**  An arm that sets a variable and joins a later test
  gets no early-return prediction (the edge into a `return` block, or into a single-successor
  block before it, is what PRED_TREE_EARLY_RETURN predicts); DOM/VRP thread the join away after
  inlining, so the code is the same and the counts are stale.  This replaced cp arms (stale flow
  into the set block) and `!bad` expects (21.6% -> 15%) at once.  Where a site needs the
  early-return prediction, a `return` in just that arm gives it back (optIniBool's warning arm).
- **Inline-time rebuild.**  A condition on a substituted constant parameter is folded during
  inlining, then TODO_rebuild_frequencies recomputes the counts: such a test leaves no stale
  flow (only its edge probabilities, as the callee estimated them).  A condition one statement
  away (`_1 = set & clear; if (_1 != 0)`) is folded by the next ccp, after the rebuild, and acts
  like a dead cp arm.
- The standalone `_optIniBool` only needs the ini log before the warning in source order
  (.rdata, and its block order); the cp arms were for the OPT sites.

### Don't retry (attempt 7)

- One optIniBool for all sites (G sites need the warning arm's join), G sites unguarded.
- Param tests in the helpers' arms (direct ones fold at inline time; two-step ones are dead
  tests, not natural); memory tests there (`xb.bootFlags & clear`: not inlined everywhere).
- parseButtonX: whole natural bodies, default/log in the reader, defensive `s &&` chains.

### Next ideas

- The result-variable lever may apply elsewhere in applyIniOptions: any remaining hint whose
  job is to remove an early-return prediction or to add stale flow into a join.  The rev feeds
  sit after `sprintf` in the rev block (their dead arms `return;`), so a natural `rev` reader
  with a result might replace part of them; the dz dummy entries still need asm-goto edges.
- parseButtonX still needs a ~45% leak from the else head to `!s` that no natural reader gives.

## Attempt 8

Lever under test: attempt 7's result variables (arms set a value and join a test; the join is
threaded after inlining, stale counts remain) applied to the remaining groups.  Drafts and
generators: tools/wip/dehint/op8*.py, build/op/a8/.

### Singles on c49ed372

Nothing IDENTICAL.  part 14 (not real), mG_cygnos/mG_smcne 38 (stale edits), rev2_4 44, po_exp2
62, mG_nosec 62, mG_nandmu 64, po2 102, pb_exp 190, po1/po_nei 231, dual_goto4 304, m_bx 321,
mac_ms 373, po_exp1 811, bx_exp 818, param 1109.

Pairs (optricks pairs, 171): nothing IDENTICAL; best pb_exp+part 14 (not real), mG_cygnos+mG_smcne 38.

### parseOption's two expects (op8po.py): arithmetic says no

- Forms for the setBoolOption test (expect, `== 1`, plain, the rest under `else` so the arm has
  no return of its own, `r = setBoolOption(); if (r) {..; return r;}`) x vlen tails (expect,
  plain, if/else both ways, `val` in place of vlen): only the current pair is IDENTICAL; best
  62 (setBool expect kept, vlen plain or if/else), 217 (vlen expect kept, setBool plain).
- The arm under `else` (r1) keeps the early-return prediction: the log block's single
  successor is the return block, which is what PRED_TREE_EARLY_RETURN looks for.
- `-p 82` and `-p 84` on the current source are 199/237 lines in parseOption: both expects
  need 17% almost exactly.  Natural predictors on that test: opcode `== 1` 28%, call 29%,
  early return 39%; their DS combinations are 9.2 / 13.7 / 19.9 / 20.7 / 28 / 29 %.  Const
  return doesn't apply (0/1 are excluded).  For vlen, the pointer heuristic points the wrong
  way (val != NULL 85%).  No natural shape gives 17%.

### macid memset: asm goto position (op8az.py)

dz1's asm goto with the memset removed, at every statement position of applyIniOptions (67):
none IDENTICAL; best 172 (inside the macid loop), 333 (xellbutton default / dualboot), 373 at
its own place.  The memset's PRED_CALL on the asm-goto block's edge is needed where it is.

### parseButtonX with a redundant result test (op8bx.py): no

`if (!b) return 0;` / `if (b) return b; return 0;` / `if (!b) goto z;` after the chain, in the
non-power arm or after the part call, with three head forms, with and without the power
expect (51 forms): 471+ (and .rdata order changes).  A live test on the reader's result puts
far more flow into `!s` than the z feed's 37.5% of the else arm.

### A shared name reader so gcc's split replaces the hand-written part (op8bn.py, op8bh.py)

- `buttonName(s)` = remopower..kiosk (no power), called from parseButton (after its power test)
  and from parseButtonX's else arm: gcc splits buttonName, but at wiredx (header 30, or 32
  with a redundant `if (!s) return 0;` in it), not at wirelessx: fnsplit refuses a split whose
  header + call overhead (2) reaches max-inline-insns-auto (40), i.e. header >= 38.  In
  parseButton the header holds !s and power too (wirelessx 32 accepted, wiredx 39 refused),
  which is why the original split lands at wirelessx.  buttonName's header would need ~6 more
  size units that fold away in both callers; nothing natural gives that.  All forms 20k+
  (.rdata: "wiredx" first).
- `buttonName` with power inside and parseButton a null-check wrapper: split at wirelessx,
  parseButton IDENTICAL (the part's name aside), but parseButtonX can't reach the part
  without re-testing power (X_E 630 in applyIniOptions: code differs), and the wrapper route
  for xellbutton (W_E, z feed before power) is 807.
- So the hand-written part is tied to parseButtonX, as attempts 1-3 found.

### MATCH: one __builtin_constant_p value per function, one expect for the rev feeds (op8k.py)

- The dead feeds only need each test's prediction and that every test folds; the tests can
  share one SSA value.  `int dead = __builtin_constant_p(xb.blSuffix[1]);` at the top of
  applyIniOptions feeds the macid memset size and the rev feeds; `long rare =
  __builtin_expect(dead, 0);` gives every test of `rare` the expect's 17%
  (expr_expected_value follows the SSA def, also through `rare == 1`).
- Rev feeds now `if (dead) { if (rare) goto dz1; return; } if (rare) { if (rare == 1) goto
  dz2; }`: IDENTICAL BYTES.  dz2's inner test must differ from its outer one: with the same
  test twice (`if (e) { if (e) ..}` or `E(k,0)` twice) early FRE/CSE folds the inner one
  and dz2 gets 8.5% instead of 1.45% (304, like no feed).  Inner forms that work: `rare ==
  1`, `rare > 0`, `rare & 1`, `rare >= 1`, `E(k == 1, 0)`, `E(k & 1, 0)`, a second cp;
  `rare > 0`/`k > 0` with E (kb) and `rare == k` are 44.
- parseButtonX's z feed: `int dead = __builtin_constant_p(xb.xellButton); if (dead) { if
  (dead > 0) goto z; }`: IDENTICAL (1 cp instead of 2).
- Removed: 5 __builtin_constant_p (rev feeds 4 -> shared, memset 1 -> shared, z feed 2 -> 1,
  plus the shared one counted once per function: 7 -> 2) and 2 __builtin_expect (rev feeds 3
  -> 1).  Full build SHA256 10dac648...1971c; progress 617/617.
- Not a new kind of shape: the feeds are still counted dead tests, with fewer builtins.

### Asm gotos and dummies (no)

- One asm goto with both labels (`:::: dz1, dz2`, either order) in macid's arm 901, in
  dualboot's 838.
- dz1/dz2 ending in `return;` (one or both) or `;`: 801-951.  The unreachables stay.

### po_hint: what it does, in numbers (lead, not tried to the end)

profile_estimate on parseOption (op7pe): every value arm's `== -1` test has early return 61%,
opcode 28% and call 71% (PRED_CALL on the success edge, whose block holds the log_printf)
-> 59.8% bad.  cputemp's and gpufan's add po_hint's call 29% on the bad edge -> 37.8%.
DS(61%, 28%) without either call is also exactly 37.8%: a shape where the success block of
those two arms doesn't count as a guarded call (no call in the edge's dest, the dest not
dominated by the test, or the dest post-dominating it) would do po_hint's job with no call
at all, and no-early-inlining would go with it.  None found that keeps the code: the log has
to follow the test directly.

op8ph.py: cputemp/gpufan arms without po_hint as `if (!= -1) {log; return 1;} goto bad;`,
if/else, plain, and with a redundant `if (!= -1)` before the log: all 231 (= po1 alone; the
redundant test folds before profile_estimate).

### Don't retry (attempt 8)

- parseOption's expects as plain / result / else-arm shapes (arithmetic: no 17%).
- dz1's asm goto anywhere else without the memset; one asm goto with both labels; dz
  dummies without unreachable.
- Redundant result tests in parseButtonX; a shared name reader without power (split lands
  at wiredx), or with power (parseButtonX can't reach the part).
- Shared feed values with the same test twice in a nest (CSE folds the inner one).

### Next ideas

- po_hint: a success block for cputemp/gpufan that PRED_CALL doesn't see (numbers above).
- parseButtonX's cp could be applyIniOptions' `dead` passed as a parameter (one cp fewer),
  but that is plumbing for a hint, not natural code: not done.
- The rest (param, 5 expects on live tests, 2 asm goto + 2 unreachable, the part) is as stuck
  as attempts 5-7 describe.

### Attempt 8: not landed (parent's call)

The shared-feed shape (`int dead = __builtin_constant_p(...)`, `long rare =
__builtin_expect(dead, 0)`, feeds testing `dead`/`rare`) matches, but it removes no
dead test: the same feeds still steer, only through fewer builtin calls. That is a
hint disguised, not removed (tools/wip/dehint/README.md), so src stays at c49ed372's
25 tricks and the shape is saved as drafts/options_sharedfeeds_candidate.patch for
the user's review. Don't count builtin-sharing as a removal in later attempts.

## Attempt 9

Focus: parseOption's po_hint group.  New tools (tools/wip/dehint/): `op9end.py` (po_hint removed;
bad-message copies at the end of the function, per-arm or shared labels, before or after
`bad:`), `op9rv.py [form]` (result-variable / repeated-test forms for value arms; ARMS=two,
temps, all, regions, two+regions, -X, +X, t-X), `op9mix.py BASE` (every myatou32 arm in BASE
except edramtemp, which gets each form).  Read predict.c (releases/gcc-6.2.0) for the call
and early-return heuristics.

### predict.c: what the two heuristics look at

- PRED_CALL on edge e: e->dest is dominated by e->src, doesn't post-dominate it, and holds a
  call with side effects (anywhere in that one block).  Looping const/pure calls count.
- PRED_TREE_EARLY_RETURN: for a block bb whose single successor is the return block R (which
  ends in GIMPLE_RETURN, single succ EXIT) and R != bb->next_bb, every edge into bb is
  predicted not taken (unless the source has a null/const/negative-return prediction).  All
  returns share one temp, so R is one block at the end; `bad:` is R's prev block, which is why
  no bad edge gets the early-return prediction while every success log block does.

### The target is a range, not 37.8%

- op9end `shared_before` (cputemp/gpufan `goto badtemp`, a copy of the bad message under a
  label before `bad:`): IDENTICAL BYTES with the bad edge at 48.8% (early return now on both
  edges, they cancel: DS(opcode 28, call 71)).  The copy's literal is expanded after all others
  (it is at the end), so .rdata stays.  `before`/`before_r` (one label per arm) also
  IDENTICAL; `after*` 256, `shared_after` 423 (then `bad:` gets the prediction for every arm),
  copies in the arm 158 (.rdata), plain 231.  Not landed: two identical error exits.
- So any shape that drops the early-return prediction from just those two success edges (or
  adds it to their bad edges) is enough.

### MATCH: an `ok` flag in cputemp's and gpufan's arms (op9rv.py, IDENTICAL BYTES)

- F4 `ok = 0; if (x != -1) { log; ok = 1; } if (!ok) goto bad; return 1;`, F4b (`if (ok)
  return 1; goto bad;`), F4c (`return ok`), F1 `ok = x != -1; if (ok) log; if (!ok) goto bad;
  return 1;`, F1b: all IDENTICAL BYTES; `ok` int, uint32_t, int8_t or scoped in the arm.
  The log block's successor is the flag's join, not the return block, so no early return on
  the success edge: bad 48.8% at profile_estimate (op7pe); DOM/VRP thread the join later.
- Not: if/else forms without a join (F1c `else goto bad; return ok`, F3) 231; `return x !=
  -1` after the log (F1d) 329; the field tested twice (F2/F2b) 293.
- Which arms: cputemp alone 102, gpufan alone 231, all 8 temps/fans 22, all 11 myatou32 arms
  22, regions only 231, two+regions IDENTICAL, all but edramtemp IDENTICAL (edramtemp plain,
  F1c or F3; op9mix).  edramtemp is the arm whose -1 test falls into bad.
- Landed F4 on cputemp and gpufan (fewest changed arms); po_hint, its `dead` local and the
  no-early-inlining attribute gone.  Full build SHA256 10dac648...1971c; progress 617/617.
  Borderline (src comment): the flag is live but redundant and exists to match.

### parseOption's two expects: not retried

Attempt 8's -p 82/84 check (199/237 lines) shows they need 17% exactly, unlike the po_hint
edges; no natural predictor mix gives 17% (attempt 8's arithmetic).

### Don't retry (attempt 9)

- Bad-message copies anywhere (in the arm: .rdata; at the end: two identical exits, only a
  candidate, op9end `shared_before`).
- The flag on cputemp alone / gpufan alone / all temps / all myatou32 arms (edramtemp must stay
  without the join).

### Next ideas

- The early-return lever (a join between the log and the return) may help other edges that
  need a prediction removed: check `bb->next_bb` and the join before writing a dead test.

## Attempt 10

Levers under test: result/flag joins (attempt 7, 9) on the expects that are left.  Tools
(tools/wip/dehint/): `op10po.py [S,V ...]` (parseOption: setBool test forms S x vlen tail
forms V; OUT=file writes the last combination).

### parseOption's vlen expect: the code matches with a join, .rdata doesn't (op10po.py)

- Tail forms where the unknown-with-value arm reaches the return through a join while the
  incomplete arm returns: `ok = 0; if (vlen) { unk; ok = 1; } if (!ok) inc; return 0;` (J1),
  `ok = 1 ... if (ok) inc` (J1b), if/else setting ok (J1c), `ok = vlen != 0; if (ok) unk; if
  (!ok) inc;` (J1d), `if (ok) return 0; inc;` (J1f), `if (vlen) unk; if (!vlen) inc;` (J25,
  repeated test, no flag): **.text identical**, 4 lines, all `.rdata` offsets: the
  incomplete message's literal comes after bad's.
- Why: VRP1 threads the join; the threaded copy of the join block is created at the end of
  the block chain (duplicate_block puts it before EXIT), and cleanup merges the incomplete
  block (single pred) into that copy, so it is expanded after `bad:` and its literal is
  numbered last.  Dumps: build/op/a10 (inc-first up to fnsplit, bad-first from vrp1).
- Counts: E (expect) has unk 19 / inc 94, J1 unk 33 / inc 33, plain (P, IE, J2, J10, J11)
  56 / 56 = 62 lines.  So the vlen test doesn't need 17%; it needs the unknown block low,
  which only the join gives without a builtin.
- setBool test: shared "
" block with macid's success (label in the arm, or a block at the
  end) never helps (797 = plain); a result join `ok = setBoolOption() == 1; if (ok) log; if
  (ok) return 1;` 245.
- Every natural heuristic on the vlen test points the wrong way for the unknown arm: the
  pointer heuristic says `val` is non-null (85%), the opcode heuristic says `vlen > 0` /
  not `vlen <= 0`, and in the plain tail the calls and early returns of the two arms cancel
  (50%).  Only a call on the unknown edge alone (29%, its arm joins while the incomplete arm
  reaches the join's test) lowers it, and that join is what VRP1 threads and merges, moving
  the incomplete literal behind bad's.  bad must stay last in block order (its literal is
  last), and the incomplete block can't be R's prev or keep a second pred, so no join form
  can keep the order.  Draft: drafts/options_parseOption_vlen_nearmiss.patch (J25; .text
  identical, .rdata off: not a match).
- setBool expect with the vlen join (J25) at other --param values: 82 300 lines (parseOption
  203), 84 574, 80 840: the setBool test alone needs 17% exactly, and the natural mixes there
  are 9.2 / 13.7 / 19.9 / 20.7 / 28 / 29%.  Stuck, as attempt 8 said.

### Rev feeds and dz dummies (op10rev.py): no natural feed exists

- profile_estimate counts (src): sprintf block 554, dz1 47 = 554 x 50% x 17%, dz2 8 = 554 x
  50% x 17% x 17%; the macid and dualboot asm-goto edges add nothing.  So the dummies' keys
  come from the feeds alone.
- dz2's feed dropped: 44 (one tie); dz1's dropped (with or without its `return;`, both
  feeds dropped, `if (!s) return;` around the rev block, a return after sprintf): 508.
- A label after the function's `return;` is reachable only by goto, so no flag or result join
  can carry flow into dz1/dz2: the feeds are tied to the dummies, and the dummies to the asm
  gotos (zero-byte heap entries).  Not a join problem.

### parseButtonX / parseButton (re-checked, nothing new tried with odds)

- `part,m_bx,pb_exp` (natural parseButton, gcc's split): 321, only applyIniOptions, as attempt
  7 found.  The power expect turns DS(const return 67%, call 71%) = 83.25% into 83.0%, which
  the remopower head (103.5 x (1-p)) needs to round to 18 (p <= 83.09%); natural mixes are
  83.25 / 79.3 / 76 / 71%.  The winbutton expect only outweighs PRED_COLD_FUNCTION (first
  match) on the call to the hand-written cold part; without `cold` the part loses its size
  optimization (attempt 3).  These are probability values, not early-return edges, so the
  join levers don't apply.

### Don't retry (attempt 10)

- Join/flag/repeated-test forms of the vlen tail (all .rdata: VRP1 merge, mechanism above).
- A shared "
" block for setBool and macid (label in the arm or at the end).
- Natural code around the rev block in place of the feeds.

### Result

No match; src/ unchanged (22 tricks).

## Attempt 11

Focus: attempt 10's vlen near miss (J25 and the ok-flag joins: .text identical, the
incomplete literal after bad's).  Tools (tools/wip/dehint/): `op11s.py file.c [out.s] [re]`
(literal order of a variant), `op11tail.py [form ...]` (tail forms with the u/i/b literal
order next to the score; OUT=file), `op11v10.py [V ...]` (attempt 10's V forms with the
order), `op11dump.sh file.c dir [flags]` (profile_estimate, vrp1, dom2, vrp2, optimized
dumps).  Reference order: u (unknown with value) LC123, i (incomplete) LC124, b (bad) LC125.

### Literal order = expand order = block chain order

String labels are numbered when the call is expanded, and expand walks the block chain, so
the order is the chain order at expand.  The tail's three messages appear nowhere else in
the object, so no earlier reference can number them first.
- J25's VRP1 dump: both edges into the join are threaded (`(82,77) -> 78` and
  `(76,77) -> 80`), the original join is removed, copies are created before EXIT.
- With -vops the vlen==0 copy is `# .MEM_210 = PHI <.MEM_16(73)>; goto inc`: a degenerate
  virtual PHI (the join merges the unknown arm's log_printf VDEF with the other path), so
  tree_forwarder_block_p fails, and cleanup merges inc (single pred) into the copy, at the
  end of the chain.  A join always has that PHI (the unknown arm has a call), so no join
  form keeps inc in place.
- The setBool copies that give inc its other preds in the final code are made by DOM3 and
  VRP2 (setBoolOption calls per dump: 1 to split-paths, 2 at dom3, 22 at vrp2, 3 after), too
  late to stop the merge.
- All attempt 10 V forms re-run with the order (op11v10.py): J1..J27 and J25 are `ubi`
  4 lines; J26 `iub` 20; P/IE/J2/J10/J11 `uib` 62; N/IEn `iub` 66; Pv/Nv 914.  No ok-flag
  variant differs from J25 on .rdata.

### No join: the re-test is folded before profile_estimate (op11tail.py T*)

- `if (vlen) { unk; return 0; } if (!vlen) inc;` (T1), `== 0` (T2), with its own return
  (T4), `else if (!vlen)` (T5), `vlen <= 0` (T7): all 62 lines (plain's profile).  FRE1
  (034t) removes the second test (dump counts 2 -> 1 at fre1), so profile_estimate sees the
  plain if/else, unk and inc at 50%.  FRE1 folds any test of vlen dominated by `vlen == 0`.
- `if (!val) inc` (T6) can't be folded at all (val NULL iff vlen 0 isn't visible): 101.

### Moving the unknown message into the val block (op11tail.py IN*, W*)

- IN/INg/INn/INe (`if (vlen) { unk; return 0; }` at the end of the val block, incomplete
  after it): 342; the val test's false edge now reaches a call with an early return, so the
  val test goes from 69.8% to 89.8% and the whole value chain moves.  INv (no vlen test) 516.
- W1/W2/W5 (unknown in the val block without return, `if (!vlen) inc` after it): the join
  keeps an unthreadable pred (val false), so inc stays in place, but the vlen test now sits
  in the val block's f0 tail: unk f0 (needs 19..33) and loses its epilogue copy, 66 lines,
  order `iub`.  W3 (no vlen test) 120, W4 (`if (!val)`) 36 `ubi`.
- So the val-false flow must pass the vlen test (f113 there), which puts the join after it.

### Named messages (op11tail.py SA*, SP*)

- A `static const char` array (function or file scope) for bad's or incomplete's message
  is emitted after every literal, at the end of .rdata (`_badfmt.3708` after loadAddons'
  literals): 42/44 lines over five functions.  A `const char *` local is folded to the
  literal (SPb/SPi = J25, `ubi`).

### What would be needed, and why it doesn't exist

The profile wants a call on the unknown edge only (a join after unk, or the incomplete
block not dominated by the vlen test with no f0 bypass); the chain wants the incomplete
block not to be a threaded copy.  The join gives the first and breaks the second through
the virtual PHI; every other spelling either loses the profile (FRE1, val bypass) or the
.rdata (arrays).  A second incomplete site merged by tail-merge would need a path that
doesn't bypass the vlen test, and there is none.  Stuck; the setBool expect and the --param
stay as attempt 10 left them.

### Don't retry (attempt 11)

- Any join/flag/repeated-test tail (the copy's virtual PHI), named arrays or pointers for
  any of the three messages, the unknown message inside the val block, a second vlen test
  without a join (FRE1).

### Result

No match; src/ unchanged (22 tricks).

## Attempt 12

Levers under test: the ones that took build.c to 0 (notes/build.md, attempts 46-70): a
small static helper holding a call (IPA-inlined, not early-inlined) brings its own
profile; type changes that renumber SSA or change inline sizes; a non-PHI statement in an
inlined helper's return block; nested ifs for `&&`; a loop ended by `i = count`.  Tools
(tools/wip/dehint/): `op12po.py [S:V ...]` (parseOption: setBool forms S x vlen tail forms V,
with the u/i/b literal order), `op12x.py levers|cross|show` (levers alone and crossed with
every single removal: rv1, rv2, rv2i, bxe, bxz, pbe, ms, po1, po2, dz2), `op12mv.py`
(optIniBoolG / parseButtonX moved to 12 places in the file, x removals).  Scratch:
build/op/a12*.

### Helpers with their own profile for parseOption's two expects (op12po.py): no

- setBool test as a helper (`boolOption(opt, val)`), 10 forms: `if (setBoolOption() == 1)
  { log; return 1; } return 0;` (int, uint32_t, _Bool), `!= 1` first, an `ok` result,
  `r = setBoolOption(); if (r == 1) log; return r;` (and `return r == 1`, `if (r)`), plain
  `if (setBoolOption())`: 246 (H2: the `r` form, caller `== 1`) to 407.  The other functions
  only move by parseOption's size (call displacements).  A shared `done:` block at the end
  (R1): 893.
- vlen tail as a helper (`unknownOption(opt, val, vlen)`, 9 forms: if/else, early return,
  void/int/uint32_t, `!vlen` first, `vlen > 0`, size_t): 442 (the caller sees one call block
  at profile_estimate, so the value chain's early-return predictions move); 376 with the
  incomplete arm first (`iub`).  `unknownValue()` returning whether it printed (U6): 4 lines,
  `ubi` (it is attempt 10's join again); the unknown message alone as a helper call (U7): 62
  = plain.
- So a helper's profile doesn't help here: its edge probabilities come from the same
  predictors, and wrapping the tail changes the caller's profile above it.

### The predictors gcc 6 has, measured (build/op/a12t/t.c, t2.c, -fdump-tree-profile_estimate-details)

opcode nonequal 28, opcode positive 73, call 29/71, early return 39/61, pointer 15, const
return 67 (paths to a constant other than 0/1 taken), negative return 4, null return 10,
loop exit 91, continue 50 (no effect in gcc 6), goto none.  For setBool (needs 17% within
about 1%; its success arm already has call 29, early return 39 and `== 1` 28, together
9.2%), the only DS mixes near 17% are call 29 + early return 39 + opcode 28 + const return
67 = 17.08%, and call 29 + const return 33 = 16.7% (no opcode, which `== 1` always adds).
Both need a const-return prediction, i.e. a success path returning a constant other than 0
or 1, which parseOption (0/1, uint32_t; mode_build tests `!parseCmdOptions`) and
setBoolOption's code don't have.  The power expect (needs 82.13 < p <= 83.09%, natural
83.25%) has no mix in range either (call 71 + const return 67 = 83.25, x early return =
76).

### Types, return statements, nested ifs, loop ends (op12x.py): all inert

- IDENTICAL alone (and so usable as bases): nested ifs for xellbutton's and xellbutton2's
  `&&` (nx1, nx2) and dvdkey's `s &&` (ndk); optIniBool's `||` as two `else if` tests (nib);
  optIniBoolG returning int / void / uint32_t, `return on & 1`, `on != 0`, `on ? 1 : 0`,
  `on > 0` (tg, tgr, tgv, gr1-gr5); parseButtonX returning uint32_t with a uint32_t b (tbx);
  parseButtonX's power arm as `return 0x11` (bxr), `s == NULL` (bxi); macidSet's and
  applyIniOptions' `i` uint32_t (tmi, tai); the macid loop indexed `s + i * 2` (mac2);
  `xb.cfLdv == 0`, `xb.dualButton == 0`, the JTAG range as two compares (cfn, dbn, jt).
- Code changes: optIniBool int (46/88), parseButton's b uint32_t (565), INI_INT's v uint32_t
  (635), parseButtonX's return or b alone uint32_t / uint8_t (852/853), macidSet with a flag
  and `i = 6` (1470).
- Cross (every IDENTICAL lever x every removal, about 240 builds): every removal scores what it
  scores alone (rv2 44, po2 62, bxz 90, pbe 190, dz2 304, rv2i 304, ms 373, rv1 508, po1 811,
  bxe 818).  None of these spellings reaches profile_estimate differently, and none changes
  the inputs of bb-reorder (block order or the heap) that the ties depend on.

### Helper position (op12mv.py): inert

optIniBoolG and parseButtonX at 12 positions each (all before applyIniOptions): IDENTICAL,
and with each removal exactly the removal's own score.  The cgraph order of the static
helpers doesn't change inline order or block numbering in a way the layout sees.

### Don't retry (attempt 12)

- Helpers for parseOption's setBool test or vlen tail (own profile: same predictors; the
  tail as a call changes the value chain's profile).
- Return types, return-block statements and position of optIniBoolG / parseButtonX; nested
  ifs for applyIniOptions' `&&`s; uint32_t loop indices: inert for every removal.
- Looking for a natural 17% (setBool) or 82.1-83.1% (power) mix: the measured predictor
  table above has none without a non-0/1 constant return.

### Result

No match; src/ unchanged (22 tricks).  The levers that worked on build act on SSA numbers,
inline order and early-return edges; options' remaining tricks are exact edge
probabilities (the expects and the param), zero-byte heap entries (the dz dummies and their
feeds, the memset) and the cold part, which none of them reaches.  A next attempt needs a
new fact about the original (another build of v1.21 or its source), not a new spelling.

## Attempt 13

Focus: applyIniOptions' cold layout (rev feeds, macid memset, the two asm gotos, dz1/dz2) and
the hand-written `_parseButton.part.0`, with build's late levers.  Tools (tools/wip/dehint/):
`op13.py alone|cross|show` (stretches of applyIniOptions as static helpers, crossed with single
removals; adds removal groups `dz1` (feed, memset, asm goto, label), `dzall` (both dummies and
everything that feeds them: 12 tricks), `feeds`, `ag1`, `ag2`, `rv1ms`), `op13bx.py` (parseButton
and parseButtonX as full chains with no hand-written part), `op13bb.py DIR [ids]` (bbro traces
with each block named by source line, calls and literals, read from the cprop_hardreg dump: the
names in p1/trl.py's output are stale), `op13sim.py REFTAG TAG [-d D] [-2]` (opsim/sim3 search:
which single or paired key changes of real heap entries reproduce the reference's extraction
order).  Dumps: `GFL="-O3 --param builtin-expect-probability=83" sh tools/wip/aio/p1/run.sh
SRC TAG` (a13cur = src, a13rv2, a13rv1, a13ms, a13bxz, a13dzall).

### Helpers for applyIniOptions' stretches (op13.py): inert or worse

- IDENTICAL alone, and every removal then scores exactly its own value: the two macid warnings
  through one `macidWarn(msg, s)` helper (mac_w), the macid loop as `setMacid(s)` (mac_loop),
  dvdkey as `dvdkeyIni()` (dvd_v, dvd_vr), cfldv as `cfldvIni()` (cf_v).  They are early-inlined
  or inlined before anything the layout sees.
- Code changes: the rev block as a helper (7 forms, void/int, `s` passed or read inside, a
  generic `iniSuffix(buf, name)`) 508 with its feeds gone (= rv1 alone; with the feeds kept in
  the caller, rev_if, 460); the whole macid read as a helper 887, the parse with `s` passed 418
  (668 as early returns); dualboot as a helper 304 (= dz2 alone) / 428 (value-returning);
  xellbutton2 as a helper 678; dvdkey with its flag test inside 1128.
- Removal costs re-measured on 5a795a3f's src: rv2 44, bxz 90, pbe 190, dz2 304, **dzall 304**
  (all 12 dz tricks at once cost what dz2 alone does), ag2 304, ag1 376, ms 373, dz1 390, rv1ms
  487, rv1 508.  So a natural fix for dzall's 304 would be worth 12 tricks; nothing found.

### What the dummies do, by name (op13bb.py on a13cur)

- dz1 (bb 261) is pushed with key -47 from the macid chars-warning asm-goto block (149, T64) and
  popped as its own trace at T69; dz2 (bb 262) with key -8 from dualboot's "ignored" block (251,
  T67), popped at T103, right after the key-8 getIniBool blocks of noremap .. olddvd.
- rv2's 44 lines: with dz2 at key 0 the key-4 getIniBool blocks pop smcnoblink, demon, patchsmc
  instead of demon, patchsmc, smcnoblink (fibheap tie), which moves three cold blocks.
- op13sim: dz2's key must be exactly -7 or -8 (-6, -9 and further fail).  No single key change
  of any real heap entry within 6 of its own key, and no pair within 1, reproduces the order
  for rv2; no single change within 8 for rv1 or ms.  So the dummy entries can't be replaced by
  a natural count change of an existing block; a replacement needs an extra heap operation
  (insert/delete) at that point, which only a zero-byte block gives.
- rv1 changes only the keys of 261/262 (dz1 47 -> 0, dz2 8 -> 16) yet also 7 alignment lines:
  the feed's `return;` also moves hot counts.  ms changes the keys of 146 and 149 and more
  (the sim with the old keys put back still differs).

### parseButton split (op13bx.py)

- Full chains in both parseButton and parseButtonX, no hand-written part: parseButtonX is
  inlined whole (fnsplit dump: "Not splitting: not called directly or called once"), 927 lines.
- With parseButtonX's chain calling `parseButton(s)` for its tail (re-tests the first names, so
  other code, a probe only): the layout is IDENTICAL, only the call (cdecl to parseButton
  instead of regparm to the part) differs (13 lines).  The part's only job is to be the else
  arm's callee.
- parseButtonX called from two sites (xellbutton2 or dualboot too) so that fnsplit splits it:
  it splits, but at winbutton (header 32), not wirelessx, and ipa-icf doesn't merge the two
  parts (different bodies); 11k lines, the other site's profile changes.  No route there.
- ipa-split.c couldn't be read (gcc.gnu.org's git web answers with an Anubis bot check);
  the fnsplit dump gave the reason above instead.

### Don't retry (attempt 13)

- Static helpers for the rev, macid, dualboot, dvdkey, cfldv and xellbutton2 stretches (the
  inert ones stay inert under every removal; the rest change code).
- Natural count changes for the dummies' job: op13sim rules out single/paired key changes of
  real entries; the dummies need extra heap operations.
- parseButtonX full chain (not split: called once) or called twice (split at winbutton, no
  ICF merge).

### Result

No match; src/ unchanged (22 tricks).

## Attempt 14

Focus: a natural source of the zero-byte blocks dz1/dz2 stand for.  Tools (tools/wip/dehint/):
`op14scan.py [obj|file.c ..]` (compiles each object with its build.sh flags, or a file, with
`-fdump-rtl-cprop_hardreg-blocks-details -fdump-rtl-bbro-details`, and lists every block that
reaches bb-reorder with no code: only labels, notes, USE/CLOBBER insns or an empty asm, with
its freq, preds, succs and the source line of each pred), `op14ret.py` (applyIniOptions as an
int function), `op14mac.py` (macid's warnings with one source copy of their tail),
`op14db.py` (dualboot's "ignored" path spellings).  Scratch: build/op/a14, build/op/a14scan.

### What dz1/dz2 are at bbro (op14scan on src)

dz1 (bb 261, freq 47) and dz2 (bb 262, freq 8): a code_label with 1 use and the bb note, no
insns, no successors; their only preds are the asm gotos (149 is a block of its own holding
just the asm goto at the head of the chars warning; dz2's asm goto ends 251, the "ignored"
log block).  Their frequencies come from the dead rev feeds (profile_estimate), whose edges
are gone by RTL.  So bbro sees a block with two successors where the reference has no branch:
149 and 251 each get one extra non-best successor, pushed into the heap and later popped as
a one-block trace.

### No natural empty block reaches bbro anywhere in the program (op14scan, all objects)

All 25 app objects and all 41 crypto objects (617 functions, 9777 blocks at cprop_hardreg):
the only blocks with no code are the hinted ones (options' 149/261/262 and mode_client's
asm-goto blocks and dz labels).  Nothing in the 0-trick objects or XeCrypt's third-party C
(edge copies, PHIs, loops, switches, noreturn asserts) leaves an empty block for bbro.

The mechanism, from the dumps: bbro's own `cfg_layout_initialize (CLEANUP_EXPENSIVE)` runs a
cleanup_cfg right before the traces, which forwards every edge through an empty block with
one successor and deletes it, so whatever reload, cprop_hardreg, peephole2 or regrename
empties is gone before bbro looks (edge copies coalesced by IRA/LRA included).  An empty
block that survives must have no successors, and C only gives those through
`__builtin_unreachable` (gcc's own: cunroll's unloop latch, removed by fab's
optimize_unreachable when its pred ends in a gcond; the macid loop isn't unrolled anyway) or a
noreturn call (the call is code).  And a block that pushes one must end in a jump that emits
no bytes: only asm goto does.  The reference has no branch at either push point (the ignored
block is `log; movl $0, xb+112; jmp L679`; the chars warning is `movl $LC, 4(%esp); jmp L670`
into the crossjumped tail), so a natural edge there would add a jcc.

### Candidates tried (cand.c through op14scan, then in options)

- Return-register clobber (`(clobber (reg ax))`, emitted by expand_null_return and at the
  fall-off end of a non-void function; flow_active_insn_p keeps it from being a forwarder, and
  it emits nothing): in cand.c it always lands in an existing block (the epilogue or the last
  statement's), never a block of its own.  applyIniOptions as int/uint32_t (op14ret.py,
  options.h's declaration aliased away): with the final `return;` 59 (adds `xor eax,eax`),
  falling off the end 1562; on the dzall base 357 every way (dzall alone 304).
- Noreturn call, abort, PHI with different values on two arms, a loop bounded by an array
  (cunroll), a 4-case switch, a reset-after-log like dualboot's (cand.c): no empty block.
- macid's warnings with one copy of the tail in the source (op14mac.py: `msg` flag, goto past
  the tail, else-if chain, default message, ok flag, ternary): the PHI of the message is
  loaded into a register before the `je` (`mov edx, LC`; the reference stores each literal
  straight to the stack slot, i.e. two calls crossjumped), so code changes: goto 104 (also
  .rdata order), the rest 718-924; with ag1/dz1/dzall removed 622-826.
- dualboot's "ignored" path (op14db.py): operands swapped and `!=` with an empty then-arm are
  IDENTICAL and inert (ag2 and dzall still 304); a local `b` (3 forms) 368-640; storing 0
  before the log 308 with or without the dummies (code changes: store order).

### Don't retry (attempt 14)

- Looking for a natural zero-byte block for bbro: none exists in gcc 6 C at -O3 without asm
  goto or __builtin_unreachable (op14scan's census plus the cleanup at bbro's start); a
  natural extra successor at 149 or 251 needs a branch the reference doesn't have.
- applyIniOptions returning int (return-register clobber): code changes.
- macid's warning tail shared in the source (PHI of the message): register load, code changes.
- dualboot's ignored path spellings above.

### Result

No match; src/ unchanged (22 tricks).  The dz group (12 tricks) can't be replaced by a
zero-byte natural block; what's left for it is the original having a different set of real
heap operations (other blocks, edges or frequencies) elsewhere in applyIniOptions, which
op13sim's single/paired key changes didn't find.  A next attempt there would have to model
several simultaneous structural changes (for example how the original's optIniBool sites
were written) with sim3, not one spot.

## Attempt 15

Focus: the cheapest single removals by things other than key values: rv2 (dz2's feed, 4
builtins, 44 lines), bxz (parseButtonX's z feed, 2 cp, 90), pbe (parseButton's winbutton
expect, 190), alone and combined with code-neutral natural changes.  Tools
(tools/wip/dehint/): `op15heap.py TAG [-at N,..] [-w b,..] [-k keys]` (the round-4 fibheap's
trees before chosen extractions of p1/sim3's replay), `op15sim.py REFTAG TAG [-lo L -hi H]
[-2 W] [-map a:b]` (op13sim with any key range, pairs within W, id remaps), `op15site.py`
/ `op15site2.py` (which optIniBool sites use optIniBool and which optIniBoolG, swept on top of
a removal).  Dumps: build/v/aio_p1/a15* (GFL="-O3 --param builtin-expect-probability=83").

### rv2: what the tie is, in the heap (op15heap.py, op15sim.py)

- a15cur vs a15rv2 traces (op13bb.py): without dz2's feed, dz2 (262) has freq 0 and is popped
  last (T111) instead of at T103 (key -8, after olddvd's getIniBool); dz1's freq goes 47 -> 57
  (dz1's outer test now has a `return` on both arms) and one hot block 925 -> 924.  Only the
  dz2 change matters: opsim with 262=-8 alone gives the reference order, 261=-47 alone doesn't.
- The heap before the three key -4 getIniBool blocks (demon 169, patchsmc 179, smcnoblink
  220): in rv2 the root list after nandmu's extraction is 220 (degree 0), 169 (degree 2,
  holding 179), 159; consolidation puts the lowest degree first, so 220 wins the tie.  With
  dz2's extra extraction at key -8 the trees are linked differently and 169 (degree 1) leads.
- op15sim over every real entry: any single key in -60..0 (53 entries), and every entry
  within +-40 of its own key (113 entries, hot trace-end keys included): only 262 (dz2) at -8
  or -7 fixes it.  Pairs within +-3 of entries with keys >= -60: none.
- dz2's freq can only come from a feed: profile_estimate gives the asm goto edge 0.0%
  (PRED_NORETURN on the path to its __builtin_unreachable), so a dz2 at key -7/-8 needs a
  dead edge of 7-8 into it.  Closed by mechanism unless the tie is broken by many key changes
  at once.
- Source order: swapping demon and patchsmc (rv2 kept) changes code and relocs (48): the
  option order is the reference's, as the hot code and the literal order say.

### bxz: what the z feed does, in numbers (a15bxz dumps)

- parseButtonX's own profile_estimate: !s 21.6% (pointer 15, call 71, early return 39),
  power 83.0% (expect), else head 1332; the feed's outer cp test 71% (call heuristic: the
  false edge reaches remopower's strnicmp) and inner `> 0` 63.4% (opcode positive 73, early
  return 39) send 600 of the else head's 1332 to the return-0 PHI arm, remopower's test 733.
- After the IPA inline the cp tests fold: the empty else head merges into remopower's test
  block, which keeps the head's count (1332 -> 18 at the call block's 132), and the z edge's
  600 stays in the threaded constant-0 block (263: 2160 + 600 -> 37, its edge still 21.6%).
- Without the feed: 263 is 29 and pops after the eleven key-37 getIniU32 blocks instead of
  before them (their order changes too), remox 2 -> 3 and the part call 0 -> 1.  op15sim
  (with 263/264 swapped back): only 263 at exactly -37 gives the reference order.
- So a natural replacement needs two things at once: ~28% of parseButtonX's entry on the
  constant-0 return (27.65..28.4%) and remopower's failure flow at most 1.89% of entry
  (remox <= 1.5), with the remopower head still 13.3%.  The !s mixes are 21.6 / 30.2 / 10.1%,
  and every constant-0 path but !s would be other code; the leak has to be a dead edge.

### pbe: tied to `cold` by predictor rank (a15pbe, part_* variants)

- Without the expect only parseButton's winbutton tail changes (6 lines: the part's tail call
  moves to the end, 0x24 no longer hoisted) plus applyIniOptions' copies (184).  The part's
  `cold` makes predict_paths_leading_to put PRED_COLD_FUNCTION (first match, 100%) on the
  winbutton test's false edge; first-match predictors win by rank and only
  __builtin_expect and the loop-iteration predictors rank above it, so with `cold` no
  natural spelling can give that edge 17%.
- Without `cold` (attempt 3): everything matches but the part's own body (not optimized for
  size: duplicated returns, constants in eax; 102).  Size optimization without the
  attribute needs NODE_FREQUENCY_UNLIKELY_EXECUTED from ipa-profile, which only propagates
  into local (static) functions.  A static part (part_st*.c): without `cold` gcc splits
  parseButton at winbutton itself (parseButton.part.2) and the part too, and the part stays
  in .text; with `cold` the code is the same but the FDE order differs (attempt 1).
- So pbe goes only with the hand-written part (or with gcc's own split, attempt 2-3's 335).

### Site forms as a code-neutral key lever (op15site.py, op15site2.py, op15gx.py)

The choice of optIniBool (OPT) or optIniBoolG at a site gives the same code after inlining
but other cold keys (G's getIniBool block is 1-2 lower, its warning 1 higher), so it moves
keys of several blocks at once with no code change, which op13sim's single/pair search
couldn't model.
- On the base: nodvd as G and olddvd as OPT are IDENTICAL (free); every other single flip
  38-204 (as attempt 1-2's m_*).  Unguarded calls (`optIniBool(...)` with no OPT guard) and a
  guard that also tests bootFlagsOff (`o2`/`g2`) change code at every site but olddvd
  (600-1600).
- **rv2 x every OPT/G assignment of the 14 sites (2^14 = 16384 builds):** no match; best
  **20 lines** (from 44), two families: patchsmc+smcnoblink as G (their getIniBool keys
  drop to -3: demon pops first, but then patchsmc, smcnoblink, smcnoeject and cygnos tie at
  -3 in the wrong order) and nandmu as OPT + olddvd as G (the -4 tie comes out right, but
  nandmu's and olddvd's getIniBool blocks swap keys -8/-6, so they swap places).  Every
  other assignment 40+.  op15sim on both 20-line dumps: no single key in -80..0, no pair
  within 2.
- bxz x assignments up to 3 flips: best 90 (= bxz alone).  bxz can't be helped by any
  structure: its 263 at key -29 can never pop before the eleven key -37 blocks the
  reference pops it ahead of.
- optIniBoolG's 126 whole-body shapes (op7w.py tops x lowers x tails) on rv2: all 44 or
  worse (the IDENTICAL ones are inert, as attempt 12 found for other levers); attempt 12's
  IDENTICAL levers (nested ifs, return types, ...) on both 20-line bases: all 20.
- op15grp.py: every joint change within +-1 of the 13 getIniBool blocks' keys (demon,
  patchsmc, smcnoblink, smcnoeject, cygnos, nandmu, nosecurity, olddvd, noremap,
  nosusecurity, nomobile, smcnocheck, noecdremap; 1.6M replays) on rv2: 0 hits; the JTAG
  five within +-2: 0 hits.  So no profile change of those blocks does dz2's job; it needs
  the extra extraction.

### Don't retry (attempt 15)

- rv2 by keys or site forms: single keys of every real entry (wide), pairs within 3, joint
  +-1 over the getIniBool group, all 16384 OPT/G site assignments, G body shapes.
- Reordering the boolean options in the source (code and relocs change).
- bxz by anything that leaves the constant-0 block below 37: it must pop ahead of the key-37
  getIniU32 blocks; the !s mixes give 21.6/30.2/10.1% and a natural constant-0 path is code.
- pbe while the part is `cold` (PRED_COLD_FUNCTION outranks every natural predictor); a
  static part (gcc then splits parseButton and the part itself; FDE order with cold).
- Unguarded or bootFlagsOff-guarded optIniBool sites (code changes).

### Result

No match; src/ unchanged (22 tricks).  The three cheapest removals are each closed by a
mechanism, not by a missing spelling: rv2 needs a zero-byte entry extracted at key -7/-8
(only a dead feed gives dz2 a count, the asm goto edge is 0% by PRED_NORETURN), bxz needs
37 in a block whose natural count is 29 and which no tie can lift past 37-key blocks, and
pbe is the price of the hand-written part's `cold`.  The site-form lever (OPT vs G) is the
one new code-neutral lever that moves cold keys in groups; it halves rv2's diff (44 -> 20)
but no assignment closes it.  A next attempt should only come back here with a different
set of real heap operations (the original's structure), e.g. a natural parseButton split
(the 335 route) where the dummies' jobs change as a whole.

## Attempt 16

Focus: the natural parseButton split as a base (parseButtonX deleted, gcc's own split of a
plain parseButton, no hand-written `_parseButton.part.0`, no winbutton expect: 7 tricks gone,
15 left), crossed with attempt 15's OPT/optIniBoolG site lever, modelled first with the
fibheap replay.  Tools (tools/wip/dehint/): `op16nat.py [-x edits] [-f sites] [-o out.c] [-v]`
(builds the natural base from today's src; edits rv1, rv2, ms, ag1, ag2 and parseButton-side
hints pe/pz/pzs/pz2; site flips as op15site.py), `op16sim.py REFTAG TAG [-map a:b] [-k b=key]
[-keys ..] [-scan LO HI]` (p1/sim3 replay with explicit key overrides; -scan: every single
entry over a range on top of the overrides), `op16site.py [-x ..] [-k K|-all] [-out f]` (OPT/G
assignments on the natural base).  Scratch build/op/a16; dumps build/v/aio_p1/a16nat (GFL="-O3
--param builtin-expect-probability=83").

### The natural base on today's source: 321, two keys

- `op16nat.py`: 321 lines, all in applyIniOptions (as attempt 4's nat2.c).  Block ids are
  the same as a15cur's except 263 <-> 264 (`-map 263:264,264:263`).
- Traces (op13bb.py on a15cur and a16nat): the xellbutton site's remopower block 188 is 17
  (key -1001717, edge 103 x 16.8%) where the reference has 18 (-1001818), its `!s` block 264
  is 29 (edge 132 x 21.6%) where the reference has 37; remox 3 vs 2 and the part call 1 vs 0
  don't reach the heap.
- op16sim: with 188 = -1001818 and 264 = -37 the replay gives the reference order; **the old
  extra round-4 entry (dx, attempt 2) is no longer needed** on today's source.  Ranges, each
  with the other fixed: 264 exactly -37; 188 any key <= -1001718 (edge 17 with block >= 18, or
  edge >= 18).  The other xellbutton blocks: the call block 186 (priority = freq) 103..146,
  the constant-store join 263 priority <= 86 (key >= -1008702), 193 free.  With 264 = -37
  alone, 188's job could also be done by xellbutton2's 198 at <= -147 (not real).  188 and
  198 at equal keys (16..19, any freq) fail: xellbutton2 pops first on a tie, so the
  xellbutton site must differ from xellbutton2's.  No single entry change does it (scan
  -80..0: 0 hits).

### Why no natural spelling can give those two keys (arithmetic)

The xellbutton site's blocks 186..191 and 264 are parseButton's split header inlined at IPA
time; their counts are the header's edge probabilities (estimated once in parseButton, shared
by all three sites) times the call block's count G, rebuilt by TODO_rebuild_frequencies at
inline time.  The header's probabilities don't depend on parseButton's spelling (attempt 3)
or on the call site.  So at the xellbutton site 264 = G x 21.6% and the power test block 187
= G x 78.4%, with power 83.2% / 16.8%:
- 264 = 37 needs G >= 169, but the call block (186, the same block) must stay <= 146, and the
  join's priority is the power-success edge G x 78.4% x 83.2%, which must stay <= 86, i.e. G
  <= 132.6.
- 188 needs the power-fail edge >= 17.5 (or the block >= 18): 187 >= 105 with 16.8%, which
  makes the success edge 87 (the join then fails), or 187 = 103 with a power probability
  <= 83.0%: that is the bxe expect (no natural predictor mix lies in 82.13..83.09%, attempt
  12).  And a power probability changed in the shared header changes xellbutton2's 198 the
  same way, which is the losing tie above.
- Extra flow into 264 can't come from the call site: the threaded copy takes the count of
  the edges threaded into it (only the `!s` edge carries b = 0), and a dead edge from the
  caller can't reach a block inside the inlined header.  Only a dead edge inside the header
  that folds after the inline rebuild (a cp feed: parseButtonX's z) does it, and in the shared
  parseButton that changes the split (below).
- So the call-site levers (nested ifs, test order, helpers with calls, wrappers, result
  variables) can only move G, which is pinned to 103..132 by the other keys; none of them can
  change the header's internal ratios.  The xellbutton site needs a header of its own, i.e.
  parseButtonX, which can only call a hand-written part.

### Hints moved into the shared parseButton (op16nat.py -x pe, pz, pzs, pz2)

- `pe` (parseButtonX's power expect on parseButton's power test): 369 (188 and 198 both 18:
  the tie, and 264 still 29).
- Any `z:` feed in parseButton (`pz` as an else-if, `pz2` in a block around the rest of the
  chain, `pzs` from the power-success arm; with or without `pe`): 1631-1773, parseButton,
  its split part and every function after them change (gcc splits parseButton differently).

### OPT/optIniBoolG sites on the natural base (op16site.py)

Every assignment of up to 5 flips and part of the 6-flip ones (5506 of 16384, results in
build/op/a16/site_all.txt; stopped there): no IDENTICAL, best 311 (nandmu as OPT, with or
without demon/patchsmc/nodvd), floor 311-333 everywhere.  As the model predicts: a flip moves
getIniBool and warning keys but not the xellbutton site's 264 (29) or the eleven key -37
INI_INT blocks it must pop ahead of, so no assignment can work on this base.  Also checked:
the thirteen key -37 blocks moved together to -36..-21 (with 264 at its own 29 or one
below): no hit.

### parseButton's split is fragile: what a hint in the shared header does (op16nat.py -x feed)

Keeping some tricks on the natural base (net gain if fewer than 7): parseButtonX's two jobs
moved into parseButton itself, so all three sites get them.
- The header limit: fnsplit picks the deepest split point whose header is an inline
  candidate; the natural header (`!s`, power, remopower, remox, winbutton) is size 31 and 38
  is refused.  The two-test z feed (bxz's nested form, or any two cp, or one cp plus a dead
  plain test) costs 7, so winbutton moves into the part: parseButton, its part and every
  later function change (1631-1773 lines).  A single-test feed fits (split unchanged).
- Single-test feeds at the power-fail head (`FEED='...' -x pe,feed`): `if (cp((int)s + 1))
  goto z;` 61% (call 71 & early return 39; dumps a16pef1, 663 lines), `> 0` / `- 1 >= 0`
  80.9% (897), `== c`, `< 0` folded at once (inert), `<= 0`, `!= 1`, `< 1` change parseButton;
  z placed inside the feed's then-arm (`FEED_AT=in`, `!s` jumps there) still gets the
  early-return prediction (the `return 0`s are lowered to one return block at the end).  A
  pointer cp (`cp(s + 1)`) folds at once (inert).  The needed share of the head is 45.5..51.2%
  (`!s` = (2165 + f x 1333) x 131.66 / 10000 in [36.5, 37.5)); no single test gives it.
- a16pef1 (pe + the 61% feed): `!s` 40, 188 = 198 = 18 (-1001818: xellbutton2 gets the same
  head, the losing tie), dualboot's remopower 246 20 (was 19); op16sim with `!s` at -37 still
  fails on that tie.  Breaking the tie needs xellbutton2's call block (131.85) below 131.3
  while xellbutton's stays above (131.66), or a heap-history change.
- So the shared-header route needs a 2-test feed (split changes) and a tie breaker; closed.

### Don't retry (attempt 16)

- The natural parseButton split with any call-site spelling, helper, wrapper, result
  variable, nested ifs or test order at the xellbutton site, or any OPT/G assignment: the
  arithmetic above (264 = G x 21.6%, the join <= 86 and the call block <= 146 pin G to
  <= 132.6) closes it.  The site sweep is futile on that base.
- parseButtonX's hints moved into the shared parseButton: two-test feeds change the split,
  single-test feeds give 61% / 80.9% (need ~48%), and 188/198 then tie.
- Looking for the dx-like extra entry: on today's source the natural base needs only the two
  xellbutton keys.

### Result

No match; src/ unchanged (22 tricks).  The natural-split route is closed by arithmetic, not
by a missing spelling: the xellbutton site's two differing keys sit inside parseButton's
inlined split header, whose ratios are shared with xellbutton2 and dualboot and can't be
moved from the call site, and the neighbouring keys pin the call block's count.  The
xellbutton site needs a header of its own with a late-folding edge (parseButtonX and its
z feed) and a power probability <= 83.0% (bxe), and a header of its own can only call a
hand-written part, which brings `cold` and pbe with it.  So the 7 parseButton-side tricks
stand or fall together, and nothing natural replaces them; a next attempt on options needs a
new fact about the original (a build or the source), not another route here.

## Attempt 17

Focus: the hand-written part (cold, section, regparm, asm label) and pbe, via gcc's node
frequency and emission-order machinery.  Tool: `tools/wip/dehint/op17.py [variant ..]`
(variants of src with the part's declaration replaced; for each: optlib score after renaming
the part's symbol with objcopy, the .eh_frame section order, gcc's expansion order from
`-fdump-ipa-cgraph`'s "Time profile order in expand_all_functions", ipa-profile's
"Processing frequency"/"promoted" lines, fnsplit's choice, the sections).  Dumps under
build/op/a17/<variant>/.  gcc.gnu.org answered ipa-split.c with the Anubis bot page again; not
retried, everything below is from dumps.

### What each part form gives (op17.py)

- `st_cold` (static + cold, attempt 1): code identical, but expanded first (FDE order).
- `st` / `st_np` (static, no attributes, with or without pbe): **parseButton and
  applyIniOptions identical but for the call's reloc** (so without `cold` the winbutton
  expect is free, as attempt 3 found for gcc's own split); only the part's body differs (102:
  not size optimised) and it is expanded first.
- `gl` (global, no attributes): 120 (cdecl calls, not size optimised); `gl_cold` 29 (cdecl).
- `gl_cold_rp` (`__attribute__((cold, regparm(1)))`, no section, no asm label): identical
  (.text.unlikely instead of .text.startup, same place in the exe).  Not landed: same count.

### Why a static part isn't unlikely: parseButton's own split

- ipa-profile promotes a local function to unlikely only if every caller edge has frequency
  0 (call block freq x 1000 / caller entry freq, integer) or comes from an unlikely caller.
- parseButtonX's call edge is 0.  parseButton's call block is 6 of 10000 (edge 0), but
  fnsplit splits parseButton at the winbutton test (BB 6; BB 7, the call alone, is refused:
  split size 3 is not more than the call overhead), so at ipa-profile time the part is called
  from parseButton.part.2, whose entry is the winbutton block (37): edge 6 x 1000 / 37 = 162.
  part.2 itself is called with edge 3 from parseButton, so it stays normal, and so does the
  part.  The inliner later re-propagates frequency only for the nodes it inlines (part.2's
  copies are promoted then), never for the offline part.
- Probe (`-fno-partial-inlining`, not usable): the static attribute-free part is promoted to
  unlikely and its body matches.

### Why a static part is expanded first

- expand_all_functions (and the early local passes) go through ipa_reverse_postorder in
  reverse: externally visible functions (pass 0, walking callers) in source order, but local
  functions only called directly are reached in pass 1, which iterates the symbol list
  newest first and is expanded oldest first, before every pass-0 function.  A source static
  is older than baseFileExists.part.1 (made during early opts), so it comes before it.  A
  local function newer than the split part (an IPA clone), or one that calls a newer node,
  comes after it.

### MATCH: an always-0 `def` argument (op17.py st_cp, st_cpb, st_cpd, st_cp_last)

`static int parseButtonPart(const char *s, int def)` with `int b = def;`, both calls
`parseButtonPart(s, 0)`, no attributes, parseButton's plain `!strnicmp(s, "winbutton", 9)`:
IDENTICAL (code, sections up to the name, .eh_frame order); full build SHA256
10dac648...1971c.
- The call with two arguments has split size 4, so fnsplit now splits parseButton at the
  call alone (BB 7, accepted, lowest frequency); part.2 is entered from a block of
  frequency 6 (edge 0) -> part.2 promoted to unlikely, then the part (second iteration),
  then its own split part.  Size optimisation and .text.unlikely follow.
- ipa-cp clones the part for def = 0 for all contexts (`parseButtonPart.constprop.5`); the
  clone is the newest node, so pass 1 visits it first and it is expanded right after
  baseFileExists.part.1: the original's order.
- `b = parseButtonPart(s, b)` (b is 0 there), `int b` as the parameter itself, and the
  definition at the end of the file all give the same bytes.  Landed the `def` form (it
  reads like getIniU32's def).  Flagged borderline in the source.
- parseButtonX's tricks don't move: bxe 797, bxz 90, both 321 (= attempt 16's natural base),
  as before.

### Don't retry (attempt 17)

- A static or global part without the extra argument and without `cold`: parseButton's
  split at winbutton keeps it normal (above), whatever its position.
- Reading ipa-split.c from gcc.gnu.org (bot check).

### Next ideas

- The lever generalises: a constant extra argument makes a local helper an IPA clone
  (emitted after every split part, in front of the pass-0 functions) and enlarges its call
  for fnsplit.  Worth remembering wherever a static helper's FDE/emission order or a split
  point is the blocker in another object.
- parseButtonX's power expect and z feed still need the xellbutton site's own header
  (attempt 16's arithmetic is unchanged).

### Result

MATCH: 22 -> 20 tricks (the hand-written part and parseButton's winbutton expect).

## Attempt 18

Focus: attempt 17's lever (a constant extra argument to a static helper: bigger call for
fnsplit, unlikely-executed promotion, a late ipa-cp clone) applied to the remaining 20
tricks.  Tools (tools/wip/dehint/): `op18dis.py OBJ FUNC [a-b]` (one function with its
.rdata immediates shown as strings), `op18rm.py [-b base] [rm|a+b ..]` (op13's removal table
re-measured on a base), `op18bx.py [variant ..] [-o out.c]` (parseButtonX with a `def`
argument, tests on it as the z feed, and parseButton's chain as a shared `buttonOf(s, def)`),
`op18site.py [-r rms] [XPX ..]` (which of xellbutton / xellbutton2 / dualboot call
parseButtonX, x removals), `op18ms.py` (the dz1 asm goto behind a real call instead of the
memset), `op18z.py [form:pos ..]` (the z feed as one cp test).  Scratch: build/op/a18.

### Removal costs on today's source (op18rm.py): unchanged by attempt 17

rv2 44, po2 62, bxz 90, rv2i 304, dz2 304, dzall 304, ag2 304, ms 373, ag1 376, dz1 390, rv1ms
487, rv1 508, feeds 508, bxe 797, po1 811 (bxe+bxz 321, attempt 17).  The new part changed
nothing the other tricks depend on.

### A test on a constant argument is not a feed (op18bx.py)

- `def` used only as a value (`if (!s) return def;`, `int b = def;`, the part called with
  `def`), with or without each parseButtonX hint: exactly the hint's own score (no hint 321,
  no z 90, no power expect 797, both kept IDENTICAL).  Predictors don't see values.
- `if (def) goto z;` (and `def > 0`, `def < 0`, `def == 1`, `if (def) return def;`) at the
  power-fail head, called with 0, in place of the z feed: **90, the same bytes as no feed at
  all** (diff identical to bxz's), with or without `-fno-ipa-cp`.  profile_estimate does give
  the test 61% (call 71, early return 39) in parseButtonX's own body, but the parameter is a
  constant when the body is copied (ipa-cp's versioning, or the inliner without it), so the
  test folds during the copy and its edge is gone before the caller's frequencies are rebuilt
  (TODO_rebuild_frequencies at inline, attempt 16).  The cp feed works because
  __builtin_constant_p is folded only at fab, after VRP1 has threaded the z edge into the
  constant-0 copy.  So a clone is not "a separately estimated body": its counts are the
  generic body's probabilities minus the folded edges, i.e. the no-feed profile.
  (`!def`, or `def` with the call passing 1, makes the arm live: other code.)
- `def` used in a join (`if (!b) b = def;`, `return b ? b : def;`): 705-830, the part loses
  its unlikely promotion (102) and applyIniOptions changes.
- parseButton's chain as `static int buttonOf(const char *s, int def)` with parseButton a
  wrapper, the xellbutton site (S1) or all three sites (S2) calling it: buttonOf is emitted as
  its own function (`buttonOf.isra.0` / `.constprop`), 30698.
- So attempt 16's arithmetic stands: the xellbutton header's ratios come from predictors on
  its code, which no argument changes, and its z flow needs an edge that survives until VRP1
  (only a builtin does).  Single-test forms of the cp feed (op18z.py: 9 forms x head / part /
  power-success): best 90 (= no feed: `== 1` and the part position are inert), the rest
  257-919; the two-test feed stays.

### Button sites calling parseButtonX (op18site.py)

parseButtonX called from two or three sites (XXP, XPX, XXX, PPX), x removals (rv2, dz2,
dzall, bxz, bxe): 321-21597, never better than the removal alone.  Called twice it is split
again (the part loses its unlikely promotion, .text.unlikely and FDE order change), so the
attempt 17 split doesn't carry over to parseButtonX.

### The macid memset is the price of dz1's asm goto (pe dumps a18/pe_cur, a18/pe_ms)

- profile_estimate: with the memset, the validateString test is 71% (call heuristic: the
  false edge's first block holds a call); without it 50%: the asm goto ends that block on
  its own, the log calls are in the next block, and gcc 6's call heuristic only scans the
  edge's destination block.  The true edge's destination is the loop preheader (no call).
- Natural alternatives for the 71%: none.  validateString is uint32_t (`> 0` folds to `!= 0`),
  `== 1` gives 28%, a do-while puts myatox8 on the true edge (29%, wrong way), swapping the
  arms gives 50%, the loop as a helper call (attempt 13, mac_loop) is a call on the true edge.
- The asm goto behind a real call (op18ms.py: after the first log_printf 634, after
  showHexPairs 598, at the end 644): the chars warning no longer crossjumps with the length
  warning (the reference merges them at the first call; a block ending in the asm goto has an
  extra successor, so outgoing edges don't match): code changes.
- So ms goes only with ag1 (dz1), and dz1's group goes only with dz2's (dzall = dz2 = 304).

### Don't retry (attempt 18)

- Constant arguments as feeds or profile changers: a test on a constant argument folds when
  the body is copied (ipa-cp or inline), before the rebuild; a value-only argument is inert.
- parseButton's chain as a shared static helper (emitted out of line), parseButtonX at more
  than one site (split again).
- The z feed as one cp test (9 forms, 3 positions).
- Moving dz1's asm goto behind a call to drop the memset (crossjump lost).

### Result

No match; src/ unchanged (20 tricks).  The new lever only works where the blocker is a split
point, a node frequency or an emission order (attempt 17's part); every remaining trick is an
edge probability (bxe, po1, po2's literal order aside), dead flow that must survive until VRP1
(bxz, the rev feeds) or a zero-byte heap entry (the dz group, and ms through the call
heuristic), and a constant argument reaches none of them.  Stale comment noted, not changed:
the xellbutton2 site's "a dead edge into the remopower test" has no dead edge under it any
more.

## Attempt 19

Focus: parseOption from the reference (po1 = setBool expect, po2 = vlen expect).  Tools
(tools/wip/dehint/): `op19.py [-p N|-np] [-d dir] [-o out.c] [-v] variant ..` (variants are
edits on the attempt's start, i.e. src with the vlen expect put back; `-d` writes
profile_estimate, vrp1, optimized-blocks-details, jump2 and bbro dumps).  Scratch:
build/op/a19 (a19ref_po.txt = the reference's parseOption with its strings).

### What the reference does, in order

strlen(opt); `len <= 0` jumps to a setBool(opt, NULL) copy whose failure goes straight to
the incomplete message; the '=' loop (error return for `=` with no value inside it); strlen
again; `len == strlen(opt)` (no '=') goes to a setBool(opt, val) copy, then `val` (no value
options: incomplete, else the chain with vlen = 0 via `xor ebp,ebp`); otherwise strlen(val),
setBool, and the chain with val known non-null.  The chain ends with `test ebp,ebp` (vlen):
the incomplete block (already placed in the no-'=' trace, with its own epilogue copy) or the
unknown message (falls through, shared epilogue).  Literals: unknown 0xab4, incomplete
0xb08, bad 0xb58; "\n" 0x6ee just before "cputemp".  So the source shape is today's; the
two expects only set frequencies.

### po2: what the vlen expect does (op19.py po2 -v, bbro dumps)

Without it the only difference is the incomplete block's epilogue copy: bb-reorder copies
the return block into a trace end when the edge frequency is >= 10% of the entry's (570 ->
57).  The incomplete block's frequency is fixed at profile_estimate (threading redirects its
inflow but doesn't change it): the vlen block (113 = the val-null flow; the chain end adds
~0) x P(incomplete).  Plain: 50% -> 56, one short; the expect: 83% -> 94.  The unknown
block may have anything below 57 (a cold label on it, `coldu`, also matches).

### MATCH: `if (val && vlen)` (op19.py vv; vvn nested, vlv `vlen && val`: all IDENTICAL)

At profile_estimate the tail is one block (`val != 0 & vlen != 0`, non-short-circuit),
50/50, unknown 56 / incomplete 56: the same profile as plain.  But VRP1 can decide it on the
val test's false edge (val == NULL there), so it threads the val-null path (113) straight to
the incomplete block; the block's own frequency stays 56 until PRE's tail merge folds the
critical-edge forwarders into it (crited1 splits the edges; build/op/a19/vvall dumps: 56 at
crited1, 113 after pre).  The unknown block keeps 56.  With `vlen` alone the val-null edge
doesn't decide vlen (vlen is a PHI of 0 and strlen(val) over the merged setBool block), so
that path is threaded only by dom3/vrp2 and RTL, after the tail merge, and the block keeps 56.
The incomplete block keeps the vlen-false edge as a second pred, so it isn't merged into a
copy at the end (attempt 10/11's J forms) and its literal stays between the unknown's and
bad's.  Landed with a "Borderline, for review" comment (the `val` test is live but
redundant).  Full build SHA256 10dac648...1971c.

### po1: the setBool window is (16.67%, 18%), set by two bb-reorder comparisons

- Measured with the vlen edge as a cold label (`coldu`, first match, so `-p N` moves only
  setBool in parseOption): 82 (18%) 199 lines in parseOption, 84 (16%) 237, 83 IDENTICAL.
- At 84 the trace list is unchanged; connect_traces picks a different predecessor for the
  "\n" trace: the best edge by probability among unconnected trace ends, which are the
  len <= 0 setBool copy (p, inherited unchanged from profile_estimate when dom3/vrp2 copies
  it) and the macid loop's exit (PRED_LOOP_ITERATIONS for 5 iterations: 1/6 = 1667).  So p
  must be > 16.67% (a tie goes to the longer trace, macid's).
- At 82 the "\n" block starts its round-3 trace before gputemp's match (its priority edge,
  the '=' copy's done edge, passes gputemp's).
- The natural 9.2% (call 29, early return 39, `== 1` 28) also puts cputemp's head into the
  round-1 trace: its frequency is 450 x 0.908 x 0.698 = 285.2 against exec_th = 570 x 50% =
  285 (a knife edge; 17% gives 261).
- Natural values: 9.2, 13.7 (no early return), 19.9 (no call heuristic), 20.7 (no opcode,
  e.g. a switch), 28.  None is in range; 16.7/17.08 need a const-return prediction (a success
  path returning a constant other than 0/1), which the code (`mov eax,1`) rules out.
- Shapes tried: the setBool success after everything (`end`: `if (setBoolOption() != 1) {
  ... } log("\n"); return 1;`, no early return, 13.7%) and `goto done` at the end (`endeq`):
  315, .rdata (the "\n" literal must be numbered before "cputemp", so its block must come
  first), and bad then gets the early-return prediction; with macid's "\n" sharing it
  (`endeq+macnl`) 249.  A `done:` label in the setBool arm shared with macid (`lab`): 811 =
  po1, the setBool test dominates macid, so the call heuristic still applies.  With the new
  tail (vv+po1) 797.
- So po1 is closed unless the competitor changes: the macid loop exit (its trip count is the
  code's) or which trace ends are unconnected when the "\n" trace is joined.

### Lever reuse on parseButtonX (quick probe)

The caller testing s before parseButtonX (`if (s) xb.xellButton = parseButtonX(s);`, or a
conditional expression), alone and with bxe/bxz removed: 853-932 in applyIniOptions (the
power/remopower profile moves).  Not pursued.

### Don't retry (attempt 19)

- Any setBool shape that drops a predictor or adds one of the natural ones: the window is
  (16.67%, 18%) and nothing natural lands there (above).
- The setBool success at the end of the function (`.rdata`: "\n" before "cputemp").
- Sharing the "\n" block with macid by label (dominated anyway).

### Next ideas

- The lever that worked: a live, redundant re-test that VRP1 can decide on an existing edge
  moves a whole path's flow into one block without changing profile_estimate's edge
  probabilities.  Look for blocks whose final frequency (not an edge probability) is what a
  trick sets: the dz feeds and bxz need flow that survives until VRP1, which this doesn't
  give (it removes flow, early), but a block that must reach a threshold might.

### Result

MATCH: 20 -> 19 tricks (parseOption's vlen expect).  The `--param` stays (the setBool,
power and rev-feed expects remain).

## Attempt 20

Focus: attempt 19's lever (a live, redundant re-test that VRP1 threads) on the tricks that set
a block's final count: bxz (the xellbutton constant-0 block, 29 -> 37), bxe (remopower >= 18),
the rev feeds and the dz/macid group.  Tool: `tools/wip/dehint/op20.py [-m] variant ..`
(`px:NAME` replaces parseButtonX with a body from BODIES, `pxe:NAME` the same without the
power expect, `cs_*` call-site spellings; `-m` prints the score and the xellbutton site's
counts from the optimized dump: c0 = the `xb.xellButton = 0` block, power, remopower, remox,
winbutton, the part call, the log block).  Scratch build/op/a20 (d_* dumps), traces
build/v/aio_p1/a20*.

### How threading moves counts (dumps, then measured)

- A jump-thread *copy* gets the summed counts of the incoming edges grouped into it, as they
  are when VRP1 runs; the *original* blocks keep their stored counts minus the threaded
  paths.  So a re-test merging two flows (say the null path and power-fail) leaves its
  estimated split in the thread *targets* (the chain head keeps the share the estimate gave
  it, real or not: "retention"), while every copy carries only real entry-edge counts.
  Attempt 19's incomplete block was a target (plus PRE's tail merge); that's why it worked.
- The threader extends a path only through empty blocks, so the copy for the null path is
  the merge block that holds the `xb.xellButton = b` store and the `!xb.xellButton` test.
- c0 in the reference is that copy: its only pred is the null edge (132 x 21.6% = 28.5) but
  its count is 37, because the z feed's edge (600 of 10000, still live at VRP1, folded at
  fab) was grouped into the same copy.

### bxz: c0 is a copy, so a live test can't lift it (closed)

- The only real path with b = 0 is the null path.  A live re-test can only route real flow
  into a copy; extra (estimated, unreal) flow lands only on targets.  So c0 = G x P(null at
  the first test) with G the call block.  The power block is G x (1 - P), and it must stay
  103 (remopower 18 and the 0x11 join <= 86 need it: attempt 16), so c0 = 37 would need
  G ~ 140 and P ~ 26.4% at once; today G = 132 (the bootFlags & 4 test) and P is 21.6%
  (pointer 15, call 71, early return 39) or 30.2% (no early return).
- Measured (score, c0, power, remopower): nat (no feed) 90, 29, 103, 18.  `s &&` on the
  power test, then `else if (s)` or `else if (!s) return 0;` (sand, srt): 839, **40**, 92, 43
  (the null edge without the early-return predictor is 30.2%, the chain head keeps the
  re-test's estimate), and the part loses its unlikely promotion (102).  `s &&` on every
  name (sall) 514, 40.  Nested `if (s)` with `if (!b && s)` / `if (s && !b)` 989.  b as a
  flag (`if (!b) {chain}`, bflag) 206: c0 29, remopower 40.  `if (s) {...}` with no early
  return, every arm returning, returns per arm: all 90 (same bytes as no feed).
- Call sites (with the feed gone): `s` local, `int i` result, `if (!(xb.xellButton = ..))`,
  `== 0`: 90.  `if (!s || !xb.xellButton)` (cs_ors): **90, same bytes**, with the log block
  70 and the part 21 (retention lands there, and those counts don't matter); `!xb.xellButton
  || !s` 665.  The caller testing s (`if (s) .. = parseButtonX(s);`, with `else = 0`, `s ?
  parseButtonX(s) : 0`, with or without the body's own null test): 683-932, c0 40 (the
  caller's null edge is 30.2% too) and power 72 or 92.
- op16sim on srt: c0 40 is not the only change (power 92, the join 119, remopower 43, an extra
  block); overriding three keys still differs.

### bxe: retention is far too coarse (closed)

- Natural power is 83.25% (call 71 + const return 67) and remopower then 17 (needs >= 17.5).
  With the z feed kept the else head's first block has no call, so without the expect the
  power test is const return alone (67%): bxe 797, c0 44, remopower 34.
- A re-test that gives the else head extra estimated flow adds a whole predictor split of
  another flow (2160 or 6500 of 10000), not the ~0.2 count needed: b1 (flag, no feed, no
  expect) 678, remopower 52; with the z feed (zb1/zb2 `if (!b)`, zr1 `r` re-tested) 1123,
  c0 58, remopower 63; zb3 / zr2 (else-if forms) are the plain bxe bytes (797).  In the
  flag forms the power test itself goes to 50% (both arms reach the re-test block).

### The rest, by mechanism

- Rev feeds (rv1, rv2) and dz1/dz2: their job is the dummies' counts (dz1 47, dz2 8), and
  a dummy is reached only by its asm goto and the dead feed.  A live edge into it would be
  a real path to `__builtin_unreachable` (gcc gives it 0%, PRED_NORETURN), and a dummy is
  never a thread target, so threading can't give it count.  The getIniBool tie rv2 settles
  needs the extra extraction (attempts 13/15), and threading adds no heap entry without code.
- Macid memset: it sets validateString's split (71/29) through the call heuristic; the
  needed counts are 146 up *and* 149 down from 51/51, and retention only raises targets.
- po1 (setBool): connect_traces compares edge probabilities, not counts (attempt 19), so
  there's no count for a re-test to move.

### Don't retry (attempt 20)

- Re-tests of s or b in parseButtonX or at the xellbutton call site for bxz: c0 is a copy
  (only real entry-edge counts) and its only real flow is G x P(null), pinned by power = 103.
- Re-test retention for bxe: it moves whole predictor splits (remopower 34-63), and the
  feed's call-free head takes the call heuristic off the power test.
- Threading for the dummies' feeds or the macid memset (unreachable gets no live flow;
  retention can't lower a count).

### Result

No match; src/ unchanged (19 tricks).  The lever works only where a trick's job is a
thread *target's* count (an original block that keeps an estimated share after its inflow
is rerouted), as with attempt 19's incomplete block.  None of the remaining tricks has that
job: bxz's block is a thread copy, bxe needs ~0.2 count where retention gives tens,
the rev/dz group's blocks are unreachable, and the memset and setBool expects set edge
probabilities.  A free fact: the xellbutton log block's and the part call's counts don't
reach the bytes (cs_ors moves them to 70 and 21 with identical bytes to plain bxz).

## Attempt 21

Focus: small constant-table loops that gcc unrolls completely, as a new source of edge
probabilities (loop exit / loop iterations predictors, cunroll's per-copy frequency scaling),
for bxe/bxz (parseButtonX), po1 (parseOption) and the rev/dz group (applyIniOptions' OPT
sites).  Tools (tools/wip/dehint/): `op21.py [-m] [-p N] [-d dir] [-v fn] variant ..`
(`px:NAME` = parseButtonX table bodies; `ms_*` = macidSet loop forms; `opt2`, `opt2b`, `optd`,
`optj`, `optg*` = OPT/optIniBoolG sites as table loops; `hm5`, `hm6`, `hp5`, `sv5`, `sp5` =
parseOption's macid loop with a trip count unknown at profile_estimate; `vvn`, `n1`, `n2`,
`eq*` = parseOption tail / setBool / '=' loop forms; every op13.RM removal by name),
`op21ms.py` (stdin `op21.py -v FN v`: instruction multiset difference, tells layout-only
diffs from code diffs).  Scratch build/op/a21 (dumps per variant).

### Where unrolling happens, and what it allows (dumps)

- profile_estimate (042) runs long before cunrolli (087) and cunroll (151); VRP1 is 096, dom2
  110, PRE 123, dom3 166, vrp2 168, fab 174.  A loop's copies inherit the loop body's
  estimated probabilities; duplicate_loop_to_header_edge scales copy k by
  prob_pass_wont_exit^k (= 1 - the in-body exit share), and the folded exit edges leave
  their destinations' counts as estimated (inconsistent flow).
- cunrolli unrolls outermost loops only when the size doesn't grow (UL_NO_GROWTH):
  2/3 x (n x (size - eliminated) + last) <= size.  cunroll (late) allows growth only with no
  non-pure call on the loop's hot path.  strnicmp/stricmp are not pure (mingw's string.h),
  so a name-matching loop (call + test = 7 kept per copy, 5 folded) unrolls at cunrolli for 2
  entries only (t2ret); 3 or 4 entries are refused ("size would grow" at cunrolli, "contains
  call and code would grow" at cunroll; t4ret: size 12-5, unrolled 20).  The static table is
  dropped once unrolled (toplevel reorder is on for options), and its strings fold to the
  shared literals.
- A loop whose calls sit behind a test predicted not taken (OPT's `!(xb.bootFlags & set)`)
  has no call on the hot path, so cunroll (late, after VRP1/dom2/PRE) unrolls it with growth
  (optj: size 47 -> 56).

### parseButtonX as a table loop: closed

- Loop predictors predict *no match*: the match is an in-body exit (loop exit heuristic,
  first match, 9% / number of exits = 4.5%), the opposite of power's needed 82.13-83.09%
  match.  t2ret ({power, remopower} as a loop, the rest explicit): power 119, remopower 116,
  remox 111 (each copy keeps ~95% of the flow).  t1ret/t3ret/t4ret/t4sz: 911-1224.
- A no-break loop (match inside, keep scanning) would test the later names after a match:
  other code.  So no loop shape gives the power edge, and the z feed's +8 counts need an edge
  alive at VRP1, which a cunrolli loop doesn't leave (its exits are gone at 087).
- Fresh look at the reference (op18dis): the xellbutton site is today's chain exactly (null ->
  `xellButton = 0` copy -> log; each name `mov edx,X; je join`; part call stored and
  tested).  Nothing new for the source shape.

### OPT sites as table loops (applyIniOptions)

- opt2 (nomobile/noremap), opt2b (nosusecurity/smcnocheck), optd (demon/patchsmc), optg3,
  optg12, optg23 (the optIniBoolG triple): 1087-1769, all code changes (bootFlags in edx
  instead of eax: the loop changes register allocation).
- optj (nodvd and olddvd as `for (i = 0; i < 2; i++) if (!(xb.bootFlags & t[i].set))
  optIniBool(t[i].name, t[i].set, 4, 0);`, olddvd's set 0): **same code, other layout (597)**.
  The second copy's guard folds only at cunroll (bootFlags & 0), so olddvd's blocks keep the
  guarded count: a test that is dead only after unrolling, a new count lever.  Crossed with
  every removal: 457 (rv1ms, alone 487) to 999; none below the removal's own cost.

### macidSet's loop forms: a whole-function scale lever

- macidSet is early-inlined, so its loop header is applyIniOptions' hottest block at
  profile_estimate (10000; entry 1815): the function's counts are 10000 / (header visits per
  entry, 5.51).  Forms with the same CFG are IDENTICAL (break + `i < 6`, `i < 6 &&` in the
  condition, while, set+break flag, pointer, `< 0xff`, sizeof, `!(==)`, `return i != 6`).
  The do-while (`do { .. } while (++i < 6)`, PRED_LOOP_ITERATIONS 5/6) gives the same code
  and 4.90 visits: every applyIniOptions count x 1.125 (495 lines, rounding and ties).  Others
  change code (brkne, set, cont, and, cnt, rev).
- ms_do and ms_brkne crossed with every removal: none below the removal alone (ms_do+ms 605,
  ms_do+bxe 868).  A uniform scale can't do bxe's job (remopower >= 17.5 needs power >= 104.5
  at 83.25%, the 0x11 join <= 86 needs power <= 103.3) or any tie that needs one key moved.

### po1: two of its three constraints have natural fixes now; a knife edge remains

- The competitor (parseOption's macid loop exit, 1/6 by PRED_LOOP_ITERATIONS, or by the
  guessed-iterations predictor from the xb.macid[i + 1] array bound) drops to the plain loop
  exit heuristic (9.0%, below the natural setBool 9.22%) when the trip count is unknown at
  profile_estimate and the store isn't an array ref: `sp5` (`static int macidRestLen = 5;`
  never written, promoted read-only at IPA and folded by ccp2; `m = &xb.macid[1]; m[i] = ..`)
  or `hp5` (a static helper `macidRest(uint8_t *mac, const char *val, int n)` called with 5).
  Both are IDENTICAL with the expect kept; with po1 removed 340 (from 797).  `hm5`/`sv5`
  (array store) keep the guessed 1/6.
- The unknown-with-value block (must stay < 57, 10% of the entry, or it gets an epilogue copy)
  is 62 at the natural 9.22%; nested `if (val) { if (vlen) { unknown } }` (vvn) gives the
  vlen test the call heuristic (29/71): unknown 34.  vvn is IDENTICAL with the expect.
- What's left (sp5+vvn+po1, 305 lines): bb-reorder round 1 takes cputemp's head (450 x 0.908
  x 0.698 = 285.48 -> 285) into the round-1 trace, because exec_th = 570 x 500 / 1000 = 285
  and the test is `freq < exec_th`.  It needs P(setBool) >= ~9.26% (natural 9.22%), or
  P(val) <= 69.56% (natural 69.8 = pointer 85 + call 29), or the '=' loop's normal exit
  <= 78.7% (natural 450/570 = 78.95).  -p sweep with sp5: 84-86 (16-14%) differ only by the
  unknown epilogue (which vvn fixes), 88-90 (12-10%) 85 lines, 91 (9%, a tie with the 9%
  exit) 797.  Rounding can't help: for any entry E, round(0.50084 E) >= floor(E / 2).
- Natural setBool values in the new window (>= 9.26, < 18): 13.7 (no early return) and 17.08
  (const return).  `n1` (`if (setBoolOption(..) == 1) log("\n"); else { ..rest.. } return 1;`)
  gives the same CFG as today (still early return 39%); `n2` (log at the end, attempt 19's
  `end`) moves the "\n" literal (.rdata).  '=' loop forms: `break` 442 (3 exits), while /
  `i = len` 18 (code), `&& !val` in the condition 188: none moves the 450 cleanly.  The '='
  test as a one-case switch (eqsw: no opcode predictor, '=' 50%, entry 665) changes the
  loop's code (413 alone); `if (opt[i] != '=') continue;` (eqne) is IDENTICAL (same CFG).

### Don't retry (attempt 21)

- Table loops over button or option names: strnicmp/stricmp aren't pure, so more than 2
  entries never unroll, and the loop predicts no match.
- OPT pairs as loops outside the JTAG block (register allocation changes); macidSet forms for
  scale (only one alternative scale, inert crossed).
- po1 via the competitor or the unknown epilogue alone: both are handled above and the
  cputemp knife edge still holds it.

### Next ideas

- po1 needs one natural probability over a threshold: P(setBool) >= 9.26%, P(val) <= 69.56%
  or the '=' loop's normal exit <= 78.7%, together with sp5/hp5 + vvn.  Look for a predictor
  on the val test or the '=' loop that costs no code (e.g. the '=' test's own predictor, the
  `*val` test inside the loop), measured on sp5+vvn+po1.
- optj's late-folding guard is a natural count lever for blocks inside the JTAG block; it
  didn't help any removal crossed alone, but it could pair with another lever.

### Result

No match; src/ unchanged (19 tricks).  New facts: late cunroll (after VRP1/dom2/PRE) unrolls
loops whose calls are off the hot path, and a guard that folds only after unrolling is a
natural count lever (optj); macidSet's loop sets applyIniOptions' whole scale; po1 is now
down to one knife edge (cputemp's head 285 against exec_th 285) once its competitor and the
unknown block are handled (sp5/hp5 + vvn, both IDENTICAL with the expect kept).

## Attempt 22

Focus: po1 (parseOption's setBool expect) from attempt 21's near miss.  Tool:
`tools/wip/dehint/op22.py [-m] [-p N|-np] [-d dir] [-o out.c] [-v fn] variant ..` (op21's
variants plus this attempt's, joined by `+`; prints parseOption's line count; `-m` adds
block counts from the optimized dump: C = cputemp's head, G = gputemp's success log, nl =
the "\n" blocks, unk, inc).  Scratch build/op/a22 (base, p86, p88 dumps; land.c).

### Modelling first: attempt 21's knife edge was not the only constraint

- `-p` sweep on sp5+vvn (the expect kept, so P(setBool) = 100 - N): parseOption matches for
  N = 83..87 (17%..13%); 88 (12%) differs by 70 lines, 82 (18%) by 199.  (applyIniOptions
  moves with N too; only parseOption's count matters here.)
- The 70 lines at 12% are the "\n" block's epilogue copy: bb-reorder copies the return block
  into a trace end only when the edge count is >= 10% of the entry (570 -> 57), and nl =
  450 x P(setBool) (450 = 570 x the '=' loop's 78.9% normal exit; the len <= 0 copy's flow
  isn't added).  nl: 13% 58, 12% 54, natural 9.22% 41.  Since nl <= 570 x 0.789 x P, no
  P under 12.7% can pass, whatever C, Rexit or P(val) do.
- Emulation (an expect on the val test, `xval`, -p sets P(val), po1 removed): P(val) 64-69%
  moves C from 282 to 261 and G to 26, and parseOption still differs by the same 70 lines.
  So C < 285 (attempt 21's edge) is real but secondary; G's round-3 threshold isn't binding.
- So P(setBool) must be in about [12.7%, 18%): of the natural mixes (attempt 12's table) only
  13.7% (call 29 + `== 1` 28, no early return) and 17.08% (needs a non-0/1 constant return).

### Taking the early-return prediction off the setBool edge

The early-return heuristic (tree_estimate_probability_bb) fires for the "\n" block because
it has a single successor, the return block, which isn't its next_bb; it then predicts all
the block's incoming edges.  Ways out: the "\n" block right before the return block, or the
"\n" block going somewhere other than the return block.

- `gd` / `gd2` (the setBool success at the very end: `goto done;` with `done:` after bad, or
  the rest inside `!= 1`): P = 13.7%, C 271, nl 62, and the .text is the reference's except
  literal addresses (16 lines, all `.rdata` offsets).  But the "\n" literal is then first
  expanded in macid's "\n" block (strings are emitted in expansion order, the bb chain order
  at expand; gd's goes after macid's ":"), and nothing after profile_estimate moves the
  block back up (thread copies are appended, merges keep the first block's place).
- `a1`/`a3` (`set = setBoolOption(); if (set == 1) log("\n"); if (set == 1) return 1;`): the
  re-test gets opcode 28 + early return 39 = 19.9%, so the value options get 80.1% of 450:
  C 252, 97 lines.  `a1x` (that re-test with an expect, -p sweep): matches for 11%..18%, so
  the re-test's own prediction decides the chain's count (retention: the val test keeps its
  estimate after VRP1 threads the join).  `a2` (flag in the arm, `if (ok)` join: 39%) C 192.
- `b1` (`return set;` in the arm) = po1 (305); `b2` (a nested `if (set)` re-test in the arm)
  228.
- **`c1`..`c5` (MATCH)**: the join *after* the value options: `if (setBoolOption(opt, val)
  == 1) log("\n"); else if (val) { ..value options.. }  if (..) return 1;`.  The setBool
  test's false edge goes straight to the val test (no prediction of its own in between), so
  the value options get the test's whole false share (C 271, as gd), the "\n" block keeps
  its early place (literal order right) and goes to the join (no early return: 13.7%, nl 62),
  and VRP1 threads the join away.  All IDENTICAL with sp5 or hp5: c1 (`set` result, `set ==
  1` twice), c2 (`set = setBoolOption() == 1`, `if (set)`), c3 (`ok` as the result), c4 (a new
  `set` flag set in the arm), c5 (the existing `ok` as that flag).  With c4/c5 vvn isn't
  needed (unk 55 < 57); c1-c3 need it (unk 72 without).  `val && vlen` is still needed
  (`vl`, plain `vlen`: inc 55, 62 lines).  Without sp5/hp5: 237 (the macid exit 1/6 beats the
  len <= 0 copy's 13.7% edge).
- Landed hp5+c5 (the helper over the never-written static; `ok` reused, no new variable).
  `hp5` objects differ only in a clone number (`_parseButtonPart.constprop.5/.6`); the link
  strips symbols.  Full build SHA256 10dac648...1971c.

### Don't retry (attempt 22)

- Reaching po1 through C (cputemp's head), G or P(val) alone: the "\n" block's epilogue copy
  needs P(setBool) >= 12.7% regardless.
- The setBool success at the end of the function (gd, n2): .rdata ("\n" expanded late).
- A re-test of the setBool result right after the "\n" arm (a1-a3) or inside it (b2): the
  re-test's own prediction (19.9% or 39%) sets the value options' count.
- Helpers for the setBool test (attempt 12's h1-h4 again with sp5+vvn: 216-377, unchanged).

### Next ideas

- The lever: an arm whose block would go straight to the return goes to a join that a later
  test decides (threaded away by VRP1), placed so that no new prediction sits on the path
  whose count matters.  It removes exactly one early-return prediction.  It doesn't reach
  power (needs 82.13-83.09%; natural 83.25% has no early return to remove, and adding one
  gives 76%) or the zero-byte feeds.

### Result

MATCH: 19 -> 18 tricks (parseOption's setBool expect).  The `--param` stays (power and the
rev feeds' expects remain).  Borderline shapes landed: the `ok` join (c5) and the
macidRest helper (hp5), both commented in src/options.c.

## Attempt 23

Focus: the remaining `__builtin_expect`s (parseButtonX's power, bxe; the rev feeds' three:
e1 = dz1's inner test, e2 = dz2's outer test, e3 = dz2's inner test), their real windows
and natural replacements.  Tools (tools/wip/dehint/): `op23.py [-m] [-e] variant ..` (edits
on src; `-m` counts from the optimized dump: dz1/dz2, the rev block, the return block, the
xellbutton site; `-e` the profile_estimate succ probabilities and predictors of every cp test
and the power test), `op23g.py [-m] [-max N] STRUCT[:forms] ..` (the rev feeds as templates
in S x test forms: p plain, lt `< 0`, eq `== 5`, gt `> 0`, ne `!= 5`, e `expect(.., 0)`;
all combinations of cost < 7), `op23win.py REFTAG TAG blocks LO HI` (op16sim key window of
one block at a time).  Scratch build/op/a23 (g1.txt = the structure sweep), dumps
build/v/aio_p1/a23cur.

### The rev feeds: what each expect is for (profile_estimate, a23cur)

- Flow: the sprintf block 554; A (`cp(+1)`, no predictor: 50%) -> B (e1, 17%) -> dz1 47 or
  return; A false -> C (e2, 17%) -> D (e3, 17%) -> dz2 8 or return.  The return block is
  1807 - dz1 - dz2 (1760).
- Natural probabilities with the expect removed: e1 and e3 are 0.0% (PRED_NORETURN, first
  match, on every edge into a block that leads to __builtin_unreachable; only
  __builtin_expect and the loop-iteration predictors outrank it), e2 is 61% (early return:
  its false edge goes straight to the return block).  Measured: e1 508 (dz1 0), e2 245 (dz2
  29), e3 44 (dz2 0); bxe 797.
- Windows (op23win on a23cur, one key at a time): dz1 -79..-39 (any count 39..79), dz2 -8 or
  -7 only.  So e1 alone has P(B) in [14.1%, 28.5%] (with P(A) 50%) and e2, e3 each [13.8%,
  18.05%) with the other at 17%.  Probes agree: dz2 16-19 always gives the same 38-line
  getIniBool tie, dz1 86/89 gives 333, dz1 39 and 79 are fine.
- **A test whose two arms both go to dummies gets PRED_NORETURN on both edges**, and the
  first-match rule excludes a predictor that predicts both directions, so such a test keeps
  its other predictors.  DS still combines the two noreturn predictions (4 and 9996 of
  10000) in list order: when the TRUE arm goes to the later-numbered dummy (dz2) the
  integer rounding quantises the result (c -> k = round(4c/(9996(1-c))), P = k/(k+4): 0, 20,
  33.3, 42.9, 50, 55.6 ..%; `== 5` 28% -> 33.3%), with the TRUE arm to dz1 it gives back
  about c.

### MATCH: dz2's inner test as a split (op23g.py dd2:p,p,e,e; landed)

`if (cp(+1)) { if (cp(+2)) goto dz1; return; }  if (expect(cp(+15), 0)) { if
(expect(cp(+16), 0)) goto dz2; goto dz1; }`: dz1's own test has no expect (noreturn: 0%, no
flow), and dz2's inner test sends its other arm (83%) to dz1, so dz1 = 277 x 17% x 83% = 39
(the bottom of its window) and dz2 stays 8.  The return block is 1767 (was 1760).  dz1's
plain test is still needed: without it (`if (cp(+1)) return;`, `ar`) A's then-edge goes
straight to the return block and gets the early-return prediction (A 39%: dz 48/10, 38
lines).  `p,lt,e,e` and `p,gt,e,e` (B as `< 0` / `> 0`) are the same bytes.  Full build
SHA256 10dac648...1971c.  Rev feeds now 4 cp + 2 expects (was 4 + 3).

### Why the rev feeds can't lose another expect (arithmetic, then the sweep)

- Natural dz sources: an edge into a dummy from a test with one live arm is 0% unless an
  expect sets it; a split test (both arms dummies) keeps its other predictors, which for a
  cp test are only the compare's: c in {50 (plain), 73/27 (`> 0`/`< 0`), 72/28 (`!= 5`/`==
  5`)} (no call can sit in a dummy, no early return); pointer compares (`(void *)(long)cp
  == 0`, 15%) change the code (321-720).  So a split's dz2 share is 20% at best (TRUE arm to
  dz2, `< 0`: k = 1), or 27% (TRUE arm to dz1, `> 0`, fine order).
- dz1 must be >= 39 and dz2 <= 8, so dz2's share of the dummies' flow must be <= 17.9%:
  natural splits alone give dz1 <= 4 x dz2 <= 34 (q1/q2 probes: dz1 18-36 -> 460-484 lines).
  So at least one expect-driven edge is needed, and with D as the only split, D's 17% is it.
- C (dz2's outer test, 17%) natural: its false edge goes to the return block (early return
  toward then), so C is 61 / 36.6 (`< 0`) / 37.8 (`== 5`) / 80.9 / 80.1%; with A's forms
  R2 = 554 x {50, 73, 72, 27, 28}% the split's inflow R2 x P(C) must be in [47, 50) (dz2 =
  17% of it in [6.5, 8.5), dz1 = 83% of it >= 39): no product lands there (nearest 54.9:
  A `> 0`, C `< 0`, dz 46/9, 38 lines).
- The op23g sweep (cur, dd1, dd2, rv1, rv2, tri1, tri2, sp1-sp4 x {p, lt, eq, gt, e} with
  cost < 7; build/op/a23/g1.txt, scores <= 120 kept): the only IDENTICAL results are dd2
  with B plain / `< 0` / `> 0` and C, D expects (cost 6).  Every cost-4/5 near miss is the
  38-line getIniBool tie (dz2 9-19) or dz1 out of its window.

### Candidate: no rev expect at all, with a dead call (drafts/options_applyIniOptions_candidate.patch)

- The rounding above depends on which noreturn prediction comes first in the edge's list:
  predictions are prepended, and tree_bb_level_predictions adds them in block order, so the
  later dummy's comes first.  With the TRUE arm to dz2 and dz2's label *before* dz1's (the
  labels swapped at the end of the function, IDENTICAL by itself), the first factor is 9996
  on the TRUE edge and small probabilities come back unrounded (P(TRUE) ~ c).
- A split's c can only be < 17.9% with a second predictor, and the only one that fits a
  dummy's arm is the call heuristic: a call with side effects in the dz2 arm (dead, like the
  arm).  `if (cp(+16) < 0) { sprintf(xb.blSuffix, "_%s", s); goto dz2; } goto dz1;`: opcode
  27 + call 29 = 13.1% to dz2.  Its inflow 150 x 36.6% = 55 (A `> 0`: 73%, so R2 150; C `< 0`
  with the early return: 36.6%) gives dz2 7, dz1 48.
- `if (cp(+1) > 0) { if (cp(+2)) goto dz1; return; }  if (cp(+15) < 0) { if (cp(+16) < 0) {
  sprintf(..); goto dz2; } goto dz1; }` + dz2 before dz1: IDENTICAL, and the full build
  matches (SHA256 10dac648...1971c, built with it in src/ and then restored).  `!= 5` for A,
  `== 5` for C or D: also IDENTICAL.  Without the swap the same feed rounds to 20% (dz2 11,
  44 lines); without the call (D plain / `< 0`) dz2 16-18.
- Cost: 4 cp + 0 expect (the landed shape is 4 + 2), but the sprintf is a dead block whose
  only job is a prediction, so it is a candidate, not landed: by README's kinds it removes
  two more expects; counted as a dead-block trick it is one net.  With it, parseButtonX's
  power is the only expect left and the --param stays (power needs 83).
- Not possible without it: no cost-5 shape exists without a dead call (C natural needs the
  split's inflow in [47, 50) with D 17%; D natural needs a share <= 17.9%).

### bxe (parseButtonX's power): closed by a ratio, not a threshold

- Real window (dumps, callee scale): the else head E = 7836 x (1 - P) is kept by the
  remopower block after the feed folds (count E x 132/10000, must be >= 17.5: E >= 1326, P <=
  83.08%) and the z feed takes 45% of E into c0 (37: P >= ~82%).  The power-success edge
  7836 x P x 132/10000 must round to <= 86 (the 0x11 join's priority, attempt 16).
- Without the expect P is 67% (const return only): the z feed's cp test is the else head's
  first block, so the call heuristic sees no call (op23 -e).  With the remopower call ahead of
  the feed (`bxc`, `int r = strnicmp(..)` first) the power test is 83.2% (call 71 + const
  return 67) and remopower is 17 (321 = bxe+bxz: the feed's outer test loses its own call
  heuristic, 50%, c0 35).
- The join and remopower both scale with the power block, so their ratio is P / (1 - P) and
  must be <= 86.49 / 17.5 = 4.94, i.e. P <= 83.17% for *any* call-site count or `!s` share;
  the natural 83.25% (4.97) is out, and no predictor available on the power edges (call,
  const return, early return 39, negative/null return need other return values) moves it by
  the 0.1-1.1% needed.  A feed in the power-success arm (to cut the join's edge) takes the
  const-return prediction off the power edge (it lands on the feed's test): 71%.
- bxz as one cp test with a dead call in its arm (op23 probes, 15 forms): c0 36 or 40,
  never 37 (as attempt 18).

### Don't retry (attempt 23)

- Natural replacements for the rev feeds' C/D expects without a dead call: the arithmetic
  above and the sweep (g1.txt, g2.txt: cur, dd1, dd2, rv1, rv2, tri1, tri2, sp1-sp4, ar, ar1,
  a2, a21 x {p, lt, eq, gt, ne, e, e1}).
- Pointer compares on a cp result (code changes); a dz feed whose then-arm returns directly
  (early return); natural splits alone (dz1 <= 4 x dz2).
- bxe by any predictor mix (ratio bound 83.17%); bxz as one test.

### Result

MATCH: 18 -> 17 tricks (the rev feeds' e1 expect: dz1's inner test).  Landed dd2:p,p,e,e
(no borderline shape: the feed is still a counted hint, only its arms changed).  Candidate
saved: the rev feeds with no expect (a dead sprintf in dz2's arm, the dummies' labels
swapped): 17 -> 15 by README's kinds, 16 if the dead call counts.

## Attempt 24

Focus: the rev feeds' last two `__builtin_expect`s (e2 = dz2's outer test C, e3 = its inner
split D) with a *live* call doing the dead sprintf's job (attempt 23's candidate).  Tool:
tools/wip/dehint/op24.py [-m] [-e] [-show] variant .. (edits on today's src/options.c: the
two feed lines and the dummies' labels, or the whole rev stretch, or the asm goto label
lists; `-m`/`-e` are op23's counts and predictions).  Scratch build/op/a24 (ref.txt = the
reference's rev stretch, s1.txt, s2.txt = the sweeps).

### Why a live call can't do it (gcc 6's call heuristic, then the shares)

- The reference's rev stretch is plain: `"rev"` getIniValue, `je` to the shared epilogue,
  sprintf with its own epilogue copy (ref.txt 26c0-26f1).  Nothing in it but the live code.
- The call heuristic predicts edge e only if e->src dominates e->dest (and e->dest doesn't
  post-dominate it), scanning e->dest's statements.  A feed test is dead (cp folds to 0), so
  every block it dominates through its dummy-ward edge is dead too: a call there is a dead
  call by construction.  The live sprintf can sit only on a feed test's *live* edge, which
  makes the dummy-ward edge *more* likely (call 29% on the live edge -> 71% to the dummies),
  and on a test with one live arm the dummy edge is noreturn 0% anyway (first match).
- The shares are fixed elsewhere: dz2 <= 8 and dz1 >= 39 (attempt 23's windows, set by the
  getIniBool tie and other blocks' keys, not by the rev code), so dz2's share of the splits'
  flow must be <= 17.9%.  Flow reaches a dummy only through splits (both arms dummies), an
  expect, or loop-iteration predictors (first match beats noreturn).  A split's predictors
  are noreturn on both edges (cancel up to rounding), the opcode heuristic (27/28/50/72/73%)
  and a call in an arm.  DS rounding (TRUE arm to the later dummy): first step
  c x 4 / (c x 4 + (1-c) x 9996) rounds to k, result k/(k+4): k = 0 needs c < 11.1%, so
  natural splits give 20% at best; with the TRUE arm to dz1 (the earlier dummy) the 9996 comes
  first and the residual r = 10000 - round(..) gives dz1 4/(4 + r) roughly: `< 0` 26.6% (dz2
  73.4%), plain 50%, `> 0` r = 1 -> 80% (dz2 20%); dz2 0% would need c >= 88.9%.  Any mixture
  of splits is >= its smallest share: >= 20% > 17.9%.
  Closed without a call (or an expect) in a split arm.
- No PRED_GOTO: gcc 6's C front end adds no goto prediction (op24 `gi:`/`gv:`: dz1's label
  inline after dz2's goto, so only one arm has a goto; the profile_estimate dump lists no goto
  heuristic, and D stays 20%: dz 44/11, 44 lines).

### Probes (s1.txt, s2.txt)

- Feeds ahead of the live sprintf (`pre:`: B1 + split feed, then the sprintf; `mid:` split
  first, B1 after the sprintf): C's false edge now enters the call block, so the call heuristic
  sends C's true edge 71%+: natural forms 304-484 lines (dz1 93-458); with both expects kept
  `pre:e,e` is 38 (dz 45/9, the sprintf block 636: its count rises with the feed's false edge
  into it).
- The live code as early returns (`er:`, feeds after the sprintf): `er:e,e` IDENTICAL (dz
  39/8, ret 1767), same cost; natural forms 304-493.  Not landed: no trick goes, and the
  nested ifs are the shape the author seems to have used.
- Two-label asm gotos (`ag:`: macid `:::: dz1, dz2`, dualboot `:::: dz1, dz2`, either order,
  with and without the rev feeds): a block with more than two successors gets even
  probabilities (no noreturn), so the live fallthrough keeps a third: 687-1092 lines (rev
  490, dz 7-55).  Dead end.

### Secondary: parseButtonX's comment (fixed, comment only)

profile_estimate (op23 -e on today's source): the z feed's outer test 71.0% (the call
heuristic on its false edge, remopower's strnicmp), the inner `> 0` 63.4% (DS of the opcode
heuristic's 73% and the early return's 39%), so 0.71 x 0.634 = 45% of the else head (1332 ->
600) goes to z.  The comment said 3/8 (50% and 75%); now gives the measured numbers.
optlib IDENTICAL, full build SHA256 10dac648...1971c.

### Don't retry (attempt 24)

- A live call (the sprintf, getIniValue, a log_printf, kvSetDvdKey) on a dummy-ward edge:
  impossible by dominance; feeds before / around the live sprintf; early-return forms of the
  live code (only `e,e` matches, no gain).
- PRED_GOTO (not in gcc 6's C front end); inline dummy labels.
- Multi-label asm gotos (even probabilities).
- Any natural split form for D (>= 20% by the rounding arithmetic above), or mixtures of
  splits.
- What's left for e2/e3: a call in a dummy arm (attempt 23's candidate, a dead call), a
  third dummy (`__builtin_unreachable`, +1 trick, and it needs >= 6 cp for the flows:
  no net gain), or keeping the expects.

### Result

NO MATCH: 17 tricks.  src/options.c changed only in parseButtonX's comment (bytes
identical).

## Attempt 25

Focus: the whole dummy group at once (`dzall`: dz1, dz2, both asm gotos, the macid memset,
the rev feeds and their expects: 11 tricks), with the many-key levers found since attempt
13.  Tools (tools/wip/dehint/): `op25.py [-d] [-o out.c] [-v fn] variant ..` (`dzall`, the
OPT/G flips `f_<site>`, `msdo`, joined by `+`; `-d` writes p1/run.sh dumps as
build/v/aio_p1/a25_<variant>), `op25site.py BASE [-x extra] [-s sites]` (every OPT/G
assignment on a base), `op25inj.py` / `op25inj2.py` (p1/sim3 replay of a tag's round-4 heap
with an injected virtual entry: inserted after one head's events, deleted after another's
or left to be extracted).  Scratch build/op/a25 (a25map.txt = the dzall -> base block id
map for the replays).
(Attempt 27: op25map.py's own outputs in build/op/a25/m_*.txt are faulty: m_dzall.txt maps
149:150, m_nodz2a/m_nodz1c/m_xa collide; a25map.txt is sound.  Every replay below re-run
with controlled maps: the verdicts stand.  See "## Attempt 27".)

### dzall on today's source

- 304 lines (applyIniOptions only), as attempt 13.  Block ids: dzall's 149 is base's 149
  (the warning block, which in base has the asm goto block in front), 150..250 -> +1,
  251..258 -> +2, 259..261 -> +4 (a25map.txt).  r3 is the reference's; r4 differs in three
  tie groups only: the key-37 getIniU32 blocks with parseButtonX's constant-0 block (c0 pops
  9th instead of 1st), the key-19 iniBoolInvalid group (smcnoeject moves up after cygnos)
  and the key 4/3 getIniBool group (smcnoblink first; cygnos before smcnoeject).
- All block frequencies are the same in dzall and base (every block, after the id map): the
  304 lines are only the heap's structure (two fewer extractions), no count moves.

### What the dummies do to the heap, and what could replace them (replays on a25_dzall)

- op15sim: no single key change of any of the 75 entries with keys in -200..0 (any value in
  -200..0), and no pair within +-4, gives the reference order (0 hits; 1m40 of replays).
- op25mut.py: dropping any one round-3/4 insert (68) or moving any one insert to any other
  position of any group (20k replays): 0 hits.
- op25inj.py `-ext` (one extra entry left to be extracted, i.e. one dummy doing both jobs):
  any push point (end of any r3/r4 head's events) x key -400..0: 0 hits.  So one dummy
  can't replace the two.
- op25inj.py / op25inj2.py (one extra entry inserted, then *deleted*, as a real block that
  a later trace visits): **hits, but only one window**: inserted after 149's extraction (the
  macid chars warning's trace, dz1's push point), key -38 .. -100, and deleted anywhere in
  the trace of 197 (xellbutton2's parseButton chain) or, for keys -38 .. -60, early in the
  trace of 243 (dualboot, up to its `remopower` push); 100 hits, every one there.  An
  insert anywhere else (any head, any position of 155, 187, 197, 243, 74, 202's events) does
  nothing.  So one live entry that is in the heap during the consolidation at 187's
  extraction and gone before 243's 249 visit would do both dummies' jobs.
- Why no real block can be that entry: inserts come only from a trace's blocks' unvisited
  successors, and 149's trace is 149 alone (it ends in `jmp` to the crossjumped tail, placed
  in round 3); a block with key -38..-100 (freq 38..100, no trace-end pred) visited in 197's
  trace (freqs 17, 3, 0, 0) or 243's (147, 115) doesn't exist either.  Only a zero-byte
  successor of 149 that a later trace visits would fit, and a dummy has no preds to be
  visited through.
- op25swap.py (two inserts of one trace step swapped: the succ edge order, which an arm
  swap in the source changes with the same code; 202 candidate swaps in rounds 1-4):
  0 single hits, 0 pair hits (20k pairs).

### Subsets: one dummy group at a time (op25.py nodz1*/nodz2*/onedz*)

- nodz2a (dz2, its asm goto and label gone; dz1 fed by `if (cp1) { if (expect(cp2, 0))
  goto dz1; return; }`, dz1 57): 304; nodz2b (+ `return` form) 304; nodz2c (`> 0`, no
  expect, dz1 0) 333.  nodz1a/b/d (memset, dz1's asm goto and label gone; dz2 fed alone)
  376-474 (nodz1b has dz2 at 8 like base and is still 376); nodz1c 304 (dz2 94).  One dummy
  for both asm gotos (dualboot's targets dz1, onedza-c): 304-333 (the second push of an entry
  already in the heap is a no-op: its key doesn't change).
- op25inj on nodz1b (dz2 kept at 8, what replaces dz1): every one of 1763 hits inserts at
  149 (extracted: keys -39..-79, dz1's known window; deleted: the dzall window).  dz1's push
  point is unique.
- op25inj on nodz2a (dz1 kept at 57, what replaces dz2): extracted hits at three push
  points: 244 (dualboot, today's, keys -6..-8), **188** (xellbutton's parseButtonX trace,
  keys -8..-19 but -11) and 198 (xellbutton2's parseButton trace, -6..-8, -12..-19).  The
  wider -8..-19 window at 188 would let the rev feeds lose both expects: A `> 0` (R2 = 27%
  of 554 = 150), C plain (early return 61%: F = 92), D split `> 0` with its TRUE arm to dz1
  (80/20): dz1 73, dz2 18.
- But the push at 188 must come *after* the trace's last block, 193, is visited (insert
  position sweep in 188's events: only after `visit 193` hits).  193 is the jump-threading
  copy of the xellbutton/xellbutton2 join that reloads xb.bootFlags (preds: 191's
  xellButton != 0 edge and the default arm 192), pushed at 191 and deleted at its visit.  An
  asm goto in the default arm (`mv:xa`/`xb`/`xc`: before/after the log, after the store)
  pushes at 192, before 193's deletion: 191 lines at best, and the joint dz1 x dz2 key replay
  of those dumps (dz1 -120..-15 x dz2 -40..0, dummies dropped from the comparison) has no
  hit at all.  In the join itself (`xk`, end of the outer block) the bootFlags reload goes
  and the code changes (1002); between the statements (`xj`) 1144.  198's trace is
  parseButton's inlined body only (no applyIniOptions statement to hold an asm goto), and
  the "alternate xell button" block is a trace of its own (`ya`/`yb` 304/681).
- The feed x placement sweep (5 places x 5 x 5 x 5 forms x arm x label order) stopped after
  the model closed it; its first 600 rows: best 191 (`xa`), as the replay predicts.

### OPT/G site assignments on dzall (op25site.py, all 8192 of the 13 sites)

No match; best 280 (smcnoblink as G, with or without smcnoeject as OPT / nodvd as G), then
282, 286, 304 (= dzall).  Single levers on dzall: msdo (macidSet as do-while, x1.125) 485,
the 13 single flips 280-408.

### Don't retry (attempt 25)

- The whole dummy group by real keys or structure: singles over -200..0, pairs +-4, drop or
  move of any one insert, swaps of any one or two inserts of a trace step (arm order), all
  OPT/G assignments, the macidSet scale.  The replay's only fix is an entry pushed in 149's
  trace (dz1's push point) that a later trace visits, and 149's trace has no other
  successor: closed by the CFG.
- One dummy for both jobs (extracted at any push point, any key -400..0); dualboot's asm
  goto to dz1.
- dz2 moved into the xellbutton site (wider key window, natural feeds): the push has to
  follow the bootFlags-reload copy's visit; no statement lands there without changing code.
- dz1 without its push at 149 (unique in every replay).

### Result

NO MATCH: 17 tricks, src/ unchanged by this attempt.  The dz group's job is pinned to two
heap operations no natural CFG gives (replays above), so the 11 tricks behind the dummies
stay.  Next attempts on options have little left with real odds; if any, look at the
original's xellbutton/xellbutton2 statements (a shape whose join has no threaded reload
copy would let an asm goto in the default arm push after the trace's end, and the rev feeds
could then lose both expects: A `> 0`, C plain, D `> 0` split, dz1 73 / dz2 18).

## Attempt 26

Focus: attempt 25's last lead, a shape for the xellbutton / xellbutton2 statements that
lets dz2's asm goto push from xellbutton's trace after the bootFlags-reload block (wider key
window, so the rev feeds could lose e2 and e3).  Tools (tools/wip/dehint/): `op26blk.py TAG
FROM TO` (one line per cprop_hardreg block: preds/succs with probabilities, calls, xb
fields read/written, literals), `op26inj.py REFTAG TAG -map .. [-heads ..] [-lo -hi] [-r3]`
(extracted virtual entry inserted at *every* position of every r4 event group, or with
`-r3` pushed into the round-4 heap at every position of every r3 group).  Scratch
build/op/a26ref.txt (reference disassembly), a26m_nodz2a.txt (the nodz2a -> base block map:
op25map.py's plus `260:261` for dz1, which it leaves unmatched; attempt 25's
m_nodz2a.txt lacks it and replays give 0 hits with it), a26inj_all.txt.

### The stretch in the reference (a26ref.txt 24b4-26b8, 2c50, 3100)

- 24b4 `xellButton != 0` -> 2650; 24c2 `test al,4` (bootFlags still in eax from 248e) ->
  2570, else falls into 24ca (smcnoeject: the xellbutton2 test is threaded away).
- Matched names (power/remopower/remox/winbutton) set edx and jump to 2c50: `mov
  [xellButton],edx; mov eax,[bootFlags]; jmp 2650` (nodz2a block 262: the threaded copy of
  the store-and-test block, with PRE's reload on its edge).
- parseButtonPart path (191): `call; test; mov [xellButton],eax; jne 2648`; default arm
  (192: log, `mov [xellButton],0x12`) falls into 2648 `mov eax,[bootFlags]` (193, the
  reload), then 2650 (194: xellAltButton test), 265e `test al,4` (195: a retest of the
  reloaded value).  So the original reads bootFlags in both conditions: a local copy read
  once would drop that retest; the reloads are PRE insertions on the call paths' edges.
- 2672-26b8 xellbutton2: parseButton inlined, store, `xellButton` test (the log at 3100),
  reload 26b3, back to 24ca.

### Why no source position lands after 193 (the mechanism)

- Events of 188's trace (nodz2a): visit 188..191, `ins 193 (-38)` (191's ne edge, 0%),
  visit 192, visit 193 (delete: consolidation).  A push after that is a successor of 193
  or of a block between 193 and 194.  194 was placed in round 2, so the trace ends there.
- Such a block N must be on 191's ne edge and the default arm (193's preds) but not on 262
  (the matched names' copy), or 262 loses its own reload (attempt 25's `xk`, 1002 lines:
  the reload moves after the asm goto, one copy for all paths).
- 262 and 191's ne edge leave the store-and-test block by the same edge (`v != 0`); the
  only predicates gcc can decide on these paths are about v, and v is {0x11, 0x20, 0x22,
  0x24} on one and an unknown nonzero value on the other, so they agree on every
  decidable test: any block after the test's false edge (an `else`, the end of the
  outer block, a statement before the xellbutton2 test, a re-test of `xb.xellButton`,
  which VRP1 threads on every incoming path) is on both.  Only a test on the value
  (`v > 0x24`) separates them, and that stays in the code on the part path.
- The default arm alone (`xa`-`xc`) pushes before 193's deletion; nested ifs instead of
  `&&` lower to the same CFG; an asm goto at the end of an outer `if (!xb.xellButton)` (a
  nested form) also sits on the bootFlags&4 == 0 path, which can then no longer be
  threaded past the xellbutton2 test (asm goto blocks can't be threaded through); the two
  sites can't swap (the second's log reads the first's result).

### Full position map (op26inj.py, a25_nodz2a against a25_base, keys -60..0)

- r4, every position of every group: 188 @7 only (after `visit 193`: -8..-19 but -11);
  198 @0..@4, i.e. anywhere in xellbutton2's parseButton trace (198-201: remopower, remox,
  winbutton, parseButtonPart; -6..-8, -12..-19); 244 @2..@4 (dualboot's parseButton:
  after 244 pushes 250, before 250's visit: a block between the null test and the power
  test, or on the power-match edge; -8..-19); 244 @0/@1/@5/@6 (-6..-8; @6 is today's
  asm goto in the "dualboot setting ignored" block).  13 positions, all listed.
- r3 (pushed into the round-4 heap), every position of every group, plain keys -60..0
  and trace-end priority keys -1000060..-1000000: 0 hits (so 196's getIniValue, 202's
  store-and-test and 204's reload, the xellbutton2 statements' own blocks, are out).
- So every wide window except 188 @7 is inside parseButton's inlined body (shared with
  parseOption; an asm goto there can't name applyIniOptions' label, and a dummy defined
  inside a private parseButton copy can't be fed by the rev feeds).

### Not tried (no real odds)

- A private parseButton copy for xellbutton2 holding dz2 and its own feed: the feed must
  sit in 198's trace (freq 17) and needs P >= 70% to give 12..19, which takes the flow
  of 199-201; dz1 would need its own expect back (nodz2a's e1); the copy exists only to
  match (a candidate at best), net at most one trick.

### Don't retry (attempt 26)

- dz2's asm goto anywhere in or around the xellbutton / xellbutton2 statements: else arm,
  end of the outer block, between the statements, nested-if forms, a re-test of
  `xb.xellButton`, a local bootFlags copy (the reference reloads and retests it), helpers
  for the xellbutton2 site (its blocks are parseButton's).  Closed by the `v != 0` argument
  above and the full position map.

### Result

NO MATCH: 17 tricks, src/ unchanged by this attempt.  The lead closes by the CFG; the dz
group has no route left that the replays allow.

## Attempt 27

Focus: audit of the recent closures, starting from attempt 26's finding that attempt 25's
m_nodz2a.txt lacks `260:261`.  Tools (tools/wip/dehint/): `op27map.py REFTAG TAG` (fixed map
generator: map line, drop line; stderr lists gap pairs, head fixes, drops, collisions),
`op27ctl.py REFTAG TAG [-map FILE|auto] SPEC ..` (Replay class; positive controls: virtual
entries injected at HEAD@POS:KEY, optionally deleted), `op27joint.py REFTAG TAG DZ1,DZ2`
(joint.py with op27map's map), `op27dom.py` (dominance probes for the call heuristic),
`op27y.py` (the private parseButton copy).  Scratch build/op/a27 (re-run outputs),
build/op/a27m_<tag>.txt/.log (fixed maps for every a25 dump).  op25map.py now prints a
superseded warning (its output is unchanged).

### What was wrong with op25map.py

- It aligns (freq, signature) and prints only matched ids.  The replays do `MAP.get(x, x)`,
  so an unmatched TAG block keeps its own id, which collides when another TAG block maps to
  that id: nodz2a's dz1 260 vs 259:260 (base's sprintf), xa's asm goto block 193 vs 194:193,
  nodz1c's dz2 260 vs 259:260; xb would have had three.
- The replays compare trace *heads*.  dzall's 149 is base's 150 by content, but base's trace
  149-150 has head 149, so `149:150` (m_dzall.txt) leaves a TAG head that never appears in
  the reference's head list: every replay fails.  a25map.txt (149:149, hand-corrected) is
  right.
- Fix (op27map.py): equal-length gaps between anchors are paired in order (the dummies),
  unequal gaps by unique signature; a TAG head mapped to a non-head takes its REFTAG
  trace's head if free; leftover TAG blocks are a drop list; targets checked unique.
- Positive controls (op27ctl.py): base vs base True; dzall + dz1 at 149@1:-39 + dz2 at
  243@6:-8 True with a25map.txt and auto, **False with m_dzall.txt**; nodz2a + 244@6:-8 True
  with a26m_nodz2a.txt and auto, **False with m_nodz2a.txt**; xa with its dz2 insert removed
  and a virtual dz2 at 245's end (-8) True for dz1 -39/-57/-73 (auto map, drop 193).

### Re-runs (controlled maps)

| Replay | Attempt | Map now | Result |
|---|---|---|---|
| op25inj -ext on dzall, keys -400..0 | 25 | a25map.txt | 0 (stands) |
| op25inj deleted-entry on dzall, -100..0 | 25 | a25map.txt | 63 hits, all at 149 -> 197 (= attempt 25's window -38..-100) |
| op25mut drop / move on dzall | 25 | a25map.txt | 0 / 0 (stand) |
| op25swap singles / pairs on dzall | 25 | a25map.txt | 0 / 0 (stand) |
| op15sim singles -200..0, pairs +-4 on dzall | 25 | a25map.txt | 0 / 0 (stand) |
| joint dz1 x dz2 keys (-120..-15 x -40..0): xa-112, xa-121, xb-112, xc-112 | 25 | auto (drop 193 / 192 / none) | 0 each (stand; xa's control passes) |
| op26inj r4/r3 position map on nodz2a | 26 | a26m_nodz2a.txt (passes) | as attempt 26 (not re-run: same map bar dz1's pairing) |
| op26inj with op25map's raw nodz2a map | (demo) | collides | 0 positions (build/op/a27/n2_inj_collide.txt) |

So no "0 hits" verdict of attempts 25-26 changes, and there are no new hits to follow.
inj1/inj_nodz1b/inj_nodz2a (attempt 25, all with hits) must have used sound maps already.

### Attempt 24's dominance argument, from the dump (op27dom.py, -fdump-tree-profile_estimate)

- `dom` (C's true arm into a block holding a call it dominates): "call: 29.0%", combined
  39% with the early return.  The heuristic fires.
- `nodom` (a cp test whose true edge jumps to a label on dualboot's live "setting ignored"
  log block, which it doesn't dominate): "no prediction: 50.0%".  No call heuristic.
- `nodom2` (a cp test in dualboot's block, true edge to a label on the live rev sprintf):
  "call: 71.0%" towards the sprintf, i.e. the heuristic predicts the *other* edge (into the
  log block, which the test dominates) not taken.  So a live call acts only through
  dominated blocks, as attempt 24 said: the argument stands.

### The private parseButton copy (attempt 26's untried idea; op27y.py)

parseButtonY = parseButton with a dz label of its own, used for xellbutton2; dualboot's asm
goto removed; the rev feeds as nodz2a's (`if (cp1) { if (expect(cp2, 0)) goto dz1; return;
}`).  Feeds: expect(cp, 1|0), nested with/without `return 0`, `> 0`; at the top, in the
power-failed arm, in the remopower-failed arm; with and without an asm goto to dz; copy
before parseButton or before applyIniOptions (same results in y1; y2.txt keeps only the
`before` rows).  build/op/a27/y1.txt, y2.txt.

- Without an asm goto the dummy is gone by bbro (dz=[57] only: a block reached only by a dead
  feed dies with it).  So the copy needs its own asm goto: the dualboot one moves, it doesn't
  go.
- With it, a feed that gives dz2 its window count (14-20: `ag`+`n2e`/`e1` in the else arm)
  drains that flow from every later block (noreturn mid-function: rev 554 -> 546-550, the
  return block 1757 -> 1730-1744): 850-1000 lines.  Today's dummies get their counts from
  feeds at the very end, where nothing is downstream; a copy's feed can't be there.
  Best overall 304-368 (dz2 0-1, i.e. no count).  Net trick count would have been -1 at
  best (rev -3, copy +1 cp +1 expect, asm goto moved) with a duplicated function: no odds.

### Don't retry (attempt 27)

- Any replay with op25map.py's m_*.txt files; use op27map.py and check a positive control
  (op27ctl.py) before trusting a 0.
- The attempt-25 replays above (all re-run: they stand); the xa/xb/xc joint keys.
- A live call for e2/e3 (dominance confirmed in the dump).
- A dz2 fed inside a parseButton copy (needs its own asm goto; mid-function flow drain).

### Result

NO MATCH: 17 tricks, src/ unchanged.  The audit found three faulty map files (and the
generator's two flaws) but every closure they fed still holds with sound maps.

## Attempt 28 (2026-11-09): the `--param builtin-expect-probability=83` alone

Goal: plain `-O3`.  Scratch: the session scratchpad's `pw/` (run.py swaps parseButtonX's
body into a base file and runs optlib; v1-v6 are the variant sets).  Base: src + the
dead-sprintf candidate (drafts/options_applyIniOptions_candidate.patch), which is IDENTICAL
at -p 83 and leaves parseButtonX's power expect as the only reader of the param.

- `-p N` sweep on src: only 83 is IDENTICAL (82: 67 lines, 81: 235, 84: 466, 90/-np: 862,
  all in applyIniOptions).  With the candidate, -np is 883.
- Without the param an expect is 90/10 (first match, no DS), and the power edge can't use 90:
  the 0x11 join is 187 x P <= 86.49, so P <= 83.5% whatever else the else arm does.
- `callfirst` (`int r = strnicmp(s, "remopower", 9)` ahead of the z feed, `!r` after it):
  power 83.2% (call 71 + const return 67) with no expect, 321 lines.  The z feed's spelling
  (8 x 8 outer/inner forms) doesn't move those 321: the remopower head (1313 at callee scale,
  17 at the site) is the whole difference.
- Extra flow into the else head, to lift 1313 to >= 1326 at 83.25%:
  - from the `!s` arm (`if (!s) { if (cp) goto el; z: return 0; }`, 20 forms): the head then
    has a predecessor that the power test doesn't dominate, so PRED_CALL drops off the power
    edge (67% only) and `!s` loses its early return (30.2%).  497-1000 lines, and big inflows
    change parseButtonPart's clone.
  - from the power-success arm (`b = 0x11; if (cp) goto el;`, depth 1-5 nests, 4 x 4 x 4 x 2
    forms): the 0x11 PHI edge now leaves the dead test, so predict_paths_leading_to_edge puts
    const return on the dead test (33% to el) and the power edge has only call (71%).  Head
    3167, part call 8 (needs 3): 497-1183 lines, and parseButtonPart.constprop changes.
  - Flow budget: with P = 71% the 29% not on the success edge must go to c0 (264, exactly 37)
    or into the chain (remopower 733, part call ~3).  No z-feed split satisfies both, so a
    success-arm feed can't work at any q.
- Fixed-probability mechanisms at gcc 6's defaults: expect 90, PRED_LOOP_ITERATIONS 1/n (5/6 =
  83.33% is above the 83.17% ratio limit), a switch's even 1/n edges, hot/cold labels and
  noreturn at the extremes.  None lands in (82.13, 83.08].  So at default params the power edge
  can't be given its probability by any spelling, hinted or not, within the constraints
  attempt 16 measured (remopower >= 17.5, join <= 86.49, c0 = 37).
- The rev feeds' expects (e2/e3, 17%) would also break at 90/10; only the dead-sprintf
  candidate frees them, and the user has not ruled on it yet.

### Result

NO MATCH: the param stays (17 tricks, src/ unchanged).  To remove it, one of the three keys
attempt 16 measured has to change: the 0x11 join's competitor (key -1008702), the remopower
threshold, or c0.  That is the heap-model search (p1/sim3, op16sim) with other entries moved
too, not a parseButtonX spelling.

### Attempt 28, continued: heap keys on the no-expect base (after 466b8dce)

Dumps: build/v/aio_p1/r28 (src at -p 83, the reference trace), cf28 (`callfirst` at plain
-O3), cfgg (callfirst with the z feed as `cp(+1) > 0` / `cp(+2) > 0`, 333 lines).
op16sim on cf28: two keys are off: xellbutton's remopower 188 (17/17) ties xellbutton2's
198 (17/17), and c0 263 is 35.  In cfgg the `> 0` outer test (73% x 63.4% = 46%) puts c0 back
at 37, so **only 188-vs-198 is left**: the replay matches for any 198 below 17/17 (edge <= 16,
or edge 17 with block <= 16), with every other key as compiled.

Why 198 can't move:
- Both sites have the same call-block count (132 = 907 x 50% x 29%) and the same callee head
  (1313 = 7836 x 16.75%), so they round to the same 17.  188 can't go up (the ratio limit
  above), so 198 must go down: G2 <= 125.6 or parseButton's head <= 1249.
- G2 is pinned from below: 203 (the "alternate xell button is disabled" block, G2 x 29%) must
  stay >= 38 and 202 (the store after parseButton, priority from the power-success edge
  197 x 83.25%) must keep priority >= 87 (replays with 203 <= 37 or 202 at 86 fail).
- parseButton's header profile doesn't change with spelling: nested `if (s)`, return-only
  arms, `b = 0` arm, `return 0` last (w3/w4 sets): the same 21.6% / 83.2% predictions and
  the same keys.  Raising its `!s` share (dead feed in the `!s` arm: DS(15, 71) = 30.2%) drops
  197 and with it 202's priority; any dead test ahead of the power call removes PRED_CALL
  from the power edge; one in the success arm takes const return.
- So with today's applyIniOptions the two sites can't be told apart without an
  exact-probability hint inside one header.  The param (or a hint on 202/203 that the source
  can't make) stays.  A route that's still open: anything that changes the heap order of
  equal keys (the tie goes to xellbutton2: insertion order), which no source lever found so
  far reaches.

### Attempt 28, last: the tie order, and why the sites need different power odds

- Tie order (scanpw scripts scanbig/scanins/scanmove on cfgg): no single key change of any
  other heap entry (large -100xxxx keys +-300 included), no dropped entry and no inserted
  dummy entry (every event position, 14 keys, push and ins) flips 188/198.  Moving 198's key
  change works only if it happens in round 4 after 188 is popped, which no source shape
  controls (it follows from 197's trace end in round 3).
- The constant-store joins pair up the same way: xellbutton's 264 (86/95) must pop after
  xellbutton2's 202 (87/32), and 264 at priority 87 works only with a frequency below ~32
  (it's 95, the whole nonzero-b flow).  So the xellbutton site needs a *lower* join and a
  *higher* remopower than xellbutton2, with the same call count (132) and the same `!s`
  share: that is exactly P(xellbutton) < P(xellbutton2), whatever G does.
- The other way round (parseButtonX natural at 83.25%, an expect in parseButton): at -p 84-86
  that is 162 lines, and the replay fixes 188/198 (198 at 15) but dualboot's remopower 246
  drops to 17 and needs 19 (its natural 83.25%); -p 87-89 is 511-597.  So the three
  parseButton sites need three different power probabilities (xellbutton <= 83.08%,
  xellbutton2 >= 84.06%, dualboot 83.25%), and the param plus parseButtonX's expect is the
  cheapest way found to give them.

Closed: the param can't go without reshaping the button-parsing sites altogether (for
example a different copy per site, which would cost more tricks than it saves).

## Attempt 29 (2026-11-09): the `--param` removed

Goal: plain `-O3` for options.  Tools: `op29gen.py` (parseButtonX bodies with up to three dead
tests in four slots), `op29fast.py` (profile model from a standalone compile, 0.25 s each),
`op29run.py` (real compile against the reference).  bbro dumps: build/v/aio_p1/n1hit, n1hit0.

### What attempt 28's wall rests on, and where it's open

- Confirmed: with the power block at 103 the else edge and the success edge come from the
  same block, so success <= 86 and else >= 17.5 need P <= 83.17%, and no predictor mix on
  an `== 0` test of a call result lands in 82.13-83.09% (call 71, constant return 67, one
  opcode heuristic of 72 or 73 in either direction: the sums of their log-odds miss the
  window; the constant return can't be doubled, and any branch in the success arm takes it
  off the power test).
- Confirmed: the other way (else edge 17 with the else head's block at 18) needs dead flow
  into the block that holds remopower's call.  A source outside the power test's dominance
  drops the call heuristic; one in the success arm takes the constant return; one in the
  else arm is a loop, whose preheader is empty.  A dead `memset` block ahead of the else
  head keeps the call heuristic, but the memset lasts until expand, so cleanup merges the
  head into it and the merged block keeps the memset block's count (a `for (;;)` with a
  dead `continue` inflates the head by 1.37 in the profile and still scores cfgg's 333).
- Open: the power block itself (187) is never in the heap (`op16sim.py r28 TAG -keys 187`:
  None), so nothing pins it at 103.  The keys are 186 (the call block, 132), 188 (else
  head: 100 x edge + block in 1718..1918), 263 (constant-0 block, exactly 37), 264 (join,
  priority <= 86) and the part's call (< 10 at callee scale, so its cgraph frequency is 0).
  A dead test at the function's entry halves everything behind it without touching 186.

### The model (op29fast.py)

Block counts at the site are round(freq x 132.3 / entry) and edge counts round(block x
probability); 263's count is the sum of the *rounded* edges that carry b = 0 (the threaded
copy takes its edges' counts), which is why a real-valued 36.52 can be 36.  Checked against
bbro: n1hit gives 188 = -1001727, 263 = -36, 264 = -1003596, as the model says, and
`op16sim.py r28 n1hit -k 263=-37` replays the reference order.

### Search and MATCH

- All bodies with up to three tests of the forms cp, `> 0`, `< 0` (24453 per call
  position): three fit every key but 263 (36), all with an entry test split between j and
  el and one `> 0` test to z at the else head.
- The 263 pieces are `!s` 14 (66 x 21.6%) and the feed's round(el x 80.9%): el 27 gives 22,
  el 28 gives 23.  el is 1293 + 5000 x c at callee scale, c the inner test's share to el:
  15.4% for `> 0` (27), 16.1% for `== 1` (28: nonequal's 28% in place of positive's 27%).
- `if (cp) { if (cp == 1) goto el; goto j; }` at entry + `if (cp > 0) goto z;` at the else
  head: **IDENTICAL at plain -O3** (model: N 52, ps 67.0, succ 35, fail 17, el 28, z 37,
  part 2).  Full build SHA256 matches.

### Result

MATCH, landed: 15 tricks (param and expect out, one `__builtin_constant_p` in), build.sh's
options case removed, optlib.py's default flags now plain `-O3`.  Not natural code: the
three tests are dead hints like the two they replace, and parseButtonX is still a private
copy of parseButton.

### Don't retry (attempt 29)

- Dead inflow into the else head by a `memset` block, a loop or a success-arm feed (above).
- Up to three tests with remopower's call ahead of the else-arm feed (CF=1): no fit in a
  full run of the first, real-valued model (the rounded model's run was stopped at the
  match); the call heuristic there keeps the power test at 83.25% or 71%.

## Attempt 30 (2026-11-10): the whole function, not one key

Focus A (a whole-function view of the dummy group), started from the fully natural file
and not from today's CFG.  Tools (tools/wip/dehint/):

- `op30.py [-d] [-o out.c] [-v fn] variant ..`: edits joined by `+` on commit 80a383bf's
  src/options.c (the 15-trick source): `dzall` the dummy group gone, `natx` parseButtonX
  gone, `nat` both, `int{b,c,d,e}` optIniInt forms called directly with the INI_INT macro
  gone (`ifn{b..}` the form alone, `icalls` the calls alone), `pbfold`/`pbfoldi`
  parseButtonPart folded back into parseButton, `f_<site>` OPT <-> optIniBoolG, `allopt`;
  `src` is today's file; `-d` writes plain -O3 p1/run.sh dumps as
  build/v/aio_p1/a30_<variant>.
- `op30tr.py TAGA TAGB [-r N]`: two dumps' trace heads side by side by block name.
- `op30site.py [-all] [-base V]`: OPT / optIniBoolG assignments on the natural base.
- `op30chk.py`: which of the landed shapes are load-bearing (one edit each on today's src).

Scratch build/op/a30 (options.orig.c = the source before this attempt).

### What the closures of attempts 13-29 all assumed

Every replay (op13sim .. op29fast) changed one or two keys on the hinted source's CFG, kept
every other block's count, and asked for the hinted dump's trace *extraction order*.  Three
of the things held fixed were never facts about the original:

- **GU = 37** (the eleven `-1` options' getIniU32 blocks; p1/NOTES.md "GU must be 37", the
  INI_INT macro's 15%).  The layout only says the blocks come after the 38-group and before
  the 19-group.
- **c0 = 37 exactly** (the block that stores xellbutton's 0 for a missing value; "must pop
  ahead of the key-37 getIniU32 blocks").  c0 sits right before the getIniU32 blocks, and
  with GU fixed at 37 that reads as "c0 wins their tie".  With a natural parseButton c0 is 29
  (132 x 21.6%), so all the layout needs is 29 > GU > 19: no tie at all.
- **188 before 198** (attempt 28: xellbutton's remopower trace must pop before
  xellbutton2's, so the two sites need different power odds).  In the natural source both
  keys are -1001717 and 198 pops *first*, with identical bytes: 188's trace is connected
  behind 187 by connect_traces ("Connection: 187 188"), so its own position in the trace
  list places nothing.  The reference is the layout, not a dump's extraction order; the
  order only mattered on the hinted heap, through what it did to later ties.

The dummies, parseButtonX's feeds and the G/OPT split were all repairs of tie orders on a
heap that had c0 inside an eleven-block tie.

### The getIniU32 blocks at 10.1%: optIniInt returns early on the good path

- Direct `optIniInt()` calls with the warning arm going to the return (the old `if (bad) {
  log; return def; } return getIniU32();`, or a result variable with the bad arm first):
  the early-return heuristic sits on the edge into the log block, DS(85% pointer, 39%) =
  78.4%, so GU is 21.6% of 249 = 54 and the eleven blocks pop ahead of the 38-group (595
  lines on the hinted source).  That is why attempt 3 wrote the body out as a macro (15%: no
  return after it), and 15% x 249 = 37 is where the tie with c0 came from.
- `if (!bad) return getIniU32(name, def); log; return def;` (op30's form `b`; `d` and `e`
  are the result-variable and `def =` spellings with the good arm first): the return block
  now follows the log block, so the early return is predicted on the *good* edge: DS(15%,
  39%) = 10.1%, GU = 25 (cfldv's 53).  The standalone optIniInt is byte-identical in all
  three forms.
- Results (optlib, plain -O3; op30.py): `intb` on the hinted source IDENTICAL (the macro was
  never needed); `dzall+intb` 44 (parseButtonX's hints without the dummies); `natx+intb` and
  **`nat+intb`: every section and relocation of the object equal to the reference's**.
  Only the split part's symbol name differs (`_parseButton.part.1`, gcc's own split, for
  `_parseButtonPart.constprop.N`), and build.sh links with -s.  `nat+intb+pbfoldi` (the
  part's body back in parseButton's else-if chain) is the same object.  `nat+ifnb` (form b
  with the macro kept: GU 37) 359, `nat+intc` (bad arm first: GU 54) 732.
- a30_src's round 4 (op30tr.py a30_base a30_src -r 4): 150 (macid chars warning), 198, 188,
  244 (dualboot), 73 (cfldv getIniU32, 53), 203, the six 38s, **c0 29 alone**, the eleven
  25s, the 19s, nodvd 11, noecdremap 10, then the getIniBool blocks.  Every tie group comes
  out in the reference's order with no dummy: the 38s, the 25s (gputemp, cputemp,
  gameregion, avregion, overedramtemp, overgputemp, gpufan, cpufan, overcputemp, edramtemp,
  dvdregion), the 19s (cygnos, demon, dualboot's remopower, smcnoblink, patchsmc,
  smcnoeject).

### One optIniBool: optIniBoolG goes too

- op30site.py (the 32 subsets of the five optIniBoolG sites flipped to OPT, on
  nat+intb+pbfoldi): 9 are the same object, among them nandmu + nosecurity + cygnos +
  smcnoeject all through OPT.  Only noecdremap needed the copy: its getIniBool block is 69 x
  15% = 10 and must pop after nodvd's iniBoolInvalid block (11); with optIniBool's old
  warning arm (`return 0`: early return, 21.6%) it is 15 (`allopt` 172).
- So one helper with the copy's body, the warning arm setting `on = 0` like every other
  arm, at every site (OPT and olddvd's direct call): **same object**.  The getIniBool blocks
  are then 6 at the top level and 3 in the JTAG block (were 8/6 and 4/3 to force the order
  by key), and the natural heap gives the reference's order of both ties (6s: noremap,
  nosusecurity, nomobile, smcnocheck, olddvd, nosecurity, nandmu; 3s: demon, patchsmc,
  smcnoblink, smcnoeject, cygnos).  The standalone optIniBool is byte-identical too.

### What is load-bearing in the landed source (op30chk.py, one edit each)

| Edit on today's src | Result |
|---|---|
| optIniInt with the warning arm returning first (the old function) | applyIniOptions 736 |
| optIniInt with a result variable, bad arm first | 736 |
| optIniInt with a result variable or `def =`, good arm first | same object |
| optIniBool's warning arm `return 0` (the old optIniBool at every site) | 172 |
| optIniBool with early returns throughout (the Linux build's shape) | 1136, and optIniBool itself 12 |
| int options with the field as the default (`optIniInt("cpufan", xb.cpuFan)`, Linux's) | same object |
| olddvd through OPT (guard on a zero mask) | same object |
| rev as `if ((s = getIniValue("rev")))` | same object |

So two things carry the cold layout, both of the same kind: which arm of a helper reaches
its return first (optIniInt: the good one, 10.1%; optIniBool: none, 15%).  gcc 6 has three
values for one `if (bad)` around a call: 21.6% (warning arm returns), 15% (no arm returns)
and 10.1% (good arm returns), and they scale every inlined copy at once.

### Landed (src/options.c, full build SHA256 10dac648...1971c)

- optIniInt: `if (!bad) return getIniU32(name, def);` then the warning and `return def`;
  the twelve int options call it (`xb.cpuFan = optIniInt("cpufan", -1)`); the INI_INT macro
  is gone.
- parseButton: one function with the whole else-if chain; parseButtonX and parseButtonPart
  are gone; gcc splits the chain after winbutton itself (`parseButton.part`,
  .text.unlikely) and inlines the head at the three sites.
- optIniBool: the warning arm sets `on = 0`; optIniBoolG is gone and every site uses OPT.
- applyIniOptions: the macid memset and asm goto, dualboot's asm goto, the rev feeds and the
  dummies dz1/dz2 are gone.
- No `Borderline, for review:` shape was added; three went (parseButtonPart's `def`,
  the INI_INT macro, optIniBoolG).  The ones left are parseOption's and parseCmdOptions'
  (attempts 9, 19, 22), untouched.
- Checks: optlib on src: only the part's symbol name differs; `objdump -h/-s/-r` of the
  object equal to build/op/reference.o's; `sh build.sh` after each step (the trick removal,
  optIniBoolG's removal, the last comment): SHA256
  10dac648197fa5cdbb82d975ab9ff11f64075c9686908dfd9a33edc533f1971c each time;
  progress.py on a scratch copy of NOTES.md: 617 / 617 (its only change is gcc's clone number,
  `baseFileExists.part.1` -> `.part.0`).  fncmp on applyIniOptions prints the same two
  0x400000 immediates as before the attempt (it reads smcnoeject's bit as an address).
- For the session that commits: README.md's options entry (0 tricks now, and its text on
  parseButton's split part), NOTES.md's Progress section and its parseButton.part text are
  stale.  build/op/reference.o is now this build's options.o (optlib on src: IDENTICAL
  BYTES; the old one is reference_a29.o, which differs only in the part's symbol name), so
  op30.py's results above read "new fn _parseButtonPart.constprop" the other way round for
  the hinted variants.

### Don't retry (attempt 30)

- Nothing is left to remove in options.c's applyIniOptions group.  Don't bring back the
  INI_INT macro (GU 37 ties c0), a warning arm that returns in optIniBool, or an optIniInt
  whose bad arm reaches the return first.
- Replays that take a hinted dump's extraction order as the reference, or that hold counts
  fixed which our own borderline shapes produced.  The reference is the binary's layout; a
  trace that connect_traces attaches to its predecessor can be created at any time.

### Next ideas

- mode_client (48 tricks) is the last file with tricks.  Run the same audit there before
  any sweep: list every "block X must be N" in its notes, mark the ones that come from a
  hinted or borderline shape and not from the layout, build the fully natural file first
  and vary the inlined helpers' return shapes (bad arm returns / no arm returns / good arm
  returns) wholesale, scoring whole objects.
- options' remaining borderline shapes are all in parseOption (the `ok` flags, macidRest,
  `val && vlen`, the uint32_t returns).  They were found the same way as the dummies (keys
  pinned on one CFG), so the same question is open for them: which callee's return shape
  (setBoolOption, myatou32, kvSetDvdKey) or which early return in parseOption gives 13.7%
  and the 57 threshold without the flags.

### Result

MATCH: **0 tricks** (15 before).  All of parseButtonX's three `__builtin_constant_p`, the
macid memset's one and its asm goto, dualboot's asm goto, the rev feeds' four
`__builtin_constant_p` and dead sprintf, and both `__builtin_unreachable` dummies are gone,
replaced by nothing: optIniInt returns early on the good path, and the code around them is
plain.

## Review (2026-11-10): all five borderline shapes approved, no source change

The user asked for options' five borderline items (parseOption's four, parseCmdOptions'
`uint32_t`) to be reviewed and settled. BORDERLINE.md asked for one attempt from the natural
parseOption first (attempt 30's lead: the shapes were fitted one at a time, attempts 9, 19
and 22, each on the state the previous ones left). That attempt doesn't match, every
mechanism is known, so all five stay, with `(approved)` on their tags and the review's
numbers in the comments. Only comments changed; full build SHA256 10dac648...1971c.

Tools (tools/wip/dehint/): `oprv.py <variants.py> [label ..] [-v label [fn]] [-o label out]`
scores variants of src/options.c (98a0eba6's) against build/op/reference.o with optlib at
plain -O3; a label may join variants with `+`. `oprv_a.py` (each shape made plain alone),
`oprv_b.py` (the product of plain spellings of all four slots: 144 sources), `oprv_c.py`
(structural respellings), `oprv_d.py` (macid loops with run-time bounds). Line counts below
are parseOption's alone; the `applyIniOptions`/`parseCmdOptions` lines some variants add are
call offsets after parseOption's size changes.

### What only parseOption sees

`setBoolOption`, `parseButton` and `stripColons` stay calls in the reference, so their
bodies don't reach parseOption's profile; macidRest is the only inlined helper. Attempt
30's lever (vary an inlined helper's return shape) has nothing else to act on here.

### The product of plain spellings (oprv_b.py)

Slots: cputemp/gpufan flag or plain; the bool arm as today, `return 1` in the arm with `==
1`, or with a plain test; `val && vlen`, `vlen`, `vlen > 0`; macidRest, a loop to 6, or a
loop bounded by `vlen` / `len` (`vlen / 2`, `i += 2` to vlen). Only today's source matches.
Best others: `vlen` alone 62, `vlen > 0` 79, the plain bool test with `vlen > 0` 156, plain
bool test 217, plain cputemp/gpufan 231 (the same with every other slot), macid loops
237-308, `return 1` in the arm 310 and up; the all-plain source 850.

### cputemp's and gpufan's `ok` flags

Plain arms: 231 lines in every combination. Mechanism unchanged from attempt 9: with the
arm's log block going straight to the return, the early-return heuristic puts bad at 59.8%
and cputemp's test falls into bad; the reference has edramtemp's. The Linux build (v1.16,
gcc 4.9) has the same arms with no extra code, but gcc 4.9 threads such a flag away too, so
it says nothing either way. The flag is the idiom approved in net's netSendFile, console_hdd's
prepSysex and fileutil's myatou32.

### The bool arm's `ok` join

`return 1` in the arm: 310 (`== 1`), 217 (plain test, 20.7%), 787 with the with-value
message moved into the value block. Attempt 22's bound is robust: the "\n" block's count is
at most 450 x P(setBool) and its epilogue copy needs 57, so P >= 12.7%; the arm returning
adds the early-return prediction (9.2%), and every way to remove it found so far is a join a
later test decides. `ok = setBoolOption(..) == 1` as the flag (attempt 22's c2) is 15.

### macidRest

The loop written out in parseOption: to 6 (306), `i + 1` indexing (237), `val + i * 2` from
1 (308), one loop with `if (i)` (273, .rdata), and bounded by a length the profile can't see:
`vlen / 2` or `len / 2` with the length tested `== 12` (308), `i += 2` to it (246), a fresh
`int n` or `size_t n` (246-308). The `vlen / 2` loop's diff starts at the prologue (one
callee-saved register fewer), not at the exit edge: the inliner's late copy of the helper's
loop brings its own IV and register choices, so the unknown trip count isn't the helper's
only job.

### `val && vlen`

- `if (vlen)` alone is 62 lines, all of them the incomplete message's missing epilogue copy.
  Dumps (`oprvdump.sh` of today's source and of `vlen`, then `oprvfreq.py` on the
  rtl_dce dump's parseOption): with `val && vlen` VRP1 threads the val-NULL edge to the incomplete block,
  which has 117 at bb-reorder (threshold 57). With `vlen` alone the val-NULL edge still
  reaches the vlen test at the end of GIMPLE (the optimized dump: its PHI has 0 on that
  edge; the vlen = 0 copies come from DOM2/DOM3/VRP2 threads, and nothing threads the test
  after them); RTL redirects it without updating the block, which keeps its old 55.
- `vlen > 0` 79; `if (vlen) .. else ..` with one return 62.
- `if (vlen)` at the end of the value block (inside `else if (val)`, no redundant test,
  `d4`): the .text is the reference's except two literal offsets. The incomplete block then
  has one predecessor, the `if (ok)` join; the join's thread copy for ok = 0 is appended to
  the chain and merged with it, so its literal is expanded after the bad message's (0xb08
  and 0xb48 for 0xb58 and 0xb08). `vlen > 0` there 6; with c2's flag 4 again.
- `vlen && val`, and nested `if (val) { if (vlen) .. }` (the author's habit): same bytes.
- Against it: the Linux build's val-NULL path tests vlen and prints the with-value message
  with a NULL value (`xor ecx,ecx` at 40d506), so v1.16 had `vlen` alone. For it: as a guard
  on a `%s` argument the val test is ordinary C, and v1.21 may have added it.

### parseCmdOptions' `uint32_t`

`int` (prototype in options.h too): 30 lines; `int` for parseOption as well: 201. The author
returns 0/1 status as `uint32_t` throughout (parseIni, FileExists, validateString,
kvSetDvdKey, checkKeys, netConnect, netMount, suLoad, getBootloaders: each returns only 0
and 1), so this one isn't really borderline.

### Don't retry (review)

- The 144 plain combinations above, the macid loops in place, the `return 1` bool arm.
- `if (vlen)` inside the value block unless something gives the incomplete block a second
  predecessor that isn't a duplicate message (`d4` is exact apart from that).
