"""python tools/wip/dehint/iw11refs.py <ira dump> <pseudo> ...: every insn referencing a pseudo in an -fdump-rtl-ira dump's final RTL, with its basic block and that block's freq."""
import re, sys

t = open(sys.argv[1], errors='replace').read()
regs = sys.argv[2:]
freq = {}
for m in re.finditer(r'^;; basic block (\d+), loop depth (\d+), count \d+, freq (\d+)', t, re.M):
    freq[int(m.group(1))] = (int(m.group(3)), int(m.group(2)))
# last RTL listing: after the last 'Disposition' or use whole text
i = t.rfind(';; Function')
insns = re.split(r'(?=^\((?:insn|jump_insn|call_insn|code_label|note|barrier)\S* )', t, flags=re.M)
bb = None
for x in insns:
    m = re.match(r'\(note \d+ \d+ \d+ (\d+) \[bb', x)
    if m:
        bb = int(m.group(1))
    for r in regs:
        if re.search(r'\(reg(?:/[a-z]+)*:SI %s(?:\s|\))|\(reg(?:/[a-z]+)*:SI \d+ \w+ \[orig:%s ' % (r, r), x) and x.startswith(('(insn', '(jump', '(call')):
            s = ' '.join(x.split())
            print('r%s bb%s f%s: %s' % (r, bb, freq.get(bb), s[:170]))
