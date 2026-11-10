# Borderline shapes awaiting review

No file has compiler tricks any more (README.md, "Compiler tricks by component"). What is
left are **borderline shapes**: ordinary C that an author could have written, but that is in
the source because of what gcc does with it. They aren't counted as tricks. Each one is for
the user to review: keep it as the author's likely shape, or try for a plainer one.

State: commit `4c1e221d` (2026-11-10). Line numbers are that commit's and will drift; the
tags don't:

```
grep -n "Borderline, for review" src/*.c
```

There are two kinds of item here:

1. **Tagged shapes** (39): each has a `Borderline, for review:` comment in the source saying
   what it does and what it replaced.
2. **Redundant file-local definitions** (not tagged in the source): declarations and
   definitions at file scope in a `.c` that the code doesn't need. The user counts these as
   borderline too. See the second section.

When an item is settled, delete its tag (or mark it `(approved)`) and update this file.

## 1. Tagged in the source

### build (16) — `src/build.c`, notes in `notes/build.md`

| Line | Where | Shape | It replaced |
|---|---|---|---|
| 379 | `align16` | a natural helper, kept so it stays a call until the early inliner | no-early-inlining on `patchBlsBlmod` |
| 401 | `findFileOffset`, `findFileSize` | return `int` like `findFile`, though the values are offsets and sizes | a register pin |
| 458 | `loadFileCrc` | the pad test repeated to pick the log; `size != e->size` can't be false there | an expect and a pin |
| 564 | `loadInputFile` | `crc` is an `int` parameter on purpose (`uint32_t` makes ipa-cp clone it) | a noclone attribute |
| 827 | `patchCpuFan` | repeats the caller's `xb.cpuFan != 0xffffffff` test | no-early-inlining and 4 hint calls |
| 941 | `extractSmcConfig` | `size` is an `int` on purpose; a struct copy where `memcpy` would do | (18 lines off otherwise) |
| 1215 | `useBuiltIn` | helper that shares two copies, chosen for IPA's inline order | a hot label and an asm barrier |
| 1231 | `defaultBl60` | `memmove` where `memcpy` would do, and not through `useBuiltIn` | a cold label and a precheck |
| 1264 | `loadBl24` | two calls where `\|\|` would do | a pin and an assume_aligned |
| 1279 | `setKitBuild` | its status return is ignored at the only call site | an expect and the `--param` |
| 1344 | `loadBlFiles` | `(int)r < 0` where `r != 0` says the same | |
| 1364 | `loadBlFiles` | `loadBl24`'s body written out, not called, with a leading `r = 0` | (25 lines off when called) |
| 1445 | `loadBlFiles` | the fallbacks as a sequence of `r` tests, where an `&&` chain is the same | a register pin |
| 1935 | `addBlsToImage` | xell (25) tested before the patches (23) in both skip tests | (63 lines off the other way) |
| 1985 | `isUpdateBl` | the 23 and 15 tests as ifs of their own, not in the `\|\|` chain | |
| 2494 | `initFlash` | helper for the salt clear and the virtual-fuse decision; its final `fuse & 1` is redundant | an expect |

### options (5) — `src/options.c`, notes in `notes/options.md`

| Line | Where | Shape |
|---|---|---|
| 503 | `parseOption` | cputemp and gpufan set an `ok` flag in the log's `if` and leave on it after, where the other value arms `goto bad` first |
| 511 | `parseOption` | a bool option sets `ok` and `if (ok) return 1;` comes after the value options, where a `return 1` in the arm would do |
| 521 | `parseOption` | macid's last five bytes go through a helper called once with the count 5 (`macidRest`) |
| 526 | `parseOption` | the unknown-with-value message tests `val && vlen`, where `vlen` alone decides |
| 717 | `parseCmdOptions` | returns `uint32_t` like `parseOption`, so its `return 0` reuses the call's 0 |

Attempt 30's lead applies here: these came from fitting to counts that may not be the
original's. Worth one attempt from the natural `parseOption` before accepting them.

### image_write (4) — `src/image_write.c`, notes in `notes/image_write.md`

| Line | Where | Shape |
|---|---|---|
| 540 | `imgAdd` | `partial > 0` on a 0-or-1 flag, where `if (partial)` says the same |
| 577 | `imgAdd` | `int used[2] = { .., 0 }`: one entry longer than needed (also a `TODO`; not counted, by the user's rule on over-long arrays). It sets a compare's order in `writeFsTable` |
| 590 | `imgAdd` | redundant `(int)pages` casts, and `len >> 9` next to `len % 512` (also a `TODO`) |
| 1005 | `finalizeImage` | `pageErased(..) <= 0` on a 0-or-1 result; `calcPageEcc` written out though the function exists; `xb.spare` and `xb.hdr` re-read after the stores; `const` on `q` and not `h` |

### net (4) — `src/net.c`, notes in `notes/net_*.md`

| Line | Where | Shape |
|---|---|---|
| 137 | `netRecvVerbose` | the select failure leaves through `size = got` and `if (got >= size) return NULL`; `status != 1` where `!status` says the same |
| 533 | `netWriteBlocks` | `netSendStr(cmd) <= 0`, though it only returns 0 or 1 and the file's other tests use `!` |
| 599 | `netSendFile` | redundant `ok` flag (`if (name && buf) {` is the same logic), and the same `<= 0` |
| 728 | `netWritePatches` | the same `<= 0` |

### keys (3) — `src/keys.c`, notes in `notes/keys.md`

| Line | Where | Shape |
|---|---|---|
| 649 | `kvPrepare` | two `alt` tests at the end where one if/else would hold `kvSet` and both encrypt calls |
| 839 | `daeEncrypt` | a bad header ends the loop with `off = size; len = 0;`, and the warning sits in the loop's exit arm, not after the loop |
| 897 | `fcrtEncrypt` | the encrypt calls written out in both arms, where an `\|\|` would need one copy |

### console_hdd (2) — `src/console_hdd.c`, notes in `notes/console_hdd_sendAvatarData.md`

| Line | Where | Shape |
|---|---|---|
| 321 | `prepSysex` | `r` kept as a flag with a second `if (r)`, where the mount arm could return `createSysexDirs()` itself |
| 346 | `sendAvatarData` | returns `long` next to `netSendFile`'s `int`; a failed send ends the loop with `i = consoleManifest.count`, not `break` |

### mode_client (2) — `src/mode_client.c`, notes in `notes/mode_client.md`

| Line | Where | Shape |
|---|---|---|
| 125 | `clientInfo` | redundant `return;` at the end of the function |
| 442 | `clientBinPatch` | redundant `return;` with nothing after it but the else arms |

### One each

| File | Line | Where | Shape | Status |
|---|---|---|---|---|
| `src/image_read.c` | 239 | `getImageSmc` | dead `excess` addend, always 0 (the head comment at line 176 also has a live but redundant `addr != lim` / `addr >= lim` pair) | kept and not counted, by the user's call |
| `src/filelist_ini.c` | 697 | `findKey` | dead `key == NULL` test | approved: the author may well have written it |
| `src/fileutil.c` | 307 | `myatou32` | `BOOL hex` set by one `if` and tested by the next | approved 2026-11-02 |

## 2. Redundant file-local definitions (not tagged in the source)

**These are borderline items too** (the user's call, 2026-11-10): a declaration or
definition at file scope in a `.c` that the code doesn't need. The original author may have
had them, they may be leftovers of the reconstruction, or they may matter to gcc.

The list comes from a syntactic scan, `python tools/wip/dehint/localdefs.py`. **None of them
has been tested**: nobody has yet removed one and checked whether the bytes change. That is
the first thing to do with each (compare the object with `build/obj/<obj>.o`, then
`sh build.sh`). CLAUDE.md also says exported prototypes belong in `src/<obj>.h`, not in a
`.c`.

### Forward prototypes of functions defined before their first use (36)

The definition comes first, so the prototype does nothing for the C.

| File | Lines | Functions |
|---|---|---|
| `src/image_read.c` | 37-57 | 21: `fsFindFile`, `loadFlashFile`, `findAnchor`, `mmcFindMobiles`, `spareVersion`, `showMobilePages`, `scanMobiles`, `setFsOffset`, `findFsRoot`, `imgGetSecurityFiles`, `findSmcConfig`, `checkBlock`, `addRemap`, `findFreeRemap`, `notZeropair`, `spareLbaOk`, `copyMmcImage`, `parseDump`, `detectController`, `checkHeader`, `getNonces` |
| `src/mode_client.c` | 17-21 | 5: `client_usage` (its `noreturn` attribute went in `4c1e221d`), `dumpKey`, `checkPatches`, `updatePatches`, `patchNand` |
| `src/filelist_ini.c` | 63, 163-165 | 4: `iniPreParse`, `memFindStr`, `memFindChar`, `checkFileCase` |
| `src/build.c` | 27, 370 | 2: `showSmcConfig`, `patchSmcConfig` |
| `src/bootloaders.c` | 16, 331 | 2: `fcrtVerifySig`; `cbDecrypt`, whose prototype is the line right above its own definition |
| `src/keys.c` | 17 | 1: `cfPatchSlots` |
| `src/mode_update.c` | 25 | 1: `getSecurityFiles` |

### Other redundant definitions

| File | Line | What | Why it's redundant |
|---|---|---|---|
| `src/image_write.c` | 48 | `#define ALIGN_BLOCK(x)` | never used |
| `src/image_write.c` | 51 | `#define setSpareLba(sp_, block)` | never used |
| `src/fileutil.c` | 19-21 | `typedef int BOOL`, `#define TRUE 1`, `#define FALSE 0` | local copies of standard names, there for `myatou32`'s `hex` flag and a few others |
| `src/image_read.c` | 35 | `int fseeko64(FILE *, long long, int)` | a local prototype for a libc function |
| `src/net.c` | 24 | `extern time_t netTimeStart;` | declares a `src/globals.c` global in the `.c`, not in a header |
| `src/filelist_ini.c` | 61-62 | `extern` for `consoleNames` and `validChars` | both are defined later in the same file |

### Needed where they are, but could move to a header

The first use comes before the definition, so these prototypes are needed unless a header
declares the function: `loadFileCrc` (`src/build.c:371`) and `pageErased`
(`src/image_write.c:36`).

### Related, for the same review (not file-local, or not strictly redundant)

- **Byte-swap spellings.** `src/xebuild.h` has four spellings of one 32-bit swap (`SWAP32`,
  `SWAP32_BUILD`, `SWAP32_IMAGE_WRITE`, `SWAP32_KEYS`) and four of the 16-bit one, and
  `src/image_read.c:18` has its own `ROT16`. Each object needs its spelling to match;
  README.md counts a byte-swap spelling as source shape.
- **Views of the 16 spare bytes.** `src/image_write.c:28-34` defines `struct spb`, `sps`,
  `sp`, `spt` and `spare`, and `src/image_read.c:793-809` defines `bigSpare` and
  `smallSpare`, for the same data.
- **`#define netRecv(len) netRecvVerbose(len, 0)`** (`src/net.c:219`): a macro where the
  binary has a function (gcc's clone of `netRecvVerbose` for `verbose` 0).

## 3. Settled, so not to be raised again

- **mode_client's four static helpers** (`bpArgs`, `wbArgs`, `oneArg`, `fileArg`,
  `src/mode_client.c:505`): not borderline, by the user's decision; the tag was dropped in
  `ee5d2d26`. Replacing them with `getArgs` is a parked question
  (`notes/mode_client.md`, "Attempt 17, second part").
- **`client_usage`'s `noreturn` attribute**: removed in `4c1e221d`, same bytes. No
  `__attribute__` is left in `src/`.
- **options**: the `INI_INT` macro, `parseButtonPart`'s always-0 argument and `optIniBoolG`
  went in `e8c0b8d8` (attempt 30).
- **`__builtin_bswap16/32/64`** in `src/fileutil.c` and `src/build.c`: byte-swap spellings,
  source shape.

## How to work an item

1. Read its comment and the notes file named above; the don't-retry lists say what has
   been tried.
2. Change the shape, compare the object with `build/obj/<obj>.o` (or
   `python tools/re/fncmp.py src/<obj>.c <name>`), then run `sh build.sh`: the SHA256 must
   stay `10dac648197fa5cdbb82d975ab9ff11f64075c9686908dfd9a33edc533f1971c`.
3. What worked on options and mode_client: don't trust a "block X must be N" that came
   from one of our own shapes; start from the plainest source and vary how the inlined
   helpers return (`notes/options.md`, "Attempt 30").
4. Update this file and the source comment with the outcome.
