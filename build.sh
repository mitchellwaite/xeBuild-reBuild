#!/bin/sh
# Build every object in src/objects.txt (src/<obj>.c with gcc if it exists,
# else src/<obj>.s with as), link them with src/link.ld into build/xeBuild.exe
# and check it against the reference.  Run from the repo root in Git Bash after
# tools/fetch_toolchain.sh.
set -e
TC=tools/toolchain-4745/mingw32/bin
OBJ=build/obj
# gcc finds cc1/as and their DLLs through PATH
PATH="$PWD/$TC:$PATH"
objs=
for f in $(grep -v '^#' src/objects.txt | tr -d '\r'); do
  mkdir -p "$OBJ/$(dirname "$f")"
  if [ -f "src/$f.c" ]; then
    case "$f" in
      # original build path, for __FILE__ in assert(); fed through stdin so
      # the #line can name it (gcc 6 has no -ffile-prefix-map)
      # src/crypto is XeCrypt's tree (headers include "bign/bigdigits.h" etc.)
      crypto/*) orig="H:/x360sdk/__NAND/nandbuild_trin/XeCrypt/${f#crypto/}.c"
                cflags="-O3 -Isrc/crypto" ;;
      # original path unknown (no assert in the app); timeutil needs -O3
      app/*) orig="$f.c"
             cflags="-O3" ;;
      *) echo "build.sh: no flags for $f" >&2; exit 1 ;;
    esac
    { printf '#line 1 "%s"\n' "$orig"; cat "src/$f.c"; } |
      "$TC/gcc.exe" -c $cflags -I"src/$(dirname "$f")" -x c - -o "$OBJ/$f.o"
  else
    "$TC/as.exe" --32 "src/$f.s" -o "$OBJ/$f.o"
  fi
  objs="$objs $OBJ/$f.o"
done
"$TC/ld.exe" -m i386pe -T src/link.ld --image-base 0x400000 -e __EntryPoint \
  --subsystem console -s --no-insert-timestamp -Map build/xeBuild.map \
  -o build/xeBuild.exe $objs
# original link time; ld 2.27 can't take a fixed timestamp itself
python re/stamp.py build/xeBuild.exe 0x5DCAB029
python re/execmp.py xeBuild.exe build/xeBuild.exe
sha256sum build/xeBuild.exe
