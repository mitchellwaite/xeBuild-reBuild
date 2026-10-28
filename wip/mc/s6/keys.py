"""python keys.py variant.c : round-4 trace starts with their last heap key and signature"""
import sys, re, os
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\wip\mc'); import mcvar
r, e = mcvar.run(sys.argv[1], ['-O3', '--param', 'builtin-expect-probability=50'])
t = mcvar.section(open(r['dir'] + '/v.c.274r.bbro').read(), 'mode_client')
cg = mcvar.section(open(r['dir'] + '/v.c.267r.compgotos').read(), 'mode_client')
sg = mcvar.sigs(cg, open(r['dir'] + '/v.s').read())
i = t.index('STC - round 4'); key = {}
for m in re.finditer(r'(?:Possible start (?:point )?of (?:next|this) round: (\d+) \(key: (-?\d+)\))|(?:Changing key for bb (\d+) from -?\d+ to (-?\d+))', t[:t.index('Final order') if 'Final order' in t else len(t)]):
    if m.start() > i and m.group(1) is None and m.group(3) is None: continue
    b = m.group(1) or m.group(3); key[int(b)] = int(m.group(2) or m.group(4))
    if m.start() > i: pass
out = []
for m in re.finditer(r'^Getting bb (\d+)\n(Basic block \1 was visited)?', t[i:], re.M):
    if m.group(2):
        b = int(m.group(1)); out.append('%s[%s]%s' % (b, key.get(b), ('=' + sg[b]) if sg.get(b) else ''))
print(' '.join(out))
