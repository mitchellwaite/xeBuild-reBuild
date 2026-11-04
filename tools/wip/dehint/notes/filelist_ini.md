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

## Attempt 3

Tools: `fl3a.py` (findKey/pin grid), `fl3b.py`, `fl3c.py` (getters on a value helper), `fl3d.py` (`first`: per-pass lifetime of a test between flpass dumps
pa and pb), `fl3e.py` (natural checks x arms x positions in findKey), `fl3f.py` (tails, and tests in place of the pin), `fl3final.py` (writes and verifies the draft; change this, not the draft).

- **findKey's unreachable: replaced by `if (buf == NULL) return -1;`** before `*q` (`fl3e.py`, 496 forms): whole-object MATCH with the pin kept. Also matches with `break` for the arm, and with `xb.iniBuf == NULL`.
  Mechanism (`fl3d.py first`): the unreachable lived until fab1, and `q == NULL` with any other arm reaches the output. `buf == NULL` lives through ch2, dom2 and PRE like the unreachable did, and dies at **vrp2**,
  because ivopts rewrites the loop's access to `MEM[base: _6, index: i]`, so vrp2 infers `_6` is non-null. **So a NULL check of a pointer whose only derefs before ivopts are `p + i` lives long and leaves no code.** That's the general lever.
  Near forms: no `q` local (`if (buf[i + len] != 0)`) 6 lines; `q < buf` 65; `q && *q` 68; `buf && *q` 45.
- **Why the pin's a separate question:** no tree pass matters, it's LRA's hard register usage levelling (`Assign` lines in `-fdump-rtl-reload`): `len + 1`'s reload r149 ties between ecx and ebx, and takes the less used one. The pin puts val's reloads (138 of freq) on ebx;
  without it they take eax (the `return val` copy) and edi. `fl3f.py pin` (306 tests x arms x positions after the findKey call): nothing beats 4 lines, since tests that die leave only frequencies and those don't reach this tie.
- **The pin too: `if (key == NULL) return -1;` in findKey's tail (instead of `buf == NULL`) plus `if (key == NULL) return NULL;` in iniU32Invalid after the off test. Whole-object MATCH, no pin, no unreachable** (`fl3l.py`, `fl3m.py`). 9 -> 9, both plain C, both dead defensive checks.
  Two classes of tail test (`fl3j.py`): (A) `buf == NULL`, `xb.iniBuf == NULL`: long-lived, iniU32Invalid right, iniBoolInvalid needs the pin. (B) `key == NULL`, `buf != xb.iniBuf`, `xb.iniSize == 0`, `len < 0`, `i < 0`: die early, iniBoolInvalid right without a pin, and only iniU32Invalid's `cmp edx,[esp+0x20]` operand order wrong.
  The getter's test fixes that. No single-test form found: with one test in the tail, 2 lines at best (`fl3l.py` two_* are all worse, 36); a test in a getter but not the tail, worse. Getter shapes for iniU32Invalid (`fl3k.py`, 10 forms) are transparent. No `q` local (`-nq`): 4 lines.
- parseIni's arms can be smaller than attempt 2's (`fl3g.py`): `comma=1,i=1,len=1,nul=1,off3=2,off4=1,x=2` matches (was 3,1,1,1,2,2,4). Spelling: `i < 0`, `len < 0` and x's `off < 0` behave as `< -1`; off3 and off4's `off < 0` don't. `off == -1` doesn't anywhere (it's removed earlier).
- **The uninitialised read is gone: `if (nbl != 6 && nbl != 9)` at comma's site** (`fl3p.py`, 192 forms; `fl3q.py arms`). nbl is a PHI of 6 and 9, and no range says it's one of those two (VRP has [6, 9]), so presumably it lives longer than the `< -1` tests, as the uninitialised one did (not checked in dumps: where it dies is worth finding). Other uninitialised reads match too (`pos`, `nul`, `n`, `noCrc`), so that isn't new; of the 32 conditions tried this is the only one on a defined value that matches. `nbl == 7`, `nbl < 6 || nbl > 9`, `nbl > 6 && nbl < 9` don't match.
  The arm must be stores (1-3 work): `return 0`, `free(buf)`, and assignments to locals don't match.
- Natural stores in place of `buf[k] = 1` (`fl3q.py site`, then in combination): `xb.nFiles = 0`, `xb.nRawPatches = 0`, `*buf = 0`, `buf[size] = 0`. Taken in the draft. They still steer: the count is what matters, not the store.
- **How a test dying at each pass acts.** Comma's PHI gets its version in dom3 (popped from the free list: 5 in the ref, 623 at the 4-test state), the nul copy in vrp2 (i_1099 against i_93), and the compare's operand order is by version (tree_swap_operands_p), so tie 1 is one position in dom3's and vrp2's pops. Probably why the long-lived tests reach it and the `< -1` ones rarely do (inferred, not proven).

### Attempt 3 result

**MATCH, 9 -> 9, all plain C now.** `drafts/filelist_ini_final.c` at plain `-O3`, written and checked by `fl3final.py`: object byte-identical, all sections compared. `sh build.sh` not run.

- Gone: `__builtin_unreachable`, the only `asm` (the pin), and the uninitialised read. No `__builtin_*` or `asm` left in the file.
- Added: `key == NULL` in findKey's tail and in iniU32Invalid; comma's test became the nbl test.
- Left (9), all dead tests: `nbl`, `i < 0`, `nul < -1`, `off < -1` x2, `len < 0`, `off < 0` in parseIni (7); `key == NULL` x2.

Failed, with miss sizes:
- Fewer parseIni tests: 2500 samples with the nbl test (`fl3q.py rand`): no match under 7. Best `len=1,nul=1,off4=1+nb=1` **4 lines, 4 tests, ties 2 and 3 wrong**; `len=3,off3=2,off4=1,x=2+nb` 6, tie 1 and 3; subsets at lean arms (`fl3q.py sub`, 63 forms): `-len` 6 lines, `-i+off3+x` 4.
- One extra natural test anywhere (`fl3n.py`, 31 sites x 10 conds x 9 arms including log/free/return) from `len=3,off3=2,off4=1,x=2` (tie 1 only, 4 lines): nothing fixes tie 1. Only `len < -1` with `pos = size` or `i = 0` at rawpatch's comma check flips it, losing tie 3, 8 lines (`fl3o.py`, 1500 arm samples around it: floor stays 8). From `len=1,nul=1,off4=1+nb` (`fl3n.py <lab> 1`): floor 4.
- Bl section tests (`fl3h.py`, 1080 forms) with `blOrder == NULL`: emitted, 600+ (the load differs after calls, ivopts doesn't get a base). `free(buf); return 0` arms at comma's site: 1000+.
- One test in findKey for both jobs: none. `buf == NULL` alone keeps the pin; `key == NULL` alone leaves 2 lines in iniU32Invalid.

### Next

1. `len=1,nul=1,off4=1+nb=1`: 4 tests, ties 2 and 3 (2 lines each). Fix those two for 7 -> 4 tests. `i` fixes tie 2 in earlier tables. Look at what they need in dom3 from `flxph2.py`.
2. A second kind of long-lived natural test. `nbl` (a PHI of constants) and pointer NULL checks based on ivopts' `MEM[base:]` are the two found. Other PHIs of constants: `noCrc` after its if (`noCrc != 0 && noCrc != 1`).
3. A single test in findKey (`fl3e.py` conds with both class properties).

Not worth retrying: getter or iniU32Invalid shapes (normalised), any test in iniBoolInvalid for the pin's own tie, `blOrder == NULL`.

### For review (not tricks, but flagged)

All nine remaining tests are dead and steer gcc, and though plain C they read as defensive checks: `if (key == NULL)` after key's been read, in findKey and iniU32Invalid; `if (nbl != 6 && nbl != 9) xb.nFiles = 0`; `if (i < 0) xb.nRawPatches = 0`. The stores in their arms are chosen by count.

## Attempt 4

Tools: `fl4lib.py` (generator on current src: `gen(tests, secs)`, `st('nb,len')`, `nscore` = diff lines with branch targets blanked), `fl4a.py` (sections as static functions called once), `fl4b.py` (dead tests at the files helper), `fl4c.py`, `fl4d.py` (helper forms and small natural helpers), `fl4show.py`.

- **Big finding: the files loop as `static void setupFiles(void)` called once: no dead test in parseIni at all, 10 lines, ties 1 and 2 right** (was 37 with no tests). Left: the files loop's own `cmp [nFiles],edi/jg` (now `cmp edi,[nFiles]/jl`), tie 3 and `cmp eax,ebx/jge` in [security]. A helper inlined at IPA gets new SSA numbers in remap order, after release_ssa, which is the free-list axis the dead tests were imitating.
- Other section helpers (bl, raw, flash, sec, cbb), all 64 subsets: 90+ lines. Whole file's targets shift, so use `nscore`, not fllib's score.
- **`setupFiles`' compare order is remap order.** Inlining remaps a body's names on first use in block order; the for loop's test block comes last, so `i` is seen before `_x = xb.nFiles` and the compare becomes `i < _x`. `for (i = 0; ; i++) { if (i >= xb.nFiles) break; ...` has the test first: `_x` gets the lower number, `_x > i`, as the ref. No dead tests: **6 lines**, two ties left, both in flashfs (`fl4f.py` is this base). (`i >= n`, `n <= i` and `return` in place of `break` are the same.)
- The two left: tie 3, and flashfs's `comma < nul` (`cmp eax,ebx/jge`). `nul`'s PHI gets its number in dom3, popped from the free list (`fl4n.py` traces a number's owners): ref `_905` above comma's `i_518`; here `_124` below `i_388`.
- From this base, 3 dead tests (`off3=2,off4=1,x=1`, `fl4k.py`): 4 lines, tie 3 right.
- **First MATCH of attempt 4: 9 -> 6.** fl4f's base (setupFiles, test first) plus `off3=2,off4=1,x=1` and one `off < -1` from `fl4r.py` (site 62, the only one of 568 that matches). 4 tests in parseIni + `key == NULL` x2. `fl4final.py` builds and checks it.
- **`if (buf[i] == key[0])` in findKey replaces iniU32Invalid's `key == NULL`: 9 -> 5.** `key[0] == buf[i]` needed that test for one compare's operand order; swapping the source does it (`fl4u.py`). (`flfk2.py`'s swap was tried with the unreachable there and no getter test, so it never showed.)

### Attempt 4 result

**MATCH, 9 -> 5.** `drafts/filelist_ini_final.c` at plain `-O3`, written and checked by `fl4final.py write` (change that, not the draft; `fl3final.py`, `flxfinal.py`, `flfinal.py` are now stale): whole object byte-identical (sha256 f27828c6...), also compiled separately against `build/obj/filelist_ini.o`, all six sections compared. `sh build.sh` not run.

- **Gone (4 net):** `nbl`, `i < 0`, `nul < -1`, `len < 0` in parseIni, and `key == NULL` in iniU32Invalid. One test added in `[rawpatch]`, so parseIni's 7 tests became 4.
- **What did it:**
  1. The files loop as `static void setupFiles(void)`, called once. IPA inlining gives it numbers after everything of parseIni's (compacted by release_ssa), so parseIni's later names change. **Before IPA, forms are normalised; after it, they aren't: that's why helpers reach what initialisers and temporaries never did.** Alone, no tests, 37 -> 10 lines. Ties 1 and 2 need no test now.
  2. `for (i = 0; ; i++) { if (i >= xb.nFiles) break;` (10 -> 6). Inlining remaps a body's names by first use in block order; test-first puts `_x` before `i`, and the compare's operands are ordered by version. So **a helper's loop form sets its compare order, and spelling doesn't.**
  3. `if (buf[i] == key[0])` in findKey: drops iniU32Invalid's test. Direct: `fl4u.py`. Attempt 3 never tried it with this tail test.
- **Left (5), all dead tests:** `off < -1` before rawpatch's `if (pos >= end)`; in flashfs `off < -1` before `if (len > 21)` (off3, 2 stores), `off < -1` after the first strrchr (off4), `off < 0` before `if (pos >= size)` (x); `key == NULL` in findKey's tail.

How the two remaining parseIni ties work (`fl4o.py <tag> <pass>`, `fl4n.py <tag> <names>` on `flpass.py` dumps):
- flashfs's `comma < nul`: dom3 pops `nul`'s PHI name from the free list. Pop list at dom3 here: 266 875 873 862 854 846 844 812 807 **124** 746 735 ...; ref: 5 866 865 863 849 798 498 786 785 **905** 782 ... Comma is `i_388`, so `nul` needs a number above 388: the slot itself holds the one low number. Either neighbour (807, 746) would do, so **one pop more or fewer before it, or `_124` elsewhere in the stack, fixes it**. `_124` was `off_124` of the bl section's memFindStr (freed at ccp2, reused by vrp1, ch2, laddress as rawPatch's `_844 * 1028`, freed by ivopts).
- Tie 3: `len_797 noCrc_796` at flashfs's join, ref `len_761 noCrc_837`: dom2 pops them across a seam in the stack, so the same sort of position.

Failed, with miss sizes (nscore, branch targets blanked):
- Sections as called-once helpers (`bl`, `raw`, `flash`, `sec`, `cbb`; `fl4a.py`, 64 subsets, `free(buf); return 0` inside): 90+. `flash` gets tie 3 right, but the frame and registers change throughout. `E`, `S`, `P`, `L` forms of the files helper (a helper per entry, for the switch, for the table lookup; `fl4c.py`): 400+. Only the whole loop works.
- Small helpers at the base (`fl4d.py`, `fl4m.py`: `iniFail`, `copyName`, `crcValue`, `fieldLen`, `sectionEnd`, `baseName`, `nameTooLong`, `dropDigit`, `setKernelStr`, `blLabel`, `setCbb`, `loadIni`, `preParse`, `setOutName`; subsets per section, 900 samples): floor 6, none fixes either tie. `iniFail`, `setOutName`, `dropDigit` and sect=s are transparent. Best moves: pre, sect=b 8 lines.
- Natural flashfs, rawpatch, bl forms (`fl4q.py`): most transparent; `strlen` 8, `nfw` 10; nothing below 6.
- Dead tests at the base: subsets and arms (`fl4b.py`, `fl4g.py`, `fl4k.py` 1500, `fl4p.py` 2200 with helpers): best 3 tests, 4 lines, then only one site of 568 fixes the last tie (`fl4r.py`). Random pairs at statement sites (`fl4s.py`, 2500): floor 6. All four tests are needed at this shape (`fl4x.py`, 256 arm sizes, subsets).
- findKey with no test: 73 with `buf[i] == key[0]` (`fl4w.py`: helper for the match, `keyAt`, `hasValue`, sized wrapper, `off` locals are all transparent, the same 73). Tail tests that match: `key == NULL`, `len < 0`, `i < 0`, `xb.iniSize == 0`, `buf != xb.iniBuf`; so the class is "dies early", with the test's own names doing the work. Test-first loop in findKey is transparent with a test, worse without.

### Next

1. The `_124` slot: shift dom3's pops by one before flashfs's `nul`, or change what's freed around ivopts, with something natural. `fl4o.py` compares stacks directly, so a candidate can be judged by its pop list rather than its diff.
2. More called-once helpers that are whole loops, like setupFiles: only that form kept the shape. Candidates: the rawpatch entry loop's body, the search of `[security]` with arguments, or the first part of `[version]`. Look at why `raw` is so far off (frame layout, `tmp` passed in?) before writing them off; `tmp` local in the helper is untried, and so is keeping `free(buf)` in the caller.
3. Test-first loops in bl, raw, flash and sec are live forms of the same kind, but not useful unless the loop is in a helper, since parseIni's own names are numbered otherwise.
4. findKey's last test: it needs a natural statement that dies early and shifts the names. No candidate yet.

### For review (not tricks, but flagged)

- `setupFiles` is natural; its `for (i = 0; ; i++) { if (i >= xb.nFiles) break;` is a little unusual, though live. It's the kind of helper that could exist in the original: findKey and `checkFileCase` already do. Its loop form is there for operand order, so it's steering, not uncounted by accident.
- The five tests still read as defensive checks but steer gcc, and their positions and store counts matter: `off < -1` can't happen, since `off != -1` and off comes from a search.

## Attempt 5

Tools: `fl5lib.py` (generator on current src: `gen(tests, kf, helpers)`, `run`, `nscore`), `fl5s.py` (diff of a helper state), `fl5a.py` (section helpers), `fl5b.py` (inlining order, memFind forms), `fl5c.py` (attempt 4's natural axes at test subsets; `FL4SRC` lets fl4lib import against commit c392b614's source), `fl5d.py` (combinations of non-transparent axes), `fl5e.py`, `fl5f.py` (out-parameter helpers), `fl5g.py` (diff of an fl5f label). Scratch and score logs in `build/filelist_ini/a5/`. Labels: `axis=value,..|tests`, tests from raw off3 off4 x (the four in parseIni).

- Whole sections, loops or entries as helpers (`fl5a.py`, 1500 states, no tests, free in or out, uint32_t, `tmp` local, test-first, `break`): best `secL:f` 39 lines, `cbb` 88 (block placement only, same ties), everything else 180+. Keeping `free(buf)` in the caller is worse than freeing in the helper (literal order and `.rdata` break). `tmp` local is worse too.
- Where setupFiles is defined, forward declarations, memFindChar and memFindStr forms (`fl5b.py`, 43 single states): transparent or far worse. Definition order does nothing.
- Attempt 4's natural axes at all 15 subsets of tests (`fl5c.py single`, 840): the only changes are numbers shifting a tie around; floor is `off3+off4+x` 4 lines (`[security]`'s `cmp ebx,esi`) and none 6 lines.
- **New lever, `fl5f.py`: a called-once helper with out-parameters for an entry's head.** `[security]`'s two searches as `findField(p, size - pos, &comma, &nul)`: no parseIni test needed for `[security]`'s compare. `hsec=cn|off4` (that helper, one dead test, `off4`): **4 lines**, the only tie `cmp ebx,eax/jge` in `[rawpatch]`'s `comma >= nul` (was `nul <= comma`). Others in the same table: `hsec=cn|` 6 lines (tie 3 and flashfs's `comma < nul`), `hbl=nl|raw` 10.
  In `hsec=cn|off4` raw's `nul` PHI gets `_365` at dom3 (needs a number above comma's `i_373`); ref has `_881` in that pop slot. dom3's stack: near `249 878 876 865 857 849 365 815 ...`, ref `129 878 870 862 840 839 881 821 ...`. (249,365) is the `[`-search's `buf + off + i` chain, (129,881) rawPatch's `_860 * 1028 + 307456`: both released by ivopts, and in near they've swapped places, with `(126,868)` (near's rawPatch chain) 18th and 19th in the stack. So which chain sits on top is what's wrong.
- Beam over everything around these states (`fl5j.py`, width 12, about 1300 distinct states): closure in 3 steps; nothing under 4 lines. Single extra dead test at every site of `hsec=cn|off4` and `hsec=cn|` (`fl5i.py`, 1100 forms each): floor stays 4.
- findKey with no test (`fl5k.py` 270, `fl5l.py` 1152 forms: scan, wrapper, compare order, `p`, loop, tail, getters plain or through `iniVal`): best 41 lines, tail `if (buf[i + len] == 0) continue; return i + len;`, getIniBool 6, iniBoolInvalid 31, getIniU32 14, iniU32Invalid 6; all reg/slot ties (`q`'s reload takes ecx, ref ebx). `iniVal` with `key[0] == buf[i]` gives the same as plain with `buf[i] == key[0]`.
- **First MATCH of attempt 5: 5 -> 4** (`fl5final.py`). `findField` for `[security]`, `preParse` (fl4m's), and three tests in flashfs: `off4` where it was, `off < -1` (2 stores) before `strncpy(xb.firmware[i], ...)`, `off < 0` (2 stores) before the crc's `tmp[8] = 0`. Found by `fl5m.py` (2 random extra tests from `hsec=cn|off4`: 2 lines, tie 3 only, 1 of 2500) then `fl5p.py` (natural axes on that state: `pre=y` or `fail=y` flip tie 3). `iniFail` matches too, but changes every error path.

### Attempt 5 result

**MATCH, 5 -> 4.** `drafts/filelist_ini_final.c` at plain `-O3`, written and checked by `fl5final.py write` (change that, not the draft; `fl4final.py` and older `*final.py` are stale, and fl4lib now needs `FL4SRC` to import, which `fl5c.py` sets): whole object byte-identical to `build/obj/filelist_ini.o` and the reference, all six sections compared. `sh build.sh` not run.

- **Gone (net 1):** `[rawpatch]`'s `off < -1`, flashfs's `off3` and `x`; one test added there at each of two new sites, so parseIni's 4 tests became 3.
- **Added, live and natural:** `static void findField(p, rem, &comma, &nul)` for `[security]`'s two searches, `static int preParse(buf, size)` for the terminators around iniPreParse. Both called once. findField's loads and stores of `*comma`, `*nul` go after IPA, so this acts where parseIni's own forms can't; **out-parameters are a stronger version of attempt 4's helper lever**. preParse is transparent elsewhere and only flips tie 3 here (`mov ebx,-1`/`xor edi,edi`).
- **Left (4), all dead tests:** in flashfs `off < -1` (2 stores) before `strncpy(xb.firmware[i], ...)`, `off < -1` (1 store) after the first strrchr, `off < 0` (2 stores) before the crc's `tmp[8] = 0`; `key == NULL` in findKey's tail.

Failed, with miss sizes (`nscore`, branch targets blanked):
- Fewer tests with findField and preParse or iniFail: `off4` plus one test anywhere (`fl5q.py 1`, 1100 forms) 4 lines; two tests without off4 (`fl5q.py 2`, 2500) 4 lines. `hsec=cn|off4` alone 4 lines (raw's compare), `off4` + 2 tests without pre/fail: 2 lines (tie 3).
- findField elsewhere: `hbl` 450, `hraw` 450, `hflash` 29 (`cn`); `nl` (return noCrc, `*len`) `hbl` 10 with `raw` or `x`, `hsec` 10; `ln`/`lv` 19+. crc block as a helper with a slot pointer (`cbl`, `cflash`, `csec=slot`): 240+. Shared `findField` for bl and sec (`shared=y`) is the same as separate. Pairs and triples of these with test subsets (`fl5f.py rand`, 4000): nothing under 4.
- Section helpers (`fl5a.py`): see above, 39+. Definition order, memFind forms (`fl5b.py`): transparent or 130+.
- findKey with no test: 41 lines at best (`fl5l.py`, 1152 forms); iniVal and scan wrappers normalise.

### Next

1. `hsec=cn|off4` is one tie off with one test: raw's `comma >= nul`. dom3's position 7 has to hold a number above comma's; which of two ivopts chains is on top decides it. Find a natural change near the `[`-search or `xb.rawPatch[i]` (a pointer to the entry, `sectionEnd` with an out-parameter) that swaps them; `fl4o.py` compares stacks directly.
2. Other out-parameter helpers around flashfs and `[rawpatch]`: only head and crc forms were tried. `n` and `pos` through pointers (`pos = readX(...)`, `&pos`) are untried, and so is a helper over `strncpy` + NUL + `pos` advance.
3. findKey: `*q` tail, or `*off` as an out-parameter from findKey (`if (!findKey(buf, key, &off))`), is untried and is the same lever. The 41-line tail's ties are all `q`'s reload register.

Not worth retrying: `free(buf)` in the caller, `tmp` local, helper definition order, memFindChar forms.

### For review (not tricks, but flagged)

- `findField` and `preParse` are live and read naturally, but both are there for numbering, not structure: findField only for `[security]`, while the other three sections keep the two calls inline, which is odd to read. `preParse` wraps three lines. By README's "a helper that exists only to change an SSA number" they could be called candidates, so you decide; they're the same kind of move as `setupFiles` and its loop form.
- The three tests' positions and store counts still matter, and `off < 0` before `tmp[8] = 0` reads badly (`off` isn't near).

## Attempt 6

Tools: `fl6lib.py` (generator on current src: `state('T1,T3|axis=v')`, drops T1 T2 T3 KF; `run`, `nscore`; pid-tagged objects, so sweeps can overlap), `fl6a.py` (natural parseIni edits, single and pair), `fl6k.py`-`fl6k7.py` (findKey). Scratch: `build/filelist_ini/a6/`.

- **findKey's tie is a frequency, not an SSA number** (attempts 1-5 had this wrong). `-fdump-tree-optimized-blocks-details`: at `key == NULL`, entry freq 293, tail 252; without, entry 418, tail 252. The names in `.optimized` are the same. LRA's register levelling picks ebx or ecx for `q`'s reload by how much entry-level code has used each, so what counts is tail/entry. `-fdump-tree-profile_estimate`: the loop exit heuristic is 9% / n_exits, and **the dead test works as a third loop exit** (3% each, not 4.5%), removed only after the profile is estimated. That's why "dies early" was the class that worked, and why `skipNul` works too.
- `if (j <= len)` (`fl6k3.py`): registers right with no test (tail 450, entry 441), but `jl` not `jne`. VRP doesn't fold it, because of the `len <= 0` path into j's PHI. **tree_predict_by_opcode gives EQ 28% except against 0, which gets none.**
- Hence **a flag or helper for the match**: `if (j == len) return 1; return 0;` in a helper `matchAt(p, key, len)`, `if (matchAt(&buf[i], key, len))` (`fl6k7.py`): threading takes the flag away after the profile. No dead test: 73 -> 6 lines, only iniU32Invalid. `return j == len` folds early and doesn't do it.
- No effect on the profile: goto and continue on mismatch paths (`fl6k5.py`), `*off`/`**val` out-parameters and a pointer return (`fl6k.py`, floor 41), iniSize check moved into findKey (`fl6k2.py`, 41), `i + j` spellings (`fl6k4.py`).
- `skipNul` parameter in memFindStr's tail form (`fl6k6.py`): 4 lines (iniBoolInvalid). A constant argument is a dead test by another name. `memFindStr(xb.iniBuf, xb.iniSize, key, 0)` directly: 282, it isn't inlined the same way.
- parseIni natural edits at `T1,T3` and `T1,T2,T3` (`sectionEnd` return/out/range, rawPatch entry pointer, `copyName`, `takeName`, `copyValue`, `fieldLen`, findField placements; `fl6a.py pair`, 1976 forms): floor stays 4 (raw's compare) and 6.
- **`key == NULL` gone, no flag or helper: a third loop exit that is live.** `char c = buf[i + len]; if (c > 0) return i + len; if (c < 0) return i + len;` (`fl6k12.py`): whole-object MATCH. Two edges leave the loop at the profile (so 3% per exit, as with the dead test), and ifcombine merges them into `c != 0` afterwards. Neither test is dead or redundant, but it's a split of one test, and it is there for the loop exit count. `*q >= 0x20` + `*q != 0` also matches and is redundant, `*q >= 0x80` + `*q != 0` is 2 lines off.
- matchAt's last 6 lines: iniU32Invalid's `movsx` of key[0] takes ecx rather than ebx. LRA's levels: ebx gets the entry-level `_5`, `_50` (scale with the preheader's freq) and q's reload (scales with the tail); it needs those under about 150, and only a third exit or a higher P(head) lowers the preheader that far. Head flag (`fl6k9.py flag100`) 155, all forms. iniU32Invalid's body (`fl6k8.py`, 80 forms), head and iniVal subsets (`fl6k11.py`, 21 forms): no change or worse. matchAt's return encodings (`fl6k10.py`, 88): 6 at best.
- Spellings of the split (`fl6final.py spell`): two ifs, `else if`, `(char)buf[i + len]` twice, `int c = (char)...` all match. `c > 0 || c < 0` is folded to `!=` by the front end: 73. `unsigned char c` with `c > 0` and `c != 0`: 73.
- Live split tests in parseIni (`fl6s.py`, 840 forms: the loop-end tests as `>` and `==`, flashfs's comma check and last-digit test, at the subsets of T1-T3): nothing below each subset's floor (4 at `T1,T3`, 6 with none). `pos >= end + 1` for the bl check is transparent. Most are worse (160+).

### Attempt 6 result

**MATCH, 4 -> 3 dead tests, with a split test in place of the fourth.** `drafts/filelist_ini_final.c` at plain `-O3`, written and checked by `fl6final.py write` (change that; `fl5final.py` is stale): object byte-identical to `build/obj/filelist_ini.o` and the reference (sha256 f27828c6...), all six sections compared. `sh build.sh` not run.

- **Gone:** findKey's `key == NULL`. **Added:** `char c = buf[i + len]; if (c > 0) ...; if (c < 0) ...`, in place of `q` and `*q != 0`.
- **Left (3), all dead tests:** flashfs's T1, T2, T3. findField and preParse stay, for numbering; nothing found removes them (`ff=none` and `pre=in` are worse at every test subset).
- **Is the split a trick?** Under the "dead or redundant" count, no: both tests are live and neither implies the other. But nobody would write it, and it's there only for the exit count, so by README's "anything else whose only job is to steer gcc" it's a candidate. Parent and user to decide. If it's rejected, the count stays at 4, and `key == NULL` is the one to keep.

Failed: all of Next items 1 and 2 from attempt 5 (`fl6a.py pair`: `sectionEnd` return/out/range, rawPatch entry pointer, name and offset locals, `copyName`, `takeName`, `copyValue`, `fieldLen`, findField placements and a nul-first findField for raw/flash, 1976 forms at `T1,T3` and `T1,T2,T3`): floors 4 and 6, the same two ties, and no form lets findField or preParse go. Only findKey moved.

### Next

1. **Check the other "numbering" ties for frequency.** findKey's was misdiagnosed as SSA numbers for five attempts; `-fdump-tree-optimized-blocks-details` and `-fdump-tree-profile_estimate` settle it in a minute. parseIni's T1-T3 might partly act by predictions too: their arms and tests change probabilities until they die. Raw's compare order and tie 3 have been traced to dom3 pops, so they probably are numbering, but this hasn't been checked by comparing frequencies at the near states.
2. A more natural form of the third exit in findKey. It has to be two edges leaving the loop at profile time that become one test afterwards. What the original had is an open question: its frequencies say three exits, so a real source shape probably exists (a helper with a constant argument like memFindStr's `skipNul` gives 4 lines, iniBoolInvalid; `fl6k6.py`). Its tail is worth more forms.
3. matchAt (no dead test, reads well) is 6 lines off: iniU32Invalid's ebx/ecx level. If something else lowers iniU32Invalid's preheader freq, it replaces the split.

Not worth retrying: goto or continue for predictions (no effect on the profile), `*off`/`**val` out-parameters from findKey, moving the iniSize check, parseIni loop-end splits.

### For review (not tricks, but flagged)

- The split: see above. Its comment says what it's for.
- Earlier notes on findKey ("pseudo-number tie", "the test's own names doing the work") were wrong: both are the frequency effect above.
- `findField` and `preParse`: still there only for numbering, as attempt 5 flagged. `findField` is still used only by `[security]`.

### Attempt 6 decision (parent session)

Not landed: the split `if (c > 0) ...; if (c < 0) ...` in findKey is live, but nobody would write it and its only job is to steer gcc, so by README.md it is a candidate, not a removal. Saved as `drafts/filelist_ini_findKey_candidate.patch` for the user to decide on. `src/` keeps `key == NULL`, still 4 tricks. `fl6final.py write` regenerates the candidate over `drafts/filelist_ini_final.c`, which now holds the same source as `src/`.

## Attempt 7

Tools: `fl7lib.py` (KF-free base split round findKey: `fk`, `run`, `diff`), `fl7a.py` (findKey control shapes), `fl7b.py` (loop test against 0), `fl7c.py` (parseIni's block and LRA frequencies per state), `fl7d.py` (natural `[flashfs]` edits at test subsets), `fl7e.py` (head and match tests with no opcode prediction), `fl7f.py` (natural guards). Score logs: `build/filelist_ini/a7/`. Lines below are `nscore`, whole object.

### Result

**NO MATCH: still 4 tricks.** Nothing natural removes `key == NULL` or a `[flashfs]` test. `drafts/filelist_ini_final.c` is untouched (same as `src/`), and there's no new candidate; attempt 6's `drafts/filelist_ini_findKey_candidate.patch` is still the only one.

### findKey's frequencies

`-fdump-tree-profile_estimate-blocks-details` on findKey, inner loop 10000:

| form | entry | header | tail | best lines |
|---|---|---|---|---|
| `key == NULL` (3 exits, src) | 114 | 3214 | 252 | match |
| no test (2 exits) | 163 | 3214 | 252 | 73 (`buf[i] == key[0]`) |
| tail `if (*q == 0) continue;` | 250 | 3214 | 252 | 41 |
| matchAt (P(match) 50%) | 172 | 3214 | 450 | 6, iniU32Invalid |

- Entry is (latch x exit share) + (tail x exit share). Header is set by P(head) 28% and the inner loop's 9%, tail by P(match) 28%. So three things move it: the number of exits, P(head), P(match).
- **The loop exit heuristic is first match, so nothing combines with it.** A loop test `x > 0` does get `opcode values positive`, but the dump marks it "(ignored)" and the combined figure stays 95.5%. `fl7b.py` (80 forms: `xb.iniSize - len - i > 0`, count-down `left`): best 41, and that is the `continue` tail again.
- `continue` has hitrate 50% in this gcc ("continue heuristics: 50.0%"), so at the head DS leaves 72%. That's why attempt 6 saw no effect. In the tail it matters only because that block loses its loop exit prediction (61%, not 4.5%), which puts entry at 250: the wrong way. `goto` shows no prediction in the dump.
- **P(head):** about 40% would give the target's entry, but `==` gets 28% and anything without an opcode prediction gets 50%. 50% through a flag or a two-return helper is too far: 155 (`fl7e.py` `flag,eq,q`, `help,eq,q`), 217 with matchAt as well. `buf[i] - key[0] == 0` and `!(a ^ b)` score the same as `==`, so they're normalised before the estimate.
- **Why matchAt stays 6 off.** In iniU32Invalid's Assign lines, key[0]'s reload goes to ebx in the ref and ecx at matchAt. The sums fit a level rule: ecx about 1600 (960 + 640), ebx 642 x 2 + 162 + x, with x = q's reload plus three entry-level reloads. Ref x = 50 + 33 + 22 + 33 = 138; matchAt x = 90 + 51 + 34 + 51 = 226; it needs about 149 or less. That rule is fitted to these numbers rather than read from LRA, and it doesn't obviously explain iniBoolInvalid's r149 below, so don't lean on the exact threshold.

**A constant argument isn't equivalent to the dead test (new).** With `skipNul` (`fl6k6.py`) findKey's estimate is identical to `key == NULL`'s (114, 3214, 252), yet iniBoolInvalid's preheader ends at 104, not 111, and its entry at 136, not 145, which goes with its 4 lines (r149 takes ebx, not ecx). 104 is what you get by taking the third exit's share out of the entry: (114 - 3% x 252) x 0.97. So, by inference from those numbers and not traced in a pass, the ipa-cp clone's folded test has its flow taken out of the frequencies, and a test dying after inlining doesn't. **If so, the third exit has to survive past IPA inlining**, which rules out anything IPA-CP can see, and it must then fold without emitting code. What folds that late is a fact already known (`key`, `len`, `i`, or `xb.iniSize` from the getter), and a test of one of those is a dead test.

Forms, all live, no dead test:
- Control shapes (`fl7a.py`, 54): `matchAt` 6; `found` tested in the loop then `break` 33 (`buf[i] == key[0]`); `off` + `break` and `goto found` 47 and 73; `break` + test of `i` after the loop, `found` after the loop 69 and 89; `keyAt` returning off or -1 88-98; `hasVal` 285; `off = i + len; i = xb.iniSize` 305; `matchAt` including the head 312; `found` in the loop head 400; `off == -1` in the loop head 419.
- Guards (`fl7f.py`, 22, plain and with matchAt): best is `key[0] == 0` return at 49 (with matchAt; the only guard under 73 and it isn't near). `len == 0` return 110 (76 with matchAt), `len < 0` return 128 (92). `len == 0` in the match arm 86 with matchAt. These emit code the target doesn't have. `if (i >= xb.iniSize - len) break;` in the arm is exactly `none` at both (73 and 6): it's gone before it can count as an exit. Bounds checks `i + len >= xb.iniSize` and `buf[i] == 0 && i + 1 >= xb.iniSize`: 185 and up.

### parseIni and the helpers: not frequency

`fl7c.py`, `.optimized` block frequencies and the freq of LRA's first assignment, src against each state:

- Dropping T3: no change at all. Dropping T1, or all three: one block 70 -> 69 and one reload 21 -> 18. Dropping T2: the same, plus one extra block and reload.
- `ff=none`, `pre=in` and both, on top of all three dropped: the same one block and reload. So **findField and preParse have no frequency effect, and attempt 5's "numbering" label stands.**
- So nothing here says frequency, unlike findKey. The ties these fix are compare and copy orders, traced in attempts 2-5 to dom2, dom3 and vrp2 pops. I didn't look at which block is the 70 -> 69 one, or whether it matters to a near state's diff.

`fl7d.py` natural `[flashfs]` edits at all 8 subsets of T1-T3 (232 forms; `crc2`'s 8 failed to compile because the edit is broken, so **`crc = 0` + a separate store is untested**). Floors unchanged: none dropped 0, `T1,T3` 4, all three 6.

- Transparent: `helse`, `hor`, `hswap`, `hne`, `ge22`, `slenge`, `sif`, `sifn`, `sinline`, `crcv`, `crcrr`, `incr`, `lastc`, `lastp`.
- Moved, all worse (lines with none dropped / all three dropped): `slen` 2/8, `lenbad` 6/8 (.rdata), `hnest` 37/29, `pospp` 40/46, `fw` 142/57, `lastsw` 111/54, `pos1st` 104/108, `flip` 198/200, `brk` 218/214, `crc8` 252/316, `crcbad` 332/326, `last` 409/398, `cfirst` 890/637.
- Pairs of `slen lenbad hnest pospp fw lastsw` at all subsets (120 forms): best `|slen+lenbad` 8, `T1,T2,T3|slen+lenbad` 10. They add up; none cancels a tie.

### Next

1. findKey: it needs an exit that lasts past inlining and then folds silently, and I found no live condition like that. Likely the end for `key == NULL`, unless the user takes the split candidate.
2. `[flashfs]`'s tests: frequency work won't help. Only the free-list axis is left (Next in attempts 4-5), and it has had many forms.
3. Small loose ends: `crc2` (fix the edit), the 70 -> 69 block. Low odds.

Not worth retrying: loop tests against 0 or count-downs for probability, `continue` or `goto` for predictions, flags or helpers for P(head), arithmetic spellings of `==`, constant arguments.

### For review

Nothing new: `src/` is unchanged. The four dead tests, findField and preParse stay, flagged in earlier attempts.

## Attempt 8

Tools: `fl8lib.py` (state labels `drops|t.var=type,axis=value`, logs in `build/filelist_ini/a8/`), `fl8a.py` (single local types x all T1-T3 subsets), `fl8b.py` (int/long combinations). Lines are `nscore`, whole object.

- parseIni's local types, one at a time at all 8 subsets of T1-T3 (`fl8a.py`, 880 forms): **no floor moves** (none 0, T1,T3 4, T1,T2,T3 6, T1,T2 10, T3 10, T1 18). `long` for size off end comma nul n i, any of `crc`'s types, `unsigned char` tmp and label: fully transparent. The rest are worse at every subset: size/end unsigned 23+ (with all dropped), nbl short 27, nbl long/unsigned 200+, noCrc unsigned 258, noCrc int 386, len long 326, pos long 499, n unsigned 614, the rest 700+.
- int/long combinations (`fl8b.py`, 2000 samples over 10 vars and noCrc's type at 4 subsets): floors unchanged.
- Helper signatures (`fl8c.py`, labels `drops|mc=..`, `ms=..`, `ptr=..`, `prot=..`, `ff=..`, `pre=..`; about 700 forms at 5 subsets): floors unchanged. **`char *buf, *p` with every `(char *)` cast gone is fully transparent (`ptr=bc`, also bc2, bc3; `buf[0]` as `(unsigned char)buf[0] == 0xff`, `== (char)0xff` or `== -1`), so the casts aren't needed**, though removing them removes no trick. memFindChar: `const unsigned char *`, `long size` transparent; `char *buf` with `unsigned char c` 6 more, `int c` 24 more, `char *`+`char` or `unsigned char`+`unsigned char` 34 more, returning `long` 700+. memFindStr: `const`, `char *str`, `long size`, `long skipNul` transparent; `char skipNul` 21 more, `char *buf` with unsigned str 32 more; `long` return far worse. Prototypes: `getFileSize` as int, myatox32/myatou32 any type transparent.
- **Conversions move single ties.** Named ties, as line positions in parseIni: A bl `comma > nul` (484), B raw `comma >= nul` (828), C flashfs `xor edi`/`mov ebx` (1263), D flashfs `comma < nul` (1270). T1,T3 has B wrong; T1,T2,T3 has C and D; T1,T2 A, C, D. `getFileSize` returning unsigned flips C alone at no drops; `preParse(..., uint32_t size)` or a `uint32_t fsize` local up to preParse flips A alone; `fread(buf, 1, size, f)` also moves (`fl8e.py single`). But (`fl8e.py rand`, 1500 combinations with fwp, crcp2, str0 at 7 subsets) floors stay: T1 8, T2 25, T3 6, T1,T2 10, T1,T3 4, T2,T3 25, all 6.
- `[flashfs]` gaps (`fl8d.py`, 39 forms at 8 subsets, 976 pairs): `crc2` in all forms (`crc = 0` + separate store, either order, `crc = myatox32` + store), `crc` re-read at the log, `if (pos < size) continue; i = 256;`, `else` for the end test, `size <= pos`, `while` with `i++`, `nameblock` (a `name` local only for the base name check), `*(xb.firmwareCrc + i)`, `uint32_t *c`, a `char c` for the last digit, `[security]`'s `*c`, a rawPatch entry pointer: all fully transparent. `char (*fw)[0x400] = &xb.firmware[i]` (`fwp`) is the one that moves things: **T1 alone 8 lines (ties A and D only)**, but 302 with no drops, 18 at T1,T3. `*(xb.firmware[i] + len) = 0` 25 at T2, T2,T3. `name` through the whole section 50+, `(xb.firmware + i)` 380+, one store at the end of the crc 280+, `break` at the end 860+, `struct fileent *e` in bl 650+. Pairs: nothing better.
- Natural second spellings and setupFiles' body (`fl8f.py`, 60 forms at 8 subsets): section heads `off >= 0` / `off != -1`: transparent or worse (`[flashfs]` `off >= 0` 64+, sec 58, raw 111, bl `off != -1` 45), `comma < 0`, reversed `||`, `pos > end - 1`, `flc_lt`: transparent. setupFiles: `e` in the loop, no `e`, `long i`, `return` for `break`, a `consoleType` local: transparent; `con` local 62+, a type local 94+, `name` 440+, `loc` pointer 680+. Floors unchanged.
- findKey and matchAt with types (`fl8g.py single`): `buf`/`p`/`key` `const` or not, `long` for i j len, the return type of matchAt, `tail=n`/`qc`: transparent, still 6 lines (iniU32Invalid). `unsigned` j or len 43+, `const unsigned char *key` or a cast in the head compare 70.
- **Author's `(x&0xFF)` masks** (tmp/dashlaunch/iniparse.c, `fl8h.py`): in memFindChar, memFindStr, findKey, getters, parseIni, iniPreParse: all fully transparent, or (`pi_l`, `fk_nnb`) a few lines worse. mask + `char *` in memFindChar 300+.
- Flag forms in the name,crc split (`fl8u.py`, 24 forms at 8 subsets: `noCrc = comma > nul`, `?:`, no flag with a repeated test or `len == comma`, a `has` flag, in bl, flashfs, security): 140+ or transparent.
- Dead tests anywhere with the conversions (`fl8s.py`, sites 208 x 2 conds x 3 arms x 5 conversions): T2 plus one test (6240 forms) floor 4; two tests with T1, T2, T3 all gone (3000 samples) floor 4. These would only have moved tests, but the conversions gave them no new way down.
- Attempt 6's helper axes (`sect ent copy adv val flen ff`) with the conversions (`fl8v.py`, 3500 samples): floors T1,T3 4, all three 6, T3 6, T1,T2 10, T1 14.

### Tie B, traced (`fl8t.py <tag> [n]`: dom3's pops with each name's pre-ivopts definition)

`flpass.py` of src (`pa`) against T1,T3 (`pb`), both in `build/filelist_ini/dump/`. At T1,T3 raw's test is `_361 <= i_369`; in src its `nul` is `_859`, above comma's number. dom3's first pops, by role:

    src:  _68  _890 _888 _877 len_869 noCrc_861 _859 len_825 noCrc_824 _576 ...
    near: _66  _878 _876 _865 len_857 noCrc_849 _361 len_815 noCrc_810 _847 ...

The first six are the bl section's threaded `-1` paths, and the seventh is raw's nul. **Only the seventh is low in near**, its neighbours on either side are both high, so one PHI more or fewer in dom3 before raw fixes B, as does any reorder of the stack there. Near's `_361` was `buf_58 + _66` (a `[`-search address); src's `_859` was `(sizetype) i_847` (raw's i), which near has three places further down. ivopts visits the loops in the same order in both (`-fdump-tree-ivopts-details`: 20, 18, 19, 4, ... at the same source lines), so the visit order isn't the cause; I didn't get to what orders the releases inside a loop. I tried to add or remove a bl PHI with `fl8u.py` and none could be had without changing bl's code.

### Attempt 8 result

**NO MATCH: still 4 tricks.** `drafts/filelist_ini_final.c` is untouched (same as `src/`). No other object or header changed: all prototype tests were done by a local redeclaration in generated sources, nothing kept.

**The direction's type and signature axes are close to exhausted.** Before IPA the source is normalised: types, casts, masks, spellings, section-head tests all give the same code or a much worse one. Floors never moved, on any axis: T1,T3 4 lines (B), T1,T2,T3 6 (C, D), KF with matchAt 6 (iniU32Invalid).

Usable findings:
- A signedness conversion before the first inlining flips a single tie (A: `preParse(.., uint32_t size)` or a `uint32_t fsize` local; C: an unsigned `getFileSize`). But these aren't the ties that are left at T1,T3 (B) or T1,T2,T3 (at T1,T2,T3 neither C nor D moved). They flip against a no-drop baseline, so it depends on the state.
- No cleanup here reduces tricks, but `char *buf, *p` with all `(char *)` casts gone, and `long` for any one of size, off, end, comma, nul, n, i, are byte-identical (combinations of `long` were only sampled with tests dropped, so recheck a combination). Free to take if wanted (parent's call; `|ptr=bc` in `fl8c.py`).

### Next

1. Tie B only: what puts `buf + _66` above `(sizetype) i_835` in ivopts' releases, given the same loop order. `-fdump-tree-ivopts-details` for `a.c`/`b.c` is in `build/filelist_ini/a8/iva.txt`, `ivb.txt`; compare the release order in the loops around raw's. If it comes down to which candidate a loop picks, that gives something to look for in the source.
2. Failing that, this file looks finished at 4 unless the user takes attempt 6's split candidate. Seven attempts plus this one give the same floors from many directions.

Not worth retrying: local types, helper signatures, prototypes, `char *` vs `unsigned char *`, `&0xFF` masks, section-head and `||` spellings, setupFiles' internals, `crc` forms, end-of-loop forms, flag forms, more conversions alone.

### For review

Nothing new landed. `src/` is unchanged; the four dead tests, findField and preParse stay, flagged in earlier attempts.
