"""python tools/wip/dehint/iw11slots.py <file.c> <fn> [gcc flags]: LRA's stack slots for <fn> (-fdump-rtl-reload-details): `Slot N regnos` lines and the frequency LRA assigned each pseudo.
Function's dump goes to build/iw/a11/r/fn.reload."""
import glob, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib

path, fn, flags = sys.argv[1], sys.argv[2], sys.argv[3:]
d = os.path.join(iwlib.BUILD, 'a11', 'r')
os.makedirs(d, exist_ok=True)
for f in glob.glob(os.path.join(d, 'a.c*')):
    os.remove(f)
open(os.path.join(d, 'a.c'), 'w', newline='\n').write(open(path, newline='').read().replace('\r\n', '\n'))
subprocess.run([iwlib.GCC, '-c', '-O3'] + flags + ['-I' + os.path.join(iwlib.R, 'src'), '-fdump-rtl-reload-details', 'a.c', '-o', 'a.o'], cwd=d, check=True, stdin=subprocess.DEVNULL)
t = open(glob.glob(os.path.join(d, 'a.c.*reload'))[0], errors='replace').read()
m = re.search(r'^;; Function %s \(.*?(?=^;; Function |\Z)' % re.escape(fn), t, re.S | re.M).group(0)
open(os.path.join(d, 'fn.reload'), 'w', newline='\n').write(m)
for l in m.split('\n'):
    if re.search(r'Slot \d+ regnos|Assigning to|Spill r|slot', l) and len(l) < 200:
        print(l)
