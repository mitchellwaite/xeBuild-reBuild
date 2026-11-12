# Bug fixes

Status: plan only, nothing implemented but the two conventions items
(K1-K2). Line numbers are at 2dc0abd5.

Goal: fix the bugs found in a review of the app's C (src/*.c and src/*.h,
not the third-party src/crypto) on 2026-11-11. Each fix goes under
`XEBUILD_FIXES` (with the original in an `#else` where it replaces code)
and gets a line in README.md's list of fixes, so `make check` still
reproduces the reference SHA256 and `make win32fixes` builds the fixed exe.

Nearly all of these are in the original xeBuild 1.21.810, and the matching
build reproduces them on purpose. Three were already known before this
review: H1, the Winchester half of M9, and the Corona header under
"Already known". The review read every line once without a separate
confirmation pass, so a few items depend on console behaviour that
couldn't be tested here; they say so.

## Severity

| Level | Meaning |
|---|---|
| Critical | Normal use can write the wrong data to a console's flash, or ignores a request not to write it |
| High | Normal inputs corrupt memory or give a silently wrong image |
| Medium | Crashes, hangs or memory corruption on unusual, damaged or over-long input; wrong output in an edge case; a platform where a mode can't work |
| Low | Wrong or missing log text, leaks, minor undefined behaviour, edge cases with no lasting effect |

## Summary

| ID | Severity | Bug | Where |
|---|---|---|---|
| C1 | Critical | `client -bp` always patches block 0 | mode_client.c:590 |
| C2 | Critical | update's flags without arguments skip the next argument (`-clean -nowrite` flashes) | mode_update.c:773-793 |
| C3 | Critical | a failed flash write reports success, and update mode then reboots | net.c:688 |
| H1 | High | SMC config raw extraction writes 0x1000 bytes into a 0x400 buffer | build.c:1159 |
| H2 | High | options.ini keys match inside other keys (`cputemp` reads `overcputemp`) | filelist_ini.c:873, 916 |
| H3 | High | more than 32 bad blocks from the console overflow `xb.badBlocks` | mode_update.c:58-65 |
| H4 | High | `nandmu` never copies the MU data beyond 64MiB; the copy seeks past EOF | image_read.c:1379-1428 |
| M1 | Medium | a 0-byte input file leaves a freed pointer behind (double free) | build.c:472-482 |
| M2 | Medium | an empty network reply's static sentinel is passed to `free()` | mode_update.c:568 |
| M3 | Medium | `patchNand` length goes negative for a small unaligned patch | mode_client.c:539-561 |
| M4 | Medium | a dropped connection mid-transfer loops forever | net.c:242-282 |
| M5 | Medium | `log_printf` uses its formatted text as a format string | log.c:84, 91 |
| M6 | Medium | update and HDD modes build host paths with backslashes (Linux/macOS) | mode_update.c, console_hdd.c |
| M7 | Medium | `-s` with no file name swallows the next switch | mode_build.c:307-319 |
| M8 | Medium | `imgAddRaw` ignores the length and copies 0x1000 bytes | image_write.c:1538-1549 |
| M9 | Medium | console type names: Winchester is "Unknown", big-block Corona/Winchester lose "bb", `-p` paths use capitals | fileutil.c:27, consoleinfo.c:170 |
| M10 | Medium | `-r` / `rev` overflow `xb.blSuffix` and `parseIni`'s `label[50]` | filelist_ini.c:541 |
| M11 | Medium | a last `[security]` line without a crc copies with length -1 | filelist_ini.c:803-816 |
| M12 | Medium | bootloader names in the ini aren't length-checked | filelist_ini.c:575 |
| M13 | Medium | command-line and ini option segments overflow 512-byte buffers | options.c:951, 1184, 1241; main.c:498 |
| M14 | Medium | short DAE, CRL and FCRT data underflow their sizes | bootloaders.c, keys.c |
| M15 | Medium | offsets and sizes read from a dump are used unchecked | image_read.c |
| M16 | Medium | offsets and sizes from the console's replies are used unchecked | mode_update.c:336-356, consoleinfo.c:291 |
| M17 | Medium | `imgAdd` bounds writes by the raw size, not the buffer it writes | image_write.c:634 |
| M18 | Medium | more than 256 filesystem files overflow `fsFileEnts` | image_write.c:816-835 |
| M19 | Medium | `[rawpatch]` bound check can wrap | build.c:3665-3667 |
| M20 | Medium | `appendAddonPatches` can write past `PATCHES_MAX` | build.c:797-858 |
| M21 | Medium | `cfBestPairing` prefers a CF slot that failed to decrypt | bootloaders.c:123 |
| M22 | Medium | `client -keys` fails once the key files exist | mode_client.c:225-229 |
| M23 | Medium | `suGetFile`'s `strncat` overflows its 40-byte buffer | sysupdate.c:144-147 |
| M24 | Medium | network command and HDD path buffers overflow on long names | net.c, console_hdd.c:485 |
| M25 | Medium | `system.manifest` parsing has no bounds | console_hdd.c |
| M26 | Medium | STFS parsing has no bounds | stfs.c |
| M27 | Medium | `stfsGetFile`'s warning has a `%s` and no argument | stfs.c:239 |
| L1-L33 | Low | see "Low" below | |
| K1-K2 | Done | conventions (CLAUDE.md), resolved with this plan | main.c:24, image_write.c:999 |

Suggested order, one commit each, each with `make check` (reference SHA256)
and `make win32fixes` passing:

1. C1-C3: the ones that can damage a console.
2. H1, H3, M1, M2, M3, M4: memory corruption and hangs on normal or likely
   input.
3. H2, M5, M10-M13, L2-L8: ini and command-line parsing.
4. H4, M8, M14-M21: image building and dump robustness.
5. M6, M9: platform and console naming.
6. M22-M27, then Low.

## Critical

### C1. `client -bp` always patches block 0

src/mode_client.c:589-590, `clientBinPatch`:

```c
rem = off % bs;
start = rem / bs;
```

`rem` is less than `bs`, so `start` is always 0. `-bp <f> <o>` reads blocks
`0..count`, copies the file in at `rem`, and writes those blocks back.

`xeBuild client -bp patch.bin 0x200000` on a 16MiB console has `rem = 0`,
so it overwrites the flash header, SMC, keyvault and CB with patch.bin and
the console no longer boots. Offset 0x200000 is never touched.

Fix: `start = off / bs`. Fix M3 and L9's `soff` log in the same commit,
since `-bp` is the only caller of `patchNand`.

### C2. update's flags without arguments skip the next argument

src/mode_update.c, `mode_update`'s argument loop: `-nowrite` (773),
`-noava` (781), `-noreeb` (787) and `-clean` (793) take no argument (the
usage text agrees), but each does `i++` before the loop's own `i++`.

`xeBuild update -clean -nowrite`, `-noava -nowrite` or `-noreeb -nowrite`
never sees `-nowrite`: the console is flashed and rebooted, the opposite
of what was asked. `-nowrite -d dump` skips `-d`, and `dump` then stops
the run with the unknown-option error.

Fix: drop the four `i++` (`#ifndef XEBUILD_FIXES` around each).

### C3. A failed flash write reports success

src/net.c:660-689, `netSendFlash`: after sending the image it reads the
console's reply and logs "success!" or "failed!", but returns 1 either way.
It returns 0 only when sending fails.

In update mode (`flashConsole`, mode_update.c:609) `ret` stays 0 after a
rejected or failed write, so the console is rebooted (`netReboot`) and the
"due to previous possible errors, console reboot is not being done"
warning never shows. `client -w` (mode_client.c:183) reports success too.

Fix: return 0 unless the reply is "OK" (`rlen == 2` and `OK_REPLY`).

## High

### H1. SMC config raw extraction overflows its buffer (known)

src/build.c:1101-1189, `extractSmcConfig`: `e->data` is
`malloc(SMCCFG_SIZE)` (0x400), but the raw-layout branch copies 8 pages of
0x200 bytes (1159-1162), 0xC00 bytes past the end. A raw config's first
page has non-zero ECD bytes at +0x20c, so every raw file takes that
branch. `loadBlFiles` tries `config_raw.bin` explicitly (1789), so this is
normal use, not a corner case.

The plain branch (1151) skips the copy when fewer than 0x400 bytes follow
the match and goes on to show, patch and write the uninitialised buffer.

Fix: copy `SMCCFG_SIZE / NAND_PAGE` pages in the raw branch, and require
`size - i >= (SMCCFG_SIZE / NAND_PAGE) * NAND_RAW_PAGE` for it. In the
plain branch return an error when `size - i < SMCCFG_SIZE`.

### H2. options.ini keys match inside other keys

src/filelist_ini.c:916-948 (`findKey`, used by `getIniBool`, `getIniU32`
and their `Invalid` checks) and 873-896 (`findIniKey`, used by
`getIniValue`) look for the key anywhere in the buffer. `iniPreParse` has
already turned every character outside `validChars` (1094, which has no
`=`) into a space and removed the spaces, so `cputemp = 70` becomes
`cputemp70` and the value is whatever follows the key.

- `overcputemp = 85` before, or without, `cputemp`: `cputemp` reads 85.
  The same goes for `gputemp`/`overgputemp` and `edramtemp`/`overedramtemp`,
  so the SMC config gets the maximum as its target temperature.
- `xellbutton2 = ...` before `xellbutton`: `xellbutton` reads
  `2wiredx...`, which `parseButton` doesn't know, so xell falls back to
  the eject button.

Fix (fixes builds): keep `=` through the preparse (add it to `validChars`)
and match a key only at the start of a line (offset 0 or after a NUL),
followed by `=`, returning the offset after the `=`. The other ini users
use `,` and section names, and xeBuild's own options.ini writer
(consoleinfo.c `optWrite` and friends) already writes `name = value;`.

### H3. More than 32 bad blocks overflow `xb.badBlocks`

src/mode_update.c:43-77, `getBadBlocks`: every block in the console's list
is appended to `xb.badBlocks` and `xb.badRemap` (0x20 entries each) with
no bound on `xb.numBad`. `addRemap` (image_read.c:1138) stops at 32; this
path doesn't. A worn NAND, or a 256/512MiB big-block one whose list
includes MU-area blocks, can report more.

Past 32 the writes run through `xb.badRemap` into `xb.consoleBlmod` and
`xb.bl`, whose pointers are later freed or used. Line 56 also divides by
`info->blockSize` unchecked.

Fix: stop at 32 with the same "MAX REMAPS" error `addRemap` gives (and fail
the update), and reject a zero block size.

### H4. `nandmu` never copies the MU data beyond 64MiB

src/image_read.c:1379-1428, `copyMuData`, called from `writeImage`
(image_write.c:1182, 1187) when `nandmu` is set:

- It checks the static `dumpSize`, set at 1731 from `checkHeader`'s
  return. `checkHeader` (1581-1607) returns any dump larger than
  `NAND_RAW_64M` as 0x3000000 (MMC) or `NAND_RAW_64M`, so
  `dumpSize <= NAND_RAW_64M` always holds. `copyMuData` prints "no data to
  copy" and clears `xb.nandMu`, so `showConsoleInfo` then reports
  "64MiB (system only)".
- If that check passed, `fseek(fp, NAND_RAW_64M, SEEK_END)` (1404) would
  seek 0x4200000 bytes past the end of the file instead of to offset
  0x4200000. The `fread` result isn't checked (1419), so the uninitialised
  `malloc` buffer would be written, and hashed into the `-s` SHA-1, as MU
  data.

The restore of the MU blocks inside the 64MiB system area
(`finalizeImage`, image_write.c:1299-1313) is separate and unaffected.

Fix: keep the file's real size apart from the truncated load size, seek
with `SEEK_SET`, and copy in chunks with each `fread` checked. Test with a
256MiB big-block dump with MU data: the output must be the dump's size
and match the dump past 0x4200000.

## Medium

### M1. A 0-byte input file leaves a freed pointer behind

src/build.c:461-521, `loadFileCrc`: once the file opens it frees `e->data`
(474), then returns 1 for a 0-byte file (477-482), or -2 when `calloc`
fails, with `e->data` still pointing at the freed block.

The firmware loop (build.c:3365-3436) loads every `[flashfs]` file into
the same `xb.files[xb.nFlashFiles]`. A 0-byte file after another one frees
the previous file's data and leaves it dangling; the `loadCommonFile`
fallback, or the next file, frees it again (double free).

Fix: `e->data = NULL; e->size = 0;` right after the `free`.

### M2. An empty network reply's static sentinel is freed

src/net.c:307-308: for a zero-length reply `netRecv` returns `&netEmpty`, a
static, which only `netFree` knows to skip. Two places pass it to `free`:

- `updateGetFile` (mode_update.c:565-569) calls `free(buf)` when `len` is 0.
- `getSecurityFiles` (mode_update.c:444) keeps the sentinel in
  `xb.flashBuf[i]` for an empty reply. `buildFlash`'s security loop
  (build.c:3468-3475) then uses it as the file's data, and
  `secdataPrepare` (keys.c:897), `extendedPrepare` (keys.c:857) or the
  loop's own cleanup (3557-3561) frees it.

Either needs the console to send a 0-byte file (to confirm what updsvr
sends for empty files). Fix: `netFree` in `updateGetFile`, and in the
`get*` functions turn an empty reply into NULL with size 0.

### M3. `patchNand` length goes negative for a small unaligned patch

src/mode_client.c:529-562: with an unaligned start it copies
`NAND_PAGE - off` bytes and subtracts that from `len`, even when `len` is
smaller. `client -bp 4byte.bin 0x100` over-reads 0x100 bytes from a 4-byte
buffer, `len` becomes -252, and `memcpy(buf, data, len)` (559) gets a huge
`size_t`.

Fix: copy `min(len, NAND_PAGE - off)` in the first step and stop once
`len` reaches 0.

### M4. A dropped connection loops forever

src/net.c:203-309, `netRecvVerbose`: in the data loop only `SOCKET_ERROR`
ends it. `recv` returning 0 (the console closed the connection) adds
nothing to `got`, and `select` keeps reporting the socket readable, so the
loop spins at full CPU. The 4-byte length header (223) is also read with
one `recv`, which can return fewer bytes.

Fix: treat 0 as a closed connection (free, log, return NULL), and read the
header in a loop until all 4 bytes arrive.

### M5. `log_printf` uses its formatted text as a format string

src/log.c:75-95: `vsnprintf` formats into `buf`, then `printf(buf)` (84) and
`fprintf(f, buf)` (91) format it again. A `%` in any logged path, file
name, ini value or console reply is parsed as a conversion and reads
missing arguments (a crash, or a write with `%n`). `iniPrintf`
(mode_ini.c:59, 63) does the same with SU file names.

The two "Cpu Fan"/"Gpu Fan" lines in `showSmcConfig` (build.c:873, 882)
spell `%%%%` to get one `%` through both passes. Fix: `fputs(buf, stdout)`
and `fputs(buf, f)`, and `%%` in those two strings (both under
`XEBUILD_FIXES`).

### M6. Update and HDD modes build host paths with backslashes

src/mode_update.c builds local paths with `\`: `ini = ".\\data\\"` (690),
`dumpBuf = ".\\"` (691), `-d` adds `"\\"` (810), `-f` makes `"%s\\"` and
`"%s\\bin\\"` (822-825), and the addon index is `".\\%d\\bin\\addon.idx"`
(205). console_hdd.c's `sendDir` joins local paths with `"\\"` (495).
Windows accepts either separator; Linux and macOS, the platforms that build
with `XEBUILD_FIXES`, take `\` as part of the name.

On Linux, `xeBuild update -f 17559` opens a file named `17559\_glitch2.ini`
in the current directory, so update mode can't work. `client -c dir`
stats `dir\name` for every entry, sends nothing, and prints "sent files to
partition OK!".

Fix: `/` in the local paths (fine on Windows too). Console-side paths
(`usv:\`, `SSEP:\`, `XCOM:`, `\Device\...`) must keep their backslashes.

### M7. `-s` with no file name swallows the next switch

src/mode_build.c:307-319: `if (argv[++i] && ...)` advances `i` even when
the next argument isn't a file name, so that switch is skipped.
`xeBuild -s -t jtag -c falcon out.bin` drops `-t`, takes `jtag` as the
output name, and builds a retail image.

Fix: test `argv[i + 1]` and increment only when it's taken.

### M8. `imgAddRaw` ignores the length

src/image_write.c:1538-1549: `imgAddRaw` logs `len` but passes
`RAWFILE_SIZE` (0x1000) to `imgAdd`, so a shorter Statistics.settings or
Manufacturing.data is over-read into the image and a longer one is cut
without a warning. Files loaded from disk sit in `loadFileCrc`'s zeroed
+0x10000 slack, so the over-read is zeros there. In update mode the data
comes from `netGetFile`, sized to the reply, and `getMobileFiles` sets the
sizes to 1024 and 128 whatever the console sent (mode_update.c:259-266), so
~3-4KiB of heap goes into the flashed image.

Fix: copy `min(len, RAWFILE_SIZE)` into a `RAWFILE_SIZE` buffer (padded the
way an empty slot is), and in `getMobileFiles` use the smaller of the
received size and 1024/128.

### M9. Console type names

- src/fileutil.c:25-32, `getConsoleTypeStr`: `type <= CONSOLE_CORONA`, so
  Winchester (7) is "Unknown" (known).
- src/consoleinfo.c:165-224, `showImageType`, builds update and client
  mode's console type from that string and passes it to `setConsoleType`.
  A Winchester gives "Unknown", so `parseConsoleInfo` fails and update
  mode can't run. Only Corona gets "4g" for an MMC NAND (Winchester 4g
  needs it too), and only Jasper and Trinity get "bb"/"bigffs", so a
  big-block Corona or Winchester would be built with the small-block
  layout. To confirm: which `nandSize`/`blockSize` such a console reports,
  and that these consoles exist (xeBuild accepts `coronabb` and
  `winchesterbb`).
- src/mode_client.c:413-421, `clientPatches`, makes
  `patches_<Name>.bin` from the capitalised names: `patches_Unknown.bin` on
  a Winchester, and on case-sensitive filesystems `patches_Trinity.bin`
  rather than the shipped lower-case names.

Fix: `type <= CONSOLE_WINCHESTER`; in `showImageType` add Winchester's
"4g" and big-block suffixes for Corona/Winchester (from the console's
reported size); build the `-p` paths from filelist_ini.c's lower-case
`consoleNames[]`.

### M10. `-r` and `rev` overflow `xb.blSuffix` and `label`

`sprintf(xb.blSuffix, "_%s", ...)` writes an unbounded string into the
0x40-byte `xb.blSuffix`: `-r` in build mode (mode_build.c:349) and update
mode (mode_update.c:757), and the ini's `rev` (options.c:1111). A value
over 62 characters overwrites `xb.numPatches`, `xb.nFiles` and what
follows. `parseIni` then formats `"[%sbl%s]"` into `label[50]`
(filelist_ini.c:433, 539-546), which overflows on the stack from a value
of 35 characters with "winchester" (40 with "xenon").

Fix: reject a suffix that doesn't fit, and size `label` for the longest
console name plus a full suffix (or `snprintf` and fail on truncation).

### M11. A last `[security]` line without a crc copies with length -1

src/filelist_ini.c:799-816: `memFindChar` searches the rest of the file for
`,`. When no comma is left, `comma` is -1, `comma > nul` is false, so
`len = comma = -1` passes `len <= FS_NAME_SIZE - 1` and
`strncpy(xb.flashFiles[i], p, (size_t)-1)` pads far past the array. The
bootloader section has a `len < 0` check (569); this one doesn't.

Fix: treat `comma < 0` as "no crc" (`comma < 0 || comma > nul`).

### M12. Bootloader names in the ini aren't length-checked

src/filelist_ini.c:575: the bootloader section copies `len` bytes into
`xb.files[blOrder[i]].name` (0x400) with no check. `[rawpatch]` (651) and
`[flashfs]` (720) reject names over 1023 characters. Fix: the same check
here.

### M13. Option segments overflow 512-byte buffers

`parseCmdOptions` (options.c:929-955), `parseRawPatches` (1162-1188) and
`loadAddons` (1218-1246) copy each `;`/`:`-separated segment into a
512-byte stack buffer with no bound on `j`, so one `-o` or `-8` segment, or
an ini `addon` list, longer than 511 characters overflows the stack.
`setBasePath` (main.c:498) copies `argv[0]` into `path[260]`.

Fix: fail with the existing "invalid arguments" error when a segment
doesn't fit; size `setBasePath`'s buffer from the string, or skip the
`chdir` when it doesn't fit.

### M14. Short DAE, CRL and FCRT data underflow their sizes

- `verifyDae` (bootloaders.c:279-310) and `daeEncrypt` (keys.c:1001-1074)
  take each DAEP segment's 16-bit length from the data and pass
  `len - 304` and `len - 336` to AES and SHA-1 with no minimum, and never
  check the segment fits in the buffer. A length of 0 or under 336, from a
  damaged dump's dae.bin or a bad file, wraps to ~4GiB and crashes.
- `verifyCrl` (bootloaders.c:201-228), `crlEncrypt` (keys.c:926-978) and
  `shaCheck` use `size - 336` for any size.
- `verifyFcrt` (bootloaders.c:338-373) and `fcrtEncrypt`
  (keys.c:1076-1114) read the IV at +256 before checking the size, and
  `fcrtVerifySig` reads +256..+320 and the signature before that.

Fix: reject a segment shorter than 336 bytes or running past the buffer,
a CRL under 336 bytes, and an FCRT of the wrong size, before touching the
data.

### M15. Offsets and sizes read from a dump are used unchecked

`checkHeader` checks header fields against the raw file size, but
`xb.dump` holds only the 0x200 data bytes of each 0x210-byte page, and
several readers trust their own fields:

- `getImageKv` (image_read.c:295) and `getImageSmc` (257) bound against
  `NAND_RAW_PAGE * xb.dumpPages` instead of `xb.dumpSize`, and
  `getImageSmc` checks only the start address, not `addr + size`.
- `getImageLdv` (119) has `cfBestPairing` read `2 * patchSlotSize` bytes
  at `sysUpdateAddr` (bootloaders.c:108-115), and `cbGetPairing` reads a
  CB at `kvAddr + kvSize` sized by its own header.
- `getNetKd` (430-443) copies a size read from the dump.
- `loadFlashFile` (459) and `fsGetFile` (529) follow FS chains with
  `& 0x1fff` into `fs->map[0x1000]`, and never check the block offsets
  against the dump.
- `findFsRoot` (902-907) copies 16KiB from a mobile offset that, on MMC,
  comes from the anchor block (up to 0xffff << 14).
- `findSmcConfig` (961-971) reads 0x400 bytes at a page that can be the
  dump's last.
- `getNonces` checks each offset against `xb.dumpSize` but then reads
  header fields past it.

Fix: check every offset plus its read length against `xb.dumpSize`, and
chain indices against the map size, and treat a failure like the existing
"not sane" paths.

### M16. Offsets and sizes from the console's replies are used unchecked

- `bldrGetKv` and `bldrGetSmc` (mode_update.c:336-356) read the KV and SMC
  at offsets and sizes taken from the console's bootloader dump's header,
  and don't check the `calloc`.
- `getFlashHdrOpts` (consoleinfo.c:291-313) reads `hdr[0x4b..0x4f]` from a
  reply of any non-zero length.
- `getFreebootOpts` (consoleinfo.c:230-251) reads `FREEBOOT08_OPTS + 15`
  without checking the core's size.

Fix: check against `xb.bl.size` and the reply lengths.

### M17. `imgAdd` bounds writes by the raw size

src/image_write.c:634: `imgAdd` checks `off + len` against `xb.rawSize`,
but copies into `xb.hdr`, which is only `xb.userSize` bytes (0x80000 to
0x200000 smaller). A bootloader or file that ends in that gap overflows
the heap. `off + len` can also wrap. Fix: check against `xb.userSize`
without the wrap.

### M18. More than 256 filesystem files overflow `fsFileEnts`

src/image_write.c:816-835: `imgAddFile` writes `fsFileEnts[nFsFiles]`
(0x100 entries, one FS table block) with no bound on `nFsFiles`. An ini
with 256 `[flashfs]` files plus the security files and `sysupdate.xexp*`
runs into `fsChain`. Fix: stop at 256 with the "will exceed available
flash space" error.

### M19. The `[rawpatch]` bound check can wrap

src/build.c:3665-3667: `end = off + f.size` is 32-bit, so
`-8 f.bin,0xffffff00` wraps under `xb.userSize` and `memcpy` writes far
outside `xb.hdr`. Fix: `off <= xb.userSize && f.size <= xb.userSize - off`.

### M20. `appendAddonPatches` can write past `PATCHES_MAX`

src/build.c:797-858:

- `size = e->size - 4` (799) underflows for a patches file under 4 bytes.
- The base patches are copied into the `PATCHES_MAX` (0x4000) buffer
  unbounded (806).
- An addon is accepted when `size + a->size <= PATCHES_MAX` (820), and then
  the end marker and count go 8 bytes after that (844-845), so a total of
  exactly 0x4000 writes 8 bytes past the buffer.

Fix: require `4 <= e->size <= PATCHES_MAX - 4`, and keep 8 bytes free in
the addon check.

### M21. `cfBestPairing` prefers a CF slot that failed to decrypt

src/bootloaders.c:97-128: `if (ldv1 >= ldv0) p0 = p1;` also picks slot 1
when it failed (`p1 = 0`, `ldv1 = 0`) and slot 0 decrypted with LDV 0. The
result is 0, so `getImageLdv` falls back to the CB's pairing or to the
guessed LDV 1. Fix: `if (p1 && ldv1 >= ldv0)`. Related:
plans/cb-ldv-1888.md (the CB's LDV is never set).

### M22. `client -keys` fails once the key files exist

src/mode_client.c:219-246, `dumpKey`: when the file already exists it calls
`FileToBuffer(file, &len)`, which overwrites `len` (the key's size) with the
file's and leaks the buffer. `sumBytes(key, len)` then sums the wrong
length: for 1blkey.txt (32 hex digits and a newline) 33 bytes of a 16-byte
key. So a second `-keys` reports every key as "not valid or file is
inaccessible", and for the RSA keys a larger existing file reads past the
key.

Fix: drop the reload, or compare the existing file's contents with a
separate length variable; free what it loads.

### M23. `suGetFile`'s `strncat` overflows its buffer

src/sysupdate.c:144-147: `char buf[40] = "$flash_"; strncat(buf, name, 40);`
can write 7 + 40 + 1 bytes. Names come from the ini and the SU, and
bootloader names have no length limit (M12), so one over 32 characters
overwrites the stack. Fix: `sizeof buf - strlen(buf) - 1`, or fail when
it doesn't fit.

### M24. Network command and HDD path buffers overflow on long names

- `netMount`, `netUnmount` and `netGetFile` `sprintf` into `cmd[260]`
  (net.c:577, 592, 607); `netSendFile` and `netMkdir` `strcpy` into
  `cmd[264]` (net.c:795, 888).
- `sendDir` builds `dstPath[260]` with `strcpy`/`strcat`
  (console_hdd.c:491-493), and `srcPath[1024]` too.

Long content paths from a manifest (M25) or a local directory tree
overflow the stack. Fix: `snprintf` and fail on truncation.

### M25. `system.manifest` parsing has no bounds

src/console_hdd.c:

- `readManifestString` (157-173) copies a 16-bit length into the caller's
  `name[512]`.
- `addTitleId` (109-122) appends to `titleIds[48]` with no bound.
- `parseManifestEntries` (244-303) walks `count` entries and their name,
  path and id offsets without checking them against `len`.
- `checkManifestHeader` (124-155) hashes `hdr.len` bytes unchecked.

The manifest's SHA-1 is its own and not a signature, so a damaged or
crafted file in the avatar folder corrupts memory during `client -e` or
update mode. Fix: bound each string and offset by the manifest's length and
the destination, and cap the title ids.

### M26. STFS parsing has no bounds

src/stfs.c:

- `stfsGetFile` (213-256) allocates from the entry's `size` but copies its
  `ab` blocks, and indexes `c->blocks` by `fb + j` without checking either.
- `stfsCheckHashes` (46-128) walks the hash tables and data blocks without
  checking them against `c->size` until after a full table.
- `stfsListFiles` and `stfsGetFile` scan the file table until an all-zero
  entry, with no end.

Fix: bound reads by `c->size`, blocks by the count found, and the copy by
the allocation.

### M27. `stfsGetFile`'s warning has a `%s` and no argument

src/stfs.c:239: the "file %s is not contiguous" warning passes no `name`, so
`vsnprintf` reads a garbage pointer as a string and usually crashes. Fix:
pass `name`.

## Low

Logic and messages:

- **L1.** Every mode compares an argument with "help" on 2 characters
  (`strnicmp(argv[i], "help", 2)`: mode_build.c:183, mode_update.c:702,
  mode_client.c:831, mode_extract.c:62), so any argument starting with
  "he", like an output name `heavy.bin`, shows the usage and exits.
  Compare the whole word.
- **L2.** `applyIniOptions` tests `xb.xellButton` where it means
  `xb.xellAltButton` (options.c:1073), so "alternate xell button is
  disabled" never prints.
- **L3.** `cfldv` is stored in the `uint8_t` `xb.cfLdv` before the
  `> CF_LDV_MAX` check (options.c:868, 974), so `cfldv=257` silently gives
  1 and `cfldv=256` is rejected as invalid. Check the full value first.
- **L4.** `nosusecurity` logs "Using NOSECURITY option" (options.c:614).
- **L5.** `olddvd` from the ini is looked up with a set mask of 0
  (options.c:1087), so `-o olddvd=false` can't suppress it, and
  `olddvd=false` sets `optFlagsOff` for NODVD and XELL_BUTTON (492), which
  also suppresses the ini's `nodvd`.
- **L6.** The command-line macid errors print `opt` ("macid") where they
  mean the value (options.c:896, 899).
- **L7.** "dualboot setting ignored!" is logged when both `xellbutton` and
  `dualboot` are 0, as with nodvd/olddvd and no dualboot (options.c:1091).
- **L8.** `parseOption`'s and `parseRawPatch`'s specific errors are at log
  level 1 (options.c:694, 896, 899, 918, 921, 924, 1130), so without `-v`
  the user sees only the generic "invalid arguments" line.
- **L9.** Format arguments: the "Unable to allocate 0x%x bytes for %c%c"
  logs pass no size (bootloaders.c:431, 496, 555); `getNetKd` prints the 6
  MAC bytes with 5 `%02x` (image_read.c:436); `patchPayloadSize` uses an
  invalid `%r4` (build.c:2765, 2768); `clientBinPatch` prints the `soff`
  pointer instead of `off` (mode_client.c:583); `dump_buffer_hex` and
  `clientManifest` pass pointers and `size_t` to `%x` (fileutil.c:106,
  mode_client.c:213, 215), which is wrong on the 64-bit builds.
- **L10.** `showExpectedFuses` shifts `0xF` by `(16 - cseq) * 4`
  (fileutil.c:729): by 64 when `cseq` is 0 and `allow` isn't, and negative
  for `cseq > 16`; both are undefined.
- **L11.** `myatou32` validates decimals with the hex check, so `7f` is
  accepted and `atoi` gives 7 (fileutil.c:380-383); `myatox32` takes up to
  16 digits into 32 bits and keeps the low ones (327); `myatol` misses `Z`
  (354).
- **L12.** Kernel versions print the QFE as `k & 0xf` (main.c:239,
  consoleinfo.c:461, console_hdd.c:316); it's 8 bits, as stfs.c:187 prints
  it.
- **L13.** `optOpen` tests `path[strlen(dir)]`, always the NUL, so it always
  adds `/` (consoleinfo.c:34). `optClose` doesn't reset `opts`, so a write
  or close after it uses a closed `FILE`.
- **L14.** `mode_ini` stops only when 1blkey.txt exists and is invalid
  (mode_ini.c:177); a missing file carries on, and the CF fails to decrypt
  later with a less helpful error, though the message says "not found or
  invalid".
- **L15.** `suExtractBl` passes the header's size to `cfDecrypt`
  (sysupdate.c:73), which wants it rounded up to 16 (`cfLen`), so a CF
  whose size isn't a multiple of 16 always fails to decrypt.
- **L16.** `checkPatches` searches from `p + 4` with a length 4 bytes too
  long (mode_client.c:280).
- **L17.** An empty `[flashfs]` name writes `xb.firmware[i][-1]`
  (filelist_ini.c:741), and the firmware loop reads `f.name[-1]`
  (build.c:3370).
- **L18.** A bootloader, `[rawpatch]` or `[security]` section with no `[`
  after it gets `end = off - 1` (filelist_ini.c:551, 637, 797): the
  bootloader section fails with "can't find enough data", and the others
  stop after their first entry.
- **L19.** `parseIni` and `loadUserIni` read `buf[1]` of a 0-byte file, and
  a 1-byte options.ini counts as multi-byte (filelist_ini.c:452, 1073).
- **L20.** `sendDir` ignores its recursive calls' result
  (console_hdd.c:515), so a failure in a subdirectory still reports
  success.
- **L21.** `sendAvatarData` returns 1 when `prepSysex` fails
  (console_hdd.c:421, 430).
- **L22.** `buildFlash` writes the power-on buttons into the header
  (`patchHeaderOpts`, build.c:2039-2077) before `patchFreeboot` replaces an
  unknown xell button with eject and clears a duplicate alt or dualboot
  button (2708-2727), so the header keeps the unsanitised values.
- **L23.** In client mode, `-keys`, `-i` and `-p` don't reject a second
  command (mode_client.c:885-889, 939-966) the way the others do
  (`ERR_TWICE`).
- **L24.** `getFreebootOpts` runs before `parseIni` has set up `xb.files`,
  so `findFile(FILE_FREEBOOT)` returns 0 and it uses `xb.files[0]`,
  leaving a freed pointer there (consoleinfo.c:232, 277).
- **L25.** `verifyBlSigs`' SE path uses `xb.files[findFile(FILE_SB)]`
  without checking that an SB was found (build.c:1474-1475).
- **L26.** `patchBlsBlmod` writes the patch set's first section into the
  CB_B entry even when the build has no CB_B (build.c:2255-2265), a NULL
  write if that section isn't empty.
- **L27.** The patch-set walkers (`patchBlsResign`, `patchBlsBlmod`,
  `fixupPatchSet`: build.c:2145, 2245, 2333) trust each section's address
  and length; a bad patches file writes outside the bootloader buffers.
- **L28.** `smcCheck` reads `smc[0x100..0x102]` whatever `len` is
  (smc.c:263).
- **L29.** `findFsRoot` prints "done! fsroot found ok!" with `puts`
  (image_read.c:885), outside the log file and the verbosity setting.
- **L30.** `getImageMobiles` logs `name` before it is set when `malloc`
  fails (image_read.c:372).
- **L31.** `kvGetConsoleId` returns the console serial and `kvGetSerial`
  formats the console id (keyvault.c:134-166); `showConsoleInfo` labels
  them correctly, but the names are swapped.

Leaks and efficiency:

- **L32.** Leaks: `iniPreParse`'s `tmp` (filelist_ini.c:129); the `FILE` in
  `readFileTo` when the file is short (fileutil.c:566); `smcPrepare`'s
  `buf` on its error returns (keys.c:457, 472, 527); every file
  `suExtractBl` and `iniWriteFlashfs` extract (sysupdate.c:59,
  mode_ini.c:85); each addon in `appendAddonPatches` (build.c:812); a
  wrong-size fuses file in `loadBl24` (1568); the socket when `connect`
  fails and a short info reply (net.c:389, 409); `s.blocks` in
  `loadStfsChecked` (console_hdd.c:229). `netClose` doesn't reset
  `netInfo` or `netSock`, so a second call double-frees.
- **L33.** `iniPreParse` copies the whole buffer into `tmp` once for every
  space and empty line it removes (filelist_ini.c:145, 186-188, 206-208):
  O(n²) in the ini's size. Compact in place with read and write indices.

Conventions (CLAUDE.md), both resolved in the commit that added this plan:

- **K1.** The fixes banner ("xeBuild reBuild (target)", main.c:24-33) has
  no line in README's list of fixes. Resolved by a rule, not a README
  line: CLAUDE.md now says the version banner doesn't count as a fix.
- **K2.** "one tab per indent level": `checkBootImage` had duplicated
  `build = SWAP16_IMAGE_WRITE(b->build);` lines one level short
  (image_write.c:999, 1013), and mode_update.c:73 was one level too deep.
  Fixed: the duplicates are gone and the `return` is re-indented (same
  bytes).

## Already known

- `buildImage` writes Corona's `smcBootAddr`/`smcBootSize` unswapped
  (image_write.c:220-221). Harmless, since `smcSetLoad` overwrites both
  when the SMC is loaded, but wrong if that ever changes.
- plans/cb-ldv-1888.md: `xb.cbLdv` is never set, so every CB's LDV is 0.

## Testing

- `make check` after each commit: the reference SHA256, since every change
  is under `XEBUILD_FIXES`.
- `make win32fixes`, and a Linux build, for each commit.
- Per fix, the input from its failure case, with the fixes build showing
  the new behaviour and the reference build the old: C2's argument orders,
  H2's options.ini orders, H1 with a config_raw.bin, M1 with a 0-byte
  firmware file, M10-M13 with over-long arguments, M14-M15 with truncated
  or edited dumps.
- C1, C3, H3, M2-M4 and M16 need a console running updsvr (or a stub
  server answering the same protocol), which the repo doesn't have.
