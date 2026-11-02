import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import t
R='\t\tif (reboot) {\n'
R2='\t\t\tif (netConnect(ip)) {\n\t\t\trok:'
BC='__builtin_constant_p(mode + %d)'
def cond(n,e): return ' && '.join(('E(%s)' if e else '%s')%(BC%(93+k)) for k in range(n))
TG={'nd':('\tnetDisconnect();\n\treturn 0;\nfail:','\tdtg: netDisconnect();\n\treturn 0;\nfail:'),
    'rr':('\tif (E(reboot))\n\t\tnetReboot','\tdtg: if (E(reboot))\n\t\tnetReboot'),
    'u2':('{ AT(u2) client_usage(2, NULL); }','{ AT(u2) dtg: client_usage(2, NULL); }'),
    'gi':('\t\t\trok: __attribute__((cold));\n\t\t\t\tcinfo','\t\t\trok: __attribute__((cold));\n\t\t\t\tdtg: cinfo')}
V={}
for tg in TG:
  for n in (1,2,3):
    for e in (0,1):
      V['%s_r%d%d'%(tg,n,e)]=[(R,'\t\tif (%s) goto dtg;\n'%cond(n,e)+R),TG[tg]]
      V['%s_c%d%d'%(tg,n,e)]=[(R2,'\t\t\tif (%s) goto dtg;\n'%cond(n,e)+R2),TG[tg]]
for k in (sys.argv[1:] or V):
    try: r,i=t.run(V[k],'s53v4_'+k)
    except AssertionError as x: print(k,'assert',x); continue
    print(k,r and (r['score'],r['es'],r['per']),i,flush=True)
