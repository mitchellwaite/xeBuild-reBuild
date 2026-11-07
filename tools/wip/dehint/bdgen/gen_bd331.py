"""Attempt 22, lab_none: the precheck and cold label gone (the plain `for`, 4/8), with loadConsoleBlFiles' case 24 in
forms that raise the defaultBl60 call sites' flow at profile_estimate (r = 1 is sites x 10.1%; it has 136 -> 14 and
needs more than the not-entered return's 20, so the sites need about 200).  `||` gives one call block with two
predecessors, so neither test gets PRED_CALL (50% and nonequal 72%: 179 -> 18); the glitch2mfg test is 29% (PRED_CALL
on loadBaseFile's block) in every form where loadBaseFile follows it.  Runs on src as of c941f014."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun

PRE_OLD = '\tif ((uint32_t)xb.nFiles <= 1)\n\t\tgoto none;\n'
END_OLD = '\treturn 0;\nnone: __attribute__((cold));\n\treturn 0;\n}'
C24_OLD = '''			case 24:
				if (!xb.glitch2mfg)
					break;
				if (loadBaseFile(e->name, e))
					r = defaultBl60(e);
				else if (e->size != 0x60)
					r = defaultBl60(e);
				break;
'''
C24 = {
    'two': C24_OLD,
    'or': '''			case 24:
				if (!xb.glitch2mfg)
					break;
				if (loadBaseFile(e->name, e) || e->size != 0x60)
					r = defaultBl60(e);
				break;
''',
    'andor': '''			case 24:
				if (xb.glitch2mfg && (loadBaseFile(e->name, e) || e->size != 0x60))
					r = defaultBl60(e);
				break;
''',
    'nest': '''			case 24:
				if (xb.glitch2mfg) {
					if (loadBaseFile(e->name, e))
						r = defaultBl60(e);
					else if (e->size != 0x60)
						r = defaultBl60(e);
				}
				break;
''',
    'eq': '''			case 24:
				if (!xb.glitch2mfg)
					break;
				if (!loadBaseFile(e->name, e) && e->size == 0x60)
					break;
				r = defaultBl60(e);
				break;
''',
}
FOCUS = ['_loadConsoleBlFiles']


def mk(b, c, pre):
    b = bdrun.sub(b, C24_OLD, C24[c], 1)
    if pre == 'none':
        b = bdrun.sub(b, PRE_OLD, '', 1)
        b = bdrun.sub(b, END_OLD, '\treturn 0;\n}', 1)
    return b


def CASES(base):
    return [('%s %s' % (c, p), lambda b, c=c, p=p: mk(b, c, p)) for c in C24 for p in ('none', 'keep')
            if (c, p) != ('two', 'keep')]
