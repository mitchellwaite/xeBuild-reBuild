# mk.sh BASE NAME N [GUARD] : insert dead scaling loop after log_set_name in mode_client
cd $(dirname $0); b=$1; n=$2; N=$3; G=${4:-'__builtin_constant_p(argc) \&\& argc == 7'}
sed "0,/log_set_name(\"client\");/s//log_set_name(\"client\");\n\tif ($G) { int k_; for (k_ = 0; k_ < $N; k_++) __asm__ volatile(\"\"); }/" $b.c > v/$n.c
r=$(sh ../s101/f2.sh v/$n.c); echo "$n $r $b N=$N G=$G" | tee -a res.txt
