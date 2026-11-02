import re,sys
L=open(sys.argv[1]).read().split('\n')
rs=[i for i,l in enumerate(L) if l.startswith('Reordered sequence')]
def seq(i):
    d={};
    for l in L[i+1:i+400]:
        m=re.match(r'\s*(\d+) (?:bb (\d+)|duplicate of (\d+)|compensation)\s+\[(\d+)\]',l)
        if m: d[int(m.group(1))]=(m.group(2) or (("d"+m.group(3)) if m.group(3) else "c0"),m.group(4))
        elif d: break
    return d
s1=seq(rs[0]); s2=seq(rs[-1])
tr={}
for l in L:
    m=re.match(r'Trace (\d+) \(round (\d)\):(.*)',l)
    if m:
        for b in re.findall(r'(\d+) \[',m.group(3)): tr[b]=m.group(1)+'r'+m.group(2)
cur=None; info={}
for l in L[rs[-1]:]:
    m=re.search(r'\[bb (\d+)\] NOTE_INSN_BASIC_BLOCK',l)
    if m: cur=int(m.group(1)); info[cur]=[]; continue
    if cur is None: continue
    for s in re.findall(r'symbol_ref[^(]*\("([^"]+)"',l):
        if s not in info[cur]: info[cur].append(s)
    m=re.search(r'\.c:(\d+)',l)
    if m and not any(x.startswith('L') for x in info[cur]): info[cur].append('L'+m.group(1))
for n in sorted(s2):
    r,f=s2[n]; o=s1.get(int(r.lstrip('d')),('?','?'))[0] if r[0] not in 'dc' else r
    print(n,'old',o,'T'+tr.get(o.lstrip('d'),'?'),'f',f,' '.join(info.get(n,[])))
