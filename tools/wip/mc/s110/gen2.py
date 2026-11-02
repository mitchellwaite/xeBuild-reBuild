import re,os
src=open('h0.c').read()
st=src.index('int mode_client(int argc'); 
def conds(s):
    out=[]
    for m in re.finditer(r'\b(if|while) \(',s):
        a=m.end()-1; d=0
        for j in range(a,len(s)):
            if s[j]=='(': d+=1
            elif s[j]==')':
                d-=1
                if d==0: break
        c=s[a+1:j]
        if '__builtin_constant_p' in c or 'asm' in c: continue
        out.append((a+1,j,c))
    return out
os.makedirs('v2',exist_ok=True)
cs=conds(src[st:]); n=0
for k,(a,b,c) in enumerate(cs):
    a+=st;b+=st
    if c.startswith('E('):
        inner=c[2:-1]; v=src[:a]+inner+src[b:]; open('v2/rmE_%02d.c'%k,'w',newline='\n').write(v); n+=1
    else:
        v=src[:a]+'__builtin_expect(!!(%s), 0)'%c+src[b:]; open('v2/x_%02d.c'%k,'w',newline='\n').write(v); n+=1
    # also wrap sub-terms of || / &&
    parts=re.split(r' (\|\||&&) ',c)
    if len(parts)>1 and not c.startswith('E('):
        for t in range(0,len(parts),2):
            p=list(parts); p[t]='__builtin_expect(!!(%s), 0)'%p[t]
            v=src[:a]+' '.join(p)+src[b:]; open('v2/t_%02d_%d.c'%(k,t//2),'w',newline='\n').write(v); n+=1
    print(k,c[:70])
print(n)
