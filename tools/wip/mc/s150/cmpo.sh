# cmpo.sh FILE.c : byte compare (plain compile, build.sh flags) of .text/.rdata/.bss + relocs with build/obj/mode_client.o; prints md5 equalities and a short disasm diff
R=/c/Users/Win11VM/Documents/GitHub/xebuildBugFix; cd $R; TC=tools/toolchain-4745/mingw32/bin; export PATH="$PWD/$TC:$PATH"; D=build/v/mc150/o; mkdir -p $D
n=$(basename $1 .c); FL="-O3 -fno-toplevel-reorder -fno-ipa-profile -fno-reorder-functions --param builtin-expect-probability=50"
{ printf '#line 1 "mode_client.c"\n'; cat $1; } | gcc.exe -c $FL $FX -Isrc -x c - -o $D/$n.o || exit 1
sec() { objdump -s -j $2 $1 | tail -n +4; }
for s in .text .rdata '.rdata$zzz'; do if [ "$(sec $D/$n.o $s | md5sum)" = "$(sec build/obj/mode_client.o $s | md5sum)" ]; then echo "$n $s SAME"; else echo "$n $s DIFF"; fi; done
if [ "$(objdump -r $D/$n.o | tail -n +4 | md5sum)" = "$(objdump -r build/obj/mode_client.o | tail -n +4 | md5sum)" ]; then echo "$n relocs SAME"; else echo "$n relocs DIFF"; fi
objdump -h $D/$n.o | grep -E " \.(text|bss|rdata)" | awk '{printf "%s %s  ",$2,$3}'; echo
objdump -d -Mintel --no-show-raw-insn $D/$n.o | tail -n +3 | sed -E 's/^ *[0-9a-f]+:\s*//; s/(j[a-z]+|call) +[0-9a-f]+.*/\1/' > $D/$n.d
objdump -d -Mintel --no-show-raw-insn build/obj/mode_client.o | tail -n +3 | sed -E 's/^ *[0-9a-f]+:\s*//; s/(j[a-z]+|call) +[0-9a-f]+.*/\1/' > $D/ref.d
diff $D/$n.d $D/ref.d | head -${2:-12} | cut -c1-60
