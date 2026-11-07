"""Attempt 47: the tail's `r` test (exp_pr) and the fail: barrier on src as of 5877c248.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a47_pr.py"""
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


def tail(new):
    return [(TAIL, new)]


def T(test):
    return tail(TAIL.replace('__builtin_expect(r != 0, 0)', test))


KIT = '''				if (xb.type > BUILD_DEVGL16) {
					if (type == 14)
						setFlashBuild(getBeU16(xb.files[i].data + 2));
					break;
				}
				if (%s)
					goto fail;
				break;
'''
ELSE = '''				if (xb.type > BUILD_DEVGL16 && type == 14)
					setFlashBuild(getBeU16(xb.files[i].data + 2));
				else if (%s)
					goto fail;
				break;
'''
BRK = '''				if (xb.type <= BUILD_DEVGL16)
					break;
				if (type == 14)
					setFlashBuild(getBeU16(xb.files[i].data + 2));
				break;
'''
BRK2 = '''				if (xb.type > BUILD_DEVGL16 && type == 14)
					setFlashBuild(getBeU16(xb.files[i].data + 2));
				break;
'''
base = {
 'src': [],
 'ne': T('r != 0'),
 'r': T('r'),
 'eqm1': T('r == -1'),
 'eqm1u': T('r == (uint32_t)-1'),
 'neg': T('(int)r < 0'),
 'gt1': T('r > 1'),
 'kit_r': tail(KIT % 'r'),
 'kit_m1': tail(KIT % 'r == -1'),
 'kit_neg': tail(KIT % '(int)r < 0'),
 'else_r': tail(ELSE % 'r'),
 'else_m1': tail(ELSE % 'r == -1'),
 'brk': tail(BRK),
 'brk2': tail(BRK2),
}
V = {}
for k, v in base.items():
    V[k] = v
    V[k + '+nobar'] = v + [BAR]
V2 = {'else_neg': tail(ELSE % '(int)r < 0'), 'else_neg+nobar': tail(ELSE % '(int)r < 0') + [BAR],
      'neg_neq': T('(int)r < 0 && r != 0'), 'neg_le': T('(int)r <= -1')}
V.update(V2)
