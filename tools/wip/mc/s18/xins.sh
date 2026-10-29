# xins.sh EVALS name... : hanneal with every ordered subset of the arm targets injected at X2
EV=$1; shift
for v in "$@"; do
 for x in 131 118 114 131,118 118,131 131,114 114,131 118,114 114,118 131,118,114 131,114,118 118,131,114 118,114,131 114,131,118 114,118,131; do
  r=$(XINS=$x RXEV=117:130 START=des_sane.json python hanneal.py ../../../build/mc$v/slotv $EV 5 2>&1 | tail -2 | head -1)
  echo "$v $x ${r:0:16}"
  echo "$r" > xi_${v}_$x.out
  case "$r" in *" 0 {"*) echo FOUNDZERO $v $x;; esac
 done
done
