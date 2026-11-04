"""python tools/wip/dehint/iw12arms.py <file.c> [fn]: at profile_estimate, in fn (default imgAddFile): each block's freq and the call in it, then each `Predictions for bb` line.  Shows what P(big) a form really gets."""
import glob, os, re, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib
path = sys.argv[1]
fn = sys.argv[2] if len(sys.argv) > 2 else 'imgAddFile'
d = tempfile.mkdtemp(dir=iwlib.BUILD, prefix='ar')
open(os.path.join(d, 'a.c'), 'w', newline='\n').write(open(path, newline='').read().replace('\r\n', '\n'))
subprocess.run([iwlib.GCC, '-c', '-O3', '-I' + os.path.join(iwlib.R, 'src'), '-fdump-tree-profile_estimate-blocks-details', 'a.c', '-o', 'a.o'], cwd=d, check=True, stdin=subprocess.DEVNULL)
t = open(glob.glob(os.path.join(d, 'a.c.*profile_estimate'))[0], errors='replace').read()
m = re.search(r'^;; Function %s \(.*?(?=^;; Function |\Z)' % re.escape(fn), t, re.S | re.M).group(0)
i = m.rfind('\n%s (' % fn)
body = m[i:]
for x in re.finditer(r'basic block (\d+), loop depth \d+, count \d+, freq (\d+).*?(?=basic block \d+, loop|\Z)', body, re.S):
    calls = re.findall(r'^\s+(?:[\w.]+ = )?(\w+) \(', x.group(0), re.M)
    conds = re.findall(r'^\s+(if \(.*\))', x.group(0), re.M)
    succ = re.findall(r'(\d+) \[([\d.]+)%\]', x.group(0).split('succ:')[-1])
    print('bb%s f%s %s %s -> %s' % (x.group(1), x.group(2), ','.join(calls), ' '.join(conds), succ))
for x in re.finditer(r'Predictions for bb (\d+)\n((?:  .*\n)+)', m[:i]):
    print('pred bb' + x.group(1), ' | '.join(l.strip() for l in x.group(2).strip().split('\n')))
iwlib.cleanup(d)
