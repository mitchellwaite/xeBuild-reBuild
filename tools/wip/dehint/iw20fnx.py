import re,sys
def fn(p,name):
    t=open(p,errors='replace').read()
    return re.search(r'^;; Function %s \(%s,.*?(?=^;; Function |\Z)'%(name,name),t,re.S|re.M).group(0)
name=sys.argv[3]
import difflib
a=fn(sys.argv[1],name);b=fn(sys.argv[2],name)
n=lambda s:[re.sub(r'_\d+','_N',l) for l in s.split('\n') if l.strip() and not l.startswith(';;   ')]
for l in list(difflib.unified_diff(n(a),n(b),lineterm='',n=0))[:80]: print(l[:110])
