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
ranks the 2 files that still have them from easiest to hardest to match with
source shape alone: ordinary C, the same `-O3` as the rest, and none of these
hints. The other 23 application files build with no tricks.

Every hint in these files has been tried on its own, and `tools/wip/hintsearch.py`
removes any that no longer change the code, but no hint-free source has been
attempted for them, so the ranking is an estimate. Trick count isn't the only
factor: a single hint can be harder to replace than several others if it sets
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
- **Declarations:** asm-label prototypes

Writing a function success-first, duplicating a block, inlining a helper by
hand and spelling a byte swap differently are source shape, so they aren't
counted. Neither are plain type casts, or an array longer than it needs to be,
which gets a `TODO` comment explaining it instead. `filelist_ini`'s `findKey`
keeps one dead `key == NULL` test that also isn't counted, because the author may
well have written a check like it; a comment on the test explains it. Likewise
`image_read`'s `getImageSmc` keeps an `excess` added to `addr` that is always 0,
which keeps `addr`'s conversion in the block PRE would otherwise move it out of;
its comment marks it "Borderline, for review", the tag the other borderline
shapes in `src/` use too.

<details>
<summary><b>1. options</b>: 22 tricks, very hard</summary>

- `--param builtin-expect-probability=83`
- 7 `__builtin_constant_p`, 7 `__builtin_expect`, 2 `asm goto` and 2
  `__builtin_unreachable`, nearly all setting the cold layout of
  `applyIniOptions`
- `_parseButton.part.0`, written by hand as a global `cold` function in
  `.text.startup` rather than coming from gcc's own function split

The main clue that this can work is that natural source (`optIniBool` inlined,
plain calls) already gives the whole hot layout. The cold layout is the unsolved
part, and it's a heap-tie problem across a very long function. A hint-free
source would also have to split `parseButton` the way gcc did.

</details>

<details>
<summary><b>2. mode_client</b>: 48 tricks, very hard</summary>

- 23 `__builtin_constant_p` feeds and 10 `asm goto` edges to dead labels, which
  set bb-reorder's heap keys
- 6 pins
- 4 hot and cold labels, 2 `if (0)` blocks and 2 `__builtin_unreachable`

The source was fitted to a simulated heap by search, over more than 130
attempts, and is nowhere near readable. A first de-tricking pass deleted the
hints that turned out not to matter, and a second found plain-C shapes for
the literal-order and `clientBinPatch` hints; the expects, and with them
the `--param`, went for arms that start with a call; feeds moved to colder blocks need
fewer terms, and some removals pay for themselves with one more label
on an existing `asm goto`, or with a test split into ifs that
repeat the same noreturn call (141 to 48;
`tools/wip/dehint/notes/mode_client.md`). `clientEraseBlock` is even inlined by hand so its labels can be
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
