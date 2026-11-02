cd $(dirname $0)
K='strnicmp(argv[i], "-keys", 5)'
for L in ks1 ks2 kn1 kip; do
sh run1.sh P1$L "({ int r_ = $K; __asm__ goto (\"\" :::: $L); !r_; })"
sh run1.sh P2$L "({ int r_ = $K; __asm__ goto (\"\" :::: $L); __asm__ goto (\"\" :::: $L); !r_; })"
sh run1.sh Q1$L "({ __asm__ goto (\"\" :::: $L); 0; }) || !$K"
done
