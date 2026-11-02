import sys; sys.path.insert(0,'../s104'); import srch
for l in open(sys.argv[1]):
    p=l.split()
    try: o=list(map(int,p[3:]))
    except: continue
    print(p[0],p[1],'d=%d'%srch.dist(o),' '.join(p[3:]))
