"""python tools/wip/dehint/iw18freq.py <file.c> [fn]: LRA's stack slots for fn with each pseudo's frequency: the sum of bb frequency over the insns that name it, from the last listing in
-fdump-rtl-ira-blocks. That this sum is what LRA sorts slots by (freq descending, then regno) is my reading; LRA's own totals aren't printed, so check it against the order of the `Slot N regnos` lines it prints.
Dumps in build/iw/a18/fq_<basename>."""
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib
path = sys.argv[1]
fn = sys.argv[2] if len(sys.argv) > 2 else 'imgAdd'
d = os.path.join(iwlib.BUILD, 'a18', 'fq_' + os.path.splitext(os.path.basename(path))[0])
os.makedirs(d, exist_ok=True)
open(os.path.join(d, 'a.c'), 'w', newline='\n').write(open(path, newline='').read().replace('\r\n', '\n'))
subprocess.run([iwlib.GCC, '-c', '-O3', '-I' + os.path.join(iwlib.R, 'src'), 'a.c', '-o', 'a.o', '-fdump-rtl-ira-details-blocks', '-fdump-rtl-reload-details'], cwd=d, check=True)


def func(suffix):
    f = [x for x in os.listdir(d) if x.endswith(suffix)][0]
    t = open(os.path.join(d, f), errors='replace').read()
    return re.search(r'^;; Function %s \(%s,.*?(?=^;; Function |\Z)' % (fn, fn), t, re.S | re.M).group(0)


ira = func('.ira')
freq = {}
names = {}
refs = {}
last = ira[ira.rfind('\n;; basic block 2,'):]
cur = 0
for blk in re.split(r'(?=^(?:\(insn|\(jump_insn|\(call_insn|\(note|\(barrier|\(code_label|\(debug_insn|;; basic block ))', last, flags=re.M):
    m = re.match(r';; basic block \d+, loop depth \d+, count \d+, freq (\d+)', blk)
    if m:
        cur = int(m.group(1))
        continue
    if not re.match(r'\((insn|jump_insn|call_insn) ', blk):
        continue
    b = re.split(r'\(expr_list|\(nil\)|\(int_list', blk)[0]
    seen = set()
    for x in re.finditer(r'\(reg(?:/[a-z]+)*:([A-Z0-9]+) (\d+)(?: \[ ?([^\]]*?) ?\])?', b):
        r = int(x.group(2))
        if r >= 53 and r not in seen:
            seen.add(r)
            freq[r] = freq.get(r, 0) + (cur * 1000 // 10000 or 1); refs.setdefault(r, []).append(cur)
            if x.group(3):
                names[r] = x.group(3)
rl = func('.reload')
for m in re.finditer(r'  Slot (\d+) regnos \(width = (\d+)\):((?:\t ?\d+)+)', rl):
    rs = [int(x) for x in m.group(3).split()]
    print('slot', m.group(1), 'w', m.group(2), [(r, freq.get(r), names.get(r, '')) for r in rs])
for r in sys.argv[3:]:
    print(r, 'bb freqs of its insns', refs.get(int(r)))
