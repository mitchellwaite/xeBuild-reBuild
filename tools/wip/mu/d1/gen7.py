"""gen7.py: -ip arm forms combined with the no-expect reboot tests, under plain -O3 and with the param kept."""
import gen1base as g1
import gen5base as g
import mkcur
import sw

L = g1.LOG
IPN = mkcur.IP_NEW
IPS = {
    'b': IPN,
    'a': """			i++;
			ip = argv[i];
			if (!argv[i] || i == argc || *argv[i] == '-') {
				%s			}
""" % L,
    'd': """			i++;
			ip = argv[i];
			if (!argv[i] || i == argc || *ip == '-') {
				%s			}
""" % L,
    'g2': """			i++;
			ip = argv[i];
			if (!ip)
				goto iperr;
			if (i == argc || *ip == '-') {
			iperr:
				%s			}
""" % L,
    'g1': """			i++;
			ip = argv[i];
			if (i == argc)
				goto iperr;
			if (!ip || *ip == '-') {
			iperr:
				%s			}
""" % L,
    'c': """			i++;
			if (i == argc || !argv[i] || *argv[i] == '-') {
				%s			}
			ip = argv[i];
""" % L,
    'cp': g1.IP_OLD_FULL,
}
A = """				if (!ret)
					netReboot(2);
				else {
					%s				}
""" % g.W
R = {
    'x_gt': ('int x = !noReboot;', 'x > 0'),
    'z1': ('int y = 0; if (noReboot) y = 1;', 'y != 1'),
    'z2': ('int y = 1; if (noReboot) y = 0;', 'y > 0'),
}
vs = []
for ik, iv in IPS.items():
    for rk, (pre, c) in R.items():
        t = g.BASE.replace(g.OLD, """			{
				%s

				if (%s) {
%s				}
			}
""" % (pre, c, A)).replace(IPN, iv)
        vs.append((ik + '_' + rk, t))
for f in ['-O3', '-O3 --param builtin-expect-probability=68']:
    print(f)
    sw.run(vs, f, save='gen7', top=12)
