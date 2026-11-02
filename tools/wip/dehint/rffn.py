"""fn.py <dumpfile> [fn]: print only the given function from a tree dump"""
import sys,re
t=open(sys.argv[1]).read()
fn=sys.argv[2] if len(sys.argv)>2 else 'readFileIn'
i=t.find(';; Function %s '%fn)
j=t.find('\n;; Function ',i+10)
print(t[i:j if j>0 else None])
