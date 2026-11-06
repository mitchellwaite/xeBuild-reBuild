# options de-tricking

Goal: `build/op/reference.o` (copy of a matching build/obj/options.o) byte-identical with fewer
hints.  69 tricks at the start of attempt 1 (README.md's list).

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
