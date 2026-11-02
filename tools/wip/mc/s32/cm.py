"""cm.py: content metric. full listings via fncmp context; multiset line diff + block multiset diff."""
import os, re, subprocess, sys
from collections import Counter
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
FL = ['-I'+os.path.join(ROOT,'src'),'-O3','-fno-toplevel-reorder','-fno-ipa-profile','-fno-reorder-functions','--param','builtin-expect-probability=50']
def sides(p):
    r = subprocess.run([sys.executable, os.path.join(ROOT,'tools/re/fncmp.py'), p, 'mode_client']+FL, capture_output=True, text=True, cwd=ROOT,
        env=dict(os.environ, FNCMP_LITERALS='1', FNCMP_CONTEXT='100000'))
    if 'MATCH' in r.stdout and '@@' not in r.stdout: return None, None
    a=[];b=[]
    for l in r.stdout.splitlines()[2:]:
        if l.startswith('@@'): continue
        if l.startswith('-'): a.append(l[1:])
        elif l.startswith('+'): b.append(l[1:])
        else: a.append(l[1:]); b.append(l[1:])
    return a,b
def blocks(x):
    out=[];cur=[]
    for l in x:
        cur.append(l)
        if l.startswith('jmp') or l.startswith('ret'): out.append(tuple(cur)); cur=[]
    out.append(tuple(cur)); return Counter(out)
def cm(p):
    a,b=sides(p)
    if a is None: return 0,0
    la,lb=Counter(a),Counter(b)
    ba,bb=blocks(a),blocks(b)
    return sum(((la-lb)+(lb-la)).values()), sum(((ba-bb)+(bb-ba)).values())
if __name__=='__main__':
    for p in sys.argv[1:]: print(p, cm(p))
