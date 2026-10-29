"""mckeys.py <variant.c> [gcc flags]: mcvar's round-4 order with each block's last heap key
and frequency (from the bbro dump), plus the wanted position."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mcvar
src = sys.argv[1]
flags = sys.argv[2:]
res, err = mcvar.run(src, flags)
if res is None: sys.exit(err)
d = res['dir']
bbro = mcvar.section(open(os.path.join(d, 'v.c.274r.bbro')).read(), 'mode_client')
cg = mcvar.section(open(os.path.join(d, 'v.c.267r.compgotos')).read(), 'mode_client')
sg = mcvar.sigs(cg, open(os.path.join(d, 'v.s')).read())
r4 = bbro.index('STC - round 4')
key = {}
for m in re.finditer(r'(?:Possible start (?:of (?:this|next) round|point of next round): (\d+) \(key: (-?\d+)\))|(?:Changing key for bb (\d+) from -?\d+ to (-?\d+))', bbro[:r4]):
    b = m.group(1) or m.group(3); k = m.group(2) or m.group(4)
    key[int(b)] = int(k)
freq = {}
for m in re.finditer(r'(\d+) \[(\d+)\]', ' '.join(re.findall(r'^Trace \d+ \(round \d+\):(.*)$', bbro, re.M))):
    freq[int(m.group(1))] = int(m.group(2))
pos = {s: i for i, s in enumerate(mcvar.WANT)}
print('inv=%d pre=%d' % (res['inv'], res['pre']))
for b in mcvar.order(bbro):
    s = sg.get(b)
    print('%4d %8s %4s  %-28s want %s' % (b, key.get(b), freq.get(b), s, pos.get(s, '')))
