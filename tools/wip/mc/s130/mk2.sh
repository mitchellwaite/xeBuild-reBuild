# mk2.sh BASE NAME M GUARD : dead nested scaling loop (outer 10000, inner M)
cd $(dirname $0); b=$1; n=$2; M=$3; G=$4
sed "0,/log_set_name(\"client\");/s//log_set_name(\"client\");\n\tif ($G) { int k_, m_; for (k_ = 0; k_ < 10000; k_++) for (m_ = 0; m_ < $M; m_++) __asm__ volatile(\"\"); }/" $b.c > v/$n.c
r=$(sh ../s101/f2.sh v/$n.c); echo "$n $r $b M=$M G=$G" | tee -a res.txt
