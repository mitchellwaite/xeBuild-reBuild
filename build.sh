#!/bin/sh
# Build build/xeBuild.exe and check it against the reference: the Makefile
# does the work (GNU make; set MAKE if it isn't `make` on PATH).  Run from
# the repo root in Git Bash after tools/fetch_toolchain.sh.  Extra arguments
# go to make, e.g. `sh build.sh -j4`.
exec "${MAKE:-make}" check "$@"
