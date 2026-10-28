# plain.sh SRC.c : unprofiled fncmp of mode_client (and clientEraseBlock) vs original, line count + diff saved
B=tools/toolchain-4745/mingw32/bin; export PATH="$PWD/$B:$PATH"
python re/fncmp.py $1 ${FN:-mode_client} -O3 -fno-toplevel-reorder -fno-ipa-profile -fno-reorder-functions -fno-asynchronous-unwind-tables --param builtin-expect-probability=50 -I wip > build/s12/plain.$(basename $1).diff 2>&1
grep -c '^[-+][^-+]' build/s12/plain.$(basename $1).diff
