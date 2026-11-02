# sw.py BASE OUT LIST_PREFIX i : swap items i,i+1 in comma list starting with prefix
import sys
b,o,p,i=sys.argv[1],sys.argv[2],sys.argv[3],int(sys.argv[4]); t=open(b).read(); a=t.index(p); e=t.index(')',a)
L=t[a:e].split(', ')
if i+1>=len(L): sys.exit(1)
L[i],L[i+1]=L[i+1],L[i]; t=t[:a]+', '.join(L)+t[e:]
open(o,'w',newline='\n').write(t)
