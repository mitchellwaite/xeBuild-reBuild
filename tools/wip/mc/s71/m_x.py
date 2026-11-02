import os,re
S70="C:/Users/Win11VM/Documents/GitHub/xebuildBugFix/tools/wip/mc/s70"; exec(open(S70+"/m_v.py").read().replace("os.path.dirname(os.path.abspath('m_w.py'))","S70"))
_m2=mod; STRIP=os.environ.get('TS','c10').split(',')
def mod(s):
    s=_m2(s)
    for L in STRIP:
        if not L: continue
        a=s.index('rok: __attribute__'); b=s.index('fkN: ;',a)
        seg=s[a:b]
        seg=re.sub(r', %s(?=[,)])'%L,'',seg)
        seg=re.sub(r'(ork\d+: goto) %s;'%L,r'\1 rkE;',seg)
        s=s[:a]+seg+s[b:]
    return s
