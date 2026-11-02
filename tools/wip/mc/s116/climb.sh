#!/bin/sh
# climb.sh ROUND EDITS... : singles on top of EDITS into rROUND, report best by f2+10*wrong
R=r$1; shift; mkdir -p $R
python - "$R" "$@" <<'PY'
import sys
R=sys.argv[1]; base=sys.argv[2:]
sys.argv=['comb.py']
exec(open('comb.py').read().split("if __name__")[0])
T=open('b0.c').read()
tg='c1 c2 c3 c7 c8 c9 c10 c11 c12 cdef hdd4 hdd5 i0 i1 p0 p1 s4 s5 t4 t5 dsp dtg ndl fail'.split()
for k,n in (('s',21),('n',32)):
  for i in range(n):
    for t in tg:
      nm='%s%02d_%s'%(k,i,t)
      if nm in base: continue
      try: open('%s/%s.c'%(R,nm),'w',newline='\n').write(apply(T,[parse(x) for x in base]+[(k,i,t)]))
      except IndexError: pass
PY
sh run.sh $R
for f in $R/*.mine; do b=${f%.mine}; s=$(grep " $b.c\$" $R/res.txt | cut -d' ' -f1); w=$(sh scan.sh $f | cut -c1-3); [ -z "$w" ] && w=000; nw=$(( (1-${w%??}) + (1-$(echo $w|cut -c2)) + (1-${w#??}) )); echo "$((s+10*nw)) $s $w $b"; done | sort -n > $R/cost.txt
head -5 $R/cost.txt
