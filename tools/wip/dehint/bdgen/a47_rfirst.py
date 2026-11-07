"""Attempt 47: the tail with the r test first (r is -1 only after a signature failure).
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a47_rfirst.py"""
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
BAR = ('\t\t\t\t__asm__ __volatile__("");\n', '')
F1 = '''				if (%s && xb.type <= BUILD_DEVGL16)
					goto fail;
				if (xb.type > BUILD_DEVGL16 && type == 14)
					setFlashBuild(getBeU16(xb.files[i].data + 2));
				break;
'''
F2 = '''				if (%s) {
					if (xb.type <= BUILD_DEVGL16)
						goto fail;
				}
				if (xb.type > BUILD_DEVGL16 && type == 14)
					setFlashBuild(getBeU16(xb.files[i].data + 2));
				break;
'''
F3 = '''				if (xb.type > BUILD_DEVGL16) {
					if (type == 14)
						setFlashBuild(getBeU16(xb.files[i].data + 2));
				} else if (%s)
					goto fail;
				break;
'''
F4 = '''				if (xb.type <= BUILD_DEVGL16) {
					if (%s)
						goto fail;
				} else if (type == 14)
					setFlashBuild(getBeU16(xb.files[i].data + 2));
				break;
'''
V = {}
for fk, f in {'and': F1, 'nest': F2, 'kitelse': F3, 'else14': F4}.items():
    for tk, t in {'r': 'r', 'neg': '(int)r < 0', 'm1': 'r == -1'}.items():
        V[fk + '_' + tk] = [(TAIL, f % t)]
        V[fk + '_' + tk + '+nobar'] = [(TAIL, f % t), BAR]
