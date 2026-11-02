import re,sys
# bbmap.py DUMP.bbro X.s : print traces with block content tags
t=open(sys.argv[1]).read()
s=open(sys.argv[2]).read().split('\n')
lc={}
for i,l in enumerate(s):
    m=re.match(r'(LC\d+):',l)
    if m:
        m2=re.search(r'\.ascii "(.*)"',s[i+1]); lc['*'+m.group(1)]=(m2.group(1) if m2 else '?').replace('\12','').replace('*','')[:22]
fo=t.index('Final order:')
body=t[fo:]
tags={}
cur=None
for l in body.split('\n'):
    m=re.match(r';; basic block (\d+), loop depth',l) or re.match(r';;  ?basic block (\d+)',l)
    m=re.match(r'\(note \d+ \d+ \d+ (\d+) \[bb (\d+)\] NOTE_INSN_BASIC_BLOCK',l)
    if m: cur=int(m.group(2)); tags.setdefault(cur,[]); continue
    if cur is None: continue
    for n in re.findall(r'symbol_ref[^(]*\("([^"]+)"\)',l):
        n=lc.get(n,n)
        if n not in ('log_printf','cinfo') and n not in tags[cur]: tags[cur].append(n)
for l in t[:fo].split('\n'):
    m=re.match(r'Trace (\d+) \(round (\d+)\):(.*)',l)
    if m:
        bbs=re.findall(r'(\d+) \[(\d+)\]',m.group(3))
        print('T%s r%s: '%(m.group(1),m.group(2))+' | '.join('%s[%s]%s'%(b,f,','.join(tags.get(int(b),[]))[:40]) for b,f in bbs))
