#!/bin/sh
# usage: d.sh SLOT OTHERCASE HDDCASE HDDERR ERASECASE "extra design" [extra overrides]
export EXTRA='--param builtin-expect-probability=50'
SLOT=$1; O=$2; C=$3; H=$4; E=$5; X=$6; shift 6
FAKE="clientEraseBlock:5>1=100 clientEraseBlock:6>1=100 clientEraseBlock:7>1=100 clientEraseBlock:8>1=100"
COMMON="--consistent --entry=clientEraseBlock:mode_client:126"
python wip/mc/s9/fdorun9.py $SLOT 129=$O 107=$O 108=$O 109=$O 110=$C 113=$C 116=$O 119=$O 120=$O 121=$E 128=$O 132=$O 112=$H 115=$H 117=1 130=1 49=7 55=2 61=1 126=1 127=1 125=1 $X --over $FAKE $COMMON "$@" 2>&1 | grep -v overrides
