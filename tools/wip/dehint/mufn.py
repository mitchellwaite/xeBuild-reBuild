"""Print one function's section of a gcc dump: python mufn.py <dump> <fn>"""
import re, sys
t = open(sys.argv[1]).read()
m = re.search(r'^;; Function %s \(' % sys.argv[2], t, re.M)
if not m: sys.exit('no function')
e = t.find('\n;; Function ', m.end())
sys.stdout.write(t[m.start():e if e > 0 else None])
