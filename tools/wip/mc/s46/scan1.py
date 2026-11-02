import sys, os, json, re
from concurrent.futures import ThreadPoolExecutor
R=r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, os.path.join(R,r'tools\wip\mc\s42')); import m, tt
base=open('A1.c').read()
dead='\t\tif (0) { rq3: client_usage(3, argv[i]); rq5: client_usage(5, argv[i]); }\n'
t0=base.replace(dead,'')
L=t0.split('\n')
a=[k for k,l in enumerate(L) if 'promptEnter = 0;' in l][0]; b=[k for k,l in enumerate(L) if 'client_usage(1, argv[i]); } } }' in l][0]
cands=[]
for k in range(a, b+2):
    for d in (dead, dead.replace('rq3: client_usage(3, argv[i]); rq5: client_usage(5, argv[i]);','rq5: client_usage(5, argv[i]); rq3: client_usage(3, argv[i]);')):
        if k <= b:  # insert as statement at line start only if previous line ends a statement
            if not re.search(r'[;{}]\s*$', L[k-1]): continue
        cands.append((k, d is dead, '\n'.join(L[:k]+[d.rstrip('\n')]+L[k:])))
def run(c):
    k, o, t = c
    r = m.meas(t, 's46_%d' % tt.tid(), fncmp=True)
    return k, o, r.get('inv'), r.get('fncmp'), r.get('order','')[:200] if 'err' not in r else r['err'][:100]
with ThreadPoolExecutor(6) as ex:
    for res in ex.map(run, cands):
        print(json.dumps(res), flush=True)
