# mk4.sh BASE NAME T N [GUARD] : dead nested loop T x N in mode_client (scale ~ 9157/(100*T*N))
cd $(dirname $0); b=$1; n=$2; T=$3; N=$4; G=${5:-'__builtin_constant_p(argc)'}
sed "0,/log_set_name(\"client\");/s//log_set_name(\"client\");\n\tif ($G) { int k_, m_; for (k_ = 0; k_ < $T; k_++) for (m_ = 0; m_ < $N; m_++) __asm__ volatile(\"\"); }/" $b.c > v/$n.c
r=$(sh ../s101/f2.sh v/$n.c); echo "$n $r $b T=$T N=$N G=$G" | tee -a res.txt
