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

Draft of the whole object, with string literals. 39 of 48 functions are
built from `src/app/keys.c` (mixed), which `python wip/keysmixed.py <names>`
makes from this file; add a function's name there (and its address to
`split.py` `C_FUNCS`, its strings to `SYMBOLS`) when it matches. Still off
(`re/fncmp.py wip/app/keys.c <name>` line counts):

- `setFuseLdv` (11; 7 when nothing inlines it): the original keeps the
  `ldv == 0` path's `xor edi,edi` (cf = 0) apart from the loop counter's
  `i = 0`; ours shares one `xor` before `test al,al`. u8/int/u32 counters,
  `cf = 0` placement and `else`/`if` orders don't change it.
- `setFuseCpuKey` (114 here, 16 with setFuseLdv external): our gcc inlines
  setFuseLdv, the original calls it. With it external the copies need typed
  struct copies (`q8`/`q16`) to get the reloads after each store; still
  missing the write-back of cpuKey (the original stores the 16 key bytes back
  to cpuKey after the fuse copies, as if `memcpy(cpuKey, fuse + 32, 16)`
  survived; ours drops it).
- `smcChecksum` (29) and `smcPrepare` (24, which inlines it): the loop is
  right; after it the original moves both sums into registers (sum2 in
  esi:edi across the first setBeU64 call, and `xor`s them on the
  `count == 0` path), ours keeps them in their stack slots.
- `fcrtEncrypt` (13): the "invalid offset" log should be the last block with
  its own epilogue; ours puts it before the shared epilogue.
- `kvPrepare` (437): ours tail-merges the inlined kvEncrypt and kvEncryptAlt
  copies (one HMAC/RC4 sequence with the salt selected); the original keeps
  both, and its size error is the fallthrough of `cmp size,0x4000`.
- `daeEncrypt` (449): ours peels the first DAEP header test and specialises
  the first iteration (`n == 0`); the original has one loop and threads only
  the `n == 0` logging.
- `cfPatchSlots` (108) and `cfEncrypt` (234, inlines it): semantics are
  right; the original's loop runs a block counter `i` from `block` and writes
  `tbl[i - block + 1]` (strength-reduced `i << 8`), with the count from a
  `while (over > 0x4000) over -= 0x4000` final value.
