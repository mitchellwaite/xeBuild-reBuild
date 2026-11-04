"""python tools/wip/dehint/iw23sw.py <gen.py> <base.c> [threads] [top]: a generator's states scored by lines, compare signature, and for writeFsTable's second copy whether the nonzero arm survives at dce4 (`keep`: the const PHI arg comes straight from the test's block) and the names sccp gives FS2 and FS1 (attempt 23). pos6 needs FS2 < FS1. Saves the keep states to build/iw/a23/keep_<gen>_<label>.c."""
import hashlib, importlib.util, itertools, os, re, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib, iw16rej
gen = sys.argv[1]; base = sys.argv[2]; th = int(sys.argv[3]) if len(sys.argv) > 3 else 4; top = int(sys.argv[4]) if len(sys.argv) > 4 else 25
sp = importlib.util.spec_from_file_location('g', gen); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
text = open(base, newline='').read().replace('\r\n', '\n')
g = os.path.splitext(os.path.basename(gen))[0]
OUT = os.path.join(iwlib.BUILD, 'a23'); os.makedirs(OUT, exist_ok=True)
def fn(tx, name='writeFsTable'):
    r = re.search(r'^;; Function %s \(.*?(?=^;; Function |\Z)' % name, tx, re.S | re.M)
    return r.group(0) if r else ''
def one(c):
    lab = '+'.join(x[0] for x in c if x[0])
    t = text
    for l, ed in c:
        for x, y in ed:
            if x not in t:
                return lab, None, 'missing ' + x[:40], '', t
            t = t.replace(x, y)
    d = tempfile.mkdtemp(dir=iwlib.BUILD, prefix='s3')
    ok, o, d = iwlib.compile_src(t, [], workdir=d, extra=['-fdump-tree-dce4=d.txt', '-fdump-tree-sccp=c.txt', '-fdump-tree-optimized=op.txt', '-fdump-tree-all-vops=q.txt'] if 0 else ['-fdump-tree-dce4=d.txt', '-fdump-tree-sccp-vops=c.txt', '-fdump-tree-optimized=op.txt'])
    if not ok:
        iwlib.cleanup(d)
        return lab, None, 'compile ' + o[:200], '', t
    idn, tot, per, notes = iwlib.report(o)
    b = fn(open(os.path.join(d, 'd.txt'), errors='replace').read())
    pm = re.search(r'# (\S+) = PHI <(?:56\((\d+)\), \S+\((\d+)\)|\S+\((\d+)\), 56\((\d+)\))>', b)
    keep = '?'
    if pm:
        c56 = pm.group(2) or pm.group(5)
        keep = 'keep' if re.search(r'<bb %s>:\n(?:\s*#.*\n)*\s*\S.*=.*\n' % c56, b) or re.search(r'if \(\S+ != 0\)\n\s+goto <bb \d+>;\n\s+else\n\s+goto <bb \d+>;\n\n\s*<bb %s>:\n[^\n]*(?:\.type = 48|CLOBBER)' % c56, b) else 'no'
    s = fn(open(os.path.join(d, 'c.txt'), errors='replace').read())
    sn = ' '.join(re.findall(r'# \.MEM_(\d+) = PHI <\.MEM_\d+\(\d+\)>\n', s))
    s8 = ''
    for x in re.finditer(r'if \((ivtmp\.\d+_\d+|_\d+) != (ivtmp\.\d+_\d+|_\d+)\)', fn(open(os.path.join(d, 'op.txt'), errors='replace').read())):
        if 'ivtmp' in x.group(0):
            s8 += '<' if x.group(1).startswith('ivtmp') else '>'
    iwlib.cleanup(d)
    tag = '%s phi=%s sccp=[%s] clob=%d' % (keep, pm.group(1) if pm else '-', sn, b.count('CLOBBER'))
    return lab, {'total': tot, 'per': per, 'notes': notes, 'sig8': s8, 'identical': idn}, tag, s8, t
res = list(ThreadPoolExecutor(th).map(one, itertools.product(*m.AXES)))
bad = [r for r in res if r[1] is None]
if bad:
    print(len(bad), 'failed, first', bad[0][0], bad[0][2][:200])
good = sorted([r for r in res if r[1]], key=lambda r: r[1]['total'])
print(len(good), 'ok')
for lab, r, tag, s8, t in good[:top]:
    print(r['total'], s8, lab, tag, {k.replace('_imgAdd', 'iA').replace('.constprop', ''): v for k, v in r['per'].items()} if len(r['per']) < 6 else len(r['per']))
for lab, r, tag, s8, t in good:
    if r['total'] == 0 or s8 == iw16rej.TARGET8:
        print('TARGET', r['total'], lab, tag)
    if r['total'] == 0 or s8 == iw16rej.TARGET8 or 'clob=1' in tag or 'clob=2' in tag:
        open(os.path.join(OUT, 'keep_%s_%s_%s.c' % (g, lab.replace('+', '_')[:50], hashlib.md5(t.encode()).hexdigest()[:5])), 'w', newline='\n').write(t)
