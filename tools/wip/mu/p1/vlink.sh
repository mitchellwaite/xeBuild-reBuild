#!/bin/sh
# vlink.sh [FILE.c] [extra flags]: link build.sh's object list with mode_update.o from a plain compile (default tools/wip/mu/p1/match.c),
# build/obj from the last build (src/ and build.sh untouched), then stamp, execmp and SHA256. Output under build/v/mu_p1/link.
set -e
cd /c/Users/Win11VM/Documents/GitHub/xebuildBugFix
TC=tools/toolchain-4745/mingw32/bin; PATH="$PWD/$TC:$PATH"; OBJ=build/obj; L=build/v/mu_p1/link; mkdir -p $L
SRC=${1:-tools/wip/mu/p1/match.c}
{ printf '#line 1 "mode_update.c"\n'; cat $SRC; } |
  "$TC/gcc.exe" -c -O3 -fno-toplevel-reorder --param builtin-expect-probability=68 $2 -Isrc -x c - -o $L/mode_update.o
objects=$(sed -n '/^objects="/,/spPseudoRand"/p' build.sh | sed 's/objects="//; s/"//')
objs=
for f in $objects; do if [ "$f" = mode_update ]; then objs="$objs $L/mode_update.o"; else [ "$f" = globals ] || objs="$objs $OBJ/$f.o"; fi; done
libs="-lmingw32 -lgcc -lgcc_eh -lmoldname -lmingwex -lmsvcrt -lpthread -ladvapi32 -lshell32 -luser32 -lkernel32"
"$TC/gcc.exe" -s -o $L/xeBuild.exe $objs -lws2_32 $libs $OBJ/globals.o -Wl,--no-insert-timestamp
python tools/re/stamp.py $L/xeBuild.exe 0x5DCAB029
python tools/re/execmp.py xeBuild.exe $L/xeBuild.exe
sha256sum $L/xeBuild.exe xeBuild.exe
objdump -h $L/mode_update.o | grep -E '^ +[0-9]+ \.' | awk '{print $2,$3}' > $L/h1.txt
objdump -h $OBJ/mode_update.o | grep -E '^ +[0-9]+ \.' | awk '{print $2,$3}' > $L/h2.txt
cmp $L/h1.txt $L/h2.txt && echo section sizes same
nm $L/mode_update.o > $L/n1.txt; nm $OBJ/mode_update.o > $L/n2.txt; cmp $L/n1.txt $L/n2.txt && echo symbols same
cmp $L/mode_update.o $OBJ/mode_update.o && echo object file bytes same
