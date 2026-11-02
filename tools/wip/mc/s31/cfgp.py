"""cfgp.py TAG b1 b2 ...: preds/succs/calls of RTL blocks (compgotos) in slot_TAG."""
import sys, os
R = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
for p in (r'tools\wip\mc\s18', r'tools\wip\mc', r'tools\wip'): sys.path.insert(0, os.path.join(R, p))
import mcvar, analyze
sd = os.path.join(R, 'build', 'v', 'mc31', 'slot_' + sys.argv[1])
cg = mcvar.section(open(os.path.join(sd, 'm.c.267r.compgotos')).read(), 'mode_client')
blk = analyze.cfg(cg)
for b in sys.argv[2:]: print(b, blk.get(int(b)))
