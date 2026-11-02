import sys, os
R = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, os.path.join(R, r'tools\wip\mc\s18'))
import hsim
Rr, keys = hsim.load(os.path.join(R, 'build', 'v', 'mc40', 'slot_' + sys.argv[1]))
for ri, r in enumerate(Rr, 1):
    print('R', ri, 'pre', r['pre'][:60])
    for b, ev in r['g'].items(): print('  g', b, ev)
