"""cur2.py: stage-2 base: reboot test without expect (x_gt), -ip arm g1, plain -O3 matches.  BASE, OLDW (writeImage block with hints), ERR."""
import gen1base as g1
import gen3base as g3
import gen5base as g
import mkcur

L = g1.LOG
IP_G1 = """			i++;
			ip = argv[i];
			if (i == argc)
				goto iperr;
			if (!ip || *ip == '-') {
			iperr:
				%s			}
""" % L
A = """				if (!ret)
					netReboot(2);
				else {
					%s				}
""" % g.W
REB = """			{
				int reboot = !noReboot;

				if (reboot > 0) {
%s				}
			}
""" % A
BASE = g.BASE.replace(g.OLD, REB).replace(mkcur.IP_NEW, IP_G1)
OLDW = g3.OLD
ERR = g3.ERR
