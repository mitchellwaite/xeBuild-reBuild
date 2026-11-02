#!/bin/sh
# pairs.sh OUT N UNIQ BASE... : all pairs of the top N distinct edits in UNIQ on top of BASE
O=$1; N=$2; U=$3; shift 3; mkdir -p $O
python - "$O" "$N" "$U" "$@" <<'PY'
import sys,itertools
O,N,U=sys.argv[1],int(sys.argv[2]),sys.argv[3]; base=sys.argv[4:]
sys.argv=['comb.py']
exec(open('comb.py').read().split("if __name__")[0])
T=open('b0.c').read()
ed=[l.split()[4].split('/')[-1] for l in open(U).read().split('\n')[:N] if l]
for a,b in itertools.combinations(ed,2):
  if a.split('_')[0]==b.split('_')[0] and a[0]=='s': pass
  open('%s/%s+%s.c'%(O,a,b),'w',newline='\n').write(apply(T,[parse(x) for x in base+[a,b]]))
PY
sh run.sh $O
for f in $O/*.mine; do b=${f%.mine}; s=$(grep -F " $b.c" $O/res.txt | cut -d' ' -f1); w=$(sh scan.sh $f | cut -c1-3); [ -z "$w" ] && w=000; nw=$(( (1-${w%??}) + (1-$(echo $w|cut -c2)) + (1-${w#??}) )); echo "$((s+10*nw)) $s $w $b"; done | sort -n > $O/cost.txt
head -5 $O/cost.txt
