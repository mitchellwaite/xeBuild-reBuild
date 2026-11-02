import sys
f=sys.argv[1]; sys.argv=['x',f,'0','0']
exec(open('wr2.py').read().split('random.seed')[0])
front2=[b for b in front]
def sc2(o):
    o=[b for b in o if b<900]; return score(o)
res=[]
r3i=max(i for i,e in enumerate(pre) if e[0]=='round')
for pos_ in range(r3i+1,len(pre)+1):
    for k in (-1000300,-5,-4,-3,-2,-1,0,1):
        p=list(pre); p.insert(pos_,('push',999,k))
        try: o=r4sim.sim(p,g,{}); res.append((sc2(o),pos_,k,o.index(999) if 999 in o else -1))
        except Exception as x: pass
# removals of pushes
for i in range(r3i+1,len(pre)):
    if pre[i][0]=='push':
        p=list(pre); del p[i]
        try: res.append((sc2(r4sim.sim(p,g,{})),'del',pre[i],0))
        except Exception: pass
# extra dummy inserted in round 4 groups
for x in first[:30]:
    for w in (0,99):
      for k in (-3,-2,-1,0,1):
        gg=dict(g); l=list(gg[x]); l.insert(min(w,len(l)),('ins','this',998,k)); gg[x]=l
        try: o=r4sim.sim(pre,gg,{}); res.append((sc2(o),'g',x,w,k))
        except Exception: pass
res.sort(key=lambda r:r[0])
for r in res[:25]: print(r if r[1] in('del','g') else (r[0],pre[r[1]] if r[1]<len(pre) else 'end',r[2],r[3]))
