"""python tools/wip/dehint/iw11sched.py <file.c> [gcc flags]: finalizeImage's preheader in sched2: compile with -fdump-rtl-sched2 -fsched-verbose=6 (scratch build/iw/a11/s),
print the two load insns (xb+48 spare, xb+56 hdr) in each RTL pass that shows them in the page loop's preheader, and the scheduler's ready-list trace for their block.
Writes build/iw/a11/s/fi.sched2."""
import glob, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib

path, flags = sys.argv[1], sys.argv[2:]
d = os.path.join(iwlib.BUILD, 'a11', 's')
os.makedirs(d, exist_ok=True)
for f in glob.glob(os.path.join(d, 'a.c*')):
    os.remove(f)
open(os.path.join(d, 'a.c'), 'w', newline='\n').write(open(path, newline='').read().replace('\r\n', '\n'))
subprocess.run([iwlib.GCC, '-c', '-O3'] + flags + ['-I' + os.path.join(iwlib.R, 'src'), '-fdump-rtl-sched2-details', '-fsched-verbose=6', 'a.c', '-o', 'a.o'], cwd=d, check=True, stdin=subprocess.DEVNULL)
t = open(glob.glob(os.path.join(d, 'a.c.*sched2'))[0], errors='replace').read()
m = re.search(r'^;; Function finalizeImage.*?(?=^;; Function |\Z)', t, re.S | re.M).group(0)
open(os.path.join(d, 'fi.sched2'), 'w', newline='\n').write(m)
print('dump chars', len(m))
for x in re.finditer(r'^\(insn (\d+) .*?\n(?:.*?\n)*?.*?"xb".*?const_int (48|56) .*$', m, re.M):
    if len(x.group(0)) < 400:
        print(x.group(1), 'xb+' + x.group(2))
