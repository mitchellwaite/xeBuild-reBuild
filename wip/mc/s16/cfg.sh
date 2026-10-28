#!/bin/sh
# cfg.sh SLOTDIR [lo hi]: pre-bbro CFG (compgotos, details) of the slot's profiled compile
R="$(pwd)"; D="$R/$1"; shift; B="$R/tools/toolchain-4745/mingw32/bin"; export PATH="$B:$PATH"
M="$(cygpath -w "$(dirname "$D")")\m.c"
mkdir -p "$D/cfgd"; cp "$D"/*.gcda "$D/cfgd/" 2>/dev/null
(cd "$D" && gcc -S -masm=intel -O3 -fno-toplevel-reorder -fno-ipa-profile -fno-reorder-functions -fno-asynchronous-unwind-tables --param builtin-expect-probability=50 -fbranch-probabilities -fprofile-dir="$(cygpath -w "$D")" -fdump-rtl-compgotos-blocks-details -I "$(cygpath -w "$R/wip")" "$M" -o - > /dev/null 2>&1)
python wip/mc/cfgdump.py "$D/m.c.267r.compgotos" mode_client "$@"
