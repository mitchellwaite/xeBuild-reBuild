# attempt 12: the guard : head ratio also follows the outer loop's iteration estimate: a second exit halves PRED_LOOP_EXIT (9 / n_exits), which would halve the head relative to the guard. Size up: one dead `break` in imgAdd's outer loop, replacing lnp2 and pin_t (net -1).
import os
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_near11.c')
TOP = '	for (b = 0; b < blocks; b++) {\n		/* blk'
BL = '		blk = start + b;\n'
PA = "		partial = (len < 0x4000) & (type != 0) & (type != '0');\n"
PP = '		p = 0;\n		if ((uint8_t)t < 15) {\n'
END = '''			}
		}
	}
#undef BLK'''
XS = {'g': '(off & 0x3fff) > 0x3fff', 'x': 'x > 0x3fff', 'f': 'first > 0x4000', 'n': '(int)(x) < 0'}
A = [('', [])]
for n, x in XS.items():
    br = '		if (%s)\n			break;\n' % x
    A.append(('t' + n, [(BL, br + BL)]))
    A.append(('a' + n, [(PA, br + PA)]))
    A.append(('p' + n, [(PP, br + PP)]))
    A.append(('e' + n, [(END, '			}\n		}\n' + br + '	}\n#undef BLK')]))
AXES = [A]
FLAGS = []
