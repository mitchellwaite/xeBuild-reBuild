# xeBuild rebuild

[![win64](https://img.shields.io/github/check-runs/mitchellwaite/xeBuild-reBuild/master?nameFilter=windows%20%28MINGW64%29&label=win64)](https://github.com/mitchellwaite/xeBuild-reBuild/actions/workflows/build.yml)
[![macOS](https://img.shields.io/github/check-runs/mitchellwaite/xeBuild-reBuild/master?nameFilter=macos&label=macOS)](https://github.com/mitchellwaite/xeBuild-reBuild/actions/workflows/build.yml)
[![linux](https://img.shields.io/github/check-runs/mitchellwaite/xeBuild-reBuild/master?nameFilter=linux&label=linux)](https://github.com/mitchellwaite/xeBuild-reBuild/actions/workflows/build.yml)

A C source rebuild of `xeBuild.exe` (v1.21 build 810) that compiles back to
the exact same bytes as the released binary. With matching source, xeBuild's
bugs can be fixed in C instead of by patching the executable.

The reference binary is `xeBuild.exe` in this folder, SHA256
`10DAC648197FA5CDBB82D975AB9FF11F64075C9686908DFD9A33EDC533F1971C`.

## Status

- [x] Produce xeBuild from C
- [x] Initial de-slopification of the decompiled source
- [ ] Fix bugs and add features

The rebuild is complete: all of the program's code is C, and the build
reproduces the original exe byte for byte. We've finished the initial
de-slopification, turning the compiler-matching output into readable source
that still builds to the same bytes, and are moving on to bug fixes and
features.

- **Application:** 25 source files (432 functions), rebuilt by hand from the
  binary.
- **Crypto:** 41 source files (185 functions) from XeCrypt, its crypto
  library, used as published.

## Fixes and enhancements

Compared with plain xeBuild 1.21.810, builds with `XEBUILD_FIXES` (every
platform but `win32`, see [Building](#building)) have:

- **Flash header fixes:** the patch slot size defaults to 0x10000 (the
  original left it 0 for Xenon, Zephyr, Falcon and Jasper XSB images), and
  Xenon and Zephyr images keep their KV size instead of 0. JRunner patched
  both after every build (`fixBuggyXeBuildImage`); XeLL needs the KV size to
  find the KV.
- **Version banner:** names the build and the compiler's target triple, e.g.
  `xeBuild reBuild (x86_64-linux-gnu)`.
- **Usage text:** lists every `-t` image type and `-c` console type the
  parser accepts, the `ini` mode and `-norandom`.
- **Console info:** names big block Corona and Winchester consoles.

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
tricks some functions needed to match (and how they were removed, under
"Compiler tricks by component"), and the checks behind each step.

## Repository layout

| Path | Contents |
|---|---|
| `xeBuild.exe` | the reference binary (never modified) |
| `src/` | the application's C source and headers |
| `src/crypto/` | XeCrypt (AES, RC4, SHA-1, MD5, DES, RSA/BigDigits) |
| `src/globals.c` | the program's uninitialized globals |
| `Makefile` | builds everything (GNU make); `make check` also checks the result |
| `tools/re/` | reverse-engineering and verification scripts |
| `tools/` | the toolchain's packages and setup, and ddisasm setup |
| `tools/ref/` | `xeBuild64`, an older (v1.16) stripped Linux x86-64 build, gcc 4.9.2: a structural cross-check only |
| `tools/wip/` | notes from the matching work (the experiments themselves are in the `wip-archive-2026-11` tag) |

## Building

You need Windows with Git Bash, GNU make (for example
`winget install ezwinports.make`) and Python. First unpack the pinned
toolchain, whose packages are in `tools/packages/` (to `tools/toolchain-4745/`;
it also rebuilds two import libraries from the mingw-w64 sources in
`tools/mingw-w64/`):

```bash
sh tools/fetch_toolchain.sh
```

Then build:

```bash
make check
```

This writes `build/xeBuild.exe`, compares it with the reference and prints
its SHA256, which should match the one above (it fails if it doesn't).
`make check -j8` builds in parallel, and a second run rebuilds only what
changed. On Windows plain `make` does the same as `make check`.

The Makefile detects the platform (or set `PLATFORM=`):

| Platform | Compiler | Output | Checked |
|---|---|---|---|
| `win32` (Windows) | the pinned toolchain | `build/xeBuild.exe` | yes, by default |
| `win32fixes` (`make win32fixes`) | the pinned toolchain, with fixes | `build/xeBuild.exe` | no |
| `win32latest` (`make win32latest`) | the MSYS2 `gcc` on PATH | `build/xeBuild.exe` | no |
| `linux` | the installed `gcc` | `build/xeBuild` | no |
| `macos` | the installed `clang` | `build/xeBuild` | no |

Only `win32` reproduces the reference, so it builds the original's
behaviour. Every other platform compiles with `-DXEBUILD_FIXES`, which turns
on new behaviour and bug fixes (listed under
[Fixes and enhancements](#fixes-and-enhancements)).

Every fix or enhancement goes under `XEBUILD_FIXES`: `#ifdef XEBUILD_FIXES`
compiles in new behaviour (with the original in an `#else` where it
replaces something), and `#ifndef XEBUILD_FIXES` compiles out original
behaviour that a fix drops. Every platform puts its objects in
`build/obj/`; switching platforms recompiles them all. `CC`, `CFLAGS`, `LDFLAGS` and
`LDLIBS` can be overridden on the command line or in an untracked
`config.mk`. Re-disassembling the binary also needs ddisasm under WSL;
NOTES.md covers that.

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
