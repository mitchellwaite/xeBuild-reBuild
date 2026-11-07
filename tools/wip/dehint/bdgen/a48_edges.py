"""Attempt 48, diagnostics for exp_pr's alignment: the SE block is 7 at profile_estimate
(bb14 298 x 0.28^3 = 6.54) and must be <= 6 so that its copies round to 3 and 1; that needs
loadBlFiles' switch block (7162 / 12 edges) about 1% lower.  Probe it with a 13th switch edge
(a duplicate of the default's log under `case 26:`; diagnostic only, it is not natural code).
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a48_edges.py"""
import os
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'src', 'build.c')
NEG = ('if (__builtin_expect(r != 0, 0))\n', 'if ((int)r < 0)\n')
D = '\t\t\tdefault:\n\t\t\t\tlog_printf(1, "####### unhandled bl load %d %s\\n", type, e->name);\n\t\t\t\tbreak;\n\t\t\t}\n\t\t}\n\t\tif (r) {\n\t\t\tlog_printf(0, "\\n\\n**** could not read'
D26 = '\t\t\tcase 26:\n\t\t\t\tlog_printf(1, "####### unhandled bl load %d %s\\n", type, e->name);\n\t\t\t\tbreak;\n' + D
D0 = D26.replace('case 26:', 'case 0:', 1)
V = {
 'neg': [NEG],
 'neg_c26': [NEG, (D, D26)],
 'neg_c0': [NEG, (D, D0)],
 'exp_c26': [(D, D26)],
}
