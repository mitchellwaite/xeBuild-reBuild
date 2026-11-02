# hl.py BASE SUBSTR K N SEED [maxpos] : climb label perm by (fncmp, inv)
import sys,subprocess,random
b,sub,K,N,seed=sys.argv[1],sys.argv[2],sys.argv[3],int(sys.argv[4]),int(sys.argv[5])
random.seed(seed); TAG='hl'+str(seed)
def ev(idx):
    subprocess.run(['python','lp.py',b,TAG+'.c',sub,K,','.join(map(str,idx))],stderr=subprocess.DEVNULL,check=True)
    c=int(subprocess.run(['sh','f.sh',TAG+'.c'],capture_output=True,text=True).stdout.strip())
    subprocess.run(['sh','dd.sh',TAG+'.c'],capture_output=True)
    iv=subprocess.run(['python','inv.py',TAG],capture_output=True,text=True).stdout.strip()
    try: iv=int(iv.split('=')[1])
    except: iv=99
    return c,iv
n=int(subprocess.run(['python','lp.py',b,TAG+'.c',sub,K,'rev'],capture_output=True,text=True).stderr.strip())
M=int(sys.argv[6]) if len(sys.argv)>6 else n
cur=list(range(n)); best=ev(cur); print('start',best,flush=True)
for t in range(N):
    nx=cur[:]
    a,c=random.sample(range(M),2)
    if random.random()<.5: nx[a],nx[c]=nx[c],nx[a]
    else: x=nx.pop(a); nx.insert(c,x)
    r=ev(nx); print(t,nx,r,flush=True)
    if r<=best: cur,best=nx,r
    if r[0]==0: break
print('BEST',best,','.join(map(str,cur)))
