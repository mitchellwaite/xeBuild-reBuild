import sys,os,difflib; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','s51')); import es
T=es.toks(os.path.join(es.R,'build','v','mc42','slot_'+sys.argv[1]))
for r in map(int,sys.argv[2:] or ['2']):
    a,b=es.M[r],T[r]
    sm=difflib.SequenceMatcher(None,a,b,autojunk=False)
    for op,i1,i2,j1,j2 in sm.get_opcodes():
        if op!='equal': print(r,op,i1,'M:',' '.join(a[max(0,i1-2):i2]),'| T:',' '.join(b[max(0,j1-2):j2]))
