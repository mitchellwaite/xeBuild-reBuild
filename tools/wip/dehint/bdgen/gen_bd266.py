"""Attempt 15, lab_none: the precheck's spelling picks its opcode heuristic (gen_bd261's lever), with no cold label.
`<= 1` gets positive (73% false); `< 2`, `== 1` (nonequal), `!= 0`-style and signed forms get other ones.  Axes:
spelling x goto none / return 0.  Runs on src/build.c after the lab_badsize landing."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun

OLD = '''	if ((uint32_t)xb.nFiles <= 1)
		goto none;
'''
LAB = 'none: __attribute__((cold));\n'
SP = {
    'le1': '(uint32_t)xb.nFiles <= 1',
    'lt2': '(uint32_t)xb.nFiles < 2',
    'sle1': 'xb.nFiles <= 1',
    'slt2': 'xb.nFiles < 2',
    'eq1': 'xb.nFiles == 1',
    'ngt1': '!((uint32_t)xb.nFiles > 1)',
    'nlt': '!(1 < (uint32_t)xb.nFiles)',
}


def mk(t, s, how):
    if how == 'goto':
        t = bdrun.sub(t, OLD, '	if (%s)\n		goto none;\n' % SP[s], 1)
        t = bdrun.sub(t, LAB, 'none:\n', 1)
    else:
        t = bdrun.sub(t, OLD, '	if (%s)\n		return 0;\n' % SP[s], 1)
        t = bdrun.sub(t, '	return 0;\n' + LAB + '	return 0;\n', '	return 0;\n', 1)
    return t


def CASES(base):
    return [('%s %s' % (s, h), lambda b, s=s, h=h: mk(b, s, h)) for s, h in itertools.product(SP, ('goto', 'ret'))]


FOCUS = ['_loadConsoleBlFiles']
