import sys
sys.argv=[sys.argv[0],sys.argv[1],'0','0']
exec(open('wr2.py').read().split('random.seed')[0])
base=score(run([]))
one=[]
for e in alle:
    try: one.append((score(run([e])),e))
    except Exception: pass
one.sort(key=lambda x:x[0]); print('base',base); 
for s,e in one[:8]: print(s,desc(e))
top=[e for s,e in one if s<=base+2][:300]
two=[]
import itertools
for a,b in itertools.combinations(top,2):
    try: two.append((score(run([a,b])),a,b))
    except Exception: pass
two.sort(key=lambda x:x[0])
for s,a,b in two[:15]: print(s,desc(a),'|',desc(b))
