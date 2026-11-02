# cmp1.sh FILE.c : one line: size, jump/nop-level byte status vs build/obj/mode_client.o
R=/c/Users/Win11VM/Documents/GitHub/xebuildBugFix; cd $R; TC=tools/toolchain-4745/mingw32/bin; export PATH="$PWD/$TC:$PATH"; n=$(basename $1 .c); D=build/v/mc150/sub
FL="-O3 -fno-toplevel-reorder -fno-ipa-profile -fno-reorder-functions --param builtin-expect-probability=50"
{ printf '#line 1 "mode_client.c"\n'; cat $1; } | gcc.exe -c $FL -Isrc -x c - -o $D/$n.o 2>/dev/null || { echo "$n ERR"; exit; }
t=$(objdump -s -j .text $D/$n.o | tail -n +4 | md5sum | cut -c1-8); r=$(objdump -s -j .text build/obj/mode_client.o | tail -n +4 | md5sum | cut -c1-8)
d=$(objdump -s -j .text $D/$n.o | tail -n +4 | diff - <(objdump -s -j .text build/obj/mode_client.o | tail -n +4) | grep -c '^<')
echo "$d $n $([ $t = $r ] && echo TEXTSAME)"
rm -f $D/$n.o
