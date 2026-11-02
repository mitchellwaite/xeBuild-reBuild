# gv.py BASE PFX : insert empty asm volatile before ('b') / after ('a') each AT(x) label
import sys,re
base,pfx=sys.argv[1],sys.argv[2]
s=open(base).read()
A='__asm__ volatile ("");'
for m in re.finditer(r'AT\((\w+)\)',s):
    if m.group(1)=='l': continue
    for f in 'ba':
        t=s[:m.start()]+A+' '+s[m.start():] if f=='b' else s[:m.end()]+' '+A+s[m.end():]
        n='%s_%s%s'%(pfx,m.group(1),f); open(n+'.c','w',newline='\n').write(t); print(n)
