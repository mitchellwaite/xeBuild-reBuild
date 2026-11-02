#!/bin/sh
# ev.sh X.c : prints "f2 entryfreq 141-round" for a variant
S=/c/Users/Win11VM/Documents/GitHub/xebuildBugFix/tools/wip/mc
f=$(sh $S/s101/f2.sh $1)
sh $S/s104/bi.sh $1 > ${1%.c}.bbinfo 2>&1
e=$(awk 'NR==1{print $6}' ${1%.c}.bbinfo)
bp=$(grep clientBinPatch ${1%.c}.bbinfo | awk '{print $4,$6}')
echo "$(basename $1) f2=$f entry=$e binpatch=$bp"
