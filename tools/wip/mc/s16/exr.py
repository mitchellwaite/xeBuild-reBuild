"""exr.py SLOT EXIT [k=v...]: best.json + exit + raw overrides; prints fncmp inv content and first diff hunk"""
import json,sys,os,subprocess
R=r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0,R+r'\tools\wip\mc\s15')
os.environ.setdefault('MCD',R+r'\build\mcpF')
import run
d=json.load(open(os.environ.get('BASE',R+r'\tools\wip\mc\s10\best.json')))
d['mode_client:104>105']=float(sys.argv[2])
for a in sys.argv[3:]:
    k,v=a.rsplit('=',1); d[k]=float(v)
f,inv,pre,o=run.run(sys.argv[1],d)
df=os.path.join(os.environ['MCD'],'slot'+sys.argv[1],'fdo.diff')
c=subprocess.run([sys.executable,R+r'\tools\wip\mc\s12\content.py',df],capture_output=True,text=True).stdout.strip()
h=[l for l in open(df) if l.startswith('@@')][:1]
print(sys.argv[2:],'fncmp',f,'inv',inv,'pre',pre,'content',c,'first',h[0].strip() if h else '-')
