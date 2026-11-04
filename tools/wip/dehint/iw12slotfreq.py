"""python tools/wip/dehint/iw12slotfreq.py <file.c> [flags]: imgAddFile's spilled pseudos 136-ish (off+len) and npages: from the reload dump, each insn that names `orig:N` or `reg N` at the last RTL listing with the block freq, summed per pseudo as LRA does (REG_FREQ = freq * 1000 / 10000, at least 1). Prints Slot lines and per-pseudo totals for pseudos in slots 6 and 7."""
import glob, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib

path, flags = sys.argv[1], sys.argv[2:]
FN = os.environ.get('IWFN', 'imgAddFile')
d = os.path.join(iwlib.BUILD, 'a12', 'sf%d' % os.getpid())
os.makedirs(d, exist_ok=True)
open(os.path.join(d, 'a.c'), 'w', newline='\n').write(open(path, newline='').read().replace('\r\n', '\n'))
subprocess.run([iwlib.GCC, '-c', '-O3'] + flags + ['-I' + os.path.join(iwlib.R, 'src'), '-fdump-rtl-ira', '-fdump-rtl-reload-details-blocks', 'a.c', '-o', 'a.o'], cwd=d, check=True, stdin=subprocess.DEVNULL)
t = open(glob.glob(os.path.join(d, 'a.c.*reload'))[0], errors='replace').read()
m = re.search(r'^;; Function %s \(.*?(?=^;; Function |\Z)' % re.escape(FN), t, re.S | re.M).group(0)
slots = re.findall(r'Slot (\d+) regnos \(width = \d+\):\s*([\d\s]+)', m)
print(' '.join('%s:%s' % (a, ','.join(b.split())) for a, b in slots))
# block freqs from the final listing
freq = {}
for x in re.finditer(r'^;; basic block (\d+), loop depth (\d+), count \d+, freq (\d+)', m, re.M):
    freq[int(x.group(1))] = int(x.group(3))
# slot refs at the final listing: (mem... (plus (reg sp) (const_int N)) ... [ orig ...
tail = m[m.rfind('\n;; basic block 0,') if '\n;; basic block 0,' in m else 0:]
tail = m[m.rfind(';; Removing') if False else 0:]
insns = re.split(r'(?=^\((?:insn|jump_insn|call_insn|note)\S* )', m, flags=re.M)
bb = None
tot = {}
for x in insns:
    h = re.match(r'\(note \d+ \d+ \d+ (\d+) \[bb', x)
    if h:
        bb = int(h.group(1))
    if not x.startswith(('(insn', '(jump', '(call')):
        continue
    for s in re.findall(r'\(const_int (\d+) \[0x[0-9a-f]+\]\)\) \[\d+ %sfp', x) :
        pass
    for off in re.findall(r'\(mem/c:[SQ]I \(plus:SI \(reg/f:SI 7 sp\)\s+\(const_int (\d+)', x):
        f = freq.get(bb, 0)
        tot.setdefault(int(off), []).append((bb, f))
for off in sorted(tot):
    print('sp+%#x' % off, 'total', sum(max(f * 1000 // 10000, 1) for _, f in tot[off]), tot[off])
