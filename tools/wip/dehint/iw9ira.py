"""python tools/wip/dehint/iw9ira.py <file.c> [gcc flags...]: compile with -fdump-rtl-ira-all (scratch dir build/iw/a9/ira) and print
for finalizeImage's page loop region (l5): the spill candidates in push order, the pops of the pseudos that matter, the pseudo numbers
of xb.hdr's and xb.spare's PHI partitions, and the page loop's block frequencies.  build/iw/a9/ira/fi.ira keeps the function's dump."""
import glob, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib

path, flags = sys.argv[1], sys.argv[2:]
d = os.path.join(iwlib.BUILD, 'a9', 'ira')
os.makedirs(d, exist_ok=True)
for f in glob.glob(os.path.join(d, 'a.c*')):
    os.remove(f)
a = os.path.join(d, 'a.c')
open(a, 'w', newline='\n').write(open(path, newline='').read().replace('\r\n', '\n'))
subprocess.run([iwlib.GCC, '-c', '-O3'] + flags + ['-I' + os.path.join(iwlib.R, 'src'), '-fdump-rtl-ira-all', 'a.c', '-o', 'a.o'], cwd=d, check=True)
t = open(glob.glob(os.path.join(d, 'a.c.*ira'))[0], errors='replace').read()
b = re.search(r'^;; Function finalizeImage \(.*?(?=^;; Function |\Z)', t, re.S | re.M).group(0)
open(os.path.join(d, 'fi.ira'), 'w', newline='\n').write(b)
for name, off in (('spare', 48), ('hdr', 56)):
    m = re.search(r'\(reg/f:SI (\d+) \[ prephitmp_(\d+) \]\)\s*\(mem/f/c:SI \(const:SI \(plus:SI \(symbol_ref:SI \("xb"\)[^\n]*\n\s*\(const_int %d ' % off, b)
    print(name, 'pseudo', m and m.group(1), 'partition name', m and m.group(2))
s = b.split('Loop 5 (parent')[1] if 'Loop 5 (parent' in b else ''
# the region's coloring: first Pushing ...,l5) line to the next "Loop"
i = b.find('Pushing a', b.find('Loop 5 (parent', b.find('Pushing a')))
j = b.find('  Loop ', i)
for l in b[i:j].split('\n'):
    if 'potential spill' in l or re.search(r'Popping a\d+\(r(\d+),l5\)', l):
        print(l.strip()[:80])
fr = re.findall(r'^;; basic block (\d+), loop depth (\d+), count 0, freq (\d+)', b, re.M)
print('depth>=2 freqs', ' '.join('%s:%s' % (x[0], x[2]) for x in fr if int(x[1]) >= 2)[:400])
