# red.py : greedy lever removal from climb1's inv-3 set, keep inv<=3, minimise fncmp
import sys
sys.argv=['climb2.py','b0.c','9','0']
exec(open('climb2.py').read().split('cur=set()')[0])
S=set(lev[i] for i in [1, 3, 5, 6, 9, 11, 14, 16, 17, 19, 20, 21, 23, 26, 27, 29, 30, 33, 34, 36, 38, 39, 40, 49, 53, 54, 55, 64, 65, 66, 71, 83, 89, 91, 93, 98, 101, 102, 103])
build(S,'rd'); cur=ev('rd'); print('start',cur,flush=True)
for p in sorted(S):
    T=S-{p}; build(T,'rd'); v=ev('rd'); print(lev.index(p),v,flush=True)
    if v[1]<=3 and v[0]<=cur[0]: S=T; cur=v
build(S,'rdbest'); print('final',cur,sorted(lev.index(p) for p in S))
