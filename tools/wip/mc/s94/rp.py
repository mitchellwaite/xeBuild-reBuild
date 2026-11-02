import sys
b,o,a,s=sys.argv[1:5]; t=open(b).read(); assert a in t; t=t.replace(a,s,1); open(o,'w',newline='\n').write(t)
