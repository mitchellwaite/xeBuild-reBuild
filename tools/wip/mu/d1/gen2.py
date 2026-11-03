"""gen2.py: -ip arm written like its siblings (argv[i] tests)."""
import gen1base as g
import sw
vs = []
L = g.LOG
OLD = g.IP_OLD_FULL
for k, v in {
    'a': """			i++;
			ip = argv[i];
			if (!argv[i] || i == argc || *argv[i] == '-') {
				%s			}
""" % L,
    'b': """			i++;
			if (!argv[i] || i == argc || *argv[i] == '-') {
				%s			}
			ip = argv[i];
""" % L,
    'c': """			i++;
			if (i == argc || !argv[i] || *argv[i] == '-') {
				%s			}
			ip = argv[i];
""" % L,
    'd': """			i++;
			ip = argv[i];
			if (!argv[i] || i == argc || *ip == '-') {
				%s			}
""" % L,
    'e': """			i++;
			if (!argv[i] || i == argc || *argv[i] == '-') {
				%s			}
			log_printf(0, "setting forced IP to %%s\\n", argv[i]);
			ip = argv[i];
			if (0)
""" % L,
}.items():
    assert OLD in g.BASE
    vs.append((k, g.BASE.replace(OLD, v)))
sw.run(vs, g.P68)
