# rb.sh NAME BASE ebfile : replace clientEraseBlockI
python - $2 $1.tmp.c $3 <<'P'
import sys
s=open(sys.argv[1]).read(); a=s.index('static void clientEraseBlockI'); b=s.index('/* the option',a)
open(sys.argv[2],'w',newline='\n').write(s[:a]+open(sys.argv[3]).read()+s[b:])
P
sh r.sh $1 $1.tmp.c 'clientEraseBlockI(const char' 'clientEraseBlockI(const char'; rm -f $1.tmp.c
