import sys,os,json,concurrent.futures as cf
sys.path.insert(0,r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s42')
os.environ['BASE']=r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s42\H5b.c'
import lev,ev,cm,tt
D=r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\build\v\mc43'
PINS=['__asm__("" :: "a"(i));','__asm__("" :: "d"(i + 1));','__asm__("" : "+a"(i));','__asm__("" :: "a"(i), "d"(i + 1));','__asm__("" : "+d"(i));']
mv=[tuple(c) for c in json.load(open('movers.json'))]
def run(x):
    c,pi=x; L=lev.make(*c).split('\n')
    k=[j for j,l in enumerate(L) if 'k55l: if (!strnicmp(argv[i], "-r"' in l][0]+1
    L[k]=PINS[pi]+' '+L[k]
    t=tt.tid(); p=os.path.join(D,'pm%d.c'%t); s='\n'.join(L); open(p,'w',newline='\n').write(s)
    r=ev.ev(s,'pm%d'%t,fncmp=False)
    if r is None: return dict(c=c,p=pi,err=1)
    return dict(c=c,p=pi,inv=r['tinv'],miss=r['tmiss'],cm=cm.cm(p) if r['tinv']<5 and not r['tmiss'] else None,o=r['o'])
C=[(c,p) for c in mv for p in range(len(PINS))]
with cf.ThreadPoolExecutor(4) as ex, open(sys.argv[1],'w') as f:
    for r in ex.map(run,C): f.write(json.dumps(r)+'\n'); f.flush()
