#!/bin/sh
# mode_update with a crafted profile (wip/gcda.py); see wip/README.md.
#   sh wip/mufdo.sh <dir> [fn:src>dst=prob ...]
# Copies wip/app/mode_update.c to <dir>/m.c (first run), compiles it once with
# -fprofile-arcs -ftest-coverage for the .gcno and the profile_estimate dump,
# writes <dir>/-.gcda (counts for mode_update and updateNand only; the
# overrides use the dump's bb numbers) and runs fncmp on the profile build.
# Prints the fncmp line count; the diff is in <dir>/fdo.diff.
# Best so far (8 lines): mode_update:39>40=62 updateNand:24>25=14.5
set -e
d=$1; shift
R=$(pwd -P)  # /c/... even when started from Python ($PWD is C:/..., which breaks PATH)
mkdir -p "$d"
[ -f "$d/m.c" ] || cp wip/app/mode_update.c "$d/m.c"
d=$(cd "$d" && pwd -W 2>/dev/null || pwd)
FL="-fno-inline-small-functions -fno-partial-inlining -fno-ipa-profile -fno-reorder-functions -O3 -fno-asynchronous-unwind-tables --param align-threshold=200 --param builtin-expect-probability=68"
# -o - : the aux name (static functions' profile ids, the .gcda name) must be
# the one fncmp's compile gets
if [ ! -f "$d/-.gcno" ] || [ "$d/m.c" -nt "$d/-.gcno" ]; then
  (cd "$d" && PATH="$R/tools/toolchain-4745/mingw32/bin:$PATH" gcc -S -I "$R/wip/app" $FL \
    -fprofile-arcs -ftest-coverage -fdump-tree-profile_estimate-blocks-details "$d/m.c" -o - >/dev/null)
fi
python wip/gcda.py "$d/-.gcno" "$d/m.c.042t.profile_estimate" "$d/-.gcda" "$@" --only=mode_update,updateNand >/dev/null
FNCMP_LITERALS=1 python re/fncmp.py "$d/m.c" mode_update $FL -fbranch-probabilities "-fprofile-dir=$d" > "$d/fdo.diff" 2>&1 || true
grep -c '^[-+][^-+]' "$d/fdo.diff" || true
