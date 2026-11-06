# options de-tricking

Goal: `build/op/reference.o` (copy of a matching build/obj/options.o) byte-identical with fewer
hints.  69 tricks at the start of attempt 1 (README.md's list).

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
