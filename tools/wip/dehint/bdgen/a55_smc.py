"""Attempt 55: the SMC failure as `if (!e->offset) { fail: r = -1; }` (smcif) or `if (!e->offset) goto fail;`
with `fail:` after the default case (smcgoto_end), with and without the barrier, crossed with each
other hint off.  Without the barrier both are 1/7 (attempt 10's size-log line) where src is 58/220.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a55_smc.py [-p ..] [-k label]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H
BASE = H.BASE

SMC = '''				e->offset = smcSetLoad(e->size);
				if (e->offset)
					break;
				/* one -1 block for the patch size, SMC and (xb.type <=
				   BUILD_DEVGL16) signature failures: the asm keeps it a block
				   of its own (else the -1 is appended to the size log, which
				   crossjump can't then share) */
			fail:
				__asm__ __volatile__("");
				r = -1;
				break;
'''
DEF = '''				log_printf(1, "####### unhandled bl load %d %s\\n", type, e->name);
				break;
			}
'''


def smcif(bar):
    return [(SMC, '''				e->offset = smcSetLoad(e->size);
				if (!e->offset) {
			fail:
%s					r = -1;
				}
				break;
''' % ('\t\t\t\t\t__asm__ __volatile__("");\n' if bar else ''))]


def smcend(bar):
    return [(SMC, '''				e->offset = smcSetLoad(e->size);
				if (!e->offset)
					goto fail;
				break;
'''), (DEF, DEF.replace('\t\t\t}\n', '\t\t\tfail:\n%s\t\t\t\tr = -1;\n\t\t\t\tbreak;\n\t\t\t}\n'
                         % ('\t\t\t\t__asm__ __volatile__("");\n' if bar else '')))]


OFFS = {'': [], 'pr': [H.PR], 'lab': [('\t\t\t\tdevgl: __attribute__((hot));\n', '')],
        'neg': [('if (__builtin_expect(r != 0, 0))\n', 'if ((int)r < 0)\n')]}
V = {}
for nm, f in (('if', smcif), ('end', smcend)):
    for bar in (1, 0):
        for k, ed in OFFS.items():
            V['%s_%s%s' % (nm, 'b' if bar else 'nb', ('_' + k) if k else '')] = f(bar) + ed
