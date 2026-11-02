import re,os
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
