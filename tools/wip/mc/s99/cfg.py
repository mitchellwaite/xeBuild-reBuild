# cfg.py DUMP N... : pred/succ of blocks from a pre-bbro -blocks-details dump (cfg/pre.txt)
import sys,re
t=open(sys.argv[1]).read()
cur=None; B={}; kind=None
for l in t.split('\n'):
    m=re.match(r';; basic block (\d+), loop depth \d+, count \d+, freq (\d+)',l)
    if m: cur=int(m.group(1)); B[cur]={'f':m.group(2),'p':[],'s':[]}; kind=None; continue
    m=re.match(r';;\s*(pred:|succ:)?\s+(\w+)(?: \[([\d.]+)%\])?\s*(?:count \d+)?\s*\(?([^)]*)',l)
    if m and cur is not None:
        if m.group(1): kind=m.group(1)[0]
        if kind: B[cur][kind].append((m.group(2),m.group(3),m.group(4)))
    elif not l.startswith(';;  ') : kind=None
if __name__=='__main__':
  for a in sys.argv[2:]:
    b=B[int(a)]; print(a,'f',b['f']); print('  P',b['p']); print('  S',b['s'])
