"""python tools/wip/dehint/iw23arm.py <gen.py> [base] [labels...]: for a generator's states, writeFsTable's second copy at each of forwprop3, ccp3, pre, lim2, dce4: the off & 0x1ffff test and the statements in its arm (attempt 23). Shape wanted at dce4: `true -> empty forwarder, false -> the PHI's block`."""
import importlib.util, itertools, os, re, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib
gen = sys.argv[1]; base = sys.argv[2]; want = sys.argv[3:]
sp = importlib.util.spec_from_file_location('g', gen); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
text = open(base, newline='').read().replace('\r\n', '\n')
for c in itertools.product(*m.AXES):
    lab = '+'.join(x[0] for x in c if x[0])
    if want and lab not in want:
        continue
    t = text
    for l, ed in c:
        for x, y in ed:
            t = t.replace(x, y)
    d = tempfile.mkdtemp(dir=iwlib.BUILD, prefix='am')
    ok, o, d = iwlib.compile_src(t, [], workdir=d, extra=['-fdump-tree-forwprop3=f.txt', '-fdump-tree-ccp3=c.txt', '-fdump-tree-pre=p.txt', '-fdump-tree-lim2=l.txt', '-fdump-tree-dce4=d.txt'])
    print('=====', lab)
    if ok:
        for n in 'fcpld':
            tx = open(os.path.join(d, n + '.txt'), errors='replace').read()
            b = re.search(r'^;; Function writeFsTable \(.*?(?=^;; Function |\Z)', tx, re.S | re.M).group(0)
            b = b[b.find('small:'):] if 'small:' in b else b
            j = b.find('.type = 48;')
            print(n, '| ' + ' | '.join(l.strip() for l in b[j:j + 700].split('\n')[1:] if l.strip() and 'MEM[' not in l)[:420])
    iwlib.cleanup(d)
