# xeBuild rebuild

Work towards a byte-identical rebuild of `xeBuild.exe` (v1.21 build 810), so its
bugs can be fixed from source rather than by patching the binary.

Reference binary: `xeBuild.exe`, SHA256
`10DAC648197FA5CDBB82D975AB9FF11F64075C9686908DFD9A33EDC533F1971C`.

## Status

| Stage | State |
|---|---|
| Identify toolchain | Done: MSYS2 gcc 6.2.0 Rev2, binutils 2.27, mingw-w64 crt-git 5.0.0.4745 |
| Disassemble to re-assemblable GNU `as` source | Done |
| Link to a byte-identical exe | Done |
| Check ddisasm's symbolization (code can move safely) | Done: audit + shift test, see below |
| Split into the original object files | **Done: 102 files (66 program + runtime), `sh build.sh` reproduces the SHA256** |
| Move functions to C | **Started: all 41 XeCrypt files (crypto + BigDigits) build from their original C source** |
| Fix bugs | Next |

## What the binary is

- 32-bit PE, linked November 2019, stripped, built at `-O3` (`main` is in
  `.text.startup`; XeCrypt's Makefile and the app's timeutil both need -O3). 104 objects compiled by
  `GCC: (Rev2, Built by MSYS2 project) 6.2.0` (one `GCC:` ident each), DWARF-2
  exception handling. Linked with the default libraries plus `-lws2_32`.
- The program is 66 objects with code: 25 application files, 15 crypto files
  and 26 files of BigDigits (David Ireland's bignum library, as extended by Dang
  Nguyen Duc), which leaked its
  build path through `assert()`
  (`H:/x360sdk/__NAND/nandbuild_trin/XeCrypt/bign/mpAdd.c` etc.).

## Layout

```
xeBuild.exe              reference binary (do not modify)
build.sh                 compile/assemble src/ + link + stamp + verify -> build/xeBuild.exe
src/objects.txt          link order
src/link.ld              link script (default i386pe order for the sections used)
src/app/                 the application (25 files)
src/crypto/              XeCrypt, all C, laid out as its source tree: the XeCrypt
                         API, aes/ (Gladman), rc4/ sha/ (OpenSSL), md5/, des/, and
                         bign/ (BigDigits bignum library + PKCS#1 RSA, hash,
                         base64), with its licence files
                         its licence files
src/runtime/             crt2, crtbegin/crtend, mingw/libgcc objects, import stubs,
                         .idata/.CRT/.tls/.rsrc, ctor/dtor lists
src/common_bss.s         COMMON (uninitialized global) block
re/ddfix.py              ddisasm output -> build/xeBuild.s + .lines.json (see below)
re/split.py              build/xeBuild.lines.json -> src/ (object boundaries, names)
re/units.py              objects from .eh_frame CIEs; profile of each for naming
re/objcmp.py             section-by-section compare of a .o against the exe
re/execmp.py             header/section/byte compare of two exes
re/stamp.py              set PE timestamp and recompute checksum
re/audit.py              symbolization audit against IDA's pointer analysis
re/shifttest.py          relink with everything moved, check every pointer followed
re/single.ld             link script for the single-file build/xeBuild.s (shift test)
re/ida_dump.py           IDA export of instructions/address fields/imports (JSON)
re/ida_export_asm.py     IDA's own MASM-style listing (reference only)
re/mapparse.py           GNU ld -Map parser
re/runtime_syms.json     names of mingw runtime functions found in the exe
tools/fetch_toolchain.sh download + verify + unpack the 2016 MSYS2 toolchain
tools/packages.sha256    hashes of those packages
tools/ddisasm/           user-local ddisasm install for WSL, and the disassembly step
build/                   generated, ignored
```

## Setup

Toolchain (Git Bash, repo root). Downloads ~55 MB from the MIT Kodi mirror of
old MSYS2 packages and unpacks to `tools/toolchain-4745/`:

```bash
sh tools/fetch_toolchain.sh
```

ddisasm (WSL Ubuntu; no root needed, installs to `~/ddisasm-root`):

```bash
wsl -d Ubuntu -- bash tools/ddisasm/install.sh
```

## Building

```bash
sh build.sh
```

Builds every object in `src/objects.txt`: `src/<obj>.c` with gcc 6.2.0 if it
exists (flags and original `__FILE__` path per directory in `build.sh`), otherwise
`src/<obj>.s` with binutils 2.27. Links them with
`ld -T src/link.ld --no-insert-timestamp -s`, writes the original link time
(`0x5DCAB029`) and recomputes the PE checksum (`re/stamp.py`; ld 2.27 can't
take a fixed timestamp), then compares against `xeBuild.exe` and prints the SHA256.

## Regenerating `src/`

```bash
wsl -d Ubuntu -- bash tools/ddisasm/disasm.sh xeBuild.exe build
python re/ddfix.py xeBuild.exe build/xeBuild.dbg.s build/xeBuild.s
python re/split.py xeBuild.exe build/xeBuild.lines.json src
sh build.sh
```

Hand-written sources began with XeCrypt's C files (October 2026). `split.py`
still writes every `.s`, overwriting those, but skips any object that has a `.c`.
So the `.c` files are maintained by hand. The functions they share with `.s`
files are named in `split.py`'s `SYMBOLS` (`_mpAdd`, `_XeCryptSha`, `__assert`,
`_memset`, ...; data too, e.g. the COMMON `_XeCryptRandomState`). Where
references alone would put data in the wrong object, `DATA_OWNERS` assigns it
(the AES tables, defined in aestab.c but used only by aescrypt/aeskey).
Every `SYMBOLS` name is `.globl` where the `.s` defines it, so a C object can
use it even if no other `.s` does; that includes import stubs, libgcc's
64-bit division, and IAT slots that dllimport declarations reference
(`__imp___errno`). `END_POINTERS` rewrites one-past-the-end pointers that
ddisasm symbolized as the following label (console_hdd's `L_45c644+16` had
pulled log's strings into console_hdd).

Application files in C (all **-O3**; timeutil doesn't match at -O2):

- `app/crc32.c`: Gary S. Brown's CRC-32 table and an `UPDC32` loop.
- `app/log.c`: verbosity, `build.log`, renaming it to `<name>.log`. The
  verbose-flag switch needs the `'\0'` case written as a separate copy of the
  level-1 body (gcc merges the copies, but block order follows them).
- `app/timeutil.c`: Wine's ntdll/kernel32 time code (`RtlTimeFieldsToTime`,
  `RtlTimeToTimeFields`, `SystemTimeToFileTime`, `FileTimeToSystemTime`,
  `FileTimeToDosDateTime`, `DosDateTimeToFileTime`, `GetSystemTime`) as cdecl
  functions with own WORD-based types, `errno = EINVAL` for SetLastError, and
  `time()`/`rand()` for the clock (GetSystemTime fills milliseconds with
  `rand() % 999`). FileTimeToDosDateTime rounds up to whole, then even, seconds.
  The names are Wine's; a file that also includes `windows.h` would clash.

From Git Bash, set `MSYS_NO_PATHCONV=1` before calling `wsl` with paths.

`disasm.sh` runs ddisasm 1.9.5 and prints with
`gtirb-pprinter --format raw --syntax intel --keep-all --listing-mode debug`:
PE output only supports MASM syntax, and the debug listing tags every line
with its original address.

`ddfix.py` strips those addresses, assembles with binutils 2.27 and, wherever
gas emits different bytes than the exe, pins the original encoding (`.byte`,
or opcode + `.long label-.-4` for branches so targets stay symbolic). Currently
528 lines are pinned: 7-byte padding `lea`s gas would shorten, near jumps it
would relax, and 2-byte `66 90` padding that ddisasm prints as two `nop`s.

Next it symbolizes what ddisasm left as numbers (943 fields, output unchanged):
`.idata` descriptor/thunk RVAs and the `.rsrc` data entry RVA become `.rva
label`, the 685 `.eh_frame` FDE pc_begin fields (pcrel sdata4) become
`.long label - .`, the `.CRT`/`.tls` TLS callback pointer becomes `.long
label`, and 3 mingw pseudo-reloc operands become `.L_464900_END+N`. Imports get
labels on their IAT slots, plus `__IAT_start__`/`__IAT_end__`/`__tls_used`
(ld fills the IAT and TLS data directories from them).

It writes `build/xeBuild.lines.json` (every line with its original address) and
a single-file `build/xeBuild.s` that links with `re/single.ld` (used by the
shift test; it needs `$zz` tail sections to get the section sizes right, which
the per-object build gets naturally).

### How the objects were recovered (`re/split.py`)

- **.text and .eh_frame, exact.** Every gcc object contributes one CIE plus
  its FDEs to `.eh_frame`, in link order, so the 94 CIEs give the objects and
  their functions. Objects without unwind info were matched byte for byte
  against the toolchain's libraries (`_chkstk_ms`, import stubs).
  `.text.startup` holds `main` (app/main), a startup function of app/options
  and crtend's constructor; the default link script's ctor/dtor lists follow.
- **.data, .rdata, .bss, inferred.** Each is split at 4-aligned labels (gas
  pads sections to 4, so objects start 4-aligned). Each atom gets the set of
  objects whose code references it, propagated through data-to-data
  pointers, and monotone boundaries in link order are chosen to minimise atoms
  placed outside a referencing object: 20 of ~1500 atoms end up there (shared
  globals). Padding stays with the object before it.
- **Fixed pieces.** `.jcr` (end of `.data`) and the eh_frame terminator are
  crtend's. The 104 `GCC:` idents (`.rdata$zzz`) go one per gcc object; the
  10 belonging to objects without code (data-only runtime objects, and likely
  one data-only program file whose data is merged into its neighbours) are in
  `runtime/no_code_objects.s`. `.idata`, `.CRT`/`.tls` and `.rsrc` are whole
  files. The COMMON block at the end of `.bss` stays one file: ld lays COMMON
  symbols out in hash-table order, so it can't be attributed to sources.
- Labels referenced from another file are `.globl`; `__ImageBase` comes from
  the link script.

### Source files

Names are inferred from content; each file's header repeats the evidence and
its original addresses. Library files use the library's own file names.

| File | Evidence |
|---|---|
| app/main | `main`, signal handlers, mode dispatch |
| app/mode_build, mode_update, mode_client, mode_extract, mode_ini | each prints its mode's usage text |
| app/build | image build: inputs with crc32 checks, patches, payloads |
| app/image_read / image_write | parse an existing NAND image / lay out and write one |
| app/bootloaders | CB/CF/CD/CE decryption, pairing, bootloader signatures |
| app/keys | CPU/1BL keys, SMC/keyvault/CRL input decryption |
| app/keyvault | keyvault hash, DVD key |
| app/smc | SMC checksum, type detection, patches |
| app/sysupdate, stfs | system update container, container/manifest hashes |
| app/options | console types, command line options |
| app/filelist_ini | file list ini parser |
| app/consoleinfo, console_hdd, net | console info/options ini, HDD transfer, winsock |
| app/log, fileutil, timeutil, crc32, xboxrom | logging, file helpers, dates, crc32, ROM names |
| crypto/xecrypt, xecryptBn | XeCrypt API and big-endian bignum helpers (C source) |
| crypto/aes/aes_modes, aestab, aescrypt, aeskey | Brian Gladman's AES (C source) |
| crypto/rc4/rc4_enc, rc4_skey, sha/sha1dgst, md5/md5 | OpenSSL RC4 (`"rc4(idx,int)"`), SHA-1; MD5 (C source) |
| crypto/des/des, bign/pkcs1-rsa, hash, base64, common | DES/3DES, RSA keygen/OAEP/PSS, hash wrappers, base64 (C source) |
| crypto/bign/mp*, sp*, bigdUtils | BigDigits functions (mpAdd, mpModExp, spMultiply, ...) (C source) |

### XeCrypt in C

All 41 crypto objects are XeCrypt, copied unmodified (LF line endings) from
[cOzInABox/XeCrypt](https://github.com/cOzInABox/XeCrypt) at commit `7d619af`
into `src/crypto/`, which mirrors that repo's tree (its headers include
`"bign/bigdigits.h"`, `"../sha/sha.h"` and so on). Only the files the program
links, and the headers they include, are copied. The whole library was built
at **-O3** (its Makefile's `-s -O3`; -O2 gives different code for 12 of the 15
crypto files outside BigDigits), and each file compiles to the reference object.
`src/crypto/LICENSE-XeCrypt.txt` is that repo's licence: MIT, plus the notices
of the projects it includes (Gladman AES, Eric Young's RC4/SHA, MD5, DES,
BigDigits). The BigDigits section says the 1.0 extension was released into
the public domain with Ireland's permission. `bign/bigdigitsCopyright.txt` is
the original 1.0 notice.

Library objects use XeCrypt's file names: the objects first named
crypto/xecrypt_bn, rsa, memwipe and md5_dgst are xecryptBn.c,
bign/pkcs1-rsa.c, bign/common.c and md5/md5.c. aestab.c defines the AES
tables, which the inferred data split had placed in aescrypt/aeskey (see
`DATA_OWNERS` in `split.py`). xecrypt.c's `XeCryptRandomState` is a tentative
definition, so it stays in the COMMON block (`common_bss.s` names it).

#### BigDigits

XeCrypt's `bign/` is Dang Nguyen Duc's extension of David Ireland's BigDigits
**version 1.0** (2001, one function per file). Only -O3's loop-to-`memset`
distribution reproduces mpSetZero, mpSetDigit and mpDivide.

The header matters: mpModExp only matches with its `const` prototypes.
Compared with upstream 1.0, the edits include `MAX_DIG_LEN` 64, no wiping of
temporaries, `assert`s in mpAdd/mpSubtract/mpMultiply and shifts of any size.
Upstream 1.0 can be found as `di-mgt.com.au/src/BigDigits.zip` on the Wayback
Machine.

mpIsPrime.c holds `mpIsPrime` (full test, unused), `mpIsPrimeShort` (trial
division only; bign/pkcs1-rsa calls it) and `mpIsPrimeRabin`. The 15-byte gap
before `mpIsPrimeRabin` is gas alignment padding: a short `jmp` over nops,
which the disassembly showed as a call.

`build.sh` feeds each file through stdin behind
`#line 1 "H:/x360sdk/__NAND/nandbuild_trin/XeCrypt/<path>.c"` so that `__FILE__`
matches (only bign's `assert`s use it).

`bigdUtils.c` (alloc/free, printing, random fill, string conversion) is
the object formerly called mpUtil. gcc turns its `malloc` + `memset(0)` into
`calloc`, as in the original.

Licence note: BigDigits 1.0's own notice asks that the attribution text in
`bigdigitsCopyright.txt` stay in distributed executables. `xeBuild.exe`
doesn't contain it, so builds distributed after bug fixes should add it.

## Symbolization checks

Two independent checks that code and data can move without breaking pointers:

```bash
python re/audit.py xeBuild.exe build/xeBuild.dbg.s build/ida_dump.json build/audit.txt
python re/shifttest.py xeBuild.exe build/xeBuild.s build
```

`build/ida_dump.json` comes from `python re/ida_dump.py build/ida/xeBuild.exe
build/ida_dump.json` (IDA 9.x, on a copy of the exe).

**audit.py** compares the source with IDA's pointer analysis (operands it
treats as addresses, data it marks as offsets, in-image dwords). Current result:

| Category | Count | Verdict |
|---|---|---|
| missed (IDA: address, source: number) | 1 | IDA false positive: string `"CBB"` at 0x459f25 |
| maybe (unmarked in-image data dwords) | 18 | strings and bit-mask tables (0x400000, 0x410000, ...) |
| false (symbol where IDA sees a constant) | 0 | |
| imagebase (`__ImageBase` as a number) | 62 | PE header reads, plus 0x400000 used as a bit mask; fine while the base stays 0x400000 |
| cross-section `sym+off` | 0 | |
| cross-label `sym+off` | 67 | struct fields addressed from a neighbouring label (`L_47a0d4+4`); fine unless data is reordered |

**shifttest.py** relinks with 16 bytes inserted before every function and every
data label, then checks every address-like word of the original against the
moved build: 7848 absolute pointers, 255 RVAs and 685 eh_frame pcrel pointers
follow their targets. What remains is noise (strings, bit masks, import-name
text, resource directory counts) and the 67 cross-label fields above, which the
per-label padding deliberately pulls apart. The moved exe also runs: its output
without arguments is identical to the original's.

Remaining caveats when editing:
- `.eh_frame` pc_range and CFA programs are still raw: a function whose size or
  stack layout changes needs its FDE regenerated (C rewrites get this from gcc).
- Keep the image base at 0x400000 (see the imagebase row).
- Don't insert data between the labels of the 67 cross-label fields.
- Function alignment is explicit padding; ddisasm's `.align`s are dropped in
  the split files, so code inserted mid-file shifts the functions after it
  (harmless, but they lose 16-byte alignment).
