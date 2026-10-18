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
      # readFileIn's __builtin_expect hints are tuned to this probability
      app/fileutil) orig="$f.c"
             cflags="-O3 --param builtin-expect-probability=65" ;;
      # kvCheckHash's __builtin_expect needs a weak hint (51-60 match)
      app/keyvault) orig="$f.c"
             cflags="-O3 --param builtin-expect-probability=55" ;;
      # showInfoKeys aligns a block at frequency 61 of 9412 (default 100
      # would need 95); 155 and up match
      app/consoleinfo) orig="$f.c"
             cflags="-O3 --param align-threshold=200" ;;
      # getBadBlocks aligns its error block, which the default (100) doesn't;
      # getConsoleFiles' netMount hint needs 68 (66-70 in other forms)
      app/mode_update) orig="$f.c"
             cflags="-O3 --param align-threshold=200 --param builtin-expect-probability=68" ;;
      # setFuseCpuKey aligns its fuse == NULL block; fcrtEncrypt's offset
      # hint needs 60
      app/keys) orig="$f.c"
             cflags="-O3 --param align-threshold=200 --param builtin-expect-probability=60" ;;
      # console_hdd's __builtin_expect hints are tuned to this probability;
      # sendAvatarData's loop is aligned (1 and 2 align other loops too)
      app/console_hdd) orig="$f.c"
             cflags="-O3 --param builtin-expect-probability=80 --param align-loop-iterations=3" ;;
      # padding between functions is top-level asm between the C ones;
      # -fno-toplevel-reorder keeps that order (gcc 6 otherwise puts all
      # top-level asm first), and the asm carries the object's .eh_frame
      app/bootloaders) orig="$f.c"
             cflags="-O3 -fno-toplevel-reorder -fno-asynchronous-unwind-tables" ;;
      # original path unknown (no assert in the app); timeutil needs -O3
      app/*) orig="$f.c"
             cflags="-O3" ;;
      *) echo "build.sh: no flags for $f" >&2; exit 1 ;;
    esac
    if [ -f "src/$f.s" ]; then
      # mixed object: splice the C functions into the .s (re/splice.py)
      { printf '#line 1 "%s"\n' "$orig"; cat "src/$f.c"; } |
        "$TC/gcc.exe" -S $cflags -fno-asynchronous-unwind-tables \
          -I"src/$(dirname "$f")" -x c - -o "$OBJ/$f.c.s"
      python re/splice.py "src/$f.s" "$OBJ/$f.c.s" "$OBJ/$f.s"
      "$TC/as.exe" --32 "$OBJ/$f.s" -o "$OBJ/$f.o"
    else
      { printf '#line 1 "%s"\n' "$orig"; cat "src/$f.c"; } |
        "$TC/gcc.exe" -c $cflags -I"src/$(dirname "$f")" -x c - -o "$OBJ/$f.o"
    fi
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
