"""python tools/wip/dehint/nrtr.py <src.c> [fn]: dumps to build/nr/tr/, prints bbro traces and tail predictions for netRecv."""
import glob, os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
d = os.path.join(ROOT, 'build', 'nr', 'tr', os.path.basename(os.path.dirname(sys.argv[1])) + '_' + os.path.basename(sys.argv[1])[:-2])
fn = sys.argv[2] if len(sys.argv) > 2 else 'netRecv'
subprocess.run([sys.executable, os.path.join(ROOT, 'tools/wip/dehint/nrdump.py'), d, sys.argv[1]], capture_output=True)
o = subprocess.run([sys.executable, os.path.join(ROOT, 'tools/wip/dehint/nrbb.py'), d, fn], capture_output=True, text=True).stdout
print('\n'.join(l for l in o.split('\n') if l.startswith('Trace')))
t = open(glob.glob(d + '/*profile_estimate')[0]).read()
i = t.index(';; Function %s ' % fn); j = t.find('\n;; Function', i + 10); s = t[i:j]
for m in re.finditer(r'Predictions for bb (\d+)\n(.*?)(?=\n\S|\Z)', s, re.S):
    ls = m.group(2).split('\n')
    print(m.group(1), ' / '.join(x.strip().replace(' heuristics', '') for x in ls if 'ignored' not in x and 'combined' not in x))
