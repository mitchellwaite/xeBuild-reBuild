import sys,difflib,re
def ld(f):
    r=[]
    for l in open(f):
        t=l.split(); 
        if not t: continue
        sig=' '.join(x for x in t[6:] if not re.match(r'L\d+$',x))
        r.append((t[0],t[3],t[5],sig))
    return r
a=ld(sys.argv[1]); b=ld(sys.argv[2])
sm=difflib.SequenceMatcher(None,[x[3] for x in a],[x[3] for x in b],autojunk=False)
for op,i1,i2,j1,j2 in sm.get_opcodes():
    if op=='equal':
        for k in range(i2-i1):
            x=a[i1+k];y=b[j1+k]; m='' if x[2]==y[2] else ' *f'
            print(f"= P{x[0]:>4} {x[1]:7} f{x[2]:>5} | V{y[0]:>4} {y[1]:7} f{y[2]:>5}{m} {x[3]}")
    else:
        for x in a[i1:i2]: print(f"- P{x[0]:>4} {x[1]:7} f{x[2]:>5} {x[3]}")
        for y in b[j1:j2]: print(f"+                          V{y[0]:>4} {y[1]:7} f{y[2]:>5} {y[3]}")
