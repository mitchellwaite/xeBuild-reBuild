import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import t
NM='\tif (NO_MODE_ARG(mode, arg)) {\n\t\tif (reboot) {\n\t\t\tif (netConnect(ip)) {\n'
V={
'base':[],
'eNM':[(NM,'\tif (E(NO_MODE_ARG(mode, arg))) {\n\t\tif (reboot) {\n\t\t\tif (netConnect(ip)) {\n')],
'eRB':[(NM,'\tif (NO_MODE_ARG(mode, arg)) {\n\t\tif (E(reboot)) {\n\t\t\tif (netConnect(ip)) {\n')],
'eNC1':[(NM,'\tif (NO_MODE_ARG(mode, arg)) {\n\t\tif (reboot) {\n\t\t\tif (E(netConnect(ip))) {\n')],
'eNC2':[('\t} else {\n\t\tif (netConnect(ip)) {\n\t\t\tfkbo','\t} else {\n\t\tif (E(netConnect(ip))) {\n\t\t\tfkbo')],
'nNC1':[(NM,'\tif (NO_MODE_ARG(mode, arg)) {\n\t\tif (reboot) {\n\t\t\tif (!E(!netConnect(ip))) {\n')],
}
for k in sys.argv[1:]:
    r,i=t.run(V[k],'s53v1_'+k); print(k,r and (r['score'],r['es'],r['per']),i,flush=True)
