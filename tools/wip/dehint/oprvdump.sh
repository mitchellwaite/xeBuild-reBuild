#!/bin/sh
# oprvdump.sh src.c outdir : plain -O3 dumps of an options.c variant (bbro details, rtl_dce
# blocks with frequencies, optimized blocks, profile_estimate); oprv.py -o writes the source
R=$(cd "$(dirname "$0")/../../.." && pwd)
TC="$R/tools/toolchain-4745/mingw32/bin"
export PATH="$TC:$PATH"
mkdir -p "$2"
{ printf '#line 1 "options.c"\n'; cat "$1"; } > "$2/options.c"
cd "$2" && "$TC/gcc.exe" -c -O3 -I"$R/src" options.c -o o.o -fdump-rtl-bbro-details -fdump-rtl-rtl_dce-blocks-details -fdump-tree-optimized-blocks -fdump-tree-profile_estimate-details
