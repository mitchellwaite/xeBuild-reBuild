"""gen1.py: first natural-shape sweep.  Each axis is tried alone on the current hints (param 68 kept while expect remains).
Axes: -ip error edge (replaces cp(i+101)), writeImage error (replaces cp r+N and wok)."""
import strip
import sw

P68 = '-O3 --param builtin-expect-probability=68'
BASE = strip.apply(['noreeb'])
HU = """		hu:
			update_usage();
"""
BASE = BASE.replace("""		{
		hu:
			update_usage();
		}
""", """			update_usage();
""")

IP_OLD = """			if (cp(i + 101))
				goto iperr;
			if (i == argc || !ip || *ip == '-') {
			iperr:
				log_printf(0, "\\n\\n***** ERROR: option flag -ip on command line but no argument provided!\\n");
				update_usage();
			}
"""
LOG = """log_printf(0, "\\n\\n***** ERROR: option flag -ip on command line but no argument provided!\\n");
				update_usage();
"""
IPS = {
    'goto1': """			if (i == argc)
				goto iperr;
			if (!ip || *ip == '-') {
			iperr:
				%s			}
""" % LOG,
    'goto2': """			if (!ip)
				goto iperr;
			if (i == argc || *ip == '-') {
			iperr:
				%s			}
""" % LOG,
    'goto3': """			if (i == argc)
				goto iperr;
			if (!ip)
				goto iperr;
			if (*ip == '-') {
			iperr:
				%s			}
""" % LOG,
    'goto4': """			if (*ip == '-')
				goto iperr;
			if (i == argc || !ip) {
			iperr:
				%s			}
""" % LOG,
    'assign': """			if (i == argc || !(ip = argv[i]) || *ip == '-') {
				%s			}
""" % LOG,
    'nest': """			if (i != argc) {
				if (ip && *ip != '-')
					goto ipok;
			}
			%s		ipok:
""" % LOG,
    'nest2': """			if (i == argc || !ip)
				goto iperr;
			if (*ip == '-') {
			iperr:
				%s			}
""" % LOG,
}

vs = [('asis', BASE)]
for k, v in IPS.items():
    assert IP_OLD in BASE
    t = BASE.replace(IP_OLD, v)
    vs.append(('ip_' + k, t))
sw.run(vs, P68)
