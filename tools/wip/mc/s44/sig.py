import sys,re
t=open(sys.argv[1]).read()
a=t.find(';; Function mode_client'); b=t.find('\n;; Function',a+10); t=t[a:b if b>0 else None]
bb=None; out=[]
for l in t.split('\n'):
    m=re.search(r'\[bb (\d+)\] NOTE_INSN_BASIC_BLOCK',l)
    if m: bb=m.group(1)
    m=re.search(r'symbol_ref[^(]*\("([^"]+)"',l)
    if m and bb: out.append(bb+':'+m.group(1))
print(' '.join(out))
