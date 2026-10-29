"""6th session batch runner: python batch.py SPEC.py
SPEC.py defines VARS = [(name, [(old, new), ...]), ...] applied to the draft (or BASE file).
Prints per variant: fncmp lines, inv, pre, keys of usage2/HDD/Block/Failed/-r."""
import sys, subprocess, os, re
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, ROOT + r'\tools\wip\mc'); import mcvar
os.chdir(ROOT)
ns = {}; exec(open(sys.argv[1]).read(), ns)
base = open(ns.get('BASE', 'tools/wip/mode_client.c')).read()
os.makedirs('tools/wip/mc/s8', exist_ok=True)
def keys(r):
    t = mcvar.section(open(r['dir'] + '/v.c.274r.bbro').read(), 'mode_client')
    cg = mcvar.section(open(r['dir'] + '/v.c.267r.compgotos').read(), 'mode_client')
    sg = mcvar.sigs(cg, open(r['dir'] + '/v.s').read())
    i = t.index('STC - round 4'); key = {}
    for m in re.finditer(r'(?:Possible start (?:point )?of (?:next|this) round: (\d+) \(key: (-?\d+)\))|(?:Changing key for bb (\d+) from -?\d+ to (-?\d+))', t):
        key[int(m.group(1) or m.group(3))] = int(m.group(2) or m.group(4))
    want = {'usage:2': 'u2', 'log:cannot send avatar d': 'av', 'log:cannot send xbox com': 'xb', 'log:Block 0x%x is outsid': 'Bl', 'log:Failed to erase bloc': 'Fa', 'strnicmp:-r': '-r'}
    return ' '.join('%s%s' % (want[s], key.get(b)) for b, s in sorted(sg.items()) if s in want)
for name, reps in ns['VARS']:
    s = base
    ok = True
    for o, n in reps:
        if o not in s: print(name, 'NOAPPLY', o[:40]); ok = False; break
        s = s.replace(o, n, 1)
    if not ok: continue
    out = 'tools/wip/mc/s8/v_%s.c' % name
    open(out, 'w', newline='\n').write(s)
    r, e = mcvar.run(out, ['-O3', '--param', 'builtin-expect-probability=50'], fncmp=True)
    if r is None: print(name, 'ERR', e[:200]); continue
    print('%-10s f=%-4d inv=%-3d pre=%d  %s' % (name, r['fncmp'], r['inv'], r['pre'], keys(r)), flush=True)
