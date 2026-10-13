#!/bin/sh
# Assemble every object in src/objects.txt, link them with src/link.ld into
# build/xeBuild.exe and check it against the reference.  Run from the repo root
# in Git Bash after tools/fetch_toolchain.sh.
set -e
TC=tools/toolchain-4745/mingw32/bin
OBJ=build/obj
objs=
for f in $(grep -v '^#' src/objects.txt | tr -d '\r'); do
  mkdir -p "$OBJ/$(dirname "$f")"
  "$TC/as.exe" --32 "src/$f.s" -o "$OBJ/$f.o"
  objs="$objs $OBJ/$f.o"
done
"$TC/ld.exe" -m i386pe -T src/link.ld --image-base 0x400000 -e __EntryPoint \
  --subsystem console -s --no-insert-timestamp -Map build/xeBuild.map \
  -o build/xeBuild.exe $objs
# original link time; ld 2.27 can't take a fixed timestamp itself
python re/stamp.py build/xeBuild.exe 0x5DCAB029
python re/execmp.py xeBuild.exe build/xeBuild.exe
sha256sum build/xeBuild.exe
