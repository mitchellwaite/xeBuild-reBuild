"""gen1base.py: BASE = src minus noreeb memset and the hu block; IP_OLD_FULL/LOG for the -ip arm."""
import strip
P68 = '-O3 --param builtin-expect-probability=68'
BASE = strip.apply(['noreeb']).replace("""		{
		hu:
			update_usage();
		}
""", """			update_usage();
""")
LOG = """log_printf(0, "\\n\\n***** ERROR: option flag -ip on command line but no argument provided!\\n");
				update_usage();
"""
IP_OLD_FULL = """			i++;
			ip = argv[i];
			if (cp(i + 101))
				goto iperr;
			if (i == argc || !ip || *ip == '-') {
			iperr:
				%s			}
""" % LOG
