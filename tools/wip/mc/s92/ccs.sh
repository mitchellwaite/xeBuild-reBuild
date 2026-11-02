B=$1; T=$2
for i in $(seq 0 29); do for d in -2 -1 1 2; do
 python cc.py $B.c ${T}_${i}_$d.c $i $d 2>/dev/null && sh ms.sh ${T}_${i}_$d | cut -c1-200
done; done
