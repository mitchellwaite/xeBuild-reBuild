"""Attempt 60, after landing useBuiltIn + the fail label after the default case: a60_est.py's still-applicable
estimate edits and useBuiltIn's forms on the new src, for exp_pr / exp_devgl.
python tools/wip/dehint/bdgen/a60lib.py tools/wip/dehint/bdgen/a60_rest.py -o "-;exp_pr;exp_devgl" """
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a60_est as E
NEG = ('if (__builtin_expect(r != 0, 0))', 'if ((int)r < 0)')
UBODY = '\tmemcpy(e->data, data, size);\n'
V = {k: v for k, v in E.V.items() if k in ('base', 'salt0', 'nand_ka', 'nr_ret', 'nr_void', 'x_nest', 'x_r', 'bl60_loc', 'pcb_fn2')}
V['ub_mm'] = [(UBODY, UBODY.replace('memcpy', 'memmove'))]
V['ub_u32'] = [('static int useBuiltIn', 'static uint32_t useBuiltIn')]
V['ub_nest'] = [('''	e->data = malloc(size);
	if (!e->data)
		return 1;
	e->size = size;
	memcpy(e->data, data, size);
	return 0;
''', '''	e->data = malloc(size);
	if (e->data) {
		e->size = size;
		memcpy(e->data, data, size);
		return 0;
	}
	return 1;
''')]
V['bl60_mc'] = [('\tmemmove(e->data, defBl60, 0x60);\n', '\tmemcpy(e->data, defBl60, 0x60);\n')]
for k in list(V):
    V[k + '_neg'] = V[k] + [NEG]
SETS = {k: (['-', 'exp_devgl'] if k.endswith('_neg') else ['-', 'exp_pr', 'exp_devgl']) for k in V}
