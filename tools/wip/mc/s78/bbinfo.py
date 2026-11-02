import re,sys
L=open(sys.argv[1]).read().split('\n')
i0=max(i for i,l in enumerate(L) if l.startswith('Final order:')); fo=L[i0+1].split()
# body after last 'Reordered sequence'
start=max(i for i,l in enumerate(L) if 'Reordered sequence' in l)
cur=None; info={}
for l in L[start:]:
    m=re.search(r'\[bb (\d+)\] NOTE_INSN_BASIC_BLOCK',l)
    if m: cur=m.group(1); info.setdefault(cur,[]); continue
    if cur is None: continue
    for s in re.findall(r'symbol_ref[^(]*\("([^"]+)"',l):
        if s not in info[cur]: info[cur].append(s)
    m=re.search(r'best78b?\w*\.c:(\d+)',l) or re.search(r'\.c:(\d+)',l)
    if m and ('L'+m.group(1)) not in info[cur] and len([x for x in info[cur] if x.startswith('L')])<1: info[cur].append('L'+m.group(1))
# freq from Reordered sequence
fr={}
for l in L[start:start+400]:
    m=re.match(r'\s*\d+ bb (\d+)\s+\[(\d+)\]',l)
    if m: fr[m.group(1)]=m.group(2)
for b in fo: print(b,fr.get(b,''),' '.join(info.get(b,[])))
print('=====')
seq=[]
for l in L[start:start+400]:
    m=re.match(r'\s*(\d+) (?:bb (\d+)|duplicate of (\d+))\s+\[(\d+)\]',l)
    if m: seq.append((m.group(1),m.group(2) or 'd'+m.group(3),m.group(4)))
for n,o,f in seq: print(n,o,f,' '.join(info.get(n,[])))
