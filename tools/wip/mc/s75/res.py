import re,sys
t=open(sys.argv[1]).read().split('\n')
lc={}
for i,l in enumerate(t):
    m=re.match(r'(LC\d+):',l)
    if m:
        m2=re.search(r'\.ascii "(.*)"',t[i+1]); lc[m.group(1)]=m2.group(1)[:40] if m2 else '?'
on=False
for l in t:
    if l.startswith('_mode_client:'): on=True
    elif on and re.match(r'\s*\.(def|globl|ident)\b',l): break
    if on: print(re.sub(r'OFFSET FLAT:(LC\d+)',lambda m:'"%s"'%lc[m.group(1)],l))
