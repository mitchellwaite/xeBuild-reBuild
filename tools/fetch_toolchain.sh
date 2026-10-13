#!/bin/sh
# Fetch the 2016 MSYS2 packages the original exe was built with, verify them
# against tools/packages.sha256 and unpack the toolchain into tools/toolchain-4745.
# Run from the repo root in Git Bash.  repo.msys2.org no longer carries these.
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
