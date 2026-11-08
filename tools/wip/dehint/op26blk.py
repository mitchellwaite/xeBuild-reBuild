#!/usr/bin/env python3
"""Attempt 26: one-line summaries of applyIniOptions' blocks in a p1 dump's cprop_hardreg
(bbro's input numbering): preds/succs with probabilities, calls, xb fields read/written,
constants stored, string literals.

python tools/wip/dehint/op26blk.py TAG FROM TO"""
import os, re, sys
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'build', 'v', 'aio_p1')
tag, lo, hi = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
t = open(os.path.join(R, tag, 'a.c.272r.cprop_hardreg')).read()
t = t[t.index(';; Function applyIniOptions'):]
t = t[:t.index(';; Function', 10)]
blocks = re.split(r'(?=^;; basic block \d+,)', t, flags=re.M)
for b in blocks:
    m = re.match(r';; basic block (\d+), loop depth \d+, count \d+, freq (\d+)', b)
    if not m or not lo <= int(m.group(1)) <= hi:
        continue
    n, f = m.group(1), m.group(2)
    pr = re.search(r';;  pred:(.*?)\n;; bb', b, re.S)
    pr = ' '.join(re.findall(r'(\d+)(?: \[([\d.]+)%\])?', pr.group(1).replace('(FALLTHRU)', '').replace('(DFS_BACK)', '')) and
                  ['%s%s' % (x, ('/' + p) if p else '') for x, p in re.findall(r'(\d+)(?: \[([\d.]+)%\])?', re.sub(r'\([A-Z_, ]+\)', '', pr.group(1)))]) if pr else ''
    sc = re.findall(r';;  succ:(.*?)\n;; lr  out', b, re.S)
    sc = ' '.join('%s%s' % (x, ('/' + p) if p else '') for x, p in re.findall(r'(\d+)(?: \[([\d.]+)%\])?', re.sub(r'\([A-Z_, ]+\)', '', sc[0]))) if sc else ''
    ev = []
    for ins in re.split(r'\n(?=\((?:insn|call_insn|jump_insn|code_label|note) )', b):
        if ins.startswith('(call_insn'):
            c = re.search(r'symbol_ref:SI \("([^"]+)"\)', ins)
            ev.append('call ' + (c.group(1) if c else '?'))
        elif ins.startswith('(jump_insn'):
            if 'asm_operands' in ins:
                ev.append('asmgoto')
            elif 'if_then_else' in ins:
                ev.append('jcc')
            else:
                ev.append('jmp')
        elif ins.startswith('(insn'):
            fs = re.findall(r'\[\d+ (xb\.[\w.\[\]]+)\+?\d* ', ins)
            st = re.match(r'\(insn \d+ \d+ \d+ \d+ \(set \(mem', ins)
            lc = re.findall(r'"\*(LC\d+)"', ins)
            for x in fs:
                ev.append(('W ' if st else 'R ') + x[3:])
            if st and not fs:
                k = re.search(r'\(const_int (-?\d+)', ins.split('\n', 2)[-1] if '\n' in ins else ins)
            for x in lc:
                ev.append(x)
    print('%4s f%-5s p[%s] s[%s]  %s' % (n, f, pr, sc, ' '.join(ev)))
