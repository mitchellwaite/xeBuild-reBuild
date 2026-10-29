#!/bin/sh
# Compile a mixed object's C file, splice it into its .s and compare the
# object's .text (alignment included, which tools/re/fncmp.py ignores) with a known
# good object, without a full build.
#   sh tools/wip/mixedcmp.sh <obj> <file.c> <good.o> [gcc flags]
# e.g. sh tools/wip/mixedcmp.sh net src/net.c /tmp/good.o --param builtin-expect-probability=65
# (copy build/obj/<obj>.o to good.o after a matching build).  Prints SAME or
# the first N (default 40) lines of the objdump diff.
TC=tools/toolchain-4745/mingw32/bin
PATH="$PWD/$TC:$PATH"
obj=$1 c=$2 good=$3; shift 3
d=$(mktemp -d)
{ printf '#line 1 "%s"\n' "$obj.c"; cat "$c"; } |
  "$TC/gcc.exe" -S -O3 "$@" -fno-asynchronous-unwind-tables -I"src/$(dirname "$obj")" -x c - -o "$d/t.c.s" || exit 1
python tools/re/splice.py "src/$obj.s" "$d/t.c.s" "$d/t.s" || exit 1
"$TC/as.exe" --32 "$d/t.s" -o "$d/t.o" || exit 1
"$TC/objdump.exe" -d -M intel --no-show-raw-insn "$d/t.o" | sed 1,6d | cut -f2- > "$d/t.dis"
"$TC/objdump.exe" -d -M intel --no-show-raw-insn "$good" | sed 1,6d | cut -f2- > "$d/g.dis"
if cmp -s "$d/t.dis" "$d/g.dis"; then echo SAME; else diff "$d/g.dis" "$d/t.dis" | head -"${N:-40}"; fi
