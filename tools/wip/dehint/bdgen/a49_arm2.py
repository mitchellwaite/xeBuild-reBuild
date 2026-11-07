"""Attempt 49: on the landed source (loadXell + loadBl24, exp_t10 gone), forms of case 24's
second arm.  python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a49_arm2.py"""
import os
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'src', 'build.c')
A2 = '''					r = 0;
					if (loadBaseFile(e->name, e))
						r = defaultBl60(e);
					else if (e->size != 0x60)
						r = defaultBl60(e);
'''
LAB = '\t\t\t\tdevgl: __attribute__((hot));\n'
V = {
 'src': [],
 'call': [(A2, '\t\t\t\t\tr = loadBl24(e);\n')],
 'call_nolab': [(A2, '\t\t\t\t\tr = loadBl24(e);\n'), (LAB, '')],
 'nor0': [(A2, A2.replace('\t\t\t\t\tr = 0;\n', ''))],
 'else0': [(A2, '''					if (loadBaseFile(e->name, e))
						r = defaultBl60(e);
					else if (e->size != 0x60)
						r = defaultBl60(e);
					else
						r = 0;
''')],
 'or': [(A2, '''					r = 0;
					if (loadBaseFile(e->name, e) || e->size != 0x60)
						r = defaultBl60(e);
''')],
}
