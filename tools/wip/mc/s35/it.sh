# it.sh NAME TH : table on st_NAME.json (tag NAME must be built) + 4 fit seeds
N=$1; TH=$2
XT=1 python tab3.py st_$N.json $N tab_$N.jsonl > tab_$N.err 2>&1
for s in 1 2 3 4; do TH=$TH python fit.py tab_$N.jsonl $N st_$N.json $s 30000 fit_${N}_$s.json 8 > fit_${N}_$s.log 2>&1 & sleep 4; done; wait
grep -h "REAL\|BEST" fit_${N}_*.log | sort -k4 -n | head -20
