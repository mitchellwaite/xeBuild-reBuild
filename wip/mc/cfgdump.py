"""Blocks of one function from an RTL dump made with -fdump-rtl-<pass>-blocks-details: frequency,
every successor with its probability, and a content hint (calls, string labels, constant
stores).  In profile builds the edge counts are printed too (as extra [?%] entries).
python wip/mc/cfgdump.py <dump> <function> [lo hi]"""
import re, sys
txt = open(sys.argv[1]).read()
fn = sys.argv[2]
s = txt.index(';; Function %s ' % fn)
e = txt.find('\n;; Function ', s + 1)
body = txt[s:e if e > 0 else len(txt)]
lo = int(sys.argv[3]) if len(sys.argv) > 3 else 0
hi = int(sys.argv[4]) if len(sys.argv) > 4 else 10**9
blocks = []
cur = None
for line in body.split('\n'):
    m = re.match(r';; basic block (\d+), loop depth (\d+), count \d+, freq (\d+)', line)
    if m:
        cur = {'bb': int(m.group(1)), 'freq': int(m.group(3)), 'succ': [], 'pred': [], 'hint': [], 'mode': None}
        blocks.append(cur); mode = None; continue
    if cur is None: continue
    if line.startswith(';;  pred:'): mode = 'pred'; line = line[9:]
    elif line.startswith(';;  succ:'): mode = 'succ'; line = line[9:]
    elif line.startswith(';;      ') and mode: line = line[2:]
    elif line.startswith(';;'): mode = None; continue
    else:
        mode = None
        m = re.search(r'\(call \(mem:QI \(symbol_ref:SI \("(\w+)"\)', line)
        if m: cur['hint'].append(m.group(1))
        m = re.search(r'\(symbol_ref(?:/\w)?:SI \("\*?(LC\d+)"\)', line)
        if m: cur['hint'].append(m.group(1))
        m = re.search(r'\(set \(mem:SI \(plus:SI \(reg/f:SI 7 sp\)\s*\(const_int (\d+) [^)]*\)\)\s*\[[^\]]*\]\)\s*\(const_int (-?\d+) ', line)
        if m: cur['hint'].append('[sp+%s]=%s' % m.groups())
        if 'tablejump' in line or 'parallel' in line and 'use (label_ref' in line: cur['hint'].append('TABLEJUMP')
        continue
    if mode:
        for m in re.finditer(r'(\d+|EXIT|ENTRY)(?: \[([\d.]+)%\])?\s*(\([A-Z_,]+\))?', line):
            if m.group(1):
                cur[mode].append((m.group(1), m.group(2), (m.group(3) or '').replace('FALLTHRU', 'F').replace('LOOP_EXIT', 'X').replace('DFS_BACK', 'B')))
for b in blocks:
    if not (lo <= b['bb'] <= hi): continue
    succ = ' '.join('%s[%s%%]%s' % (d, p or '?', f) for d, p, f in b['succ'])
    print('%4d %6d  -> %-40s  %s' % (b['bb'], b['freq'], succ, ' '.join(b['hint'])[:70]))
