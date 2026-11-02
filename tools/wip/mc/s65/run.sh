cd /c/Users/Win11VM/Documents/GitHub/xebuildBugFix/tools/wip/mc/s65
B=../s64/best_d.json
PMIN=1 PMAX=2 PDR=0.2 python sa.py p1 3600 651 $B POST=2 > p1.log 2>&1 &
sleep 6; PMIN=1 PMAX=2 PDR=0.2 python sa.py p2 3600 652 $B POST=1 > p2.log 2>&1 &
sleep 6; PMIN=2 PMAX=2 python sa.py p3 3600 653 ../s62/best_b.json POST=2 > p3.log 2>&1 &
sleep 6; R3W=3 python sa.py f4 3600 654 $B > f4.log 2>&1 &
wait
