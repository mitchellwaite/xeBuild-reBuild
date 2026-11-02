"""cfg.py <dir> [pass ...]: compact CFG of readFileIn after a pass, plus registered threads"""
import sys,re,glob,os
d=sys.argv[1]; passes=sys.argv[2:]
for p in passes:
    fs=[f for f in glob.glob(d+'/a.c.*t.'+p)]
    t=open(fs[0]).read()
    i=t.find(';; Function readFileIn '); j=t.find('\n;; Function ',i+10); t=t[i:j if j>0 else None]
    print('=====',os.path.basename(fs[0]))
    for l in t.split('\n'):
        if re.search(r'Registering jump thread|Threaded jump|Cancelling',l): print(l.strip())
    k=t.rfind('\nreadFileIn (')
    body=t[k:]
    for blk in re.split(r'\n(?=;;   basic block )',body)[1:]:
        m=re.match(r';;   basic block (\d+).*?freq (\d+)',blk)
        ss=[]
        for l in blk.split('\n')[1:]:
            s=l.strip()
            if not s or s.startswith(';;') or s.startswith('goto') or s.startswith('else') or s=='}': continue
            ss.append(s)
        succ=re.findall(r';;\s+(?:succ:)?\s+(\d+|EXIT) \[?([\d.]*)%?\]?\s*\(?([A-Z_,]*)',blk[blk.find('succ:')-3:]) if 'succ:' in blk else []
        pr=re.findall(r'(?:pred:)?\s+(\d+|ENTRY) \[',blk[blk.find('pred:'):blk.find('\n  ',blk.find('pred:'))])
        print('bb%s f=%s <-%s -> %s'%(m.group(1),m.group(2),','.join(pr),' '.join('%s[%s]'%(a,b) for a,b,c in succ)))
        for s in ss: print('    ',s)
