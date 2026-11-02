import sys,os,json,concurrent.futures as cf
sys.path.insert(0,r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s42')
import ev,cm,tt
D=r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\build\v\mc43'
L=open(sys.argv[1]).read().split('\n')
PINS=['__asm__("" :: "a"(i));','__asm__("" :: "d"(i));','__asm__("" :: "a"(i + 1));','__asm__("" :: "d"(i + 1));',
 '__asm__("" : "+a"(i));','__asm__("" : "+d"(i));','__asm__("" :: "a"(i), "d"(i + 1));','__asm__("" :: "d"(i), "a"(i + 1));',
 '__asm__("" :: "r"(i));','__asm__("" :: "m"(i));','__asm__("" :: "a"(a));','__asm__("" :: "d"(a));']
LINES=[int(x) for x in sys.argv[2].split(',')]
def run(c):
    ln,pi=c; M=list(L); M[ln-1]=M[ln-1].rstrip()+' '+PINS[pi] if M[ln-1].rstrip().endswith((';','{')) else PINS[pi]+' '+M[ln-1]
    t=tt.tid(); p=os.path.join(D,'ps%d.c'%t); s='\n'.join(M); open(p,'w',newline='\n').write(s)
    r=ev.ev(s,'ps%d'%t,fncmp=False)
    if r is None: return dict(c=c,err=1)
    return dict(c=c,inv=r['tinv'],miss=r['tmiss'],cm=cm.cm(p) if r['tinv']<5 else None,o=r['o'])
C=[(l,p) for l in LINES for p in range(len(PINS))]
with cf.ThreadPoolExecutor(4) as ex, open(sys.argv[3],'w') as f:
    for r in ex.map(run,C): f.write(json.dumps(r)+'\n'); f.flush(); print(r['c'],r.get('inv'),r.get('cm'),flush=True)
