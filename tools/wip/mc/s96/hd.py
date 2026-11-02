# hc.py BASE PREFIX N SEED : hill-climb permutation of dead-goto ifs on line PREFIX by fncmp then inv
import sys,subprocess,random
b,pre,N,seed=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4])
random.seed(seed)
TAG='hd'+str(seed)
def ev(idx,name=None):
    name=name or TAG
    subprocess.run(['python','pf.py',b,name+'.c',pre,','.join(map(str,idx))],stderr=subprocess.DEVNULL,check=True)
    c=int(subprocess.run(['sh','f.sh',name+'.c'],capture_output=True,text=True).stdout.strip())
    subprocess.run(['sh','dd.sh',name+'.c'],capture_output=True)
    iv=subprocess.run(['python','inv.py',name],capture_output=True,text=True).stdout.strip()
    try: iv=int(iv.split('=')[1])
    except: iv=99
    return c,iv
n=int(subprocess.run(['python','pf.py',b,TAG+'.c',pre,'rev'],capture_output=True,text=True).stderr.strip())
cur=list(range(n)) if len(sys.argv)<6 else list(map(int,sys.argv[5].split(","))); KI=len(sys.argv)>6
key=lambda r:(r[1],r[0]) if KI else r
best=ev(cur); print('start',best,flush=True)
for t in range(N):
    nx=cur[:]
    if random.random()<.5:
        a,c=random.sample(range(n),2); nx[a],nx[c]=nx[c],nx[a]
    else:
        a=random.randrange(n); x=nx.pop(a); nx.insert(random.randrange(n),x)
    r=ev(nx)
    print(t,nx,r,flush=True)
    if key(r)<=key(best):
        cur,best=nx,r
        if r[0]==0: break
print('BEST',best,','.join(map(str,cur)))
