# mk3.sh BASE NAME N GUARD : dead scaling loop inside clientEraseBlock (callee-local rounding)
cd $(dirname $0); b=$1; n=$2; N=$3; G=$4
sed "0,/uint32_t block = myatoh32(sblock, -1);/s//uint32_t block = myatoh32(sblock, -1);\n\tif ($G) { int k_, m_; for (k_ = 0; k_ < 10000; k_++) for (m_ = 0; m_ < $N; m_++) __asm__ volatile(\"\"); }/" $b.c > v/$n.c
r=$(sh ../s101/f2.sh v/$n.c); echo "$n $r $b callee N=$N G=$G" | tee -a res.txt
