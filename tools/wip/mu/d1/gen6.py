"""gen6.py: spell the noReboot test so an opcode predictor sees a non-zero compare at profile_estimate, folding to == 0 later."""
import gen5base as g
import sw

A = """				if (!ret)
					netReboot(2);
				else {
					%s				}
""" % g.W
vs = []
for k, c, pre in [
    ('x_gt', 'x > 0', 'int x = !noReboot;'),
    ('x_ge', 'x >= 1', 'int x = !noReboot;'),
    ('y_ne1', 'y != 1', 'int y = noReboot != 0;'),
    ('y_lt1', 'y < 1', 'int y = noReboot != 0;'),
    ('b_ne', 'b != 1', '_Bool b = noReboot;'),
    ('b_eq0', 'b == 0', '_Bool b = noReboot;'),
    ('x2_ne', '(!noReboot) != 0', ''),
    ('e1', '!noReboot == 1', ''),
    ('n1', '!!noReboot != 1', ''),
    ('n2', '!!noReboot < 1', ''),
    ('c1', '(noReboot ? 1 : 0) != 1', ''),
    ('c2', '(noReboot ? 0 : 1) > 0', ''),
    ('z1', 'y != 1', 'int y = 0; if (noReboot) y = 1;'),
    ('z2', 'y > 0', 'int y = 1; if (noReboot) y = 0;'),
    ('z3', 'y > 0', 'int y; if (noReboot) y = 0; else y = 1;'),
    ('u1', 'u < 1', 'unsigned u = noReboot;'),
    ('u2', 'u <= 0', 'unsigned u = noReboot;'),
    ('s1', 's <= 0', 'unsigned u = noReboot; int s = u != 0;'),
]:
    vs.append((k, g.BASE.replace(g.OLD, """			{
				%s

				if (%s) {
%s				}
			}
""" % (pre, c, A))))
sw.run(vs, '-O3', save='gen6')
