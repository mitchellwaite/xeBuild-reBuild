# ins.py BASE OUT ANCHOR SNIPPET [before]: insert snippet after (or before) first occurrence of anchor
import sys
b,o,a,s=sys.argv[1:5]; t=open(b).read(); i=t.index(a)
if len(sys.argv)>5: t=t[:i]+s+t[i:]
else: t=t[:i+len(a)]+s+t[i+len(a):]
open(o,'w',newline='\n').write(t)
