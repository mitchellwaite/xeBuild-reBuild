#!/bin/sh
# vlink.sh : link the object list of build.sh with options.o from a plain compile of tools/wip/aio/p1/match.c
# (build/obj from the last build; src/ and build.sh untouched), then stamp, execmp and SHA256. Output under build/v/aio_p1/link.
set -e
cd /c/Users/Win11VM/Documents/GitHub/xebuildBugFix
TC=tools/toolchain-4745/mingw32/bin; PATH="$PWD/$TC:$PATH"; OBJ=build/obj; L=build/v/aio_p1/link; mkdir -p $L
{ printf '#line 1 "options.c"\n'; cat tools/wip/aio/p1/match.c; } |
  "$TC/gcc.exe" -c -O3 --param builtin-expect-probability=83 -fno-ipa-profile -fno-reorder-functions -Isrc -x c - -o $L/options.o
objects=$(sed -n '/^objects="/,/spPseudoRand"/p' build.sh | sed 's/objects="//; s/"//')
objs=
for f in $objects; do if [ "$f" = options ]; then objs="$objs $L/options.o"; else objs="$objs $OBJ/$f.o"; fi; done
libs="-lmingw32 -lgcc -lgcc_eh -lmoldname -lmingwex -lmsvcrt -lpthread -ladvapi32 -lshell32 -luser32 -lkernel32"
"$TC/gcc.exe" -s -o $L/xeBuild.exe $objs -lws2_32 $libs $OBJ/globals.o -Wl,--no-insert-timestamp
python tools/re/stamp.py $L/xeBuild.exe 0x5DCAB029
python tools/re/execmp.py xeBuild.exe $L/xeBuild.exe
sha256sum $L/xeBuild.exe xeBuild.exe
