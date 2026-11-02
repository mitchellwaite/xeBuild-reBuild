# gen.py NAME EDIT... : v/NAME.c from c0.c (clean base); all edits are dead cp gotos / labels / asm goto (equivalent)
import sys
s = open('c0.c').read()
def rep(a, b):
    global s
    assert a in s, a
    s = s.replace(a, b, 1)
PL = 'P' in sys.argv[2:]
if PL: sys.argv.remove('P'); s = s.replace('#define AT(l)\n', '#define AT(l) l:\n', 1)
if not PL: rep('#define AT(l)\n#define JUMP(...)\n', '#define AT(l) l:\n#define JUMP(...) __asm__ goto ("" :::: __VA_ARGS__)\n')
rep('\t\t\tcinfo = netGetInfo();\n\t\t\tswitch (mode) {', '\t\t\tdsp: cinfo = netGetInfo();\n\t\t\tswitch (mode) {')
J1 = 'JUMP(c12, c11, p0, i0, c9, hdd4, hdd5, c2, c1, c10, u2, cdef, c8, c7, c3, s5);'
J2 = 'JUMP(i1, p1, hdd5, hdd4, c10, c9, c1, c7, cdef);'
def chain(base, n):
    return ' && '.join('(char *)__builtin_constant_p(mode + %d) == (char *)1' % (base + j) for j in range(n)) if n else '__builtin_constant_p(mode + %d)' % base
EB = s[s.index('/* -eb <b> */\nvoid clientEraseBlock'):s.index('/* the option\'s argument(s)')]
EI = EB.replace('void clientEraseBlock', 'static void clientEraseBlockI')
EI0 = EI
def erep(a, b):
    global EI
    assert a in EI, a
    EI = EI.replace(a, b, 1)
for e in sys.argv[2:]:
    k, _, a = e.partition('=')
    if k == 'Ef': erep('AT(efail) log', 'efail: __attribute__((%s)); log' % a); continue
    if k == 'Eo': erep('{ log_printf(0, "\\n\\n***** ERROR: Block', '{ eout: __attribute__((%s)); log_printf(0, "\\n\\n***** ERROR: Block' % a); continue
    if k == 'Ei': erep('} else\n\t\tlog_printf(0, "\\n\\n***** ERROR: Invalid', '} else\n\t\t{ einv: __attribute__((%s)); } log_printf(0, "\\n\\n***** ERROR: Invalid' % a); continue
    if k == 'Ec': erep('{', '{'); EI0 = None; continue
    if k == 'Ej': erep('JUMP(efail);', ''); continue   # drop eout->efail asm goto
    if k == 'Ek': erep('JUMP(efail);', 'if (__builtin_constant_p(block + %s)) goto efail;' % a); continue
    if k == 'Es': erep('log_printf(0, "Success!\\n");', '{ log_printf(0, "Success!\\n"); if (__builtin_constant_p(block + 9)) goto %s; }' % a); continue
    if k == 'Uh': rep('{ AT(u2) client_usage(2, NULL); }', '{ u2: __attribute__((%s)); client_usage(2, NULL); }' % a); continue
    if k == 'J1':   # replace rok jump list ('' -> remove)
        rep(J1, 'JUMP(%s);' % a if a else ''); J1 = None
    elif k == 'J2':
        rep(J2, 'JUMP(%s);' % a if a else '')
    elif k == 'F':  # feed switch: dead cp chain before NO_MODE_ARG test -> dsp ; a=n
        rep('\tif (NO_MODE_ARG(mode, arg)) {', '\tif (%s) goto dsp;\n\tif (NO_MODE_ARG(mode, arg)) {' % chain(700, int(a)))
    elif k == 'Fr':  # feed from reboot path after netGetInfo
        rep('\t\t\t} else\n\t\t\t\tgoto fail;', '\t\t\t\tif (%s) goto dsp;\n\t\t\t} else\n\t\t\t\tgoto fail;' % chain(720, int(a)))
    elif k == 'Fu':  # feed from usage arm
        rep('{ AT(u2) client_usage(2, NULL); }', '{ if (%s) goto dsp; AT(u2) client_usage(2, NULL); }' % chain(740, int(a)))
    elif k == 'G':  # dead cp goto label,n before NO_MODE_ARG
        lab, n = a.split(','); rep('\tif (NO_MODE_ARG(mode, arg)) {', '\tif (%s) goto %s;\n\tif (NO_MODE_ARG(mode, arg)) {' % (chain(760, int(n)), lab))
    elif k == 'Hd':
        rep('dsp: cinfo', 'dsp: __attribute__((hot)); cinfo')
    elif k == 'Cr':  # remove cold on rok
        rep('rok: __attribute__((cold));', 'rok: ;')
    elif k == 'R':
        o, n = a.split('|'); rep(o.replace('\n','\n').replace('\t','\t'), n.replace('\n','\n').replace('\t','\t'))
    else:
        raise SystemExit('bad ' + k)
if EI != EI0:
    s = s.replace("/* the option's argument(s)", EI + "/* the option's argument(s)", 1)
    rep('clientEraseBlock(arg);', 'clientEraseBlockI(arg);')
open('v/%s.c' % sys.argv[1], 'w', newline='\n').write(s)
