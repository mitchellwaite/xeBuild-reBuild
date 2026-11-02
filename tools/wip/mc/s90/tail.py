import sys
N={'LC157':'inv','LC140':'-ip','LC142':'-r','LC144':'-w','LC146':'-e','LC148':'-c','LC150':'-i','LC152':'-p','LC154':'-v','LC118':'Blk','LC117':'Fer','LC114':'Inv','LC156':'hdd5','LC155':'hdd4','clientInfo':'Info','clientPatches':'Pat','client_usage':'CU'}
on=False;out=[];last=None
for l in open(sys.argv[1]):
    p=l.split()
    if len(p)<6: continue
    toks=[x.lstrip('*_') for x in p[6:]]
    if 'LC157' in toks: on=True
    if not on: continue
    if p[3]==last: continue
    last=p[3]
    nm=[N[x] for x in toks if x in N]
    out.append('%s%s:%s'%(nm[0] if nm else '',p[2] if nm and nm[0] in('CU','Info','Pat') else '',p[5]))
    pass
print(' '.join(out))
