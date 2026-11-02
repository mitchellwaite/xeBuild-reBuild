# mk2.py BASE OUT ARMBODY [COND]: replace the -keys arm body (and optionally its condition)
import sys
s = open(sys.argv[1]).read()
a = '} else if (!strnicmp(argv[i], "-keys", 5)) {\n\t\t\tmode = 3;\n\t\t\targ = dummy;\n'
assert a in s
c = sys.argv[4] if len(sys.argv) > 4 else '!strnicmp(argv[i], "-keys", 5)'
s = s.replace(a, '} else if (' + c + ') {\n\t\t\t' + sys.argv[3] + '\n', 1)
open(sys.argv[2], 'w', newline='\n').write(s)
