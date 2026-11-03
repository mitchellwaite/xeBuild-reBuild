#!/bin/sh
# vlink.sh [FILE.c] [flags]: compile FILE.c as build.sh does (default match.c, -O3), compare every section and the relocs with build/obj/mode_update.o,
# link build.sh's object list with it, stamp, execmp, SHA256.  Output under build/v/mu_d1/link.  Touches nothing that build.sh tracks.
set -e
cd /c/Users/Win11VM/Documents/GitHub/xebuildBugFix
TC=tools/toolchain-4745/mingw32/bin; PATH="$PWD/$TC:$PATH"; OBJ=build/obj; L=build/v/mu_d1/link; mkdir -p $L
SRC=${1:-tools/wip/mu/d1/match.c}
FL=${2:--O3}
{ printf '#line 1 "mode_update.c"\n'; cat $SRC; } |
  "$TC/gcc.exe" -c $FL -Wall -Wno-unused-label -Isrc -x c - -o $L/mode_update.o 2>&1 | grep -E "warning|error" | head -20 || true
sec() { objdump -s -j $2 $1 | tail -n +4; }
for s in .text .data .bss .rdata '.rdata$zzz' .eh_frame; do
  if [ "$(sec $L/mode_update.o $s | md5sum)" = "$(sec $OBJ/mode_update.o $s | md5sum)" ]; then echo "$s SAME"; else echo "$s DIFF"; fi
done
if [ "$(objdump -r $L/mode_update.o | tail -n +4 | md5sum)" = "$(objdump -r $OBJ/mode_update.o | tail -n +4 | md5sum)" ]; then echo "relocs SAME"; else echo "relocs DIFF"; fi
objects=$(sed -n '/^objects="/,/spPseudoRand"/p' build.sh | sed 's/objects="//; s/"//')
objs=
for f in $objects; do if [ "$f" = mode_update ]; then objs="$objs $L/mode_update.o"; else [ "$f" = globals ] || objs="$objs $OBJ/$f.o"; fi; done
libs="-lmingw32 -lgcc -lgcc_eh -lmoldname -lmingwex -lmsvcrt -lpthread -ladvapi32 -lshell32 -luser32 -lkernel32"
"$TC/gcc.exe" -s -o $L/xeBuild.exe $objs -lws2_32 $libs $OBJ/globals.o -Wl,--no-insert-timestamp
python tools/re/stamp.py $L/xeBuild.exe 0x5DCAB029
python tools/re/execmp.py xeBuild.exe $L/xeBuild.exe
sha256sum $L/xeBuild.exe xeBuild.exe
cmp $L/mode_update.o $OBJ/mode_update.o && echo object file bytes same
