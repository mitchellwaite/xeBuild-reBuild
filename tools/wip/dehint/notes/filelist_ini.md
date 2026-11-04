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

## Attempt 2

Tools: `flx.py` (dead/flen generator on current src, subset search), `flx1.py` (findKey decl order),
`flx2.py` (parseIni decl order), `flx3.py` (axes in combination, random sample, `DEADP`/`AXP` env),
`flx4.py` (`diff`/`hill`/`save` of a state label `flen|dead+dead|ax=v,ax=v`), `flx5.py` (initialisers).

- Subset search on current src (768 forms, flen asm/nest/plain): no free removal. Best 4 lines at
  `asm|t+len` and `nest|i+off3+off5+t`.
- Declaration order: findKey no effect at all (120 perms x 6 test forms). parseIni: discrete changes
  but never below each state's floor.
- Initialisers (`int comma = 0`, per-loop too; 800 samples): no effect on the floor. Early ccp frees
  those names, but it isn't the free list vrp2 uses.
- **New closest state: `nest|comma+i+off3+off4+off5+t+len|e=scope,lenc=scope`: 8 lines, only `nul` test
  left and no asm**; `e` in the files loop, `len`/`noCrc` per section. Three independent ties:
  (1) bl `cmp edx,ebx/jle` vs `cmp ebx,edx/jge` (`_5 > i_1093` vs `i_89 < _460`; set at **vrp2**, where
  threading's update_ssa takes recycled names; before it both forms are `_a < _b`), (2) rawpatch
  `lea ebp,[ebx+ebp+1]`, (3) flashfs `mov ebx,-1`/`xor edi,edi` order on the threaded path (PHI order, from
  version order of old names in update_ssa).
- `nest|comma+i+off3+off4+off5+t+len|` (no scoping needed): same 8 lines; natural axes (`flx3.py`, `flx7.py` with
  tie vectors, 1500 samples, 25 axes: scopes for s e p n comma/nul len/noCrc crc, loop endings, flag heads, `left` temporary,
  `name` pointer, char local for the last byte, split ++counts, p reuse, crc forms) are either fully transparent or far worse (100+).
  Not one flips a tie alone. **They're normalised before the free list matters.**
- One extra dead test anywhere (`flx6.py`, 182 points x 9 vars) at S: floor stays 8. At `nest|i+off3+off5+t`: floor 4. At
  `asm|t+len`: floor 2 (only tie 3 left, with an `off` test in the rawpatch loop or [security] head). Strlen block anywhere (`flx8.py`): nothing.
- Tie vectors over all subsets (`flx9.py`): **no flen=nest state ever has tie 3 right.** `i` is what fixes tie 2, `comma` tie 1.
  Tie 3 right only in asm at: all, -i, and -comma-t (`-23`). So nesting is blocked by tie 3 alone.
- Tie 3's mechanism: dom3's threading makes single-arg PHIs `len_809`, `noCrc_560` in the flashfs loop; update_ssa then adds
  the join's PHIs in old-name version order. Names popped from the free list in dom3 run high-to-low here, and low-to-high in the ref
  (`flxphi.py` traces the order per pass; S turns NL at dom3, the ref stays LN).
- Tie 1 is also late: vrp2 (`_5 > i_1093` in the ref, `i_89 < _460` at S; both `_a < _b` until strlen).
- The comma test can't move to a defined variable: `flx6` at `asm|comma|` matches only with another *uninitialised* read just before
  the bl loop (`pos` or `nul` at `pos = off;`). So the point is `x_N(D) < -1` surviving to RTL, where nothing else does: an uninitialised
  read is the trick's mechanism. `end`, `i`, `off`, `size`, `len` there don't match.
- memFindChar shapes (`flxa.py`): `ret` with break or `while` compile the same when they match, others change memFindChar or are far worse.
  iniBoolInvalid pin (`flxb.py`, 120 forms: val type, off test, nest, return forms): all 4 lines or worse.
- Moved test: `asm|comma+t|` plus `if (off < -1)` before [version]'s `len =` (`flxc.py`): 4 lines, only rawpatch's `cmp ebx,eax/jge`.
  Also `asm|len|` with it: 2 lines (net zero tricks). Natural axes at comma+t, comma+len and comma+t+off3 with it (`flxf.py`, 2374
  forms): no change.
- **Arm length is an axis** (`flxj.py`): a dead test's arm with k stores frees more names at the same point. `nest|i=3` (one test, three stores)
  has tie 3 right, the first nest state that does. Free-list position is what matters, as the dumps say: `len`/`noCrc` get their numbers in
  **dom2**, from what vrp1..sra freed. Bl: S `len_810 noCrc_807`, ref `len_762 noCrc_843`; `flxph2.py` shows this per pass.
- Goto forms for the path check (`flxh.py`, `flxi.py`): identical to nest. `nestcopy` (only strncpy in the good arm) keeps all ties with all tests, but
  has the literal order wrong (6 lines, .rdata).
- Arm sizes sampled (`flxk.py`, `flxl.py` beam, `flxm.py` diff; states as `nest|comma=3,i=1,...`, all in build/filelist_ini/xk.txt). No asm in any of these.
  Closest so far: `nest|comma=1,i=1,len=3,off3=5,off4=4,off5=2` 2 lines (tie 3 only); `nest|comma=3,i=1,len=1,nul=1,off3=2,off4=2,off5=3` 4 lines (ties 1-3 right,
  [security]'s `cmp ebx,esi` wrong); `nest|len=3,off3=5,off4=1,off5=4` 4 lines, **4 tests, no uninitialised read**, only tie 1 wrong.
- **First MATCH of attempt 2:** `nest|comma=3,i=1,len=1,nul=1,off3=2,off4=2,off5=3` plus `if (off < -1) buf[0] = 1;` in flashfs (10 positions match, e.g. before `if (pos >= size)`):
  no asm, no strlen block, 8 dead tests (arms of 1-3 stores). 11 -> 10. `comma`'s uninitialised read still there. Found by `flxn.py`.
- `flxn.py` scan found the 8-test match; `flxp.py` (sampling drops and arm sizes, `START`/`KMAX` env) took it to 7.

### Attempt 2 result

**MATCH, 11 -> 9.** `drafts/filelist_ini_final.c` at plain `-O3`: object byte-identical (sha256 f27828c6...), all sections compared. Written and verified by
`flxfinal.py` (`flfinal.py` is attempt 1's and now stale: don't run it, it would overwrite the draft). `sh build.sh` not run.

- Gone: `[flashfs]`'s literal asm (path check nested, `if (len <= 1023) {...} else {err}`), the `t_` strlen block, `off5` (the one after `free(buf)`).
- Added: one `off < -1` test before flashfs's `if (pos >= size)`. So 9 parseIni tricks became 7 tests.
- Left (9): tests `comma` (3 stores, uninitialised read), `i`, `nul`, `off3` (2), `off4` (2), `len`, `x` (4 stores); `findKey`'s unreachable; `iniBoolInvalid`'s pin.
- **Arm sizes are part of the steering.** Stores in a dead arm free names; nobody would write them naturally. Count each test as one trick, but they're no less a hint for it.
- Matching states are few: 13 of about 5000 sampled, all 7-test ones with comma, i=1, len=1, nul=1, off3, off4, x>=4.

Failed: 6 tests, 2500 samples: best 2 lines (`comma=3,i=1,len=3,off3=8,off4=2,x=4`, tie 3) and 4 (`nul`, no `len`). 4 tests with no uninitialised read: `nest|len=3,off3=5,off4=1,off5=4`, 4 lines, tie 1 only; one more test anywhere
(`flxn.py`, 1746 forms) doesn't fix it. Natural axes on near states (`flxo.py`, 1926 forms): transparent, same floors.

### Next

1. More arm-size search from the match: 6 tests, moving `x` as well (its position is fixed in `flxp.py`), and moving the others. Positions and sizes together haven't been sampled.
2. `comma`: only an uninitialised variable has matched there (it lasts until RTL). Look for another way to fix tie 1, starting from the 4-test state above, which has no comma.
3. What natural code frees names between vrp1 and dom2? That is the real axis: names popped in dom2 and dom3. Early-dying forms (initialisers, temporaries) do nothing; dead tests with arms do. Natural code VRP1 removes, such as a
   redundant range check on `len` or `n`, is the place to look.
4. findKey and the pin: arm sizes untried on anything there; a plain `if (q == 0)`-style test with a store arm in place of the unreachable is worth a run. Decl order and val type do nothing (`flx1.py`, `flxb.py`).

Not worth retrying: declaration order, initialisers, scopes and temporaries alone, goto forms of the path check (same as nest).
