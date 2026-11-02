# grid.sh PREFIX : grid over lever groups on $BASE (default c0.c)
cd $(dirname $0); . ./vars.sh; n=0
P=$1
for a in - A E; do for b in - K Q; do for c in - K Q; do for d in - I P J; do for g in - G; do
 set -- "$MK"; shift 0
 case $a in A) set -- "$@" "$EK" "$EK2";; E) set -- "$@" "$E1";; esac
 case $b in K) set -- "$@" "$K7";; Q) set -- "$@" "$Q7";; esac
 case $c in K) set -- "$@" "$K12";; Q) set -- "$@" "$Q12";; esac
 case $d in I) set -- "$@" "$UL" "$FI";; P) set -- "$@" "$UL" "$FP";; J) set -- "$@" "$UL" "$FI0";; esac
 case $g in G) set -- "$@" "$PL";; esac
 nm=${P}_$a$b$c$d$g; sh g.sh $nm "$@" | cut -c1-200
done; done; done; done; done
