# options de-tricking

Goal: `build/op/reference.o` (copy of a matching build/obj/options.o) byte-identical with fewer
hints.  69 tricks at the start of attempt 1 (README.md's list).

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
