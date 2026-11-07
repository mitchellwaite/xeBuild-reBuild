"""Attempt 48: every combination of the loadBlFiles-side items (exp_pr as the expect, plain or
`(int)r < 0`; the barrier on/off; the devgl label on/off; exp_t10 on/off), lab_none (label,
precheck, both) and exp_devgl, on src/build.c.  Functions are scored separately by a46run, so
the joint question per param is whether one row per function is clean at the same p.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a48_combo.py -p 0,90,91,92,93,94,95,96,97,98,99"""
import os, itertools
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'src', 'build.c')
T10 = ('} else if (__builtin_expect(type == 10, 0)) {', '} else if (type == 10) {')
PR = {'e': None, 'p': ('if (__builtin_expect(r != 0, 0))\n', 'if (r != 0)\n'),
      'n': ('if (__builtin_expect(r != 0, 0))\n', 'if ((int)r < 0)\n')}
BAR = ('\t\t\t\t__asm__ __volatile__("");\n', '')
LAB = ('\t\t\t\tdevgl: __attribute__((hot));\n', '')
NONEP = ('\tif ((uint32_t)xb.nFiles <= 1)\n\t\tgoto none;\n', '')
NONEL = ('none: __attribute__((cold));\n', 'none:\n')
NONEB = ('none: __attribute__((cold));\n\treturn 0;\n', '')
DEV = ('if (__builtin_expect(xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16, 0))',
       'if (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16)')
V = {}
for pr, bar, lab, t10 in itertools.product('epn', (0, 1), (0, 1), (0, 1)):
    e = []
    if PR[pr]:
        e.append(PR[pr])
    if bar:
        e.append(BAR)
    if lab:
        e.append(LAB)
    if t10:
        e.append(T10)
    V['L_%s%s%s%s' % (pr, 'B' if bar else '', 'D' if lab else '', 'T' if t10 else '')] = e
V['C_lab'] = [NONEL]
V['C_both'] = [NONEP, NONEB]
V['F_dev'] = [DEV]
