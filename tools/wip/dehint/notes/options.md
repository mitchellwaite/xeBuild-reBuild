# options de-tricking

Goal: `build/op/reference.o` (copy of a matching build/obj/options.o) byte-identical with fewer
hints.  69 tricks at the start of attempt 1 (README.md's list).

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
v1.16 build (tmp/xeBuild64) for optIniBool, parseButton, parseOption and applyIniOptions;
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
strings: function extents in tmp/xeBuild64), `op6dis.py ADDR` (one Linux function with string
immediates and guessed callee names resolved; outputs kept in tmp/strs/aio64.txt and po64.txt),
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
