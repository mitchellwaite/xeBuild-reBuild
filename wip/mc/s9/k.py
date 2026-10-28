"""print round-4 keys of a profile slot: python k.py SLOTDIR"""
import sys, re
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\wip\mc'); import mcvar
d = sys.argv[1]
t = mcvar.section(open(d + '/m.c.274r.bbro').read(), 'mode_client')
cg = mcvar.section(open(d + '/m.c.267r.compgotos').read(), 'mode_client')
sg = mcvar.sigs(cg, open(d + '/fdo.s').read())
i = t.index('STC - round 4'); key = {}
for m in re.finditer(r'(?:Possible start (?:point )?of (?:next|this) round: (\d+) \(key: (-?\d+)\))|(?:Changing key for bb (\d+) from -?\d+ to (-?\d+))', t):
    key[int(m.group(1) or m.group(3))] = int(m.group(2) or m.group(4))
order = mcvar.order(t)
print(' '.join('%s=%s' % (sg.get(b, b), key.get(b)) for b in order if sg.get(b) in mcvar.WANT))
