"""python tools/wip/dehint/nrbb.py <dumpdir> [fn]: netRecvVerbose's bbro trace log, and each block's freq and first call."""
import re, sys
d = sys.argv[1]
fnname = sys.argv[2] if len(sys.argv) > 2 else 'netRecvVerbose'
import os
t = open(os.path.join(d, next(f for f in os.listdir(d) if f.endswith('r.bbro')))).read()
i = t.index(';; Function %s' % fnname)
s = t[i:]
j = s.find('\n;; Function ', 10)
s = s[:j] if j > 0 else s
k = s.find('Reordering with the STC')
e = s.find('Trace ', k)
print('\n'.join(l for l in s[k:].split('\n') if re.match(r'(STC|Getting bb|Basic block|Trace |Connection|Duplicated|  *[0-9]+ )', l))[:6000])
blocks = re.split(r'\n(?=;; basic block|\(note \d+ \d+ \d+ \d+ \[bb \d+\] NOTE_INSN_BASIC_BLOCK)', s[:k])
seen = {}
for m in re.finditer(r'^;; basic block (\d+), loop depth (\d+), count \d+, freq (\d+)(.*?)(?=^;; basic block|\Z)', s[:k], re.M | re.S):
    if m.group(1) in seen:
        continue
    b = m.group(4)
    call = re.search(r'symbol_ref[^\n]*"(\w+)"[^\n]*\n?', b)
    calls = re.findall(r'\(call .*?"([^"]+)"', b, re.S)
    strs = re.findall(r'\[\*?LC\d+\]|"([a-zA-Z_][^"]{0,30})"', b)
    succ = re.findall(r';; +succ: +(.*?)(?:\n;;\n|\n\()', b, re.S)
    seen[m.group(1)] = 1
    print('bb', m.group(1), 'depth', m.group(2), 'f', m.group(3), calls[:2], ' '.join(x.strip() for x in succ)[:120].replace('\n', ' '))
