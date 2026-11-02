# g.sh NAME EDIT... : gen + f2 + dump + keys of window blocks
cd $(dirname $0); n=$1; shift; python gen.py $n "$@" || exit 1
cp c0.ref v/$n.ref; r=$(sh ../s101/f2.sh v/$n.c); sh dump.sh $n >/dev/null 2>&1
k=$(python fq.py $n)
echo "$n $r | $k | $*" >> res.txt; echo "$n $r | $k"
