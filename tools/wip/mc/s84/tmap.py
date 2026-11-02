import re
def lines_after(L, start_pat, pat):
    s=next(i for i,l in enumerate(L) if start_pat in l)
    return next(i+1 for i in range(s,len(L)) if pat in L[i])
def target(src, order):
    L=open(src).read().split('\n')
    lm={'u2':lines_after(L,'AT(u2)','AT(u2)'),
        'wb3':lines_after(L,'wb3: client_usage','wb3: client_usage'),
        'wb4':lines_after(L,'wb3: client_usage','client_usage(4, argv[i])'),
        'wb5':lines_after(L,'wb3: client_usage','client_usage(5, argv[i])'),
        'eb5':lines_after(L,'"-eb"','client_usage(5'),
        'ip3':lines_after(L,'"-ip", 3','client_usage(3'),
        'c3':lines_after(L,'"-c", 2','client_usage(3'),
        'c5':lines_after(L,'"-c", 2','client_usage(5')}
    nm={'LC157':'inv','LC140':'-ip','LC142':'-r','LC144':'-w','LC146':'-e','LC148':'-c','LC118':'Blk','LC117':'Fer','LC114':'Inv','LC156':'hdd5','LC155':'hdd4','clientInfo':'Info','clientPatches':'Pat'}
    m={}
    for l in open(order):
        p=l.split(); toks=[x.lstrip('*_') for x in p[6:]]
        if p[1]!="old" or not p[2].isdigit(): continue
        b=int(p[2])
        for t in toks:
            if t in nm and (nm[t] not in m or nm[t] in ('Info','Pat')): m[nm[t]]=b
            if t.startswith('L') and t[1:].isdigit():
                for k,v in lm.items():
                    if v==int(t[1:]) and 'client_usage' in toks: m.setdefault(k,b)
    names=['inv','-ip','hdd5','hdd4','u2','-r','Blk','Fer','-w','wb4','wb3','-e','Inv','Pat','Info','wb5','eb5','ip3','c3','c5','-c']
    return [m[n] for n in names], m
if __name__=='__main__':
    import sys; print(target(sys.argv[1],sys.argv[2]))
