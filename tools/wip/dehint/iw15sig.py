"""python tools/wip/dehint/iw15sig.py <file.c>...: compare signature in writeFsTable's ivopts dump: for each page-loop or outer compare, in dump order, `>` when the increment's
version is above the bound's, else `<`. Target (src, reference): small1 `<`, big inner `>`, big outer `>`, small2 `<`, small3 `<`, i.e. <>><<. Also prints the lines differing."""
import glob, os, re, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib
def sig(path):
    t = open(path, newline='').read().replace('\r\n', '\n')
    d = tempfile.mkdtemp(dir=iwlib.BUILD, prefix='sg')
    open(os.path.join(d, 'a.c'), 'w', newline='\n').write(t)
    subprocess.run([iwlib.GCC, '-c', '-O3', '-I' + os.path.join(iwlib.R, 'src'), '-fdump-tree-ivopts', 'a.c', '-o', 'a.o'], cwd=d, check=True, stdin=subprocess.DEVNULL)
    f = glob.glob(d + '/a.c.*t.ivopts')[0]
    tx = open(f, errors='replace').read()
    m = re.search(r'^;; Function writeFsTable \(.*?(?=^;; Function |\Z)', tx, re.S | re.M).group(0)
    b = m[m.find('\n{'):]
    s = ''; ns = []
    for x in re.finditer(r'if \(ivtmp\.\d+_(\d+) != _(\d+)\)', b):
        a, c = int(x.group(1)), int(x.group(2))
        s += '>' if a > c else '<'
        ns.append((a, c))
    iwlib.cleanup(d)
    return s, ns
if __name__ == '__main__':
    for p in sys.argv[1:]:
        s, ns = sig(p)
        r = iwlib.score_text(open(p, newline='').read().replace('\r\n', '\n'), [])
        print(os.path.basename(p), s, ns, iwlib.fmt(r)[:110])
