#!/bin/sh
# applyIniOptions with a crafted profile: sh aiofdo.sh <dir> [overrides]
# <dir>/a.c must exist. Prints blk.py and fncmp line counts.
set -e
d=$1; shift
R=$(pwd -P)
d=$(cd "$d" && pwd -W 2>/dev/null || pwd)
FL="${AIOFL:--fno-ipa-profile -fno-reorder-functions -O3 -fno-asynchronous-unwind-tables --param builtin-expect-probability=83}"
ONLY=${AIOONLY:-applyIniOptions}
if [ ! -f "$d/-.gcno" ] || [ "$d/a.c" -nt "$d/-.gcno" ]; then
  (cd "$d" && PATH="$R/tools/toolchain-4745/mingw32/bin:$PATH" gcc -S -I "$R/wip" -I "$R/src" $FL \
    -fprofile-arcs -ftest-coverage -fdump-tree-profile_estimate-blocks-details "$d/a.c" -o - >/dev/null)
fi
python re/gcda.py "$d/-.gcno" "$d/a.c.042t.profile_estimate" "$d/-.gcda" "$@" --only=$ONLY >/dev/null
python wip/blk.py "$d/a.c" applyIniOptions $FL -fbranch-probabilities "-fprofile-dir=$d" > "$d/blk.diff" 2>&1 || true
FNCMP_LITERALS=1 python re/fncmp.py "$d/a.c" applyIniOptions $FL -fbranch-probabilities "-fprofile-dir=$d" > "$d/fdo.diff" 2>&1 || true
echo "blk $(grep -c '^[-+][^-+]' "$d/blk.diff") fncmp $(grep -c '^[-+][^-+]' "$d/fdo.diff")"
