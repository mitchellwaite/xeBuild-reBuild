#!/bin/sh
# cmpo.sh FILE.c : plain compile as build.sh would (gcc -c, flags below), section bytes + relocs vs build/obj/mode_update.o
R=/c/Users/Win11VM/Documents/GitHub/xebuildBugFix; cd $R; TC=tools/toolchain-4745/mingw32/bin; export PATH="$PWD/$TC:$PATH"; D=build/v/mu_p1/o; mkdir -p $D
n=$(basename $1 .c); FL="-O3 -fno-toplevel-reorder --param builtin-expect-probability=68"
sec() { objdump -s -j $2 $1 | tail -n +4; }
{ printf '#line 1 "mode_update.c"\n'; cat $1; } | gcc.exe -c $FL $FX -Isrc -x c - -o $D/$n.o || exit 1
for s in .text .data .bss .rdata .text.startup '.rdata$zzz' .eh_frame; do if [ "$(sec $D/$n.o $s | md5sum)" = "$(sec build/obj/mode_update.o $s | md5sum)" ]; then echo "$n $s SAME"; else echo "$n $s DIFF"; fi; done
if [ "$(objdump -r $D/$n.o | tail -n +4 | md5sum)" = "$(objdump -r build/obj/mode_update.o | tail -n +4 | md5sum)" ]; then echo "$n relocs SAME"; else echo "$n relocs DIFF"; fi
objdump -h $D/$n.o | grep -E " \.(text|rdata|eh_frame)" | awk '{printf "%s %s  ",$2,$3}'; echo
