# Work in progress

C ports that don't match yet, kept out of `src/` so `build.sh` still uses
the generated asm (and still reproduces the SHA256).

## app/console_hdd.c

12 of 14 functions match with `re/fncmp.py`. The two that don't:

- `sendDir`: 11 differing lines, all in the epilogue layout. The original
  shares the `xor eax,eax` return-0 block between the opendir failure (`je`)
  and the mkdir failure (fallthrough), and copies the epilogue onto the
  success path. Ours copies it onto the failure paths instead, because
  bb-reorder copies onto edges of at least 10% of the entry frequency and the
  opendir failure is at 41 vs 40.5. `__builtin_expect(!netMkdir(...), 0)`
  with `--param builtin-expect-probability=85..95` gets it to 9 lines.
- `sendAvatarData`: about 47–60 lines.
  - The original's send loop is rotated (a `count > 0` guard) and indexes
    with `imul ebx,ebp,1032`. Ours gets a pointer IV from ivopts.
  - The loop's failure path reuses `netSendFile`'s result (`mov edi,eax`,
    uncprop), but the manifest failure uses `xor edi,edi`.
    `int netSendFile` makes both reuse it; `u32` makes neither.

`sendDir` calls libmingwex's `stat` (448820). That address has no `SYMBOLS`
name, because `_stat` is already the msvcrt import in `src/runtime/idata.s`.
Giving 448820 the name `_stat` relinked `filelist_ini`'s call and broke the
SHA. Sort out which symbol the C `stat()` call should bind to before
building console_hdd from C.

To resume: move it back to `src/app/`. The names it needs are already in
`re/split.py` `SYMBOLS`. Iterate with `python re/fncmp.py
src/app/console_hdd.c <name>` or `python wip/fnrep.py`, then regenerate and
`sh build.sh`.

## app/options.c

Draft of the whole object, with string literals.  The matching
functions are built from `src/app/options.c` now, a mixed object that uses
`extern` names for the strings: baseFileExists (+ its `.part.0`),
perboxExists, iniConsoleType, setConsoleType, optIniInt, stripColons,
macidSet, setBoolOption, parseRawPatch, parseRawPatches, addPatch.
setBoolOption's 4 fncmp lines are ddisasm writing 0x400000 as
`__ImageBase` (the bytes match).  parseButton matches here but stays asm in
the build (its split part at 449640 is called from asm).  When the rest
matches, move this file over `src/app/options.c` (literals back, data
from the `.s`) and drop the object from `C_FUNCS`.  Still off:

- `optIniBool` (6 lines): register choice in `(bootFlags & ~clear) | set`
  (ours `or ebx,eax`, so sched2 hoists `mov eax,1` above the store).
  Nothing calls it (applyIniOptions inlines every use), so its return type
  is free: `_Bool` (or char/short/long) stops uncprop reusing
  perboxExists' result for `return 0`; `int`/`u32` give 22 lines.
  `u32 perboxExists` also works but breaks perboxExists itself.
- `applyIniOptions` (924): the "already set" path must be the likely one.
  Guarding each call in the caller with `if (!(xb.bootFlags & bit))` (the
  call heuristic) and `switch (xb.type) { case 2: }` (no == heuristic)
  fixed most of the layout.  nodvd clears 4, not 6 (`and ~4; or 2`).
  What is left is bb-reorder (see `-fdump-rtl-bbro-details`):
  - After setting nomobile and nosecurity the original duplicates the next
    option's test (`or; test eax,next; mov [flags],eax; jne`) and falls
    into that option's out-of-line block.  connect_traces only copies a
    7-byte block when the edge into it carries >= 10% of the entry
    frequency (1815 here, so >= 181).  Ours has 68 on that edge: guard 29%
    x bootFlagsOff clear 39% x set 54%.  The type-2..5 options (cygnos...)
    are not duplicated, which fits a set path between 10% and 20%.
  - The inlined `if (perboxExists(name))` is 50/50 in ours (both arms
    call).  In the original's hot noecdremap copy perbox-false falls
    through; in the guarded ones the perbox-true trace is connected after
    it.  Writing `if (!perboxExists(name)) {ini} else {perbox}` gets
    noecdremap right and the guarded ones wrong.
  - No guards, early inlining (`--param early-inlining-insns=1000`),
    `&&`/`|` guards on both flag words, and several optIniBool shapes were
    all worse; the line count is a poor score for these (use a block-order
    listing instead).
  - optIniBool tests `if (!bad) { getIniBool... } else { warning }`, so
    the getIniBool-false block comes before the warning in block order.
    Then jump2 crossjumps the two `mov eax,[bootFlags]` reloads into one
    block (the original's shared `mov eax,[flags]; jmp next`), and each
    getIniBool test and its ini log end up in one cold block, as in the
    original.  crossjump(A,B) is only tried with A the lower-numbered
    block, and only A can be redirected when it matches completely (1
    insn < min-crossjump-insns), so the warning-first order never merges
    them.  `wip/blk.py` diff 88 -> 76 lines.  What is left is the perbox
    direction (perbox-true falls through in the original, except
    noecdremap's).
  - Also off: the xellbutton registers (ebx vs edx) and the dualboot /
    type reload (`mov edx,[type]` kept for `cmp edx,2`).
- `parseOption` (69, was 454): what fixed most of it:
  - macid loop `for (i = 0; i < 5; i++) ... xb.macid[i + 1] = myatox8(val
    + i * 2)`: the IV starts at 0 (uncprop reuses stricmp's 0, which is
    what needs ebp for vlen) and the exit test stays on i.
  - One `setBoolOption` call after `vlen = len == strlen(opt) ? 0 :
    strlen(val)`, then `if (!vlen && !val)` incomplete; gcc threads it
    into the original's three copies (len<=0, '=', no '=').
  - `switch (setBoolOption(...)) { case 1: ... }` (no `==` heuristic), so
    the len<=0 copy's done edge (20.7%) beats the macid loop exit (16.7%)
    when connect_traces picks done's predecessor.
  - `goto bad`, done/incomplete written inline.
  What is left is the first options' layout.  Ours behaves like the
  original shifted by one option (our cputemp is laid out like its gputemp)
  and the vlen=0 `jmp` block sits one slot early.  `__builtin_expect(len ==
  strlen(opt), 0)` at `--param builtin-expect-probability=85` fixes the
  shift (62 lines) but then cputemp's -1 test goes to bad.  The original
  needs success at cputemp's -1 test and bad at edramtemp's, which uniform
  probabilities can't give under my reading of bb-reorder (rounds: exec
  thresholds 285/114/28 of entry freq 570).  The "early return" predictor
  (61%) comes from tree_estimate_probability_bb: an edge into a block that
  jumps to the return block, unless that block is the return block's
  `next_bb`; ours fires on every success block, not on `bad` (it precedes
  the return block).  Tools: wip/blk.py (block order diff vs options.s), wip/bbmap.py
  (bb-reorder traces with source lines and edge probabilities).
  The u32 return/validateString prototypes stop the return value living in
  esi, but they cost parseCmdOptions 15 lines (it matched with an int
  return).
- `loadAddons` (11): the original keeps j=0 in eax across the over-limit
  warning (caller-save); ours rematerialises it.  That spill also blocks
  the head merge of `lea eax,name; mov [esp+8],eax` above the `jg`, which
  is the other half of the diff.  Moving `j = 0`, a pointer instead of an
  index, unsigned j and a do-while made no difference or worse.

Findings:
- DashLaunch (same authors) has the ini reader in C:
  https://github.com/cOzInABox/dashLaunch/blob/main/dll/iniparse.c.
  `getIniBool` is its `iniGetBool` (`"true"`,4 / `"false"`,5 / default),
  `parseIni` starts with `iniStart`'s `buf[0] == 0xff || buf[1] == 0xff`
  check, and the `j = len + 1` loop exits are the same habit as its
  `i = 16`.  Use it as a style reference for filelist_ini.
- 449640 is `parseButton.part.N` (ipa-split of a single parseButton with
  an if/else chain).  gcc puts it in `.text.unlikely`; split.py calls that
  piece `.text.startup`.  The real i386pe script merges `*(.text.*)` in
  object order, so link.ld needs `*(.text.*)` instead of
  `*(.text.startup)` when this object is built from C.
- The temperature/fan/region fields must be u32 (an int would let the
  -1 default reuse the loaded value).

## app/bootloaders.c

Draft of the whole object, with string literals. 12 of 19 functions match.
They are built from `src/app/bootloaders.c`, which has the other 7 as
top-level `__asm__` blocks (plus the strings and `.eh_frame`), so its C
uses `extern` names for the strings (`msg_*` in SYMBOLS). To move one of
the 7, replace its `__asm__` block with the C from here. The 7 that don't
match yet:

- `cbDecrypt`, `cdDecrypt`, `ceDecrypt` (1 line each): the calloc failure
  path. The original does `xor ebx,ebx` (ebx holds the return value). Ours
  relies on ebx already being 0 after `test eax,eax; mov ebx,eax; je`.
  `-fdisable-tree-uncprop1` doesn't change it, so RTL drops the set, not
  tree uncprop. A `void *` return or temp breaks the shared ebx return
  (12 lines), and so does a single `return buf` at the end (57 lines).
  Undeclared (int) calloc doesn't help either. The success branch has to
  set `*outLen` itself (`buf = 0` on the free path) to get down to 1 line.
- `cfDecrypt` (4): the original returns `checkZeros(...) != 0` as
  `mov edx,1; test eax,eax; cmovne eax,edx`. Ours is `setne; movzx`.
  Tried `!!`, `?1:0`, `if (ok) ok = 1`, a `ret` variable, u32: all setne.
- `daeVerifySig` (4): block order only. The `!pub2a4` return (`mov eax,1;
  ret` before the prologue) should come last, after the FAIL log. A
  `memset` for the zero HMAC key and `if (!ok) FAIL else good` were needed
  to get this far. `__builtin_expect` on the pub test doesn't move it.
- `verifyFcrt` (10): block order. The inlined fcrtVerifySig's "sig good"
  block should sit right after the size-error return, and the "already
  decrypted"/"no pub key" blocks at the end.
- `verifyDae` (189): ours clones daeDecrypt (`daeDecrypt.constprop`, perBox
  = 1) and peels the first DAEP header test. The original calls
  daeDecrypt normally and keeps `buf` in ecx, spilled around calls. A
  `perBox ? cpuKey : key28c` select still gets cloned.

What did match: `= {0}` on the second HMAC buffer in verifySecdata gave a
different register choice; `memset(hash, 0, 16)` matched. unscramble's
state index is `j = (j + 1) & 3` with `t = buf[i] * 251` computed first.
The signature-log ifs are `if (ok) good else FAIL` in crlVerifySig and
fcrtVerifySig.

## app/filelist_ini (draft: wip/app/filelist_ini.c, SYMBOLS/IAT diff: filelist_ini_split.diff)

Flags: `-O3 -fno-tree-loop-vectorize` (with vectorize on, PRE's eliminate drops the
`PHI <'A', validChars[j+1]>` the original has in iniPreParse's validChars loop).
- MATCH: iniFindKey (409310, 4-arg, `label` flag; getIniValue inlines it), findChar, checkFileNames.
- iniPreParse: 15 lines. Left: `;` position kept in ebx (ours reloads [28]) and the
  setne order (0xff vs '\n') in the comment count loop.
- getters use their own 2-arg helper `findKey(buf, key)` with global iniSize and `p = &buf[i]`;
  getIniBool must return `long` (int def). 10/30/8/8 lines: LRA reload ebx/ecx tie.
- matchFileNames 23 (dir ptr in ebp), loadUserIni 30 (keep `iniSize + 1` in a local).
- stat at 448820 needs SYMBOLS `_stat` + IAT_NAMES `'_stat': '__imp___stat'`.
- validChars is read with [0] folded to 'A', so the object needs C data (bootloaders-style one .c).
- parseIni (409430-40aa10) not started.

## app/keys.c

Draft of the whole object, with string literals. 40 of 48 functions are
built from `src/app/keys.c` (mixed), which `python wip/keysmixed.py <names>`
makes from this file; add a function's name there (and its address to
`split.py` `C_FUNCS`, its strings to `SYMBOLS`) when it matches. Line counts
below are `FNCMP_LITERALS=1 python re/fncmp.py wip/app/keys.c <name>` (the
variable makes the draft's literals compare equal to the `.s`'s named
strings). setFuseLdv matched by declaring `u32 i;` before `u64 cb, cf;`
(that stops the `xor edi,edi` for `i = 0` moving above `test al,al`); its
print loop is `for (i = 0; i < 16; i++) ... fuse[56 + i]`, which compiles
the same but costs more in the inliner (now over max-inline-insns-auto),
so setFuseCpuKey calls it as the original does. Still off:

- `setFuseCpuKey` (16): only the cpuKey write-back is missing (the original
  stores the 16 key bytes it loaded back to cpuKey after the fuse copies;
  `*(q16 *)cpuKey = *(q16 *)(fuse + 32)` is in the draft). The copies are
  fuse lines 3..6 (24/32/40/48 = key lo, lo, hi, hi). Ours: postreload's
  cselib deletes the store as storing what is already there, and sched2
  hoists the key loads above the fuse+24 store; both mean gcc thinks the
  `fuse` stores can't alias cpuKey (q8 vs q16 TBAA, MEM_REF offsets). The
  original has them aliasing (loads after the fuse+24 store, store kept) but
  still loads all 16 bytes before the fuse+32/40 stores. Tried: memcpy/u64/
  u32/struct forms for each copy (build/keys/sk3.t), `extern u8 cpuKey[]`
  (aliases, but then the 16-byte copy goes word by word), larger cpuKey.
- `smcChecksum` (29) and `smcPrepare` (24, which inlines it): the loop is
  right except `cmp ebp,[end]` operand order; after it the original moves
  both sums into registers (sum2 in esi:edi across the first setBeU64 call,
  `xor`s on the `count == 0` path), ours keeps sum2 in its stack slot. IRA
  has a loop region in both; `-fira-region`/`-fira-algorithm` don't help.
- `fcrtEncrypt` (13): the "invalid offset" log should be the last block with
  its own epilogue; ours puts it before the shared epilogue. All four exits
  having their own epilogue means bb-reorder copied the epilogue into each,
  which needs each exit edge at >= 10% of the entry frequency
  (DUPLICATION_THRESHOLD); ours: `size != 0x4000` is predicted 72% taken
  (opcode heuristic; the call heuristic is on both sides and cancels), so
  the main path has 28% and the three exits can't all reach 10%. Declaring
  getBeU32 pure brings it to 51% but isn't the original. Nested if/else,
  inverted conditions, a static hash-check helper (changes the frame) and
  `__builtin_expect` on either test don't give it.
- `kvPrepare` (437): ours tail-merges the inlined kvEncrypt and kvEncryptAlt
  copies (one HMAC/RC4 sequence with the salt selected); the original keeps
  both (their registers differ), and its size error is the fallthrough of
  `cmp size,0x4000`.
- `daeEncrypt` (443): `if (size) do { ... } while (off < size)` with
  `buf[off + k]` header tests stops gcc peeling the first iteration and gets
  the original's 108-byte frame; still off: the processing block (call
  daeEncryptOne, `n++`) comes before the loop head in ours, and the
  original keeps buf/size/orig in edi/ebp/esi and `len` in memory.
- `cfPatchSlots` (37) and `cfEncrypt` (94, inlines it): `SWAP16` is
  `((x & 0xff) << 8) + ((x & 0xff00) >> 8)` (not a rotate in the loop or the
  last slot, a rotate for `tbl[0]`), and one `tbl[0] = SWAP16(n)` after the
  `if (end > max)` (the zero case shares it). Left: `cmp edx,edi` operand
  order in the loop (the same flip as smcChecksum) and register choice in
  the tail. cfEncrypt's inlined copy also tests `over == 0`, which the
  standalone one doesn't; `buf[539] = (type == 2)` is an if/else there.

## app/mode_update.c

Draft of the whole object, with string literals. 11 of 14 functions are
built from `src/app/mode_update.c` (mixed), which `python wip/mumixed.py
<names>` makes from this file (strings become `mu_<address>` externs, the
statics become externs for the `.s`'s `.bss`); a new match needs its name
there, its address in `split.py` `C_FUNCS` and the printed strings in
`SYMBOLS`. The object builds with `--param align-threshold=200`
(getBadBlocks' error block). Line counts are `FNCMP_LITERALS=1 python
re/fncmp.py wip/app/mode_update.c <name>`.

Matching notes: uncprop return reuse is steered by prototype types
(getSecurityFiles and verifyExtended `u32`, unscramble `int`; netMount and
the inlined helpers `u32` so getConsoleFiles' `int` returns `xor eax,eax`).
wantFile is a `ret` flag with the log after the tests (that puts the
second and third stricmp out of line). parseAddonIdx needs `u32 ok` and a
plain match loop (no `if (n)`). updateGetFile reads `updating` into a local
first: with the extern `updating` of the mixed build that keeps the load
before the stores; with a `static updating` the local gives 8 lines and the
plain read matches (so the original may have had it non-static).

Still off:

- `getConsoleFiles` (6): the bad-blocks failure (`call getBadBlocks` out
  of line) should fall into the shared `xor eax,eax; ret`, and the mount
  failure get its own epilogue; ours has it the other way round. Every
  early-return/nested combination of the five checks and the
  int/u32 return-type combinations give 6 or worse.
- `getSecurityFiles` (12): the smc BLDR path should end with a copy of the
  `size > 0x2fff` test (bb-reorder duplication into the success trace, as
  the kv path already does). That needs the test-to-success edge at >= 10%
  of the entry frequency; ours is about 7% (kv size test 39%, verify 50%,
  smc size 39%). Early-return vs nested forms of the four checks don't
  get there.
- `mode_update` (722): everything after the argument loop is cold in ours
  (the loop is predicted ~45 iterations), so bb-reorder scatters the main
  path over round-4 traces; the original keeps connect, getConsoleFiles,
  buildImage, flash, avatar and reboot as one trace. The type suffix is an
  if/else chain (a switch gives a jump table). Moving the post-build code
  into a static helper doesn't change it.

## app/image_read.c

Draft of the whole object, with string literals. 17 of 33 functions are
built from `src/app/image_read.c` (mixed), which `python wip/irmixed.py
<names>` makes from this file; a new match needs its name there and its
address in `split.py` `C_FUNCS` (all of image_read's strings are in
`SYMBOLS` as `ir_<address>`). Compare with the strings as those names, not
with `FNCMP_LITERALS=1`: two cold blocks that differ only in their string
look the same to the literal mode (getImageMobiles "matched" that way with
its two allocation-failure blocks swapped). `wip/irlit.py`'s `externize()`
turns the draft into that form.

The statics that a C function writes (fsBuf, fsValid, fsOffset, anchor,
mobiles) stay `static` in the mixed file and `re/splice.py` drops their
`.lcomm`, so the alias analysis is the original's (as externs, memcpy
clobbers fsOffset and loadFlashFile reloads it). dumpSize is only written
by the .s's code, so it stays extern (as a static gcc would think it is
always 0).

Matching notes: findFsRoot's list loop is not unrolled only as `if
(found) { if (i) mobile else fsroot }` (with `if (i == 0)` first cunroll
sees a constant conditional and unrolls it; `--param
max-completely-peeled-insns=150` also works). LBAs are `b[513] + (b[514] &
0xf) * 256` (`<< 8` folds into `(x << 8) & 0xf00`). addRemap needs `u32 b =
block;` (unused) so block's SSA name comes before the loads and the compare
is `cmp esi,[mem]`, and `numBad >= 32`. copyMuData returns `u32` (an `int`
return reuses fseek's 0). `x != x / k * k` instead of `x % k`.

Still off (fncmp lines):

- `buildCleanup` (3): the first loop's end is an immediate in the
  original, a register in ours.
- `getImageLdv` (2): the copy of the pairing's LDV byte is scheduled before
  the `cfLdv` test.
- `checkHeader` (4): `size < addr || hdr.size > addr` is evaluated in the
  other order.
- `remapBadBlocks` (6): the inlined findFreeRemap keeps its `numBad != 0`
  guard.
- `findAnchor` (11, with `u32 shaSelfCheck`): the "invalid" log for the
  second block is jump-threaded into two copies; the original keeps one and
  tests ok0 after it.
- `copyMmcImage` (11): uncprop reuses memcmp's 0 for `return 0`; every
  non-int return type merges the returns instead.
- `getImageKv` (22, nested form): the alt-KV success and the failures
  should get their own epilogues (bb-reorder needs >= 10% of the entry
  frequency on those edges).
- `listFlashFiles` (23), `fsGetFile` (70), `detectController` (61): register
  allocation (fsGetFile has fsValid and name in esi/edi swapped).
- `getImageSmc` (~100): the original has two variables for the SMC address
  (one for the checks and memcpy, one for the logs) and threads the size
  check into both address branches.
- `scanMobiles` (31): spareVersion must be called (inlined) so the version
  load compares as `cmp [mem],reg`; left: `off` placement and the older-path
  advance block being duplicated instead of the deleted path falling through.
- `showMobilePages` (115): register allocation of the page IVs and letter.
- `loadDump` (~780): in progress; numPages is stored once from a `pages`
  variable; the name buffer and spill slots differ.
- `checkBlock` (200), `parseDump` (366): block layout not worked on yet.

imgGetSecurityFiles matches only with loadFlashFile `noinline`: gcc inlines
it here (growth 39, under max-inline-insns-auto 40), the original didn't.
getNonces' magic tests are 16-bit rotates (`ROT16`).

## app/mode_client.c

Draft of the whole object, with string literals.  14 of 16 functions
match (`FNCMP_LITERALS=1 python re/fncmp.py wip/app/mode_client.c <fn>`).
12 are built from `src/app/mode_client.c`, made by `python wip/mcmixed.py
<names>` (strings -> `mc_<addr>` externs, `cinfo` extern; SYMBOLS has all
of the object's string names).  Two matching functions stay asm in the
mixed build:

- `client_usage`: its switch table is data, which a mixed object's C
  can't emit.  It matches with the real string names too.
- `clientKeys`: ipa-inline inlines one of the four `dumpKey` calls, and
  all four have the same badness.  Which one wins is a fibheap tie that
  depends on every edge in the TU: the full draft inlines the first (as
  the original), the mixed file the second.  It comes back when the whole
  object is C.

Style that matched: nested positive `if`s with the error in the `else`
(clientEraseBlock, clientReadBlocks, updatePatches), early returns only
for the first two checks in clientWriteBlocks; `same = 0; if (len == cur
&& !memcmp) same = 1; if (!same) send` in updatePatches; a `type = 0`
chain then `if (type) ... else error` in clientPatches; increments last
in patchNand's loops (`off -= 512` after the pointers).  Operand order of
a compare follows SSA versions: `start + count <= info / bs` written
without a temporary, and dumpKey's `u32 want = sum;` at entry (the
parameter's default def must be older than the sumBytes result).
clientInfo keeps `out` (NULL unless createDir worked) apart from `dir`
and copies `dir`.  `client_usage` needs `noreturn` on its prototype so
the mixed file (where it is extern) compiles getArgs the same.

`checkPatches` matched (built): `off = 0; if (type == 2) off = 16;` (gcc
then threads the copy loop and the memset on `off`; the `?:` gave a
sete/shl and no threading), `if (off) memset(buf, 0xff, off)`, and nested
positive ifs with a single `return 0` after the countInst error's `else`.
Early `return 0`s for the two findInst results matched fncmp but jumped
to the JTAG path's tail-merged `return 0`: fncmp compares every label as
`l`, so it can't see a jump going to the wrong block.  Only the full
build showed it (`.text` 0x10 longer); compare jump targets before
building: `python wip/jcmp.py wip/app/mode_client.c <fn>` diffs `objdump`
offsets and internal jump targets of a `gcc -c` object against the exe.

Still off:

- `clientBinPatch` (9 lines): `const u8 *data` (the caller's `u8 *` vs
  inlined patchNand's `const u8 *` kept them apart in out-of-SSA, so data
  was copied into a second stack slot) and the memcpy/patchNand choice as
  `switch (cinfo->nandSize) { default: patchNand; break; case 0x3000000:
  memcpy; }` (the original's layout needs a 50% branch; `==` predicts
  28%, `__builtin_expect` with `builtin-expect-probability=50` is the only
  `if` that matches) fix registers, slots and layout.  Left: after
  patchNand's 512-byte loop LRA reloads `len - 512` into edi where the
  original uses esi.  It's a tie between esi and edi broken by
  frequency-weighted register usage (`register_usage_leveling`), so some
  block frequency still differs.  Declaration order, local types,
  patchNand spellings that still match, error-first branch flips and pins
  on `file`/`off`/`count`/`start` didn't move it.  An unguarded
  `__asm__("" :: "D"(file), "S"(off))` was needed before `const data` and
  isn't now.  Forcing 50% (expect + param) on each other branch, or
  sweeping their probability, never removes it; manual inlining of the
  patch loops (instead of the patchNand call) is much worse.
- `mode_client` (about 410): only `-rb` calls getArgs; the other options
  check their arguments inline with different `||` orders and loads
  hoisted above the argc test in some (see the asm).  The `-bp`/`-wb`
  stores follow getArgs' order (`start = b` before the mode check, then
  `i += 2` and a reload of `argv[i - 1]`).  "unable to connect" is the
  last string, so its log is at the end of the source.
  - The tail has two netConnect calls but one netReboot and one
    netDisconnect: `if (mode && arg) { if (netConnect) { info; switch }
    else goto fail; } else if (reboot) { if (netConnect) info; else goto
    fail; } else usage(2); if (reboot) netReboot; netDisconnect; return
    0; fail: log` gives the original's blocks (only their layout
    differs).  One connect with `if (mode && arg)` retested after it
    computes the condition with setne/and instead.
  - Hypothesis: every option calls getArgs and all but `-rb` were
    inlined.  With all options as getArgs calls, ipa-cp clones
    getArgs.constprop for the `(mode, 1, NULL, NULL)` calls and inlines
    only 4 of 6 (unit growth), so the clone stays; `static inline`
    inlines `-rb` too.  Hand-written checks (as in the draft) are closer
    so far.  `-keys` stores mode before `arg = dummy` in the original,
    and `-i`/`-p` store the mode before `arg = dummy`.
  - fncmp's line count mostly measures block layout here; a chunk
    multiset compare (split after each jump) separated content from
    layout diffs.
  - Locals declared `reboot, ip, arg, mode` give the original's loop
    entry stores and PHI copy order (mode before `arg = dummy` in
    `-keys`/`-i`/`-p`); `a = argv[i + 1]` before the test in `-r`/`-w`
    gives the hoisted load.  Both are in the draft.
  - `-bp`/`-wb`: the original keeps the first argument in ebp (arg's
    register), ours in eax; no spelling or check order of those two
    blocks changes it.  A uniform spelling at every site doesn't give the
    original's mixed `||` orders, so the per-site orders are in the
    source.  getArgs at `-wb` alone stays a call (size 52 > the
    max-inline-insns-auto limit; einline growth 43); `inline` on getArgs
    breaks everything.
  - Tail: the `goto fail` shape above changes no chunk content and only
    layout; the switch's case order in the source doesn't matter.  After
    the loop all frequencies are 0-1 so layout is tie-broken;
    `__builtin_expect(mode && arg, 1)` gets closer (465 -> 366 lines), so
    the original's post-loop frequencies differ from ours, probably from
    something in the loop.
  - Found the loop's frequency difference: gcc's call heuristic only
    looks at the first block of each edge's destination.  With the checks
    written inline, an option's taken edge has no call (the next
    strnicmp test has one), so every option is predicted 71% taken and
    the chain decays fast.  In the original the arg-taking options' taken
    edges also had a call at profile_estimate time (50/50).  Diagnostics
    that reproduce it: a guarded `hint()` call (fileutil's rf_hint) at the
    start of `-bp`/`-wb`/... bodies, or `__builtin_expect(!strnicmp(...),
    1)` with `--param builtin-expect-probability=50` on `-bp, -wb, -eb,
    -ip, -e, -c` (greedy search's best set): 412 -> 182 lines, chunk diffs
    17/20 -> 11/11.  The hint call adds call edges that flip clientKeys'
    dumpKey tie (the hint with `optimize` on the hint itself leaves a
    `rep ret` function); the expect version keeps clientKeys.  Neither is
    in the draft yet because what's left doesn't match either:
    - `-bp`/`-wb`: IRA pops `a` (cost 848) before the `(i + 1) * 4`
      temp (564), so `a` gets edx/eax; the original has `a` in ebp (arg's
      register).  An inlined getArgs (a `static inline` copy of getArgs
      called at `-wb`) gives `a` in ebp but rotates i / i + 1 / the
      scaled index through ecx/eax/edx differently.  getArgs-shaped
      spellings by hand (shared `a`, `first`/`j`) change nothing.
    - The `||` orders differ per site in the original ((!a, ==) at -bp,
      -eb, -ip, -e, -c; (==, !a) at -wb, -r, -w), while one inlined helper
      gives the same order everywhere, so if getArgs was inlined it was
      only at some sites.
    - The tail still lays out the reboot-only path's getinfo/reboot/
      disconnect as one fall-through trace.
  - Inline limits: getArgs at `-wb` has growth 43 (> max-inline-insns-auto
    40), `-rb` 62.  Any per-file `max-inline-insns-auto` other than 40
    breaks clientKeys (dumpKey inlining), so a limit param is out.

## app/net.c

Draft of the whole object (all 32 functions, data as statics). 15 match
and are built from `src/app/net.c` (mixed): netFree, netTimerStart/End/
Elapsed, netSendStr, netSendData, netCheckOk, netOpenSocket, netClose,
netDisconnect, netGetInfo, netDumpNand, netGetBldrs, netGetBadBlocks,
netReboot. `python wip/netmixed.py <fns>` makes the src file from the
draft; test the draft with `FNCMP_LITERALS=1` (net.s's strings are named
`net_<address>`). The src file gives the strings as `static const char
net_X[] = "..."`, not externs, so gcc still folds `strlen` of a command
in an inlined netSendStr; splice.py drops gcc's .rdata copies. netRecv
stays asm and is declared `regparm(1)` (gcc's local convention for it).
The names for the unexported functions and data (`netRecv`,
`netFindBeacon`, `netSock`, `netEmpty`, `netStartTime`, ...) are in
`split.py` SYMBOLS, and the ws2_32 IAT slots are renamed to winsock2.h's
`__imp__send@16` spelling (`IAT_NAMES`; `.string` lines are skipped so
"bind"/"connect" in messages survive).

What got the last four:

- netGetBldrs/netGetBadBlocks: an integer (u32) return type. With a
  pointer type the null-return predictor (90%) makes the netRecv path
  likely; the original lays out send failure first.
- netReboot: each branch has its own `if (netSendStr(...)) OK else failed`
  (crossjumping merges the tails); an `ok` variable gives `sete`.
- netDumpNand: the send written out, `send(netSock, "GTFL\n", 5, 0) == 5`.
  Through netSendStr the send check is a 50/50 call-predictor tie (both
  arms call); inlined at profile time the opcode predictor (`==` unlikely)
  makes failure the likely path, as the original lays it out. einline
  refuses netSendStr ("growth 8 exceeds early-inlining-insns divided by
  number of calls"); `--param early-inlining-insns=30` matches netDumpNand
  too but breaks netDisconnect and netReboot, so some functions in the
  original called it and some wrote the send out.
- uncprop: netMount/netUnmount/netConnect/netSendFlash returning `int` let
  uncprop reuse netCheckOk's or netOpenSocket's 0 for `return 0`
  (`mov eax,ebx`). `u32` returns stop it (netMount/Unmount 24 -> 4 lines).

Open (diff lines from `re/fncmp.py`):

- netGetFile 5, netReadBlocks 5: `xor eax,eax` (the 0 return) is hoisted
  above `cmp; je` by ifcvt's IF-CASE-2 (ce1). It needs the 0 path under
  ~20.8% (or a predictable branch, 2%/98%) to be refused, but the original
  lays the 0 path out as the likely one, and `-fno-if-conversion` matches.
  In find_if_case_1 (0 block as THEN) the cost scales by the *other* edge,
  so a fallthrough 0 block at 79-90% would be refused and keep this
  layout; expand always puts the netRecv block first, though.
- netMount 4, netUnmount 4: `cmp ebx,netEmpty`/`mov [esp],ebx` where ours
  says eax (cprop_hardreg propagates the netRecv result into the blocks
  after `cmp len,2`; in the original that block can't have inherited it).
- netReadInfo 4: the first of the 8 swapped words uses ebx/ecx the other
  way round (reassoc operand ranks; the other seven agree). Eight explicit
  field swaps fix it but change the epilogue duplication.
- OK-reply check (netFormatSysex/Compat 6, netEraseBlock, netWriteBlocks,
  netSendFile, netMkdir, netWritePatches, netSendFlash): not netCheckOk
  (that one inlines as `sete`). netFormatSysex/Compat write it out as `ret
  = 0; if (len == 2 && getBeU16(r) == OK_REPLY) ret = 1; netFree(r); if
  (ret) return 1; return 0;`: the `if (ret)` defeats phiopt's sete. Left:
  jump2's head merge of `mov eax,1` above `je` (`-fdisable-rtl-jump2`
  stops it) and the cprop_hardreg ebx/eax as in netMount. The others still
  call netCheckOk in the draft.
- netConnect 39: as above, the original ends `mov eax,1; test; jne` with
  every failure sharing one `xor eax,eax` block.
- netRecv 56/netRecvVerbose 57: the original has a separate copy of the
  `buf != netEmpty` check on each failure path. Registers differ: size
  ebx, got edi, buf esi. `-fno-tree-dominator-opts` gets netRecv to 23.
- `-fno-tree-dominator-opts`, `-fno-if-conversion`, `-mbranch-cost=1`,
  `-O2`: none is better for the whole file.

## app/build.c

Draft of the object, started with the file loaders (14 of 41 functions so
far). 9 match and are built from `src/app/build.c` (mixed): findFileOffset,
findFileSize, findFile, readMetaFile, makeTimestamp, loadCommonFile,
loadBinFile, loadLocalFile, setFileData. `python wip/mixed.py app/build
<fns>` makes the src file from the draft (a generic netmixed.py: strings
become `bd_<address>` statics, set up per object in its `OBJS`). Test the
draft with `FNCMP_LITERALS=1`; `sh wip/all.sh wip/app/build.c <fns>` runs
fncmp over a list.

- loadFileCrc is an inlined helper: loadBaseFile, loadBaseFileMeta,
  loadCommonFile, loadInputFile, loadBinFile and loadLocalFile (twice) are
  wrappers around it, and loadCommonFile/loadBinFile/loadLocalFile match
  with it inlined. Its own out-of-line copy is 14 lines off (the
  verbose "reading %s (0x%x bytes)" block is placed after the returns), so
  the mixed C keeps its body only for inlining (`inline` in mixed.py's
  OBJS); splice.py drops gcc's copy of a function the .s still defines.
- The Win32 time calls are timeutil.c's cdecl ports, not imports: no
  windows.h, declare them as in timeutil.c.
- timestampToFileTime (16 lines, uncalled): the original computes and
  stores each argument in turn in eax; ours loads both halves first.
  Not the prototype, not TER or sched2.
- loadBaseFileMeta (21): the original falls through to `return 0` when
  meta is NULL; ours (pointer heuristic) falls into the meta block.
- loadInputFile (~360): the SUPD / nanddump / USVR / common-dir fallback
  chain; the original keeps `r != 0` as a byte (`setne dl`) and tests
  `common & failed` with `and`, and its loadCommonFile tail call is a
  separate return. Two shapes tried (early returns, `r = 0`).
- loadBaseFile is static with gcc's local convention (eax, edx); it
  is only testable once its callers are drafted.
