import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import t
NM='#define NO_MODE_ARG(m, a) (!((m) && (a)))'
NC='\t\tif (reboot) {\n\t\t\tif (netConnect(ip)) {\n'
EC=(NC,'\t\tif (reboot) {\n\t\t\tif (E(netConnect(ip))) {\n')
V={
'm1':[(NM,'#define NO_MODE_ARG(m, a) (!(E(m) && (a)))'),EC],
'm2':[(NM,'#define NO_MODE_ARG(m, a) (!((m) && E(a)))'),EC],
'm3':[(NM,'#define NO_MODE_ARG(m, a) (!(E(m) && E(a)))'),EC],
'm4':[(NM,'#define NO_MODE_ARG(m, a) (!(E(m) && (a)))')],
'm5':[(NM,'#define NO_MODE_ARG(m, a) (!((m) && E(a)))')],
'm6':[(NM,'#define NO_MODE_ARG(m, a) (!(E(!!(m)) && (a)))'),EC],
}
for k in sys.argv[1:]:
    r,i=t.run(V[k],'s53v2_'+k); print(k,r and (r['score'],r['es'],r['per']),i,flush=True)
