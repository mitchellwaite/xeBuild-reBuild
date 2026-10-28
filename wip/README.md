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
  - 2026-10-20, checked against gcc 6.2's bb-reorder.c (official GCC
    repo, tag `releases/gcc-6.2.0`; see CLAUDE.md).  The perbox test is exactly 50/50
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

Draft of the whole object, with string literals. All 33 functions match;
`src/app/image_read.c` is the whole object (no `.s`), made from this file
by `python wip/irwhole.py` and built with `-fno-toplevel-reorder`: the
strings become `static const char ir_<address>[]` arrays, each defined
before the first function whose part of .rdata it lies in, and the
variables go in the original's .data/.bss order. The history below is
from when the object was mixed (`wip/irmixed.py`, removed). Compare with
the strings as those names (`wip/ircmp.py` does), not with
`FNCMP_LITERALS=1`: two cold blocks that differ only in their string
look the same to the literal mode (getImageMobiles "matched" that way with
its two allocation-failure blocks swapped). `wip/irlit.py`'s `externize()`
turns the draft into that form.

The statics that a C function writes (fsBuf, fsValid, fsOffset, anchor,
mobiles) stay `static` in the mixed file and `re/splice.py` drops their
`.lcomm`, so the alias analysis is the original's (as externs, memcpy
clobbers fsOffset and loadFlashFile reloads it). dumpSize stays extern
(it used to be written only by the .s's code, and as a static gcc would
think it is always 0; loadDump, which writes it, matches with it extern).

When all 33 match, `python wip/irwhole.py` makes the whole-object
`src/app/image_read.c` (no .s, `-fno-toplevel-reorder`): each string becomes
a `static const char ir_<addr>[]` array before the first function that uses
it (aligned 4 from 31 bytes, else 1), and the variables go in the
original's order; it checks every string's address. Tested on the 27 built
functions: .rdata strings and .bss come out at the original's offsets and
all 27 still match. Not yet checked: .data is 0x1c bytes against the .s's
0x20 (maybe only padding before the next object).

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

Matched 2026-10-26 (four parallel agents; `python wip/ircmp.py <draft>
<name> [flags]` runs fncmp and jcmp with the strings externized, and is safe
to run in parallel):

- `getImageKv`, no hints: the alt-KV part comes after the whole first-KV
  if/else as `if (ok && size == 0x8000)`, with `ok` (0 at entry) the first
  verifyExtended result. Branch probabilities are guessed (profile_estimate)
  before jump threading, while that join still exists: the kv-fail and
  alloc-fail blocks fall into the `ok` test, not into the return, so the
  early-return heuristic doesn't fire on their edges, and the sanity test
  comes out at exactly 50/50 (both arms call). STC round 1 then builds
  [not-sane log, return] first, the return block belongs to that trace, and
  connect_traces gives the alt-success, kv-fail and alt-fail ends their own
  epilogue copies, as in the original. VRP/DOM thread the `ok` tests away
  later (ok is 0 on every failure path), so the final CFG is the nested one
  with the original's frequencies. No expect-hint set on the nested shape
  can do this. A block before the return that needs exactly 50% is a cue
  for this kind of shape (natural prediction only).
- `checkBlock`: -1 is lba's initial value and the ECC check is guarded by
  `if (lba != -1)`, so the bad-block exits don't reach the return as
  negative constants (the negative-return predictor would make them 4%);
  they get the opcode heuristic (72%) and DOM/VRP thread them past the
  guard, and ce1 (find_if_case_2) hoists `esi = -1` above each pad test
  (head-merged into one copy before the bigBlock test). -6 is assigned in
  each bbController arm (`if (block && block == other) lba = -6; else lba
  = ...`) with the range checks under `if (lba != -6)`: -6 in the small
  block's lba PHI stops VRP folding `lba > 0`'s false edge to 0 (the big
  block's lba is >= 0, so there the 0 is a real singleton, `xor esi,esi`;
  needs `lba > 0`, not `lba &&`). Order `if (xb.bigBlock)` first, then
  `else if (!xb.muChecked) {warning} else {...}`. The original loads b[513]
  twice: a plain second read is CSE'd by FRE, a `volatile` (or u16) read
  isn't. The MU-type test is a signed int compare of the byte: an opaque
  `__asm__("" : "+d"(t))` copy stops reassoc merging it with the zero test
  into `(u8)(t-1) <= 40`.
- `showMobilePages`, no hints or attributes (the old pins and
  no-tree-loop-ivcanon were compensating for wrong source): `u16 len`
  (`len = s[7] + (s[8] << 8)`, printed as len, tested `len & 0x8000`) and
  `(u32)letter` in the printf. The pre-loop copies were never an IRA tie.
  With u16 len PRE inserts `(int)len` then `(short)len`, so the `[60]`
  store is that value's own move after the zero-extend. The `(u32)letter`
  no-op cast is hoisted into both arms by PRE, letter's PHI dies, dce4
  frees it with len's, and ivcanon/ivopts reuse those versions, which gives
  the inner loop's `cmp ebx,esi` (forwprop4 puts the lower SSA version
  first).
- `loadDump`: return type `u32`, `int size`, `u32 ret` (with an int return
  uncprop turns `return 0` on the `!size` path into `size` and coalesces
  them); `pages` declared before `rawSize`; `size % 528`; the positive
  `if (detectController(...)) {...} else {log}`. buildCleanup (inlined four
  times) must keep `&xb.mobile` in ebx and `&xb` in esi across all copies:
  its first loop is `for (i = 0; i < sizeof(xb.mobile) /
  sizeof(xb.mobile[0]); i++)` (both loop bases ivopts IVs, which dom3
  shares; `i < 11` holds the end in esi, the pointer loop's base is only
  shared by RTL PRE and cse_local undoes it). copyMmcImage's body is
  written out in loadDump (its no-if-conversion attribute stops inlining,
  and loadDump needs ce1 to hoist `ret = 1` and the 0x1080000 constants).
  The mmc test must be predicted in (50%, 52.6%] (ce1 hoists only above
  50%; better_edge_p lets the mmc trace take the log block only within
  10%): `notZeropair() != (size == 0)` adds the 72% opcode-nonequal
  prediction (VRP folds it to `!= 0` later) and a `hot` label in the log
  arm adds 15%, with the call heuristic 71% -> 52.6%. Independent of
  builtin-expect-probability.

The last two, matched 2026-10-27 by a third round of agents after two
earlier rounds (their variants, notes and tools are in
`tmp/image_read_agents/`, untracked, without the compiler dumps):

- `getImageSmc` built (2026-10-27, third round; agent notes and tools in
  `tmp/image_read_agents/getImageSmc3/`). Sequential tests reached by
  gotos: `if (!addr) goto zero; else { vhot: hot; } zback: if (addr !=
  0x800 && addr != 0x1000) goto bad; bback: <size test>`, with both log
  arms (`zero:` and `bad:`, the latter with a hot label) at the end of the
  function inside `if (0) { ... }`. VRP1 and DOM2 then give the zero and
  bad paths their own size-test copies and jump2 crossjumps their 7-insn
  tails (the zero path becomes `[esp+8]=0; jmp` into the bad log);
  `"no-tree-tail-merge"` in the optimize attribute (with no-if-conversion
  and no-if-conversion2) stops PRE merging the two copies' forwarders.
  The goto layout fixes `mov edi,ebx`: RTL cse1 walks paths branch edge
  first and a block shared by paths keeps the last path's choice; with
  the arms at the end the paths run zero, bad, valid, so the bad log reads
  edi and the entry test ebx. The same order gives the original
  ebx/esi/edi and `cmp ebx,eax`. Frequencies: the else's hot label puts
  the zero path at 6.7%; `if (!h) __builtin_unreachable();` before the
  0x3000 log moves the call out of the arm's first block, so only the
  0x3800 edge gets the call prediction (p(0x3000) 86.3%: keeps the zero
  copy within crossjump's 50% and the 0x3800 path at 11.6%, between bbro's
  10% copy and 20% align thresholds); `__builtin_expect(sane, 0)` cancels
  the early-return heuristic the end arms add (else the success path gets
  its own epilogue copy). The size-ok `__asm__("" : "+D"(addr))` pin and
  the size-bad hot label stay; the not-sane hot label and the
  `unscramble() != (h == 0)` hint are gone. Each hint is needed (2-81
  lines without one).
- `parseDump` built (2026-10-27, third round; notes and tools in
  `tmp/image_read_agents/parseDump3/`). `parseDump` and `spareLbaOk`
  return `unsigned long`: uncprop reuses a zero for the ZEROPAIR `return
  0` only if its type is compatible with the return type, so neither the
  u32 counter's zero nor memcmp's int zero is taken, but spareLbaOk's
  `unsigned long` one is. Shape: an if-chain on `-2, -1, -3, -6, -4` (a
  switch makes a jump table); loop over `u32 n` with `int blk = n;` at
  the top; partial-block test `int rr = xb.numPages % ppb; if (rr)`. The
  three remap calls go to `addRemapP`, a static tail-first copy of
  addRemap written with gotos (MAX/append tail before the loop body): the
  original's inlined guards are `xor; xor; test; jne body; jmp zero`,
  which ce1's find_if_case_2 makes only when the guard's next GIMPLE block
  is not the preheader, and with a for loop cddce2 always puts the
  preheader there; the standalone addRemap keeps the plain form, so it
  stays separate. `if (blk >= blocks) __builtin_unreachable();` before the
  -4 handler's `if (blk < blocks)` (VRP deletes the test after the branch
  estimate) and before the final remap; `__asm__("")` before the -4
  handler's `dst = blk` (one merge block, so postreload CSE doesn't rewrite
  one `mov ebp,[44]` copy); `int block` / `int i` in addRemapP for the
  `cmp [mem],reg` orders. -1 case: `b2 = blk; __asm__("" : "+r"(b2));`
  after the log call drives the inlined loop (LRA puts the argument load
  in esi), the second parameter `ablock = blk` keeps the append reloading
  [44]. The counter init `xor ebp,ebp` is IRA: n's pre-loop allocno gets
  ebp only if its cost beats the ebp holder's spill cost (5559); addRemapP
  takes a 5th parameter `cb` used as `__asm__("" : : "ri"(cb), "ri"(cb),
  "ri"(cb), "ri"(cb));` after `body:`, with blk passed in the -4 call and 0
  in the others (the "i" alternative, no code): four register uses per -4
  iteration raise n's cost to 5603 (3 uses: 5119, too few). Per-function
  optimize attributes for IRA (regions, algorithm, pressure, slots) didn't
  help.

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

Draft of the whole object, with string literals.  Compare a function with
`FNCMP_LITERALS=1 python re/fncmp.py wip/app/mode_client.c <fn> -O3 --param
builtin-expect-probability=50`.  (The long notes on how the other 15
functions and the hot part of `mode_client` were matched are in this file at
commit 6e3d2db.)

`mode_client` (2026-10-27): 56 fncmp lines; every block's content matches
and only the order of the ~25 cold traces of bb-reorder's last round
differs.  What that order says, with our RTL bb numbers (wip/mc/mcvar.py
identifies the blocks by content): the original extracts
`-ip, HDD-error x2, usage(2), -r, "Block outside", "Failed", -w, usage(4,cx),
usage(3,cx), -e, "Invalid", patches(NULL), info(NULL), usage(5,cx),
usage(5,dx), usage(3,dx), usage(3,ax), usage(5,ax), -c, -i, -p, ...`; ours
`-ip, usage(2), HDD x2, -r, Block, Invalid, -w, info, patches, Failed,
u4cx, u3cx, u3dx, -e, u5ax, u5cx, u5dx, u3ax, -c, ...`.  The last round
extracts a min-heap keyed by -frequency, so in the original the HDD errors
were at least as frequent as usage(2).  usage(2) gets 4: the copied loop
header's exit edge is 2% of the entry (214); 2% is gcc's floor for a loop
with >= 5 exits (every noreturn usage call is an exit), and the entry is
>= the 200 units of post-loop flow, so usage(2) >= 4 whatever the source.
The HDD errors are 50% of a switch case (both arms call) and a case is
1/13 of the dispatch; the dispatch is the switch path's share of the 200
post-loop units, and it must be <= 1/3 or the arg test falls into the
switch path (expand splits `(mode==0)|(arg==0)` into q/2 and
(q/2)/(1-q/2); connect_traces follows the higher probability; checked with
FDO at 40-46% and with `E()` on the test: the layout breaks exactly there).
So HDD <= 3 < 4 under every mechanism I could model, and the original must
have a tail or loop structure that makes usage(2) colder or the cases
hotter (not an `if (argc < 1)` check: that makes usage(2) key 0, far too
late; not nested `if (mode) if (arg)`: ifcombine's merged test still
splits the same way).

Searched and excluded (tools in `wip/mc/`): keys alone can't do it
(`mcsim2.py` replays the heap with frequency overrides, incl. the
"Changing key" priority form; bounded searches `mcfsearch.py`/`mcstage.py`
plateau at 3 inversions, always usage(2) before the HDD errors); then/else
polarity of every cold `if` changes nothing (gcc canonicalizes; `mcgen.py`
toggles); `E()` on each of the 50 cold conditions and every combination of
the six toggles that do move blocks (hdd, erase2, noereboot, tail, norok,
nofail; `mcexp.py`, `mccombo.py`) never put the HDD errors first without
breaking the hot part; a crafted profile (`fdorun.py` turns a frequency
design into gcda.py overrides, run from the same path as the instrumented
compile) can raise the cases but distinct case probabilities also change
which case trace connect_traces puts after the dispatch (all case edges
tie at 1/13 and the 4-block erase trace wins by length), the round-3
threshold (10) builds cases >= 10 early, and the inlined clientEraseBlock
needs `--mult`.  re/gcda.py now applies several overrides on one source
block as a group (needed for switch edges).  Score a variant with
`python wip/mc/mcvar.py <file.c>` (inversions and matching prefix of the
cold order, FNCMP=1 adds the fncmp count); `wip/mc/bbsum.py` lists a
bbro dump's traces with each block's calls, `wip/mc/mcblk.py` diffs the
block order against the original's .s.

Source-shape search (2026-10-27, second session), negative:

- Tail structures without the draft's hints (`wip/mc/gen2.py`: usage check
  first or not, `if (mode && arg)` / inverted / `!mode || !arg`, failure as
  `goto fail` / inline `return 0` / `else log`, the reboot+disconnect tail
  common or duplicated; `wip/mc/tailvar.py` has the hand-written ones and
  an early-return `clientEraseBlock`): every hint-free variant is >= 123
  fncmp lines and none puts the HDD errors before usage(2).  The usage check
  first (`if (!(mode && arg) && !reboot) client_usage(2, NULL)`, then the
  retest, which gcc threads) does make the switch path 50% and the HDD
  errors 4 (cold order inv 18, prefix 4), but then the arg test falls into
  the switch path (110 lines): expand splits the combined test q/2 then
  (q/2)/(1-q/2), and the trace follows the switch edge unless its block
  fails round 1's exec threshold while the reboot test passes the 40%
  branch threshold, i.e. P(switch) <= 42.9%.  With P(switch) <= 42.9% the
  dispatch is <= 80 and a case <= 6, so an HDD error (half a case, 72% with
  `(hwFlags & 0x20) == 0x20`) is <= 3 < usage(2) = 4 whatever the connect's
  probability; and the connect itself has no heuristic above 61% (early
  return on the failure block) unless the failure path is noreturn/cold.
  The `== 0x20` spelling changes nothing in the order.
- Why the hinted draft needs its hints: `fail: cold` gives the switch
  connect 99.9% ok (without it the shared `goto fail` block isn't dominated
  by either connect, so only the ok edges get PRED_CALL and both connects
  are 29% ok); `rok: cold` keeps the reboot connect falling into fail; and
  `E(reboot)` cancels the early-return penalty on the netDisconnect block
  (gcc 6 exempts only the function's last block, `last_basic_block_p`), so
  in the original the `if (reboot) netReboot; netDisconnect; return 0` tail
  was probably the last code in the function and the "unable to connect"
  log before it (it is the last string, but has no code after it).
- The heap itself: `wip/mc/mcsolve.py` (fibsolve on the draft's dump, all
  28 small keys symbolic) reaches 19 of the 40 round-4 starts at best (it
  can't get `-w` after Block/Failed), `wip/mc/mcgrid.py` (7776 frequency
  designs replayed with mcsim2) bottoms out at 6 inversions, all equal-key
  ties ((Block, Failed), (u4cx, u3cx), Invalid vs -e, the -bp/-wb/-eb
  usage blocks vs patches/info), and `wip/mc/mcearly.py` (single key
  changes in rounds 2-3, event-driven from round 2) moves nothing.  So the
  original's insertion history into the last heap differs from the draft's,
  not just its keys; a crafted profile changes that history (the FDO
  baseline, `python wip/mcfdo.py <abs dir> wip/app/mode_client.c`, is 126
  lines / inv 40 by itself), which is the only remaining lever besides a
  structure nobody has guessed.  usage(2)'s 4 comes from dom2 threading the
  copied header's 2% exit through the post-loop tests (the block is 0 until
  `sink` merges the 4-unit copy), and the entry can't be below 175 (rounds
  put it in 141..240, the 2% loop-exit floor at 200+).

Crafted profile (2026-10-27, third session), also negative, but the tooling
now works for this object:

- Profile-build mechanics learned on the way (all in `re/gcda.py` now):
  gcc 6 inlines a global callee with its gcda counts *unscaled* (the clone's
  count is the callee's, not the call site's), so `--entry=fn:caller:bb`
  ties the callee's entry count to the call block's; the callee's empty
  return block is merged into one of its leaf blocks after inlining, which
  gave that leaf the whole entry count (Success or Invalid depending on the
  leaf counts) until `fn:bb>1=P` routed 100% of each erase leaf's flow
  through its fake exit arc (the join count becomes 0, the leaves keep their
  own counts); `--consistent` is needed once an edge is zero.  With the
  plain frequencies as the design (`wip/mc/fdorun.py c1400 ...`, see the
  slot dirs under build/mcfdo) the profile build is 64 lines and has the
  plain build's cold order.
- The blocker: at the arg test the trace always ends (the reboot test has
  two predecessors and is copyable, `copy_bb_p`), so connect_traces picks
  the switch or the reboot path by edge probability, i.e. P(switch) <=
  1/3 in every mode, plain or profile (the 42.9% window in the paragraph
  above was wrong; the earlier notes' 1/3 was right).  Then the dispatch is
  <= 62, a case <= 5 and an HDD error <= 3, while usage(2) is >= 4 unless
  the loop-exit probability is lowered, which compresses every cold key into
  0..2 and multiplies the ties.  Designs that keep the hot layout (D4:
  cases 7/6.55 in two equal-key groups, HDD 50.5%, chain 45/50/50%) reach
  prefix 8 of 40, inv 15, with the arg test falling into the switch path
  (fncmp 148); the realized frequencies match the design exactly, so the
  tooling isn't the limit.  Scripts: `wip/mc/mcgrid.py` (grid over
  cold keys on a build's own dump), `wip/mc/mcsolve.py`, `mcearly.py`.

## app/net.c

Built entirely from `src/app/net.c` (no .s) since 2026-10-27; this draft
is the same code with plain string literals. The src file gives every
string as a `static const char net_<address>[]`: gcc emits variables in
reverse definition order (net is built without -fno-toplevel-reorder,
which would emit the netRecv clone last), so the arrays are defined from
the last .rdata string to the first, aligned as gcc aligns a literal
(`aligned(4)` from 31 bytes, else 1). With literals, netReadInfo's and
netConnect's strings come out in a different order from the original's;
the rest already matched. `.bss` order is the reverse of the statics'
definitions too (netEmpty is defined before netInfo). The names for the
unexported functions and data (`netRecv`, `netFindBeacon`, `netSock`,
`netEmpty`, `netStartTime`, ...) are in `split.py` SYMBOLS, and the ws2_32
IAT slots are renamed to winsock2.h's `__imp__send@16` spelling
(`IAT_NAMES`; `.string` lines are skipped so "bind"/"connect" in messages
survive).

Test the draft with `FNCMP_LITERALS=1 python re/fncmp.py wip/app/net.c
<fn> -O3 --param builtin-expect-probability=65` (netRecv:
`FNCMP_GCCSYM=_netRecvVerbose.constprop.1`); `python wip/fnvar.py
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

The last two (2026-10-27):

- netRecv is IPA-CP's `netRecvVerbose.constprop` for verbose 0:
  `#define netRecv(len) netRecvVerbose(len, 0)` after netRecvVerbose (the
  local calling convention, the function order and the 13 calls + 2 tail
  jumps all fit). Two things made the clone match:
  - Registers (size/buf/got in ebx/esi/edi): got sits right at IRA's
    caller-save cost threshold (ira-costs.c, the ALLOCNO_CALL_FREQ
    adjustment: an allocno crossing calls keeps edx/ecx only while class
    cost + call freq x 8 stays under its memory cost). An empty `asm ("" :
    : "g"(got))` before the short-count log puts the clone's got over it
    and leaves netRecvVerbose matching. Uses of got elsewhere move
    netRecvVerbose's got too. What the original had instead of the asm is
    unknown.
  - The `*len = 0` slot was alias analysis, not LRA. netSock is public, not
    `static`: a public global may be aliased by a pointer store, so sched2
    keeps `*len = 0` after the `netSock` load (anti-dependence) and issues
    it between the fd_count and fd_array stores, as the original. With
    netSock static and its address never taken, points-to separates them
    and the store issues at t=3 alone. (The earlier theory, that the
    original's `mov edx,eax` was a reload after NOTE_INSN_FUNCTION_BEG, was
    the wrong lead: the edx copy is the same either way.) In general, a
    store or load whose slot moves in sched2 can mean that a global's
    linkage (static or public, address taken or not) differs from the
    original, which the exe shows only through codegen like this.
  Ruled out on the way: `*len = 0` first, u32 casts on the log arguments,
  split or reordered declarations of got, the asm after the log (48 lines
  each); IRA/LRA/sched params; the do-while and no-tree-ch forms (28).
- netWritePatches and the other netEmpty functions: the unmerged
  `mov eax,1` pair after `cmp r,netEmpty` comes from a scope clobber. The
  reply length lives in a block that ends after `netFree(r)`, and the
  `if (ret) return 1; return 0;` is outside it:
  `{ int rlen; if (!netSendStr(..) || !netSendData(..) || !(r =
  netRecv(&rlen))) return 0; ret = rlen == 2 && getBeU16(r) == OK_REPLY;
  netFree(r); } if (ret) return 1; return 0;`. After threading, T's
  `r == &netEmpty` edge (ret known 1) leaves the scope on its own path,
  through its own gimple block (`rlen ={v} {CLOBBER}; goto <return>`) where
  the `retval = 1` PHI copy lands. At expand T's false edge gets a
  jump-only block, which into_cfglayout removes, so in cfglayout order T is
  followed by neither successor; fixup_reorder_chain gives T a jump block
  for its fall-through, and at jump2 T's successors are {jump block,
  `eax=1` block}. flow_find_head_matching_sequence stops at the jump, so
  try_head_merge_bb has nothing to merge; a jump block reached by
  fall-through can't be forwarded in rtl mode and merge_blocks_move needs
  CLEANUP_EXPENSIVE, so it survives jump2, and bbro removes it later. So
  the `no-crossjumping` attributes were only standing in for the scope:
  netFormatSysex/Compat and netEraseBlock now match without any
  attribute. Details:
  - The block must hold the sends too (a block starting at netRecv: 36-45
    lines in netFormatSysex); every `return 0` path has to leave through
    the same clobber copy.
  - `ret = rlen == 2 && ...` (or `ret = 1; if (... fails) ret = 0;`) gives
    the branch sense at T; `ret = 0; if (...) ret = 1;` stops the merge
    but flips `je`/`jne`.
  - netWritePatches keeps `no-early-inlining` (without it the free block
    shares the epilogue, bbro's duplication threshold) and needs the three
    tests folded into one `||`: separate `if (!x) return 0;` tests leave 2
    lines (`mov [esp],ebx` instead of eax before getBeU16). vrp1 threads
    the inlined netSendData's `hdr` clobber block and creates the copies in
    redirection-hash order (keyed on the target block's index,
    tree-ssa-threadupdate.c); with the rlen clobber the failure copy lands
    between `len != 0` and the netRecv block, crited1 puts the loop-exit
    split before netRecv, netRecv ends up last in the chain, and
    cprop_hardreg (chain order, inheriting only from an already visited
    single predecessor) doesn't see `ebx = eax` at the getBeU16 block.
  - netWriteBlocks, netSendFile and netMkdir keep their attributes. In the
    scoped `||` shape they differ only in the branch sense at T (2, 4 and
    2 lines); the next step there would be T's edge probabilities.
  Ruled out: netEmpty public, volatile, const, extern, or as `u8[4]`, `u8`,
  `u64`, `void *` (no effect); about 35 global flags; global
  `-fno-crossjumping` (breaks seven matched functions, so the original
  crossjumped); `ret` as u8/_Bool/char/u16/u32; netFree spellings testing
  netEmpty first.
- `-fno-tree-dominator-opts`, `-fno-if-conversion`, `-mbranch-cost=1`,
  `-O2`: none is better for the whole file.

## app/build.c

Draft of the whole object (all 41 functions). 40 match and are built
from `src/app/build.c` (mixed): findFileOffset, findFileSize, findFile,
readMetaFile, makeTimestamp, loadCommonFile, loadBinFile, loadLocalFile,
setFileData, iniRangeOk, raiseKernel, patchHeaderOpts, rotSumSha,
countBits, isUpdateBl, patchPayloadSize, showSmcConfig, blmodMissing,
patchFreeboot, encodeUpdateBls, logPowerButton, timestampToFileTime,
loadBaseFile, loadBaseFileMeta, loadFileCrc, extractSmcConfig,
verifyBlSigs, appendAddonPatches, patchSmcConfig, checkBl, fixupPatchSet,
patchBlsResign, calcBlAreaSize, patchBlsBlmod, addBlsToImage, loadInputFile,
addUpdateBls, loadConsoleBlFiles, buildFlash, encodeBls.
Switch tables go through
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
- loadInputFile (built from C, 2026-10-23): the SUPD / nanddump / USVR /
  common-dir fallback chain. The `setne; and; test al,al` boolean PHI at
  the common test comes from PRE, which builds it only if the `r = 0`
  paths still reach that test, i.e. vrp1/dom2 haven't threaded them (they
  thread only into blocks ending in a condition): `u32 ts` declared inside
  the `if (fs && r)` block puts its CLOBBER at the fs join, keeping it a
  real block (without: ~356 lines). `u32 r` (the `(int)` on return stops
  coalescing it with the return value: separate `mov eax,esi`; 93). Tail
  `if (common && r) r = loadCommonFile(...); return r;` (a `return
  loadCommonFile` gets early-return + call heuristics, 21%, and loses its
  round-2 key; 263). SUPD and USVR failure arms first (`if (crc != c)
  warn; else { meta; r = 0; }`; USVR's is a peephole2 register effect via
  block index order). May need retuning once loadBlFiles is in C (IPA
  context).
- checkBl (built from C, 2026-10-23): `__builtin_expect(crc == 0xffffffff,
  0)` in the SC and SD cases (not SE) sends enough branch frequency to
  `bad` for the loop-head alignment rule. History: fncmp MATCH
  (2026-10-22, probability 98) but the link was 16
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
- appendAddonPatches (built from C, 2026-10-23): `a = &xb.files[19 + i]`
  instead of `&addons[i]` fixes the lea order: ch2 then reuses free-list
  names for the renamed loop PHIs, PRE's temp gets a fresh higher name
  (prephitmp_80 > size_32) and the refold keeps `size + prephitmp`.
  History (18): positive-condition nesting fixed most of it;
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
- fixupPatchSet (built from C, 2026-10-23): the Linux v1.16 build
  (tmp/xeBuild64, found by its "Fixing up patch set" reference) shows the
  loop: after the shift it sets `off = e->size` and goes back to the test,
  no `break`; gcc 6 threads that edge to the exit, so it looks like a break
  here. With that latch (no hot label, no `continue`) the profile gives the
  original's allocation: off spills, n stays in a register, and the copy
  loop's byte temp takes esi, so LRA hands p ebx (`mov ebx,eax`). The off
  reloads are gcse-after-reload moves into the predecessors. `t = off + 4`
  as its own name gives the shared off + 4 and the skip from the old off.
  Earlier (`break` + hot label, 71 lines) the copy loop was 84% and off's
  cost outweighed n, p and e together: no pin could move the spill to off.
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
- patchSmcConfig (built from C, 2026-10-23): `cb_hint(&dead)` at the start
  of all four store arms (cpu/gpu ok and 0x7f) breaks both fibheap ties the
  original's way; a hint in one ok arm only (PRED_CALL) makes its log block
  hotter but its ok block colder (8 lines). Of hint subsets over six spots
  only the four-arm one matches; hot/cold labels give fncmp MATCH but miss
  an alignment (fncmp can't see it: build/v/trio/offcmp.py compares
  assembled offsets). `optimize("no-early-inlining")` and the gpu warning
  after the return (string order) are kept. History (10): two cold blocks (gpu/cpu fan warnings) in the
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
- patchBlsResign (built from C, 2026-10-23; xeBuild64 0x406750 has the
  same loop as fixupPatchSet). The no-header-copy shape is that latch
  (`else { copy; off = p->size; }`), not something stopping pass_ch.
  - `if (n != 2) { body } else { copy }`: with `n == 2` first the body
    starts with a label at LRA time and LRA's inheritance EBB stops there,
    so `cmp [n],2` and `test n` don't share a `mov esi,[n]` (348 lines with
    `n < 2`). `addr != 0xffffffff` first (51/49 tie, prev_bb rule).
  - `t = off + 4` before the -1 test; `off += 8` before `if (n)`, then
    `d[off + i]`, `off += len` (else PRE/sink puts off + 8 in each arm).
  - After the loop, failure arms first (`!blVerifySig`, `if (xb.prvKey)`,
    `if (!memcmp)`): postreload's reload_combine_recognize_const_pattern
    moves `reg += xb` past address uses only if reg isn't live at the
    block's jump target, i.e. the jump must go to the good path.
  - `if (sb) {...} else ...; return ok;` with `if (ok) Done`, no early
    returns (early-return predictor 39% on blSign fail; at 50/50 a round-3
    fibheap tie pops success first). `u32 blSign` stops uncprop reusing its
    0 result for the fail return.
- patchBlsBlmod (built from C, 2026-10-23): patchBlsResign's walk, with
  `if (!n) {cbb} else {cd}` (the original jumps to cd; `if (n)`: 223
  lines). `int size`: `(unsigned)size` gets its own PHI/pseudo (esi) while
  size spills to `[60]`; as u32 they are one spilled pseudo. `if (blmod &&
  size) {...}` instead of an early return (the main path must fall through
  at LRA time for the size reload's EBB). `hdr[0x49] = i >> 8` before
  `hdr[0x4a] = i`. Last 2 lines, the loop-entry spill store order (cd
  before pt): IRA emits region-border moves by pseudo regno, partitions
  numbered by lowest SSA version; the early inliner walks callees last call
  first, giving pt's findFile the freed VDEF names. `-fno-ipa-pure-const`
  or `optimize("no-early-inlining")` on the function (used) fix it; ~20
  spellings didn't.
- calcBlAreaSize (built from C, 2026-10-23): `x = findFile(N); size =
  findFileOffset(N) + xb.files[x].size` (size load after the offset loop;
  212 -> 95). `u32 x` (int: 123) fixes the type==2 offset register, the xell
  compare order and the `imul; add OFFSET _xb` pointer: those orders follow
  PRE temps reusing freed SSA names, and arm reorders or helpers that fix
  them break the layout. In type > 5 the 12/14 lookups go through x (13
  direct: 4 lines). The sum stays in esi through the 13 add, then `mov
  ebx,esi` after `cmp ecx,14`: a `"+b"(size)` pin after `x = findFile(14)`
  (before it, the flags clobber puts the copy before the cmp). The files[]
  bound (>= 18) and declaration order don't matter.
- loadBlFiles (16, 2026-10-24; was 668; loadConsoleBlFiles' case-24 copy
  and a nested `if (r) { if (type == 9) { if (!suGetCF) break; } ... }`
  9-group, 78 -> 73): the switch is a separate static
  `u32 loadBl(e, i)` (inlined), called under the "none" test (`if
  (strnicmp(e->name, "none", 4) || e->crc) r = loadBl(e, i); else r =
  0;`). The guarded call gives P(switch) 0.645 (case blocks under round-1
  threshold), and ipa-cp, which runs before inlining, sees loadInputFile/
  checkBl calls per loadBl call (0.03-0.08): no loadInputFile, loadFileCrc
  or checkBl clones in the full draft, and loadLocalFile matches there.
  Inline in the loop, every shape tried was >= 254 lines with the clones.
  `u32 r` (int: uncprop reuses the switch index for `r = 1`); no `goto
  fail`, errors set r and break; takeFile written out inline (as a call it
  takes the 29% call heuristic). Case order (5..21, 6, 24, 1, 22, 25, 3, 4,
  23, 27, 2, default) comes from peephole2's rotating free-register search
  over the seven `mov reg,[mem]; test` loads (blocks visited in reverse).
  Case 27 needs `__asm__("" : "+a"(d))` on the data pointer. Left: case 24
  copy scheduling, case 23's `mov edi,-1` not cross-jumped, the r test
  duplicated into case 6, cold-block order, and two jump threads: the FSM
  threader counts the caller/helper `r` PHI merge (a `u32 *pr` out-param
  fixes that one: build/v/lbf/topr.py, 80 lines), and the type-11 pub1bl
  path is 8 stmts against the limit of 7. Scratch: build/v/lbf/.
  Third pass (2026-10-24, 73 -> 25, scratch build/v/lbf3/: runfiles.py
  flags, traces3.py + bbro.sh, phim.py PHI order per pass, j2.sh/ce1.sh
  crossjump/ifcvt logs):
  - `static void loadBl(e, i, u32 *pr)` writing `*pr` (caller `r = 0; if
    (...) loadBl(e, i, &r); if (r) ...`): one r, so the FSM threader no
    longer counts the caller/helper PHI; the sigfail setFlashBuild copy is
    threaded in dom2, before ivopts (`imul eax,[esp+44],1068`).
  - Signature check failed arm first (string order nokey < failed <
    passed; xeBuild64 agrees): `else if (!cbVerifySig(..)) { failed; *pr =
    -1; } else if (type) passed;` (always-true `type` takes PRED_CALL off
    the passed edge: 71%). 73 -> 45.
  - Case 23 `badsize: __attribute__((hot));` first in the `e->size & 3`
    arm (appendAddonPatches' cold block after the type-9 checkBl; a hot
    label adds no CFG edges, a guard block reshuffles PHI order). 45 -> 41.
  - Case 27 `__builtin_expect(type == 27, 1) && loadBaseFile(...)` breaks a
    freq-149 tie (keyvault_alt before config.bin). 41 -> 25.
  Left (25): the type-11 pub1bl/nokey thread (13; dom2's FSM reaches A via
  M's PHI args, the passed route marks A visited and is rejected at 9
  insns; vrp1's joiner copy reverses M's edge order; `if (pr) *pr = 0;`
  after the nokey log makes the thread but zeroes the test block's
  frequency, 32), the type-10 checkBl crossjump (8; vrp2's joiner copy
  gets REG_BR_PROB 10000 so fixup_reorder_chain doesn't invert it like the
  type-9 copies), `mov edi,-1` (3; ce1 find_if_case_2 hoists it, jump2
  head-merges the split block), the SE `ja`/`jbe` polarity (2). gcc 6
  keeps one FSM path per entry block per pass, marks visited_bbs before
  rejecting, and prepends redirection lists (joiner copies get preds in
  reverse).
  Fourth pass (2026-10-24, 25 -> 16, scratch build/v/lbf4/): the type-10
  checkBl crossjump needs all three of `else if (__builtin_expect(type ==
  10, 0)) { if (!suGetCG(..)) break; goto chk; }` (chk: before the checkBl
  call; the copy is then made in vrp1/dom2, before sink's forwarders, so
  its branch probability matches the type-9 copies'; outgoing_edges_match
  refuses > 50% apart), case 6 `u32 r6 = checkBl(..., 6, ...); __asm__(""
  : "+r"(r6)); *pr = r6;` (else it merges with type 10 on 6 insns, >=
  PARAM_MIN_CROSSJUMP_INSNS 5), and the expect (keeps bbro from copying the
  r test into the tail). `if (xb.type <= 5) break; if (type == 14)
  setFlashBuild` fixes the signature-failed `mov edi,-1`. Left (16): the
  type-11 thread (13): dom2's FSM threads through vrp1's shared checkBl
  copy and duplicate_thread_path's scaling zeroes the `type == 11` test's
  frequency, so in bbro it gets the type-17 test's priority and pops early;
  the original needs it popped between the signature-failed and SE traces
  (no priority: type-17 -> pub1bl edge >= exec_th 44, ours 43; freq ~25);
  ~60 variants failed. SE `ja` (2; joiner copy REG_BR_PROB 10000). Case
  23's -1 (1): appended inside the single-successor log block at expand,
  so crossjump can match only 1 insn. build/v/lbf4/b4.c (23 lines, also
  `if (pub1bl) { if (!cbVerifySig) failed; else if (type) passed; } else
  nokey;`) generates the type-11 block fully, misplaced after the type-9
  checkBl tail. In the whole-object build loadBlFiles' diff is the same
  and its strings are already in order (no arrays needed).
  Fifth pass (2026-10-24, still 16, scratch build/v/lbf5/: flt.py replays
  a bbro dump with one block's key overridden). The type-11 thread has two
  blockers. A: vrp1 makes one shared checkBl joiner copy (entered from the
  14/9/9/10 paths) and stops at the type-11 block (it holds the `type !=
  5`/`!= 17` ASSERT_EXPRs, so thread_around_empty_blocks refuses it); dom2's
  four FSM threads over {copy, type-11 block} (which also make the per-type
  checkBl copies) scale the region by the copy's remaining flow: 86 -> 80
  -> 63 -> 2 -> 0. B: even unzeroed, the type-17 -> pub1bl edge is 122 x
  0.701 / 2 = 42.8 < exec_th 44, and the block pops between the signature-
  failed and SE traces only for keys -22..-27 (unzeroed 36.5): it needs
  loadBl's 50% `type == 5 || type == 17` split (no heuristic) at ~0.556-0.585,
  or flows with F + c >= 174 and F - c in 44..54 (now F = 122, c = 49).
  FSM limit (gcc 6.2): n_insns counts every path block but the entry
  source, PHIs only in blocks with > 1 pred and succ and for other vars,
  minus 1; rejected at 2n >= 15 (two nested `__builtin_assume_aligned` at
  chk kill the dom2 threads: type-11 unzeroed but 9/SE share one checkBl,
  92/99). Crossjump only redirects a fully matched src1 (the non-fallthru
  pred, else the lower index): case 23's log block is src1 against the
  high-index split-edge -1 blocks. SE `ja`: the `xb.type <= 5` test is
  0/100 before dom3 (vrp1 joiner threads drain it). Failed: precomputed
  flags (forwprop folds them), 5/17/11 tests on the pre-SE type (117-284),
  `^`/`!=`/`+` forms (96-127), `int *pr` (133-379).
  Sixth pass (2026-10-24, structural, still 16; scratch build/v/lbf6/,
  lnx.txt = xeBuild64's loadBlFiles at 0x405280 annotated): v1.16 has the
  draft's structure (r != 0 -> type 9 suGetCF / 10 suGetCG with its own
  checkBl; 9 and SE share one checkBl; else generic checkBl, then 17/5/11
  tests, the signature block, `xb.type <= 5` before `type == 14`; no bit
  test, no inner switch), as does IDA. b4.c's signature form `if (pub1bl)
  { if (!cbVerifySig) failed; else if (type) passed; } else nokey;` is
  supported by .rdata (gcc 6.2 places FSM copies at split_edge_bb_loc(entry),
  so the nokey copy expands first: nokey < failed < passed) and verifyBlSigs'
  style; in the whole-object build it gives .rdata and sizes SAME (23
  lines, the type-11 block after the type-9 checkBl tail). Blocker A is
  structural under this source: duplicate_thread_path scales the region by
  (head - entry)/head, FSM paths go before forward ones, and the c11 block
  can't be empty (`type` live after it). Targets: c11 unprioritised with
  key -27..-22 (freq ~23-26); type-17 -> pub1bl edge >= 44 (g + c >= 176,
  g - c in 44..54, c ~68-78, now 49); merged 9/10 checkBl -> r-test edge <
  88. Dropping the type-10 expect fixes B (edge 44) but c11 stays 0 (25);
  separate 5/17/11 ifs get ifcombined (81/89; without ifcombine c11
  survives at 11 but each test is 28%); explicit SE/10 checkBl calls
  31-272; `type == 5 || type == 17` always folds to a 50% BIT_IOR.
  Seventh pass (2026-10-26, still 16; scratch build/v/lbf8/: mv.py
  variants, ev.sh = lines + c11/sigfail/SE trace keys, tr.py = bbro traces
  mapped by freq alignment, pp.py/fl.py/cb.py = per-pass block freqs,
  rb.py = RTL block listing; gcc 6.2 threader sources fetched to the
  session scratchpad, identical across 6.1-6.5):
  - Zeroing, exactly: dom2 registers FSM paths [c11, X] for X's literal
    PHI args (vrp1 joiner copy, 9/9/14/10); duplicate_thread_path scales
    the whole region {X, c11} by (freq(X) - entry)/freq(X), so c11 (and
    its generic flow) ends at 0. Only a region {c11} (entry edge straight
    into c11 with a literal PHI arg, i.e. single-valued copies) or forward
    threads (update_profile subtracts) keep c11. FSM is called from
    thread_across_edge whenever the forward search fails, on any edge into
    c11, and only looks at literal INTEGER_CST PHI args.
  - Arithmetic: without the type-10 expect (19.9% type == 10, 61%
    suGetCG) all-forward subtraction gives c11 = 29 and 17 -> pub1bl = 46:
    c11 then pops right after sigfail (tie broken correctly), SE after
    (build/v/lbf8 noexp_aa2: assume_aligned x2 at chk makes dom2 reject
    the FSM paths, but then 9/SE/10 share one copy with `mov esi,9/14`,
    as in v1.16). c11 = 0.305 (g - c'), edge = 0.1525 (g + c'): all
    copy flows must pass the 5|17 block and be subtracted from c11.
  - Per-type constant copies (9, 10, SE) must still exist, and the 9/10
    tails fold into the post-switch r-test R by RTL crossjump in jump2:
    crossjump only redirects a fully matched 'from' block, and 'from' is
    the edge source with the lower bb index. Copies made by threading get
    high indices (base: copies 121-125, R 113, R is 'from'); source-level
    explicit calls get low ones, so their `cmp di,0; je latch` tails never
    fold into R (the `test edi,edi; je l` hunks).
  - Best new structure (64 lines, s20a_b4/s21g_b4/s23b_b4/s25ar_b4): SE and
    10 explicit (own checkBl + r-test + `goto sig`), 9 through chk with
    `if (type != 9) { __asm__("" : "+r"(type)); if (!type)
    __builtin_unreachable(); }` (PHI for vrp1, no PRED_CALL on the edge;
    the unreachable keeps `else if (type)` foldable), a `} else
    __asm__ __volatile__("");` block funnelling both 9 entries (blocks the
    dom3 forward joiner that otherwise subtracts the 9 flow a second time
    on top of the FSM [c11] thread), and `__builtin_expect(i != 0, 1)`
    guards before the SE/10 calls (a guarded call block gets PRED_CALL;
    `type == 10` guards are folded before profile_estimate, `i != 0` is
    not). c11 = 29 and lands between sigfail and SE. Left: case 25's xell
    tail placement, the R dup into the type-6 tail, 9/10 tails not folded
    into R (N9 merges into the 9 copy: low index), sigfail setFlashBuild
    via [ebx] instead of i, plus the old -1 and ja. A volatile asm inside
    c11 (`({ __asm__ __volatile__(""); type == 11; })`) also blocks
    ifcombine/reassoc and the forward double, but its copy sits on the
    copies' latch path and blocks the R crossjump.
  - Dead ends: params (fsm-scale-path-stmts, max-jump-thread-duplication-
    stmts, max-fsm-*: none better than 18); switch inline in the loop and
    always_inline loadBl (c11 zeroed the same way); a 2-case switch for
    5/17 (c11 lands in the main trace); 9/10 without own r-tests (flows not
    x0.61, c11 9); int-typed r tests (still threaded); `*pr = 0` after the
    r-test (VRP keeps an unused assert in the split edge block).
  Eighth pass (2026-10-26, crafted profile, best 15; wip/app/build_fdo.patch
  applies to the commit that adds it: b4.c's signature form as the draft,
  NOPROF macro, mixed.py `profiled`, build.sh second compile `fprof`/`ffns`
  spliced by `splice.py _loadBlFiles=<fdo.s>`, src/app/build.prof with the
  best overrides; regenerate with split.py after applying):
  - A profile can't undo the zeroing: duplicate_thread_path scales the
    region by (X - e)/X in counts or frequencies, so c11 ends at 0 in every
    regime (zero-count entries keep it, but then the 9/10/SE paths are
    cold: 190-225). No pass after dom2 rebuilds frequencies (only inlining
    and versioning do). Counts can't be inconsistent at read (re/gcda.py
    `--consistent` makes exact integer flows so 0% overrides don't solve
    to -1).
  - Counts for loadBlFiles+loadBl (PROFILE_READ): with b4.c and `9>10=0
    15>20=0 13>14=0.5 16>17=18` (loadBl dump numbers) c11, its pub1bl copy
    and nokey land right (c11 is never-executed, key 10000, popped last),
    17 lines; left an ivopts tie (131 = 131, complexity picks a third IV for
    &e->size, `[40+esp]` for i): with counts the loop estimate is 11
    iterations (guessed: none, AVG_LOOP_NITER 5), candidate cost 5 not 6.
    The estimate is latch/preheader counts, tied to the body/entry
    frequency ratio bbro's thresholds use. `--mult=loadBl:K` (inlined
    called-once bodies keep their own counts, so K decouples body from
    caller) with a 4-iteration loop fixes the IVs, but then the caller's
    loop blocks are colder than the switch and better_edge_p's
    lower-frequency-destination rule breaks the main trace (106-371).
  - Counts for loadBl only, loadBlFiles NOPROF (guessed loop, IVs right):
    the inlined body keeps loadBl's counts in a guessed caller (copy_body
    scales by callee->count), so threads mix count and frequency updates.
    Best 15 (build.prof): c11 chain right after sigfail and SE polarity
    right (fibheap ties among key-0 blocks: build/v/lbf9/r4.py replays round
    4 with key overrides). Left: the generic type-14 setFlashBuild block
    (36) is drained like c11 (its type == 14 test's region), so it is
    absorbed into the SE trace instead of following `cmp esi,14`, and case
    23's -1. The NOPROF attribute can't go on the other 40 functions in the
    one compile (callees with their own optimize attribute don't inline into
    the three no-early-inlining callers: iniRangeOk, raiseKernel, findFile,
    cb_hint; loadInputFile/loadLocalFile also differ), hence the second
    compile. Scratch build/v/lbf9/ (fdo.sh, probe.sh, search.py greedy,
    grid.py, r4.py/r4s*.py heap what-ifs, lbf.sh = fncmp of build.sh's
    profile compile via re/fncmp.py FNCMP_ASM).
  - Next: make block 36 hot before the SE trace is built (its key must be
    below the SE block's), e.g. a NOPROF-regime override that leaves the
    type-14 test's region undrained, or combine the PROFILE_READ regime
    (17, layout right) with a source change that breaks the ivopts tie.
  Ninth pass (2026-10-26, fncmp MATCH, link 34 bytes off; the setup is
  wip/app/build_fdo.patch, which now applies to the ninth-pass commit;
  regenerate with split.py after applying; scratch build/v/lbf10/: rb.sh =
  build.sh's -DBUILD_FDO compile of any source copy + fncmp + .p2align count,
  var.py variants, search.py, gcda_runs.py = gcda.py with GCDA_RUNS):
  - Counts for loadBlFiles+loadBl+loadBl60 (PROFILE_READ regime, 17) plus
    `#ifdef BUILD_FDO` xb.files[5] (FILES_BOUND): the array bound caps the
    loop's niter estimate (11 from the counts), ivopts' candidate cost is 6
    again and the third IV goes. 17 -> 3 (-1 and the SE `ja` left).
  - Case 23's -1: a shared `fail: __asm__ __volatile__(""); *pr = -1;` at
    the end of loadBl, reached by `goto fail` from the size log, the SMC
    failure and the signature failure (`if (xb.type <= 5) { if (*pr) goto
    fail; break; }`). The asm keeps the block of its own (without it the
    forwarder is merged away or the -1 lands in the log block), and with
    all three -1 paths through it there is no split-edge -1 block left for
    crossjump to refuse. Then overrides `21>22=70 22>90=5` (X and the r
    test after it) give the SE copy of X the original's probability (the
    vrp1 joiner copies' TRUE edge was 0% from the counts) and keep the
    sigfail c14 copy hot (`mov edi,-1` after the cmp, not `or` before it):
    fncmp MATCH (src/app/build.prof in the patch).
  - Left: the final nokey log (L_42ada0) must be `.p2align 4,,7`-aligned.
    In PROFILE_READ compute_alignments skips it (count 0, so
    optimize_bb_for_size_p), and it is laid out last only because c11, SE
    and nokey all have bbro key BB_FREQ_MAX (never executed) and fibheap
    ties pop them c11, SE, nokey. A hot count needs count > runs while
    never-executed needs count * 20 < runs, so nokey's key drops to -freq
    and it pops before c11/SE (10 lines; any 15>20 > 0); the alignment rule
    also needs its freq >= 1 (prev SE block freq 0). Keeping it last then
    needs c11 and SE keys <= nokey's, i.e. c11 with a count/freq at bbro,
    which dom2's FSM drain still takes to 0 (c11 has 16384/1 at vrp1). With
    runs = 0 (GCDA_RUNS=0) nothing is never-executed and the build still
    matches (keys 0 instead of 10000, same ties), nokey still cold.
  - Dead ends: an extra statement in the type-14 setFlashBuild block (FSM
    limit 2n >= 15) makes the forward threader handle it after ivopts
    (`[ebx]` instead of `imul [esp+44]`); loadBlChk (r test in an inlined
    helper with counts) 111-566; moving the fail log before the loop
    (`if (0) { fail: ... }`, crossjump index order) 9; the J block in
    regime (b) 18-66; a dead `if (never) goto nokey` edge (count without
    flow) moves nokey the same way as 15>20.
  - Pitfall: a profile compile with `-o out.s` (aux name `out`) silently
    finds no .gcda and compiles guessed; keep `-o -` (build/v/lbf10/rb.sh).
  - Next: un-drain c11 in this regime (its trace must be keyed before SE
    and nokey once nokey is hot), or a way to make the nokey block hot at
    compute_alignments without its count (none in gcc 6.2 that I found).
  Tenth pass (2026-10-26, built from C; the ninth-pass setup is now in the
  tree, build_fdo.patch is gone; scratch build/v/lbf11/):
  - The predicates: final's compute_alignments skips a block unless
    maybe_hot (count > runs and >= the summary's hot threshold), then a
    jump-only target is aligned if its incoming EDGE_FREQUENCY sum >
    freq_max / align-threshold, or freq > 10 x prev's. bbro keys
    BB_FREQ_MAX if probably-never-executed (count * 20 < runs), else -freq.
    So nokey can't be never-executed and hot; with `--runs=0` (gcda.py
    option, the summary's run count) nothing is never-executed, c11/SE/nokey
    all key 0, same ties, still matching. Then nokey needs a hot count with
    frequency 0 and an incoming edge frequency > 100.
  - Dead-edge circulation (`NK_DEAD`/`NK_LABEL`, -DBUILD_FDO only): S `if
    (nk_never2) goto nk_b;` before the pub1bl test Q (`nk_q:`), C `if
    (nk_never3) goto nk_b;` before cbVerifySig, B `nk_b: if (nk_never1) goto
    nk_q;` before the log. {Q, C, B} is irreducible (entries at Q and B), so
    no preheader takes Q's count. Overrides 16>22=9.5 17>22=82.8 22>16=99.999
    15>22=0: Q's count ~6x its real flow, the log's flow the smallest
    (gcda.py scales it to the hot threshold; frequency rounds to 0). ccp2
    folds the tests, B and C become forwarders, Q->log keeps 9.5% of Q
    (edge frequency ~104 > 100). The log edge's probability must stay under
    bb-reorder's round-3 branch threshold (10%): at 40% (v1, the B-loop only)
    nokey went to that round's heap, was re-pushed later and the fibheap tie
    popped it before SE and c11.
  With loadBl/loadBlFiles (or loadConsoleBlFiles) in C, extractSmcConfig
  was 8 lines off (both loop compares `cmp ebp,esi; jb`): ipa-split only
  considers functions with a direct caller in the TU. Fixed with
  `__attribute__((noinline))` on extractSmcConfig (ipa-split skips
  noinline functions), in the build since loadConsoleBlFiles.
- addBlsToImage (built from C, 2026-10-23; was 347; xeBuild64 0x4071d0 has the
  layout): log first, dispatch second (`if (type != 10 && type != 16 &&
  type != 24) log;` then a 10/16/6/24/else chain, type 24 logging again
  under the glitch test); threading makes the original's two test chains.
  findFile takes constants (9/15, 20/9), one inlined loop each. Skip order
  `if (xb.type == 1 && (23||25)) retail; else if (xb.type > 5) { devkit }
  else if (type == 25 && ...) xell` (8 other orders 19-244 lines). Type-23
  offset `if (glitch2mfg) +0x60; else if (4||5) +0x60; else +0x10`. `int
  off` (u32: the cmov ties off to e->offset, 241 lines). The last 8 lines
  (built from C, 2026-10-23): the xell warning block (freq 75) was under
  the round-2 threshold (84 = entry 421 x 0.2) while the original aligns
  it (so > freq_max/100 ~91, round 2, popping before the f01c found
  block). PRED_CALL (29%) fired twice on that path (the `type == 25` edge
  into the imgSize() block, then the log block). An always-true
  `__builtin_expect(type != 24, 1)` between `type == 25` and imgSize()
  gives a call-free block (28% nonequal instead of 13.7%); VRP drops the
  test. Inside the warning arm instead it matches fncmp but aligns
  L_42c2ee (only offcmp sees it). Scratch: build/v/abti/, build/v/abti2/.
- addUpdateBls (built from C, 2026-10-23; xeBuild64 0x407870, "skipping
  xell"): plain addBlsToImage-shaped source (log first, then the
  10/16/24/else imgAdd chain; findFile(9)/(15) literals; 9/23 if-chain),
  12 lines as soon as the rest of the tree was right (an earlier goto/pin
  construct was 95). The last 12 were the loop head: rotate_loop ends the
  trace at the hottest exit, and the original needs freq(bt -> body) >
  freq(head -> body). Those come from isUpdateBl's inlined profile: fold
  pairs the `||` chain into (23|15), (16|9), (10|24), 25 blocks, each with
  the early-return heuristic (39%, the last 19.9%); reassoc keeps 23 in
  the first (DOM2 shares `type == 23` with the 23 arm) and the bit test in
  the second. isUpdateBl(int type) `return __builtin_expect(type == 23 ||
  type == 15, 0) || ...` lowers the head edge (isUpdateBl still matches);
  the expect on (16|9) breaks the dispatch (86), on `type == 23` alone
  breaks isUpdateBl. Scratch: build/v/aub/, build/v/aub2/.
- loadConsoleBlFiles (built from C; was 323): loadBlFiles' recipe, a
  static `u32 loadConsoleBl(e)` helper (inlined; no ipa-cp clones, the
  loadInputFile crc==0 evaluation drops to 190). Cases 3/4/27/2 `if
  (xb.dumpX) { using } else { err; r = -1; }` (.rdata order); case 27
  re-reads `xb.files[xb.nFlashFiles]` after free; case 24 inline, not via
  loadBl60 (dom3 threading its 0/1 return zeroes the r-test frequency),
  with `__builtin_expect(xb.glitch2mfg, 0)`: the switch successors have
  equal fibheap keys and pop in reverse case order only if nothing touches
  the heap meanwhile, so case 24's trace must run into the latch (edge >=
  440, P <= 28.6%; build/v/lcb/fib.py replays a bbro dump through gcc 6's
  fibonacci_heap). `__builtin_expect(type == 9, 0)` in the 9-group puts the
  loadInputFile path in a round-1 trace so fail is connected after the r
  test. Built from C (2026-10-23, second pass, scratch build/v/lcb2/):
  - `static inline __attribute__((always_inline)) loadConsoleBl`: the
    profile is then estimated after early inlining, as if the switch were
    in the loop (186 lines without). The glitch2mfg expect goes. Bounds
    from alignment: a jump target without fallthru is aligned only above
    freq_max/100 (~95); the original aligns the case-24 tail, appendAddon,
    the cfg/smc errors and checkBl, not CF or ret0.
  - 9-group `if (r) { if (expect(type == 9, 0)) { if (suGetCF(..)) r = 0;
    } else if (type == 10) { if (suGetCG(..)) r = 0; } if (r) break; }`:
    each suGet failure stays its own fallthrough block until LRA, which
    puts the r restore there, and jump2 crossjumps the two into one block
    (the `&&` form lets LRA hoist it above `je`).
  - Case 24 copy `u8 *p = e->data; __asm__("" : "+r"(p)); e->size = 0x60;
    memcpy(__builtin_assume_aligned(p, 4), defBl60, 0x60);`: sched2 breaks
    the tie by forward dependence count, so the size store comes first only
    if it depends on the rep movsd; points-to had e {xb.files} and the copy
    {HEAP}, the asm makes it unknown; assume_aligned keeps `rep movsd`
    without the unaligned prologue (2 lines without). loadBlFiles' case 24
    probably takes the same fix.
  - `if ((u32)xb.nFiles <= 1) goto none;` before the loop, `none:
    __attribute__((cold)); return 0;` after the return: the shrink-wrapped
    `xor eax,eax; ret` gets freq 0 and pops last (4).
  - Case 2 `if (__builtin_expect(type != 2, 0)) break;` (always false, VRP
    drops it) lowers the smc error (107 -> ~105) under the cfg error, which
    tie in gcc 6's fibheap otherwise (287 without; build/v/lcb2/rep.py,
    sweep.py, r3sim.py replay keys).
  defBl60 is named in split.py's SYMBOLS (0x44a700).
- encodeBls (built from C; was 1048): `if (xb.type == 2) {JTAG} else if
  (xb.type > 3) {...} else {...}` (`<= 3` is 50/50; tested first, prev_bb
  pulls it into the hot trace). Type 24 is a guarded log before each switch
  (`if (type != 24) log;` + `case 23: case 24: case 25: break;`; `<= 3`:
  `if (type != 24 || xb.glitch2mfg)`), not a `continue` (957 -> 34): VRP
  threads type==24 past the switch and the profile update empties the
  switch-to-latch edge, so the latch follows the kvPrepare trace instead
  of rotating the loop. `j = findFile(N);` before each call (JTAG case 1
  keeps it inline). `u32 cbb` in struct xebuild (uncprop reused the zero
  cbb register for a findFile loop's `i = 0`); `u16 cfEncrypt` (as keys.c;
  `movzx eax,ax`); `int ldv` parameter (`add [esp+100],eax`; buildFlash
  loses its `movzx esi,si`). f01c tail `e = &xb.files[findFile(14)]`.
  Left: 3 `cmp i,n` vs `cmp n,i` in inlined findFile loops (16, 13, 9):
  the original's ch2 preheader copy of nFiles has a lower SSA version (free
  list) than i; ours are fresh names. ~40 neutral variants don't move it;
  no-early-inlining breaks the layout (1542). Second pass (2026-10-23,
  scratch build/v/ebl2/: chmap.py prints ch2's new<-old name table):
  ch2 pops a LIFO free list (names freed after VRP1, then VRP1's
  ASSERT_EXPR names in reverse bb order, then older names), handling the
  f01c tail loops first, then the main loop, then the 24 switch loops; n'
  is each loop's second name. Asserts take the names free at VRP start:
  ours has one (fre3 frees 26, 24 of them degenerate `i = PHI <0>` in case
  blocks, but cleanup removes those forwarders and loop_optimizer_init
  recreates 24 preheaders, using them up). The original needs ~17 free
  then: a structural difference before VRP. One dead store (`if (i < 1)
  xb.cfLdv = 0;`) moves the one low name onto a single target (4 lines);
  two or more flip the tail loops instead (all 780 pairs of 40 positions
  tried, >= 2 left). Built from C (2026-10-24): a `static int
  findFileN(type)` helper that reads `n = xb.nFiles` before its loop, used
  for those three lookups: n gets an early, low SSA version that ch2 never
  copies, so the compare is `cmp n,i` with otherwise identical code (no
  free-list games needed; try it for other inlined findFile loops). The
  link then showed one byte fncmp/offcmp miss: the f01c tail's `je` went
  past the `xor eax,eax` of `return 0` (uncprop reused the zero f01c for
  the return); `u32 f01c` in struct xebuild keeps the constant (every other
  user still matches). defPayload/defCore are named in SYMBOLS.
- buildFlash (built from C, 2026-10-23; was 2473; hot path offsets match to
  0x12fb, .rdata order exact): image_write prototypes now use the SYMBOLS
  names (`imgAddRaw` must stay void: int costs 20); `int mobile[11].size`
  (signed cmovg); `u8 anchor[0x1b]` (OFFSET _mmcAnchor, anchorNum at
  +0x1b); `encodeUpdateBls(int, int ldv)` (u16 puts a movzx before the
  call; still matches). `struct fileent f` scoped per block (shares the
  inlined SYSTEMTIME's slot: 1180-byte frame); no tmp/name locals
  (`xb.files[xb.nFlashFiles]`, `xb.firmware[i]` re-read; a name local made
  a cast pseudo, ~150 lines). Firmware: one shared first load then `if (r
  && last == 'p')` (the non-p edge loses PRED_CALL, p 28%, cold p-chain).
  Security loop `for (k...) { ...; if (k) log("\n"); }` with a found flag.
  Mobile a switch on k. fuse `if (__builtin_expect(type == 4 || type == 5,
  0)) fuse = 1;` is a hint (else setne sinks, 171); `!(xb.type == 1 ||
  xb.type > 5)` for SSA numbering (166). Built from C (2026-10-23, second
  pass, scratch build/v/bfl2/):
  - Security not-found group: its entry must have frequency in (153, 188)
    to land in round 3 between patchBlsResign's `return 1` (188) and "could
    not read file" (153). The SUPD fallback sets `found` with no `goto
    got`, then `if (!found) { flashBuf ... else secdata/extended ... }`: a
    test on a PHI of constants gets no prediction (50%), halving the
    flashBuf block (1945 -> 1137, x 15% pointer heuristic = 170); threading
    removes the test later.
  - blmod: `if (!loadBaseFile(...)) {...} else patchConsoleBlmod();`, a
    static void helper (IPA-inlined: PRED_CALL on both arms, 50/50, found
    falls through by prev_bb) whose early return after the NULL patch puts
    the early-return predictor on that arm (console arm 39%, freq 8.6, above
    the findFile(9) zero-trip block's 7).
  - `int i` (fuse findFile(24) loop compare) and the void helper
    (findFile(27)): ch2 copies loop headers in a fixed order taking names
    LIFO from the free list (copyprop1/phiopt1 frees, VRP1 threading PHIs);
    type swaps are a cheap search for it (build/v/bfl2/sig.py, names.py).
  - ipa-cp: with buildFlash and loadConsoleBlFiles in C, loadInputFile's
    crc==0 clone evaluates 509 > 500 (freq_sum 4101: buildFlash's rawpatch
    2.17 and firmware 1.71 calls) and loadLocalFile, loadConsoleBlFiles and
    buildFlash move. No source shape lowered those calls without moving the
    layout, so loadInputFile is `__attribute__((noclone))` (the original
    has no clone; noclone only stops the copy).
- Whole object in C (2026-10-26, no build.s): build.c keeps the mixed
  file's code; functions in the original order (static helpers before their
  first user), strings as static arrays in .rdata order before the first
  function using them, `aligned(4)` from 31 bytes else `aligned(1)`, .data
  arrays defined in order, all under `-fno-toplevel-reorder`. loadBlFiles
  still comes from the -DBUILD_FDO compile, spliced in with `re/splice.py
  --whole` (function chunk to .cfi_endproc, so its jump table and FDE come
  along). That compile needs `-ftoplevel-reorder`: under
  -fno-toplevel-reorder the NK_DEAD statics aren't read-only to
  ipa-reference and ccp2 keeps their tests. The "jmp _patchPayloadSize" at
  0x42ced1 was gas's long-padding jump, not code. The old patch's .text
  0x20 deficit was loadBlFiles (unsolved then).

## app/image_write.c

**Done (2026-10-27): whole object in C, no `.s`.** `src/app/image_write.c`
is the draft itself (`wip/app/image_write.c`, the same file), built with
`-O3 --param builtin-expect-probability=50` in gcc's default top-level
order. What the last step needed (README has the summary):

- imgWritePage is not a function of the source: it is imgAdd's ipa-cp
  clone for len 0x1000, type 1, pad 0 (addSmcConfig's and imgAddRaw's
  calls are `imgAdd(off, src, 0x1000, 1, next, 0)`). Type 1, not 0: the
  partial page count gives the 8 pages per block. Evidence: with gcc's
  clone the three clones come out in the original's `.text` order
  (ipa-cp makes off 0, then len 0x1000, then type 0; ipa_reverse_postorder
  visits local nodes newest first, so expansion emits them oldest first);
  the hand-written function (static) was always emitted first. The clone
  was 55 lines from the original with type 0 and 4 with type 1 before
  any pin work. The old dead `len++` pin at the top of imgAdd's block loop
  had hidden len from ipa-cp (a modified parameter gets no predicates):
  len 0x1000's evaluation 9 -> ~5900 without it.
- New clone names: imgWriteStart `.constprop.1`, imgWritePage `.2`,
  imgWriteAt `.4` (type 42's clone, inlined into imgAddFile, is `.3`).
- imgAdd's dead pins were re-laid out by a randomized search
  (tmp/image_write_agents/fin4: `score.py` = one compile + fncmp of all
  46 + opcmp + ipa-cp evaluations; `anneal.py`/`fcd.py` over `<<<a@@b>>>`
  templates made by `mk3.py`). The winning set: `x > first + 0x4000`
  `blocks += 2` before the memcpy, three in the block loop (`__asm__("")`
  bodies and one `blocks++`), one in the FS loop, one before the end
  marker test (`start++`) and `blocks += 2` before `imgEnd =`; no
  `int dmy`.
- imgAddFile's range test (the inlined imgAdd's `raw < off || raw < off +
  len`, combined by ifcombine): the original tests `off + len > raw`
  first. Two things: the operands' order is SSA version order (forwprop
  canonicalises), and VRP1's jump threading of the two dead `len & 0x3fff`
  tests copies the block after the head `len++` pin, so anything computed
  there (imgFits' sum and limit) is renumbered above the inlined rawSize
  load. So imgAddFile computes `lim` and `end = off + len` before the pin,
  end kept alive by `__asm__("" :: "g"(end))` (DOM2 later replaces the
  inline's own off + len by it). The order of the two tests is the order
  of the two SSA names ifcombine pops from the free list: copyprop1
  releases its dead PHIs in reverse dominator order, so the names come
  from the inlined imgAdd's dead-pin PHIs (imgAdd's pin layout decides).
- imgAddFile's error block: the dead test in the fits body is threaded
  away by VRP1, which multiplied the fits edge by the dead test's 50%
  (error edge 75%, so bbro made the error block the head's fallthrough).
  A `cold` label in the dead arm keeps the fits edge likely.
- finalizeImage's literals come out in statement order (not layout
  order): the donor block-style mismatch error is the outer if's else, and the
  remap loop's "not sane" error comes before the "not required" arm.

Before (mixed object): the 45 matching functions built from
`src/app/image_write.c`, a mixed object made by `python wip/mixed.py app/image_write <fns>` (its OBJS entry
turns the draft's `copyright` and `mobileOffset` definitions into
externs; the `.s` keeps the data). imgWriteAt (0x40eef0) is gcc's ipa-cp
clone of imgAdd for type 0, pad 1, built as `_imgAdd.constprop.3`, and
imgWriteStart (0x40e950) the clone for off 0 as well,
`_imgAdd.constprop.1` (see the findings): the
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
- imgWriteStart (regparm src, len, next) is imgAdd's ipa-cp clone for off
  0, type 0, pad 1 (built 2026-10-27; agent log and tools in
  `tmp/image_write_agents/imgWriteStart/`). Its three callers
  (writeInitialHeader's 0x1ffb call, checkBootImage's two) call
  `imgAdd(0, ..., 0, next, 1)`; writeInitialHeader's big-block call
  stays imgWriteHdr (the original inlines that one). ipa-cp clones the
  off 0 value only at an evaluation >= 500 (the default
  ipa-cp-eval-threshold), and off 128 (netKd's calls) must stay below.
  The old body gave 395/166; two dead `if (x > 0x3fff) blocks++; /
  start++;` at the top of the block loop add ~19 time each (585/246),
  pins in the page loop would add ~188 each (off 128 cloned too). With
  a third dead `start++` at the top of the FS loop and three dead `if (i
  != 16) off++;` in writeFsTable (the old three head pins in imgAdd
  removed), SSA numbering gives the original compare operand order in
  both clones and writeFsTable. The off-0 clone is made first, so
  imgWriteAt became `.constprop.3`. A route with `--param
  ipa-cp-eval-threshold=300` (155..365) also works, not used.
- Draft base after that (2026-10-27, one agent for both imgAdd and
  imgAddFile; log and tools in `tmp/image_write_agents/addpair/`):
  standalone imgAdd 93 -> 12 lines, imgAddFile 256 -> 45, everything
  built still matching (off 0 / off 128 evaluations 563 / 237). What
  changed:
  - Spare stores through per-layout structs (`struct spb` big block,
    `struct sps` small): in `struct sp` b1lo..b2hi share one bitfield
    representative, so the b2lo store had no MEM_EXPR and sched2 couldn't
    move `cmp type,1` above it.
  - Dead pins: `if (x + 0x4000 < first) blocks++;` (twice) and `if ((len
    & 0x3fff) > 0x3fff) start++;` at the top of the block loop, `if
    (first > 0x4000) blocks++;` before the memcpy and one more `x + 0x4000
    < first` before `imgEnd =`. Pins computing `first + 0x4000` in the loop
    add ~120 to the off 0 evaluation each; `x > 0x7fff`, `(x >> 14) != 0`
    and `x == 0x4000` fold away early. The FS-loop pin and writeFsTable's
    `if (i != 16) off++;` pins are gone.
  - imgAdd setup: `t = type - '1'` and `partial` first in the loop body,
    `pg = len / 512 + 1; pages = pg;`, `int left`, `npages, pages`
    declaration order, an unused `int dmy;`, and `__asm__("" ::
    "g"(t))` first in the `t < 15` block (dead in every clone; t/partial
    slot order in the standalone).
  - A hot label on the `else` of `if (!partial) npages = 32;` (imgAddFile
    137 -> 45: DOM2's threading no longer zeroes the npages guard edge,
    so the block loop isn't rotated).
  - imgAddFile: `int nFsFiles` is a global (mixed.py OBJS subs makes it
    extern; the original reloads it after the clone's calls), the block
    number `SWAP16((u16)(off >> 14) - xb.fsStart)` (16-bit subs, no rol),
    one dead `if ((len & 0x3fff) > 0x3fff) off++;` before the imgFits
    test.
  Left in imgAdd: `left = (pages + 4) & -4` is expanded before `len >> 8`
  and the `type - 42` test (lim2 hoists the diamond's then-block right
  after the setup; the original hoists it after ivopts), so len >> 8 gets
  eax, not ebx. Every spelling of the rounding, other types for left and
  setup temporaries were tried (`addpair/tiny/` is a small repro). Left
  in imgAddFile (ties): the bigBlock test's peephole2 scratch (edi, the
  original edx), the range test order, the npages/pages cmov form
  (`lea edx,[edi+512]; cmovne`), the end marker's register and the ERR
  block before the small-block call.
- imgAdd builds from C (2026-10-27, `tmp/image_write_agents/addpair2/`).
  lim2 walks a loop's blocks in inverted postorder with siblings sorted
  so that a then-block whose only successor is the join comes first, so
  the `left` diamond's then-block was hoisted before every inner-loop
  invariant. Its PHI is left for lim4 (after ivopts) only while it is
  expensive (determine_max_movement: costs of dependencies in the same
  loop accumulate). The fix: the outer body computes only npages
  (`if (len % 512) npages = (len + 512) / 512; else npages = len /
  512;`), the inner loop computes `pages = len / 512; if (len % 512)
  pages++;` after `s = ...`, the small arm stores `32 - pages`, and
  `left = pages; if (left & 3) left = (left + 4) & ~3;` opens the big
  arm's `type != 0x2a && type != 0x2c` block. The pins were retuned:
  `if (x > first + 0x4000) blocks++;` before the memcpy and before
  imgEnd, `if ((len & 0x3fff) > 0x3fff) len++;` at the top of the block
  loop with the two `x + 0x4000 < first` ones, and imgAddFile's pin is
  `len++` (evaluations 559 / 235). imgAddFile is then 30 lines: the
  pages cmov form is fixed by the inner-loop pages.
- imgAddFile draft (2026-10-27, 24 lines, `addpair2/FINAL.c`): fits-first
  `if (__builtin_expect(imgFits(off, len), 1)) {...} else log_printf(...)`
  with dead `time++` pins in the head and at the top of the fits body.
  peephole2 picks scratch registers with a static search offset that
  carries across insns and functions (blocks walked in reverse layout
  order); the body pin makes VRP1 rebuild the strcpy/bigBlock-test block
  last in the layout, which gives the original's edx (bigBlock test) and
  ecx (end marker), so function order matters for the whole-C build.
  Left: the ERR block lands right after the head (the original has it
  after the end-marker block, before the small-block call; 18 lines) and
  the range test checks `off` first (original `off + len`: ifcombine
  builds `a | b` from recycled SSA names, forwprop sorts by version).
  Every form found trades the ERR placement against the registers:
  with a body pin registers are right and ERR wrong, without one the
  reverse; fits-first without the expect, or hot/cold labels on the
  bigBlock arms, place ERR right but shift the head's RA.
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
- finalizeImage built (2026-10-27; agent notes and offs.py, an
  instruction-offset check against the original, in
  `tmp/image_write_agents/finalizeImage/`). The ECD loop names `xb.hdr +
  ...` / `xb.spare + ...` at each use; the big-block LBA loop is `spare =
  xb.spare; s = spare + b * 0x1000 + p * 16` (end-pointer outer IV). The
  ECD memcpy's unknown-alignment prologue: malloc goes through `void
  *xmalloc(size_t) __asm__("_malloc") __attribute__((malloc));` (same
  call and points-to, but CCP gives MALLOC_ABI_ALIGNMENT only to calls
  gimple_call_builtin_p accepts, and ivopts keeps alignment on new IVs,
  so no loop form loses it). Its result goes to `void *mem` and the loop
  pointer is `raw = (u8 *)mem`: the types differ, so out-of-SSA doesn't
  coalesce them (own pseudo, spilled to [40+esp]) and the 4-insn
  preheader is too costly for ce1 to hoist the hdr/spare loads above the
  `xb.blocks` guard. `int size` (printf takes the int PHI, the multiplies
  the u32 one: size and blocks each live in two places). Remap loop: only
  `from` is a local and the test reads `xb.remapTo[i]` (two locals fold
  `&&` to `&`, one branch at 29% and a rotated loop); the products are
  computed before the copy printf and `u32 off` before the zero-fill
  printf (otherwise LRA saves `from` across the call). One pin, `__asm__(""
  :: "a"(xb.hdr));` before the memcpys, settles the ECD loop's register
  ties.
- writeFsTable built (2026-10-27; notes and a jump-target comparer in
  `tmp/image_write_agents/writeFsTable/`). `setBeU16(blk, ...)` with blk
  from the realign (PRE would merge imgAdd's `start` into a shared `off >>
  14`, the original recomputes it); the call's len is `i * 0x400` after
  the 16-iteration copy loop, known only at VRP1 (a constant len lets FRE3
  merge imgAdd's `off + len` with the log's `off + 0x4000`, and ifcombine
  joins the two range tests); the two imgAdd calls as `if (!xb.bigBlock)
  goto small; <big call>; goto done; small: <small call>; done:` (same
  blocks, but VRP1 visits the paths the other way, so the small path's
  `blocks` isn't widened to VARYING and the vectorizer leaves that FS loop
  alone); `optimize("no-tree-scev-cprop")` on writeFsTable; and a
  never-taken `if (i != 16) off++;` before the log, a numbering pin (VRP1
  deletes it; it makes ivopts give the big path's inner counter a recycled
  SSA version above its bound, so forwprop4 orders the compare as the
  original). The count of such pins is tuned together with three dead
  `if (x > 0x3fff) start++;` right after `first = ...` in imgAdd (x is
  `off & 0x3fff`), which shift the free SSA list so the clone's chain-loop
  bound is `ivtmp + blocks` (`lea ebx,[eax+esi]`; fncmp doesn't see that
  operand order, `tmp/image_write_agents/opcmp.py` and the build do; two
  imgAdd pins with four writeFsTable pins also work). Shared imgAdd body
  changes that came with it (the clone still matches): `start = (off - x) >> 14`
  (x gets a second use: combine keeps `and eax,16383; test`), the tail as
  if/else, the LBA stores through `struct sp` bitfields (`b2lo`/`b0`,
  `b1lo`/`b5`) plus `s[1]`/`s[0]`, `s[9]` before `s[5] = 1` in the
  bigBlock arm and `s[12]; s[9] = sp9; s[2] = 1;` in the small arm (sched2
  breaks ties by source order).
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
