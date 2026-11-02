#!/bin/sh
D=$(cd $(dirname $0); pwd)
for f in "$@"; do cp $D/b0.ref ${f%.c}.ref; echo "$(basename $f .c) $(sh $D/../s101/f2.sh $f)"; done
