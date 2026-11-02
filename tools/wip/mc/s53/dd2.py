import sys,os,difflib; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import es2,es
T=es2.toks(os.path.join(es.R,'build','v','mc42','slot_'+sys.argv[1]))
for r in map(int,sys.argv[2:]):
    a,b=es2.M[r],T[r]
    print('R%d M:'%r,' '.join(a)); print('R%d T:'%r,' '.join(b))
