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

Draft of the whole object, with string literals, from before the hints.
The object is built entirely from `src/app/options.c` now (no options.s;
README has how the strings are emitted).  setBoolOption's 4 fncmp lines
are ddisasm writing 0x400000 as `__ImageBase` (the bytes match).  Notes
from getting there:

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
- 2026-10-21, applyIniOptions written as goto code in the original's
  block order (`wip/app/options_aio_goto.c`; to try it, replace the
  stand-in in src/app/options.c and put it after macidSet).  With
  `optimize("no-reorder-blocks", "no-reorder-blocks-and-partition",
  "no-tree-tail-merge", "no-crossjumping")` gcc keeps the source block
  order exactly (fncmp 247 lines, from 1177 with bbro on).  The inlined
  parseButton tail is called by name: `int parseButtonPart(const char *)
  __asm__("_parseButton.part.1") __attribute__((regparm(1)))` (gcc's
  number for the part in the whole-C build).  Why each flag:
  - tree tail-merge drops one of two identical split-edge forwarders, then
    the survivor merges with its successor at the forwarder's position
    (moves the cpufan block into the chain).
  - jump2's crossjump redirects each chain test (`cmp [x],-1; je`) into
    the identical tail of its duplicate after the previous option's store.
    The original's duplicates are bbro copies made after jump2.  The 50%
    probability rule in outgoing_edges_match can't protect them: it needs
    the two tests' probabilities 50% apart, and then the gpufan..dvdregion
    labels can't get the original's alignment.
  Two things this approach cannot do, both of which need bbro's STC:
  - the epilogue copy after sprintf (only connect_traces' copy_bb
    duplicates the `add esp; pop; pop; ret` block; no other gcc 6 pass
    copies an epilogue, and without bbro it is emitted once);
  - macid's shared error tail (`mov [esp+4],msg` in each predecessor, one
    log/showHexPairs/log): only crossjumping makes that, and it has to be
    off for the duplicates.
  Smaller things still open in that draft: `(f & ~4) | 2` folds to `& ~6`
  (write it as two statements, like setBoolOption), `(f | X) & Y` folds to
  `f & Y` in the nomobile/nosecurity duplicates (needs a pin), and
  registers (esi for bootFlagsOff, the xellbutton2 registers).
  So STC has to stay on.  Next step: a full STC simulator (find_traces,
  connect_traces, copy_bb_p from gcc 6.2 bb-reorder.c, on top of
  wip/fibsim.py's heap) fed with the CFG, frequencies and REG_BR_PROB values
  gcc sees before bbro, to work out which profile gives the original
  layout.  The goto form helps there because it fixes block order and the
  CFG shape, so only the profile is left to find.
- 2026-10-22, crafted profile (like mode_update): src/app/options.c
  builds applyIniOptions with a profile (build.sh), `src/app/options.prof`
  its edge overrides (re/gcda.py, `@file` accepted), written by
  `python wip/aiodesign.py <profile_estimate dump>`.  The code matched
  first, then the block layout, then (below) the label alignment padding.
  What it took:
  - Counts only for applyIniOptions; the rest are `#pragma GCC optimize
    ("no-branch-probabilities", "no-reorder-functions")`.  A callee with an
    optimize attribute can't be inlined into a caller with other options
    (ipa-inline.c:453), so applyIniOptions inlines always_inline copies
    (optIniInt, stripColons, macidSet, parseButton's first tests), and
    po_hint needs parseOption's attribute too.  A profile build never
    splits (feedback fnsplit: "not inlinable"), so parseButton's part is
    an explicit `cold`, `.text.unlikely` function named `_parseButton.part.0`,
    and parseButton calls it (with an expect on the winbutton match: the
    cold call is predicted never taken otherwise, and 36 isn't hoisted).
  - The layout: the original's cold blocks are ordered by heap ties among
    identical options.  Here every trace start gets its own frequency in
    the original's order (bands per STC round, priority keys where a pred
    ends a trace, round 3's count test on stale threaded counts, the 10%
    copy threshold); see the comments in aiodesign.py.  The strip loop's
    back edge must stay <= 87% (ivopts uses the profile's trip count).
  - Source: xellAltButton/dualButton u32 (else uncprop reuses the field
    load as parseButton's 0); the option set as two statements (nodvd's
    `and ~4; or 2`); an empty `__asm__("")` in macid's valid branch (stops
    find_if_case_2 hoisting `i = 0` above validateString's test; it does so
    even with the guessed profile); `if (xb.type == 2)` outside the type
    2..5 block (VRP threads that block's range test past it, not a switch,
    and smcnoblink's skip path gets the original's type reload).
  - Alignment (final.c compute_alignments): a jump target with no fallthru
    is aligned when its incoming edge frequency > freq_max / 100 (or it is
    10x its layout predecessor); with a fallthru, when branch > 4 x
    fallthru (align-loop-iterations).  mingw emits only `.p2align 4,,10`,
    so labels at 1..5 mod 16 never get padding; alignreq-style tables need
    that.  The original's padding fits gcc's guessed profile (freq_max
    3716, threshold 37: "alternate xell" at 38 aligned, getIniU32 at 37
    not).  The designed bands put getIniU32 and a few others above my
    threshold (25).  A threshold of 52 (freq_max 5200..5299) would sort all
    but xellbutton2's header rest, which needs a priority key, and
    L_425c30 (dualButton test after olddvd's warning): the original pads it
    as a loop (branch > 4 x fallthru), and with olddvd's I falling out of P
    that can't hold under a consistent profile (PL + 5G > 4I with I >= PL).
    The original's frequencies there must be stale ones left by jump
    threading; a profile alone can't give them.
  - 2026-10-22 (later), matched (src/app/options.c, analysis tools in
    wip/aio/README.md).  Stale counts come from dead edges: a test of a
    never-written static (`aio_never*`) is still there when the profile is
    read (pass 042t), IPA marks the static read-only and ccp2 folds the
    test.  gcc doesn't touch the counts when an edge goes, so a block whose
    dead in/out edge carried flow keeps that count (a block merged into it
    keeps the first block's count; an emptied forwarder just goes).  Four
    of them:
    - freq_max: `--param align-threshold` is per object (gcc 6 params
      aren't per function) and 45 drops padding in parseOption, so the
      threshold 56 comes from freq_max 5650: a dead cycle through the
      blSuffix test.  A natural loop doesn't work (its preheader merges into
      the header and keeps the real count); a second dead entry from the
      type != 2 path makes the cycle irreducible, so there is no preheader.
    - xellbutton2's header rest: `&& !skip` on parseButtonI's power match
      gives it a dead pred.  Its block keeps 66 (heap order, between the
      warning and dualboot) while its edge says 46 (not aligned).
    - L_425c30: olddvd's OPT written out with two dead tests.  Q before
      iniBoolInvalid merges into that block and leaves it 435 (with a dead
      pred, else it is removed as a forwarder), so I->W (W 65) is 390, in
      round 2's trace, and I->G 53, under the threshold.  The dead exit at
      olddvd_set gives the merged `and ~4` block 250 more, so the branch
      edges into the test beat 4 x W.
    - band shift: the round-4 bands above 52 moved up 4 (I's 57..62) so the
      xellbutton default block's 56 (loop alignment test) stays under the
      threshold.
    bb-reorder detail that mattered: a block ending in a call always takes
    its fallthru into the trace (find_traces_1_round's ends_in_call), so W
    keeps L after it however cold W is.
- 2026-10-22, applyIniOptions without a profile (started, paused by the
  user; nothing in src/ changed).  Goal: build options with gcc's guessed
  profile only, using dead-edge nudges (the `aio_never` trick works there
  too: profile_estimate runs while the dead tests still exist) to break the
  ties the crafted profile's bands break.  The user chose nudges over a
  natural-source-only search.
  - Tools: `python wip/aiog.py <cfg.json> <out.c>` turns src/app/options.c
    into a profile-free variant (pragmas and the crafted design's dead edges
    removed, options as OPTK with per-option form/expect hints, cfg as in
    wip/aiosearch.json).  `sh wip/aio/grun.sh <dir>` compiles `<dir>/a.c`
    without a profile and writes lab.txt/trl.txt/al.txt plus blk, fncmp,
    label-mismatch and padding counts (aldiag.py works on it too).
    wip/blk.py reads the original from git (56e988e) now.
  - Baseline: src as is, guessed: blk 155, fncmp 1404.  aiog with
    wip/aiosearch.json: blk 72, fncmp 892, lab 246, align-diffs 44.  Its
    traces match the FDO build's (wip/aio/t, the reference) up to round 2;
    the strip loop is 4523 there (2535 with the profile), so freq_max and
    the alignment threshold (45) differ too.  Round 3/4 starts tie between
    identical options; the FDO design gives each its own frequency
    (aiodesign.py bands), so a profile-free match needs about one nudge per
    trace start (roughly 40-60).
  - Nudge primitives: a dead exit (`if (dead) return;`) in front of a block
    lowers it and everything after it (the emptied test is removed as a
    forwarder, the block keeps its count).  A dead entry into a test block
    that merges into the next block raises that block.  Edge probabilities
    of real branches stay predictor values, so EDGE_FREQUENCY (priority
    keys, label alignment) only follows the source block's frequency.
    Predictor probabilities for the dead test (builtin-expect-probability
    83, measured): `if (v) return;` 61% (call 71 DS early-return 39), with
    expect 0: 17%, expect 1: 83%, `v > 0`: 80.9%, `v < 0`: 36.7%,
    `v == 3`: 37.8%, `if (v) goto out` (no return) 71%.  Products of these
    give the fractions.
  - Next: copy the FDO reference's round 3/4 trace-start frequencies
    (wip/aio/t/trl.txt) as targets, add nudges in source order and rebuild
    after each, checking the first trace that differs from the reference.

## app/bootloaders.c

Draft of the whole object, with string literals. All 19 functions match
and are built from `src/app/bootloaders.c`, which has no asm left: its
strings are `static const` arrays (`msg_*`) in the original's .rdata order
(built with `-fno-toplevel-reorder`); with literals, daeVerifySig,
fcrtVerifySig and cb/cd/ceDecrypt emit their error strings first.

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

Whole object in C now (no filelist_ini.s). The literal order gcc emits for parseIni
(expand-time block order) puts error strings before the code they follow in the
original, so its strings are `static const` arrays in the original's order, defined
before it and emitted in place by `-fno-toplevel-reorder` (`aligned(4)` from 31 bytes,
`aligned(1)` below: a user alignment stops gcc's array bump). validChars and
consoleNames are defined after loadUserIni (extern before) for the same reason.

Mixed since 17269c2; built from src/app/filelist_ini.c: getIniValue, memFindStr (4-arg,
`skipNul`), memFindChar, checkFileCase, loadUserIni (keep `iniSize + 1` in a local;
strings are `_fi_<addr>`), fixFileCase (`optimize("ira-region=one")`: regional IRA kept
&st in a register instead of dir; ira-region doesn't help any other function here).
- iniPreParse needs `-fno-tree-loop-vectorize` (with it on, PRE's eliminate drops the
  `PHI <'A', validChars[j+1]>` of the validChars loop), and validChars as C data ([0] is
  folded to 'A'). Built from src since the third 2026-10-21 session: the mixed C keeps a
  `static const` string copy of validChars (74 chars, so gcc emits `.ascii` with no NUL;
  a brace list gives `.byte`s, which re/splice.py refuses), split.py names the .s's
  label `_validChars`, and splice.py drops gcc's copy. Object flags in build.sh.
  - setne order (fixed): the original's loop body tests `'\n'` first and its ch2 header
    copy 0xff first. `&` operands sort by SSA version, the body keeps the source order
    and the copy takes names off the LIFO free list. So the source tests `'\n'` first,
    and a dead `if (i < 0) buf[0] = 1;` after the lines-to-strings loop (VRP1 drops it
    after release_ssa, before ch2; its freed .MEM name shifts the free list) puts the
    copy in 0xff-first order. An empty extra loop does the same but survives to RTL.
  - ebx: at RA time PRE's split-edge block for the not-`;` `i + 1` sits right after the
    `cmp ...,59` (split_edge_bb_loc puts it after the source when the join's previous
    block falls into the join), so the `;` block isn't in the compare's EBB and LRA
    can't inherit the reload of i into ebx. The original's `;` block must follow the
    compare. Tried: `continue`, `k = i + 1`, `else ;`, explicit increments (moves i to
    ebp, 146 lines), output-asm pins on &buf[i] and i (143), the LRA EBB probability
    cutoff param (no change).
- getters (getIniBool, iniBoolInvalid, getIniU32, iniU32Invalid): built from src since
  this commit. Own 2-arg helper `findKey(buf, key)` with global iniSize and `p = &buf[i]`;
  getIniBool returns `long`; myatol must be declared `char myatol(char)`. The q pin in
  findKey is `int d; __asm__("" : "=r"(d) : "b"(q)); if (d) __builtin_unreachable();`:
  with an output the asm isn't volatile, so it's no sched2 barrier (an input-only pin was,
  and luid put the `lea edx,[eax+esi]` before the reload of q); the unreachable keeps DCE
  from deleting it. The getters keep their `"b"(val)` pins. Worth trying wherever an
  input-only pin fixes RA but leaves a scheduling tie.
- DashLaunch (tmp/dashlaunch/iniparse.c, same as GitHub main) doesn't carry over:
  iniFindLabelOffset is case-insensitive (myatol + _strnicmp) and skips spaces/'=', the
  original search does neither. iniGetBool/iniGetDword-shaped getters (`if (found) {...}`,
  `&iniData[off]` per use, the out-param helper) give 25-78 lines (iniBuf reloaded after
  each call); its `j = sizeof(validChars) + 1` exit gives iniPreParse 36, its `while`
  comment loop no change.
- parseIni (409430-40aa10, 5.6 KB) drafted in wip/app/filelist_ini.c (from a Hex-Rays
  decompile; its tables/names are still `extern`). 486 of 1241 normalized lines equal
  (fncmp with full context, FNCMP_LITERALS=1), 549 with
  `--param max-jump-thread-duplication-stmts=12`. It has a jump table (L_4501e8); re/splice.py
  places gcc's tables at the .s's `#@J` markers, so it can join the mixed file once it
  matches (its strings need extern names or splice-dropped static copies). Findings:
  - Errors are `log; free(buf); return 0;` at each site (gcc crossjumps the tails), not
    a `goto fail`.
  - Build-name sprintf: one `sprintf(tmp, "<fmt>", xb.kernelStr, xb.outName)` per
    branch (crossjumped into one call; jtag's isn't, its nbl = 9 reuses the [version]
    loop's j == 9).
  - File loop: `e->type`/`e->offset` are assigned from locJtag/locDevk/... inside each
    build-type branch (separate loads per branch), and the switch re-reads `e->type`
    (the original's `cmp [ebx+1028],27` / `mov edx,[ebx+1028]`). A `loc` pointer picked
    by the branches gives a cmov and one shared load.
  - [rawpatch], [flashfs], [security] use `xb.rawPatch[i].name`, `xb.firmware[i]`,
    `xb.flashFiles[i]` directly, not a `name` pointer: `x[i][len] = 0` is `i*size+len`
    addressing in the original while the strncpy dest and the log use an IV pointer.
  - [security] sets noCrc/len in an if/else (jump threading then gives the original's
    two strncpy copies; the ternary gave a cmov). Ours still makes a third copy for the
    both-not-found path with len folded to -1; the original sends it to the crc copy.
  - bl section noCrc: the original keeps it in [esp+52] (shared with the return value:
    uncprop turns the return 0 after a noCrc test into noCrc) and doesn't thread its
    strncpy block. Ours has 13 statements there (dom2's limit is 15), so it threads;
    param 12 is the stand-in. The original's block must be bigger (or hold something
    that stops threading, e.g. a volatile asm).
  - The original re-reads `xb.files[blOrder[i]]` at each use (imul [edi],1068).
  - Register allocation: the original spills buf to [44] from the malloc on; ours gives
    it ebp in IRA's top region (same costs, so it's the competing pseudos).
    `-fno-tree-pre` gets [44] (and 618 lines), so some PRE redundancy in our source
    isn't in the original's. Declaration order doesn't matter (546-549 over 25 orders).
  - Version search: `ira-region=one` gives the original's `[buf+j+i]` addressing and buf
    in a spill slot, but the frame slots move ([32] vs [44]) and the total drops.
  - `python wip/skel.py <fn> [flags]`, a call/string/jump skeleton diff (ignores registers), shows block order and
    duplication differences much more clearly than fncmp's line diff here.

- 2026-10-21 session: parseIni 486 -> 866/1241 (wip draft). Fixes, in order of gain:
  `pos = pos + len + 1` (not `pos += len + 1`, which lets PRE make a len+1 PHI; this put
  buf in a spill slot and gave the 1180-byte frame); bl `if (len < 0)` error test after
  picking len (stops dom2 duplicating the strncpy block, gives the original's `js`);
  `if (!noCrc) {crc...} else crc = 0` in bl and [flashfs]; loop exits as
  `if (pos >= end) i = N;` instead of `break` (the original lays the exit as fallthrough);
  `flags & 7` as an if/else chain (5, 6, 7 order).
  Left: register allocation in the bl loop (IRA spills `i` for `pos`; the original keeps i
  in ebp and spills `i*4`; nbl starts in ebp in the original), comma/nul compare operand
  order in [rawpatch] (SSA-version tie: nul's PHI is created in vrp2 with a lower
  version), the bl trace (original: comma>nul block falls into strncpy) and cold-block order.
- iniPreParse: 15 more loop shapes tried this session (continue/else/do-while/while,
  explicit per-path increments, inner while); none moves the not-';' split block, still 11.

- Second 2026-10-21 session: parseIni 866 -> 1233/1241. Most of the gap was profile, not
  code shape; the IRA rotation and the bl-loop cold order fixed themselves once the block
  frequencies were right. In order:
  - `u32 noCrc` and a `u32` return: with int, uncprop turned the n == 0 path's PHI arg into
    noCrc (gimple_can_coalesce_p needs compatible types); the original keeps `xor ebx,ebx`.
  - `struct fileent files[19]` (padding keeps the offsets): the files loop's trip count is
    PRED_LOOP_ITERATIONS_GUESSED from the array bound (35 -> 97.2%); 19 (jtag's nFiles) puts
    the cold loc blocks among the bl blocks as in the original (18 is too cold).
  - label test `off < 0` (bl entry frequency), bl `len = comma; noCrc = 0; if (comma > nul)
    {...}` (the comma path's block placement).
  - [flashfs] and [security] each have their own not-found block. The shared `goto
    noFlashfs` meant the error block wasn't dominated by the security test, so only the
    found edge got PRED_CALL (found 62%); with its own block the two call predictions
    cancel (found 80%), which warms [security] enough for the original's cold order.
  - Dead stores `if (nul < -1) buf[0] = 1;` (flashfs loop) and `if (off < -1) buf[0] = 1;`
    (devk branch): their freed SSA names flip the comma/nul compare order in all three
    loops. Found with a greedy search (scratch hill.py: insert after every statement,
    keep the best, repeat); an uninitialised variable in the dead store works too but
    don't.
  - The `"S"(pos)` pin of the first pass isn't needed after the frequency fixes.
  Left (8 lines, all [flashfs]/[security] cold code; none moved by single dead stores,
  declaration order or loop-end forms):
  - [security] search: the original sets `i = 0` / `11` before the guard's `jle` and
    hoists `buf + i` (`lea esi,[ebp+edx]`); ours (and both [rawpatch] searches) compute
    `(buf + j) + i` in the inner loop. Probably range info splitting `(sizetype)(i + j)`.
  - [security] log: LRA keeps `xb.flashFiles[i]` in esi because the latch (`i++`, `+= 22`)
    is the log block's fallthrough at RA time (EBB); the original reloads into eax and
    later does `add [52],22`. GIMPLE order is log, latch, exit in both [flashfs] and
    [security].
  - Copy-order ties: flashfs `mov ebx,-1` / `xor edi,edi`, security `xor eax,eax` /
    `xor ebx,ebx` (PHI copies; declaration order moves the bl one, not these).
  - security crc-size error: crossjump shares `mov [4+esp],msg` with flashfs's error.
- Third 2026-10-21 session. Object flags for the draft are now `-O3 -fno-tree-loop-vectorize
  --param align-threshold=120` (re/progress.py WIP_FLAGS); the 10 built functions still
  JMATCH with them.
  - iniPreParse matches (fncmp and jcmp). The `;` block was never an EBB problem: the
    original's `mov ebx,eax` is LRA inheriting i from the `;` block (bb6) into the inner
    loop's preheader (bb8, EBB 6 7 8). Ours had no free register for it because LRA
    assigns the `&buf[i+1]` reload group (3 refs in bb6, freq 3*16 = 48) before the i
    inheritance group (2 refs in bb6 + 1 in bb8, 16+16+15 = 47), and the former took ebx.
    REG_FREQ is block freq / 10, floored, so bb6 162 -> 16, bb8 155 -> 15. A dead loop
    `for (j = 0; j < 18; j++) if (i < 0) buf[j] = 1;` at the top of the empty-lines loop
    body is estimated before VRP/DCE remove it and becomes the hottest block, scaling the
    profile so bb6/bb8 are 147/140 (both 14): the tie goes to the lower regno (i's group).
    K = 18 or 21 there; in the lines-to-strings loop it flips that loop's exit cmp.
    The memcpy block after `ret` is aligned in the original (77 > max/T needs T >= 117;
    T = 200 aligns too much), hence align-threshold 117-150.
  - parseIni 15 lines (fncmp count of +/- lines). [security]'s log reads `xb.flashCrc[i]`
    (no crc variable): out-of-SSA emits a block's constant PHI copies in reverse PHI order,
    and with crc's PHI created later (FRE) the n == 0 path is `xor eax,eax; xor ebx,ebx`.
    The same form in [flashfs] changes nothing (kept the crc variable there).
  Left:
  - [security] search guard: the original's `xor edx,edx; mov edi,11` before `test eax,eax`
    is ce3 if-conversion (find_if_case_1) speculating the preheader into the guard block,
    as it does for the body's `xor eax,eax` before `cmp ...,91`. Needs the preheader to end
    in a jump at ce3 (ours falls through into the header) and, by cheap_bb_rtx_cost_p with
    BRANCH_COST 3, a skip probability over ~54% for two insns (ours: REG_BR_PROB 300). So
    the original's guard had a very different probability. A hinted copy of memFindStr
    for [security] loses the CSE of size - 10 with [rawpatch]. Checked against this
    function's successful ce3 conversions (bb 151/207/267: fallthrough 28%, one insn).
    memFindStr is inlined at IPA, after parseIni's profile_estimate, so every inline
    copy starts with memFindStr's own 3%; an early `return -1` in memFindStr (plain or
    hinted) changes far more than the guard.
  - [security] log/latch (2 hunks): fixed with `--param
    lra-inheritance-ebb-probability-cutoff=60` (51-70; build.sh object flags): ours
    inherited the `[52]` reload into esi across the call because the latch is the log
    block's 50% fallthrough (EBB 321 322 323). Exit-likely hints, `break`/`continue` forms
    and latch clobber asms all changed other code. The other 10 C functions don't move.
  - [flashfs] len == 0 path: PHIs `_292 = PHI <len-1, -1>` and `noCrc_506 = PHI <.., 0>`
    in the block after the trailing-1/2 test, both from jump threading's update_ssa (order
    by old SSA version); the original has noCrc's copy first. Untried: shifting those
    versions with a dead store before the threading (single dead stores anywhere in
    parseIni don't, per a 1600-variant search).
  - security crc-size error: crossjump pairs it with [flashfs]'s same-message error (7-insn
    tail incl. `[4]=msg`) before the common error tail; in the original it joins the common
    tail at `[esp]=0`. Return block preds at jump2 start with the [security] error (bb318),
    so try_crossjump_bb pairs everything with it first (310 -> 318 splits it at `[esp]=0`,
    later 268 -> 318 matches 7). The pred order comes from earlier edge removals
    (unordered_remove moves the last pred into the hole). If-chain order and argument
    spellings of the [security] crc error don't change it.
  - Dead-store and dead-loop searches (all of parseIni, 5 variables / k-loops) with the
    current flags: nothing gets below 8 fncmp lines; the H3/H5 changes they find come
    with 30+ other lines.
- Fourth 2026-10-21 session (gcc 6.2 sources: cfgcleanup.c, ifcvt.c, ira-emit.c,
  cfgexpand.c).
  - Crossjump fixed (6 lines left): the [security] name-length error is `goto secName`
    to a block after `return 1`. try_crossjump_bb pairs (e, e2) only when e's block
    index is lower, and redirects e's block into a split of e2's. The return block's
    preds start [sec crc error, sec name error, ...] (outof_cfglayout moves them to
    the front), so with the name error first in the chain it was redirected into a
    split of the crc error, whose head then fell into the shared tail and later
    matched flashfs's `[4]=msg`. With the name error last, the crc error is the one
    redirected (its `[4]=msg` stays), as in the original.
  - Guard: the original's `xor edx,edx; mov edi,11` before `test` is find_if_case_2,
    not case 1, in ce1/ce2 (before IRA): the preheader is the guard's branch target
    (expand's jumpif, because the guard's GIMPLE next_bb isn't the preheader). Case 1
    can't apply (it needs skip probability > 54%). After that, outof_cfglayout must
    find the loop header right after the guard so it inverts the jump to `jle NF`;
    IRA's buf move then splits the fallthrough edge (its own block, `mov ebp,[44]`),
    and ce3 leaves it alone (case 1 needs a jump at its end). Our chain is
    [guard, preheader, header] (loopinit's split_edge_bb_loc), so the jump sense is
    `jle` from the start. `goto secSearch; secNF: <error> secSearch: off = ...; if (off
    == -1) goto secNF;` gets the chain [guard, NF, preheader, header]: ce2 converts,
    but NF stays between guard and header, so the jump stays `jg`, and ce3 then
    speculates the IRA block too (`mov ebp,[44]` before `test`, 6 lines, no other
    change). Fixed (2 lines left) by also moving [flashfs]'s identical not-found
    block (`goto noFlashfs`) after the [security] code: jump2 then crossjumps the
    whole [security] block into it (block index order), leaving a forwarder with
    the guard as its only pred, and try_simplify_condjump inverts the guard to
    `jle` into IRA's reload block (which follows the forwarder) before ce3 sees it.
  - PHI order (flashfs len == 0 path): single dead stores that fix it (e.g. `if (comma
    < -1)` after the [rawpatch] strncpy) flip the comma/nul compare ties in the bl,
    [rawpatch] and [security] loops. Greedy searches (scratch hill.py: best single
    insertion of `if (v < -1) buf[0] = 1;` per round) reach P fixed with 5 more stores
    but a flipped [version] exit compare (6 lines, before the goto changes), or 18 lines
    from the current draft.
  - jcmp shows three differences fncmp can't (they predate this session): [rawpatch]'s
    `pos = pos + n + 1` is `lea ebp,[ebx+ebp+1]` in the original (`[ebp+ebx+1]`
    ours; operand order is an encoding difference; `n + pos`, `pos + (n + 1)` don't
    help), and two [rawpatch] blocks get jump alignment in ours only: the nul-found
    block (`cmp bl,44`, freq 79) and the latch (`add edi,1`, branch 82) against
    freq_max 9120 / 120 = 76. The comma-found block (79) is aligned in both, by the
    prev_bb * 10 rule. So the original's [rawpatch] loop is relatively colder (or
    the nul-found block colder than the comma-found one); iniPreParse needs
    align-threshold >= 117, so the param can't do it.
  - The mixed build plumbing is ready (scratch patch, re-creatable): parseIni's data
    names are blJtag 44a020, blDevgl 44a044, blTestk 44a05c, blDevk 44a074, blRetail
    44a08c, locDevgl 44a0c0, locTestk 44a140, locDevk 44a1a0, locJtag 44a200,
    locRetail 44a2a0, fnNone 44a320, fnKvAlt 44a380, fnXellGg 44a3a0, fnXell2f 44a3c0,
    fnSmcConfig 44a400, fnFreeboot 44a420, fnFuses 44a440, fnPayload 44a460, blOrder
    479e84 (COMMON, so `extern int *blOrder`), consoleNames 450400 (its [0] is NULL;
    `extern const char *const consoleNames[8]`); strings as `static const char
    fi_<addr>[]` copies (memFindStr's strlen must fold). With those, parseIni from
    src differs only by the issues above.
- Fifth 2026-10-21 session: align-threshold back to the default (100).
  - parseIni's two [rawpatch] alignments can't come from its profile: block
    37 (multi-byte error, branch freq 77) is aligned and the nul-found block
    (79) and latch (82) aren't, so at any threshold the loop would have to be
    >= 4% colder relative to block 37, and every way of cooling it (prefetch
    on the found arm, dead early exits, split error tests, expects on the
    found test) moves IRA's spill slots (&tmp vs nbl rank) or downstream
    bbro by hundreds of lines. Even 1.5% does. With the default threshold
    (100; 100-111 work) all of parseIni's alignments match, so 120 was the
    stand-in: iniPreParse's memcpy block (77 vs max 8995) was the reason.
  - iniPreParse at 100: its block must be > 89. The bb8 -> memcpy edge
    (POSITIVE 73% with the memcpy call heuristic: 52.5%) can't rise: at 53%
    bbro lays the block inline. So the ';' test (NONEQUAL 28%) is
    `__builtin_expect(buf[i] == ';', 0)` with `builtin-expect-probability=65`
    (64-66 align it), and the dead loop's K = 44 (43-45) restores the spill
    slots and the ebx inheritance tie. All 11 functions JMATCH; the build
    reproduces the SHA.
  - parseIni matches (built from src since this session; 12 of 12). The
    lea order is combine's simplify_plus_minus sorting registers by pseudo
    number: [rawpatch]'s n is coalesced with its memFindChar loop's i,
    whose ch2 header-copy PHI took free-list name 11, so its partition
    (and pseudo) came before pos's. The [flashfs] PHI order and the
    [security] comma/nul compare are the same resource: one recycled name
    that dom3 (the compare's PHI) or vrp2's threading (the noCrc PHI)
    takes. `< -1` dead stores die in VRP1, too early to separate them; a
    `strcpy` to a dead local plus `if (strlen(t_) != 2)` survives until the
    strlen pass (between dom3 and vrp2) and frees names in that window.
    With it, greedy searches over single `< -1` stores (scratch hill.py,
    scored by jcmp's mnemonic-and-register diff, which fncmp's line count
    misses) fixed the rest. 10 dead statements in all.
  - Mixed plumbing: strings as `fi_<addr>` (four section labels static),
    data names in split.py (bl*, loc*, fn*, consoleNames, blOrder in
    common_bss).

## app/keys.c

Whole object in C since 2026-10-22 (no keys.s): `src/app/keys.c` is this
draft plus the key buffers' initial values, three functions' strings as
arrays in the original's order, and the original's function order
(shaCheck before crlEncrypt, daeEncrypt before fcrtEncrypt, shaHeader
last), built with `-fno-toplevel-reorder`.  wip/keysmixed.py (the mixed
build's generator) is gone; the notes below are the matching history.  Line counts
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

kvPrepare (built since 2026-10-22) has alt in ecx, saved around each call.
IRA only offers a call-clobbered register when its caller-save cost
(frequency of the calls crossed x save+restore) is below the memory
cost, and `improve_allocation` then takes a callee-saved one if spilling
its owner is cheaper; so the main path has to be colder than the
`else if` form makes it.  The size check is a separate `if` after the
0x3ff0 fix-up: profile_estimate runs before jump threading, so the 60%
error edge applies to both paths (main 4000 instead of 4823).  The
rest is bb-reorder and LRA (found by coordinate descent over structure
and hints, scratch harness `build/keys/kvgen.py`):
- `if (!checkZeros(buf, 16))` first: the original re-saves alt before
  the second checkZeros, so that block starts a new LRA EBB (a jump
  target at expand time); `__builtin_expect(..., 0)` makes the other arm
  the main trace.
- bb-reorder's exec thresholds are {500, 200, 50}‰ of the entry
  frequency; a block whose predecessor ends a trace gets priority in its
  round.  Hot labels are 85% DS predictors (cold labels are absolute,
  frequency 0); the C front end emits no `goto` predictor.  Hot labels on
  the "ok" arms of the 88-byte check and the hash check, one on the
  verifyExtended failure arm, and `if (__builtin_expect(!alt, 0))
  {kvSet ...} else ...` give the original's trace order (D, K, F, G, H)
  and LRA's spill-slot order ([56]/[60]; slots go to spilled pseudos by
  descending frequency).

cfPatchSlots and cfEncrypt (built since 2026-10-22): the slot index `i`
(u32, from 1) and the count `n` are separate variables, the last slot is
`if (over)` after a `over > 0x4000` loop (the original computes the last
index as `trips + 2` and n as `(trips + 1) + 1`, and cfEncrypt's copy
keeps the `over == 0` test).  n is `short` (cfPatchSlots returns short,
cfEncrypt u16 with a `short n`): a 16-bit add isn't CSE'd with the
index's, so the standalone's `lea edx,[2+eax]` / `add eax,2` pair comes
out.  No optimize attribute any more; `__builtin_expect(end > max, 1)`
orders cfEncrypt's two cold blocks.  The draft declares the external
prototype up top and puts `__attribute__((always_inline))` on its own
line before `inline short cfPatchSlots(` so keysmixed picks it up (its
`grep` of src for names misses `short`/`u16` functions: pass them).

- `daeEncrypt` (matched 2026-10-22): the 5-line version below kept a
  reload of off after the shared "success!" log.  LRA's inheritance EBB
  breaks at any block whose head is a label (lra_inheritance), so the
  original's save-without-restore means that block fell into its own
  copy of the encrypt code, which crossjumping merged into the main one
  after reload.  A source copy in the n path alone gave 8; in the n == 0
  path the copy's `n++` folds to `n = 1` and won't merge.  So both first
  attempts share one block: `if (!n) log(...)` before each decrypt lets
  gcc thread the n paths apart while the success block (with the copy)
  stays shared.  That gave 87 (a [56]/[60] spill slot swap in the n == 0
  alternate path); a cold label on the success block fixed it
  (scratchpad climb over hints and labels on this shape).  The pins stay.
  Earlier notes:
  `if (__builtin_expect(size, 1)) do { ... }
  while (off < size)`, `buf[off + k]` header tests with per-test hints,
  hot labels on the `n != 0` retry arm and the alternate-key arm, the
  second give-up path `goto fail` into the first's `n = 0; off = size + 1`.
  Two register pins: `__asm__("" : "+b"(off))` after the declarations
  makes the zero an ebx value live across malloc/memcpy (the original's
  `xor ebx,ebx` ... `mov edx,ebx`: off's parent allocno in ebx, the loop's
  in edx), and `__asm__("" :: "d"(off))` at the loop top keeps off in edx
  and buf in edi (IRA otherwise pops off first: it has strictly more uses).
  Found with `build/keys/daegen.py` (coordinate descent over loop form,
  header spelling, types/declaration order, pins and hints).  Left: the
  shared "success!" block (first-attempt success in both n paths) saves
  off to [44] and jumps past the encrypt block's own save; ours reloads
  edx and jumps to the save, so sched2 also mixes the save into the
  argument stores.  Making that block fall into daeEncryptOne
  (`goto ok` ... `ok: log_printf(...)` before it) changes too much.

## app/mode_update.c

The whole object is built from `src/app/mode_update.c` (no `.s` since
2026-10-22; `mode_update` from build.sh's profile compile, see the
2026-10-22 notes below). This draft, with string literals and statics, is
what `wip/mufdo.sh` experiments on; it is older than src (getBadBlocks there
still has the early return that needed `align-threshold=200`). Line counts
are `FNCMP_LITERALS=1 python re/fncmp.py wip/app/mode_update.c <name>`.

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
  `re/gcda.py` that reproduces the guessed profile exactly (no overrides:
  the same 30-line diff) with counts only for mode_update and updateNand.
  Overrides set single edge probabilities with no source change and leave
  getConsoleFiles' param alone: `mode_update:39>40=62` (the `-noreeb` match)
  gives 22, plus `updateNand:24>25=14.5` (writeImage error) gives **8**. Left
  is one swap: "avatar data skipped, no HDD detected" (updateNand 13>18) is
  placed right after the `-clean` arm instead of after the WARNING block.
  Moving 13>18 alone breaks others (18-28%: 28 lines, 30-36%: 8), and
  greedy single-edge and random 2-3-edge searches (`wip/mufdo_search.py`)
  over all two-way branches find nothing below 8.
  2026-10-21: in bbro numbering (profile build) the original's round-4
  order is `-clean` (46) then devkit strcat (90), WARNING (122), no-HDD
  (118), testkit strcat (94); ours at 8 lines is 118, 90, 122. Adding
  `updateNand:13>18=22 updateNand:19>20=60` (WARNING up to 3, no-HDD down
  to 2) gives 20 lines with 122, 90, 118: only devkit/WARNING swapped.
  WARNING can't pass netReboot (`20>22` over 50 flips that branch).
  On every config 90's tree (90[94]) is linked *under* the 118/122 node
  at an equal key, so it comes out after it. `python wip/fibwhatif.py
  <dump>` (event-driven what-if replay) finds no key change that gives
  the original's whole round-4 order: any 1-3 nodes by +-2, any 1-2 by
  +-4, any 4 of the 14 nearby nodes by +-2, dropping one insertion, or
  one phantom node at any time. A greedy search from the 20-line point
  and 400 random steps each from 8 and 20 (`wip/mufdo_search.py`) find
  nothing below 8. Swapping the hasHdd arms (no-HDD first) changes nothing.
  So the original's heap history differs from ours somewhere outside
  these blocks' keys (trace structure or CFG); edge or count overrides
  alone won't fix it.
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
- 2026-10-22: `mode_update` MATCHes with a crafted profile (overrides in
  `wip/mufdo.sh`'s header, 11 edges, no `-noreeb` override). How it was
  found: `python wip/fibsolve.py <bbro dump> [K]` searches the last STC
  round symbolically. The heap only compares keys, so each undetermined
  comparison branches (<, =, >) over a weak order of the round's small keys,
  pruned at the first extraction that breaks the original's trace order
  (`WANT`; `FLEX` are traces connect_traces attaches elsewhere, so their
  extraction time is free). Limited discrepancy search (K = comparisons
  unlike the dump's integers); `FIBD=n` keeps keys integers within n of the
  dump's (Bellman-Ford), `FIBALL=1` keeps going and prints fewest-change
  solutions, `FIBFIX=bb,..` pins keys. Exhaustive search without K never
  finishes; at K=4 it finds solutions in a minute. The no-HDD swap needs
  four key levels: devkit strcat > WARNING > no-HDD > testkit (ours has
  3, 2, 3, 2), which drags along retail/jtag/`%s_update`/nowrite-skip/argc<=0
  +1 and -clean at the guessed 4: 9 keys
  (`python wip/fibmin.py <dump> bb=key..` checks and shrinks a set). The
  argc<=0 block (`ip = dumpDir = NULL` before the loop) is entry x loop exit,
  so the loop exit must be above gcc's 2% PRED_LOOP_EXIT floor (2.1%; 2.14%,
  i.e. 15%/7 exits, fails; ours has 21 exits), and the other edges then
  hold the update tail at 9 (round 3's threshold is 10) and the parseIni
  failure at 7. The window is narrow (97.95 and 97.86 fail), so this is a fit
  to the layout, not the original's profile; no source for it is known.
  Tuning went fastest by building with `-fdump-rtl-bbro-details` and
  comparing the last two rounds' keys against the target set, not by fncmp
  line counts.
- Whole object (2026-10-22): one `-fbranch-probabilities` compile. Functions
  without counts in the `.gcda` are compiled as never executed, and counts
  for all of them change inlining (inlining checkBadBlocks/getBootloaders
  into getConsoleFiles needs -finline-small-functions, and with it the
  profile inlines getConsoleFiles into mode_update). So only mode_update and
  updateNand get counts, and the rest are
  `optimize("no-branch-probabilities", "no-reorder-functions")`: they keep
  the guessed profile (the attribute also stops getConsoleFiles inlining
  into mode_update, CIF_OPTIMIZATION_MISMATCH) and `.text` (without it the
  profile's callees go to `.text.hot`). `-fno-ipa-profile` keeps the hot
  test. The profile build aligns two more mode_update labels at
  align-threshold=200, so getBadBlocks is success-first (`if (list) {...
  return 1;}`): no early-return predictor, its error block at 6.7% (freq
  126) is aligned at the default. The variables are zero-initialized
  globals (extern-like aliasing, which updateGetFile needs) in .bss order,
  under -fno-toplevel-reorder. Strings are literals except where a
  function's literal order (its expand-time block order) differs from the
  original's: there the strings up to the last out-of-order one are arrays
  defined before the function, in address order (an array placed for a
  later function moves the earlier ones up, e.g. getSmc/getKv's, which come
  out with getSecurityFiles that inlines them). Found by inlining all and
  making the first mismatch (and its function's earlier strings) arrays until
  the order matched: 26 arrays.

## app/image_read.c

Draft of the whole object, with string literals. 27 of 33 functions are
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

remapBadBlocks: the inlined findFreeRemap drops its `numBad != 0` guard
only with `if (!xb.numBad) __builtin_unreachable();` before the call (VRP
keeps `numBad > i` symbolic for `u32 i`; `int i` flips the exit compare).
copyMmcImage returns `u32` (an `int` return reuses memcmp's 0) and has
`optimize("no-if-conversion")`, or ce1 hoists `ret = 1` above the branch.
irmixed takes an `__attribute__((…))` prefix on the definition line.
findAnchor: dom3 registers four threads through the second shaSelfCheck
(ok0 known x valid/invalid log) and keeps one per incoming edge, in an
order `unordered_remove` shuffles, so it can't keep both "valid" threads
the original has; an `__asm__("")` after the "invalid" log stops those
threads being registered. Then `u32 ok0, ok1` (int ok1 is reused for
`return 0`) and expects `(ok0, 1)`, `(!ok1, 1)`, `(ok1, 1)` (the sweep's
only full match; others leave the cold `!ok0 && ok1` copy unaligned).
`wip/jcmp.py` now treats an exe address against any .o addend as equal, so
it prints JMATCH for a real match.

Still off (fncmp lines):

- `getImageKv`: fncmp MATCHes with `__builtin_expect(…, 1)` on `size ==
  0x8000`, the first verifyExtended and the sanity test, at
  builtin-expect-probability 67-70 (no natural predictor gets the alt-KV
  success edge to 10% of entry). But jcmp shows the `size != 0x8000` exit
  jumps to the alt-success epilogue instead of the shared one after the
  "not sane" log, so the build differs by 4 bytes; not built yet. Without
  hints: 26. `python wip/kvsweep.py` sweeps hint subsets x probabilities
  with jcmp; a 3-hint sweep (56-94) was stopped before finishing. At the
  default probability (90, which findAnchor's hints need, and the param is
  object-wide) no subset of up to 4 hints matches; best is 12 lines
  (`size == 0x8000` and the alt verifyExtended, both 1). With jcmp fixed,
  a full 66-72 x up-to-3-hint sweep has no JMATCH; only the 3-hint set at
  67-70 fncmp-matches, and no fourth hint helps. bbro (P=68): STC round 2
  makes the return block (bb 18) its own trace before the "not sane" log
  (17), so connect_traces chains alt-success -> return and 17 gets the
  copy; the original has it the other way. Early-return shapes are worse.
- `getImageSmc` (117, was 163): `int addr`, `int size` and `!addr || (addr
  != 0x800 && addr != 0x1000)` give the two address registers (int for the
  logs, its unsigned twin for the checks and memcpy) and the layout. Left:
  the original's addr == 0 path prints a constant 0 (a phi copy on that
  edge, tails cross-jumped), and the bad-address path keeps its 0x1000
  copies on the size-test edges where ours are head-merged above the call
  (cfgcleanup try_head_merge_bb, after RA). if/else-if and separate `if
  (!addr)` forms, casts and types were worse.
- `showMobilePages` (45 fncmp lines, was 163). What got it there:
  `u32 page, end;` with the if-form align (page's PHI gets the lower SSA
  version, so the entry test is `cmp page,end`); `page << 9` in the loop's
  printf instead of an `off` IV (off goes to memory, page*528 to ebp);
  `optimize("no-tree-loop-ivcanon")` (ivcanon's counter changes the SSA
  names ivopts recycles, which flips the inner loop's `cmp ebx,esi`);
  `"a"(letter)`; and an opaque `lo` for len kept live past the add (sum in
  hi's esi). Left: the block before the loop. The original's cmov result
  is eax (`cmove eax,edi`), copied to edx, ebx and edi; the edx copy is
  split into edi around the log call (IRA gave a call-crossing page a
  call-clobbered reg), and page*528 is computed in edi then moved to ebp.
  Ours keeps one page in edi. Pins ("a"/"d"/"b"/"D" on page and off),
  expects, IRA/sched option attributes and other loop forms didn't get
  closer. Also the len spill store comes before `movzx edx,si` in ours.
- `loadDump` (~780): in progress; numPages is stored once from a `pages`
  variable; the name buffer and spill slots differ.
- `checkBlock` (200), `parseDump` (366): block layout not worked on yet.

listFlashFiles: load order `b16 = e->block; size = e->size; block =
SWAP16(b16); time = e->time;` keeps e in ebp (the other orders of the
three loads and the swap don't). fsGetFile: `int v = fsValid;
__asm__("" : : "S"(v));` (v is reused for `return 1`); it inlines fsFind,
so irmixed leaves fsFind without noinline (fsFindFile's call keeps it
emitted). scanMobiles: `off = page << 9` at the loop top, before the type
tests, so tree-sink moves it into spareVersion's inlined join (after lo,
before the high bytes; written after the call it lands after ver, before
the call above the tests); and `__builtin_expect(len & 0x8000, 1)` in the
older-version path puts the advance block after the found path's stores.

detectController: five code-free asm hints. `if (n > 1) __asm__("" :
"+a"(found))` (u32 found) puts found in eax outside the loop, so the two
`found = 0` edge copies head-merge into one `xor eax,eax` and the loop
entry stores eax (`"a"` alone lets the 0 be rematerialized as an immediate
store); `"b"(i)` at the loop top. IRA ties each LBA sum to its low byte
(lo in eax, lo2 in edx); an asm use of lo at the start of the else path,
and of lo2 before the second compare and at the start of its match
branch, keeps them live past the adds, so the sums take hi's register (ebp,
ecx) as in the original. Writing hi before lo, or `|`, `^`, casts and
`ira-algorithm=priority` didn't get there.

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

`clientBinPatch` matched (built): `const u8 *data` (the caller's `u8 *`
vs inlined patchNand's `const u8 *` kept them apart in out-of-SSA, so data
was copied into a second stack slot) and the memcpy/patchNand choice as
`switch (cinfo->nandSize) { default: patchNand; break; case 0x3000000:
memcpy; }` (the original's layout needs a 50% branch; `==` predicts 28%)
fix registers, slots and layout.  The last register (after patchNand's
512-byte loop LRA reloads `len - 512` into esi, gcc picked edi) is a tie in
LRA's `find_hard_regno_for_1`: no cost or preference separates esi and
edi, so it takes esi only if `lra_hard_reg_usage[esi] <= [edi]`.  Usage
counts hard-register references too, so before "Done!" two
`{ int r; __asm__ volatile("" : "=D"(r)); __asm__ volatile("" :: "D"(r)); }`
add four edi refs at that block's frequency (code-free; one pair is too
little, three refs flip a tail-copy reload instead).  That also flips the
earlier start/count reload pair (tfreq 372 each, start's thread first by
regno), which decides on the same esi-vs-edi comparison; an extra
`__asm__("" :: "r"(count))` before netWriteBlocks raises count's thread
frequency so it is assigned first and takes esi.  Read the order and
assignments in `-fdump-rtl-reload-details` ("Assigning to ... tfreq").
Expect sweeps (pairs over all 11 conditions, 55-95) never got below 8 lines.

Still off:

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
  - Parked by the user (2026-10-22): mode_client stays mixed, 15 of 16.
  - Whole object (2026-10-22): every other function matches when the draft
    is compiled as one file (client_usage and clientKeys included), and its
    `.rdata` string order is the original's except "failed!\n"
    (clientInfo) and "Unable to read file %s!" (filelist_ini's ordered
    string arrays fix those).  mode_client is the only blocker.
  - Best so far, 138 lines: the `goto fail` tail above plus 50% expects
    (param 50) on -bp, -wb, -eb, -e, -c, `mode && arg`, the switch-path
    `netConnect` and the trailing `if (reboot)`; found by a greedy search
    over every condition seeded with the notes' set.  Left: the `mode &&
    arg` false path should fall through (orig) but the switch path does,
    -bp/-wb's `a` register, one duplicated netDisconnect, and the cold
    block order at the end.  Other tail spellings (one netConnect, `goto
    done`, if/else flips) are 164-270.
  - Not getArgs at every option: the original's -bp reloads `argv[i + 1]`
    after storing i, which hand-written checks give and an inlined getArgs
    (a `static inline` copy) can't (after inlining `start` is a local
    argv can't point to).  The copy at -bp/-wb/-eb/-ip is 269 unhinted but
    worse than the hand-written form once hinted (needs -fno-ipa-icf: ICF
    folds getArgs into the copy and inlines -rb too).  A `pure` strnicmp
    (no PRED_CALL on the next-option edges) is 1072.
  - Crafted profile (`wip/mcfdo.py`, `wip/mcfdo_search.py`, re/gcda.py
    `--threshold`): mode_client's entry is < 1/1000 of the loop, so every
    block must be hot and the default threshold overflows the counts (ICE
    in create_edge); `--threshold=64` works.  NOPROF on clientEraseBlock
    stops its inlining into mode_client's case 10 (+63 lines), so it gets
    counts too.  With no overrides the profile build is 208 lines for the
    138-line hinted source: profile mode orders the cold switch cases and
    error blocks differently (not a count-resolution issue, thresholds
    64-8000 agree).  The greedy override search from the plain draft
    stopped at 273.  Compile from the same path as the instrumented
    compile: otherwise gcc drops the profile (`coverage-mismatch`), with
    no message when the .gcda is just missing.
  - 56 lines (2026-10-23, the draft; param 50): every block up to the
    round-4 (coldest) traces matches; only their order differs.  What got it:
    - Exit layout: gcc's ifcombine keeps the *outer* test's probability for
      `mode && arg`, and expand splits it (q/2, then (q/2)/(1-q/2) for the
      arg test).  The original's mode test falls into the arg test and that
      into the reboot path, so the combined test needs P <= 1/3: plain
      `mode && arg` (no expect) gets PRED_CALL's 29% (its then-block calls
      netConnect).  Ties in connect_traces go to the longer trace.
    - `if (!(mode && arg)) { reboot path } else { switch path }`: the
      inverted if makes the reboot path the RTL fall-through, which ends
      LRA's EBB there, so `mode` is reloaded (eax / ecx) instead of being
      inherited into esi across netConnect.
    - `fail: __attribute__((cold));` (both connects' shared error) and
      `rok: __attribute__((cold));` (reboot-path netGetInfo): the reboot
      test after the switch keeps netDisconnect in its own trace and the
      reboot-path getinfo/netReboot trace is created after it.  Label
      attributes are PRED_HOT_LABEL (85%) / PRED_COLD_LABEL predictors.
    - -bp/-wb `a` in ebp: IRA pushes allocnos by frequency; `a` (3 refs)
      beat the `(i + 1) * 4` temp (2 refs) and took edx.  Two
      `__asm__("" :: "r"((unsigned)(i + 1) * 4))` uses before the second
      argument load raise the temp (code-free).
    - -wb's `j = i + 1`: its int i+1 needs a second use, or TER folds it
      into the ifcombined `(j == argc) | !a` and expand emits `cmp edx,esi`.
      -bp's `j = i + 2; if (j == argc || !b ...)`: fold (at parse time,
      both operands simple) makes `(argc == j) | (b == 0)` in source order;
      `i + 2 == argc || !b` isn't simple and ifcombine puts `!b` first.
  - Round-4 order (left): the cold traces (error log blocks, usage calls,
    -ip/-r/-w/-e/-c/-i/-p) come out of bb-reorder's fibonacci heap with
    keys 0..-7, mostly tied, so their order depends on the whole heap
    history.  Our `client_usage(2, NULL)` (threaded entry edge, key -4)
    comes before the HDD errors (-2, half of case 4/5's 4), which the
    original has after them: in a min-heap that needs the HDD errors at
    <= -4 (cases 4/5 at 8+) or a colder usage(2).  Replaying our heap
    events (wip/fibsim.py, fibwhatif.py) with changed keys (scratch
    solvers: best-first, annealing, a realizability-bounded design search)
    reaches the original's first 21 traces at best, 12 with realizable
    bounds; no single hint or hint pair from greedy searches (expects on
    every option, labels on every cold block) improves the 56.  So the
    original's heap history (round-3 push order or keys) likely differs
    from ours.  A profile build (mcfdo.py) keeps the hot part matching
    (clientEraseBlock needs its entry count scaled by its call site, or
    case 10's inlined blocks get frequency 0), but the standalone
    clientEraseBlock and clientKeys (NOPROF breaks its dumpKey tie) then
    differ, so it would need mode_client spliced from a profile compile.

## app/net.c

Draft of the whole object (all 32 functions, data as statics). 30 match
and are built from `src/app/net.c` (mixed): netFree, netFindBeacon,
netTimerStart/End/Elapsed, netSendStr, netSendData, netCheckOk,
netOpenSocket, netClose, netDisconnect, netGetInfo, netDumpNand,
netGetBldrs, netGetBadBlocks, netReboot, netMount, netUnmount, netGetFile,
netReadBlocks, netFormatSysex/Compat, netWriteBlocks, netEraseBlock,
netMkdir, netSendFlash, netReadInfo, netSendFile, netRecvVerbose,
netConnect. `python wip/netmixed.py <fns>` makes the src file from the
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

Tools: `python wip/netmixed.py <fns>` lists the string SYMBOLS it uses (add
missing ones to split.py, and the function to C_FUNCS, then regenerate);
`sh wip/mixedcmp.sh app/net src/app/net.c good.o --param
builtin-expect-probability=65` compares the spliced object with a good
build's net.o including alignment (fncmp doesn't); `python wip/fnvar.py
wip/app/net.c <fn> <forms file> [attrs]` scores body variants (FLAGS for
the probability, CMPFN/GCCSYM for the netRecvVerbose clone).

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
  (ok is threaded away after profile_estimate). netInfo must stay
  `static` in the mixed file (netmixed.py keeps it once netReadInfo is in
  C; splice.py drops its .lcomm): as an extern, sched2 puts the `netInfo =
  info` store above the two `reserved` stores (`malloc` on netRecv's
  declaration also fixes that).
- netSendFile (wip only): `if (!name) return 0; if (!buf) return 0;` then
  a C99 `char cmd[264] = "SNDF";` at function scope (an inner block's cmd
  clobber gives the `!name` return its own PHI, so a second `xor eax,eax`
  block), no-crossjumping, and `__asm__("" : : "m"(buf))`: separate tests
  get the pointer heuristic, which puts buf's two uses just over IRA's
  memory-vs-callee-saved cost, so buf went to esi. The shared return-0
  block is `.p2align`ed in the original (compute_alignments: branch
  frequency > 4 x the fallthru from the send failure, align-loop-iterations;
  ours was 4750 vs 2190, the strlen loop's expansion halving the send
  block). `__builtin_expect(!name, 0)` with the object's
  `builtin-expect-probability` 55-65 (now 65, for netRecvVerbose) aligns it and changes nothing
  else; `!name || !buf` tests buf first and flips the send branch, and
  `--param align-loop-iterations=2` also aligns a netSendData block.
- netFindBeacon: `volatile u32 addr;` set to 0 after `socket()`. The
  original keeps addr in a stack slot, stored once and loaded on every
  return (even the socket-failure one), so it was a memory variable; with
  it in memory the setsockopt/bind/select-error paths, each written as
  `log; closesocket(s); return addr;`, crossjump into one tail and the
  timeout path keeps its own copy.
- netConnect: nested positive tests (every failure logs and falls through
  to one `return 0`), the socket code written out in each branch with a
  branch-local `struct sockaddr_in` (not netOpenSocket), and per branch
  `log; if (netReadInfo()) goto ok;` with `ok: return 1;` after the final
  `return 0`. Why each piece: phiopt and ce1 only leave the readinfo test
  alone if its failure edge goes to a block that isn't an empty forwarder
  (mergephi splits a shared forwarder for the test's edge), so the edge has
  to cross the branch scope's clobbers; those clobber blocks also collect
  every failure, so they reach RTL as the one `xor eax,eax` block. Each
  branch needs its own scope variable, else the two success edges share a
  block and ce2's find_if_case_2 (which speculates `eax = 1` above the
  test, moving readinfo's result to edx) needs a single-predecessor ELSE.
  With both copies speculated, jump2 crossjumps them (7 insns from the
  success log call), which is the label in the middle of the ip branch.
  `goto ok`: `if (x) return 1;` puts the success block right after the
  test, so the test falls through to it and case 2 doesn't apply; the
  return's finally copy for a goto lands after the branch. Early-return
  style (`return 0` per failure) gives uncprop a coalescable 0 (addr when
  the return is u32, WSAStartup's result when int) and loses the layout.

Open (diff lines from `re/fncmp.py`):

- netWritePatches 9 (4 without no-crossjumping/no-early-inlining, where
  only jump2's head merge of the two `mov eax,1` differs). With
  no-crossjumping the inlined netSendData's two failures reach the return
  through a block holding hdr's clobber, a different PHI edge from the
  send failure's, so they get their own `xor`. hdr shares rlen's stack slot
  in the original, so it really is the inlined netSendData. The head merge
  is try_head_merge_bb (needs single-pred successors that aren't df-dirty);
  an empty asm in the netEmpty branch stops it but breaks the threading.
  2026-10-21 (gcc 6.2 cfgcleanup.c, bb-reorder.c): the same unmerged pair
  of `mov eax,1` after `cmp r,netEmpty` is in all seven of netWriteBlocks,
  netEraseBlock, netSendFile, netFormatSysex/Compat, netMkdir and
  netWritePatches, and nowhere else in the exe, and our six matches all
  lean on no-crossjumping, so the original avoids the merge some common
  way. No tail form does (netFormatSysex: `return ret`, `ret = cond`,
  `if (!ret)`, explicit `r != &netEmpty`, nested ifs, free per path: 4-23
  lines with crossjumping on). One candidate mechanism: a dirty successor
  makes try_head_merge_bb return false and sets only block_was_dirty, not
  `changed`, so if no later iteration runs the merge is lost; csa (just
  before jump2) leaves the blocks it touches dirty. Not reproduced.
  Writing the free out as `if (r != &netEmpty) free(r); else if (ret)
  __asm__("");` stops the merge and leaves 7 lines: the free block's
  epilogue copy, because the written-out test gives the free path 62% of
  the failure block (204), under bbro's copy threshold (entry 2486 / 10 =
  248); netFree inlined late gives 81% (265). A late-inlined helper with
  the asm in netFree's else (53%), a netEmpty asm after netFree, and an
  asm in netFree itself (breaks 14 other functions) were worse.
  2026-10-23: without the attributes netWritePatches is 7 lines (the head
  merge and the free tail's epilogue copy). jump2's own trace: the head
  merge happens in iteration 1 at the netEmpty test T, before any
  crossjump, with both successors clean and single-predecessor. Ruled
  out: csa/dse2 leaving blocks dirty (csa changes nothing in these
  functions and calls df_analyze first); a jump block between T and the
  `eax=1` block (gimple_split_edge puts the split for T->return right
  after T whenever return's previous block falls into it, which every
  source order here does); -O2, -Os, -fno-tree-vrp/-dominator-opts,
  -fno-thread-jumps, -fno-tree-tail-merge/-pre (all worse); netCheckOk
  forms; block-scoped len/rlen (clobbers change the frame); nested
  positive tests; 15 tail spellings for netFormatSysex (all 4, the head
  merge). ce1/ce2 report IF-CASE-2 for T but don't convert it (T0 is
  converted), in the original too. Untested candidate: a dead insn in one
  successor in jump2's first try_optimize_cfg run, deleted by run_fast_dce
  after that run's crossjumps, so the second run sees a dirty successor
  and stops.
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
  2026-10-22, what the 13 lines are:
  - `*len = size` and the recomputed `cmp`: no-dom also turns off
    phi-only cprop, so a loop-closed `got_3 = PHI <got_44>` survives to
    RTL; cse's jump equivalence on `got_3 == size` then stores got, and
    the exit compare isn't the latch's. With dom on both are right (dom
    makes it `*len = got_44`, and cse's equivalence on the latch's own
    compare turns it back into size, `je` reusing the `jle` flags). So dom
    has to stay on; the problem is only the register rotation.
  - The rotation is IRA order, which follows pseudo numbers, which follow
    SSA versions. Into-SSA gives the loop PHI `got_1`; ch's header copy
    replaces it with a recycled name (`got_74`, freed by vrp1's asserts),
    so got's pseudo (r107) comes after size's (r98), got is one unsplit
    allocno colored first, and it takes ebx. With the loop's PHI kept
    (`got = 0; if (got < size) do { ... } while (got < size);`) got is
    r87, IRA splits it at the loop, and size/buf/got get ebx/esi/edi as in
    the original, with `*len = size` and the flag reuse right (28 lines).
    What's left there is layout: that explicit guard is predicted 73%
    (the header copy of a `while` gets the loop's 97%), and when dom
    threads its false path straight to the short-count log, the `got ==
    size` edge goes to 81%, so the tail flips; with the success test inside
    the guard (30 lines) the sense is right but the log block (freq 358 vs
    the while form's 186) starts its own trace before recv-fail's.
    `while (got < size) { do ... while (got < size); }` with
    `optimize("no-tree-ch")` also gets the registers (28: guard `cmp
    got,size`, tail at the end). Declaration order and FD_SET spellings
    change nothing. `__builtin_expect` can't help: the object's 65% is
    fixed by netSendFile.
  - `*len = 0`: sched2 issues `mov [edx],0` alone at t=3 (it waits only on
    the frame allocation's memory clobber; the stack stores wait a cycle
    for sp). The original issues it in insn order after `[60]=1` and
    before `[64]=sock`, as if it depended on the `[esp+44]` spill store
    only, i.e. RTL alias didn't know edx was the incoming pointer. Ours
    knows: `dx = ax` is the parameter set-up insn, before
    NOTE_INSN_FUNCTION_BEG, where find_base_value still takes an argument
    register's base. In the original the len pseudo was probably spilled
    whole and `mov edx,eax` is an LRA reload copy after the note (base
    unknown). So it is the same IRA difference again.
  - netRecv may be IPA-CP's `netRecvVerbose.constprop` (verbose 0): the
    local calling convention, the function order (the clone is emitted
    first, netRecvVerbose after netSendStr) and the 13 calls + 2 tail
    jumps to it all fit. Replacing netRecv with `#define netRecv(len)
    netRecvVerbose(len, 0)` makes gcc clone it, but the clone has the same
    rotation (54 lines); `FNCMP_GCCSYM=_netRecvVerbose.constprop.2`
    compares a clone. netRecvVerbose's own original keeps verbose in its
    stack slot and tv's address in ebp, unlike ours.
  - netRecvVerbose (built): `u32 verbose` (as an int, uncprop gives the
    non-verbose loop's `got = 0` the value of verbose, known 0 there, which
    keeps verbose in ebx; uncprop needs the two to be coalescable, i.e. the
    same type) and `__builtin_expect(verbose, 0)` on the "waiting for"
    printf with the object's probability at 65 (verbose path 29% -> 35%,
    so its loop's trace starts before the shared recv-failure block's).
    At 52-62 the hint matches fncmp but aligns the verbose `size <= 0`
    exit; hinting all five tests matches at 55-65 too, but then IPA-CP
    finds no benefit in cloning for verbose 0, so the single hint is the
    one consistent with netRecv being the clone. The original's loop is
    unswitched on verbose, as ours.
  - The clone (`#define netRecv(len) netRecvVerbose(len, 0)`, compare with
    `FNCMP_GCCSYM=_netRecvVerbose.constprop.2`) is netRecv except for the
    register rotation and the `*len = 0` slot (54 lines). The rotation is
    not pseudo order but a caller-save cost threshold: an allocno crossing
    calls keeps edx/ecx (and then gets colored late, leaving ebx to size)
    only while class cost + call freq x 8 stays under its memory cost
    (ira-costs.c, the ALLOCNO_CALL_FREQ adjustment; "N avail. regs" in the
    IRA dump: 1-6 below the threshold, 3-6 above). got sits right at it:
    the do-while form was 1984 vs ~1970, the clone 1904 vs ~1970. One more
    use of got on the short-count failure path (an empty `asm ("" : :
    "g"(got))` before its log) puts the clone over and leaves
    netRecvVerbose matching: the clone is then 6 lines, only the
    `*len = 0` slot. Uses in the loop (or at the success return, or after
    `got = 0`) also move netRecvVerbose's got, which sits just under the
    same threshold the other way; hints on the loop's error tests wreck
    it. What the original had there instead of the asm is unknown.
  - `*len = 0` slot: our `dx = ax` is LRA's inheritance rewrite of the
    parameter move (insn 2, before NOTE_INSN_FUNCTION_BEG), so alias
    analysis knows edx is the incoming pointer and sched2 issues the store
    at t=3 alone. Hiding len behind `asm ("" : "+r"(len))` makes the store
    wait (it then aliases only the alias-set-0 spill slot: points-to says
    *len can't be fds, and tv is long), which is the original's order, but
    loses the edx copy. So the original's `mov edx,eax` was probably a
    reload of the spilled len, not inherited, after the note, turned into a
    copy by postreload. bb2 is one EBB and nothing in it blocks
    inheritance in ours; the LRA/sched params tried don't change it.
    2026-10-22, the mechanism in gcc 6.2: init_alias_analysis seeds eax,
    edx and ecx with the argument base (FUNCTION_ARG_REGNO_P) and marks
    them seen; `edx = eax` keeps that base only while copying_arguments,
    i.e. before NOTE_INSN_FUNCTION_BEG in insn order (find_base_value
    returns 0 for a non-fixed hard reg after it, and record_set then drops
    edx's base). So the original's copy came after the note. LRA undoes an
    inheritance only if the inheritance pseudo is spilled (r156 got edx
    here), and in one block it always inherits, so the original reached
    LRA with something else: a block boundary between the parameter move
    and the store, or a separate pointer for the store. Entry-block
    spellings (explicit fd stores, winsock.h FD_SET, store orders,
    `len[0]`) change nothing. An asm-laundered copy just for the store
    (`int *l = len; asm ("" : "+r"(l)); *l = 0;`, or `"=r" : "0"`) puts
    the store in the original's slot, but leaves `mov eax,edx` in the clone
    (3 lines) and moves netRecvVerbose's `lea ebp` (2); earlier positions
    are worse (10/11), a volatile asm too (4/7). A register variable would
    give both functions the same register, but the originals differ (eax
    in netRecvVerbose's fresh load, edx in the clone's copy).
    2026-10-23: IRA spills len (r111) whole in the clone ("Popping
    a3(r111) -- spill"), so the entry `dx = ax` is LRA inheritance from
    the parameter store, not an allocation. If LRA reloaded instead
    (`dx = [esp+44]` at the store, after the note), postreload could turn
    it into `dx = ax` only while ax still holds len, i.e. with the store
    before the netSock load. Moving `*len = 0` first / after tv / after
    FD_ZERO: clone 7, netRecvVerbose 10. `asm ("" : : "g"(len))` at seven
    places (short-count, size == 0, success, both early failures, -1,
    after calloc): clone stays 6 at best.
- `-fno-tree-dominator-opts`, `-fno-if-conversion`, `-mbranch-cost=1`,
  `-O2`: none is better for the whole file.

## app/build.c

Draft of the whole object (all 41 functions). 27 match and are built
from `src/app/build.c` (mixed): findFileOffset, findFileSize, findFile,
readMetaFile, makeTimestamp, loadCommonFile, loadBinFile, loadLocalFile,
setFileData, iniRangeOk, raiseKernel, patchHeaderOpts, rotSumSha,
countBits, isUpdateBl, patchPayloadSize, showSmcConfig, blmodMissing,
patchFreeboot, encodeUpdateBls, logPowerButton, timestampToFileTime,
loadBaseFile, loadBaseFileMeta, loadFileCrc, extractSmcConfig,
verifyBlSigs. Switch tables go through
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
  with it inlined. Its out-of-line copy (called by loadInputFile) matches
  with two hints. The "reading %s (0x%x bytes)" block must reach
  bb-reorder's round 2 (frequency >= 2000 of 10000; it's 1102 unhinted),
  else it lands after the returns: `__builtin_expect(verbose, 1)` at
  probability 92-99 (build.sh's 95) gives 2095. Hints on the zero-size
  test raise it too but change the pad-path frequency that the inlined
  callers inherit (loadCommonFile breaks); verbose is constant 1 in every
  caller, so they don't see this hint. The out-of-line copy then has e
  and f swapped (esi/ebx): an `"S"(e)` pin in the pad-log block fixes it,
  and only loadCommonFile (e in esi already) keeps that block when
  inlined; a pin elsewhere moves the other callers' registers.
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
- checkBl: fncmp MATCH (2026-10-22, probability 98) but the link is 16
  bytes short: the original aligns the crc-failure (`bad`) block
  (`.p2align 4,,10`, so the next case block's padding goes too). Hints:
  hot label on the size error plus a guarded `cb_hint` call on the other
  edge (1.7% -> 19%, over the copy threshold), `__builtin_expect` on every
  `crc != c` (keeps `bad` under it), a `"D"(type)` pin. `bad` is aligned
  only as a "loop head" (it has a fallthru pred, the B case): needs
  branch freq > 4 x fallthru and their sum > 100 (1% of entry). Ours: only
  3 crc-fail edges branch there (others share tails), ratio 3, sum ~55;
  the switch default adds nothing (its block gets freq 0 at expand) but
  its 10% stale share makes `bad` > 1000 if crc fails are any likelier.
  A `(unsigned)(type - 5) > 16` pre-check (expect 0) instead of the
  default fixes the frequencies, but with 9 switch edges instead of 10
  the case-block ties (fibheap) come out in another order (18 lines);
  moving `case 12` last fixes that but loses a duplicated `crc == -1`
  test after the SE raiseKernel (2 lines). align-threshold /
  align-loop-iterations params would do it but move other functions'
  alignment. Earlier notes:
  structure right (the SE case's dead extra crc32 call is in
  the source); an `asm("" :: "a"(m))` on bl[0] gives the original's
  registers. Left: the original copies the epilogue into the size-error
  (-3) block, not the crc-failure one. In ours the -3 block is colder
  (call + negative-return heuristics, 1.7%) than the crc failure (20.8%).
  bb-reorder copies the 7-insn epilogue only over edges above the
  duplication threshold (10% of entry): so in the original the -3 edge
  is above it and the crc failure below, which needs other predictions
  on both (no negative-return on -3, no opcode-nonequal on `crc != c`?).
  The size check in a static helper returning 0/1 (IPA-inlined after
  checkBl's profile is estimated) does get the epilogue copied into -3,
  but -3 is then too hot (placed after the jump table) and `size` takes a
  register (119 lines). The crc failure can't drop below 10% by
  predictions alone: the switch default (`c = 0; goto bad`) brings ~8%.
- extractSmcConfig (matches, built from C; compare it
  in the mixed file, `MIXED_SRC=<draft> MIXED_OUT=<out> python wip/mixed.py`:
  the whole draft has callers, so fnsplit splits it and the inlined-back
  part renumbers SSA names). What each hint fixes:
  - Return value: with patchSmcConfig returning int, uncprop reuses its
    result for the no-patch `return 0` (`test eax,eax; je`). patchSmcConfig
    `u32` (and `u32 patched`, else its own regs change) keeps the PHI
    constant; ifcvt case 2 then hoists `ret = 0` above the test, as in the
    original (`mov edx,eax; xor eax,eax; test edx,edx`). That needs the
    patched block P below 1/3 of T (else bb-reorder's A-B-C rule makes P the
    fallthrough) and the no-patch edge under 98% (predictable -> no hoist).
  - The error string is the function's last .rdata string: `goto notfound`
    to a block after `return 0`. Its hot label makes T colder than the
    return block, so IRA gives ret eax (LRA saves it across P's calls,
    44-byte frame) instead of ebx/edx (the patch result's eax copy wins
    otherwise, with or without calls in P). A second hot label lowers P
    under the 10% duplication threshold (P ends `jmp`, no epilogue copy)
    while P still comes before the offset log (both 29% call heuristic).
  - Loops: bb-reorder's rotate_loop puts the most frequent exit last; the
    loop-exit heuristic gives both exits 4.5% and the bound exit wins on
    frequency. `__builtin_expect(i + N <= size, 1)` makes it 2%: the latch
    then sits before the cond (`jmp cond; latch: mov ebx,esi; cond:`).
  - `cmp next,size; ja`: forwprop folds every compare with the lower SSA
    version first. size's default def is made at loop 1's compare, before
    loop 2's temp, so loop 2 gets `size >= next`. `(void)&size` makes size
    addressable until update_address_taken, which then gives it a late
    version. (int/long/u32 combinations, casts, struct-by-value, pointer
    forms (`buf + i + N <= buf + size`: right order but signed `jg`), a
    PHI `next` variable and loop2 rewrites all fail.)
  - `"S"(i + 0x200), "D"(buf)` pin in loop 1: next/size/buf in esi/ebp/edi
    (IRA pops size before next otherwise).
  - `__builtin_expect(size - i >= 0x400, 1)`: the extract memcpy's shape.
  - The extract memcpy's dst/temp (eax/edx, built from C 2026-10-23):
    `__asm__("" : "+r"(src) : "r"(buf))` on a `src = buf + i` local. Without
    it the raw loop's src IV (eax) leaves an (eax, 1) cost record on buf
    via their shuffle copy; gcc 6.2's `restore_costs_from_copies` calls
    `update_costs_from_allocno` with decr_p true, so the "restore" replays
    it, the extract src (in buf's thread) gets eax -2 and dst, which
    conflicts with it, eax +2 -> edx. buf live past `buf + i` removes the
    extract src's copy to buf. An input-only pin is volatile, a scheduling
    barrier (2 lines); a `"+a"` dst pin leaves a dead spill store.
  The raw branch is success-first (`else if (size - i >= 0x4200)`): .rdata
  has "raw" before the error.
- appendAddonPatches (18): positive-condition nesting fixed most of it;
  the "not enough room" log and `size -= 4` blocks go after the return in
  the original. They are separate round-1 traces, ordered by frequency:
  room 1615 (both arms call, 50%), `size -= 4` 905 (`== 0xffffffff`,
  28%), the post-loop 900. The original has both below the post-loop.
  An `if (xb.nAddons > 0)` guard fixes `size -= 4` but hoists `added = 0`
  (15 lines); `continue` is a 50% predictor in gcc 6, no help. The draft's
  `if (xb.nAddons)` guard is a fncmp MATCH, but the link differs in one
  byte: the room check is `lea edx,[esi+eax]` (size + a->size) in the
  original, `[eax+esi]` in ours (fncmp doesn't see lea operand order).
  PRE's elimination refolds `prephitmp + size` with the lower SSA version
  first; with the guard, ch2 renames size's PHI (size_76) and frees the old
  header PHI names, which PRE reuses (prephitmp_5), so size comes second.
  Without the guard PRE got a fresh name (pretmp_77 > size_71) and the
  order was right. A guarded do-while (no ch) gets the order right but
  hoists `added = 0` above the test and tests `je` (5 lines); with a `> 0`
  guard it's `jle` but opcode-positive moves the room log again. ~300
  combinations of equivalent spellings (in and around the loop) all keep
  `[eax+esi]`.
- logPowerButton: fncmp can't tell its identically shaped log blocks
  apart, so check the string order in the link. The original's .rdata
  string order is gcc's expand order, i.e. source order: cases 0x59, 0x58,
  0x5a, 0x56, 0x57 after 0x55, each `if ((xb.flags & 7) > 4)` first. The
  case order sets the bb-reorder ties of the three outlined arms.
- fixupPatchSet (71): the original's copy (n == 2) is the loop's hot
  fallthrough and the record parsing goes after the return. Ours had the
  loop-exit heuristic on `n == 2` (4.5%). Now (2026-10-22) `if (n != 2)
  { parse; continue; }` (PRED_CONTINUE bypasses the loop-exit heuristic, 51%)
  plus a hot label on the copy, and `v = getBeU32(p + off); off += 4;`
  first (the original computes off + 4 once for both arms): layout matches.
  Left: registers. Five values live in the loop (p, n, off, e, findFile's
  index); the original spills off, ours spills n. Pins ("D"(n), "b"(p),
  "S"(e)), an "m"(off) operand and the index form (`xb.files[f]`) move the
  spill elsewhere but not to off. -fno-tree-ch isn't it: pass_ch doesn't
  copy this loop in ours either.
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
- verifyBlSigs (matches, built from C): a switch with SC/SD before SE (gcc orders bit-test
  clusters by case count, then label number; 12..13 counts as one range).
  The .rdata strings give the nesting (2026-10-22): each case tests the
  positive condition first (`if (pub1bl)`, `if (sb)`, `if (xb.prvKey)`,
  `if (sd)`) and the sign/resign results are `if (!blSign(...)) fail; else
  ok` (failure strings come first). No early `nFiles <= 1` return: that's
  the loop guard (it stores ok = 1 and joins the common exit). blCheckHash
  declared u32 so the inlined findFile(11) counts from its 0 result.
  The cold-trace order comes from the loop's guessed trip count, i.e. the
  `xb.files` bound: `files[19]` plus padding (as in filelist_ini.c) puts
  the exit at ~5% instead of 2.9% (`files[35]`), raising the entry
  frequency and so the bb-reorder round thresholds (entry x 500/200/50
  per mille); only p ~0.05-0.055 works. A pointer IV (no bound) gives 62
  lines. The `i = 1` / `ok = 1` preheader store order follows declaration
  order (`ok` declared first). The struct change leaves every other C
  function unchanged; it may also move loadBlFiles/loadConsoleBlFiles
  loop frequencies (the loadInputFile clone).
- patchSmcConfig (10): two cold blocks (gpu/cpu fan warnings) in the
  other order; the gpu warning passes no argument (the cpu one does).
  Its string is after the function's last ones in .rdata, so its block is
  last at expand; a `goto` to a block after the return reproduces the
  string order, but not the layout. The two traces tie (keys -1035148)
  and come out of the fibheap in the other order. The tied blocks are the
  inlined iniRangeOk "out of range" logs (cpu bb23, gpu bb30, round 3);
  ties pop LIFO, and their insertion order comes from the round-2 tie of
  the cpu/gpu range tests (22, 29), itself from hot-path order. A
  string after the function's others means the original's gpu warning
  block is a jump-threading copy (copies go at the end of the CFG), so
  that block must end in a test on a local that every path into it
  knows, which then disappears; our draft has no such test (vrp2 only
  copies the reload tests). Arm order, nesting, `== 0` forms and
  `__builtin_expect` on the warning tests change nothing; expects on the
  outer `!= 0xffffffff` tests break the hot layout. In the link the
  whole gpu pair (range log + warning) comes before the cpu pair. Breaking
  the tie needs the gpu range-fail path hotter without making gpu's ok
  block (`[18+esi]`, also a LIFO tie, already right) colder than cpu's, so
  only the outer test can carry it. Tried (2026-10-22, probability 98):
  hot/cold labels on the outer arms (85%, 46-78 lines), a guarded hint
  call in the gpu ok arm (log order right, ok blocks swap: 8 lines), in
  the outer else (100+ lines), `ok = iniRangeOk(); ...` threading forms
  (10-35 lines). With no-early-inlining, iniRangeOk is a call heading both
  outer arms, so PRED_CALL stays symmetric. 2026-10-23: returns u32 now
  (extractSmcConfig's uncprop, above; still 10). Also no change: the gpu
  warning in an inlined static helper (inlined blocks don't go to the end
  of the CFG; the string stays in source order), and cpu outer-test
  spellings (`+ 1 != 0`, `!(== -1)`, `(int) != -1`, `< 0xffffffff` all
  fold back to `!= -1`).
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

The 41 matching functions build from `src/app/image_write.c`, a mixed
object made by `python wip/mixed.py app/image_write <fns>` (its OBJS entry
turns the draft's `copyright` and `mobileOffset` definitions into
externs; the `.s` keeps the data). imgWriteAt (0x40eef0) is gcc's ipa-cp
clone of imgAdd for type 0, pad 1, built as `_imgAdd.constprop.2`: the
src file carries imgAdd's and imgAddFile's bodies (OBJS `inline`; both
still asm, so splice.py drops gcc's copies) so that their calls and
writeInitialHeader's netKd calls make the clone, and with the off
argument varying (imgAddFile) it stays a parameter. The clone needs `u32
b` for the block loop (with `int b` VRP2 leaves the peel's third test
`> 3`), but imgAdd itself is 88/78 with `u32 b` and 21/19 with `int b`,
so the body is still not the original's. Draft of the whole object (IDA pseudocode: `build/decomp_13.txt`, made with
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
- imgWritePage builds from C (2026-10-23) with empty-asm pins: `"S"(off +
  0x1000)` before the `x` pin (head registers), `"S"(start + blocks),
  "a"(start * 512)` before the block loop (start reloaded straight into
  the IV's ebp), and the end marker as `x = ~xb.fsStart; __asm__("" :
  "+a"(x)); fsTable[(int)(x + start) + (int)blocks]`. The pin ties the
  not to the add's output; the signed sum keeps reassoc from pairing
  `start + blocks` in gimple (DOM would then use the IV's exit value), so
  RTL CSE finds the spilled loop bound, as in the original. Each pin is
  needed.
- imgAddMobile: big block path first, error path duplicated (crossjumped),
  small path `if (imgFits) {...; return ret;}`. Left (18 lines): the
  "mobileOffset already set" block's placement.

Still off:
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
- imgWritePage (history; it matches now, see above) (17 lines, 7 normalised): `x = off & 0x3fff;
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
- imgWritePage (history, 17): two RA spots. (1) After the memcpy the original
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
- writeInitialHeader builds from C (2026-10-21). Why imgWriteStart never
  inlined: i386 promotes prototyped u16 arguments, so the call's jump
  function is an int constant while the `next != 0xf1f1` predicate is on
  the 16-bit parameter; evaluate_conditions_for_known_args drops
  conditions whose operand size differs, so the 0xf1f1 and 0x1ffb calls
  get the same estimate (65). The big-block call goes to imgWriteHdr, a
  static copy without the FS table that only it calls, so it inlines as a
  called-once function. An exact copy gets merged back by ICF. Three more
  things were needed:
  - The bigBlock arm writes `s->b0 = 0xff` and the other arm writes
    `*(u8 *)s = block`. With both spelled `s->b0`, cselim sinks the pair
    to the join and b0 is stored after byte 1.
  - The inner loop runs over absolute page numbers, `(start + b) * 32`
    up to `(start + b + 1) * 32`. Only fncmp can't see why: with a known
    32-trip inner loop under the guessed outer loop, the inlined loop is
    156x the entry, so the 0x1ffb call block falls under align-threshold
    and loses its `.p2align`. With a 32-trip loop and a constant length
    it is 14x and the netKd block gains one. The original sits in
    between (35-50x); a guessed inner trip count lands there.
    Hot/cold labels can't tune it, since loop-iteration predictions are
    first-match and outrank the label predictions.
  - imgWriteHdr has no labels and the plain ternary tail; the smaller
    "just the header" versions (no outer loop, or a constant length)
    change the block order.
- imgWritePage's tail (`mov eax,ecx; not eax; add eax,[end]`): expand
  substitutes (TER) the single-use `~fsStart` into the sum, and
  simplify_plus_minus sorts the plus operands by regno. The new not
  register comes last, so the add is tied to `end`. With -fno-tree-ter
  the not is tied, as in the original, but the sum is split into
  `+start +blocks`. The original needs gimple `_86 = ~fs + end` with
  `end` being the spilled loop bound. With an `"S"(start + blocks)` asm
  pin before the loop (13 lines), the pin also gets `start` reloaded
  straight into ebp, but dom3 replaces `end` in the tail with the IV's
  exit value (`lea eax,[ebp+ecx]`). Asm outputs on `end` and
  loop forms over `start..start+blocks` (guard) are worse.
- imgWriteAt (2026-10-23): 249 -> 48 normalised lines (152 raw). What
  each piece does:
  - `first = (off & 0x3fff) ? 0x4000 - (int)(off & 0x3fff) : 0`: the int
    cast keeps uncprop from putting x (known 0 on that edge) in the PHI,
    so the cmove takes a literal 0 (`mov edi,0`) as in the original.
  - `if (off & 0x3fff) blocks++` (not `if (first)`): the original tests x.
  - `int b` (spare loop): ivopts then compares `blocks > b`
    (`cmp [28],eax; ja`); with u32 b it is `b < blocks`.
  - `__asm__("" :: "g"(next))` before the imgEnd store: emits nothing,
    but the extra reference puts next before start in LRA's spill slots
    ([32]/[36]); LRA orders slots by reference frequency, then regno, and
    next is a late (parameter) pseudo. `"m"` keeps next in its incoming
    slot instead; other spots move the RA.
  - FS loop with its own counter `i`, the range check as `xb.rawSize <
    off || xb.rawSize < off + len`.
  Left: the tail. The original has `rem < 0x4000 ? rem : rem % 0x4000`
  (cmovb), but as a plain function that ternary threads differently and
  lays out `len <= first` hot; `rem % 0x4000` is what the draft has (no
  cmovb). The ternary does lay out right when the body is a `static
  inline` helper that imgWriteAt calls (IPA-inlined, so its CFG/SSA come
  from the helper; 196/52 with the pieces above), but then the inlined
  SSA numbering canonicalises the range check to `off > raw` (`ja`).
  Also left in both: the chain loop's preheader (the original recomputes
  `start - fs` for the 16-bit chain value), the vector peel's `== 3`
  (ours: `> 3`, VRP knows blocks >= 1 there; the original doesn't), and
  the order of the cold peel exits. Labels, statement order, the `rem`/
  `first` temporaries, `>>`/`/` spellings, loop forms and counter types
  were searched (scratch cv.py coordinate descent) without gains.
- imgWriteAt and imgWriteStart look like gcc IPA-CP clones of imgAdd
  (2026-10-23): imgAdd(off, src, len, type 0, next, pad 1), and the same
  with off 0. With type 0 every type/partial test in imgAdd folds away
  and `pad == 1` leaves `if (tail) memset`, i.e. imgWriteAt; the original
  imgAdd's head and FS-table code (vector peel included) are imgWriteAt's.
  It explains what no standalone spelling could: a clone gets its CFG
  and edge order from copying (like an inlined body, so the head lays out
  like the original), but its SSA names are made lazily in statement
  order (so the range check stays `raw < off`, as in a plain function).
  With imgWriteAt's calls rewritten to imgAdd(..., 0, next, 1), the
  clone `_imgAdd.constprop.2` reproduces the original's first 26
  instructions, registers included, with no pins (wip/app/
  image_write_clone.c, 68 normalised lines). The pipeline can take it:
  splice.py already drops gcc's copy of a function the .s keeps in asm,
  so the C file can carry imgAdd's body only for its clone, and SYMBOLS
  can name 0x40eef0 `_imgAdd.constprop.N` (cf. `_baseFileExists.part.0`).
  The off-0 clone (imgWriteStart) appears only with `--param
  ipa-cp-eval-threshold=100` (then 211/67 from the old imgAdd draft), so
  imgAdd's real body must make that specialisation worth more.
  Pieces found for imgAdd: `int b` counter loop over blocks with the LBA
  `start + b` (the generic imgAdd's ivopts turns it into the original's
  absolute `[64]`/`[76]` `jne` loop), `int i` for the FS loop, the
  memset under `pad == 1 && tail`-style threading (the original sets `bl
  = pad == 1` on tail != 0 paths), the page counts as `npages = len /
  512; if (len % 512) npages = (len + 512) / 512;` and `pages = len / 512
  + (len % 512 != 0);` (two cmoves, as in the original).
  Left in the clone: the original threads `tail` through every path (4
  memcpy copies), ours merges the x != 0 paths and re-tests tail; the
  spare loop keeps only the absolute IV (the original clone keeps the
  0-based counter, as the standalone version does: same IV candidates,
  found in a different order, so ivopts breaks ties differently); the
  vector peel (6 tests vs 5) and cold order.
  Standalone best for comparison (scratch, not in the draft): imgWriteAt
  as a wrapper around a `static inline` body taking `xb.rawSize` as a
  parameter (fixes the compare order) with `__asm__("" :: "b"(len),
  "d"(src))` after the range check: 121 raw / 45 normalised. Its last
  differences come from VRP: the spare loop's exit assertion grows
  `blocks`' range one step per visit, so the peel counter's PHI is
  widened and one `!= 3` test stays `> 3` (`jbe`).
- imgWriteStart: the same `"g"(next)` reference before imgEnd, 60 -> 58.
  Calling a static inline body copy estimated with off unknown (as
  above) gives the original's head order (len == 0, len <= 0x3fff and
  tail cold) but the range check's `cmp [raw],len` operand order needs
  imgWriteStart's own SSA numbering (raw loaded before len's default
  def is created), so the draft keeps its own body.
- tmp/xeBuild64 decompiles with IDA (idapro on a copy of the ELF):
  imgWriteStart 41b1b0, imgWritePage 41b3b0, imgWriteAt 41b5c0,
  buildImage 41b810, imgAdd 41c960, imgAddFile 41ce20. Older source;
  structure only.
- imgAdd rebuilt (2026-10-23, wip/app/image_write_clone.c): 21 raw /
  19 normalised lines, and its imgWriteAt clone 11/11. What each piece
  does:
  - The page counts, `partial`, `sp9`, `left` and the page count
    selection are computed inside the block loop (LIM
    hoists them). With them before the loop the `len <= first` path
    shares the memcpy block with the others; inside the loop jump
    threading gives it its own memcpy copy and jumpy `pad == 1`, `len`
    tests (blocks = 1 there decides the loop guard), as in the original.
    The selection before p's computation puts the partial test
    at the loop head, with the !partial, type-out-of-range path threaded
    to `end = 32, p = 0`.
  - Variables are reused, which matters through TER: TER won't forward
    an expression into a statement that redefines the same user
    variable. `if (!partial) npages = 32;` (then `end = p + npages`)
    keeps npages' cmov at its definition, right after the `len & 511`
    test, instead of at its single use; `left = pages; if (left & 3)
    left = (left + 4) & ~3;` keeps the `(pages + 4) & ~3` arm early
    while the cmov is forwarded into s[9]'s computation. Both as in the
    original (and `type` then lands in esi, as in the original).
  - `off & 0x1ffff` is written at each use (p's computation and the
    bigBlock s[9]) rather than kept in an `o128` variable, and `sp9 =
    32 - pages` is computed in the loop body (removing it as dead code,
    with `32 - pages` inline, changes SSA numbering: 25 -> 222 lines).
  - `if (len % 512) { npages = (len + 512) / 512; pages = len / 512 + 1;
    } else { pages = npages = len / 512; }`: npages' PHI first.
  - `first = x ? 0x4000 - x : 0` without the `(int)` cast: with it PRE
    makes a new name for first and the compare becomes `cmp [len],first`.
  - `if (pad == 1) if (tail)` (nested), `if (type != 0x2a && type !=
    0x2c)` for the bigBlock spare bytes (the 42/44 arm second), `partial
    = type != 0 && type != '0' && len < 0x4000`, `pages`/`npages` from
    one `if (len % 512)`, no labels and no `"g"(next)` asm.
  - `u32 i` for the FS-table loop: the vector peel then matches in
    imgAdd, and the clone keeps only the `== 3` / `> 3` test and its
    exit blocks.
  Left in imgAdd: `type - '1'` comes first in the original's setup
  block (ours is LIM'd after the left arm), the original re-tests `len &
  511` for pages' cmov (`test ebx,ebx`, ebx then reused for `len >> 8`),
  and `len >> 8` / `(type - 42) & ~2` come before the left arm.
  `t1 = type - '1'` anywhere in the loop body changes nothing (forwprop
  folds it into the compare). Left in the clone: VRP2 evaluates the
  peel's `> 3` assert chain while `blocks`' range is still growing (the
  block loop's exit assertion `blocks <= b`), the chain collapses to
  VARYING and the `== 3` test stays `> 3`; no equivalent spelling of
  the FS-table or block loop code changed that.
