# gen.py BASE OUT pat n repl [pat n repl ...]: replace nth (0-based) occurrence
import sys
s=open(sys.argv[1]).read(); a=sys.argv[3:]
for k in range(0,len(a),3):
    p,n,r=a[k],int(a[k+1]),a[k+2]; idx=-1
    for _ in range(n+1):
        idx=s.find(p,idx+1); assert idx>=0,(p,n)
    s=s[:idx]+r+s[idx+len(p):]
open(sys.argv[2],'w',newline='\n').write(s)
