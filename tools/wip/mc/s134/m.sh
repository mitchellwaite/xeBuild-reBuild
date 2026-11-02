# m.sh NAME SEDEXPR : apply sed to best34, f2
n=$1; shift; sed "$@" ${BASE:-best34.c} > v/$n.c; cp c0.ref v/$n.ref; cmp -s v/$n.c ${BASE:-best34.c} && { echo "$n NOCHANGE"; exit; }
r=$(sh ../s101/f2.sh v/$n.c); echo "$n $r | $*" | tee -a res.txt
