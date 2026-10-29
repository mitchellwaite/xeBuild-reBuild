#!/bin/sh
R=$(cd "$(dirname "$0")/../../.." && pwd -P)
# run.sh <dir> <overrides file>: build with overrides, dumps, labeled diff (mismatches) and r3/r4 traces
S=$(cd "$(dirname "$0")" && pwd -P)
cd $R
sh $S/aiofdo.sh $S/$1 $(grep -v '^#' $S/$2) 
sh $S/dumps.sh $S/$1
cd $S
python lab.py $1/o.s | grep -v '^\* -:\.  *$' > $1/lab.txt
grep -c '^\*' $1/lab.txt
python trl.py $1 > $1/trl.txt
