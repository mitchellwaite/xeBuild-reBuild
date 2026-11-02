"""cp.py TAG POST 'tgt:depth,...' [site]: best_d + POST + compensation dead i-bcp gotos from loop top into post-loop labels.
targets: nm (then-branch of NO_MODE_ARG, before reboot test), nc (else netConnect), dtg, ndl"""
import sys,os,json
D=os.path.dirname(os.path.abspath(__file__)); import importlib.util as U
def L(n,p):
    s=U.spec_from_file_location(n,p); m=U.module_from_spec(s); s.loader.exec_module(m); return m
SA=L('sa64',os.path.join(D,'..','s64','sa.py')); X=L('exp61',os.path.join(D,'..','s61','exp.py'))
def cv(v,d,o): return ' && '.join('__builtin_constant_p(%s + %d)'%(v,o+k) for k in range(d))
def text(st,comp,site='top'):
    s=SA.text(st); gs=''
    for n,(t,d) in enumerate(comp):
        if d<=0: continue
        lab={'nm':'cpnm','nc':'cpnc','dtg':'dtg','ndl':'ndl','rb':'cprb'}[t]
        gs+='if (%s) goto %s;\n'%(cv('i',d,1700+20*n),lab)
    a='		if (__builtin_constant_p(mode + 130)) goto dtg;\n'; assert s.count(a)==1
    s=s.replace(a,a+'		cpnm: ;\n')
    a='		if (reboot) {\n			if (netConnect(ip)) {'; assert s.count(a)==1
    s=s.replace(a,'		cprb: if (reboot) {\n			if (netConnect(ip)) {')
    a='	} else {\n		if (netConnect(ip)) {\n			fkbo:'; assert s.count(a)==1
    s=s.replace(a,'	} else {\n		cpnc: if (netConnect(ip)) {\n			fkbo:')
    if site=='top':
        a='	for (i = 0; i < argc; i++) {\n'; assert s.count(a)==1; s=s.replace(a,a+gs)
    else:
        a='	for (i = 0; i < argc; i++) {\n'; s=s.replace(a,gs.replace('(i +','(argc +')+a)
    return s
if __name__=='__main__':
    st=json.load(open(sys.argv[5] if len(sys.argv)>5 else os.path.join(D,'..','s64','best_d.json'))); st['POST']=int(sys.argv[2])
    comp=[(p.split(':')[0],int(p.split(':')[1])) for p in sys.argv[3].split(',') if p]
    s=text(st,comp,sys.argv[4] if len(sys.argv)>4 else 'top')
    r=SA.T.es2.run(s,sys.argv[1],True)
    print(sys.argv[2:5],{k:r.get(k) for k in ('es2','per2','fncmp')} if r else r,flush=True)
    open(os.path.join(D,'o_%s.c'%sys.argv[1]),'w',newline='\n').write(s)
