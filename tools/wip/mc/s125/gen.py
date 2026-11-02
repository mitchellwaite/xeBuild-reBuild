# gen.py NAME EDIT... : build v/NAME.c from b18.c applying named edits
import sys
s = open('b18.c').read()
def rep(a, b):
    global s
    assert a in s, a
    s = s.replace(a, b, 1)
KEYS = '} else if (!strnicmp(argv[i], "-keys", 5)) {'
IP = '} else if (!strnicmp(argv[i], "-ip", 3)) {'
END = 'client_usage(1, argv[i]); } } }\n\t}'
SCP = 'if (__builtin_constant_p(i + 300)) goto cdef;'
nb = 0
def nb_add():
    global nb
    nb += 1
for e in sys.argv[2:]:
    k, _, a = e.partition('=')
    if k == 'Lk':   # label kky on -keys test
        rep(KEYS, '} else { kky: if (!strnicmp(argv[i], "-keys", 5)) {'); nb += 1
    elif k == 'Li':  # label kipt on -ip test
        rep(IP, '} else { kipt: if (!strnicmp(argv[i], "-ip", 3)) {'); nb += 1
    elif k == 'Gs':  # dead cp goto from -s arm to label a
        rep(SCP, SCP + ' if (__builtin_constant_p(i + 310)) goto %s;' % a)
    elif k == 'Gk':  # dead cp goto from -keys arm
        rep('\t\t\tmode = 3;\n', '\t\t\tif (__builtin_constant_p(i + 320)) goto %s; mode = 3;\n' % a)
    elif k == 'Hs':
        rep('} else if (!strnicmp(argv[i], "-s", 2)) {', '} else if (!strnicmp(argv[i], "-s", 2)) { khl: __attribute__((hot));')
    elif k == 'Hk':
        rep('\t\t\tmode = 3;\n', '\t\t\tkhk: __attribute__((hot)); mode = 3;\n')
    elif k in ('T','E','B','S','K','W','M'):  # dead cp chain goto: T loop top, E -eb arm, B before -s test; a=label,nconj
        p = a.split(','); lab = p[0]; n = int(p[1]); base = {'T': 900, 'E': 910, 'B': 920, 'S': 930, 'K': 940, 'W': 950, 'M': 960}[k] + (int(p[2]) if len(p) > 2 else 0)
        c = ' && '.join('(char *)__builtin_constant_p(i + %d) == (char *)1' % (base + j) for j in range(n)) if n else '__builtin_constant_p(i + %d)' % base
        g = 'if (%s) goto %s; ' % (c, lab)
        if k == 'T': rep('if (__builtin_constant_p(i + 320) && __builtin_constant_p(i + 321)) goto u2;', g + 'if (__builtin_constant_p(i + 320) && __builtin_constant_p(i + 321)) goto u2;')
        elif k == 'E': rep('arg = argv[++i];\n\t\t\tlog_printf(0, "erase block', g + 'arg = argv[++i];\n\t\t\tlog_printf(0, "erase block')
        elif k == 'S': rep(SCP, SCP + ' ' + g)
        elif k == 'W': rep('log_printf(0, "setting shutdown on completion', g + 'log_printf(0, "setting shutdown on completion')
        elif k == 'M': rep('log_printf(0, "reboot has already been set on command line, ignoring -s', g + 'log_printf(0, "reboot has already been set on command line, ignoring -s')
        elif k == 'K': rep('mode = 3;\n\t\t\targ = dummy;', g + 'mode = 3;\n\t\t\targ = dummy;')
        else: rep('} else if (!strnicmp(argv[i], "-s", 2)) {', '} else { ' + g + 'if (!strnicmp(argv[i], "-s", 2)) {'); nb_add()
    elif k == 'Ls2':
        rep('log_printf(0, "setting shutdown on completion', 'ks2: log_printf(0, "setting shutdown on completion')
    elif k == 'Ls1':
        rep('log_printf(0, "reboot has already been set on command line, ignoring -s', 'ks1: log_printf(0, "reboot has already been set on command line, ignoring -s')
    elif k == 'R':  # raw old|new
        o, n = a.split('|'); rep(o.replace('\n','\n').replace('\t','\t'), n.replace('\n','\n').replace('\t','\t'))
    else:
        raise SystemExit('bad ' + k)
if nb:
    rep(END, 'client_usage(1, argv[i]); } } }' + '}' * nb + '\n\t}')
open('v/%s.c' % sys.argv[1], 'w', newline='\n').write(s)
