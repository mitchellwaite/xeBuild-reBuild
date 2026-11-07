"""Attempt 54: exp_pr by the tail's test order: type == 14 first (r is 0 there), so the
`xb.type > 5` test guards setFlashBuild directly (PRED_CALL on it), the r test after.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a54_t14.py [-p 0,99]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H

BASE = H.BASE
OLD = '''				if (xb.type <= BUILD_DEVGL16) {
					if (__builtin_expect(r != 0, 0))
						goto fail;
					break;
				}
				if (type == 14)
					setFlashBuild(getBeU16(xb.files[i].data + 2));
				break;
'''
SB = 'setFlashBuild(getBeU16(xb.files[i].data + 2));'
T = {
 'a': '''				if (type == 14) {
					if (xb.type > BUILD_DEVGL16)
						%s
					break;
				}
				if (xb.type <= BUILD_DEVGL16 && R)
					goto fail;
				break;
''' % SB,
 'b': '''				if (type == 14) {
					if (xb.type > BUILD_DEVGL16)
						%s
				} else if (xb.type <= BUILD_DEVGL16 && R)
					goto fail;
				break;
''' % SB,
 'c': '''				if (type == 14 && xb.type > BUILD_DEVGL16)
					%s
				else if (xb.type <= BUILD_DEVGL16 && R)
					goto fail;
				break;
''' % SB,
 'd': '''				if (type == 14) {
					if (xb.type > BUILD_DEVGL16)
						%s
					break;
				}
				if (xb.type <= BUILD_DEVGL16) {
					if (R)
						goto fail;
				}
				break;
''' % SB,
 'e': '''				if (xb.type > BUILD_DEVGL16) {
					if (type == 14)
						%s
					break;
				}
				if (R)
					goto fail;
				break;
''' % SB,
}
RS = {'r': 'r', 'n': '(int)r < 0', 'x': '__builtin_expect(r != 0, 0)'}
V = {}
for k, s in T.items():
    for rk, rs in RS.items():
        V[k + rk] = [(OLD, s.replace('R', rs).replace('BUILD_DEVGL16 && r', 'BUILD_DEVGL16 && r') )]
