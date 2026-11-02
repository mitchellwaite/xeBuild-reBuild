import sys,os,cm,ev
D=os.path.dirname(os.path.abspath(__file__))
for f in sys.argv[1:]:
    p=os.path.join(D,f)
    c=cm.cm(p)
    r=ev.ev(open(p).read(),'r_'+f.replace('.','_'),fncmp=False)
    print(f,'cm',c,'inv',r and r['tinv'],'miss',r and r['tmiss'],flush=True)
