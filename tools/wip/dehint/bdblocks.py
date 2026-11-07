"""python tools/wip/dehint/bdblocks.py build/bd/dump/loadBlFiles.bbro [pattern]: one line per block of bbro's final RTL
(after reordering): new index, the old (trace list) index, frequency, and a short summary of its insns (calls, compares
with constants, stores of constants), so a frequency in the trace list can be tied to source.  Attempt 28."""
import re, sys

t = open(sys.argv[1], errors='replace').read()
pat = sys.argv[2] if len(sys.argv) > 2 else None
# the last "Reordered sequence" block maps new index -> old index, freq
seqs = [m.start() for m in re.finditer(r'^Reordered sequence:', t, re.M)]
s = seqs[0]
body = t[s:]
mp = {}
for m in re.finditer(r'^ (\d+) bb (\d+)  \[(\d+)\]', body, re.M):
    if m.group(1) in mp:
        break
    mp[m.group(1)] = (m.group(2), m.group(3))
rest = body
cur = None
out = {}
order = []
for line in rest.splitlines():
    m = re.match(r'\(note \d+ \d+ \d+ (\d+) \[bb \d+\] NOTE_INSN_BASIC_BLOCK\)', line)
    if m:
        cur = m.group(1)
        if cur in out:  # second listing: stop
            break
        out[cur] = []
        order.append(cur)
        continue
    if cur is None:
        continue
    m = re.search(r'symbol_ref:SI \("(\w+)"\)', line)
    if m and '(call' in line:
        out[cur].append('call ' + m.group(1))
    m = re.search(r'\(compare:\w+ \(.*?\)\s*\(const_int (-?\d+)', line)
    if m:
        out[cur].append('cmp %s' % m.group(1))
    m = re.search(r'compare:CC\w* \((?:mem|reg)', line)
    m2 = re.search(r'REG_BR_PROB (\d+)', line)
    if m2:
        out[cur].append('p%s' % m2.group(1))
for b in order:
    old, fq = mp.get(b, ('?', '?'))
    sm = ' '.join(out[b])
    if pat and not re.search(pat, sm + ' old%s' % old):
        continue
    print('%4s old %4s [%5s] %s' % (b, old, fq, sm))
