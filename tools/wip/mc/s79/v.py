import sys
b,o=sys.argv[1],sys.argv[2]; s=open(b).read(); a=sys.argv[3:]
for i in range(0,len(a),2):
    assert s.count(a[i])==1,(a[i],s.count(a[i])); s=s.replace(a[i],a[i+1])
open(o,'w',newline='\n').write(s)
