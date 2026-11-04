"""python tools/wip/dehint/iw12blocks.py <file.c> <pass> [fn] [flags]: one line per block of fn (default imgAddFile) at a tree pass
(-fdump-tree-<pass>-blocks): bb, loop depth, freq, successors with probability, last statement. Pass e.g. optimized, fixup_cfg4, cunroll."""
import glob, os, re, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib

path, pas = sys.argv[1], sys.argv[2]
fn = sys.argv[3] if len(sys.argv) > 3 and not sys.argv[3].startswith('-') else 'imgAddFile'
flags = [a for a in sys.argv[3:] if a.startswith('-')]
d = tempfile.mkdtemp(dir=iwlib.BUILD, prefix='bl')
open(os.path.join(d, 'a.c'), 'w', newline='\n').write(open(path, newline='').read().replace('\r\n', '\n'))
subprocess.run([iwlib.GCC, '-c', '-O3'] + flags + ['-I' + os.path.join(iwlib.R, 'src'), '-fdump-tree-%s-blocks-details' % pas, 'a.c', '-o', 'a.o'], cwd=d, check=True, stdin=subprocess.DEVNULL)
f = glob.glob(os.path.join(d, 'a.c.*t.%s*' % pas))[0]
t = open(f, errors='replace').read()
m = re.search(r'^;; Function %s \(.*?(?=^;; Function |\Z)' % re.escape(fn), t, re.S | re.M)
if not m:
    sys.exit('no ' + fn + ' in ' + f)
parts = re.split(r'^\s*;;\s+basic block (\d+), loop depth (\d+), count \d+, freq (\d+)', m.group(0), flags=re.M)
for i in range(1, len(parts), 4):
    bb, depth, fr, body = parts[i:i + 4]
    succ = re.findall(r';;\s+(?:succ:\s+)?(\d+|EXIT) \[([\d.]+)%\]', body.split('succ:')[-1]) if 'succ:' in body else []
    st = [l.strip() for l in body.split('\n') if l.strip() and not l.strip().startswith(';;') and not l.strip().startswith('<') and not l.strip().startswith('#') and not l.strip().startswith('goto') and not l.strip().startswith('else') and l.strip() not in '{}']
    print('bb%-3s d%s f%-5s -> %-28s %s' % (bb, depth, fr, ' '.join('%s:%s' % s for s in succ), (st[-1] if st else '')[:70]))
iwlib.cleanup(d)
