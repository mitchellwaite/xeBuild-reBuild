"""python tools/wip/dehint/nrone.py <generator.py> <exact tag> <outname>: write one variant to build/nr/one/<outname>.c, dump, print got's
IRA line in the clone, V and C line counts."""
import importlib.util, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nrsweep
gen, tag, name = sys.argv[1:4]
spec = importlib.util.spec_from_file_location('g', gen)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
for v in m.variants():
    if v[0] == tag:
        break
else:
    sys.exit('no tag')
out = os.path.join(nrsweep.ROOT, 'build', 'nr', 'one')
os.makedirs(out, exist_ok=True)
p = os.path.join(out, name + '.c')
r = nrsweep.run((v[0], v[1], p, list(v[2]) if len(v) > 2 else []))
print('V', r[1], 'C', r[2], 'r', r[7:], p)
d = os.path.join(out, name + '.d')
o = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'nrdump.py'), d, p], capture_output=True, text=True).stdout
for sec in o.split('== '):
    if sec.startswith('IRA netRecvVerbose.constprop'):
        for l in sec.split('\n'):
            if re.search(r'\b(got|size)\b|Result', l):
                print(l)
    if sec.startswith('BBRO'):
        print(sec.strip()[:400])
