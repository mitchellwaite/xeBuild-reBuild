#!/bin/sh
# run.sh DIR : f2 of every DIR/*.c, 4 parallel, into DIR/res.txt
ls $1/*.c | xargs -P4 -I{} sh -c 'echo "$(sh ../../s101/f2.sh {}) {}"' | sort -n > $1/res.txt
