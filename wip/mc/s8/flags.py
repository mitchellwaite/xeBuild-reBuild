"""s8 flag sweep: python flags.py [SRC] -- prints fncmp/inv/pre/keys of the draft (or SRC) under extra flag sets."""
import sys, os, re
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, ROOT + r'\wip\mc'); import mcvar
os.chdir(ROOT)
src = sys.argv[1] if len(sys.argv) > 1 else 'wip/app/mode_client.c'
BASE = ['-O3', '--param', 'builtin-expect-probability=50']
SETS = [[]]
for v in (45, 48, 52, 55, 60):
    SETS.append(['--param', 'builtin-expect-probability=%d' % v])
for v in (10, 100, 300, 3000, 10000):
    SETS.append(['--param', 'hot-bb-frequency-fraction=%d' % v])
for v in (0, 1, 3, 4):
    SETS.append(['--param', 'predictable-branch-outcome=%d' % v])
SETS += [['-O2'], ['-fno-thread-jumps'], ['-fno-tree-dominator-opts'], ['-fno-guess-branch-probability']]
def keys(r):
    t = mcvar.section(open(r['dir'] + '/v.c.274r.bbro').read(), 'mode_client')
    cg = mcvar.section(open(r['dir'] + '/v.c.267r.compgotos').read(), 'mode_client')
    sg = mcvar.sigs(cg, open(r['dir'] + '/v.s').read())
    key = {}
    for m in re.finditer(r'(?:Possible start (?:point )?of (?:next|this) round: (\d+) \(key: (-?\d+)\))|(?:Changing key for bb (\d+) from -?\d+ to (-?\d+))', t):
        key[int(m.group(1) or m.group(3))] = int(m.group(2) or m.group(4))
    want = {'usage:2': 'u2', 'log:cannot send avatar d': 'av', 'log:cannot send xbox com': 'xb', 'log:Block 0x%x is outsid': 'Bl', 'log:Failed to erase bloc': 'Fa', 'strnicmp:-r': '-r'}
    return ' '.join('%s%s' % (want[s], key.get(b)) for b, s in sorted(sg.items()) if s in want)
for extra in SETS:
    fl = list(BASE)
    if extra[:1] == ['-O2']: fl[0] = '-O2'; extra = []
    fl += extra
    r, e = mcvar.run(src, fl, fncmp=True)
    if r is None: print(' '.join(fl), 'ERR', e[:200]); continue
    print('%-45s f=%-4d inv=%-3d pre=%d  %s' % (' '.join(fl[1:]), r['fncmp'], r['inv'], r['pre'], keys(r)), flush=True)
