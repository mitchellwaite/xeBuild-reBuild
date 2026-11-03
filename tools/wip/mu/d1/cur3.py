"""cur3.py: stage-3 base: cur2 + `int ok = !r; if (ok <= 0)` for the writeImage error.  python cur3.py writes cur.c (with dn) and nodn.c (without)."""
import os

import cur2
import strip

HERE = os.path.dirname(os.path.abspath(__file__))
WNEW = """			if (dumpDir) {
				r = writeImage(xb.outName);
				{
					int ok = !r;

					if (ok <= 0)
						%s
				}
				log_printf(0, separator);
			}
""" % cur2.ERR
BASE = cur2.BASE.replace(cur2.OLDW, WNEW)
DN = strip.R['dn'][0][0]
assert DN in BASE
NODN = BASE.replace(DN, '')

if __name__ == '__main__':
    for n, t in (('cur.c', BASE), ('nodn.c', NODN)):
        with open(os.path.join(HERE, n), 'w', newline='\n') as f:
            f.write(t)
