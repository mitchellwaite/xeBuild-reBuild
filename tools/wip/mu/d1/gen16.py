"""gen16.py: more spellings of the -ip test on the flashConsole base (plain reboot test, ok <= 0)."""
import axes as a
import gen1base as g1
import gen14
import sw

L = g1.LOG
FORMS = {
    'g1': a.IPS['g1'],
    'c': a.IPS['c'],
    'b': a.IPS['b'],
    'assign': """			i++;
			if (i == argc || !(ip = argv[i]) || *ip == '-') {
				%s			}
""" % L,
    'c2': """			i++;
			ip = argv[i];
			if (i == argc || !argv[i] || *ip == '-') {
				%s			}
""" % L,
    'c3': """			i++;
			ip = argv[i];
			if (i == argc || !argv[i] || *argv[i] == '-') {
				%s			}
""" % L,
    'n1': """			i++;
			ip = argv[i];
			if (i == argc || (!ip || *ip == '-')) {
				%s			}
""" % L,
    'n2': """			ip = argv[++i];
			if (i == argc || !ip || *ip == '-') {
				%s			}
""" % L,
    'n3': """			ip = argv[i + 1];
			i++;
			if (i == argc || !ip || *ip == '-') {
				%s			}
""" % L,
    'n4': """			i++;
			if (i != argc) {
				ip = argv[i];
				if (ip && *ip != '-')
					goto ipok;
			}
			%s		ipok:
""" % L,
    'n5': """			i++;
			ip = argv[i];
			if (i != argc && ip && *ip != '-')
				goto ipok;
			%s		ipok:
""" % L,
    'n6': """			i++;
			ip = argv[i];
			if (i == argc || !ip || !*ip || *ip == '-') {
				%s			}
""" % L,
    'n7': """			i++;
			ip = i == argc ? NULL : argv[i];
			if (!ip || *ip == '-') {
				%s			}
""" % L,
    'n8': """			i++;
			ip = argv[i];
			if (i == argc || ip == NULL || ip[0] == '-') {
				%s			}
""" % L,
    'n9': """			i++;
			ip = argv[i];
			{
				int bad = i == argc;

				if (bad || !ip || *ip == '-') {
					%s				}
			}
""" % L,
    'n10': """			i++;
			ip = argv[i];
			if (i == argc) {
				%s			}
			if (!ip || *ip == '-') {
				%s			}
""" % (L, L),
    'n11': """			{
				char *arg = argv[++i];

				if (i == argc || !arg || *arg == '-') {
					%s				}
				ip = arg;
			}
""" % L,
}
if __name__ == '__main__':
    vs = []
    for k, v in FORMS.items():
        s = a.build(a.HEAD, a.REB['plain'], a.ERRS['ok_le'], v)
        vs.append((k, gen14.split(s)))
    sw.run(vs, '-O3', save='gen16')
