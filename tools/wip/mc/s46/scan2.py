import sys, os, json, re
from concurrent.futures import ThreadPoolExecutor
R=r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, os.path.join(R,r'tools\wip\mc\s42')); import m, tt
t=open('../s44/P.c').read()
L=t.split('\n')
r=[k for k,l in enumerate(L) if 'k55l: if (!strnicmp(argv[i], "-r", 2))' in l][0]
v=[k for k,l in enumerate(L) if '"-i", 2)) {' in l and k>r][0]
# arms -w,-e,-c : lines after the -r arm up to -i
for k in range(r+8, v):
    for n in (3,5):
        if L[k].strip()=='client_usage(%d, argv[i]);' % n: L[k]=L[k].replace('client_usage(%d, argv[i]);'%n,'goto wq%d;'%n)
a=[k for k,l in enumerate(L) if 'promptEnter = 0;' in l][0]
deads={'35':'\t\tif (0) { wq3: client_usage(3, argv[i]); wq5: client_usage(5, argv[i]); }','53':'\t\tif (0) { wq5: client_usage(5, argv[i]); wq3: client_usage(3, argv[i]); }'}
cands=[]
for k in range(a-30, r+1):
    if not re.search(r'[;{}]\s*$', L[k-1]) : continue
    for nm,d in deads.items(): cands.append((k,nm,'\n'.join(L[:k]+[d]+L[k:])))
def run(c):
    k, o, t = c
    rr = m.meas(t, 's46_%d' % tt.tid(), fncmp=True)
    return k, o, rr.get('inv'), rr.get('fncmp'), rr.get('order','')[:200] if 'err' not in rr else rr['err'][:100]
with ThreadPoolExecutor(6) as ex:
    for res in ex.map(run, cands): print(json.dumps(res), flush=True)
