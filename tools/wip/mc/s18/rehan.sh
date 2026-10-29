# rehan.sh EVALS SEED name... : hanneal (current constraints) on existing variant histories
EV=$1; SD=$2; shift 2
for v in "$@"; do
  r=$(RXEV=117:130 START=des_sane.json python hanneal.py ../../../build/mc$v/slotv $EV $SD 2>&1 | tail -2 | head -1)
  echo "$v ${r:0:20}"
  echo "$r" > rh_$v.out
done
