"""axes.py: building blocks for full-source variants with no dn block.  build(top, reb, err, ip) -> source text."""
import cur2
import cur3
import gen1base as g1
import gen5base as g5
import strip

L = g1.LOG
BASE0 = cur3.NODN  # has REB (x_gt), WNEW, IP_G1
assert cur2.REB in BASE0 and cur3.WNEW in BASE0 and cur2.IP_G1 in BASE0
W = g5.W
A = cur2.A


def reb(pre, c):
    return """			{
				%s

				if (%s) {
%s				}
			}
""" % (pre, c, A)


REB = {
    'plain': """			if (!noReboot) {
%s			}
""" % A,
    'x_gt': cur2.REB,
    'z2': reb('int reboot = 1; if (noReboot) reboot = 0;', 'reboot > 0'),
    'z1': reb('int y = 0; if (noReboot) y = 1;', 'y != 1'),
}


def err(pre, c):
    return """			if (dumpDir) {
				r = writeImage(xb.outName);
				{
					%s

					if (%s)
						%s
				}
				log_printf(0, separator);
			}
""" % (pre, c, cur2.ERR)


ERRS = {
    'ok_le': cur3.WNEW,
    'ok_lt': err('int ok = !r;', 'ok < 1'),
    'plain': """			if (dumpDir) {
				r = writeImage(xb.outName);
				if (r)
					%s
				log_printf(0, separator);
			}
""" % cur2.ERR,
}
IPS = {
    'b': """			i++;
			if (!argv[i] || i == argc || *argv[i] == '-') {
				%s			}
			ip = argv[i];
""" % L,
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
    'g1': cur2.IP_G1,
    'g2': """			i++;
			ip = argv[i];
			if (!ip)
				goto iperr;
			if (i == argc || *ip == '-') {
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
HEAD = """	int ret, r;

	if (getConsoleFiles(dumpDir)) {
		updating = 1;
		ret = buildImage();
		if (!ret) {
"""
assert HEAD in BASE0
TOP = {
    'top_ret': """	int ret, r;

	if (!pret)
		return;
	if (getConsoleFiles(dumpDir)) {
		updating = 1;
		ret = buildImage();
		if (!ret) {
""",
    'and_pret': """	int ret, r;

	if (getConsoleFiles(dumpDir)) {
		updating = 1;
		ret = buildImage();
		if (!ret && pret) {
""",
    'pret_and': """	int ret, r;

	if (getConsoleFiles(dumpDir)) {
		updating = 1;
		ret = buildImage();
		if (pret && !ret) {
""",
    'gcf_and': """	int ret, r;

	if (pret && getConsoleFiles(dumpDir)) {
		updating = 1;
		ret = buildImage();
		if (!ret) {
""",
}


def build(top, r, e, i):
    t = BASE0.replace(HEAD, top).replace(cur2.REB, r).replace(cur3.WNEW, e).replace(cur2.IP_G1, i)
    return t
