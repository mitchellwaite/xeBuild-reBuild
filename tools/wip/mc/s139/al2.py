import sys,difflib,re
def ld(f):
    r=[]
    for l in open(f):
        t=l.split()
        if not t: continue
        sig=' '.join(x for x in t[6:] if not re.match(r'L\d+$',x))
        r.append(dict(new=t[0],old=t[2],tr=t[3],f=t[5],sig=sig))
    return r
a=ld('../s111/pf/bbinfo.txt'); b=ld('dd/vEa/bbinfo.txt')
sm=difflib.SequenceMatcher(None,[x['sig'] for x in a],[x['sig'] for x in b],autojunk=False)
M={}
for op,i1,i2,j1,j2 in sm.get_opcodes():
    if op=='equal':
        for k in range(i2-i1): M[a[i1+k]['old']]=b[j1+k]['old']
# move-matched: unique sig among unmatched
ua=[x for x in a if x['old'] not in M]; mb=set(M.values()); ub=[x for x in b if x['old'] not in mb]
for x in ua:
    c=[y for y in ub if y['sig']==x['sig'] and x['sig']]
    if len(c)==1: M[x['old']]=c[0]['old']
import json; json.dump(M,open('map.json','w'))
# P r4 trace heads in emitted order
seen=set();heads=[]
for x in a:
    if x['tr'].endswith('r4') and x['tr'] not in seen: seen.add(x['tr']); heads.append(x)
print('P r4 heads (P old -> V old):')
print(' '.join(f"{h['old']}->{M.get(h["old"],"?")}" for h in heads))
seen=set();vh=[]
for x in b:
    if x['tr'].endswith('r4') and x['tr'] not in seen: seen.add(x['tr']); vh.append(x['old'])
print('V r4 heads:',' '.join(map(str,vh)))
