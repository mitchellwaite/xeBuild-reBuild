"""Attempt 48: lab_none without the precheck and label is 4/8: the not-entered return (20) is
taken before the r = 1 block (14) in bb-reorder's last round.  The r = 1 block would pass it at
>= 21, which the glitch2mfg guard at 50% instead of 71% (PRED_CALL on loadBaseFile's block)
gives (about 24).  Forms of console's case 24 guard, all without the precheck and label.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a48_none.py"""
import os
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'src', 'build.c')
NONEP = ('\tif ((uint32_t)xb.nFiles <= 1)\n\t\tgoto none;\n', '')
NONEB = ('none: __attribute__((cold));\n\treturn 0;\n', '')
C24 = '''				if (!xb.glitch2mfg)
					break;
				if (loadBaseFile(e->name, e))
					r = defaultBl60(e);
				else if (e->size != 0x60)
					r = defaultBl60(e);
				break;
			case 25:'''
F = {
 'base': None,
 'or': '''				if (!xb.glitch2mfg)
					break;
				if (loadBaseFile(e->name, e) || e->size != 0x60)
					r = defaultBl60(e);
				break;
			case 25:''',
 'nest': '''				if (xb.glitch2mfg) {
					if (loadBaseFile(e->name, e))
						r = defaultBl60(e);
					else if (e->size != 0x60)
						r = defaultBl60(e);
				}
				break;
			case 25:''',
 'and2': '''				if (xb.glitch2mfg && loadBaseFile(e->name, e))
					r = defaultBl60(e);
				else if (xb.glitch2mfg && e->size != 0x60)
					r = defaultBl60(e);
				break;
			case 25:''',
 'brk2': '''				if (!xb.glitch2mfg)
					break;
				if (!loadBaseFile(e->name, e) && e->size == 0x60)
					break;
				r = defaultBl60(e);
				break;
			case 25:''',
 'and1': '''				if (xb.glitch2mfg && (loadBaseFile(e->name, e) || e->size != 0x60))
					r = defaultBl60(e);
				break;
			case 25:''',
}
V = {}
for k, f in F.items():
    e = [NONEP, NONEB]
    if f:
        e.append((C24, f))
    V['c_' + k] = e
    V['cl_' + k] = [(C24, f)] if f else []
