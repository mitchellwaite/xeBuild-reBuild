# show.py DUMP : round-3-end pushes and round-4 ops per trace
import sys
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s86'); import r4sim
pre,g,first=r4sim.load(sys.argv[1])
i=max(j for j,e in enumerate(pre) if e[0]=='round')
print('r3 ops', [e for e in pre[i:] if e[0] in('push','ins') and e[-1]>-99][-40:])
for b in first: print(b, [e if e[0]!='ins' else (e[2],e[3]) for e in g[b] if e[0]!='visit'], 'V', [e[1] for e in g[b] if e[0]=='visit'])
