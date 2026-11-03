"""gen8.py: writeImage error test spelled so an opcode predictor lowers it (replaces cp r+N and wok).  With the x_gt reboot test, g1 -ip arm, plain -O3."""
import cur2
import sw

vs = []
E = cur2.ERR
for k, pre, c in [
    ('plain', '', 'r'),
    ('ok_lt', 'int ok = !r;', 'ok < 1'),
    ('ok_le', 'int ok = !r;', 'ok <= 0'),
    ('ok_ne', 'int ok = !r;', 'ok != 1'),
    ('bad_eq', 'int bad = r != 0;', 'bad == 1'),
    ('f1', 'int ok = 1; if (r) ok = 0;', 'ok <= 0'),
    ('f2', 'int ok = 1; if (r) ok = 0;', 'ok != 1'),
    ('f3', 'int bad = 0; if (r) bad = 1;', 'bad == 1'),
    ('f4', 'int bad = 0; if (r) bad = 1;', 'bad > 0'),
    ('f5', 'int ok = 0; if (!r) ok = 1;', 'ok <= 0'),
    ('f6', 'int ok = 0; if (!r) ok = 1;', 'ok != 1'),
    ('f7', 'int bad = 1; if (!r) bad = 0;', 'bad == 1'),
]:
    vs.append((k, cur2.BASE.replace(cur2.OLDW, """			if (dumpDir) {
				r = writeImage(xb.outName);
				{
				%s
				if (%s)
					%s
				}
				log_printf(0, separator);
			}
""" % (pre, c, E))))
sw.run(vs, '-O3', save='gen8')
