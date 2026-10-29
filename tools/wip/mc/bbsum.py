"""Summarise bb-reorder's traces: python bbsum.py <bbro dump> <fn> <asm.s> <pre-bbro dump>
Block contents (calls, strings, const stores) come from the pre-bbro dump (same numbering)."""
import re, sys
dump, fn, asm, cdump = sys.argv[1:5]

def section(path):
    txt = open(path).read()
    s = txt.index(';; Function %s ' % fn)
    e = txt.find('\n;; Function ', s + 1)
    return txt[s:e if e > 0 else len(txt)]

body, cbody = section(dump), section(cdump)
strs, cur = {}, None
for l in open(asm):
    m = re.match(r'^(LC\d+):', l)
    if m:
        cur = m.group(1); continue
    m = re.match(r'^\s*\.(?:ascii|string)\s+"(.*)"', l)
    if m and cur:
        strs.setdefault(cur, m.group(1).replace('\12', '|').replace('\0', '')[:22]); cur = None
blocks, cur = {}, None
for l in cbody.split('\n'):
    m = re.search(r'\[bb (\d+)\] NOTE_INSN_BASIC_BLOCK', l)
    if m:
        cur = int(m.group(1)); blocks[cur] = []; continue
    if cur is None: continue
    m = re.search(r'\(call \(mem:QI \(symbol_ref:SI \("(\w+)"\)', l)
    if m: blocks[cur].append('call ' + m.group(1))
    for m in re.finditer(r'\(symbol_ref:SI \("(LC\d+)"\)', l):
        blocks[cur].append('"%s"' % strs.get(m.group(1), m.group(1)))
    m = re.search(r'\(set \(mem:SI \((?:plus:SI )?\(reg/f:SI 7 sp\)(?: \(const_int \d+ \[0x[0-9a-f]+\]\))?\)\s*\[.*?\]\)\s*\(const_int (\d+) ', l)
    if m and m.group(1) != '0': blocks[cur].append('#' + m.group(1))
for m in re.finditer(r'Trace (\d+) \(round (\d+)\):((?:\s+\d+ \[\d+\])+)', body):
    bbs = re.findall(r'(\d+) \[(\d+)\]', m.group(3))
    print('T%-3s r%s  ' % (m.group(1), m.group(2)) + ' ; '.join('%s[%s] %s' % (b, f, ' '.join(blocks.get(int(b), []))) for b, f in bbs))
