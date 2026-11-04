# attempt 15: partial's forms on foraa (`&&` + block offset local): imgAdd's pad order is the race between the ifcombine `&` name and tail's (notes). A form with no threaded iftmp PHI might change who is on top after dce2.
import os, itertools
BASE = os.environ.get('IWB', 'build/iw/a14/foraa.c')
P0 = "		partial = type != 0 && type != '0' && len < 0x4000;\n"
T0 = '''		if (partial > 0) {
			if (len % 512)
				npages = (len + 512) / 512;
			else
				npages = len / 512;
		} else
			npages = 32;
'''
BODY = '''			if (len % 512)
				npages = (len + 512) / 512;
			else
				npages = len / 512;
'''
C = ["type != 0", "type != '0'", "len < 0x4000"]
A = []
for perm in itertools.permutations(C):
    ap = ' && '.join(perm)
    l = '_'.join(str(C.index(x)) for x in perm)
    A.append(('and' + l, [(P0, '		partial = %s;\n' % ap)]))
    A.append(('dir' + l, [(P0, ''), (T0, '		if (%s) {\n%s		} else\n			npages = 32;\n' % (ap, BODY))]))
    A.append(('tern' + l, [(P0, '		partial = %s ? 1 : 0;\n' % ap)]))
    A.append(('if0' + l, [(P0, '		partial = 0;\n		if (%s)\n			partial = 1;\n' % ap)]))
    A.append(('if1' + l, [(P0, '		if (%s)\n			partial = 1;\n		else\n			partial = 0;\n' % ap)]))
    A.append(('np' + l, [(P0, ''), (T0, '		npages = 32;\n		if (%s) {\n%s		}\n' % (ap, BODY))]))
A.append(('nest', [(P0, ''), (T0, "		npages = 32;\n		if (type != 0)\n			if (type != '0')\n				if (len < 0x4000) {\n%s				}\n" % BODY)]))
A.append(('small', [(P0, "		partial = type != 0 && type != '0';\n		partial = partial && len < 0x4000;\n")]))
A.append(('small2', [(P0, "		small = type != 0 && type != '0';\n		partial = small && len < 0x4000;\n"), ('	int partial;\n', '	int partial;\n	_Bool small;\n')]))
T = [('', []), ('t1', [('		if (partial > 0) {\n', '		if (partial) {\n')]), ('t2', [('		if (partial > 0) {\n', '		if (partial == 1) {\n')])]
def safe(a):
    return a
AXES = [A]
FLAGS = []
