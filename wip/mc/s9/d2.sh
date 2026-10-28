#!/bin/sh
# usage: d2.sh SLOT X SMALL ERRPCT [extra design k=v ...] -- 9 tied cases at X, 128/116/132 at SMALL
export EXTRA='--param builtin-expect-probability=50'
SLOT=$1; X=$2; S=$3; P=$4; shift 4
FAKE="clientEraseBlock:5>1=100 clientEraseBlock:6>1=100 clientEraseBlock:7>1=100 clientEraseBlock:8>1=100"
COMMON="--consistent --entry=clientEraseBlock:mode_client:126"
python wip/mc/s9/fdorun9.py $SLOT 129=$X 107=$X 108=$X 109=$X 110=$X 113=$X 116=$S 119=$X 120=$X 121=$X 128=$S 132=$S 112=2 115=2 117=1 130=1 49=7 55=2 61=1 126=1 127=1 125=1 "$@" --over mode_client:115\>117=$P mode_client:118\>120=$P $FAKE $COMMON 2>&1 | grep -v overrides
