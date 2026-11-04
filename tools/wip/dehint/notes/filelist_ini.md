# filelist_ini (whole object)

Tools in `tools/wip/dehint/` (run from there). Everything takes `src/filelist_ini.c` as its base
(`FLBASE=<file>` overrides); the reference is `build/filelist_ini/reference.o`, a copy of
`build/obj/filelist_ini.o` from a matching build.

- `fllib.py`: compile as build.sh does, whole-object and per-section compare, `sweep` (about 14/s)
- `flshow.py`, `flbs.py <tag> <fn>`: listing or diff; `fldump.py`: one function's gcc dump;
  `flpass.py a.c b.c fn`: which passes differ between two sources
- `flsmall.py`: cost of each single trick removal, from src
- `flfinal.py`: **rebuilds and checks the draft** from src plus the accepted edits. Change this, not
  the draft: `edits()` for fixFileCase and iniPreParse, `PI` and `DEAD` for parseIni, `tidy()` for
  layout
- `flpi.py`: parseIni's tail as a generator; axes flash, sec, seclen, flen, raw, dead
- `flsub.py`, `flsub2.py`: all 1024 subsets of the dead tests at given shapes
- `flg1.py` (spellings), `flhill.py` (one-off natural edits, greedy), `flpe.py`, `flff.py`
  (fixFileCase), `flpp.py` (iniPreParse), `flfk1.py`-`flfk4.py` (findKey and getters)

## Attempt 1

**Result: MATCH, 22 tricks -> 11.** `drafts/filelist_ini_final.c` at plain `-O3` (no other flags) gives
a filelist_ini.o byte-identical to the reference, whole file; every section also compared. `sh build.sh`
was not run, because src/ is the parent's to change.

### What each removal needed

- **`-fno-tree-loop-vectorize`, `--param builtin-expect-probability=65`, iniPreParse's
  `__builtin_expect` and both dead tests (5 tricks): one change.** The validChars loop ends with
  `j = sizeof(validChars) + 1;` rather than `break`, the idiom memFindStr already has as `j = len + 1`.
  Its effect on the loop's shape was doing all that the five were doing. Everything else
  in iniPreParse is unchanged. Found by `flpp.py`. Other forms with all five removed: `break`, with or
  without casts, a `char c` temp and `while` are all 155 lines (46 if `-fno-tree-loop-vectorize` stays);
  a `valid` flag is 241.
- **fixFileCase's `optimize("ira-region=one")`:** `path` and `st` declared in the while body (`flff.py`,
  1920 forms). Any form with `st` or `path` in the body matches; `dir` stays at the top, the loop stays
  `while ((de = readdir(d)) != NULL)`, with the early return. Both `ge` and `continue` on stat match.
- **`[rawpatch]`'s big literal asm:** found first, else not found: `if (off != -1) {...} else log`.
  The source comment said this shape renumbers what the dead stores tune; it does, and the subset
  search then finds the two dead tests below can go as well.
- **The dead `off < -1` in the devkit arm and in the rawpatch loop:** `flsub.py` subset search with the
  above. These are the only subset that gives a match at this shape.
- **`[security]`'s literal asm, plus every goto and label in the tail:** `[flashfs]` as `if (off != -1)
  {loop} else {err}` closed *before* `[security]`; `[security]` the same; the ok tail after; the name
  check as `if (len <= 21) {...} else {err}`, like `[rawpatch]`'s own `comma <= 1023`. `noSecurity`,
  `secSearch`, `noFlashfs` and `secName` are gone. The not-found literal comes before `[security]`
  because that's where the flashfs else now sits.
- **`--param lra-inheritance-ebb-probability-cutoff=60`:** no longer does anything at this tail. Plain
  `-O3` matches. It was presumably needed for the goto form's blocks.

### Left (11)

- parseIni: `comma < -1`, `i < -1`, `nul < -1`, `off < -1` x3, `len < -1`, the `t_` strlen block (8), and
  the `[flashfs]` literal asm (1)
- `findKey`'s `__builtin_unreachable`, `iniBoolInvalid`'s `"b"(val)` pin

### Tried, with miss sizes

All at the natural tail, lines of parseIni unless stated.

- **The `[flashfs]` literal asm.** Plain `if (len > 1023) {err}`: 6, all three `.rdata` offsets (the
  "path" literal must come after "name" and "Line"), so literal order only. `if (len <= 1023) {...}
  else {err}`, which gives the right order: 574 with the dead tests as they are, but 4 with `i off2 off3
  t off5` removed, and 37 with none left. `nest2` (end test inside the good arm): 8 at best, no better.
- **All dead tests gone, flen=nest: 37.** About six independent ties: `cmp` operand order in the bl,
  rawpatch and security loops, the `lea` operand order for `pos + n + 1`, `xor edi`/`mov ebx` order at
  flashfs's `len = -1` path, and esi/edi/ebp in the `[security]` search.
- **Best with flen=nest: 4**, keeping `off1 comma nul off4 len`: `lea ebp,[ebx+ebp+1]` is spelled
  `[ebp+ebx+1]`, and `xor edi,edi`/`mov ebx,-1` swap. Removes `i`, `off3`, `t`, `off5` and the asm if
  those two ties can be found. **Closest thing to do next.**
- `flg1.py` 1568 spellings of the three `comma`/`nul` ifs and of `pos + n + 1`: no effect at all (37). They
  normalise. `flhill.py` about 30 one-off natural edits (`noCrc` type, `e` scope, `pos` in the `for`, label
  and cbb polarity, end/log order, and so on) at both baselines: nothing better than 37 and 4.
- **Why spelling doesn't help:** the compare's operand order is decided by SSA version. The ref has
  `_5 > i_474`, the dead-free form `i_448 < _606`, so `comma` needs a low recycled number. That comes from
  the free-name list, so source that frees names before the inliner runs is the axis, not spelling.
- **`findKey` unreachable: 53**, over getIniBool 10, iniBoolInvalid 27, getIniU32 8, iniU32Invalid 8.
  `flfk2.py` 2304 forms (signature, compare order, loop end, compare spelling, tail, limit local) and
  `flfk4.py` (`key[0]` in a char, int or unsigned char local: worse, 71 and up): none beats 53. `flfk3.py`
  getter shapes: they normalise, no effect (early `return` vs nesting, no val, `ret` local are worse).
  Mechanism, from dumps: a register tie (`lea ecx`/`ebx`, for `len + 1`, and the q pointer). With the
  unreachable, the SSA names at PRE are `_24 = (int) pretmp_44` and `q_38`; without, `_38` and
  `_41 = (int) pretmp_46`. The `q == 0` test lives past PRE, and changes which names are free when
  PRE makes the `(int) key[0]`. So it's a pseudo-number tie, not a shape as such. Best partial form:
  `if (buf[i + len] == 0) continue; return i + len;` with `buf[i] == key[0]`: getIniBool 6, iniU32Invalid 6,
  but getIniU32 14.
- **`iniBoolInvalid` pin: 4** (`lea ebx`/`ecx` for `len + 1`, a swap) with the unreachable kept. The 13
  shapes in `flfk3.py` give 4 (normalised) or worse. Same tie as findKey's, so try them together.
- `flash=nest` (the whole of `[security]` inside the flashfs if) also matches, but needs sec=cur with its
  gotos, so it wasn't taken.

### Next

1. Locals in the innermost block were what fixed fixFileCase, and `j = N + 1` what fixed iniPreParse. Neither
   has been tried across parseIni's sections: scoped `tmp`, `label`, per-section `comma`/`nul`/`p`, `s`
   in the flashfs block (`sscope` in flhill was tried at 37 and 4 only, without other edits).
2. The flen=nest 4-line state: find what fixes the `lea` and the `xor`/`mov` ties. `t`'s comment says vrp2's
   threading orders the noCrc PHI's copies, so look at flashfs's `noCrc`/`len` as a form without a flag, e.g.
   testing `len == comma` or `comma` itself after the if rather than `!noCrc`. That changes the PHI and
   hasn't been tried. Same for the bl and security loops.
3. Free-name axis for `comma`'s number: natural shapes *before* the first inlining that free names. Look
   at what `_5` was in the early dumps.
4. findKey and the pin together: look for something else that frees names in the same place. Note that a
   defensive `if (q && *q)` is untested, and it would still be a dead test, though plain C beating
   the unreachable counts for something.

Not worth retrying: more spellings of the `comma > nul` ifs, getter shapes, `key[0]` locals, `flen=nest2`.

### For review (not tricks, but flagged)

- `j = sizeof(validChars) + 1` in iniPreParse: same behaviour as `break` (j ends at 76, not 74), and the
  same idiom as the file's other search loops. Reads naturally.
- `[security]`'s not-found still logs "[flashfs]" (sic, it's in the original's strings).
- Pre-existing, not introduced here: `if (comma < -1)` in parseIni's bl section reads `comma` before it
  is assigned. It survives into `.optimized` as `comma_244(D) < -1`, so the comment's "VRP1 drops them"
  isn't right for this one (the RTL passes do), and it should go for that reason too.
