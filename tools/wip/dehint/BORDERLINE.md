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

1. **Tagged shapes** (39, 7 of them approved): each has a `Borderline, for review:` comment
   in the source saying what it does and what it replaced.
2. **Redundant file-local definitions**: all removed (2026-11-10), same bytes. The second
   section says what went and what is left (two prototypes that are needed).

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

### keys (3, all approved 2026-11-10) — `src/keys.c`, notes in `notes/keys.md` ("Review")

| Line | Where | Shape | Why it stays |
|---|---|---|---|
| 648 | `kvPrepare` | two `alt` tests at the end where one if/else would hold `kvSet` and both encrypt calls | Only `if (!alt) kvSet` has a call on just one arm, so the call heuristic gives alt 71%; every single if/else has calls on both arms (50%). 8 one-test forms tried (128-398) |
| 840 | `daeEncrypt` | a bad header ends the loop with `off = size; len = 0;`, and the warning sits in the loop's exit arm, not after the loop | The binary's failed-decrypt arm computes `size + 1 + len` at the latch, so the author ends this loop through `off`. With the warning in the exit arm a `break` would skip it, which the binary prints after a bad header; `len = size - off` is 551 |
| 902 | `fcrtEncrypt` | the encrypt calls written out in both arms, where an `\|\|` would need one copy | The call heuristic counts only on arms the test dominates, so a shared encrypt block drops the warning edge to 875, under the 1000 its own epilogue copy needs (`\|\|` 25 lines). Helpers 50-100 |

### console_hdd (2, both approved 2026-11-10) — `src/console_hdd.c`, notes in `notes/console_hdd_sendAvatarData.md` ("Review")

| Line | Where | Shape | Why it stays |
|---|---|---|---|
| 323 | `prepSysex` | `r` kept as a flag with a second `if (r)`, where the mount arm could return `createSysexDirs()` itself | No spelling without a flag matches (8 tried), and the reason is known: the mount test mustn't guard the call. Same form as `myatou32`'s approved `hex` |
| 350 | `sendAvatarData` | returns `long` next to `netSendFile`'s `int`; a failed send ends the loop with `i = consoleManifest.count`, not `break` | `sendCompatData` needs `long` for its return and its `ret`, so `long` is the author's type for these results. `break` makes a pointer IV (39 lines) |

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
| `src/fileutil.c` | 307 | `myatou32` | `bool hex` (was `BOOL`) set by one `if` and tested by the next | approved 2026-11-02 |

## 2. Redundant file-local definitions: removed (2026-11-10)

The user counted these as borderline too. All of them went, with the same bytes; the scan
(`python tools/wip/dehint/localdefs.py`) now flags none. What was removed:

- **Forward prototypes of functions defined before their first use** (36): 21 in
  `image_read.c`, 5 in `mode_client.c`, 4 in `filelist_ini.c`, 2 each in `build.c` and
  `bootloaders.c`, 1 each in `keys.c` and `mode_update.c`.
- **Two of them were not redundant**: `cfPatchSlots` (`keys.c`) and `imgGetSecurityFiles`
  (`image_read.c`) are C99 `inline` definitions, and the plain prototype is what made gcc
  emit their out-of-line copies (without it both copies vanish). Their definitions now say
  `extern inline`, which is the same thing in one place. The scan can't see this.
- `image_write.c`'s unused `ALIGN_BLOCK` and `setSpareLba` macros.
- `fileutil.c`'s `typedef int BOOL` / `TRUE` / `FALSE`: the uses are `<stdbool.h>` `bool`/`true`/`false` now (`validateString` keeps its `uint32_t` return: a `bool` one changes five callers' objects).
- `image_read.c`'s `fseeko64` prototype (`<stdio.h>` declares it).
- `net.c`'s `extern time_t netTimeStart`: now in `xebuild.h`'s Globals block, which
  includes `<time.h>` for it.
- `filelist_ini.c`'s `extern`s for `consoleNames` and `validChars`: moved to
  `filelist_ini.h`. They're still needed, since both are defined at the end of the file for
  the .rdata order and used before there.

### Needed where they are, but could move to a header

The first use comes before the definition, so these prototypes are needed unless a header
declares the function: `loadFileCrc` (`src/build.c`) and `pageErased`
(`src/image_write.c`).

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
