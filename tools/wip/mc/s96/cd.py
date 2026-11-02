# cd.py BASE TAG start_counts : coordinate descent over dsp goto counts (0..4) by (fncmp,inv)
import sys,subprocess
b,TAG,cs=sys.argv[1],sys.argv[2],list(map(int,sys.argv[3].split(',')))
def ev(c):
    subprocess.run(['python','dc.py',b,TAG+'.c',','.join(map(str,c))],check=True)
    f=int(subprocess.run(['sh','f.sh',TAG+'.c'],capture_output=True,text=True).stdout.strip())
    subprocess.run(['sh','dd.sh',TAG+'.c'],capture_output=True)
    iv=subprocess.run(['python','inv.py',TAG],capture_output=True,text=True).stdout.strip()
    try: iv=int(iv.split('=')[1])
    except: iv=99
    return f,iv
best=ev(cs); print('start',best,flush=True)
for rnd in range(2):
  imp=False
  for j in range(12):
    for v in range(5):
        if v==cs[j]: continue
        nx=cs[:]; nx[j]=v; r=ev(nx); print(j,v,r,flush=True)
        if r<best: best,cs,imp=r,nx,True
  if not imp: break
print('BEST',best,','.join(map(str,cs)))
