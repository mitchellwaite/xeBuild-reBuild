import re,sys
T0=open('b0.c').read()
def apply(src,edits):
    vs=[e for e in edits if e[0]=='s']; ws=[e for e in edits if e[0]=='n']
    for kind,i,t in vs:
        lines=src.split('\n'); start=sum(len(l)+1 for l in lines[:640])
        pat=re.compile(r'(__asm__ goto ?\("" :::: |JMP\()([a-z0-9_, ]+)\)')
        m=[m for m in pat.finditer(src) if m.start()>start][i]
        src=src[:m.end(2)]+', '+t+src[m.end(2):]
    lines=src.split('\n'); off=sum(len(l)+1 for l in lines[:736]); end=sum(len(l)+1 for l in lines[:792])
    pos=[m.start() for m in re.finditer(r'break;',src) if off<m.start()<end]
    pos+=[m.end() for m in re.finditer(r'AT\([a-z0-9]+\)',src) if off<m.start()<end]
    ins=sorted([(pos[i],t) for _,i,t in ws],reverse=True)
    for p,t in ins: src=src[:p]+'JMP(%s); '%t+src[p:]
    return src
def parse(name):
    m=re.match(r'([sn])(\d+)_(\w+)',name); return (m.group(1),int(m.group(2)),m.group(3))
if __name__=='__main__':
    out=sys.argv[1]; names=sys.argv[2:]
    open(out,'w',newline='\n').write(apply(T0,[parse(n) for n in names]))
