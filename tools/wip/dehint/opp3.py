"""Attempt 3: parseOption's po_hint group (2 po_hint calls + no-early-inlining).
Variants of the bad-value copies draft that try to keep the bad string's .rdata
position (the original's: parseOption's last string).

python tools/wip/dehint/opp3.py [variant ...]   (no args: all)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

BAD = 'log_printf(1, "\\n\\n***** ERROR: parsing option \'%s\', value \'%s\' is incorrect!\\n", opt, val);'
NEI = '__attribute__((optimize("no-early-inlining")))\n'
HINT = 'po_hint(&dead);\n\t\t\t\tgoto bad;'


def base():
    t = optlib.read_src(optlib.SRC)
    assert NEI in t and t.count(HINT) == 2 and BAD in t
    return t


def copies(t, rep):
    t = t.replace(NEI, '')
    return t.replace(HINT, rep)


def v_copies():
    return copies(base(), BAD + '\n\t\t\t\treturn 0;')


def v_static():
    # the message as a file-scope array
    t = base()
    msg = BAD.split('(1, ', 1)[1].rsplit(', opt, val', 1)[0]
    t = t.replace('static void po_hint', 'static const char badValue[] = %s;\nstatic void po_hint' % msg)
    t = t.replace(BAD, 'log_printf(1, badValue, opt, val);')
    return copies(t, 'log_printf(1, badValue, opt, val);\n\t\t\t\treturn 0;')


def v_static_local():
    t = base()
    msg = BAD.split('(1, ', 1)[1].rsplit(', opt, val', 1)[0]
    t = t.replace('\tint dead;\n', '\tstatic const char badValue[] = %s;\n\tint dead;\n' % msg, 1)
    t = t.replace(BAD, 'log_printf(1, badValue, opt, val);')
    return copies(t, 'log_printf(1, badValue, opt, val);\n\t\t\t\treturn 0;')


def v_ptr():
    # a const char * to the literal, taken at bad's position? (literal still expanded first use)
    t = base()
    msg = BAD.split('(1, ', 1)[1].rsplit(', opt, val', 1)[0]
    t = t.replace('static void po_hint', 'static const char *const badValue = %s;\nstatic void po_hint' % msg)
    t = t.replace(BAD, 'log_printf(1, badValue, opt, val);')
    return copies(t, 'log_printf(1, badValue, opt, val);\n\t\t\t\treturn 0;')


def v_badfn():
    # a helper that prints the message (not inlined early? it is: tiny)
    t = base()
    t = t.replace('static void po_hint', 'static uint32_t badValue(const char *opt, const char *val)\n{\n\t%s\n\treturn 0;\n}\nstatic void po_hint' % BAD)
    t = t.replace(BAD + '\n\treturn 0;', 'return badValue(opt, val);')
    return copies(t, 'return badValue(opt, val);')


V = {k[2:]: v for k, v in dict(globals()).items() if k.startswith('v_')}

if __name__ == '__main__':
    names = sys.argv[1:] or list(V)
    for n in names:
        t = V[n]()
        if '-w' in os.environ.get('OPW', ''):
            open('build/op/%s.c' % n, 'w', newline='\n').write(t)
        print(n, optlib.fmt(optlib.score_text(t)))
