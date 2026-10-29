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
