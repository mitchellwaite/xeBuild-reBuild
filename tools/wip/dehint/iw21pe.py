"""python tools/wip/dehint/iw21pe.py <gen.py> <base.c> [fn]: for each (label, edits) of the generator's STATES: lines at plain -O3 per function, and fn's profile_estimate predictions for
blocks with more than one predictor or an opcode/return one, from -fdump-tree-profile_estimate-details. Scratch under build/iw/a21/pe."""
import importlib.util, os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib
sp = importlib.util.spec_from_file_location('g', sys.argv[1]); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
base = open(sys.argv[2], newline='').read().replace('\r\n', '\n')
fn = sys.argv[3] if len(sys.argv) > 3 else 'imgAdd'
top = os.path.join(iwlib.BUILD, 'a21', 'pe', os.path.splitext(os.path.basename(sys.argv[1]))[0])
os.makedirs(top, exist_ok=True)
def one(st):
    lab, ed = st
    t = base
    for x, y in ed:
        if x not in t:
            return lab, 'missing ' + x[:50], []
        t = t.replace(x, y)
    d = os.path.join(top, re.sub(r'\W', '_', lab)); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'a.c'), 'w', newline='\n').write(t)
    fl = ['-c', '-O3', '-I' + os.path.join(iwlib.R, 'src'), 'a.c', '-o', 'a.o', '-fdump-tree-profile_estimate-details']
    r = subprocess.run([iwlib.GCC] + fl, cwd=d, capture_output=True, text=True)
    if r.returncode:
        return lab, 'ERR ' + r.stderr[:300], []
    res = iwlib.fmt(iwlib.score_text(t, []))
    out = []
    pf = [x for x in os.listdir(d) if 'profile_estimate' in x]
    if pf:
        tx = open(os.path.join(d, pf[0]), errors='replace').read()
        k = re.search(r'^;; Function %s \(%s,.*?(?=^;; Function |\Z)' % (fn, fn), tx, re.S | re.M)
        if k:
            for b in re.findall(r'^Predictions for bb \d+\n(?:  .*\n)+', k.group(0), re.M):
                if re.search(r'opcode values positive|early return|opcode values nonequal|const return|call', b) :
                    out.append(' | '.join(x.strip() for x in b.strip().split('\n')))
    return lab, res, out
for lab, res, out in ThreadPoolExecutor(4).map(one, m.STATES):
    print('==', lab, res[:170])
    if '-q' not in sys.argv:
        for o in out:
            print('   ', o)
