"""Attempt 62 diagnostics (not natural, behaviour changes): does the SE chain close with 13 switch targets
(SE = 597 x 12/13), or with one loop exit?  python tools/wip/dehint/bdgen/a61_semeas.py tools/wip/dehint/bdgen/a62_diag.py"""
DEF = '\t\t\tdefault:\n\t\t\t\tlog_printf(1, "####### unhandled bl load %d %s'
V = {
    'c26_break': [(DEF, '\t\t\tcase 26:\n\t\t\t\tbreak;\n' + DEF)],
    'c0_break': [(DEF, '\t\t\tcase 0:\n\t\t\t\tbreak;\n' + DEF)],
}
LOG = '\t\t\t\tlog_printf(1, "####### unhandled bl load %d %s'
V['c26_dup'] = [(DEF, '\t\t\tcase 26:\n' + LOG + '\\n", type, e->name);\n\t\t\t\tbreak;\n' + DEF)]
V['c26_dup_tn'] = V['c26_dup'] + [('if (__builtin_expect(r != 0, 0))', 'if ((int)r < 0)')]
V['c26_dup_tr'] = V['c26_dup'] + [('if (__builtin_expect(r != 0, 0))', 'if (r != 0)')]
