# mingw-w64 import library sources

Unmodified files from mingw-w64 at commit
`e05f3e86898d91b870c9c7256efd24c8dd6de9cb` (2016-11-23,
https://github.com/mingw-w64/mingw-w64), under the licence in `COPYING`:

- `mingw-w64-crt/lib32/kernel32.def`
- `mingw-w64-crt/lib32/msvcrt.def.in`
- `mingw-w64-crt/def-include/msvcrt-common.def.in`

`tools/fetch_toolchain.sh` builds the toolchain's `libkernel32.a` and
`libmsvcrt.a` from them, as the original exe's were (NOTES.md, Runtime).
