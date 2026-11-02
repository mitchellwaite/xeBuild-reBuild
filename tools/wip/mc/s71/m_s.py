import os,re
STRIP=os.environ.get('TS','c12').split(',')
def mod(s):
    for L in STRIP:
        if not L: continue
        a=s.index('rok: __attribute__'); b=s.index('fkN: ;',a)
        seg=s[a:b]
        seg=re.sub(r', %s(?=[,)])'%L,'',seg)
        seg=re.sub(r'(ork\d+: goto) %s;'%L,r'\1 rkE;',seg)
        s=s[:a]+seg+s[b:]
    return s
