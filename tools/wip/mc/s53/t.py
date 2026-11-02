"""t.py: apply named substitutions to c_t2A, run es, print per-round + R1 tail keys + R2 first traces."""
import sys,os,re,json
D=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.join(D,'..','s51'))
import es
B=open(os.path.join(D,'..','s52','c_t2A.c')).read()
def app(s,subs):
    for a,b in subs:
        assert a in s,a
        s=s.replace(a,b,1)
    return s
def info(tag):
    t=open(os.path.join(es.R,'build','v','mc42','slot_'+tag,'bbro_mc.txt')).read()
    r1=t[t.find('STC - round 1'):t.find('STC - round 2')]
    i=r1.find('Getting bb 37'); seg=r1[max(0,i-900):i]
    keys=re.findall(r'start of (?:this|next) round: (\d+) \(key: (-?\d+)\)',seg)
    r2=t[t.find('STC - round 2'):t.find('STC - round 3')]
    g=re.findall(r'Getting bb (\d+)',r2)[:6]
    return keys[-6:],g
def run(subs,tag,base=B,fn=False):
    r=es.run(app(base,subs),tag,fncmp=fn)
    if not r: return None,None
    try: k=info(tag)
    except Exception as e: k=repr(e)
    return r,k
