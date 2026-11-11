# Big-endian (PowerPC) builds

Status: plan only. The XeCrypt part is a ready patch for upstream
(plans/xecrypt-big-endian.patch); nothing in src/ has changed.

Goal: xeBuild builds and runs on big-endian PowerPC and writes the same
files as the x86 builds. Targets: 32-bit G3/G4 Macs (Mac OS X 10.4/10.5 or
Linux), 64-bit G5s, and the Xbox 360 itself: ArchPOWER (32-bit userland on a
64-bit kernel) and the fully 64-bit 360 distributions. So both ILP32 and
LP64 big-endian matter. `make check` keeps the reference SHA256 throughout.

## Summary

The code was written for x86 and assumes a little-endian host in eight
ways. Byte-wise helpers (`getBeU16`, `setBeU16/32/64`, the `p[0] << 8 | p[1]`
reads) are already portable; everything below is not.

| # | What | Where | Sites |
|---|---|---|---|
| 1 | BE/LE read helpers that are x86-only | fileutil.c:39-58 | 3 functions (~60 callers) |
| 2 | Unconditional swap macros, `__builtin_bswap16` | xebuild.h:60-69; build.c, image_read.c | 133 macro uses, 8 builtins |
| 3 | Constants stored pre-swapped | image_write.c `buildImage`, build.c, smc.c | 28 header values, 1 SMC value, 12 byte patterns |
| 4 | EDC (page ECC) computed over native 32-bit words | image_write.c:286, 322 | 2 loops |
| 5 | Bit-fields laid over on-disk bytes | image_write.c, image_read.c, build.c, stfs.c | 8 structs |
| 6 | Host-order values viewed as bytes, raw copies | keyvault.c, consoleinfo.c, net.c, keys.c, timeutil.c | 7 places |
| 7 | XeCrypt's Xbox-format bignums and key fields | crypto/xecrypt.c, crypto/xecryptBn.c | 32 swaps: upstream patch |
| 8 | Not byte order: alignment, old compilers, Makefile | stfs.c, xboxrom.c, mode_*.c, Makefile | see below |

What a big-endian build does today: dumps fail `checkHeader`'s magic test,
every bootloader fails `checkBl`'s size check ("BL size is bigger than the
file"), so nothing builds. With 1-2 fixed it would build, but every page's
ECC and LBA would be wrong (4, 5), the header's offsets wrong (3), every RSA
check would fail and resigning would write garbage (7), and the SMC and
freeboot patches would silently not apply (3).

The fix keeps the reference build's preprocessed source unchanged: byte
order is one compile-time switch, the conversions become endian-aware macros
whose little-endian expansion is the current text, and the few logic
rewrites go under `XEBUILD_FIXES` (as CLAUDE.md asks), where the x86-64 Linux
and macOS builds run them too. In the app that's about 70 edited sites
plus the macro definitions; the 133 swap-macro uses and the ~60 helper
callers need no edit. XeCrypt's 32 sites go upstream first.

## Findings

### 1. Read helpers (fileutil.c)

- `getBeU32` (fileutil.c:39): `memcpy` then `__builtin_bswap32`, so on a BE
  host it returns the byte-reversed value. Most of the code's big-endian
  reads go through it (bootloader sizes, CF/CG/CE headers, the patch set,
  STFS manifests, net replies, the KV signature area, fuses).
- `getBeU64` (fileutil.c:47): native 64-bit load then `__builtin_bswap64`.
  Unused outside fileutil, but wrong the same way (and an unaligned load).
- `getLeU32` (fileutil.c:52): a plain `memcpy`, so it's a raw copy, not a
  little-endian read, on BE. Its only caller is the beacon (6 below), which
  relies on exactly that.

`getBeU16`, `setBeU16`, `setBeU32`, `setBeU64` and XeCrypt's
`xcgetBeU32/xcsetBeU32` are byte-wise and portable.

### 2. Swap macros and direct builtins

`SWAP16`, `SWAP32` and the per-object spellings (`SWAP32_BUILD`,
`SWAP16_IMAGE_WRITE`, `SWAP32_KEYS`, ...) in xebuild.h:60-69 always swap.
They're used 133 times in 9 files (SWAP32 71, SWAP16_IMAGE_WRITE 24,
SWAP32_IMAGE_WRITE 19, SWAP16 8, SWAP32_BUILD 5, SWAP16_KEYS 3,
SWAP16_BUILD 2, SWAP32_KEYS 1). I checked every use: each converts the
console's big-endian data to or from host order (flash header, FS table and
chain, bootloader headers, STFS entries, the HDD manifest, `struct
consoleinfo` from the console, SMC config fields, the SMC hash words, the CF
patch-slot table, FAT timestamps). None is a swap that must happen on every
host, so on BE they all become the identity.

`calcConfigSum` (fileutil.c:650) returns the SMC config checksum already
arranged for a swapped store (`*(uint32_t *)smc = SWAP32_BUILD(sum)`,
build.c:1062). With an identity `SWAP32_BUILD` the stored bytes are the same
on both hosts, and `smcConfigOk` (smc.c:128) builds its side byte-wise, so it
stays correct.

Eight sites call `__builtin_bswap16` directly for the same purpose:
build.c:885 and 1032 (SMC game region), image_read.c:1624-1690 (`getNonces`'
bootloader magics).

### 3. Pre-swapped constants

Values written with a native-width store into big-endian data, already
byte-swapped by hand, so they come out right only on x86.

`buildImage` (image_write.c:146-245) fills `flashHdr`, whose fields are big
endian, with 28 non-zero literals (the two `kvSize = 0` are fine):

| Field | Literal | Value on disk |
|---|---|---|
| magic | 0x4fff | 0xff4f |
| build | 0x6007 | 0x0760 (1888) |
| qfe | 0x80 | 0x8000 |
| cbOffset | 0x800000 / 0xc00000 | 0x8000 / 0xc000 |
| cfOffset, sysUpdateAddr (JTAG) | 0x700 | 0x70000 |
| sysUpdateCount | 0x0200 | 2 |
| kvVersion | 0x1207 | 0x0712 |
| kvAddr | 0x400000 | 0x4000 |
| kvSize | 0x400000 / 0x800000 | 0x4000 / 0x8000 |
| patchSlotSize | 0x100 / 0x200 | 0x10000 / 0x20000 |
| smcBootSize, smcBootAddr | 0x300000, 0x100000 | 0x3000, 0x1000 |
| smcBootAddr, smcBootSize (Corona/Winchester) | 0x800, 0x3800 | 0x80000, 0x380000 (see Found on the way) |

`patchSmcConfig` stores the default DVD region as `0x1000000` (big-endian 1)
through a `uint32_t *` (build.c:1044).

Byte patterns kept in integers and passed to `findInst`/`replaceInst` as
bytes. On BE they search for the reversed bytes, so the patch is skipped
with a warning, or silently:

| Where | What | Bytes searched |
|---|---|---|
| build.c:2655-2656 | freeboot hold address (`hold[0..1]`) | 80 00 00 00 01 00 30 78 |
| build.c:2710-2711 | 9199 replacement (`hold[2..3]`) | 80 00 00 00 00 1f ff f8 |
| build.c:2724 | payload `li r4, n` (`pat`) | 38 80 ff ff |
| smc.c:39 | JTAG/glitch check (`pat2`) | d0 00 00 1b |
| smc.c:102 | smcnoeject (`inst`, `repl`) | a2 90 b3 22 → c3 22 00 00 |
| smc.c:114 | smcnoblink (`inst[2]`, `repl[2]`) | e4 a2 cf 92 e0 a2 ce 22 → e4 d3 22 00 ... |

`mode_client.c`'s `0xffffffff` section marker is the same either way.

### 4. EDC over native words (image_write.c)

`calcEcd` (286) and `pageEccOk` (322) read the 512 data bytes and 12 spare
bytes as `unsigned int *` and consume each word from bit 0 up: the NAND EDC
is defined over little-endian 32-bit words. On BE every page's ECD is wrong:
built images fail ECC on the console, every block of a dump reads as an ECD
error (and gets remapped), and `checkHeader` takes a raw dump for an MMC one.

### 5. Bit-fields over on-disk bytes

gcc allocates bit-fields from the low bit on x86 and from the high bit on
big-endian PowerPC (Linux and Darwin), so these nibbles and flags swap
places within their byte:

| Struct | Where | Fields | Used for |
|---|---|---|---|
| `spb`, `sps`, `sp`, `spt` | image_write.c:29-38 | `b1lo/b1hi`, `b2lo/b2hi`, `type:6/ecc3:2` | LBA high nibble and block type in every page's spare |
| `bigSpare`, `smallSpare` | image_read.c:990-1007 | `blockId0/fsUnused0`, `fsBlockType/ecc3` | reading a dump's LBAs, MU detection, controller detection |
| `fan` | build.c:371 | `speed:7/override:1` | SMC config fan display |
| `stfsEnt` | stfs.c:14 | `namelen:6/contig:1/dir:1` | STFS entries: non-contiguous files are skipped, so system update extraction breaks |

### 6. Host-order values viewed as bytes, raw-copy assumptions

- `kvGetGameRegion` (keyvault.c:100): a native `uint16_t` load from the KV,
  then a hand-written swap (`((x & 0xff) << 8) + (x >> 8)`).
- `showImageType` (consoleinfo.c:175): `((uint8_t *)info)[4] == 8 ||
  (((uint8_t *)info)[8] & 8)`. `netReadInfo` has already converted those
  fields to host order, so x86 tests the low bytes of `kernel` and
  `usvrFlags` and PowerPC the high bytes: client mode would pick the wrong
  `bb`/`bigffs` console type. Keep x86's meaning. Its intent is unclear
  (it reads the kernel version's QFE byte).
- Beacon (net.c:149, 453, 459): the console's IPv4 address is copied with
  `getLeU32` into `addr` and from there into `sin_addr.s_addr`, and the log
  prints it from the low byte up. That works because `getLeU32` is a raw
  copy on x86. Once `getLeU32` really reads little-endian (1), a BE host
  would connect to the reversed address. It should be a raw 4-byte copy,
  printed byte by byte.
- Dates in secdata, CRL and DAE (keys.c:902, 960, 989, from build.c:3467-3479):
  `memcpyrev(dst, (uint8_t *)&ft, 8)` turns the host `FILETIME` into a
  big-endian 64-bit count only on a little-endian host. The date is then
  encrypted into the file, so the damage doesn't show.
- `LARGE_INTEGER` (timeutil.c:35-43): `{LowPart, HighPart}` over
  `QuadPart` is little-endian only (Wine swaps them under `WORDS_BIGENDIAN`),
  and `DosDateTimeToFileTime` writes `QuadPart` straight into the `FILETIME`
  through a cast (timeutil.c:295). On BE the round trips cancel out, but
  every `FILETIME` holds its halves swapped, which then reaches the dates
  above.
- Build number (mode_update.c:205, mode_client.c:387-399):
  `*(uint16_t *)((uint8_t *)info + 5)` reads bits 8-23 of the host-order
  `kernel`. It gives the same number on both byte orders, by luck, but it's
  an odd-address load. Spell it `(uint16_t)(info->kernel >> 8)`.

### 7. XeCrypt

XeCrypt keeps keys and bignums in the console's layout: `u64` digits, least
significant first, each one big endian, plus big-endian `cqw`/`dwPubExp`.
Its PC port converts with unconditional `bswap32`/`bswap64`:

- xecryptBn.c: `XeCryptLoadQuad`/`XeCryptStoreQuad` (45, 61) have an
  aligned fast path that byte-swaps a native load; the byte-wise path is
  portable. `XeCryptBnQwNeModMul` (238, 8 swaps) and `XeCryptBnQwNeCompare`
  (380, 2) swap each digit.
- xecrypt.c: 20 swaps of key fields and constant digits in
  `XeCryptBnQwBeSigCompute/Verify/Create`, `XeCryptBnQwNeRsaPrvCrypt/PubCrypt`,
  `XeKeysPkcs1Verify/Create` and `XeCryptBnQwNeRsaKeyGen`.
- The one swap that must stay: `XeCryptBnQw_SwapDwQwLeBe` (xecrypt.c:25)
  reverses each qword whatever the host.

On BE today `bswap32(pRsa->cqw)` is 0x20000000, so every signature check
fails (CB, CD, KV, CRL, FCRT) and `blSign` can't sign.

The other crypto is portable as built: AES (Gladman's brg_endian.h detects
PowerPC on Linux and Darwin; `SAFE_IO` byte-wise I/O; `FIXED_TABLES` are
built for the byte order), SHA-1 (neither `L_ENDIAN` nor `B_ENDIAN` is
defined, so it takes the byte-wise path), MD5 (word loads only on
x86/vax), DES (byte-wise `LOAD32H`), RC4, BigDigits (32-bit `DIGIT_T`
arithmetic; xecryptBn's conversions to it are byte-wise) and crc32.c. Two
places in BigDigits are little-endian only but xeBuild never calls them (see
Step 2).

### 8. Not byte order

- Unaligned loads: stfs.c:151-158 reads `*(uint32_t *)(hdr + 0x971a)` and
  `+ 0x9722` (2 mod 4); the build-number load above is at an odd address;
  `blSign` (xboxrom.c:42) passes `s.sig`, at offset 36, to XeCrypt as `u64 *`
  and `XECRYPT_SIG *`. PowerPC Linux and Mac OS X fix these up in hardware
  or the kernel's alignment handler, slowly. They're also undefined
  behaviour that `-O3` may exploit. Replace them with `getBeU32`/`memcpy`,
  and align `sig`.
- AltiVec: the Xbox 360's VMX128 is missing some standard AltiVec
  instructions, so xeBuild must contain no vector code on any PowerPC
  build. A binary built on a G4 under ArchPOWER's 32-bit userland may be run
  on a 360, so this applies to every PowerPC build, not just ones made on a
  360. The source has none of its own (no `altivec.h`, `vector` types or
  `vec_*` calls). But gcc generates it whenever the target CPU has AltiVec,
  through `-O3`'s auto-vectorizer and its inline block copies and clears.
  That happens with `-mcpu=7400`/`7450` (G4), `970` (G5, a common ppc64
  default) or POWER7 and later (VSX, which includes AltiVec). Step 6 turns
  it off. libc's own routines (memcpy and the like) pick their
  implementation at run time from the CPU the kernel reports, which is the
  distribution's business.
- Old compilers. `cc` on PowerPC Mac OS X is Apple's gcc 4.0.1 (Tiger) or
  4.0/4.2 (Leopard), and the code doesn't build with it:
  - `_Static_assert` (xebuild.h:44) needs gcc 4.6;
  - `extern inline` (image_read.c:915, keys.c:665) means "no out-of-line body"
    under the gnu89 inline rules that gcc before 4.3 always uses (and gcc 4.3-4.9
    by default), so a call that isn't inlined fails to link;
  - `__builtin_bswap32/64` need gcc 4.3, `__builtin_bswap16` gcc 4.8.

  Step 6 handles all three without touching the reference build. Nothing
  else needs C99 mode or a newer libc: there are no `for (int ...)`
  declarations, no compound literals, and no libc calls Tiger lacks
  (`inet_pton` and `vsnprintf` are there).
- Makefile: `macos` sets `CC := clang`, which doesn't exist on PowerPC Mac OS
  X; `-Wl,-map` may not be supported by the linkers there (cctools ld on
  Tiger, an early ld64 on Leopard). Tiger ships GNU make 3.80, and the
  Makefile's `else ifeq` needs 3.81 (Leopard has 3.81). `linux` works as
  is, natively or with `CC=powerpc-linux-gnu-gcc`; the banner gets the
  triple from `-dumpmachine`.
- `char` is unsigned on PowerPC Linux (signed on Mac OS X). The scan found
  nothing that depends on it: the ini reader uses `unsigned char`, and the hex
  parsers mask with `& 0xFF`.
- 32/64-bit: G3/G4 and ArchPOWER on the 360 are ILP32; G5 and the 64-bit 360
  distributions LP64. LP64 already builds (x86-64 Linux/macOS) but has never
  been checked against the reference's output, so 64-bit PowerPC would
  inherit any LP64 bug.
- Struct layout: the on-disk structs are naturally aligned, so their
  offsets are the same under PowerPC SysV and Darwin's "power" alignment.
  Nothing asserts it yet.
- Memory on the 360 (512 MB shared): building a 64 MiB image from a dump
  peaks at about 200 MB (dump, image, raw buffers), which is fine. But
  `copyMuData` (nandmu) mallocs the whole MU area at once, up to ~450 MB for a
  512 MB Jasper dump; see Found on the way.

## Approach

Rules:

1. For anything outside `XEBUILD_FIXES`, the little-endian preprocessed
   text stays as it is, or folds to the same constants. `make check` proves
   it after every step.
2. One byte-order switch, from the compiler's predefined macros, so no new
   system headers (they could change the reference build).
3. A big-endian build requires `XEBUILD_FIXES` (`#error` otherwise). Every
   platform but win32 already defines it, and win32 is x86 only.
4. Logic rewrites that are better everywhere go under `XEBUILD_FIXES`, with
   the original in the `#else`, so the x86 fixes builds exercise them too.
5. The big-endian code paths use only shift-based swaps, never the
   `__builtin_bswap*` functions, so any gcc or clang compiles them.
6. XeCrypt changes go upstream (cOzInABox/XeCrypt) first; src/crypto then
   syncs to the merged upstream (converted to LF, as now).

### Step 1: the switch, the macros and the helpers

In xebuild.h, after the includes. It mirrors XeCrypt's test from Step 2,
so the app doesn't wait for that PR:

```c
/* 1 on a big-endian host (PowerPC).  gcc 4.6+ and clang predefine
   __BYTE_ORDER__; older gcc on PowerPC and Apple's gcc define __BIG_ENDIAN__.
   The same test as XeCrypt's XECRYPT_BIG_ENDIAN (crypto/xecryptTypes.h). */
#if defined(__BYTE_ORDER__) && defined(__ORDER_BIG_ENDIAN__)
#define XB_BIG_ENDIAN (__BYTE_ORDER__ == __ORDER_BIG_ENDIAN__)
#elif defined(__BIG_ENDIAN__)
#define XB_BIG_ENDIAN 1
#else
#define XB_BIG_ENDIAN 0
#endif
#if XB_BIG_ENDIAN && !defined(XEBUILD_FIXES)
#error "a big-endian build needs XEBUILD_FIXES (the Makefile sets it on every platform but win32)"
#endif

/* swaps with shifts: any compiler, folded for constants (x is used more
   than once) */
#define BSWAP16(x) ((uint16_t)((((x) & 0xffu) << 8) | (((x) >> 8) & 0xffu)))
#define BSWAP32(x) ((uint32_t)((((x) & 0xffu) << 24) | (((x) & 0xff00u) << 8) | \
			(((x) >> 8) & 0xff00u) | (((x) >> 24) & 0xffu)))
```

The swap macros become:

```c
#if XB_BIG_ENDIAN
/* the console's data is already in host order */
#define SWAP16(x) ((uint16_t)(x))
#define SWAP32(x) ((uint32_t)(x))
#define SWAP32_BUILD(x) SWAP32(x)
#define SWAP16_BUILD(x) SWAP16(x)
#define SWAP16_IMAGE_WRITE(x) SWAP16(x)
#define SWAP32_IMAGE_WRITE(x) SWAP32(x)
#define SWAP32_KEYS(x) SWAP32(x)
#define SWAP16_KEYS(x) SWAP16(x)
#define SWAP16_BUILTIN(x) SWAP16(x)
#else
/* the current definitions, character for character */
...
#define SWAP16_BUILTIN(x) __builtin_bswap16(x)
#endif
```

Every use passes a 16- or 32-bit value, so the casts lose nothing. The 8
`__builtin_bswap16(...)` calls become `SWAP16_BUILTIN(...)`, which expands
to the same tokens on little-endian. Optionally, later: rename
`SWAP16/32*` to `BE16/BE32*` to say what they do. A macro's name doesn't
reach the compiler, only its expansion.

fileutil.c: `getBeU32` and `getLeU32` keep their `memcpy` and swap only on
the other byte order; `getBeU64` does the same through `memcpy`:

```c
unsigned int getBeU32(const uint8_t *p)
{
	uint32_t v;

	memcpy(&v, p, 4);
#if XB_BIG_ENDIAN
	return v;
#else
	return __builtin_bswap32(v);
#endif
}

unsigned int getLeU32(const uint8_t *p)
{
	uint32_t v;

	memcpy(&v, p, 4);
#if XB_BIG_ENDIAN
	return BSWAP32(v);
#else
	return v;
#endif
}
```

### Step 2: XeCrypt (upstream PR)

The patch is plans/xecrypt-big-endian.patch (3 files, +54 -31). It applies
with `git apply` to upstream's `main`, which is still 7d619af, the commit
src/crypto was copied from. Upstream stores LF; a Windows checkout's
CRLF comes from `core.autocrlf`.

xecryptTypes.h, after the `bswap` block:

```c
// host byte order: XECRYPT_BIG_ENDIAN is 1 on a big-endian host (PowerPC).
// gcc 4.6+ and clang predefine __BYTE_ORDER__; older gcc on PowerPC and
// Apple's gcc define __BIG_ENDIAN__. Define it before this header to override.
#ifndef XECRYPT_BIG_ENDIAN
	#if defined(__BYTE_ORDER__) && defined(__ORDER_BIG_ENDIAN__)
		#define XECRYPT_BIG_ENDIAN (__BYTE_ORDER__ == __ORDER_BIG_ENDIAN__)
	#elif defined(__BIG_ENDIAN__)
		#define XECRYPT_BIG_ENDIAN 1
	#else
		#define XECRYPT_BIG_ENDIAN 0
	#endif
#endif

// the 360's big-endian values (key fields, bignum digits) to and from host
// order; bswap16/32/64 above always swap
#if XECRYPT_BIG_ENDIAN
	#define XeBe32(x) (x)
	#define XeBe64(x) (x)
#else
	#define XeBe32(x) bswap32(x)
	#define XeBe64(x) bswap64(x)
#endif
```

It doesn't test `_BIG_ENDIAN` or `BIG_ENDIAN`: some libcs define those on
every host. MSVC defines no `__BYTE_ORDER__`, so it gets 0, which is right
for every Windows target.

Then every `bswap32(` and `bswap64(` in xecrypt.c and xecryptBn.c becomes
`XeBe32(`/`XeBe64(`, except xecrypt.c:25:

| File | Function | Sites |
|---|---|---|
| xecrypt.c | `XeCryptBnQwBeSigCompute` | 339, 340, 342 |
| | `XeCryptBnQwBeSigVerify` | 355, 357 |
| | `XeCryptBnQwBeSigCreate` | 373, 376, 388, 389 |
| | `XeCryptBnQwNeRsaPrvCrypt` | 444 |
| | `XeCryptBnQwNeRsaPubCrypt` | 474, 479, 481 |
| | `XeKeysPkcs1Verify`, `XeKeysPkcs1Create` | 521, 538 |
| | `XeCryptBnQwNeRsaKeyGen` | 590, 605, 620, 635, 644 |
| xecryptBn.c | `XeCryptLoadQuad`, `XeCryptStoreQuad` (fast paths) | 52, 67 |
| | `XeCryptBnQwNeModMul` | 247, 251, 258 (2), 268, 289, 300, 303 |
| | `XeCryptBnQwNeCompare` | 385, 386 |
| kept | `XeCryptBnQw_SwapDwQwLeBe` (always reverses each qword) | xecrypt.c:25 |

Checked:

- With the pinned gcc 6.2.0, `gcc -E` before and after gives identical output
  for xecrypt.c, xecryptBn.c, des/des.c (the other file that includes
  xecryptTypes.h) and app files that reach it through xebuild.h (build.c,
  image_write.c, keys.c, xboxrom.c). So the local copy, synced to it, still
  passes `make check`.
- Forced on (`-DXECRYPT_BIG_ENDIAN=1`), both files compile cleanly, and
  only the `SwapDwQwLeBe` swap remains in the preprocessed xecrypt.c.
- Upstream's whole tree (its 60 bign files, `xecryptHmacSha.c`, which xeBuild
  doesn't link) has no other `bswap` or `XeCryptLoadQuad` use.

Also worth raising in the PR, but not needed by xeBuild (it never calls
them). Adding them locally would change the reference build:

- bign/pkcs1-rsa.c:454, 602, 630, 649 (OAEP encrypt/decrypt, PSS sign/verify)
  and bign/base64.c:130 cast byte strings to `DIGIT_T *`. That reads the
  bytes as host-order 32-bit digits, so a BE host gets different results
  from an LE one. Converting each 32-bit word from little-endian bytes
  around the RSA primitive would give BE the LE results.
- `XeCryptBnQwNeCompare` (xecryptBn.c:383) loops `for (i = cqw - 1; i >= 0;
  i--)` on an unsigned `i`: for two equal numbers it runs past index 0 and
  reads out of bounds. It needs its own commit: the fix changes the
  reference build's code, so src/crypto shouldn't sync past it (or only
  under `XEBUILD_FIXES`).

### Step 3: constants

Two constant macros in xebuild.h, built on Step 1's shift swaps. Both fold
at compile time:

```c
#if XB_BIG_ENDIAN
#define BE16C(x) ((uint16_t)(x))	/* a big-endian field's value */
#define BE32C(x) ((uint32_t)(x))
#define BYTES32(x) BSWAP32(x)		/* the word whose bytes in memory are x's on x86 */
#else
#define BE16C(x) BSWAP16(x)
#define BE32C(x) BSWAP32(x)
#define BYTES32(x) (x)
#endif
```

- `buildImage`'s 28 header values are written as what they mean:
  `flashHdr.magic = BE16C(0xff4f)`, `flashHdr.kvAddr = BE32C(0x4000)`,
  `flashHdr.patchSlotSize = BE32C(0x10000)`, and so on (the table in 3).
  It also spells the header fix's `patchSlotSize = 0x100` (0x10000 on disk) as what it means.
  The constants fold to the same numbers, so the code should be identical;
  `make check` decides. Any site where it isn't gets a per-site `#if
  XB_BIG_ENDIAN`.
- build.c:1044: `BE32C(1)`.
- The byte patterns keep their x86 spelling, tagged: `uint32_t pat2 =
  BYTES32(0x1b0000d0);	/* d0 00 00 1b */`. That's the same tokens in
  parentheses on little-endian. Byte arrays would read better, but they
  change the reference build's code, so they'd have to sit under
  `XEBUILD_FIXES` beside the originals. Leave that to de-slopification.

### Step 4: EDC and bit-fields

EDC: one macro for "a little-endian word in host order"; the two loops read
`v = ~LE32_WORD(*data++);` (the same expression as `~*data++` on
little-endian). On BE it's a function, so `*data++` is evaluated once:

```c
#if XB_BIG_ENDIAN
static inline uint32_t xbSwap32(uint32_t v)
{
	return BSWAP32(v);
}
#define LE32_WORD(x) xbSwap32(x)
#else
#define LE32_WORD(x) (x)
#endif
```

Bit-fields: under `#if XB_BIG_ENDIAN`, declare each byte's fields in
reverse order (the `__LITTLE_ENDIAN_BITFIELD` pattern of Linux's `struct
iphdr`). The little-endian text, and the matching notes beside it, are
unchanged:

```c
struct sp
{
	uint8_t b0;
#if XB_BIG_ENDIAN
	/* gcc fills big-endian bit-fields from the top bit */
	uint8_t b1hi:4, b1lo:4;
	uint8_t b2hi:4, b2lo:4;
#else
	uint8_t b1lo:4, b1hi:4;
	uint8_t b2lo:4, b2hi:4;
#endif
	uint8_t b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15;
};
```

The same for `spb`, `sps`, `spt` (`ecc3:2, type:6`), `bigSpare`,
`smallSpare`, `fan` (`override:1, speed:7`) and `stfsEnt` (`dir:1,
contig:1, namelen:6`). Bit-field order is implementation-defined, so the
spare bytes are among the first things to check on a big-endian build
(Verification).

### Step 5: rewrites under XEBUILD_FIXES

Each with the original in the `#else`:

- `kvGetGameRegion`: `f = getBeU16(kv + 0x1c);`, and the last line returns
  `(f & 0x120) != 0`.
- `showImageType`: `(uint8_t)info->kernel == 8 || (info->usvrFlags & 8)`,
  x86's meaning.
- Beacon: copy the 4 address bytes as they are (`memcpy(&a, pkt + 4, 4);
  addr = a;`), and print `((uint8_t *)&addr)[0..3]` in `netConnect`. Same
  output on x86.
- Dates: a helper in keys.c, used at the three `memcpyrev` sites:

  ```c
  /* the FILETIME at date as the console stores it: a big-endian 64-bit count */
  static void putFileTime(uint8_t *out, const uint8_t *date)
  {
  	const FILETIME *ft = (const FILETIME *)date;

  	setBeU32(ft->dwHighDateTime, out);
  	setBeU32(ft->dwLowDateTime, out + 4);
  }
  ```

- timeutil.c: `LARGE_INTEGER`'s two parts in reverse order under `#if
  XB_BIG_ENDIAN`, as Wine does. `DosDateTimeToFileTime` converts into a local
  `LARGE_INTEGER` and copies `u.LowPart`/`u.HighPart` into the `FILETIME`, in
  place of the cast.
- Unaligned loads: `getBeU32(hdr + 0x340)` etc. in `stfsCheckHeader`;
  `(uint16_t)(info->kernel >> 8)` for the build number (mode_update.c:205,
  mode_client.c:387-399); `uint8_t sig[256] __attribute__((aligned(8)))` in
  `blSign`.
- Layout asserts beside the types: `sizeof(struct flashhdr) == 0x80`,
  `struct fsent` 0x20, `struct consoleinfo` 0x4a0, `XECRYPT_RSAPUB_2048`
  0x110, `XECRYPT_SIG` 0x100, `stfsEnt` 64, `offsetof(struct mfFile, hdr) ==
  0x138`, `struct blhdr` 16. They're compile-time only, but that's no reason
  to put them outside `XEBUILD_FIXES`.
- Reproducible output, for comparing runs: `GetSystemTime`
  (timeutil.c:304) uses `$SOURCE_DATE_EPOCH` in place of `time(NULL)` when
  it's set, the reproducible-builds convention. Today `xb.sysTime` is always
  1, so the built-in default time in `makeTimestamp` is unreachable; with
  `-norandom`, this is the last source of variation.

### Step 6: the system cc on Mac OS X, old compilers, docs

Yes, there's an alias: `cc`. On every Mac OS X it's the system compiler:
Apple's gcc on PowerPC 10.4/10.5 (4.0.1 on Tiger, 4.0 or 4.2 on Leopard),
and Apple clang on current Intel and Apple-silicon macOS
(`/usr/bin/cc` runs clang through `xcrun`). It's also GNU make's default
`CC`, which the Makefile already detects as "not given". So `macos` drops
its `CC := clang` and takes make's `cc`. On current macOS that's the same
Apple clang as now. On PowerPC it's Apple's gcc, which the shims below make
work. A newer gcc (MacPorts, Tigerbrew) still works with `make CC=...`.

Makefile:

```make
# --- macos: the system compiler (cc: Apple clang today, Apple gcc on
# PowerPC Mac OS X 10.4/10.5); make's default CC is already cc
else ifeq ($(PLATFORM),macos)
TC_BIN ?=
EXE := build/xeBuild
PLAT_LDFLAGS := -Wl,-x
PLAT_LIBS :=
ifeq ($(shell uname -p),powerpc)
# cctools ld (Tiger) and early ld64 (Leopard) may lack -map;
# make MAP_FLAGS=... puts it back
MAP_FLAGS :=
else
MAP_FLAGS := -Wl,-map,$(MAP)
endif
```

- No AltiVec or VSX on PowerPC, in the fixes block beside `TARGET_TRIPLE`
  (so win32, the reference build, never runs it). The test asks the
  compiler what it targets: gcc and clang define `__powerpc__` on Linux,
  Apple's gcc `__ppc__` and `__POWERPC__`.

  ```make
  # PowerPC: no AltiVec/VMX or VSX code.  The Xbox 360's VMX128 lacks some
  # AltiVec instructions, and gcc's -O3 vectorizer uses them whenever the
  # target CPU has AltiVec (G4, G5/970, POWER7+).  The source has no vector
  # code of its own; CFLAGS=-maltivec puts it back (CFLAGS come last).
  ifneq ($(shell $(TC_ENV) $(CC) -dM -E -x c /dev/null 2>/dev/null | \
  	grep -E '__(powerpc|ppc|POWERPC)__'),)
  PLAT_CFLAGS += -mno-altivec
  # VSX includes AltiVec; gcc before 4.5 (Apple's 4.0/4.2) has no -mno-vsx
  ifeq ($(shell $(TC_ENV) $(CC) -mno-vsx -E -x c /dev/null >/dev/null 2>&1 \
  	&& echo ok),ok)
  PLAT_CFLAGS += -mno-vsx
  endif
  endif
  ```

  The flags only stop gcc from using vector registers. They don't touch the
  ABI: without vector types in the code there's nothing for
  `-mabi=no-altivec` to change. The rest of the instruction set follows the
  compiler's default `-mcpu`, which a distribution that runs on the 360
  already sets to something the Xenon runs.
- `QUIET_WARNINGS` adds its clang-only flags when `$(CC)` is clang
  (`$(CC) -dM -E -x c /dev/null | grep __clang__`), not when the platform
  is `macos`. Its gcc list needs gcc 4.4 or later (older gcc rejects
  unknown `-Wno-` options), so leave `QUIET_WARNINGS` off with Apple's gcc.
- Tiger: GNU make 3.81 or later from Tigerbrew or MacPorts, or built from
  source (Tiger ships 3.80).
- The CI macOS job's "Compiler" step runs `cc --version` instead of
  `clang --version`.

Code shims, all expanding to the current tokens with gcc 6.2:

- xebuild.h, before the asserts: for gcc before 4.6 (not clang), define
  `_Static_assert(e, msg)` as a negative-size array typedef
  (`typedef char XB_CAT(xbAssert, __LINE__)[(e) ? 1 : -1]`, with the usual
  two-level `##` paste macro for `XB_CAT`).
- xebuild.h: `XB_EXTERN_INLINE` is `extern inline` where
  `__GNUC_STDC_INLINE__` is defined (C99 inline rules, as gcc 6.2 uses), and
  plain `inline` otherwise. Under the gnu89 rules plain `inline` is what C99
  calls `extern inline`: inlinable, and the external definition. The two
  `extern inline` functions (image_read.c:915, keys.c:665) use it.
- The big-endian paths need no builtins (rule 5). Intel Macs on 10.4-10.6
  also have gcc as `cc`, and their x86 path calls `__builtin_bswap*`, which
  Apple's gcc 4.0 lacks. That would need a version-tested fallback there.
  Not part of this plan.

Docs:

- README: the `macos` row says "the system `cc`"; PowerPC Linux and Mac OS X
  rows; note that crypto/ is XeCrypt with the upstream big-endian change.
- NOTES.md: a short "Byte order" section (what `SWAP*`, `BE16C`, `BYTES32`
  and `LE32_WORD` mean, and the bit-field rule), so de-slopification keeps
  them straight.
- Optional: a compile-only CI job with Ubuntu's PowerPC cross compilers
  (`gcc-powerpc-linux-gnu`, `gcc-powerpc64-linux-gnu`) catches big-endian
  build breaks before there's hardware or a test run. It can also check
  for vector code (Verification 2), and with `CFLAGS=-mcpu=970` too, to show
  the flags win over a CPU that has AltiVec.

## Verification

1. `make check` after every step. Steps 1, 3, 4 and 6 must not change the
   reference build; step 5 is under `XEBUILD_FIXES`, so it can't, but run
   it anyway; step 2's identity is already shown above (rerun after the sync).
2. No vector code: every PowerPC build's disassembly must have no AltiVec
   or VSX instruction. That means no `v*` mnemonic, no `lv*`/`stv*` vector
   loads and stores, no `mtvscr`/`mfvscr`, `dst*`/`dss*`, `mtvrsave`, and
   no VSX `lxv*`/`stxv*`/`lxs*`/`stxs*`/`xs*`/`xv*`/`xx*`. No scalar
   PowerPC mnemonic starts with those prefixes, so on Linux this is a
   one-liner that must print nothing:

   ```bash
   objdump -d build/xeBuild | awk -F'\t' '{print $3}' | grep -E '^(v[a-z]|lv|stv|lxv|stxv|lxs|stxs|xs|xv|xx|mtvscr|mfvscr|dst|dss|m[tf]vrsave)'
   ```

   (With a cross toolchain, `powerpc-linux-gnu-objdump`; on Mac OS X,
   `otool -tV`, whose columns differ.)
3. Images: the test-file suite, in a later session. For runs to compare
   byte for byte, the build provides `-norandom` (exists), `SOURCE_DATE_EPOCH`
   (step 5), and `TZ=UTC` (`DosDateTimeToFileTime` uses `mktime`). A
   32-bit and a 64-bit big-endian build must each match the x86-64 fixes
   build. The findings say where to aim it:
   - built images for each NAND layout: small block, big block controller,
     big block, bigffs, MMC (ECC, LBAs, spare bytes, header values);
   - dumps read back, including ones with bad blocks and remaps, and the
     noremap/noecdremap options;
   - SMC: each patch option (patchsmc, smcnoeject, smcnoblink) and
     smc_config overrides (fans, game and DVD region, MAC);
   - freeboot with the 9199 kernel string, payload size patching;
   - signatures: SB-signed chains with SB_priv.bin (resigning), KV, CRL,
     FCRT checks;
   - secdata, CRL, DAE dates (with and without `.meta` files);
   - system update extraction (STFS), the ini and extract modes;
   - client mode against a console (beacon address, console info, `bb`/
     `bigffs` detection).
   Run the matrix on x86-64 Linux first: anything it finds there is an LP64
   bug, which 64-bit PowerPC shares.
4. Hardware: flash one image built on a PowerPC host to a real console. That's
   the final proof that ECC, LBAs and signatures are right. Run xeBuild
   itself on the 360 too, with a build made on a G4 or G5 if there is one.

## Order of work

Each app step ends with `make check` and a commit:

1. Switch, swap macros, helpers, `SWAP16_BUILTIN`.
2. XeCrypt: your upstream PR; then sync src/crypto (LF) and `make check`.
3. Constants: header, DVD region, patterns.
4. EDC and bit-fields.
5. `XEBUILD_FIXES` rewrites, layout asserts, `SOURCE_DATE_EPOCH`.
6. Makefile (`cc`, no AltiVec/VSX on PowerPC), old-compiler shims, README,
   NOTES.md.
7. The test-file suite (later session), then hardware.

Steps 1 and 3-6 don't depend on step 2. A big-endian build is right only
once all of 1-6 are in.

## Found on the way (not byte order)

- `copyMuData` (image_read.c:1404, nandmu) seeks with `fseek(fp, 0x4200000,
  SEEK_END)`, 0x4200000 bytes past the end of the file, so `fread` reads
  nothing and the MU area written to the image is uninitialised memory. The
  original does the same (the build matches). Under `XEBUILD_FIXES`: seek
  from `SEEK_SET`, and copy in chunks, which also keeps the 360's memory
  free.
- Corona/Winchester's `smcBootAddr = 0x800`, `smcBootSize = 0x3800` in
  `buildImage` are 0x80000 and 0x380000 on disk. They're harmless:
  `smcSetLoad` rewrites both from the SMC's size (during `loadBlFiles`, after
  `writeInitialHeader`) and a build without an SMC fails. Step 3 keeps the
  bytes; fix them separately if wanted.
- `XeCryptBnQwNeCompare`'s unsigned loop (Step 2).

## Decisions

- XeCrypt: changes go upstream via your PR (the patch here); src/crypto
  syncs afterwards.
- macOS: the system `cc`, whatever it is; old Apple gcc gets shims, not a
  required newer compiler.
- The 360: both ArchPOWER's 32-bit userland and fully 64-bit distributions.
- PowerPC builds have no AltiVec or VSX code (`-mno-altivec`, and
  `-mno-vsx` where the compiler knows it): the 360's VMX128 lacks some
  AltiVec instructions, and one build may run on both a Mac and a 360.
- Testing: the image suite comes in a later session; no qemu runs here.
