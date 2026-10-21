# Work in progress

C ports that don't match yet, kept out of `src/` so `build.sh` still uses
the generated asm (and still reproduces the SHA256).

## app/console_hdd.c

All 14 functions match and are built from `src/app/console_hdd.c` with
`-O3 --param builtin-expect-probability=80 --param align-loop-iterations=3`
(the expect param like fileutil/keyvault; 3 aligns sendAvatarData's loop
as the original, 1 or 2 align other loops too). `sendDir` matches: both
failure paths `goto fail`, and `fail:` sits after `return 1` with a
`__builtin_prefetch(0)` (no code on i686) that keeps it a GIMPLE block, so
jump2 cross-jumps the xor and bbro copies it for the send failure.

`sendAvatarData` needed:
  - `int netSendFile` with `long ret` and a `long` return: uncprop only
    reuses a call result for a PHI's 0 when the types are compatible, so
    the loop failure (which assigns ret) gets `mov edi,eax` and the
    manifest failure keeps `xor edi,edi`.
  - The loop indexes with `k = (u32)__builtin_assume_aligned((void *)i, 1)`.
    scev can't see through it, so ivopts keeps `imul ebx,ebp,1032` instead
    of a pointer IV, and it expands to nothing (an empty asm pin needs a
    reg copy; with `int k` PRE's value numbers of the cast chain change
    the SSA name reuse and flip an inlined freeManifest compare).
  - An explicit `if (count > 0) do ... while` guard, and
    `__asm__("" :: "r"(i))` after the loop: with i live there, RTL
    if-conversion (ce1) can't speculate `i = 0` above the guard.
  - `__builtin_expect` on the loop failure, and on netMount in prepSysex
    (cold mount failure, so bbro orders the cold blocks as the original;
    prepSysex itself is unchanged at p <= 80). The manifest send is an
    if/else so the success path falls into `out` and jump2 cross-jumps the
    createSysexDirs failure's `mov edi,1` with it.
  - `__asm__("" :: "i"("sending manifest to %s\n"))` before the loop:
    gcc numbers and emits string literals in expand order, and the
    original has the manifest literal before the loop's (fncmp doesn't
    see .rdata order).

`wip/fnrep.py` plus small generators (variants joined by `=====`) found
these; `-fdump-rtl-bbro-details` traces and `-fdump-tree-pre-details`
explain the block order and SSA numbering.

`sendDir` calls libmingwex's `stat` (448820). msvcrt's `_stat` IAT slot
had that name, so `re/split.py` renames the slot to `__imp___stat`
(`IAT_NAMES`, like `_stricmp`) and 448820 is `_stat`.

## app/options.c

Draft of the whole object, with string literals.  The matching
functions are built from `src/app/options.c` now, a mixed object that uses
`extern` names for the strings: baseFileExists (+ its `.part.0`),
perboxExists, iniConsoleType, setConsoleType, optIniInt, stripColons,
macidSet, setBoolOption, optIniBool, parseButton (+ its `.part.0`), parseCmdOptions, parseRawPatch,
parseRawPatches, addPatch, loadAddons.
setBoolOption's 4 fncmp lines are ddisasm writing 0x400000 as
`__ImageBase` (the bytes match).  When the rest
matches, move this file over `src/app/options.c` (literals back, data
from the `.s`) and drop the object from `C_FUNCS`.  Still off:

- `optIniBool` builds from src now: an empty asm pins the OR result to
  eax (`"+a"`), so sched2 can't hoist `mov eax,1` above the store.  The
  return type stays `_Bool` (uncprop would reuse perboxExists' result for
  `return 0` with int).  The pin doesn't change applyIniOptions, which
  inlines every use.
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
  - 2026-10-20, checked against gcc 6.2's bb-reorder.c (fetch it from
    gcc-mirror `releases/gcc-6.2.0`).  The perbox test is exactly 50/50
    (call heuristic on both arms).  When the edges are hot enough to stay
    in a trace (round 3: edge freq >= 5% of entry), better_edge_p picks
    the next_bb arm.  When they are colder, connect_traces picks the higher
    probability and, on a tie, the strictly longer successor trace.
    perbox-false's trace is 3 blocks (ini test, warning, the eax reload
    that jump2 crossjumps *before* bbro; no crossjump runs after it), and
    perbox-true's is 2 (log, OR).  So our cold nomobile group goes false;
    smcnocheck/cygnos/... tie 2-2 and keep the first edge (true).
  - So in the original nomobile's perbox test must be in-trace (freq >=
    ~180 of 1815) with true as next_bb, and the dup after nomobile and
    nosecurity needs the OR edge >= 181 (perbox test >= ~335).  noecdremap's
    must be cold (< 180, connect picks the longer false trace) or in-trace
    with false as next_bb.  Its bootFlagsOff test must not favour clear
    (the hot trace ends there; connect needs skip >= clear).
  - With the inlined copies sharing optIniBool's own profile (IPA inline,
    our current shape), nomobile's guard must be < 50% clear (hot path
    skips) and noecdremap's >= 50% (hot path continues), and the inner
    probabilities are equal, so nomobile's perbox frequency is always below
    noecdremap's.  The constraints need the reverse, so the copies'
    probabilities must differ per call site: the original's copies were
    estimated in the caller's context (early-inlined, a macro, or written
    out per option).  The Linux gcc 4.9 build has the same noecdremap vs
    nomobile split, which also points at source structure.
  - Probe: `__attribute__((always_inline))` on optIniBool (no `inline`
    keyword, so the out-of-line copy is still emitted and still matches),
    `optimize("no-early-inlining")` on applyIniOptions so a guarded
    `po_hint(&dead)` call survives to profile_estimate (keeps the guards at
    29% clear), and for noecdremap `if (!(bootFlags & 0x80000000)) { if
    (__builtin_expect(!(bootFlagsOff & 0x80000000), 0)) optIniBool(...) }`.
    The whole hot path then matches, and so do all the perbox directions
    except olddvd.  The cold trace order is further off (blk.py 87 lines),
    and there is still no dup.  In caller context the sign tests pick up
    the opcode heuristic (73%), which is why noecdremap needs the expect.
  - 2026-10-20, mixed source forms (`wip/aiosearch.py`, best config in
    `wip/aiosearch.json`; blk.py 76 -> 67).  No single form fits every
    option.  noecdremap (and olddvd's in-trace copy) want the out-of-line
    profile: guard + `optIniBool` call, IPA-inlined, whose bootFlagsOff
    test is 39% clear.  That puts its perbox block in round 2 with
    priority (right after the -1 chain), and with `if (!perboxExists)` the
    in-trace tie goes to next_bb = the ini path.  Caller context can't
    give that: the sign test's opcode heuristic (73%) DS-combined with
    PRED_CALL gives 52.5%, and expect gives 17%; it needs 27..50%.  The
    other options want the body in caller context (OPTK): expect on the
    bootFlags test (17% clear, so their cold blocks are round 3 and come
    after cygnos/macid), expect clear on bootFlagsOff, and expect true on
    perbox.  Then the OR edge clears the 10% copy threshold, the dups
    after nomobile/nosecurity appear, and the whole nomobile...smcnoeject
    group matches.  Left: olddvd's perbox direction (its join block is
    taken by whichever arm's trace is built first, an exact heap tie) and
    the round-4 cold-block order (ties in gcc's fibonacci heap, which any
    probability change reshuffles).  Also still off: the xellbutton
    registers and the type reload (see above).  bb-reorder rules worth
    knowing: better_edge_p prefers the *lower-frequency* destination
    when probabilities are within 10%; connect_traces' dup needs both the
    edge into the copied block and that block's edge to the next trace
    start >= 10% of the entry frequency.
- `parseOption` builds from src (was 69 lines here).  The key was the
  Linux build: it tests `val == NULL` after setBoolOption and jumps to the
  unknown/incomplete tail, so the value options sit inside `if (val) {...}`
  (gcc 6 threads the test away).  That alone fixed the gputemp/edramtemp
  layout.  The rest are hints (see the comment in src): `po_hint()` calls
  on cputemp's and gpufan's bad edges (PRED_CALL; gpufan's only moves a
  `.p2align` from avregion's test to gameregion's, which tiny rounded
  frequencies decide), and `__builtin_expect` on the setBoolOption `== 1`
  and `vlen` tests with builtin-expect-probability=83 (82 and 84 differ:
  the done edge must stay below gputemp's match edge but above the macid
  loop exit, and the incomplete block must reach the epilogue-copy
  threshold of 57).  The int/u32 clash is solved with an `int
  parseOptionInt(char *) __asm__("_parseOption")` declaration for
  parseCmdOptions.  fncmp ignores padding; compare raw offsets when the
  object size is off.  wip/app/options.c keeps the pre-hint draft.
- `loadAddons` builds from src: addPatch declares `path` inside the
  `numPatches <= 15` block.  With it at function scope, the inlined
  `path ={v} {CLOBBER}` joins the over-limit and strcpy paths before the
  latch, so their `j = 0` sits in a multi-pred block; without the join it
  stays in the over-limit path's extended block and cse drops it (j is
  still the 0 set before `cmp edx,4`).

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

Draft of the whole object, with string literals. All 19 functions match
and are built from `src/app/bootloaders.c`, which keeps the strings,
`.eh_frame` and padding as top-level `__asm__`, so its C uses `extern`
names for the strings (`msg_*`, labels in its .rdata asm).

- `ceDecrypt`: cbDecrypt's fix (below) keeps the calloc-fail
  `xor ebx,ebx` but rotates the registers (IRA gives bl esi instead of
  ebp). Input-only pins `"S"(len), "D"(hmacKey)` in an `if (buf)` block
  just before the real `if (buf)` (jump threading removes it) restore them.
- `daeVerifySig`: block order. ifcombine merges `!pub2a4 || size < 288`
  and the pair keeps the size test's probability (61%); expand gives the
  first jump half of it, and the shrink-wrapped `!pub2a4` return (freq
  ~P*P/2) came out above the FAIL block. A guarded `hint(&dead)` call on
  the size path (PRED_CALL; the function has
  `optimize("no-early-inlining")`) brings P to 39%. The hint stores to a
  dead local, not a static: with `-fno-toplevel-reorder` a write-only
  static stays in .bss.

How the others matched:

- cb/cdDecrypt: three passes each prove `buf == 0` on the calloc-fail path
  and drop the original's `ret = 0`: tree uncprop (turns the 0 into
  `buf`), CSE1 (jump equivalence, then a no-op set) and postreload's
  move2add (implicit set from a fallthrough `ne` jump). The source has the
  success branch first (`if (buf) { ...; return buf; } log; return 0;`,
  so the fail block is the jump target) and
  `optimize("no-tree-dominator-opts", "no-cse-follow-jumps")`.
- cfDecrypt: `if (ok) ok = 1; return ok;` with
  `optimize("no-tree-dominator-opts", "no-tree-vrp")`; DOM/VRP otherwise
  fold ok to 0 on the false edge and phiopt makes a setne.
- verifyDae: `noclone` on daeDecrypt (no `.constprop`); the header-error
  path stays in the loop (`else { log; off = size; }`, so loop-header
  copying stops after `off < size`); `buf[off + k]` addressing; and the
  signature check is a separate `always_inline` copy (`daeSigCheck`) with
  `if (ok)` first. Inlined before profile estimation it gets an even
  ok/FAIL split; the standalone daeVerifySig needs `if (!ok)`.
- verifyFcrt: fcrtVerifySig is `inline __attribute__((always_inline))`
  with a plain prototype (external copy still emitted, same code).
- `memset(hash, 0, 16)` in verifySecdata (not `= {0}`); unscramble's
  `j = (j + 1) & 3` after `t = buf[i] * 251`; `if (ok) good else FAIL` in
  crlVerifySig and fcrtVerifySig.

## app/filelist_ini (draft: wip/app/filelist_ini.c)

Mixed since 17269c2; built from src/app/filelist_ini.c: getIniValue, memFindStr (4-arg,
`skipNul`), memFindChar, checkFileCase, loadUserIni (keep `iniSize + 1` in a local;
strings are `_fi_<addr>`), fixFileCase (`optimize("ira-region=one")`: regional IRA kept
&st in a register instead of dir; ira-region doesn't help any other function here).
- iniPreParse needs `-fno-tree-loop-vectorize` (with it on, PRE's eliminate drops the
  `PHI <'A', validChars[j+1]>` of the validChars loop), and validChars as C data ([0] is
  folded to 'A'), so it can't go into the mixed file as is. 15 lines left: the `;` position
  kept in ebx (ours reloads [28]) and the setne order in the comment-count loop (the
  peeled copy tests 0xff first, the loop body '
' first). Tried: every char/uchar/&0xFF
  spelling and both orders of the two tests (reassoc ties on SSA versions; `(char)x & 0xFF`
  on both with '
' first gives the right order but SImode compares), while/for/break
  forms, and a sweep of ~35 -f flags. None below 15.
- getters (getIniBool, iniBoolInvalid, getIniU32, iniU32Invalid): own 2-arg helper
  `findKey(buf, key)` with global iniSize and `p = &buf[i]`; getIniBool returns `long`;
  myatol must be declared `char myatol(char)`. Pins `__asm__("" :: "b"(q))` on
  `q = &buf[i + len]` in findKey plus `"b"(val)` in the getter fix both LRA ties (len+1
  in ecx, the found pointer in ebx): 2 lines each for the first three. The 2 lines: sched2
  tie, the asm is a barrier, so the reload of q and `lea edx,[eax+esi]` (i + len, CSE'd
  from q's address) both get priority 4 through it and luid puts the lea first; without
  the asm, the load's latency to the cmp wins. Tried: output-operand pins (break IVopts),
  pins on the return path, `q - buf`, `i + j`, sched heuristic flags. iniU32Invalid: 12,
  the key[0]/`j == len` operand orders differ (cmp edx,eax).
- DashLaunch (tmp/dashlaunch/iniparse.c, same as GitHub main) doesn't carry over:
  iniFindLabelOffset is case-insensitive (myatol + _strnicmp) and skips spaces/'=', the
  original search does neither. iniGetBool/iniGetDword-shaped getters (`if (found) {...}`,
  `&iniData[off]` per use, the out-param helper) give 25-78 lines (iniBuf reloaded after
  each call); its `j = sizeof(validChars) + 1` exit gives iniPreParse 36, its `while`
  comment loop no change.
- parseIni (409430-40aa10, 5.6 KB) drafted in wip/app/filelist_ini.c (from a Hex-Rays
  decompile; its tables/names are still `extern`). 474 of 1241 normalized lines equal
  (fncmp with full context, FNCMP_LITERALS=1). It has a jump table (L_4501e8), so it
  can't be a mixed-file C function: it needs the whole object in C (bootloaders-style,
  strings/data as top-level asm or C). Findings:
  - Errors are `log; free(buf); return 0;` at each site (gcc crossjumps the tails), not
    a `goto fail`.
  - The original keeps the bl section's noCrc as a flag ([esp+52], which also holds the
    return value: uncprop turns the return 0 after a noCrc test into noCrc). Our dom2
    threads noCrc through the strncpy block (12 stmts, under
    max-jump-thread-duplication-stmts=15) unless that block is bigger; the hoisted
    `crc = 0` is a stand-in. dom3 threading the [flashfs] block is right (the original's
    comma-at-0 copy has the strncpy folded away). [security] has one strncpy per branch.
  - The original re-reads `xb.files[blOrder[i]]` at each use (imul [edi],1068).
  - Version search: `ira-region=one` gives the original's `[buf+j+i]` addressing and buf
    in a spill slot, but the frame slots move ([32] vs [44]) and the total drops.

## app/keys.c

Draft of the whole object, with string literals. 44 of 48 functions are
built from `src/app/keys.c` (mixed), which `python wip/keysmixed.py <names>`
makes from this file; add a function's name there (and its address to
`split.py` `C_FUNCS`, its strings to `SYMBOLS`) when it matches. Line counts
below are `FNCMP_LITERALS=1 python re/fncmp.py wip/app/keys.c <name>` (the
variable makes the draft's literals compare equal to the `.s`'s named
strings). setFuseLdv matched by declaring `u32 i;` before `u64 cb, cf;`
(that stops the `xor edi,edi` for `i = 0` moving above `test al,al`); its
print loop is `for (i = 0; i < 16; i++) ... fuse[56 + i]`, which compiles
the same but costs more in the inliner (now over max-inline-insns-auto),
so setFuseCpuKey calls it as the original does.

setFuseCpuKey matched once key1bl/cpuKey/key28c became fields of `xb`
(0x26c/0x27c/0x28c, as in main.c's struct): as separate 16-byte variables
gcc's oracle rules out `fuse + 24` reaching them (a pointer can't point
before a variable's start), so the cpuKey write-back went; inside `xb` the
fuse stores may alias it.  The copies are plain memcpys, the last one
`memcpy(xb.cpuKey, fuse + 32, 16)`.  Its NULL block is aligned:
`__builtin_expect(fuse == NULL, 0)` (40% at the object's probability)
raises its frequency over the default align-threshold.  (The object used
`--param align-threshold=200` for this before, which also aligns
smcChecksum's `count == 0` block.)

smcChecksum and smcPrepare (which inlines it) match with two hints.  The
original keeps the loop's sums in memory but the value after the loop in
registers (`xor`s on the `count == 0` path, sum2 in esi:edi across the
first call): two pseudos, where out-of-SSA coalesces ours into one.  The
loop sums are `long long` and copied each iteration to `u64 s1, s2`
(sunk to the exit), which `gimple_can_coalesce_p` won't merge (different
types).  The standalone copy's exit `cmp` has the iv first in the
original; ours gets the bound first because forwprop4 re-canonicalizes
the compare by SSA version (the bound reuses the old iv's freed names).
So the body is `smcSum` (always_inline, inlined into smcPrepare as is)
and `smcChecksum` wraps it with `optimize("no-tree-forwprop",
"no-tree-reassoc")`: the body's early passes run with the object's flags,
the wrapper's late ones without forwprop (the cmp) and reassoc (SWAP32's
first add).  An `optimize` attribute can't change alignment (gcc computes
the alignment logs once per file).

fcrtEncrypt's four exits each get their own epilogue copy, which
bb-reorder makes only for exit edges at >= 10% of the entry frequency.
That needs `size != 0x4000` near 50% (getBeU32 and verifyFcrt declared
pure, so only the log side has the call heuristic) and
`__builtin_expect(off < 0x4000, 1)` at builtin-expect-probability 60
(set for the object).

Still off:

- `kvPrepare` (246): the hash check is the inlined `kvHashOk` (its ver/key
  share stack slots with the inlined kvEncrypt copies, which gives the
  original's 108-byte frame), and `__builtin_expect(kv->size != 0x4000, 1)`
  makes the size error the fallthrough.  Still off: register allocation.
  The original has name in esi and alt in ecx, saved around each call
  (caller-saves); ours gives alt esi (popped right after file) and spills
  name, so the two kvEncrypt copies come out alike and cross-jumping
  merges their tails (the original keeps both, with buf+16 in [56] on
  one side and edi on the other).  Hints on the other tests (all 243
  combinations), declaration order and other expect probabilities don't
  change it.
- `daeEncrypt` (443): `if (size) do { ... } while (off < size)` with
  `buf[off + k]` header tests stops gcc peeling the first iteration and gets
  the original's 108-byte frame; still off: the processing block (call
  daeEncryptOne, `n++`) comes before the loop head in ours, and the
  original keeps buf/size/orig in edi/ebp/esi and `len` in memory.
  The original's off is a loop-region allocno in edx, saved around each
  call, with the parent's copy in ebx (`xor ebx,ebx` ... `mov edx,ebx`
  before the guard): IRA regional allocation, like smcChecksum's sums and
  kvPrepare's alt in ecx.  Loop forms (for/while/do-while), header test
  spellings and hints on the header, hash and loop tests (best 403) don't
  give it, and no object-wide IRA flag (-fira-region, -fira-loop-pressure,
  -fno-ira-hoist-pressure, ...) helps any of the five without breaking
  the 42 that match.
- `cfPatchSlots` (27) and `cfEncrypt` (94, inlines it): `SWAP16` is
  `((x & 0xff) << 8) + ((x & 0xff00) >> 8)` (not a rotate in the loop or the
  last slot, a rotate for `tbl[0]`), and one `tbl[0] = SWAP16(n)` after the
  `if (end > max)` (the zero case shares it). The loop's exit `cmp` had the
  bound first (ivopts rewrites the compare use last, so the bound reuses
  names the other uses freed, and forwprop4 sorts by version);
  `always_inline, optimize("no-tree-forwprop")` on cfPatchSlots fixes it
  standalone (37 -> 27) without changing cfEncrypt.  The smcChecksum-style
  wrapper doesn't work here: the inliner re-folds `end > max` against the
  wrapper's low-numbered `max`.  Left: the tail.  The original computes
  `n` twice (`lea edx,[2+eax]` / `add eax,2`: index and `block + n - 1`
  from one, `tbl[0]` and the return from the other), ours once; no flag
  in the attribute changes that (48 tried).  cfEncrypt's original tail
  has `(trips + 1) + 1` unfolded and no PRE'd `block - 1`, and its copy
  tests `over == 0` (giving n = 0), which the standalone one doesn't;
  `while (over)` loops with a clamp or break (8 forms) give a different
  structure (95+).  `buf[539] = (type == 2)` is an if/else there.

## app/mode_update.c

Draft of the whole object, with string literals. 12 of 14 functions are
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

getConsoleFiles needs `__builtin_expect(netMount(...), 1)` at 68% (build.sh
sets `builtin-expect-probability=68` for the object). The bad-blocks trace
only takes the shared return block if the mount-failure block (estimated
frequency) drops below round 2's 2000 while the mount-success edge stays
under round 1's 5000: the netMount success estimate must be about 67-70%.
No predictor combination gives that (gcc 6's "early return" heuristic
predicts each failure path *taken*, 61%, unless its block is the last one
before the return block; both sides calling gives the call heuristic 50%).
With the bad-blocks check as the outer `if (checkBadBlocks()) {...} log;`
66-70 all match.

getSecurityFiles is three functions: the loop, then `getKv(dir)` and
`getSmc(dir)` as static helpers (inlined) with their own early returns.
Written as one function, no hint combination works: the smc BLDR path's
copy of the `size > 0x2fff` test needs both its edges >= 10% of the entry
frequency, which needs the kv-good path in round 2 of bb-reorder, and then
the BLDR block's trace comes before the verify-failure block's.

Still off:

- `mode_update` (30, no hints): the update path is nested `if (ok) {...}
  else {log; ret = N;}`. The failure strings in `.rdata` come after the
  success-path strings, innermost first (buildImage, getConsoleFiles,
  parseIni, parseConsoleInfo, netConnect), which is the else-branch order.
  netConnect, parseConsoleInfo and parseIni are nested in mode_update, so
  the 5s in the return phi get const-return (netConnect 33%, pCI 54.7%,
  parseIni's 1 gets early-return 79.3%). getConsoleFiles onwards is
  `static void updateNand(dumpDir, int *pret)` (nested, `*pret = N`),
  called as `updateNand(dumpDir, &code); ret = code;`: profile_estimate
  runs before IPA inlining, so inside the helper there is no const-return
  (gCF 50%, bI 61% early-return), and the `code` copy keeps `ret` an SSA
  name in mode_update (passing `&ret` kills its const-return) and
  coalesced with the helper's ret (one `ebx`; a `u32` return splits it).
  Nesting also fixes `dumpDir` in `esi` (LRA inheritance runs along
  fallthrough EBBs, so success must be the fallthrough before bbro).
  Left: four swaps among frequency 0-4 cold blocks in the last bbro round
  (flash-skipped/-clean, no-HDD, writeImage error, -r/-i errors). Those
  are Fibonacci-heap ties: strlen-loop headers (DFS back edges) and
  blocks after a trace end get priority keys, the rest go by frequency,
  and equal keys follow the heap's shape. A replay of the heap from the
  bbro dump reproduces our order exactly, and no small key change
  (+-3, up to 5 nodes, any round) nor a phantom node gives the
  original's, so its heap history differs in shape somewhere. Hint and
  structure searches (expects, labels, if/else swaps, tail sub-helpers)
  didn't get below 30.
  `python wip/fibsim.py <-fdump-rtl-bbro-details dump>` replays the heap
  and checks every extraction (all 60 match). In bbro numbering the
  original's last-round order needs, besides ties: `-clean` test 4 -> 3
  (with `-v` still 2), writeImage error 2 -> 1, no-HDD 3 -> 2 and the
  `-ip` error 3 -> 2; even then no-HDD stays the heap parent of the
  WARNING block (linked in a consolidate at equal key), so one pair is
  still swapped. A `__builtin_expect` making the `-noreeb` match 60-65%
  likely gives the `-clean` change (30 -> 22 lines), but getConsoleFiles
  needs the param at exactly 68 (67 and 69 fail), and expect is
  first-match, so both can't hold. Param-free hints can't make 60-65%
  there (both arms call: 50%; hot label 85%, cold 0%), and no single hint
  call or hot/cold label on any arm of mode_update/updateNand improves 30.
  A "phantom" branch (test of a never-written static guarding a hint
  call, folded after IPA) does divert frequency at profile time, but its
  test block merges into the next one and keeps its own frequency.
  `continue` (50%) and `goto` (none) add no usable predictor in gcc 6.
- Crafted profile (2026-10-20): `sh wip/mufdo.sh <dir> [overrides]` builds
  mode_update with `-fbranch-probabilities` and a `.gcda` from
  `wip/gcda.py` that reproduces the guessed profile exactly (no overrides:
  the same 30-line diff) with counts only for mode_update and updateNand.
  Overrides set single edge probabilities with no source change and leave
  getConsoleFiles' param alone: `mode_update:39>40=62` (the `-noreeb` match)
  gives 22, plus `updateNand:24>25=14.5` (writeImage error) gives **8**. Left
  is one swap: "avatar data skipped, no HDD detected" (updateNand 13>18) is
  placed right after the `-clean` arm instead of after the WARNING block.
  Moving 13>18 alone breaks others (18-28%: 28 lines, 30-36%: 8), and
  greedy single-edge and random 2-3-edge searches (`wip/mufdo_search.py`)
  over all two-way branches find nothing below 8. Next: read the bbro
  dump/heap (`wip/fibsim.py`) for no-HDD vs WARNING keys and set counts
  for unequal keys directly (a block-count override instead of edge
  probabilities), or override the major arm or three-way edges.
  What a profile build needs, all found the hard way: the arcs compile and
  the profile compile must both use `-o -` (static functions' profile ids
  and the `.gcda` name come from the aux name); the summary record must come
  before the function records; `-fno-inline-small-functions` (else known_hot
  and count-scaled badness inline getConsoleFiles into mode_update; the
  called-once inline of updateNand stays); `-fno-partial-inlining` (feedback
  fnsplit makes `.part` clones); `-fno-ipa-profile` (it raises the hot
  threshold to 99.9% of the unit's time); `-fno-reorder-functions` (a hot
  node goes to `.text.hot`). Counts for every function in the TU don't work
  (inline order follows counts); the TU can't be cut down to mode_update
  alone either (747 lines: it needs update_usage etc. visible).
  Moving it to the build would mean a second compile of the same C file with
  these flags, splicing only mode_update from it (splice.py would need to
  allow a second pass), and generating the `.gcda` in build.sh.
- Whole object from this draft: `.rdata` string order differs already in
  getBadBlocks (its error string comes second, the original's last), and
  `.data` is 4 bytes where mode_update.s has `useConsoleAddons` plus 0x14
  zero bytes (0x18).

## app/image_read.c

Draft of the whole object, with string literals. 20 of 33 functions are
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

- `remapBadBlocks` (2): the inlined findFreeRemap keeps its `numBad != 0`
  guard. The wear-area test as `< numBlocks - 32` with the remap path
  first keeps ce1 (find_if_case_2) from hoisting `b = numBlocks - 1` above
  it. `int i` drops the guard (VRP1 gets `numBad >= 1` from the signed
  IV, so the inner loop is entered without a test) but flips the exit
  compare to `cmp ecx,esi`; `u32 i` IV ranges stay symbolic, and
  `__builtin_unreachable()` bounds on `i` don't help.
- `findAnchor` (11, with `u32 shaSelfCheck`): the "invalid" log for the
  second block is jump-threaded into two copies; the original keeps one and
  tests ok0 after it (with `xor eax,eax` hoisted above the test). Other
  tail shapes (`ret` variable, if/else-if, ok1 first, nested) don't help.
- `copyMmcImage` (11): uncprop reuses memcmp's 0 for `return 0`; every
  non-int return type merges the returns instead. With `u32` it matches
  under `-fno-if-conversion`: ce1 moves the success path's `ret = 1` above
  the branch because that edge is predicted 61% (call 71%, early return
  39%); the original's must have been <= 50%. `__builtin_expect` and other
  shapes didn't get there.
- `getImageKv`: fncmp MATCHes with `__builtin_expect(…, 1)` on `size ==
  0x8000`, the first verifyExtended and the sanity test, at
  builtin-expect-probability 67-70 (no natural predictor gets the alt-KV
  success edge to 10% of entry). But jcmp shows the `size != 0x8000` exit
  jumps to the alt-success epilogue instead of the shared one after the
  "not sane" log, so the build differs by 4 bytes; not built yet. Without
  hints: 26. `python wip/kvsweep.py` sweeps hint subsets x probabilities
  with jcmp; a 3-hint sweep (56-94) was stopped before finishing.
- `listFlashFiles` (23), `fsGetFile` (70): register allocation (fsGetFile
  has fsValid and name in esi/edi swapped).
- `detectController` (35, was 61): pins `"D"(n)` after the small-block log
  and `"b"(i)` at the loop top give the original's registers. Left: the
  original head-merges the two `found = 0` edge copies into one `xor
  eax,eax` before `n <= 1` and keeps found in eax outside the loop (memory
  inside); `int found` merges but spills found everywhere.
- `getImageSmc` (117, was 163): `int addr`, `int size` and `!addr || (addr
  != 0x800 && addr != 0x1000)` give the two address registers (int for the
  logs, its unsigned twin for the checks and memcpy) and the layout. Left:
  the original's addr == 0 path prints a constant 0 (a phi copy on that
  edge, tails cross-jumped), and the bad-address path keeps its 0x1000
  copies on the size-test edges where ours are head-merged above the call
  (cfgcleanup try_head_merge_bb, after RA). if/else-if and separate `if
  (!addr)` forms, casts and types were worse.
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

buildCleanup's first loop ends at `&xb.smc` (a pointer loop with `m !=
&xb.smc`; `i < 11` holds the end in a register). getImageLdv's `ldv` is
`u32`, tested as `(u8)ldv > 32`. irlit leaves every string on an `__asm__` line alone (pins). checkHeader's SysUpdateAddr test is two
`if`s with an `__asm__("")` between: as `||` ifcombine makes `a | b` with
the second test's SSA name first, and forwprop orders operands by version;
written the other way round the order is right but the blocks move.

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

Draft of the whole object (all 32 functions, data as statics). 28 match;
26 are built from `src/app/net.c` (mixed): netFree, netFindBeacon,
netTimerStart/End/Elapsed, netSendStr, netSendData, netCheckOk,
netOpenSocket, netClose, netDisconnect, netGetInfo, netDumpNand,
netGetBldrs, netGetBadBlocks, netReboot, netMount, netUnmount, netGetFile,
netReadBlocks, netFormatSysex/Compat, netWriteBlocks, netEraseBlock,
netMkdir, netSendFlash. `python wip/netmixed.py <fns>` makes the src file from the
draft (it keeps a function's `__attribute__` line); test the draft with
`FNCMP_LITERALS=1` (net.s's strings are named `net_<address>`). The src
file gives the strings as `static const char net_X[] = "..."`, not
externs, so gcc still folds `strlen` of a command in an inlined
netSendStr; splice.py drops gcc's .rdata copies. netRecv stays asm and is
declared `regparm(1)` (gcc's local convention for it). The names for the
unexported functions and data (`netRecv`, `netFindBeacon`, `netSock`,
`netEmpty`, `netStartTime`, ...) are in `split.py` SYMBOLS, and the ws2_32
IAT slots are renamed to winsock2.h's `__imp__send@16` spelling
(`IAT_NAMES`; `.string` lines are skipped so "bind"/"connect" in messages
survive).

What got them:

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
- netSendStr as `if (send(...) != len) return 0; return 1;` rather than
  `return send(...) == len;`: that fixed the cprop_hardreg ebx/eax in
  netMount/netUnmount (the netRecv block no longer precedes the `cmp
  len,2` block when cprop_hardreg walks them, so nothing is inherited) and
  the ifcvt `xor eax,eax` hoist in netGetFile/netReadBlocks. netSendStr
  itself compiles the same.
- OK-reply check written out (not netCheckOk, which inlines as `sete`):
  `r = netRecv(&rlen); if (!r) return 0; ret = 0; if (rlen == 2 &&
  getBeU16(r) == OK_REPLY) ret = 1; netFree(r); if (ret) return 1; return
  0;` plus `__attribute__((optimize("no-crossjumping")))`, which stops
  jump2's head merge of the two `mov eax,1` above `cmp ebx,netEmpty`
  (netFormatSysex/Compat, netEraseBlock). netWriteBlocks also needs
  `no-early-inlining`: with netFree inlined early its `!= netEmpty` edge
  (call predictor) puts the free block at frequency 953, under bbro's 1000
  duplication threshold, so it shares the epilogue. netMkdir has it inside
  `if (name) { char cmd[264] = "MKDR"; ... } return 0;` (the original
  zeroes eax for the `!name` return and the memset together).
- netSendFlash: `{ int rlen; u8 *r = netRecv(&rlen); if (r && rlen == 2 &&
  getBeU16(r) == OK_REPLY) { netFree(r); success } else { netFree(r);
  failed } }`. rlen in a block shares its stack slot with netTimerEnd's
  `now` (one `lea esi,[28+esp]` for both).

What got them (this round):

- netReadInfo (wip only): eight explicit field swaps, not a loop. cunroll
  gives the loop's first copy fresh SSA names in reverse statement order,
  so reassoc's equal-rank tie (SSA version) flips its first add. The
  straight-line swaps then need the success block to start without a call
  (else the call heuristic makes `len > 1183` 29% and bbro shares the
  epilogue): `int ok = 0; if (send == 5) { r = netRecv; if (r && len >=
  size) ok = 1; } if (!ok) { failed; return 0; } swaps; logs; return 1;`
  (ok is threaded away after profile_estimate). Not built: in the mixed
  file netInfo is extern, and sched2 then puts the `netInfo = info` store
  above the two `reserved` stores.
- netSendFile (wip only): `if (!name) return 0; if (!buf) return 0;` then
  a C99 `char cmd[264] = "SNDF";` at function scope (an inner block's cmd
  clobber gives the `!name` return its own PHI, so a second `xor eax,eax`
  block), no-crossjumping, and `__asm__("" : : "m"(buf))`: separate tests
  get the pointer heuristic, which puts buf's two uses just over IRA's
  memory-vs-callee-saved cost, so buf went to esi. Not built: the shared
  return-0 block is `.p2align`ed in the original (compute_alignments:
  branch frequency > 4 x fallthru, align-loop-iterations). Ours has the
  separate tests' frequencies (the `&&` form's would align it);
  `--param align-loop-iterations=2` aligns it but also a netSendData block.
- netFindBeacon: `volatile u32 addr;` set to 0 after `socket()`. The
  original keeps addr in a stack slot, stored once and loaded on every
  return (even the socket-failure one), so it was a memory variable; with
  it in memory the setsockopt/bind/select-error paths, each written as
  `log; closesocket(s); return addr;`, crossjump into one tail and the
  timeout path keeps its own copy.

Open (diff lines from `re/fncmp.py`):

- netWritePatches 9 (4 without no-crossjumping/no-early-inlining, where
  only jump2's head merge of the two `mov eax,1` differs). With
  no-crossjumping the inlined netSendData's two failures reach the return
  through a block holding hdr's clobber, a different PHI edge from the
  send failure's, so they get their own `xor`. hdr shares rlen's stack slot
  in the original, so it really is the inlined netSendData. The head merge
  is try_head_merge_bb (needs single-pred successors that aren't df-dirty);
  an empty asm in the netEmpty branch stops it but breaks the threading.
- netConnect 39: the original ends `mov eax,1; test; jne` with every
  failure sharing one `xor eax,eax` block. Ours: phiopt1 turns `if
  (!netReadInfo()) return 0; return 1;` into `setne` (with no-ssa-phiopt,
  ce1 does), and uncprop makes the beacon-failure return reuse addr, so the
  PHI lives in ebx and every failure gets `xor ebx,ebx`. The original's
  readinfo-failure block must be a lone `eax=0` that the `log; eax=0`
  failure blocks crossjump into (a 1-insn crossjump is allowed when one
  block matches whole). Block-local `sa`/`saLen`, readinfo in both
  branches, goto forms and `int` return didn't keep the branch.
- netRecv 58/netRecvVerbose 53: the drafts now write `if (buf !=
  &netEmpty) free(buf); return NULL;` on each failure path (the original
  repeats the check per path) and netRecv ends `if (got == size) { *len =
  size; return buf; }` then the short-count failure, which puts the success
  block last as in the original. What's left in netRecv is registers (size
  ebx, got edi, buf esi in the original; ours esi/ebx/edi), which come
  from dom: with `optimize("no-tree-dominator-opts")` it is 13 lines (the
  `*len = 0` store scheduled first, a recomputed `cmp` before the `je` to
  the success block, block order). dom rewrites `*len = size` to `*len =
  got` from the `got == size` equivalence and leaves a degenerate
  `got = PHI <0>` preheader; moving `*len = 0` or swapping the comparison
  didn't change it.
- `-fno-tree-dominator-opts`, `-fno-if-conversion`, `-mbranch-cost=1`,
  `-O2`: none is better for the whole file.

## app/build.c

Draft of the whole object (all 41 functions). 24 match and are built
from `src/app/build.c` (mixed): findFileOffset, findFileSize, findFile,
readMetaFile, makeTimestamp, loadCommonFile, loadBinFile, loadLocalFile,
setFileData, iniRangeOk, raiseKernel, patchHeaderOpts, rotSumSha,
countBits, isUpdateBl, patchPayloadSize, showSmcConfig, blmodMissing,
patchFreeboot, encodeUpdateBls, logPowerButton, timestampToFileTime,
loadBaseFile, loadBaseFileMeta. Switch tables go through
split.py's `#@J` marker (README, mixed objects); checkBl, loadBlFiles,
loadConsoleBlFiles and encodeBls have them too. `python wip/mixed.py app/build
<fns> > syms.txt` makes the src file from the draft (a generic
netmixed.py: strings become `bd_<address>` statics, set up per object in
its `OBJS`); `python wip/mixedsyms.py bd syms.txt` puts the string names
in split.py's SYMBOLS. Test the draft with `FNCMP_LITERALS=1`; `sh
wip/all.sh wip/app/build.c <fns>` runs fncmp over a list. fncmp doesn't
check offsets from named symbols: a wrong `struct xebuild` field offset
only shows in `sh build.sh`.

- loadFileCrc is an inlined helper: loadBaseFile, loadBaseFileMeta,
  loadCommonFile, loadInputFile, loadBinFile and loadLocalFile (twice) are
  wrappers around it, and loadCommonFile/loadBinFile/loadLocalFile match
  with it inlined. Its own out-of-line copy is 14 lines off (the
  verbose "reading %s (0x%x bytes)" block is placed after the returns), so
  the mixed C keeps its body only for inlining (`inline` in mixed.py's
  OBJS); splice.py drops gcc's copy of a function the .s still defines.
- The Win32 time calls are timeutil.c's cdecl ports, not imports: no
  windows.h, declare them as in timeutil.c.
- rotSumSha is XeCryptRotSumSha with logging: byte loops over a `u8
  sum[32]` (the zeroing loop stays a dword loop, the inversion becomes 8
  `not dword`).
- patchPayloadSize's messages say `%r4` (sic), so the source did too.
- raiseKernel takes (magic, build, qfe) words; only build is used.
- timestampToFileTime: `__builtin_bswap16` stays a call in GIMPLE, which
  TER won't put into the call's arguments, so both swaps were computed
  first. `SWAP16` with u16/u32 casts folds to a rotate before the bswap
  pass and is computed at its argument store, like the original (the
  `+`/mask SWAP16 forms of the other objects become bswap16 calls again).
- loadBaseFile, loadBaseFileMeta: `path` is declared inside `if
  (xb.baseDir[0]) { ... }`. Declared at function scope, tail merging
  (`-ftree-tail-merge`) joins the baseDir `return -1` with the inlined
  loadFileCrc's fopen-failure one, which moves the cold blocks; scoped,
  the clobber of `path` sits on one path only and the two stay apart.
  loadBaseFile is `noinline, noclone` in the mixed file: blmodMissing is
  its only C caller, so gcc would inline it or make a `.constprop` copy.
- loadInputFile (~360): the SUPD / nanddump / USVR / common-dir fallback
  chain; the original keeps `r != 0` as a byte (`setne dl`) and tests
  `common & failed` with `and`, and its loadCommonFile tail call is a
  separate return. Two shapes tried (early returns, `r = 0`).
- checkBl (14): structure right (the SE case's dead extra crc32 call is in
  the source); an `asm("" :: "a"(m))` on bl[0] gives the original's
  registers. Left: the original copies the epilogue into the size-error
  (-3) block, not the crc-failure one. In ours the -3 block is colder
  (call + negative-return heuristics, 1.7%) than the crc failure (20.8%).
  bb-reorder copies the 7-insn epilogue only over edges above the
  duplication threshold (10% of entry): so in the original the -3 edge
  is above it and the crc failure below, which needs other predictions
  on both (no negative-return on -3, no opcode-nonequal on `crc != c`?).
- extractSmcConfig (~140): the original's two search loops aren't header-
  copied (`xor eax,eax; jmp cond`); `found == 1` (cmp eax,1) is right.
- appendAddonPatches (18): positive-condition nesting fixed most of it;
  the "not enough room" log and `size -= 4` blocks go after the return in
  the original. They are separate round-1 traces, ordered by frequency:
  room 1615 (both arms call, 50%), `size -= 4` 905 (`== 0xffffffff`,
  28%), the post-loop 900. The original has both below the post-loop.
  An `if (xb.nAddons > 0)` guard fixes `size -= 4` but hoists `added = 0`
  (15 lines); `continue` is a 50% predictor in gcc 6, no help.
- logPowerButton: fncmp can't tell its identically shaped log blocks
  apart, so check the string order in the link. The original's .rdata
  string order is gcc's expand order, i.e. source order: cases 0x59, 0x58,
  0x5a, 0x56, 0x57 after 0x55, each `if ((xb.flags & 7) > 4)` first. The
  case order sets the bb-reorder ties of the three outlined arms.
- fixupPatchSet (~95): like extractSmcConfig, the original's loop is not
  header-copied and keeps `off` on the stack; `__attribute__((cold))` is
  not it.
- blmodMissing matches now that loadBaseFile has its other callers.
- loadBaseFile is static with gcc's local convention (eax, edx).
- With the whole object drafted, ipa-cp clones loadFileCrc (verbose=1) and
  loadInputFile (loadBlFiles' constant arguments); the original has neither
  clone and calls loadFileCrc out of line only from loadInputFile. The
  clone moves loadLocalFile's registers (76 lines in the full draft; it
  matches in the mixed file, which leaves the big callers out). The cause
  is loadInputFile's `crc == 0` clone (`-fdump-ipa-cp-details`: time 40,
  size 322, freq_sum 6066, evaluation 753 against 500). With it stopped
  (a test `noclone`) the loadFileCrc clone goes too and loadLocalFile
  matches. Most of freq_sum is loadBlFiles' and loadConsoleBlFiles' calls
  at ~2.07 per call (`-fdump-ipa-cgraph`); at ~1 each it would be under
  500. So match those loops first.
- showSmcConfig: the fan bytes are bitfields (`u8 speed:7, override:1`;
  `cmp byte,0; js` plus a separate reload for the speed), the regions
  `__builtin_bswap16`/a SWAP32 macro with `(x << 24) + (x >> 24)` first.
- patchFreeboot: `opts = bootFlags & 0xf` before the `& 9` test (gcc sinks
  the `and` into the else path; masking in an else gets if-converted);
  the hold-address pattern and its 9199 replacement are one `u32[4]`;
  `strncmp(kernelStr, "9199", 4)` (inline `repz cmpsb`).
- encodeUpdateBls: a `switch`, not an if-chain (block order).
- verifyBlSigs (169): a switch with SC/SD before SE (gcc orders bit-test
  clusters by case count, then label number; 12..13 counts as one range).
- patchSmcConfig (10): two cold blocks (gpu/cpu fan warnings) in the
  other order; the gpu warning passes no argument (the cpu one does).
  Its string is after the function's last ones in .rdata, so its block is
  last at expand; a `goto` to a block after the return reproduces the
  string order, but not the layout. The two traces tie (keys -1035148)
  and come out of the fibheap in the other order.
- patchBlsResign/patchBlsBlmod (~330), fixupPatchSet: the patch-set walk
  loop isn't header-copied in the original; `-fno-tree-ch` reproduces
  that shape, so something in the source stops pass_ch.
- calcBlAreaSize (212): the original looks up the offset before the size.
- addBlsToImage (361), addUpdateBls (204), loadBlFiles, loadConsoleBlFiles,
  encodeBls, buildFlash: first drafts from heavily jump-threaded
  pseudocode; behaviour checked against it, layout not worked on.
- buildFlash names image_write's helpers (`imgAdd*`, `imgFs*`, ...) only
  in the draft so far; give them SYMBOLS names when building it.

## app/image_write.c

The 38 matching functions build from `src/app/image_write.c`, a mixed
object made by `python wip/mixed.py app/image_write <fns>` (its OBJS entry
turns the draft's `copyright` and `mobileOffset` definitions into
externs; the `.s` keeps the data). Draft of the whole object (IDA pseudocode: `build/decomp_13.txt`, made with
`build/decomp_unit.py ... 13`). `sh wip/iwst.sh` prints every function's
fncmp status. The data it uses are xb fields (0x28-0x5c: spare/hdr/raw
buffers, sizes, FS start/end blocks) and COMMON globals from
`common_bss.s`, named in SYMBOLS: mmcAnchor (4c9164), fsFiles
(4c97c0), fsTable (4cb7c0), hdrTemplate (4cd7c0), imgEnd (4cd840). The
object's own data: `copyright` (.data 44a580, patched per console type),
mobileOffset (46f9c0) and the statics nFsFiles (46f9c4), smcPage (46f9e0).
mobileOffset is reloaded after imgAdd returns, so it isn't a static that
ipa-reference can see through: a global (`u32 mobileOffset;`, in .bss
because the original isn't -fcommon for it, or initialised to 0).

Findings:
- calcEcd and friends are the well-known NAND ECD code (`unsigned int i = 0,
  val = 0; unsigned int v = 0;`, `data = (unsigned int *)spare` at 0x1000);
  only that declaration order matches.
- `xb.bigBlock ? 0xf1f1 : 0x1ffb` as an argument becomes sbb/and/add;
  the original has two calls (`if (xb.bigBlock) return f(.., 0xf1f1);
  return f(.., 0x1ffb);`) that crossjumping merges into a branch.
- The spare LBA writes are bitfield stores (`struct sp`), in the order
  LBA high nibble, bad-block byte, LBA low byte.
- imgWriteStart (regparm src, len, next) is its own function, not an
  ipa-cp clone of imgWriteAt (gcc doesn't clone it).
- checkBootImage returns `long`: as `int`, uncprop reuses the tested
  `xb.bigBlock` (0) register for `return 0`. `u32 bigBlock` fixes it too
  but breaks fixupEmptyFsBlocks.
- buildImage: the size/kv/cf stores follow the asm order once the
  swapped CB offset is a local stored after the constants; the switch has
  no `case 0`; `else if (type != 6 && type != 8)` (MMC/16M nested) before
  the 64M case; the malloc check is two tests (`if (!hdr) return -1;
  if (!spare) return -1;`), which puts the cold blocks in the original's
  order. The two registers left (the `xb.bigBlock` test in switch case 4
  is ebx in the original, the type 2 `bigBlock` test edx) take empty-asm
  pins (`__asm__("" :: "b"(bb))`, `"d"(bigBlock)`); fncmp still shows
  ddisasm's `__ImageBase` for 0x400000 (same bytes). Its jump table goes
  through split.py's `#@J` marker (README, mixed objects).
- smcSetLoad: SWAP32's top byte is `((x) & 0xff) << 24`; only that form
  folds `(0x4000 - size) << 24` into `-(size << 24)`. The other
  functions compile the same either way.
- blockEccOk: `pages` variable (no entry guard), `continue` after both
  tests; pageEccOk ends `if (spare[15] != ...) return 0; return 1;` (the
  standalone function compiles the same, the inlined copy branches the
  original way).
- imgAddMobile: big block path first, error path duplicated (crossjumped),
  small path `if (imgFits) {...; return ret;}`. Left (18 lines): the
  "mobileOffset already set" block's placement.

Still off:
- writeInitialHeader: the original inlines imgWriteStart(&hdrTemplate,
  0x80, 0xf1f1) (the `cmp rawSize,127` and one-block spare loop) but calls
  it for 0x1ffb, and checkBootImage calls it for both. Ours inlines none:
  `-fdump-ipa-inline-details` estimates ~60 for the call (limit:
  max-inline-insns-auto 40, or 50 with a loop-iterations hint). Helpers
  must be macros, not static inline functions, or ipa-split splits
  setFsTable and the `next != 0xf1f1` predicate doesn't shrink the
  estimate. `static inline` imgWriteStart inlines every call.
- setFsTable is one loop with the chain/fill test inside it, which gcc
  unswitches: that is what puts `SWAP16(next)` (rol) and `start - fsStart`
  before the chain test. SWAP16 is `(((x) << 8) & 0xff00) + (((x) >> 8) &
  0xff)`: the chain values' `>> 8` is then done in 16 bits (`shr bx,8`).
  The tmp/xeBuild64 (gcc 4.9) copies of imgWriteStart/imgWriteAt/
  imgWritePage have the original's layout too (chain loop falls through,
  the tail memcpy+memset block last), and compute the tail with `cmovb`
  (`rem < 0x4000 ? rem : rem & 0x3fff`), `blocks = rem >> 14`
  unconditionally, then `if (tail) blocks++; if (off & 0x3fff) blocks++`.
- imgWriteStart (234 lines with registers normalised, 113 with the chain
  bias below): the head is right
  with `tail` and `blocks` as above (all 80 spellings of the
  tail/blocks/first statements tried come to 113). Left: block order.
  The `rem & 0x3fff` branch's two edges come out of jump threading with
  no probabilities, and bbro takes the memset side as the fallthrough;
  the original takes the other one. The fill/chain unswitch test is
  50/50 and ours lays out the fill loop first; any bias to the chain
  (`__builtin_expect(... , 0)` on the fill test, even at probability 55)
  gives the original's order (234 -> 113), but costs imgWritePage and
  imgWriteAt lines. -fno-thread-jumps / max-fsm-* params change nothing.
- imgWritePage (17 lines, 7 normalised): `x = off & 0x3fff;
  __asm__("" : "+c"(x));` before `start` gives the original's ecx and
  separate `test`; `__attribute__((noclone))` keeps ipa-cp from cloning
  it for 0x1ffb, and then addSmcConfig/imgAddRaw match in the draft too.
  Left: the block loop's IV is a copy of the reloaded `start` (the
  original reloads straight into ebp), and the end-marker index's
  operand order. `__builtin_expect(next != 0xf1f1, 1)` at
  builtin-expect-probability 55-60 fixes the latter (11 lines).
- Return types: with `u32` returns the `return -1` paths lose gcc's
  negative-return prediction; imgWriteStart then inlines into every
  caller (ipa-split header), with `int` into none. The original inlines
  exactly the header's 0xf1f1 call, so its estimate sits between.
- imgWriteStart: `__builtin_expect` on the range check (0) and on
  `next != 0xf1f1` (1) at the default probability takes it to 20
  normalised lines (registers and the order of the fill loop's five
  peel exits: the original has 5,1,2,3,4, ours 5,4,3,2,1; same in imgAdd).
  Those hints also move the inline estimates, so they need checking
  against writeInitialHeader.
- imgAddMobile: builds from C with `__builtin_expect(imgFits(off,
  len), 1)` on the small-block test and `--param
  builtin-expect-probability=50` (build.sh, for the whole object). That
  makes every expect in image_write 50%, so the expect hints below are
  gone. Use label attributes instead (`l: __attribute__((hot));` or
  `cold` at the start of a block): PRED_HOT/COLD_LABEL is 85%, combined
  with the other heuristics by DS, whatever the param.
  The 50% expect overrides the early-return heuristic (39%), which puts
  the fits block's trace before the "already set" one; the 50/50 base
  keeps the align block a 1-block trace, so bbro still duplicates it.
  (Earlier tries: hint calls via PRED_CALL get the order but pull the
  align block into a longer trace, losing the copy.)
- imgWritePage (17): two RA spots. (1) After the memcpy the original
  loads start straight into ebp (the block iv) and derives end/pgoff from
  it; ours reloads start into esi and copies to ebp last (the iv's PHI
  copy is emitted after ivtmp*512 and end in the preheader, so LRA
  inherits esi). (2) Tail `fsTable[start + n - 1 - fsStart]`: expand
  sorts plus operands by regno, giving `(plus end not)`, so the add ties
  to end (`mov eax,[4+esp]; not ecx`); the original ties to the not.
  Tried without luck: all expression/cast forms of the tail (reassoc
  canonicalises them), loop forms (b from start adds a guard), local
  types/order, ~60 optimize attributes, setFsTable as a function, guarded
  dead uses of start+blocks. Best: `__asm__("" :: "a"(start + blocks));`
  before the loop, 11 lines (fixes (1)'s ebp, tail becomes lea).
- finalizeImage (132 normalised): the ECD loop names `xb.hdr + ...` /
  `xb.spare + ...` in each use (PRE then keeps both in registers and
  reloads them after the ECC write, like the original); `int blocks`
  stops forwprop folding the remap bounds test into a MAX; the
  bbController swap indexes `xb.spare[i * 16 + k]`; the big-block LBA loop
  is `n = xb.blocks / 8; s = xb.spare;` with a running pointer and
  `((struct sp *)s)->b2lo = b >> 8`. Left: the ECD memcpy (the original
  doesn't know the destination's alignment, but an asm on `raw` also
  loses its points-to and xb.hdr gets reloaded), registers and layout in
  the remap loop.
- imgAdd/imgAddFile/writeFsTable: imgAddFile's big-block path is
  `imgAdd(off, data, len, 0x2a, 0xffff, 1)`; that call and writeFsTable's
  two inline as ipa-cp clones called once (imgAdd must not be `inline`,
  or imgAddMobile's calls inline too). imgAdd's head is imgWriteAt's
  (`if (len > first)`, cmov tail), npages `len % 512 ? (len + 512) / 512
  : len / 512` before pages, `p + (partial ? npages : 32)` inside the
  block loop, len stored high byte first, and `left` computed at its use
  (writeFsTable's copy unswitches on `off & 0x1ffff`). writeFsTable takes
  `blk = off >> 14` before the big-block realign and again inside it.
  Left: layout ties (imgAddFile's spare loop puts the small-block side
  inline), and standalone imgAdd's `pad == 1 && tail`, which GENERIC
  folds to `&` (both operands simple), so its then-path memcpy isn't
  duplicated as in the original.
- imgWriteStart with labels (2026-10-20): 172 -> 60 normalised lines.
  A hot label on the chain store moves the fill loop out of the main
  trace (89). The `len & 0x3fff` test after threading: its tail == 0
  memcpy copy is shared with the `len == 0` path, and bbro only chains it
  after the test if that edge's frequency beats the `len == 0` edge's
  (a cold `len == 0` label alone gets the head right, 88). The best
  combination from a coordinate-descent search over 10 label spots
  doesn't follow that reasoning though: cold labels in the
  `len > first` branch, the `rem >= 0x4000` side and `tail != 0`, hot on
  `next != 0xf1f1`, the chain store and `return -1`, cold on the 0xffff
  end marker). The ternary tail as if/else is not equivalent (other
  counts). Left: the fill loop's vector peel registers (bound spilled),
  `lea r,[r-1]` vs `mov/sub`, and the order of the cold blocks after the
  main trace. Same labels on imgWriteAt: 249 -> 202, but its frame is
  76 bytes vs 60 (structural); imgAdd's head form didn't help there.
  writeInitialHeader: imgWriteStart(0xf1f1) specialised to len 128
  still estimates size 65 (growth ~60, limit 40, or 50 with a
  loop-iterations hint); `op2 != 61937` covers only size 16, so the
  original body must be smaller where next is known.
- tmp/xeBuild64 decompiles with IDA (idapro on a copy of the ELF):
  imgWriteStart 41b1b0, imgWritePage 41b3b0, imgWriteAt 41b5c0,
  buildImage 41b810, imgAdd 41c960, imgAddFile 41ce20. Older source;
  structure only.
