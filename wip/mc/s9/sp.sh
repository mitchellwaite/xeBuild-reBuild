#!/bin/sh
# split-test (sp.c) profile build: sp.sh SLOT MODE0PCT ARGNULLPCT HDDPCT [extra overrides]
# prep: python wip/mcfdo.py "$(cygpath -w "$PWD")\build\mcsp" wip/mc/s9/sp.c
export EXTRA='--param builtin-expect-probability=50'
export MCFDO_DIR="$(cygpath -w "$PWD")\build\mcsp"
SLOT=$1; M=$2; A=$3; H=$4; shift 4
FAKE="clientEraseBlock:5>1=100 clientEraseBlock:6>1=100 clientEraseBlock:7>1=100 clientEraseBlock:8>1=100"
COMMON="--consistent --entry=clientEraseBlock:mode_client:${ENTRY:-127}"
python wip/mc/s9/fdorun9.py $SLOT --over mode_client:105\>107=$M mode_client:106\>107=$A mode_client:112\>133=0 mode_client:116\>118=$H mode_client:119\>121=$H mode_client:122\>123=25 mode_client:129\>130=25 mode_client:49\>50=26.9231 mode_client:50\>56=28.5714 mode_client:56\>64=50 clientEraseBlock:2\>8=25 clientEraseBlock:3\>7=33.3 clientEraseBlock:4\>6=50 $FAKE $COMMON "$@" 2>&1 | grep -v "overrides\|realized"
