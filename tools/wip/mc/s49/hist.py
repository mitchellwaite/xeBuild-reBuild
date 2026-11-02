"""hist.py SLOTDIR : print hsim round/group event history (named blocks)."""
import sys, os
R = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, os.path.join(R, r'tools\wip\mc\s18')); sys.path.insert(0, os.path.join(R, r'tools\wip'))
import hsim
Rr, keys = hsim.load(sys.argv[1])
for ri, r in enumerate(Rr, 1):
    print('R%d pre' % ri, ' '.join(('%s%s' % (x[0][0], x[1]) if x[0]!='ins' else 'i%s:%s' % (x[2], x[1][0])) for x in r['pre']))
    for b, es in r['g'].items():
        print('R%d g%s' % (ri, b), ' '.join(('%s%s' % (x[0][0], x[1]) if x[0]!='ins' else 'i%s:%s' % (x[2], x[1][0])) for x in es))
