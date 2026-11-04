"""attempt 21: which Dempster-Shafer combinations of predictor values land P(partial arm) on imgAdd's grid.
Grid: round(900 * P) % 10 == 0 with 56 <= P <= 85 (attempt 20's expect probes). Values: tree-level hitrates
measured in profile_estimate dumps (see the notes); gcc's combine is integer arithmetic on base 10000 and this is
floating point, so anything within 0.5 of a grid line needs checking by compiling."""
import itertools, sys
V = {'pos+':73,'pos-':27,'ne+':72,'ne-':28,'call_else':71,'call_arm':29,'ret_else':61,'ret_arm':39,'const_else':67,'const_arm':33}
def comb(ps):
    a=b=1.0
    for p in ps:
        a*=p/100; b*=1-p/100
    return a/(a+b)
seen={}
names=list(V)
for n in range(1,5):
    for c in itertools.combinations_with_replacement(names,n):
        if ('pos+' in c and 'pos-' in c) or ('ne+' in c and 'ne-' in c): continue
        if sum(x.startswith(('pos','ne')) for x in c)>1: continue
        P=comb([V[x] for x in c])
        f=900*P
        if 0.56<=P<=0.85 and abs(f-round(f/10)*10)<0.5:
            print('%6.2f %6.1f %s'%(P*100,f,' '.join(c)))
