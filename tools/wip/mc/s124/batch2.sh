cd $(dirname $0); export BASE=b18N.c
K='strnicmp(argv[i], "-keys", 5)'
J='__asm__ goto ("" :::: klat);'
sh run1.sh N_P1 "({ int r_ = $K; $J !r_; })"
sh run1.sh N_P2 "({ int r_ = $K; $J $J !r_; })"
sh run1.sh N_Q1 "({ $J 0; }) || !$K"
sh run1.sh N_Q2 "({ $J $J 0; }) || !$K"
sh run1.sh N_A1 "!$K && ({ $J 1; })"
sh run1.sh N_A2 "!$K && ({ $J $J 1; })"
sh run1.sh N_PQ "({ $J 0; }) || ({ int r_ = $K; $J !r_; })"
