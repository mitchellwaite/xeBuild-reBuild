# xeBuild rebuild

A C source rebuild of `xeBuild.exe` (v1.21 build 810) that compiles back to
the exact same bytes as the released binary. With matching source, xeBuild's
bugs can be fixed in C instead of by patching the executable.

The reference binary is `xeBuild.exe` in this folder, SHA256
`10DAC648197FA5CDBB82D975AB9FF11F64075C9686908DFD9A33EDC533F1971C`.

## Status

- [x] Produce xeBuild from C
- [ ] De-slopification of the decompiled source
- [ ] Fix bugs

The rebuild is complete: all of the program's code is C, and the build
reproduces the original exe byte for byte. The decompiled C still reads like
compiler-matching output, so we're doing de-slopification next: turning it
into readable source while it keeps building to the same bytes. Bug fixes
come after that.

- **Application:** 25 source files (432 functions), rebuilt by hand from the
  binary.
- **Crypto:** 41 source files (185 functions) from XeCrypt, its crypto
  library, used as published.
- **Runtime:** the MinGW startup code, libraries and import tables come from
  the toolchain itself, linked the way gcc links any program.

## How it was done

1. **Found the original toolchain.** The binary was built with MSYS2's
   gcc 6.2.0 and binutils 2.27 (2016) at `-O3`. The same packages are fetched
   from an archive mirror, because newer versions produce different code.
2. **Disassembled it** with ddisasm into assembly that rebuilds to the same
   exe.
3. **Split it into the original source files.** The exception-handling
   tables mark where each of the original objects starts and ends.
4. **Rewrote each file in C** one function at a time, until gcc's output
   matched the original exactly.

[NOTES.md](NOTES.md) has the details: how the binary was taken apart, the
tricks some functions needed to match, and the checks behind each step.

## Compiler tricks by component

The application files match, but many only match because of hints that steer
gcc and that the original source almost certainly didn't contain. This list
ranks the 25 files from easiest to hardest to match with source shape alone:
ordinary C, the same `-O3` as the rest, and none of these hints.

The ranking is an estimate from reading the source and the matching notes. No
hint-free version has been tried. Trick count isn't the only factor: a single
hint can be harder to replace than several others if it sets something like
register ties or bb-reorder's heap order.

**How tricks are counted:** one for each non-default gcc option in `build.sh`,
and one for each use of a hint in the source (macro uses count individually).
These are the hints:

- **Branch hints:** `__builtin_expect`, hot and cold labels, and calls to
  guarded hint functions
- **Dead code:** `__builtin_constant_p` feeds, `__builtin_unreachable`, and
  dead tests and blocks
- **Empty `asm`:** register pins, literal ordering, `asm goto` edges and
  barriers
- **Attributes:** per-function `optimize(...)`, inlining and cloning control,
  and others
- **Declarations:** asm-label prototypes and per-file views of `xb.files`

Writing a function success-first, duplicating a block, inlining a helper by
hand and spelling a byte swap differently are source shape, so they aren't
counted. Neither are plain type casts.

<details>
<summary><b>1. crc32</b>: 0 tricks, done</summary>

Gary S. Brown's table and `UPDC32` loop, compiled as written.

</details>

<details>
<summary><b>2. mode_extract</b>: 0 tricks, done</summary>

Usage text, loading a NAND dump and listing its files, in plain C.

</details>

<details>
<summary><b>3. smc</b>: 0 tricks, done</summary>

Plain C.

</details>

<details>
<summary><b>4. log</b>: 0 tricks, done</summary>

Needs no hints. One shape detail: the verbose-flag switch writes the `'\0'`
case as its own copy of the level-1 body, which sets the block order.

</details>

<details>
<summary><b>5. xboxrom</b>: 0 tricks, done</summary>

Its only oddities are four casts to `xecrypt.h`'s types, marked
`TODO(prototype cast)`.

</details>

<details>
<summary><b>6. timeutil</b>: 0 tricks, done</summary>

Wine's time conversion code, compiled as written.

</details>

<details>
<summary><b>7. main</b>: 0 tricks, done</summary>

Needs no hints. One loop sets 13 `xb` fields as an array, marked
`TODO(xebuild.h cast)`.

</details>

<details>
<summary><b>8. mode_build</b>: 1 trick, easy</summary>

- 1 declaration: `XB_PATCHES`, a union view of `xb.files`

This probably reflects how the original declared the struct, so settling the
shared header should remove it, as long as the other files that need a
different view still match.

</details>

<details>
<summary><b>9. sysupdate</b>: 1 trick, easy</summary>

- 1 asm-label prototype: `FileExistsU32`, which reads `FileExists` as `uint32_t`

`stfs` needs the `int` version. A separate declaration in each file should
replace the alias, for example a plain local prototype.

</details>

<details>
<summary><b>10. stfs</b>: 2 tricks, easy</summary>

- 1 `__builtin_expect` and 1 register pin (`fb` in `esi`), both on the loop guard
  in `stfsGetFile`

This is one register choice in one function, so it should be a matter of trying
local variable and loop shapes.

</details>

<details>
<summary><b>11. mode_ini</b>: 3 tricks, easy</summary>

- 2 pins on `&data` and `&len` in `iniWriteFlashfs`
- 1 asm-label prototype: `suFirstFileU32`

The file is small, and the pins probably stand in for the original's local
variables.

</details>

<details>
<summary><b>12. keyvault</b>: 3 tricks, easy</summary>

- `--param builtin-expect-probability=55`
- 1 `__builtin_expect` and 1 cold label, both in `kvCheckHash`

The weak hint range (51-60 match) suggests the original got a similar small
bias from its branch shape.

</details>

<details>
<summary><b>13. consoleinfo</b>: 3 tricks, moderate</summary>

- `--param align-threshold=200`, because `showInfoKeys` aligns a block at
  frequency 61 of 9412
- 1 `__builtin_unreachable`, which shifts dom2's block numbers and so sets
  which copy gets duplicated first
- 1 asm-label prototype: `log_printfInt`

There are few tricks, but the alignment means finding a shape that gives that
block the right estimated frequency.

</details>

<details>
<summary><b>14. fileutil</b>: 7 tricks, moderate</summary>

- `--param builtin-expect-probability=65`
- All in `readFileIn`: 2 `__builtin_expect`, 1 register pin on three variables
  (`edi`, `ebx`, `esi`), 1 guarded `rf_hint()` call, and `optimize("no-early-inlining")`
- 1 dead test: the `'X'` comparison in `myatou32`, which can never match but
  changes the branch estimate

Only one function is really at stake, but that function took a long search. The
`myatou32` test may well be in the original, so it may not need replacing.

</details>

<details>
<summary><b>15. console_hdd</b>: 9 tricks, moderate</summary>

- `--param builtin-expect-probability=80` and `--param align-loop-iterations=3`
- 2 `__builtin_expect`, 1 literal-order `asm` and 1 pin, in `prepSysex` and
  `sendAvatarData`
- `__builtin_assume_aligned`, which hides the loop index from scev so ivopts
  keeps the `imul`
- `__builtin_prefetch(0)`, which keeps `sendDir`'s `fail:` as its own GIMPLE block
- 1 asm-label prototype: `netMountInt`

`sendAvatarData` is the difficult part: its loop form has to defeat ivopts and
if-conversion without any hints.

</details>

<details>
<summary><b>16. net</b>: 9 tricks, moderate</summary>

- `--param builtin-expect-probability=65`
- 4 per-function `optimize` attributes: `no-crossjumping` on three functions
  and `no-early-inlining` on two (`netWriteBlocks` has both)
- 2 `__builtin_expect`, on `netRecvVerbose` and `netSendFile`
- 2 pins, on `got` and `buf`

Each function needs only a small fix. The exception is `netRecvVerbose`, whose
IPA-CP clone (`netRecv`) and register choice both depend on its hints. Blocking
crossjumping without the attribute takes differences between the blocks.

</details>

<details>
<summary><b>17. bootloaders</b>: 11 tricks, moderate</summary>

- 5 `optimize` attributes: `no-tree-dominator-opts`, `no-tree-vrp`,
  `no-cse-follow-jumps` and `no-early-inlining`, on `cfDecrypt`, `cbDecrypt`,
  `cdDecrypt`, `ceDecrypt` and `daeVerifySig`
- 3 inlining and cloning attributes: `noclone` on `daeDecrypt`, `always_inline`
  on `daeSigCheck` and `fcrtVerifySig`
- 1 guarded `hint()` call, 1 literal-order `asm` and 1 register pin

The disabled passes suggest the original kept a value alive differently, such
as `ok` or `buf` on a failure path. Finding that shape would likely fix all
three `*Decrypt` functions at once.

</details>

<details>
<summary><b>18. mode_update</b>: 22 tricks, hard</summary>

- `-fno-toplevel-reorder` and `--param builtin-expect-probability=68`
- Dead layout hints in `mode_update` and `updateNand`: 9 `__builtin_constant_p`,
  2 `asm goto`, 1 `__builtin_unreachable`, 1 `if (0)` dummy block, 1 dead
  `__builtin_memset`, 1 pin and 1 hot label
- 2 `__builtin_expect`, on `getConsoleFiles` and `updateNand`
- 1 asm-label prototype (`verifyExtendedU32`) and `XB_PATCHES`

Without the dead hints, the only difference was cold-block order in the last
bb-reorder round, with no register changes, so the target is narrow. It is still
a Fibonacci-heap tie, which needs the exact frequencies. The natural-source
approach that helped `options` hasn't been tried here.

</details>

<details>
<summary><b>19. image_write</b>: 21 tricks, hard</summary>

- `--param builtin-expect-probability=50`
- 9 dead tests in `imgAdd` and `imgAddFile`, which VRP1 removes
- 5 register and slot pins, across `buildImage`, `imgAdd`, `imgAddFile` and
  `finalizeImage`
- 2 `__builtin_expect`, 2 hot and cold labels, and
  `optimize("no-tree-scev-cprop")` on `writeFsTable`
- 1 asm-label prototype: `xmalloc`, which stops CCP assuming `malloc`'s alignment

The dead tests set `imgAdd`'s IPA-CP value and which SSA names get recycled.
Those decide three clones and the compare operand order throughout, so a
hint-free source would have to land on the same numbers. The layout was found by
search.

</details>

<details>
<summary><b>20. keys</b>: 25 tricks, hard</summary>

- `-fno-toplevel-reorder` and `--param builtin-expect-probability=60`
- 12 `__builtin_expect` and 4 hot and cold labels, mostly in `kvPrepare` and
  `daeEncrypt`, which set trace order and LRA's spill-slot order
- 2 `pure` redeclarations (`getBeU32`, `verifyFcrt`), which only this file can use
- `optimize("no-tree-forwprop", "no-tree-reassoc")` on `smcChecksum`
- 2 `always_inline` and 2 pins (`off` in `daeEncrypt`)

The hints are spread over several functions, and `kvPrepare` depends on several
of them together. The `smcChecksum` attribute exists because its standalone copy
must differ from the inlined one, which is hard to get from one source.

</details>

<details>
<summary><b>21. filelist_ini</b>: 27 tricks, hard</summary>

- 4 options: `-fno-toplevel-reorder`, `-fno-tree-loop-vectorize`,
  `--param builtin-expect-probability=65` and
  `--param lra-inheritance-ebb-probability-cutoff=60`
- 13 dead tests (`< -1` and `< 0` stores, a `strlen` block), whose freed SSA
  names set compare order and pseudo numbers
- 3 literal-order `asm`, 3 pins and 1 `__builtin_unreachable` in `findKey`
- 1 `__builtin_expect`, `optimize("ira-region=one")` and `XB_FILES_BOUND`

The SSA-numbering hints are the problem. Their effects are indirect, and each
source change disturbs the rest. Vectorization and LRA's cutoff are global
options with no direct source equivalent.

</details>

<details>
<summary><b>22. image_read</b>: 35 tricks, hard</summary>

- `-fno-toplevel-reorder`
- 10 register pins across `checkBlock`, `detectController`, `fsGetFile` and others
- 5 `__builtin_expect`, 5 hot labels, 4 `__builtin_unreachable` and 3 empty `asm`
  barriers
- 2 `optimize` attributes (`no-if-conversion` and related), on `getImageSmc` and
  `copyMmcImage`
- 2 literal-order `asm`, 1 `volatile` cast (`b[513]` loaded twice), `noinline`
  and 1 asm-label prototype

There's no single hard knot like the other hard files, but many functions each
need their own solution. The pins fix register allocation, which is the hardest
thing to get from shape alone.

</details>

<details>
<summary><b>23. build</b>: 63 tricks, very hard</summary>

- `-fno-toplevel-reorder` and `--param builtin-expect-probability=98`
- 22 `__builtin_expect`, 10 pins, 6 hot and cold labels and 5 `cb_hint()` calls,
  across `loadFileCrc`, `extractSmcConfig`, `patchSmcConfig`, `loadBl` and others
- 2 `__builtin_constant_p`: a dead entry in `loadBl`'s `checkBl` copy that lives
  until dom2
- 3 `no-early-inlining` attributes, 4 inlining and cloning attributes, and 2
  `__builtin_assume_aligned`
- 4 asm-label prototypes, `XB_FILES_BOUND`, 1 literal-order `asm` and 1 barrier

It's the largest file at 2,843 lines. The expect probability has to sit in a
narrow, unusually high range (92-99), and the dom2 entry is there to keep one
frequency from scaling to 0. The file is also long enough that the source was
only ever fitted function by function.

</details>

<details>
<summary><b>24. options</b>: 80 tricks, very hard</summary>

- 3 options: `--param builtin-expect-probability=83`, `-fno-ipa-profile` and
  `-fno-reorder-functions`
- 32 `__builtin_constant_p`, 17 `__builtin_expect`, 3 `asm goto`, 3
  `__builtin_unreachable` and 3 dead blocks, nearly all setting the cold layout
  of `applyIniOptions` (three dummy heap entries among them)
- 2 `po_hint()` calls and 2 `no-early-inlining` attributes, for `parseOption`
- `_parseButton.part.0`, written by hand as a global `cold` function in
  `.text.startup` rather than coming from gcc's own function split
- 3 asm-label prototypes, `XB_PATCHES`, 3 hot and cold labels, 3 pins, 1
  literal-order `asm`, 1 barrier and `always_inline`

The main clue that this can work is that natural source (`optIniBool` inlined,
plain calls) already gives the whole hot layout. The cold layout is the unsolved
part, and it's a heap-tie problem across a very long function. A hint-free
source would also have to split `parseButton` the way gcc did.

</details>

<details>
<summary><b>25. mode_client</b>: 250 tricks, very hard</summary>

- 4 options: `-fno-toplevel-reorder`, `-fno-ipa-profile`,
  `-fno-reorder-functions` and `--param builtin-expect-probability=50`
- 159 `__builtin_constant_p` feeds and 31 `asm goto` edges to dead labels, which
  set bb-reorder's heap keys
- 18 pins, including ones that only raise LRA's `edi` usage
- 10 hot and cold labels, 6 expects, 6 empty-struct scopes, 4 dummy blocks and
  feeds, and 3 `__builtin_unreachable`
- 3 asm-label prototypes (`net.c`'s block numbers as `uint32_t`), 3 data
  attributes for `.bss` and `.rdata` padding, 2 literal-order `asm` and 1 barrier

The source was fitted to a simulated heap by search, over more than 130
attempts, and is nowhere near readable. `clientEraseBlock` is even inlined by
hand so its labels can be reached. `mode_client` itself is one long option loop
and switch, so nearly every change moves the rest of the layout. Rewriting it
from scratch is probably the only way to find the natural shape.

</details>

`src/globals.c` isn't ranked because it holds only data: it uses `-fno-common`,
`-fno-toplevel-reorder`, `aligned(4)` and padding arrays to put the COMMON block
in address order, because the original's order came from a linker hash table.

## Repository layout

| Path | Contents |
|---|---|
| `xeBuild.exe` | the reference binary (never modified) |
| `src/` | the application's C source and headers |
| `src/crypto/` | XeCrypt (AES, RC4, SHA-1, MD5, DES, RSA/BigDigits) |
| `src/globals.c` | the program's uninitialized globals |
| `build.sh` | builds everything and checks the result |
| `tools/re/` | reverse-engineering and verification scripts |
| `tools/` | the toolchain's packages and setup, and ddisasm setup |
| `tools/wip/` | experiments and notes from the matching work |

## Building

You need Windows with Git Bash and Python. First unpack the pinned
toolchain, whose packages are in `tools/packages/` (to `tools/toolchain-4745/`;
it also rebuilds two import libraries from the mingw-w64 sources in
`tools/mingw-w64/`):

```bash
sh tools/fetch_toolchain.sh
```

Then build:

```bash
sh build.sh
```

This writes `build/xeBuild.exe`, compares it with the reference and prints
its SHA256, which should match the one above. Re-disassembling the binary
also needs ddisasm under WSL; NOTES.md covers that.

## Credits and licences

- XeCrypt ([cOzInABox/XeCrypt](https://github.com/cOzInABox/XeCrypt)) is MIT
  licensed and includes code from Brian Gladman (AES), Eric Young (RC4,
  SHA-1), MD5, DES, and David Ireland's BigDigits as extended by Dang Nguyen
  Duc. Its licence files are in `src/crypto/`.
- BigDigits 1.0 asks that its attribution text
  (`src/crypto/bign/bigdigitsCopyright.txt`) be kept in distributed
  executables. The original `xeBuild.exe` doesn't include it, so builds
  distributed with bug fixes should add it.
- `src/timeutil.c` is based on Wine's time conversion code, and
  `src/crc32.c` on Gary S. Brown's CRC-32.
