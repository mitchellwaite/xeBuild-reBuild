"""r3.py tag: per raw bb in round-3 events show spmap name + key, match vs tag."""
import sys,os,re
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','s53')); import es2,es,hsim
import analyze
def show(sd,rnd=3):
    bbro,sp=analyze.spmap(sd)
    t=open(os.path.join(sd,'bbro_mc.txt')).read()
    a=t.find('STC - round %d'%rnd); b=t.find('STC - round %d'%(rnd+1)); seg=t[a:b if b>0 else len(t)]
    out=[]
    for line in seg.split('\n'):
        m=re.search(r'(Getting bb|start of next round:|start point of next round:|Changing key for bb) (\d+)(.*)',line)
        if m:
            n=int(m.group(2)); k=re.findall(r'-?\d+',m.group(3))
            out.append('%s %d=%s %s'%(m.group(1)[:3],n,sp.get(n,'?'),' '.join(k)))
    return out
if __name__=='__main__':
    rnd=int(sys.argv[2]) if len(sys.argv)>2 else 3
    A=show(os.path.join(es.R,'build','mcmatch','slotm'),rnd); B=show(os.path.join(es.R,'build','v','mc42','slot_'+sys.argv[1]),rnd)
    import itertools
    for x,y in itertools.zip_longest(A[:int(sys.argv[3]) if len(sys.argv)>3 else 45],B[:int(sys.argv[3]) if len(sys.argv)>3 else 45],fillvalue=''): print('%-45s | %s'%(x,y))
