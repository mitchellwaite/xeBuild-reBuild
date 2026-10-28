#!/bin/sh
# Fetch the 2016 MSYS2 packages the original exe was built with, verify them
# against tools/packages.sha256 and unpack the toolchain into tools/toolchain-4745,
# then rebuild its kernel32 and msvcrt import libraries as the original's were
# (below).  Run from the repo root in Git Bash.  repo.msys2.org no longer
# carries these packages.
set -e
M=https://mirrors.mit.edu/kodi/build-deps/win32/msys2/repos/mingw32
T=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$T/pkgs"; cd "$T/pkgs"
for f in $(sed 's/^.*\*//' ../packages.sha256 | tr -d '\r'); do
  [ -f "$f" ] || curl -sfLO "$M/$f"
done
sha256sum -c ../packages.sha256
O=$T/toolchain-4745; rm -rf "$O"; mkdir -p "$O"
for f in *binutils* *gcc-6* *gcc-libs* *gmp* *zlib* *libiconv* *winpthread* \
         *default-manifest-6.4-2* *crt-git-5.0.0.4745* *headers-git-5.0.0.4747*; do
  tar -xJf "$f" -C "$O" --exclude='.*'
done
"$O/mingw32/bin/gcc.exe" --version | head -1
"$O/mingw32/bin/ld.exe" --version | head -1

# The original's crt-git build came between mingw-w64 e05f3e8 (2016-11-23,
# CreateRemoteThreadEx in kernel32.def) and b508bb8 (2017-01-27,
# _create_locale in msvcrt.def.in): the same objects as 4745, but newer
# kernel32 and msvcrt import libraries, whose hints are in the exe.  No
# package of it survives, so build those two as mingw-w64-crt does, from
# e05f3e8's .def files (verified against tools/importlibs.sha256) with this
# dlltool, each with 4745's own objects (lib32_lib*_a-*.o) added, and put
# them in the toolchain's lib directory in place of 4745's.  (They have to be
# in the same directory as the other import libraries: ld's default script
# sorts the .idata pieces by file name, directory included.)
C=e05f3e86898d91b870c9c7256efd24c8dd6de9cb
D=$T/pkgs/mingw-w64-crt-$C
mkdir -p "$D/lib32" "$D/def-include"
for f in $(sed 's/^.*\*//' "$T/importlibs.sha256" | tr -d '\r'); do
  [ -f "$D/$f" ] || curl -sfL -o "$D/$f" \
    "https://raw.githubusercontent.com/mingw-w64/mingw-w64/$C/mingw-w64-crt/$f"
done
(cd "$D" && sha256sum -c "$T/importlibs.sha256")
B=$O/mingw32/bin; L=$O/mingw32/i686-w64-mingw32/lib; I=$O/importlibs
PATH="$B:$PATH"
mkdir -p "$I"; cd "$I"
"$B/gcc.exe" -E -x c "$D/lib32/msvcrt.def.in" -Wp,-w -I"$D/def-include" |
  sed 's/^#/;/' > msvcrt.def
cp "$D/lib32/kernel32.def" kernel32.def
for d in kernel32 msvcrt; do
  "$B/dlltool.exe" --as-flags=--32 -m i386 -k --as="$B/as.exe" \
    --output-lib lib$d.a --input-def $d.def
  mkdir -p obj-$d
  objs=$("$B/ar.exe" t "$L/lib$d.a" | grep '^lib32_')
  (cd obj-$d && "$B/ar.exe" x "$L/lib$d.a" $objs)
  (cd obj-$d && "$B/ar.exe" rc ../lib$d.a $objs)
  "$B/ranlib.exe" lib$d.a
  cp lib$d.a "$L/lib$d.a"
done
