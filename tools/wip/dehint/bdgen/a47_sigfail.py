"""Attempt 47: the xb.type <= 5 exit in the signature-failed arm itself, the tail without an r test.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a47_sigfail.py"""
import os
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'src', 'build.c')
TAIL = '''				if (xb.type <= BUILD_DEVGL16) {
					if (__builtin_expect(r != 0, 0))
						goto fail;
					break;
				}
				if (type == 14)
					setFlashBuild(getBeU16(xb.files[i].data + 2));
				break;
'''
SF = '''							log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);
							r = -1;
'''
BAR = ('\t\t\t\t__asm__ __volatile__("");\n', '')
T_BRK = '''				if (xb.type <= BUILD_DEVGL16)
					break;
				if (type == 14)
					setFlashBuild(getBeU16(xb.files[i].data + 2));
				break;
'''
T_AND = '''				if (xb.type > BUILD_DEVGL16 && type == 14)
					setFlashBuild(getBeU16(xb.files[i].data + 2));
				break;
'''
T_KIT = '''				if (xb.type > BUILD_DEVGL16) {
					if (type == 14)
						setFlashBuild(getBeU16(xb.files[i].data + 2));
				}
				break;
'''
S1 = SF.replace('\t\t\t\t\t\t\tr = -1;\n', '\t\t\t\t\t\t\tif (xb.type <= BUILD_DEVGL16)\n\t\t\t\t\t\t\t\tgoto fail;\n\t\t\t\t\t\t\tr = -1;\n')
S2 = SF.replace('\t\t\t\t\t\t\tr = -1;\n', '\t\t\t\t\t\t\tr = -1;\n\t\t\t\t\t\t\tif (xb.type <= BUILD_DEVGL16)\n\t\t\t\t\t\t\t\tgoto fail;\n')
S3 = SF.replace('\t\t\t\t\t\t\tr = -1;\n', '\t\t\t\t\t\t\tif (xb.type <= BUILD_DEVGL16)\n\t\t\t\t\t\t\t\tgoto fail;\n\t\t\t\t\t\t\telse\n\t\t\t\t\t\t\t\tr = -1;\n')
V = {}
for sk, s in {'s1': S1, 's2': S2, 's3': S3}.items():
    for tk, t in {'brk': T_BRK, 'and': T_AND, 'kit': T_KIT}.items():
        V[sk + tk] = [(SF, s), (TAIL, t)]
        V[sk + tk + '+nobar'] = [(SF, s), (TAIL, t), BAR]
