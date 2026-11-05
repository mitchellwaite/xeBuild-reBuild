"""parseDump without the dead blk >= 0 test: the body nested under the tests (the author's favourite) instead of continue/goto.  Watching entry and tail (irfq.py)."""
import os
BASE = 'src/image_read.c'
FOCUS = ['_parseDump']
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', BASE), newline='').read().replace('\r\n', '\n')
_a = _src.index('		/* blk >= 0 is always true')
_b = _src.index('		if (dst != blk) {\n			if (blk >= blocks - 32)')
_c = _src.index('next:\n		;\n')
OLD = _src[_a:_c + len('next:\n		;\n')]
TAIL = _src[_b:_c]
L1 = 'log_printf(1, "bad block at 0x%x (raw offset 0x%x), block ignored\\n", blk, src - raw);\nif (!addRemap(blk, dst, blocks))\nreturn 0;\n'
L3 = 'log_printf(0, "***** WARNING: nanddump.bin has a bad LBA at block 0x%x (raw offset 0x%x), block LBA ignored\\n", blk, src - raw);\n'
L6 = ('log_printf(0, "***** WARNING: nanddump.bin has a mixed controller LBA at block 0x%x (raw offset 0x%x), block ignored\\n", blk, src - raw);\n'
      'log_printf(0, "               this is likely caused by previously using jaspersb on a jasper type console!\\n", blk, src - raw);\n')
L4 = ('if (dst == -4) {\nlog_printf(1, "ECD error at block 0x%x (raw offset 0x%x), block will be remapped\\n", blk, src - raw);\n'
      'if (!addRemap(blk, -1, blocks))\nreturn 0;\ndst = blk;\n}\n')
REST = L4 + TAIL


def seq(e1, e3, e6, rest=REST):
    """each arm leaves the loop body with its own exit"""
    return f'if (dst == -1) {{\n{L1}{e1}}}\nif (dst == -3) {{\n{L3}{e3}}}\nif (dst == -6) {{\n{L6}{e6}}}\n{rest}'


def chain(rest=REST):
    return f'if (dst == -1) {{\n{L1}}} else if (dst == -3) {{\n{L3}}} else if (dst == -6) {{\n{L6}}} else {{\n{rest}}}\n'


def nch(rest=REST):
    return (f'if (dst == -1) {{\n{L1}}} else {{\nif (dst == -3) {{\n{L3}}} else {{\nif (dst == -6) {{\n{L6}}} else {{\n{rest}}}\n}}\n}}\n')


def neg(rest=REST):
    return (f'if (dst != -1) {{\nif (dst != -3) {{\nif (dst != -6) {{\n{rest}}} else {{\n{L6}}}\n}} else {{\n{L3}}}\n}} else {{\n{L1}}}\n')


BODIES = {
    'sgc': seq('goto next;\n', 'continue;\n', 'continue;\n'),
    'scc': seq('continue;\n', 'continue;\n', 'continue;\n'),
    'sgg': seq('goto next;\n', 'goto next;\n', 'goto next;\n'),
    'chain': chain(),
    'nch': nch(),
    'neg': neg(),
}
TOP = {
    'cont': lambda b: 'if (dst == -2)\ncontinue;\n' + b,
    'goto': lambda b: 'if (dst == -2)\ngoto next;\n' + b,
    'wrap': lambda b: 'if (dst != -2) {\n' + b + '}\n',
    'chn2': lambda b: 'if (dst == -2) {\n} else {\n' + b + '}\n',
}
END = 'next:\n		;\n'
AX = []
for bk, b in BODIES.items():
    for tk, t in TOP.items():
        s = t(b)
        if 'next' in s:
            s += END
        AX.append((bk + '.' + tk, [(OLD, s)]))
AXES = [AX]
