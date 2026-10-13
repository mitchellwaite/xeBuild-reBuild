"""Emit a C function body that reproduces one function of the original binary
as a top-to-bottom basic asm block (for functions not yet matched from C).

python re/asmfunc.py <xeBuild.exe> <lines.json> <ref.o> <ref_text_base> <addr> [str_addr=C-literal ...]

The function body comes from the ddisasm lines (Intel syntax, original
encodings pinned), references to other functions use split.py's SYMBOLS
names, string addresses become "i" operands so gcc shares its own .rdata
literal, and the .cfi_* directives are rebuilt from the reference object's
FDE so gas emits the same .eh_frame entry.  Ends with __builtin_unreachable()
so gcc adds no epilogue.
"""
import json, os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(__file__))
from split import SYMBOLS

TC = os.path.join(os.path.dirname(__file__), '..', 'tools', 'toolchain-4745', 'mingw32', 'bin')


def fde_program(refo, start):
    out = subprocess.run([os.path.join(TC, 'objdump.exe'), '--dwarf=frames', refo],
                         capture_output=True, text=True).stdout
    blocks = out.split('\n\n')
    blk = [b for b in blocks if re.search(r'FDE .*pc=0*%x\.\.' % start, b)][0]
    m = re.search(r'pc=([0-9a-f]+)\.\.([0-9a-f]+)', blk)
    lo, hi = int(m.group(1), 16), int(m.group(2), 16)
    at, ops = lo, []
    regs = {'r3': 'ebx', 'r5': 'ebp', 'r6': 'esi', 'r7': 'edi'}
    for l in blk.splitlines():
        m = re.search(r'DW_CFA_advance_loc\d?: \d+ to ([0-9a-f]+)', l)
        if m:
            at = int(m.group(1), 16)
            continue
        m = re.search(r'DW_CFA_def_cfa_offset: (\d+)', l)
        if m:
            ops.append((at, '.cfi_def_cfa_offset %s' % m.group(1)))
        m = re.search(r'DW_CFA_offset: (r\d+) \(\w+\) at cfa(-\d+)', l)
        if m:
            ops.append((at, '.cfi_offset %s, %s' % (regs[m.group(1)], m.group(2))))
        m = re.search(r'DW_CFA_restore: (r\d+)', l)
        if m:
            ops.append((at, '.cfi_restore %s' % regs[m.group(1)]))
        if 'DW_CFA_remember_state' in l:
            ops.append((at, '.cfi_remember_state'))
        if 'DW_CFA_restore_state' in l:
            ops.append((at, '.cfi_restore_state'))
    return lo, hi, ops


def main():
    exe, lj, refo, base, addr = sys.argv[1:6]
    base, addr = int(base, 16), int(addr, 16)
    strs = dict((int(k, 16), v) for k, v in (a.split('=', 1) for a in sys.argv[6:]))
    d = json.load(open(lj))
    L, A = d['lines'], d['addr']
    lo, hi, cfi = fde_program(refo, addr - base)
    end = addr + (hi - lo)
    i = A.index(addr)
    body = []
    while True:
        a = A[i]
        if a is not None and a >= end:
            break
        body.append((a, L[i].strip()))
        i += 1
    names = {}
    for k, v in SYMBOLS.items():
        names['FUN_%x' % k] = v
        names['.L_%x' % k] = v
    opnum = {}
    out = []
    ci = 0
    for a, t in body:
        if a is not None:
            while ci < len(cfi) and cfi[ci][0] - lo + addr <= a:
                out.append(cfi[ci][1])
                ci += 1
        if not t:
            continue
        def sub(m):
            s = m.group(0)
            v = int(s.split('_')[1], 16)
            if v in strs:
                opnum.setdefault(v, len(opnum))
                return '%%c%d' % opnum[v]
            if s in names:
                return names[s]
            return s
        t = re.sub(r'(?<![\w.$])(?:FUN|\.L)_[0-9a-f]+', sub, t)
        out.append(t)
    while ci < len(cfi):
        out.append(cfi[ci][1])
        ci += 1
    lines = ['\t__asm__ __volatile__(', '\t\t".intel_syntax noprefix\\n"']
    lines += ['\t\t"%s\\n"' % t.replace('\\', '\\\\').replace('"', '\\"') for t in out]
    lines += ['\t\t".att_syntax prefix\\n"']
    ops = sorted(opnum, key=opnum.get)
    lines.append('\t\t: : %s);' % ', '.join('"i" (%s)' % strs[v] for v in ops) if ops else '\t\t);')
    lines.append('\t__builtin_unreachable();')
    print('\n'.join(lines))


main()
