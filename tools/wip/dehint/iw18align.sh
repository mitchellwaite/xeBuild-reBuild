#!/bin/sh
# sh tools/wip/dehint/iw18align.sh <name> <file.c>: alias dumps (they print ALIGN/MISALIGN for pointer names) into build/iw/a18/al_<name>,
# then, for each tree pass, the 512-byte memcpy dests in finalizeImage's ECD loop and their ptr info.
R=$(cd "$(dirname "$0")/../../.." && pwd)
export PATH=$R/tools/toolchain-4745/mingw32/bin:$PATH
d=$R/build/iw/a18/al_$1; mkdir -p "$d"; cp "$2" "$d/a.c"; cd "$d" || exit 1
rm -f a.c.*; gcc -c -O3 -I"$R/src" a.c -o a.o -fdump-tree-all-alias || exit 1
for f in a.c.*; do
  python "$R/tools/wip/dehint/iw18align.py" "$f"
done
