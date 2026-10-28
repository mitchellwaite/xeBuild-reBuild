#!/bin/sh
# usage: fdo.sh SLOT EXITPCT CASE HDD "extra design" -- extra overrides
# cases all = CASE, HDD errors = HDD, loop exit EXITPCT (post = 10000*p)
export EXTRA='--param builtin-expect-probability=50'
SLOT=$1; P=$2; C=$3; H=$4; X=$5; shift 5
POST=$(python -c "print(10000*$P/100)")
export MC_POST=$POST
FAKE="clientEraseBlock:5>1=100 clientEraseBlock:6>1=100 clientEraseBlock:7>1=100 clientEraseBlock:8>1=100"
COMMON="--consistent --entry=clientEraseBlock:mode_client:126"
python wip/mc/s9/fdorun9.py $SLOT 129=$C 107=$C 108=$C 109=$C 110=$C 113=$C 116=$C 119=$C 120=$C 121=$C 128=$C 132=$C 112=$H 115=$H 117=1 130=1 49=7 55=2 61=1 126=1 127=1 125=1 $X --over mode_client:104\>105=$P $FAKE $COMMON "$@" 2>&1 | grep -v overrides
