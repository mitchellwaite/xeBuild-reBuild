# gg.sh NAME BASE SPEC... : gk + f2 + dump + fq
cd $(dirname $0); n=$1; b=$2; shift 2; python gk.py $b v/$n.c "$@" || exit 1
cp c0.ref v/$n.ref; r=$(sh ../s101/f2.sh v/$n.c); sh dump.sh $n >/dev/null 2>&1
k=$(python fq.py $n); echo "$n $r | $k | $b $*" >> res.txt; echo "$n $r | $k | $*"
