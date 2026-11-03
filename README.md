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

The application files match, but some only match because of hints that steer
gcc and that the original source almost certainly didn't contain. This list
ranks the 11 files that still have them from easiest to hardest to match with
source shape alone: ordinary C, the same `-O3` as the rest, and none of these
hints. The other 14 application files build with no tricks.

Every hint in these files has been tried on its own, and `tools/wip/hintsearch.py`
removes any that no longer change the code, but past `stfs` no hint-free source
has been attempted, so the ranking there is an estimate. Trick count isn't the
only factor: a single hint can be harder to replace than several others if it sets
something like register ties or bb-reorder's heap order.

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

`console_hdd` isn't listed because it has none of these hints, but `sendAvatarData`'s
loop still isn't code the author is likely to have written.
[Its notes](tools/wip/dehint/notes/console_hdd_sendAvatarData.md) have the plan for
another try.

<details>
<summary><b>1. net</b>: 6 tricks, moderate</summary>

- `--param builtin-expect-probability=65`
- 2 per-function `optimize` attributes: `no-crossjumping` on `netSendFile` and
  `no-early-inlining` on `netWritePatches`
- 1 `__builtin_expect`, on `netSendFile`
- 2 pins, on `got` and `buf`

Each function needs only a small fix. The exception is `netRecvVerbose`, whose
IPA-CP clone (`netRecv`) still needs the `got` pin for its register choice. Scoping
`rlen` in a block removed `netMkdir`'s attribute, and with `<= 0` on the first send
removed `netWriteBlocks`'s two, but it leaves `netSendFile` 4 lines off.
`netWritePatches` is 10 lines off without its attribute, and a helper holding the
reply check was further off.

</details>

<details>
<summary><b>2. bootloaders</b>: 9 tricks, moderate</summary>

- 5 `optimize` attributes: `no-tree-dominator-opts`, `no-tree-vrp`,
  `no-cse-follow-jumps` and `no-early-inlining`, on `cfDecrypt`, `cbDecrypt`,
  `cdDecrypt`, `ceDecrypt` and `daeVerifySig`
- 1 `always_inline`, on `daeSigCheck`
- 1 guarded `hint()` call, 1 literal-order `asm` and 1 register pin

The three `*Decrypt` attributes each come down to one `xor ebx,ebx` on the
`calloc` failure path, which gcc drops because it knows `buf` is 0 there. Return
types, a separate variable for `calloc`'s result and scoping `key` were no
closer. `cfDecrypt` is 20 lines off without its attribute.

</details>

<details>
<summary><b>3. stfs</b>: 2 tricks, hard</summary>

- 1 `__builtin_expect` and 1 register pin (`fb` in `esi`), both on the loop guard
  in `stfsGetFile`

This was ranked easy, but over 900 source shapes didn't remove either hint: loop
forms, local types and scopes, helpers, and the copy inside the scan loop. The
best reaches 26 differing lines, only swapping `esi` and `ecx`. IRA colours `fb`
before the `c->blocks` pseudo, so `fb` takes `ecx`. Changing the guard's
probability didn't fix it, and low values change the layout too. A match
probably needs something that makes `ecx` unavailable to `fb`.

</details>

<details>
<summary><b>4. mode_update</b>: 16 tricks, hard</summary>

- `-fno-toplevel-reorder` and `--param builtin-expect-probability=68`
- Dead layout hints in `mode_update` and `updateNand`: 7 `__builtin_constant_p`,
  1 `asm goto`, 1 `__builtin_unreachable`, 1 `if (0)` dummy block, 1 pin and 1
  hot label
- 1 `__builtin_expect`, on `updateNand`
- `XB_PATCHES`

Without the dead hints, the only difference was cold-block order in the last
bb-reorder round, with no register changes, so the target is narrow. It is still
a Fibonacci-heap tie, which needs the exact frequencies.

</details>

<details>
<summary><b>5. image_write</b>: 18 tricks, hard</summary>

- `--param builtin-expect-probability=50`
- 7 dead tests in `imgAdd` and `imgAddFile`, which VRP1 removes
- 4 register and slot pins, across `buildImage`, `imgAdd` and `finalizeImage`
- 2 `__builtin_expect`, 2 hot and cold labels, and
  `optimize("no-tree-scev-cprop")` on `writeFsTable`
- 1 asm-label prototype: `xmalloc`, which stops CCP assuming `malloc`'s alignment.
  `-fno-builtin-malloc` doesn't replace it

The dead tests set `imgAdd`'s IPA-CP value and which SSA names get recycled.
Those decide three clones and the compare operand order throughout, so a
hint-free source would have to land on the same numbers.

</details>

<details>
<summary><b>6. keys</b>: 20 tricks, hard</summary>

- `-fno-toplevel-reorder` and `--param builtin-expect-probability=60`
- 10 `__builtin_expect` and 4 hot and cold labels, mostly in `kvPrepare` and
  `daeEncrypt`, which set trace order and LRA's spill-slot order
- 1 `pure` redeclaration (`getBeU32`), which only this file can use
- `optimize("no-tree-forwprop", "no-tree-reassoc")` on `smcChecksum`, 2 lines off
  without it
- 2 pins (`off` in `daeEncrypt`)

The hints are spread over several functions, and `kvPrepare` depends on several
of them together. The `smcChecksum` attribute exists because its standalone copy
must differ from the inlined one.

</details>

<details>
<summary><b>7. filelist_ini</b>: 23 tricks, hard</summary>

- 4 options: `-fno-toplevel-reorder`, `-fno-tree-loop-vectorize`,
  `--param builtin-expect-probability=65` and
  `--param lra-inheritance-ebb-probability-cutoff=60`
- 12 dead tests (`< -1` and `< 0` stores, a `strlen` block), whose freed SSA
  names set compare order and pseudo numbers
- 3 literal-order `asm`, 1 pin and 1 `__builtin_unreachable` in `findKey`
- 1 `__builtin_expect` and `optimize("ira-region=one")`

The SSA-numbering hints are the problem. Their effects are indirect, and each
source change disturbs the rest. Vectorization and LRA's cutoff are global
options with no direct source equivalent.

</details>

<details>
<summary><b>8. image_read</b>: 32 tricks, hard</summary>

- `-fno-toplevel-reorder`
- 8 register pins across `checkBlock`, `detectController`, `fsGetFile` and others
- 5 `__builtin_expect`, 5 hot labels, 4 `__builtin_unreachable` and 3 empty `asm`
  barriers
- 2 `optimize` attributes (`no-if-conversion` and related), on `getImageSmc` and
  `copyMmcImage`
- 2 literal-order `asm`, 1 `if (0)` block and `noinline`

There's no single hard knot like the other hard files, but many functions each
need their own solution. Several hints are only 3 or 4 lines from going, so this
is probably the best of the hard files to work through next.

</details>

<details>
<summary><b>9. build</b>: 54 tricks, very hard</summary>

- `-fno-toplevel-reorder` and `--param builtin-expect-probability=98`
- 19 `__builtin_expect`, 9 pins, 6 hot and cold labels and 5 `cb_hint()` calls,
  across `loadFileCrc`, `extractSmcConfig`, `patchSmcConfig`, `loadBl` and others
- 2 `__builtin_constant_p`: a dead entry in `loadBl`'s `checkBl` copy that lives
  until dom2
- 3 `no-early-inlining` attributes, 3 inlining and cloning attributes, and 2
  `__builtin_assume_aligned`
- 1 asm-label prototype (`imgAddInt`), `XB_FILES_BOUND` and 1 literal-order `asm`

It's the largest file at 2,800 lines. The expect probability has to sit in a
narrow, unusually high range (92-99), and the dom2 entry is there to keep one
frequency from scaling to 0.

</details>

<details>
<summary><b>10. options</b>: 70 tricks, very hard</summary>

- `--param builtin-expect-probability=83`
- 30 `__builtin_constant_p`, 16 `__builtin_expect`, 3 `asm goto`, 3
  `__builtin_unreachable` and 2 `if (0)` blocks, nearly all setting the cold
  layout of `applyIniOptions`
- 2 `po_hint()` calls and 1 `no-early-inlining` attribute, for `parseOption`
- `_parseButton.part.0`, written by hand as a global `cold` function in
  `.text.startup` rather than coming from gcc's own function split
- 1 asm-label prototype (`parseOptionInt`), `XB_PATCHES`, 1 cold label, 3 pins, 1
  literal-order `asm`, 1 barrier and `always_inline`

The main clue that this can work is that natural source (`optIniBool` inlined,
plain calls) already gives the whole hot layout. The cold layout is the unsolved
part, and it's a heap-tie problem across a very long function. A hint-free
source would also have to split `parseButton` the way gcc did.

</details>

<details>
<summary><b>11. mode_client</b>: 142 tricks, very hard</summary>

- `-fno-toplevel-reorder` and `--param builtin-expect-probability=50`
- 89 `__builtin_constant_p` feeds and 19 `asm goto` edges to dead labels, which
  set bb-reorder's heap keys
- 10 pins, including ones that only raise LRA's `edi` usage
- 7 hot and cold labels, 6 expects, 3 `if (0)` blocks, 3 `__builtin_unreachable`
  and 2 literal-order `asm`

The source was fitted to a simulated heap by search, over more than 130
attempts, and is nowhere near readable, though about 40% of its hints turned out
not to matter. `clientEraseBlock` is even inlined by hand so its labels can be
reached. `mode_client` itself is one long option loop and switch, so nearly every
change moves the rest of the layout. Rewriting it from scratch is probably the
only way to find the natural shape.

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
