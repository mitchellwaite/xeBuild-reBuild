# Big-endian (PowerPC) builds

Status: plan only, nothing implemented.

Goal: xeBuild builds and runs on big-endian PowerPC and writes the same
files as the x86 builds: 32-bit G3/G4 Macs (Mac OS X 10.4/10.5 or Linux),
64-bit G5s, and the Xbox 360 itself under ArchPOWER. `make check` keeps the
reference SHA256 throughout.

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
| 7 | XeCrypt's Xbox-format bignums and key fields | crypto/xecrypt.c, crypto/xecryptBn.c | 32 swaps (2 in a load/store fast path) |
| 8 | Not byte order: alignment, compiler, Makefile | stfs.c, xboxrom.c, mode_*.c, Makefile | see below |

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
and macOS builds run them too. About 100 edited sites plus the macro
definitions; the 133 swap-macro uses and the ~60 helper callers need no edit.

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
arithmetic; xecryptBn's conversions to it are byte-wise) and crc32.c.
bign/pkcs1-rsa.c casts byte strings to `DIGIT_T *` in its
encrypt/decrypt/sign functions, which is little-endian only, but xeBuild
never calls them.

### 8. Not byte order

- Unaligned loads: stfs.c:151-158 reads `*(uint32_t *)(hdr + 0x971a)` and
  `+ 0x9722` (2 mod 4); the build-number load above is at an odd address;
  `blSign` (xboxrom.c:42) passes `s.sig`, at offset 36, to XeCrypt as `u64 *`
  and `XECRYPT_SIG *`. PowerPC Linux and Mac OS X fix these up in hardware
  or the kernel's alignment handler, slowly. They're also undefined
  behaviour that an AltiVec-vectorizing `-O3` may exploit. Replace them with
  `getBeU32`/`memcpy`, and align `sig`.
- Compiler: the code needs `_Static_assert` (xebuild.h:44), C99 `extern
  inline` (image_read.c:915, keys.c:665) and `__builtin_bswap16`, so gcc 4.8
  or later (with `-std=gnu99` before gcc 5, whose gnu89 default makes `extern
  inline` emit no body, a link error), or clang. Xcode's gcc 4.0/4.2 on
  Tiger/Leopard is too old; use a newer gcc from MacPorts or Tigerbrew. Debian
  ports and ArchPOWER ship current gcc.
- Makefile: `macos` defaults to clang, which doesn't target PowerPC on
  10.4/10.5, and `-Wl,-map` may not exist in their linkers (Tiger links
  32-bit PowerPC with cctools ld). `linux` works as is, natively or with
  `CC=powerpc-linux-gnu-gcc`; the banner gets the triple from `-dumpmachine`.
- `char` is unsigned on PowerPC Linux (signed on Mac OS X). The scan found
  nothing that depends on it: the ini reader uses `unsigned char`, and the hex
  parsers mask with `& 0xFF`. A `-funsigned-char` x86 build confirms it
  (Tests below).
- 32/64-bit: G3/G4 userlands are ILP32; G5 and the 360 may run 64-bit (LP64)
  ones. LP64 already builds (x86-64 Linux/macOS) but has never been checked
  against the reference's output, so ppc64 would inherit any LP64 bug.
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
5. XeCrypt edits stay minimal and marked, and are offered upstream
   (cOzInABox/XeCrypt). README's "used as published" for the crypto changes
   to say so.

### Step 1: the switch, the macros and the helpers

In src/crypto/xecryptTypes.h, which every crypto file and xebuild.h (through
crypto/xecrypt.h) already include:

```c
/* 1 on a big-endian host (PowerPC).  gcc 4.6+ and clang predefine
   __BYTE_ORDER__; older gcc on PowerPC and Apple's gcc define __BIG_ENDIAN__.
   No headers: _BIG_ENDIAN and friends are defined on every host by some libcs. */
#if defined(__BYTE_ORDER__) && defined(__ORDER_BIG_ENDIAN__)
#define XECRYPT_BIG_ENDIAN (__BYTE_ORDER__ == __ORDER_BIG_ENDIAN__)
#elif defined(__BIG_ENDIAN__)
#define XECRYPT_BIG_ENDIAN 1
#else
#define XECRYPT_BIG_ENDIAN 0
#endif

/* the Xbox's big-endian key fields and bignum digits to and from host order;
   bswap16/32/64 stay the unconditional swaps */
#if XECRYPT_BIG_ENDIAN
#define XeBe32(x) (x)
#define XeBe64(x) (x)
#else
#define XeBe32(x) bswap32(x)
#define XeBe64(x) bswap64(x)
#endif
```

In xebuild.h, after the includes:

```c
#define XB_BIG_ENDIAN XECRYPT_BIG_ENDIAN
#if XB_BIG_ENDIAN && !defined(XEBUILD_FIXES)
#error "a big-endian build needs XEBUILD_FIXES (the Makefile sets it on every platform but win32)"
#endif
```

and the swap macros become:

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
```

XeCrypt: every `bswap32`/`bswap64` in xecrypt.c and xecryptBn.c except
xecrypt.c:25 becomes `XeBe32`/`XeBe64`, including the fast paths in
`XeCryptLoadQuad`/`XeCryptStoreQuad`. On little-endian the expansion is
unchanged. xecrypt.c and xecryptBn.c have no `assert`, so the edits don't
move any `__LINE__` into .rdata.

### Step 2: constants

Two constant macros in xebuild.h. Both fold at compile time:

```c
#define BSWAP16C(x) ((uint16_t)((((x) & 0xffu) << 8) | (((x) >> 8) & 0xffu)))
#define BSWAP32C(x) ((uint32_t)((((x) & 0xffu) << 24) | (((x) & 0xff00u) << 8) | \
			(((x) >> 8) & 0xff00u) | (((x) >> 24) & 0xffu)))
#if XB_BIG_ENDIAN
#define BE16C(x) ((uint16_t)(x))	/* a big-endian field's value */
#define BE32C(x) ((uint32_t)(x))
#define BYTES32(x) BSWAP32C(x)		/* the word whose bytes in memory are x's on x86 */
#else
#define BE16C(x) BSWAP16C(x)
#define BE32C(x) BSWAP32C(x)
#define BYTES32(x) (x)
#endif
```

- `buildImage`'s 28 header values are written as what they mean:
  `flashHdr.magic = BE16C(0xff4f)`, `flashHdr.kvAddr = BE32C(0x4000)`,
  `flashHdr.patchSlotSize = BE32C(0x10000)`, and so on (the table in 3).
  This also helps plans/header-fixes.md, which had to decode these values.
  The constants fold to the same numbers, so the code should be identical;
  `make check` decides. Any site where it isn't gets a per-site `#if
  XB_BIG_ENDIAN`.
- build.c:1044: `BE32C(1)`.
- The byte patterns keep their x86 spelling, tagged: `uint32_t pat2 =
  BYTES32(0x1b0000d0);	/* d0 00 00 1b */`. That's the same tokens in
  parentheses on little-endian. Byte arrays would read better, but they
  change the reference build's code, so they'd have to sit under
  `XEBUILD_FIXES` beside the originals. Leave that to de-slopification.

### Step 3: EDC and bit-fields

EDC: one macro for "a little-endian word in host order"; the two loops read
`v = ~LE32_WORD(*data++);` (the same expression as `~*data++` on
little-endian):

```c
#if XB_BIG_ENDIAN
#define LE32_WORD(x) __builtin_bswap32(x)
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
contig:1, namelen:6`). Bit-field order is implementation-defined, so a
known-answer test checks the resulting bytes (Tests).

### Step 4: rewrites under XEBUILD_FIXES

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
- Reproducible output for the tests: `GetSystemTime` (timeutil.c:304) uses
  `$SOURCE_DATE_EPOCH` in place of `time(NULL)` when it's set, the
  reproducible-builds convention. Today `xb.sysTime` is always 1, so the
  built-in default time in `makeTimestamp` is unreachable; with
  `-norandom`, this is the last source of variation.

### Step 5: build system and docs

- Makefile: on Darwin with `uname -p` = powerpc, default `CC` to `gcc`, and
  let `MAP_FLAGS` be overridden (or `MAP=0`) for old linkers. Document
  `CFLAGS=-std=gnu99` for gcc 4.8/4.9. Add `make test`, with `RUN=` for
  a cross build, e.g. `make test RUN="qemu-ppc -L /usr/powerpc-linux-gnu"`.
- CI (.github/workflows/build.yml): a `linux-ppc` job on ubuntu-latest, one
  entry for `powerpc-linux-gnu` and one for `powerpc64-linux-gnu`. It installs
  the `gcc-<triple>` cross compiler and `qemu-user` (check the package names
  on the runner image), runs `make PLATFORM=linux CC=<triple>-gcc`, then `make
  test` under qemu. A `-funsigned-char` x86 job would add nothing: the ppc
  jobs already have unsigned `char`.
- README: PowerPC rows in the platform table, the compiler requirement, and
  the XeCrypt patch. NOTES.md: a short "Byte order" section (what `SWAP*`,
  `BE16C`, `BYTES32` and `LE32_WORD` mean, and the bit-field rule), so
  de-slopification keeps them straight.

## Tests

1. `make check` after every step. Steps 1-3 must not change the reference
   build; step 4 is under `XEBUILD_FIXES`, so it can't, but run it anyway.
2. Known-answer tests (`make test`): synthetic data only, so they run in CI.
   A small driver linked with the app objects (main.c compiled a second time
   with `-Dmain=xebuildMain` for it):
   - helpers and macros: `getBe*`, `getLeU32`, `SWAP*`, `BE16C`, `BE32C`,
     `BYTES32` against expected bytes;
   - spare bytes from `setBlockSpare` and `imgAdd` for small block, big
     block controller and big block, sample LBAs and block types; the
     bit-field structs read back;
   - EDC: `calcEcd`/`pageEccOk` on fixed synthetic pages;
   - XeCrypt: standard SHA-1, HMAC-SHA1, RC4 and AES vectors; a `RotSumSha`
     vector; with a test 2048-bit key stored in Xbox format,
     `XeCryptBnQwBeSigCreate` + `XeCryptBnQwNeRsaPrvCrypt` +
     `XeCryptBnQwBeSigVerify` and `XeKeysPkcs1Verify` on stored signatures;
   - SMC: `smcChecksum`, `smcEncrypt`/`unscramble`, `calcConfigSum`/
     `smcConfigOk`, `smcPatch` on a buffer holding the three patterns;
   - dates: the 8 bytes `putFileTime` writes for a fixed DOS date (TZ=UTC);
   - an STFS entry's flags and name length.

   The expected values come from the x86 build, which matches the
   reference, generated once and committed.
3. Image comparison, local (real dumps, keys and firmware can't go in the
   repo or CI): a script runs a matrix of console types (xenon, falcon,
   jasper, jasperbb, jasperbigffs, trinity, corona, corona4g), build types
   (retail, jtag, glitch, glitch2, glitch2m, devgl), with and without a
   nanddump.bin, plus the update, extract and ini modes. Each run uses
   `-norandom`, `SOURCE_DATE_EPOCH` and `TZ=UTC`. The image, extracted files,
   ini and log (but for the banner) from ppc32 and ppc64, under qemu or on
   hardware, must match the x86-64 fixes build byte for byte. Run the matrix
   on x86-64 Linux first. Anything it finds there is an LP64 bug, which
   ppc64 shares, so fix it before the big-endian work.
4. x86 fixes build against the reference: the step 4 rewrites are small and
   covered by the known-answer tests. For more, run xeBuild.exe under
   Wine with libfaketime at the same fixed time and compare.
5. Hardware: build natively on a G4 (ppc32) and on a G5 or the 360 under
   ArchPOWER (ppc64), run a subset of the matrix, and flash one built image
   to a real console. That's the final proof that ECC, LBAs and signatures
   are right.
6. Client mode needs a console running xeBuild's dashboard-side client, so
   run it from a PowerPC host against a real console, or against a small
   Python stub that sends the "NSvr" beacon and replies to GTIN, GETF and
   so on.

## Order of work

Each step ends with `make check` and a commit:

0. Test harness: known-answer driver, `SOURCE_DATE_EPOCH`, comparison
   script. Run it on x86-64 Linux and fix what it finds.
1. Switch, swap macros, helpers, `SWAP16_BUILTIN`.
2. XeCrypt.
3. Constants: header, DVD region, patterns.
4. EDC and bit-fields.
5. `XEBUILD_FIXES` rewrites, layout asserts.
6. Makefile, CI, README, NOTES.md.
7. qemu ppc32/ppc64 comparison, then hardware.

A big-endian build is right only after step 5; steps 1-4 can't be checked
on their own beyond `make check` and the known-answer tests.

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
  `writeInitialHeader`) and a build without an SMC fails. Step 2 keeps the
  bytes; fix them separately if wanted.
- `XeCryptBnQwNeCompare` (xecryptBn.c:383) counts `u32 i` down with `i >=
  0`, so for two equal numbers it runs past index 0 and reads out of
  bounds. Only `XeCryptBnQwBeSigCreate` calls it.

## Open questions

- XeCrypt: patch the copy here (marked) and offer the changes upstream, or
  upstream first?
- Mac OS X: 10.4 or 10.5? That decides the toolchain (Tigerbrew or
  MacPorts) and whether the Makefile changes in step 5 are enough.
- The 360 under ArchPOWER: 64-bit or 32-bit userland? Both are covered,
  but it decides which qemu target matters most.
