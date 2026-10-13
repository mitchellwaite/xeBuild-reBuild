#!/bin/sh
# Assemble + link src/xeBuild.s into build/xeBuild.exe and check it against the
# reference.  Run from the repo root in Git Bash after tools/fetch_toolchain.sh.
set -e
TC=tools/toolchain-4745/mingw32/bin
mkdir -p build
"$TC/as.exe" --32 src/xeBuild.s -o build/xeBuild.o
"$TC/ld.exe" -m i386pe -T src/xeBuild.ld --image-base 0x400000 -e __EntryPoint \
  --subsystem console -s --no-insert-timestamp -Map build/xeBuild.map \
  -o build/xeBuild.exe build/xeBuild.o
# original link time; ld 2.27 can't take a fixed timestamp itself
python re/stamp.py build/xeBuild.exe 0x5DCAB029
python re/execmp.py xeBuild.exe build/xeBuild.exe
sha256sum build/xeBuild.exe
