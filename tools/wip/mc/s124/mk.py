# mk.py BASE OUT KEYSCOND : add spare labels (ks1 ks2 kn1 kip klat) to BASE and replace the -keys test
import sys
s = open(sys.argv[1]).read()
def rep(a, b):
    global s
    assert a in s, a
    s = s.replace(a, b, 1)
rep('\t\t\t\tlog_printf(0, "reboot has already been set on command line, ignoring -s\\n");',
    '\t\t\t\t{ ks1: log_printf(0, "reboot has already been set on command line, ignoring -s\\n"); }')
rep('\t\t\t\tlog_printf(0, "setting shutdown on completion\\n");',
    '\t\t\t\tks2: log_printf(0, "setting shutdown on completion\\n");')
rep('\t\t\tlog_printf(0, "<enter> key on completion suppressed\\n");',
    '\t\t\tkn1: log_printf(0, "<enter> key on completion suppressed\\n");')
rep('\t\t\tlog_printf(0, "setting forced IP to %s\\n", ip);',
    '\t\t\tkip: log_printf(0, "setting forced IP to %s\\n", ip);')
if 'klat:' not in s:
    rep('client_usage(1, argv[i]); } } }\n\t}', 'client_usage(1, argv[i]); } } }\n\tklat: ;\n\t}')
if len(sys.argv) > 3:
    rep('} else if (!strnicmp(argv[i], "-keys", 5)) {', '} else if (' + sys.argv[3] + ') {')
open(sys.argv[2], 'w', newline='\n').write(s)
