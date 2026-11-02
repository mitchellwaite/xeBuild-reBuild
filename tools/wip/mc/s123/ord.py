# ord.py: round-4 trace order of ours vs profiled (mapped to our block numbers)
import sys, re
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s86')
import r4sim
m = {}; 
for l in open('map.txt'):
    a, b = l.split()[:2]; m[int(b)] = int(a)
m[108] = 112
inv = {v: k for k, v in m.items()}
def traces(f):
    T = open(f).read(); out = []
    for mm in re.finditer(r'Trace (\d+) \(round (\d)\):(.*)', T):
        out.append((int(mm.group(1)), int(mm.group(2)), [int(x) for x in re.findall(r'(\d+) \[', mm.group(3))]))
    return out
if __name__ == '__main__':
    to = traces('dd/mc.bbro'); tp = traces('pf/mc.bbro')
    print('ours r4:'); 
    for t, r, bs in to:
        if r == 4: print(' T%d' % t, ' '.join(str(b) + ('' if b in inv else '*') for b in bs))
    print('prof r4 (mapped to ours; ?=unmapped):')
    for t, r, bs in tp:
        if r == 4: print(' T%d' % t, ' '.join(str(m.get(b, '?%d' % b)) for b in bs))
