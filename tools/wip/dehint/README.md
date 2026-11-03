# Removing compiler tricks, one function at a time

The `moderate` files in README.md's "Compiler tricks by component" should build
with plain `-O3` and source shape alone. Each function is worked on by one agent
at a time, and an attempt that doesn't match is retried from the notes here.

## Queue

Status is `open`, `MATCH` (draft matches, not landed), `landed <commit>` or `parked`.

| # | Object | Function | Tricks to remove | Status |
|---|--------|----------|------------------|--------|
| 1 | fileutil | readFileIn | 2 expect, pin on edi/ebx/esi, rf_hint, no-early-inlining | landed 454b47d |
| 2 | fileutil | myatou32 | dead `'X'` test | landed b17d678 |
| 3 | console_hdd | sendAvatarData (inlines prepSysex) | 2 expect, literal asm, pin, assume_aligned, align-loop-iterations | landed at the user's request; retry for natural code later (see its notes) |
| 4 | net | netRecvVerbose (netRecv is its clone) | `got` pin (expect removed, 6d5d62b) | parked with the pin after 8 attempts, at the user's request (see its notes) |
| 5 | net | netWriteBlocks | no-crossjumping, no-early-inlining | open |
| 6 | net | netSendFile | no-crossjumping, expect, `buf` pin | open |
| 7 | net | netWritePatches | no-early-inlining | open |
| 8 | bootloaders | cfDecrypt | no-tree-dominator-opts, no-tree-vrp | open |
| 9 | bootloaders | daeVerifySig (inlines daeSigCheck where used) | no-early-inlining, hint(), literal asm, always_inline on daeSigCheck | open |
| 10 | bootloaders | cbDecrypt | no-tree-dominator-opts, no-cse-follow-jumps | open |
| 11 | bootloaders | cdDecrypt | no-tree-dominator-opts, no-cse-follow-jumps | open |
| 12 | bootloaders | ceDecrypt | no-tree-dominator-opts, no-cse-follow-jumps, pin on len/hmacKey | open |

When the last hint in an object goes, its `--param` options in `build.sh` go too
(they only act on `__builtin_expect` and loop alignment).

## What counts as a MATCH

All of these, for the function and anything inlined into it:

1. `python tools/re/fncmp.py <file> <name>` prints MATCH with **no flags** passed.
   For a clone, set `FNCMP_GCCSYM`. `--param` and `-f` flags don't count.
2. No hint from README.md's list: `__builtin_expect`, hot or cold labels, guarded
   hint calls, `__builtin_constant_p`, `__builtin_unreachable`, dead tests or
   blocks, empty `asm`, `optimize` or inlining attributes, asm-label prototypes,
   `__builtin_assume_aligned`, `__builtin_prefetch`, `register` variables, or
   anything else whose only job is to steer gcc.
3. The source reads as code someone would write. Types, scopes, loop forms,
   helpers, statement order, declaration order and `goto` are all fair game.

A hint moved elsewhere, or disguised as ordinary code, isn't a match. Report what
actually happened: a near miss is a near miss, however close.

Live but redundant code that reads naturally is acceptable and lands, flagged for
the user's review. `myatou32`'s `BOOL hex` flag is the approved example: one `if`
sets it and the next tests it. Source that compiles to the right bytes but no one
would write is a candidate, not a match: for example a `for (;;)` entered and left
through labels, or a helper that exists only to change an SSA number. Save a
candidate as `drafts/<obj>_<function>_candidate.patch`, leave `src/` unchanged, and
report it for review.

## Landing a MATCH

Copy the shape into `src/<obj>.c` and run `sh build.sh`. The SHA256 must still be
`10dac648197fa5cdbb82d975ab9ff11f64075c9686908dfd9a33edc533f1971c`. fncmp doesn't
see `.rdata` order or alignment, and other functions in the object can move, so a
function isn't done until the full build matches. If it doesn't, restore
`src/<obj>.c` and record why in the notes.

## Notes

Each function has `notes/<obj>_<function>.md`. Read it before starting, and
append to it as you go, not only at the end, so a stopped attempt loses nothing:

- each shape tried, or the generator's axes, with its diff size
- the best source so far, saved as `drafts/<obj>_<function>_best.c`
- which gcc pass decides the remaining difference, and how you know
- what to try next, and what not to bother retrying
