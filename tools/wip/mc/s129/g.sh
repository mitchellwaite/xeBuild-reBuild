cd $(dirname $0); n=$1; shift; python gen.py $n "$@" && r=$(sh ../s101/f2.sh v/$n.c) && echo "$n $r $*" >> res.txt && echo "$n $r $*"
