import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import t
A='\tif (NO_MODE_ARG(mode, arg)) {\n'
L=('\t} else {\n\t\tif (netConnect(ip)) {\n\t\t\tfkbo','\t} else {\n\t\tnc2: if (netConnect(ip)) {\n\t\t\tfkbo')
R='\t\tif (reboot) {\n'
BC='__builtin_constant_p(mode + %d)'
def cond(n,e):
    return ' && '.join(('E(%s)' if e else '%s')%(BC%(93+k)) for k in range(n))
V={}
for n in (1,2,3,4):
  for e in (0,1):
    V['pre%d%d'%(n,e)]=[(A,'\tif (%s) goto nc2;\n'%cond(n,e)+A),L]
    V['rb%d%d'%(n,e)]=[(R,'\t\tif (%s) goto nc2;\n'%cond(n,e)+R),L]
for k in sys.argv[1:]:
    r,i=t.run(V[k],'s53v3_'+k); print(k,r and (r['score'],r['es'],r['per']),i,flush=True)
