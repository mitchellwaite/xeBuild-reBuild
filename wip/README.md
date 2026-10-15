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

Draft of the whole object (it can't be a mixed object: every function
uses string literals).  As of this draft, matching with `re/fncmp.py`:
parseButton, baseFileExists, perboxExists, iniConsoleType, setConsoleType,
optIniInt, stripColons, macidSet, parseRawPatch, parseRawPatches, addPatch.
setBoolOption's 4 lines are ddisasm writing 0x400000 as `__ImageBase`
(really a match).  Still off:

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
  - Also off: the xellbutton registers (ebx vs edx) and the dualboot /
    type reload (`mov edx,[type]` kept for `cmp edx,2`).
- `parseOption` (454): block layout (gputemp's body is placed after the
  error blocks in the original).  The u32 return/validateString prototypes
  stop the return value living in esi, but they cost parseCmdOptions 15
  lines (it matched with an int return).
- `loadAddons` (11): the original keeps j=0 in eax across the over-limit
  warning (caller-save); ours rematerialises it.  That spill also blocks
  the head merge of `lea eax,name; mov [esp+8],eax` above the `jg`, which
  is the other half of the diff.  Moving `j = 0`, a pointer instead of an
  index, unsigned j and a do-while made no difference or worse.

Findings:
- 449640 is `parseButton.part.N` (ipa-split of a single parseButton with
  an if/else chain).  gcc puts it in `.text.unlikely`; split.py calls that
  piece `.text.startup`.  The real i386pe script merges `*(.text.*)` in
  object order, so link.ld needs `*(.text.*)` instead of
  `*(.text.startup)` when this object is built from C.
- The temperature/fan/region fields must be u32 (an int would let the
  -1 default reuse the loaded value).
