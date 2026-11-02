import re,sys
L=open(sys.argv[1]).read().split('\n')
st=max(i for i,l in enumerate(L) if l.startswith(';; Function mode_client'))
L=L[st:]
rs=min(i for i,l in enumerate(L) if l.startswith('Reordered sequence'))
mp={}
for l in L[rs+1:]:
  m=re.match(r'\s*(\d+) (bb (\d+)|duplicate of (\d+))',l)
  if not m: break
  mp[int(m.group(1))]=m.group(3) or ('d'+m.group(4))
cur=None; out=[]
rs2=max(i for i,l in enumerate(L) if l.startswith("Reordered sequence"))
for l in L[rs2:]:
  m=re.search(r'\[bb (\d+)\] NOTE_INSN_BASIC_BLOCK',l)
  if m: cur=int(m.group(1)); out.append([cur,[]]); continue
  if cur is None: continue
  m=re.search(r'symbol_ref:SI \("(\w+)"\)',l)
  if m and 'REG_CALL_DECL' not in l: out[-1][1].append(m.group(1))
  m=re.search(r'\(const_int (-?\d+) \[',l)
  if m and 'sp' in l: out[-1][1].append('#'+m.group(1))
for b,c in out: print(b,mp.get(b),' '.join(c))
