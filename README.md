# xeBuild rebuild

Work towards a byte-identical rebuild of `xeBuild.exe` (v1.21 build 810), so its
bugs can be fixed from source rather than by patching the binary.

Reference binary: `xeBuild.exe`, SHA256
`10DAC648197FA5CDBB82D975AB9FF11F64075C9686908DFD9A33EDC533F1971C`.

## Status

| Stage | State |
|---|---|
| Identify toolchain | Done: MSYS2 gcc 6.2.0 Rev2, binutils 2.27, mingw-w64 crt-git 5.0.0.4745 |
| Disassemble to re-assemblable GNU `as` source | Done: `src/xeBuild.s` |
| Assembled object matches exe (outside relocated fields) | Done: every section, 0 differing bytes |
| Link to a byte-identical exe | **Done: `sh build.sh` reproduces the SHA256** |
| Check ddisasm's symbolization (code can move safely) | Next |
| Split into the original 66 source files | Later |
| Move functions to C, fix bugs | Later |

## What the binary is

- 32-bit PE, linked November 2019, stripped. About 104 objects built with
  `GCC: (Rev2, Built by MSYS2 project) 6.2.0`, DWARF-2 exception handling.
- Layout: crt2 `0x401000-0x401500`, crtbegin `0x401500-0x401630`, program code
  `0x401630-0x446b30` (66 objects), mingw runtime `0x446b30-0x449030`, msvcrt
  import thunks, then `.text.startup` (`main` at `0x4492c0`, so built at `-O2` or higher).
- Data: `.data 0x44a008-0x44b6a4`, `.rdata 0x44c064-0x463284`,
  `.bss 0x46f034-0x479ac8`, uninitialized globals `0x479e84-0x50ec88`.
- Links against the default libraries plus `-lws2_32`.
- Leaked source paths show XeCrypt bignum code compiled in
  (`H:/x360sdk/__NAND/nandbuild_trin/XeCrypt/bign/mp*.c`).

## Layout

```
xeBuild.exe              reference binary (do not modify)
build.sh                 assemble + link + stamp + verify -> build/xeBuild.exe
src/xeBuild.s            generated GNU-as source for the whole image
src/xeBuild.ld           linker script placing each section at its original address
re/ddfix.py              ddisasm output -> src/xeBuild.s (see below)
re/objcmp.py             section-by-section compare of a .o against the exe
re/execmp.py             header/section/byte compare of two exes
re/stamp.py              set PE timestamp and recompute checksum
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

Assembles `src/xeBuild.s` with binutils 2.27, links it with `ld -T src/xeBuild.ld
--no-insert-timestamp -s`, writes the original link time (`0x5DCAB029`) and
recomputes the PE checksum (`re/stamp.py`; ld 2.27 can't take a fixed
timestamp), then compares against `xeBuild.exe` and prints the SHA256.

## Regenerating `src/xeBuild.s`

```bash
wsl -d Ubuntu -- bash tools/ddisasm/disasm.sh xeBuild.exe build
python re/ddfix.py xeBuild.exe build/xeBuild.dbg.s src/xeBuild.s
sh build.sh
```

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

`ddfix.py` then prepares the single object for linking:
- imports become labels on their IAT slots (ddisasm leaves them undefined), and
  `__IAT_start__`/`__IAT_end__`/`__tls_used` let ld fill the IAT and TLS data
  directories; the import and resource directories come from the `.idata` and
  `.rsrc` sections as a whole, as in the original;
- sections get the exe's flags and alignment (`.eh_fram` is the truncated
  `.eh_frame`);
- gas pads a section's size up to its alignment, but the exe's `.text`, `.data`
  and `.bss` end on 4-byte boundaries, so their last bytes move to a 4-aligned
  `$zz` continuation (`.text$zz` is code+data, matching the original's ctor/dtor
  list words; the `.bss` tail is a COMMON block).

## Known gaps

The rebuild is exact, but every pointer ddisasm failed to symbolize is still a
hard-coded number, which only works while nothing moves. One is known: the TLS
callback pointer at `.CRT` 0x510020 (-> 0x446e60) is printed as the string
`` "`nD" ``. Before editing code, audit for more (e.g. relink with sections
shifted and diff).
