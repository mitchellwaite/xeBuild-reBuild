"""tr.py TAG [all]: round-3/4 traces of slot_TAG with block names (sp numbers / calls), keys at pop."""
import sys, re, os
R = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
for p in (r"tools\wip\mc\s18", r"tools\wip\mc", r"tools\wip"): sys.path.insert(0, os.path.join(R, p))
import mcvar, analyze
sd = os.path.join(R, 'build', 'v', 'mc35', 'slot_' + sys.argv[1])
bbro, sp = analyze.spmap(sd)
cg = mcvar.section(open(os.path.join(sd, 'm.c.267r.compgotos')).read(), 'mode_client')
blk = analyze.cfg(cg)
def nm(b):
    s = sp.get(b)
    c = blk.get(b, {}).get('calls', [])
    t = str(b)
    if s is not None: t += '=' + str(s)
    if c: t += '(' + c[0][:8] + ')'
    return t
for l in bbro.splitlines():
    m = re.match(r'Trace (\d+) \(round (\d)\):(.*)', l)
    if m and (m.group(2) in '34' or len(sys.argv) > 2):
        bs = re.findall(r'(\d+) \[(\d+)\]', m.group(3))
        print('T%s r%s: ' % (m.group(1), m.group(2)) + ' '.join('%s[%s]' % (nm(int(b)), f) for b, f in bs))
