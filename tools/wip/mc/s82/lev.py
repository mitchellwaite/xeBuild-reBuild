import sys, subprocess, random, json, os
B=open('b0.c').read()
def bc(base,n,typ=0):
    if n==0: return None
    if typ: return ' && '.join('(char *)__builtin_constant_p(i + %d) == (char *)1'%(base+k) for k in range(n))
    return ' && '.join('__builtin_constant_p(i + %d)'%(base+k) for k in range(n))
U2='if (__builtin_constant_p(i + 320) && __builtin_constant_p(i + 321)) goto u2;'
K55='if ((char *)__builtin_constant_p(i + 30) == (char *)1 && (char *)__builtin_constant_p(i + 30 + 1) == (char *)1) goto k55l;'
WB3='if ((char *)__builtin_constant_p(i + 60) == (char *)1 && (char *)__builtin_constant_p(i + 61) == (char *)1) goto wb3;'
LU1='if ((char *)__builtin_constant_p(i + 10) == (char *)1 && (char *)__builtin_constant_p(i + 10 + 1) == (char *)1) goto lu1;'
K67='if ((char *)__builtin_constant_p(i + 40) == (char *)1 && (char *)__builtin_constant_p(i + 41) == (char *)1 && (char *)__builtin_constant_p(i + 42) == (char *)1) goto k67l;'
K61='if ((char *)__builtin_constant_p(i + 20) == (char *)1 && __builtin_constant_p(i + 20 + 1) == 3) goto k61l;'
CU4='				client_usage(4, argv[i]); }\n			start = b;'
CU4L='				{ wb4: client_usage(4, argv[i]); } }\n			start = b;'
ES=r'esucc: log_printf(0, "Success!\n"); }'
EE='eerase: log_printf(0, "erasing block 0x%x...", block);'
def feed(base,n,lab,typ=1):
    c=bc(base,n,typ); return '' if c is None else 'if (%s) goto %s;'%(c,lab)
L={ 'u2':[2,1,3,0], 'k55':[2,3,1,4], 'wb3':[2,1,3,4], 'wb4':[0,2,3,4,5], 'es':[0,1,2], 'ee':[0,1,2,3], 'k67':[3,2,4,5], 'k61':[1,0], 'lu1':[2,1,3,0], 'ip3':[0,1,2,3,4], 'c3':[0,1,2,3,4], 'c5':[0,1,2,3,4], 'eb5':[0,1,2,3,4], 'wb5':[0,1,2,3,4]}
def make(ch):
    s=B
    def rep(o,n):
        nonlocal s; assert s.count(o)==1,o; s=s.replace(o,n)
    rep(U2, feed(320,ch['u2'],'u2',0) + ('' if ch['wb4']==0 else ' '+feed(340,ch['wb4'],'wb4',0)))
    if ch['wb4']: rep(CU4,CU4L)
    rep(K55, feed(30,ch['k55'],'k55l'))
    rep(WB3, feed(60,ch['wb3'],'wb3'))
    rep(LU1, feed(10,ch['lu1'],'lu1'))
    rep(K67, feed(40,ch['k67'],'k67l'))
    if ch['k61']==0: rep(K61,'')
    if ch['es']: rep(ES,r'esucc: if (%s) goto efail; log_printf(0, "Success!\n"); }'%' && '.join('__builtin_constant_p(block + %d)'%(7+k) for k in range(ch['es'])))
    if ch['ee']: rep(EE,'eerase: if (%s) goto eout; log_printf(0, "erasing block 0x%%x...", block);'%' && '.join('__builtin_constant_p(block + %d)'%(7+k) for k in range(ch['ee'])))
    for key,anchor,pat,base in (('ip3','"-ip", 3','client_usage(3, argv[i]);',360),('c3','"-c", 2','client_usage(3, argv[i]);',380),('c5','"-c", 2','client_usage(5, argv[i]);',400),('eb5','"-eb", 3','client_usage(5, argv[i]);',420),('wb5','"-wb", 3','client_usage(5, argv[i]);',440)):
        if ch.get(key,0):
            a=s.index(anchor); k=s.index(pat,a); lab='L'+key
            s=s[:k]+'{ %s: %s }'%(lab,pat)+s[k+len(pat):]
            hook='goto u2;' if ch['u2'] else 'goto wb3;'
            h=s.index(hook)+len(hook)
            s=s[:h]+' '+feed(base,ch[key],lab,0)+s[h:]
    return s
def ev(ch,name):
    open(name+'.c','w',newline='\n').write(make(ch))
    c=subprocess.run(['sh','f.sh',name+'.c'],capture_output=True,text=True).stdout.strip()
    subprocess.run(['sh','dd.sh',name+'.c'],capture_output=True)
    t=subprocess.run(['python','tail.py','d/%s/order.txt'%name],capture_output=True,text=True).stdout.strip()
    return int(c), t
if __name__=='__main__':
    cur={k:v[0] for k,v in L.items()}
    for kv in sys.argv[2:]:
        k,v=kv.split('='); cur[k]=int(v)
    print(ev(cur,sys.argv[1]))
def inv(name):
    from tmap import target
    try: T,_=target(name+'.c','d/%s/order.txt'%name)
    except Exception: return 999
    pos={b:i for i,b in enumerate(T)}; seen=[]
    for l in open('d/%s/order.txt'%name):
        p=l.split()
        if len(p)>2 and p[1]=='old' and p[2].isdigit() and int(p[2]) in pos and int(p[2]) not in seen: seen.append(int(p[2]))
    q=[pos[b] for b in seen]
    return sum(1 for i in range(len(q)) for j in range(i+1,len(q)) if q[i]>q[j])
