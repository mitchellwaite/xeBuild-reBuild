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

- `optIniBool` (22 lines; 6 with a `long` return): register choice in
  `(bootFlags & ~clear) | set`.
- `applyIniOptions` (924): the "already set" path must be the likely one.
  Guarding each call in the caller with `if (!(xb.bootFlags & bit))` (the
  call heuristic) and `switch (xb.type) { case 2: }` (no == heuristic)
  fixed most of the layout.  Next: noecdremap (bit 31), the xellbutton
  registers (ebx vs edx), and the later off-trace blocks.
- `parseOption` (454): block layout (gputemp's body is placed after the
  error blocks in the original).  The u32 return/validateString prototypes
  stop the return value living in esi, but they cost parseCmdOptions 15
  lines (it matched with an int return).
- `loadAddons` (11): the original keeps j=0 in eax across the over-limit
  warning (caller-save); ours rematerialises it.

Findings:
- 449640 is `parseButton.part.N` (ipa-split of a single parseButton with
  an if/else chain).  gcc puts it in `.text.unlikely`; split.py calls that
  piece `.text.startup`.  The real i386pe script merges `*(.text.*)` in
  object order, so link.ld needs `*(.text.*)` instead of
  `*(.text.startup)` when this object is built from C.
- The temperature/fan/region fields must be u32 (an int would let the
  -1 default reuse the loaded value).
