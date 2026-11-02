n=$1; shift; python hk.py $n "$@"; cp c0.ref v/$n.ref; r=$(sh ../s101/f2.sh v/$n.c); echo "$n $r | hk $*" | tee -a res.txt
