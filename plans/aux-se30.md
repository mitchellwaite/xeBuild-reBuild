# A/UX on the Macintosh SE/30

Status: plan only, nothing implemented. It builds on plans/big-endian.md,
which has to land first.

Goal: a native xeBuild for Apple's A/UX 3.x on a Macintosh SE/30 (68030 at
16 MHz, 68882 FPU, 128 MB RAM) that writes the same files as the x86-64
fixes build, in every mode: build from a dump, update, client (over
Ethernet), extract and ini. It is a fixes platform like `linux`, so it
compiles with `XEBUILD_FIXES`. `make check` keeps the reference SHA256
throughout.

## Summary

It's feasible, and most of the code work is already planned. The 68030 is
a big-endian ILP32 CPU, the same case as the G3/G4 targets in
plans/big-endian.md. What A/UX adds on top of that plan:

| # | What | Why | Size |
|---|---|---|---|
| 1 | m68k deltas to the big-endian plan | gcc 2.x predefines no byte-order macro; Gladman's AES header includes `<endian.h>` | small |
| 2 | C99 features gcc 2.7.2 lacks | `_Bool`/`bool`, a flexible array member, one mixed declaration | 6 sites |
| 3 | A/UX compat layer (headers and a few functions) | no `stdint.h`, `vsnprintf`, `strcasecmp`, `inet_pton`, `fseeko`, `%ll` | new, A/UX only |
| 4 | A shell build script and `make aux-dist` | no GNU make 3.81 on A/UX; gcc 2.7.2 has no `-MP -MF -MT` | new |
| 5 | Lower peak memory (`XEBUILD_FIXES`) | a 64MB big block build peaks at about 200MB; nandmu mallocs up to 462MB at once | medium |
| 6 | Table-driven page ECD (`XEBUILD_FIXES`) | the bit-serial ECD is most of the run time at 16 MHz | small |

The machine needs some changes to the assumed setup:

- **ROM.** A/UX doesn't need a 32-bit clean ROM. It manages memory itself,
  and owners report it hanging with IIsi, IIfx and ROMinator ROMs in an
  SE/30. The stock ROM with 128MB is the known-good setup.
- **A/UX version.** Use A/UX 3.0.1, the release Apple supported on the
  SE/30, rather than 3.1.1.
- **Filesystem.** Everything goes on UFS, because the data files'
  names are longer than SVFS's 14 characters.

With today's bit-serial ECD, expect 5-15 minutes for a 16MB image and up
to an hour for a 64MB big block one. The table-driven ECD (6) cuts most of
that (see Speed).

## The machine and A/UX

### A/UX version

- Apple's A/UX 3.0 Installation Guide lists the SE/30, with at least 8MB of
  RAM and an 80MB disk.
- 3.1 and 3.1.1 were fully tested only on the Workgroup Server 95. The
  comp.unix.aux FAQ says "A/UX 3.1.1 will _NOT_ run reliably on the MacII,
  MacIIx, MacIIcx or SE/30". Some owners run it on SE/30s anyway.
- Target 3.0.1 (3.0.2 if you have it). The QEMU setup below also boots
  3.0.1, so the development and target systems match.

### ROM

The plan assumed a 32-bit clean ROM. Under A/UX that doesn't help, and it
may stop A/UX booting:

- A/UX's kernel manages all physical memory. kconfig's `MAXPMEM = 0`, the
  default, means "use all available physical memory". The 32-bit clean ROM
  matters only to Mac OS. The Mac environment inside A/UX uses A/UX's own
  ROM patches.
- Owners report A/UX hanging at a grey screen on an SE/30 with a IIfx or
  IIsi ROM (applefritter, 68kmla). One saw "Standalone program space is too
  small" with a MacSIMM IIsi ROM. Another saw A/UX 3.0.1 freeze with the
  ROMinator II's stock image (2023, unresolved). In each of these reports,
  the fix was the stock ROM.
- With the stock SE/30 ROM and 128MB, "A/UX boots fine" (applefritter). One
  user did run 3.1.1 on a 128MB SE/30 with a custom-patched ROMinator
  image, but only with its Turbo040 disabled.

Decision for the owner: keep the stock ROM for A/UX (dual-booting Mac OS 7
then needs MODE32 for more than 8MB there), or try the ROMinator first and
fall back if it hangs. Phase 0 settles this before any code work.

### RAM and process memory

- 128MB works on an SE/30 under A/UX, per two owner reports. A 2026 test on
  a Quadra 950 found 128MB and 256MB "too much" for A/UX; the error wasn't
  described. If the SE/30 misbehaves, 64MB is the fallback.
- What xeBuild can use:
  - The A/UX kernel takes its share.
  - The buffer cache takes 10% by default (`NBUF = 0`).
  - The Mac environment gets 16MB by default from 3.0.1 on.
  - Log in over telnet, or from a terminal session that doesn't start the
    Finder, and xeBuild gets nearly everything else.
- Pages are 4KB. kconfig's `MAXUMEM` limits a process's virtual address
  space to at most 0x20000 pages (512MB).
  - Its default is unverified. Measure it in Phase 0 with a malloc probe.
  - A 1991 report says changing `MAXUMEM` left a system unbootable, so keep
    a known-good kernel.
  - csh has no `limit` command, and `ulimit` sets only the file size.
- Swap: the installer presets 18MB; the manual advises 2-3 times RAM. Use a
  swap partition of at least 256MB (`swap -a` adds one later).

### Disk and filesystem

- UFS (Berkeley FFS, 255-character names) is the default root filesystem
  from A/UX 3.0. SVFS (System V, 14-character names) is still offered.
- xeBuild needs UFS. These names are longer than 14 characters:
  - `patches_g2m_<console>.bin` and `patches_g2_<console>.bin`
  - `Statistics.settings` and `Manufacturing.data`
  - `keyvault_alt.bin`
  - `xell-gggggg.bin`
  - the output names, such as `<console>_retail_<ver>.bin`

  On SVFS they would be truncated and could collide.
- Files are limited to 2GB (32-bit `off_t`). xeBuild's largest file is a
  528MB Jasper 512 dump, so that's fine. On 3.0.1, also keep each filesystem
  under 2GB: the 3.1 ReadMe says boot-time fsck can't check a larger root,
  and 3.1 is the release that added filesystems up to 4GB.
- A nandmu build on a Jasper 512 needs about 1.1GB free (the dump and the
  output), plus the swap partition.
- The SE/30's SCSI has no DMA. Mac OS benchmarks show about 1.2MB/s on the
  internal bus. NetBSD on an SE/30 with 128MB measured 0.7MB/s writes and
  1.5MB/s reads. There are no A/UX figures; assume 0.5-1.2MB/s.

### Network (client and update modes)

- A/UX's TCP/IP needs an Ethernet card it has a driver for:
  - The Asanté MacCon SE/30 is used under 3.0.1 and 3.1.1.
  - A Farallon PDS card was detected by 3.1.1.
  - The current SEthernet/30 has an A/UX driver
    (github.com/rhalkyard/SEthernet-AUX).
  - LocalTalk can't carry IP.
- It runs at 10Mbit, with no DHCP: set a static address with `newconfig`.
  The console's port autonegotiates, so a switch between them is enough.
- Beacon:
  - xeBuild only receives the console's UDP beacon (net.c:95-160), and
    udp(5P) says A/UX delivers broadcasts.
  - socket(2N) documents no `SO_BROADCAST`. net.c:115 sets it and gives up
    if that fails, so the A/UX build skips the call when the header doesn't
    define it.
  - `-ip <addr>` (mode_client.c:85, mode_update.c:90) bypasses the beacon
    entirely.
  - A known A/UX bug: the startup scripts ignore `/etc/NETADDRS`' broadcast
    address. Add `broadcast` to the ifconfig line.
- Throughput is unverified. Guess 100-300KB/s, so 1-3 minutes per 16MB.

### Speed

- The CPU is a 68030 at 15.67 MHz with a 68882, 256-byte caches and no
  external cache. A Dhrystone run under Mac OS measured 2,667 per second,
  about 1.5 DMIPS (coarse timer).
- Unlike the 68000, the 68030 does misaligned word and long accesses in
  hardware, so unaligned loads cost time but never trap.
- There are no SHA-1/RC4 measurements for this CPU. Estimates: SHA-1
  50-120KB/s, RC4 250-400KB/s.

Where the time goes, for one build:

- **Page ECD.** `pageEccOk` (image_write.c:358) runs on every used page of
  a dump being loaded (`blockEccOk`, image_read.c:1108). `calcEcd`
  (image_write.c:321) runs on every used page written. Both loop over 4198
  bits per page, about 11 instructions per bit with gcc 2.7.2, so roughly
  13ms per page. That is up to 7 minutes per pass for 16MB and up to 28 for
  64MB.
- **Disk.**
  - 16MB: 15-35 seconds each way.
  - 64MB: 1-2 minutes each way.
  - The nandmu MU copy (462MB for a Jasper 512): 15-30 minutes.
- **Crypto.**
  - The bootloaders' RC4, SHA-1 and HMAC take tens of seconds.
  - An RSA-2048 verify (small public exponent) is at most about 17 modular
    multiplies, around a second.
  - `blSign`'s private-key resign (devkit with `SB_priv.bin`) is two
    1024-bit CRT exponentiations, around a minute.
  - xeBuild doesn't generate keys.
- **The optional SHA-1 of the whole output** (`xb.sha1Write`,
  image_write.c:1172) costs 2-5 minutes for 16MB, 10-20 for 64MB, and over
  an hour with a nandmu MU copy.

## Toolchain

| Option | State | Verdict |
|---|---|---|
| A/UX `cc` | K&R, no ANSI mode, `long long` unlikely; COFF via `/bin/as`, `/bin/ld` | no |
| Apple `c89` (A/UX Developer Tools 1.1, sold separately) | ANSI C89; `long long` unknown | fallback only |
| gcc 2.7.2 (Jim Jagielski's A/UX port), native | binary on a mirror of ftp.mayn.de (discmaster), installs in `/usr/local/Gnu`; gas and the native `ld` through collect2 (as the 2.5.7/2.6.3 READMEs describe) | **recommended** |
| gcc ≤ 3.2 cross (`--enable-obsolete`) and binutils ≤ 2.30 | GCC 3.1 obsoleted A/UX and 3.3 removed it; binutils dropped A/UX COFF in 2.31. 2002 sources on a 2026 host | not worth it |
| uyjulian/aux_crosscompile_toolchain | modern ELF binutils/gcc and an A/UX 3.1 sysroot; work in progress (headers are the open blocker) | watch it |
| Retro68 | builds Mac OS applications, not Unix processes | no |

What gcc 2.7.2 gives: `long long` with libgcc's 64-bit divide (the build
already calls `__divdi3`, `__moddi3`, `__udivdi3` and `__umoddi3`), `//`
comments (unless `-ansi`), `inline` with the gnu89 rules, `__attribute__`,
`-include`, and `-O2`/`-O3`. What it doesn't: mixed declarations and code
(gcc 3.0), C99 flexible arrays and `_Bool` (3.0), C99 `inline` semantics
(4.3), `__builtin_bswap*` (4.3), `_Static_assert` (4.6), `stdint.h`, and the
`-MF -MT -MP` dependency flags (3.0).

Its A/UX configuration predefines `unix`, `m68k` and `AUX` (and gcc's
`__m68k__` spellings). It defaults to 68020 code with inline 68881
instructions (`TARGET_DEFAULT` is 68020 | 68881 | bitfield). Its driver
knows A/UX `cc`'s `-ZP`/`-ZS`/`-ZB` (POSIX, SVID, BSD) environment flags.

### Development setup

Compile in an emulator; run on the SE/30.

1. **QEMU's `q800` (QEMU 8.2 or later)** boots A/UX 3.0.1 with a real
   Quadra 800 ROM (checksum 0xf1acad13). AUXrunner packages a QEMU A/UX
   with FTP from the host. Use it to compile and to run the image suite: it
   is far faster than an SE/30.
   - It emulates a 68040, so it can't catch 68030-only problems.
   - Keep gcc's 68020/68881 defaults and never pass `-m68040`.
   - Reboots don't work; kill QEMU at the chime.
2. **An SE/30 emulator** checks the 68030 and SE/30 hardware before the
   real one:
   - Snow emulates the SE/30, and v1.5.0 added A/UX support. A forum report
     has A/UX 3.1 running on its SE/30.
   - MAME has a `macse30` driver; its wiki marks A/UX booting as fixed in
     0.289.

   Shoebill emulates only the II, IIx and IIcx, and has been unmaintained
   since 2016.
3. **The real SE/30**, last.

Build on the same A/UX release as the SE/30, so the binary links against
the same libc. Whether 3.0.1 binaries use a shared libc that differs
between releases is unverified. A static link avoids the question, if A/UX
`ld` allows one.

### Getting files in and out

- A/UX 3.0.1 has `ftp`, `ftpd`, `telnetd` and NFS (`mount -t nfs`). Once
  the network is up, FTP the source tarball and the data in, and the images
  out.
- Without a network: A/UX can't mount HFS, and nothing modern writes A/UX
  UFS. So put the files on an HFS volume (hfsutils `hcopy`), copy them
  across in A/UX's Finder, and run `fcnvt` to strip the AppleSingle data
  (FAQ M.07).
- A/UX's `tar` is the old format, with a 100-character path limit;
  xeBuild's paths are well under it. Ship an uncompressed tar, or use
  A/UX's `compress`.

## Code changes

### 1. Prerequisite: the big-endian plan, with m68k deltas

plans/big-endian.md steps 1-6 do the byte-order work: swap macros, read
helpers, pre-swapped constants, EDC words, bit-fields, host-order views and
XeCrypt. Its old-compiler shims are `_Static_assert`, `XB_EXTERN_INLINE`
and no builtins on big-endian paths.

For the 68030 it needs these additions:

- **Byte-order test.** gcc 2.7.2 defines neither `__BYTE_ORDER__` (gcc 4.6)
  nor `__BIG_ENDIAN__` (PowerPC and Apple only). So `XB_BIG_ENDIAN`
  (xebuild.h) and `XECRYPT_BIG_ENDIAN` (xecryptTypes.h) each get a branch:

  ```c
  #elif defined(__m68k__) || defined(m68k) || defined(__mc68000__)
  #define XB_BIG_ENDIAN 1
  ```

  Add it to plans/xecrypt-big-endian.patch before the upstream PR. Until
  then, the A/UX build can pass `-DXECRYPT_BIG_ENDIAN=1`, the override the
  patch already allows.
- **Gladman's AES.** brg_endian.h:42 includes `<endian.h>` and
  `<byteswap.h>` whenever `__GNUC__` is defined, and A/UX has neither. The
  compat layer (3 below) supplies an `endian.h` that defines `__BYTE_ORDER`
  as `__BIG_ENDIAN`, which brg_endian.h:80 then picks up, and an empty
  `byteswap.h`. XeCrypt is unchanged.
- **Bit-fields.** gcc fills m68k bit-fields from the top bit, as on
  PowerPC, so the plan's reversed declarations apply. Confirm it with a
  probe on A/UX (Verification).
- **Alignment.**
  - The m68k System V ABI aligns `int`, `long`, pointers and `long long` to
    2 bytes, not 4 or 8. A gcc 6.2 `-Wpadded` pass over every file finds
    implicit padding only in `struct smcopts` (xebuild.h:545). That struct
    is in-memory and the padding is at its end, so every on-disk and wire
    struct keeps its offsets and size.
  - The big-endian plan's layout asserts (`struct flashhdr` 0x80,
    `struct consoleinfo` 0x4a0, ...) prove this at compile time; on gcc
    2.7.2 they go through the `_Static_assert` shim.
  - `blSign`'s `aligned(8)` may not be honoured on gcc 2.7.2's stack, which
    is harmless on a 68030.
- **Unaligned loads.** The plan's fixes are still needed (they're undefined
  behaviour), but on the 68030 they're about correctness, not traps.

### 2. C features gcc 2.7.2 lacks

Found by compiling every file with the pinned gcc 6.2 and
`-std=gnu89 -Wc90-c99-compat -Wdeclaration-after-statement -DXEBUILD_FIXES`.
That list, minus what gcc 2.7.2 accepts as GNU C:

| Feature | Where | Change |
|---|---|---|
| `_Bool` | image_write.c:630, options.c:301, 304 | compat header: `#define _Bool int` (gcc < 3). Every value stored is 0 or 1 (a comparison, or getIniBool's 1/0/`def`), so the result is the same; check `optIniBool`'s callers pass `def` as 0/1 |
| `bool`, `<stdbool.h>` | fileutil.c:10, 366 | compat `stdbool.h` |
| flexible array member | console_hdd.c:56 (`struct mfEntry e[]`) | `e[XB_FLEX]`. xebuild.h defines `XB_FLEX` as empty unless it's already defined, and auxcompat.h defines it as `0` (a GNU zero-length array) for gcc < 3. gcc 6.2's preprocessed text is unchanged; `make check` |
| mixed declaration | mode_update.c:746 (`char *arg = argv[i];`) | respell (declare at the top of the arm's block); `make check` decides whether it's the same bytes. If not, `#if` it |
| `_Static_assert`, `extern inline`, `__builtin_bswap*` | xebuild.h:44-45, image_read.c:915, keys.c:688, ... | the big-endian plan's step 6 shims |

Nothing to do for these, which gcc 2.7.2 accepts as GNU C: `//` comments
(never pass `-ansi`), `long long` and `LL`/`ULL` constants, and trailing
commas in enums. All three are common in src/ and src/crypto.

### 3. The A/UX compat layer

A new directory, src/port/aux/, used only by the A/UX build script. It is
not in `OBJECTS`, so the reference build never sees it. Check that
tools/re/progress.py and fncmp.py don't count it.

The script force-includes `auxcompat.h` (`-include`) ahead of every file,
so the app's sources need no A/UX `#ifdef` for these.

Headers:

- `stdint.h`, `inttypes.h`: the exact-width types over char, short, int and
  `long long`; no `PRI*64`, since A/UX's printf has no `ll`.
- `stdbool.h`; `endian.h` and an empty `byteswap.h` (for brg_endian.h).
- `sys/select.h`, which includes `<sys/types.h>` and `<sys/time.h>`.
- `auxcompat.h`:
  - `_Bool` and `XB_FLEX` for gcc < 3.
  - `fseeko`/`ftello` as `fseek`/`ftell` (xebuild.h already maps
    `fseeko64` to `fseeko`; every file is under 2GB).
  - The prototypes for auxcompat.c.

Functions (auxcompat.c). The A/UX 3.0.1 man pages document no `snprintf`,
`vsnprintf`, `strcasecmp`, `strdup`, `strerror`, `memmove`, `fseeko` or
`inet_pton`. xeBuild needs these:

| Missing | Used by | Replacement |
|---|---|---|
| `vsnprintf` | log.c:80, mode_ini.c:58 (512-byte buffers) | `vsprintf` into a 16KB static buffer, then a truncating copy. Messages are a format plus paths of at most `MAXPATHLEN`, so 16KB doesn't overflow. A bundled portable `vsnprintf` is the alternative |
| `strcasecmp`, `strncasecmp` | `stricmp`/`strnicmp` (xebuild.h:29-30), 174 calls | ten-line versions |
| `inet_pton` | net.c:61 (`WSAStringToAddressA`) | `inet_addr` for the dotted IPv4 form |
| `SO_BROADCAST` | net.c:115 | `#ifdef SO_BROADCAST` around the call (receiving the beacon doesn't need it) |

Check these exist when bringing A/UX up (Phase 0); each is a one-line shim
if not:

- `remove`: else `unlink`.
- `difftime`, `gmtime`, `mktime`, `rename`, `chdir`.
- `opendir`/`readdir`: `<dirent.h>` is documented.
- `SIGABRT`: else `SIGIOT`.
- `select`, `setsockopt`, `recvfrom`.
- Which library holds the socket calls (man sections 2N and 3N): libc,
  `-lbsd` or another.

Formats. A/UX's printf documents only the `l` modifier, so the two 64-bit
conversions change, under `XEBUILD_FIXES` so that every fixes build prints
the same:

- image_read.c:1506, 1509 print a file size with `%llx`. Use
  `(unsigned long)size` and `%lx`: a dump is at most 528MB.
- The KV serial uses `"%011" PRIu64` (keyvault.c:15-19). Format the
  `uint64_t` in decimal by hand, with the same 11 digits, through libgcc's
  64-bit divide.

Other A/UX notes:

- The FAQ says A/UX's `<sys/types.h>` makes `size_t` signed. Watch the
  first compile for comparison warnings; xeBuild mostly uses `int` and
  `uint32_t`.
- `rand()` returns 15 bits. `XeCryptRandomInit` and `GetSystemTime` use
  only the low bits, so this changes nothing.
- The signal handlers (main.c:73-78) use plain `signal()`. Under System V
  semantics a handler resets after one signal; xeBuild's handlers exit,
  so it doesn't matter.

### 4. Build: a shell script and `make aux-dist`

A/UX has at most GNU make 3.74 (ported), and the Makefile needs 3.81
(`else ifeq`) and gcc 3's dependency flags. So:

- tools/aux/build.sh, a Bourne shell script:
  - It compiles the objects in `OBJECTS` order from a generated
    `objects.txt`:
    - app files: `gcc -O2 -DXEBUILD_FIXES -DXEBUILD_TARGET='"m68k-apple-aux3.0.1"' -Isrc/port/aux -include auxcompat.h`
    - `src/crypto` files: the same, plus `-Isrc/crypto`.
  - It links with the POSIX environment, gcc's `-ZP` (exact libraries to
    confirm in Phase 0), then strips.
  - `-O2`, not `-O3`: gcc 2.7.2's `-O3` only adds `-finline-functions`, and
    the old optimiser is the likelier source of miscompiles. Try `-O3` once
    the image suite passes.
- A `make aux-dist` target on the host writes build/aux/xebuild-aux.tar:
  src/ (with src/port/aux), tools/aux/build.sh, and `objects.txt` written
  from `$(OBJECTS)`. The link order stays defined in one place. The
  target adds no recipe to the existing ones, so `make check` is
  unaffected.
- Expect a full compile to take most of an hour on the SE/30 (an estimate)
  and a few minutes in QEMU.
- A `PLATFORM=aux` section in the Makefile only makes sense if a cross
  compiler becomes practical (Toolchain).

### 5. Memory (`XEBUILD_FIXES`)

Peaks today, from the allocation sites, for 128MB of RAM:

| Job | Today | After (a)-(d) |
|---|---|---|
| 16MB image from a 16MB dump | about 50MB: dump, image, raw | about 20MB |
| 48MB eMMC (Corona 4GB) | about 100MB: load `raw` + dump, then dump + image | about 50MB |
| 64MB big block from a big block dump | about 200MB: load `raw` + dump, then dump + image + `xb.raw` | about 70MB |
| the same with nandmu | as above, plus an extra 190/462MB at once (Jasper 256/512, image_read.c:1411) | about 135MB (it keeps the dump, see (b)); an extra 64KB for the MU copy |

Each figure also includes the loaded flash files, a few MB.

Over physical RAM, A/UX pages to the swap partition, at the SCSI speeds
above. So these four, each with the original in the `#else`:

- **(a) Chunked MU copy, and its seek.** `copyMuData` (image_read.c:1379)
  seeks with `fseek(fp, 0x4200000, SEEK_END)` (line 1404). That is past the
  end of the file, so the "MU data" written is uninitialised memory. This is
  the big-endian plan's "Found on the way" bug. Seek from `SEEK_SET`, and
  copy and hash in 64KB chunks.
- **(b) Free the dump once it's loaded.**
  - Its only later readers are the nandmu restore (image_write.c:1305-1306)
    and extract mode (mode_extract.c:115). Confirm there are no others
    first.
  - Without those, free `xb.dump`/`xb.dumpSpare` after `loadDump`
    (image_read.c:1699) has taken the KV, SMC, mobiles and security files.
  - A nandmu build still keeps the dump for the restore, unless the
    restore re-reads those blocks from the dump file. Re-reading brings a
    64MB nandmu build down to about 70MB too.
- **(c) Write the raw image a block at a time.**
  - `finalizeImage` (image_write.c:1202) mallocs `xb.rawSize` (line 1214)
    and assembles the whole image. `writeImage` (image_write.c:1127)
    writes it, and hashes it if asked (line 1172).
  - Instead, assemble each block into a 0x21000-byte buffer and write and
    hash it.
  - The nandmu restore (image_write.c:1298-1306), which copies dump blocks
    into `xb.raw`, moves into the same loop.
- **(d) Read the dump a block at a time.** `loadDump` reads the whole raw
  dump (image_read.c:1764) before splitting it into `xb.dump` and
  `xb.dumpSpare`. `parseDump`'s remapping reads blocks from that buffer.
  This is the largest of the four; it's needed only for the 132MB load peak
  of a 64MB dump.

They help every platform, including the Xbox 360 itself (big-endian plan).
Each gets a README line.

### 6. Speed (`XEBUILD_FIXES`)

- **Table-driven ECD.**
  - The ECD loop (`calcEcd`/`pageEccOk`, image_write.c:321, 358) is a
    reflected LFSR:

    ```c
    val ^= bit;
    if (val & 1)
    {
    	val ^= 0x6954559;
    }
    val >>= 1;
    ```

  - The bits are taken from bit 0 of each little-endian word. That is
    the same as each byte in memory order, low bit first, inverted.
  - So the byte-at-a-time form
    `val = (val >> 8) ^ ecdTable[(val ^ (uint8_t)~*p++) & 0xff]` gives the
    same result over the 512 data bytes and the first 12 spare bytes. The
    last 6 bits stay bit-serial.
  - That's about ten times fewer instructions: under a minute per 16MB pass
    on the SE/30.
  - It is also byte-order independent, so these two loops no longer need
    the big-endian plan's `LE32_WORD`.
  - Check it against the bit-serial version on random pages (a test
    program) and with the image suite.
- **Leave the whole-image SHA-1 off** unless it's wanted (Speed above).
- **Run without the Finder**, over telnet: the Mac environment costs memory
  and CPU.

## Verification

1. **`make check` after every step.** The big-endian plan's steps and the
   respelled sites must not change the reference build. Everything else is
   under `XEBUILD_FIXES` or only in the A/UX build.
2. **Probes, in QEMU and on the SE/30, before xeBuild itself:**
   - byte order and bit-field order (a struct of `b1lo:4, b1hi:4` over a
     known byte);
   - `sizeof`/`offsetof` of the on-disk structs (build them with the
     layout asserts);
   - `long long` multiply, divide and shift against known values;
   - `printf("%lx")`;
   - a malloc probe that grows until it fails, which measures the
     effective `MAXUMEM`;
   - whether `SO_BROADCAST` is defined, and receiving a broadcast.
3. **The image suite** (big-endian plan, Verification 3). Every output must
   match the x86-64 Linux fixes build byte for byte, using `-norandom`,
   `SOURCE_DATE_EPOCH` and `TZ=UTC`.
   - Run the whole matrix in QEMU, which is fast.
   - Run a subset on Snow or MAME `macse30`, then on the SE/30: one 16MB
     glitch2 build from a dump, one 64MB big block build, one nandmu
     build, extract, and client mode against a console.
   - Record the timings in a NOTES.md table.
4. **Hardware.** Flash an image the SE/30 built to a real console and boot
   it.

## Order of work

0. **Bring-up, no code.**
   - Settle the ROM: stock ROM, or the ROMinator if it boots.
   - Install A/UX 3.0.1 on UFS, with swap of at least 256MB.
   - Set up the Ethernet card and FTP.
   - On the host: QEMU `q800` with A/UX 3.0.1.
   - Install gcc 2.7.2 in both.
   - Run hello world and the probes (Verification 2) in both.
1. **The big-endian plan, steps 1-6**, with the m68k deltas in 1. Each step
   ends with `make check` and a commit; PowerPC cross-compiles catch breaks
   early.
2. **gcc 2.7.2 and A/UX support:**
   - the six sites in 2;
   - src/port/aux;
   - tools/aux/build.sh and `make aux-dist`.
   - The first A/UX binary, built in QEMU.
3. **The image suite in QEMU** against x86-64 Linux; fix every difference.
4. **Memory (a)-(d) and the table-driven ECD**, each with `make check` and a
   README line.
5. **Snow/MAME SE/30, then the real SE/30**: the subset, timings, client
   mode, and flashing a console.
6. **Docs:**
   - README: an `aux` row in the platform table (built with
     tools/aux/build.sh, not the Makefile), and a line per new fix.
   - NOTES.md: the A/UX notes and the timings.

Phase 0 decides whether the rest is worth doing on this machine. Phases 1
and 4 are useful to every platform even if the SE/30 never runs xeBuild.

## Risks and open questions

- **ROM.** A non-stock ROM may not boot A/UX at all (The machine). This is
  the first thing to test.
- **128MB.** It works for two SE/30 owners; one Quadra 950 test found
  128MB too much. Fall back to 64MB: the memory fixes keep every job under
  about 70MB, except a nandmu build that keeps its dump (5 (b)).
- **A/UX version.** 3.0.1 is the supported one. If 3.1.1 is what's
  installed, test it before relying on it.
- **gcc 2.7.2 availability.**
  - The binary survives on one mirror (discmaster's copy of ftp.mayn.de,
    `apple/apple_unix/GNU_stuff`). It isn't known which A/UX release it
    was built on.
  - Fallback: build gcc 2.7.2 from source with the A/UX diffs
    (`gcc-2.7.2.aux.diffs.gz`, same directory), bootstrapped with A/UX's
    `cc`, in QEMU.
  - Keep a copy of both in tools/packages/, as for the pinned toolchain.
- **gcc 2.7.2 miscompiles.** The image suite is the check. A function that
  differs gets a per-file `-O1` in build.sh and a note.
- **`MAXUMEM`.** The default is unknown, and changing it has broken systems
  before. Measure it first; with the memory fixes it likely doesn't need
  changing.
- **Libraries.** The shared vs static libc across A/UX releases, and
  which library holds the socket calls, are unverified; Phase 0 settles
  both.
- **I/O and network speeds under A/UX** are unmeasured; the estimates come
  from Mac OS and NetBSD on the same hardware.
- **Cross-compiling later.** If uyjulian/aux_crosscompile_toolchain
  matures, a `PLATFORM=aux` Makefile section could replace the in-emulator
  compile. Nothing in this plan depends on it.

## Sources

- A/UX 3.0 Installation Guide and Local System Administration (UFS default,
  2GB files, 4KB pages, swap advice):
  http://bitsavers.trailing-edge.com/pdf/apple/mac/a_ux/aux_3.0/
- A/UX 3.0.1 man pages: `cc`, `kconfig` (`MAXPMEM`, `MAXUMEM`), `socket`,
  `udp`, `printf`, `mount`: https://www.typewritten.org/Manual/Apple/A:UX/3.0.1/
- comp.unix.aux FAQ: 3.1.1 on the SE/30; gcc ports; libUTIL; FTP and file
  transfer; Ethernet cards: http://www.faqs.org/faqs/aux-faq/part1/ (and
  part2-part4)
- aux-penelope (version and hardware chart, setup):
  https://aux-penelope.com/hardware.htm
- ROMs and 128MB on the SE/30: http://www.applefritter.com/node/1744;
  68kmla threads 25528, 36001 and 43415; 128MB on a Quadra 950:
  https://lowendmac.com/2026/fun-with-a-quadra-950-and-a-whole-lot-of-ram/
- gcc 2.7.2 for A/UX:
  https://discmaster.textfiles.com/browse/11929/ftp.mayn.de-pub.zip/ftp.mayn.de-pub/apple/apple_unix/GNU_stuff;
  GCC's A/UX config (`a-ux.h`): predefines and `TARGET_DEFAULT`; GCC 3.1/3.3
  release notes (obsoleted, removed); https://gcc.gnu.org/c99status.html
- Modern A/UX cross toolchain (WIP):
  https://github.com/uyjulian/aux_crosscompile_toolchain
- QEMU q800 and A/UX 3.0.1:
  https://lists.gnu.org/archive/html/qemu-devel/2023-09/msg01975.html;
  AUXrunner: https://mendelson.org/auxrunner.html
- Snow (SE/30 emulator with A/UX): https://github.com/twvd/snow; MAME:
  https://wiki.mamedev.org/index.php/Driver:Mac_68K
- SE/30 Ethernet under A/UX: https://github.com/rhalkyard/SEthernet-AUX;
  68kmla thread 35652 (Farallon PDS)
- SE/30 speed: 68kmla Dhrystone thread 24799; SCSI: lowendmac's SE/30
  benchmarks, NetBSD port-mac68k 2003-11 (Bonnie++, no DMA)
