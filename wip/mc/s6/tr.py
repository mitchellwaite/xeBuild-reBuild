import sys, re
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\wip\mc'); import mcvar
r, e = mcvar.run(sys.argv[1], ['-O3', '--param', 'builtin-expect-probability=50'])
t = mcvar.section(open(r['dir'] + '/v.c.274r.bbro').read(), 'mode_client')
for l in t.split('\n'):
    if l.startswith('Trace ') and '(round 4)' not in l: print(l[:300])
print(r['dir'])
