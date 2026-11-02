import sys,re
t=open(sys.argv[1]).read()
a=t.find(';; Function mode_client'); b=t.find('\n;; Function',a+10); t=t[a:b if b>0 else None]
want=set(sys.argv[2:]); cur=None; buf=[]
ins=re.split(r'\n(?=\((?:insn|call_insn|jump_insn|note|code_label|barrier))',t)
for x in ins:
    m=re.search(r'\[bb (\d+)\] NOTE_INSN_BASIC_BLOCK',x)
    if m: cur=m.group(1)
    if cur in want and not x.startswith('(note'):
        s=' '.join(x.split()); s=re.sub(r'<[^>]*>','',s); s=re.sub(r'C:/\S+','',s)
        print(cur, s[:230])
