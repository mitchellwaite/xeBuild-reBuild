"""Attempt 9: parseOption without po_hint / no-early-inlining.  cputemp's and gpufan's bad
edges need a guarded call at profile_estimate (PRED_CALL); a copy of the bad message is
one, but a copy inside the arm numbers the bad string first (.rdata).  Here the copies sit
at the end of the function, after `bad:` or before it, one label per arm or shared.

python tools/wip/dehint/op9end.py [form...]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

HINT = '''			if (xb.%s == -1) {
				po_hint(&dead);
				goto bad;
			}
'''
BADMSG = '\tlog_printf(1, "\\n\\n***** ERROR: parsing option \'%s\', value \'%s\' is incorrect!\\n", opt, val);\n\treturn 0;\n'
BAD = 'bad:\n' + BADMSG
ARMS = [('cpuTemp', 'badcpu'), ('gpuFan', 'badgpu')]


def base(t):
    t = t.replace('static void po_hint(int *p) { *p = 1; }\n\n', '')
    t = t.replace('__attribute__((optimize("no-early-inlining")))\nuint32_t parseOption',
                  'uint32_t parseOption')
    t = t.replace('\tint dead;\n\tchar *val = NULL;', '\tchar *val = NULL;')
    assert BAD in t
    return t


def form(t, f):
    t = base(t)
    for fld, lab in ARMS:
        h = HINT % fld
        assert h in t, fld
        if f == 'plain':
            t = t.replace(h, '\t\t\tif (xb.%s == -1)\n\t\t\t\tgoto bad;\n' % fld)
        elif f == 'inarm':
            t = t.replace(h, '\t\t\tif (xb.%s == -1) {\n\t\t\t\tlog_printf(1, "\\n\\n***** ERROR: parsing option \'%%s\', value \'%%s\' is incorrect!\\n", opt, val);\n\t\t\t\treturn 0;\n\t\t\t}\n' % fld)
        elif f in ('after', 'before', 'after_r', 'before_r'):
            t = t.replace(h, '\t\t\tif (xb.%s == -1)\n\t\t\t\tgoto %s;\n' % (fld, lab))
        elif f in ('shared_after', 'shared_before'):
            t = t.replace(h, '\t\t\tif (xb.%s == -1)\n\t\t\t\tgoto badtemp;\n' % fld)
    labs = [lab for _, lab in ARMS]
    if f.endswith('_r'):
        labs = labs[::-1]
    copies = ''.join('%s:\n%s' % (l, BADMSG) for l in labs)
    if f.startswith('after'):
        t = t.replace(BAD, BAD + copies)
    elif f.startswith('before'):
        t = t.replace(BAD, copies + BAD)
    elif f == 'shared_after':
        t = t.replace(BAD, BAD + 'badtemp:\n' + BADMSG)
    elif f == 'shared_before':
        t = t.replace(BAD, 'badtemp:\n' + BADMSG + BAD)
    return t


FORMS = ['plain', 'inarm', 'after', 'after_r', 'before', 'before_r', 'shared_after', 'shared_before']


def main():
    t = optlib.read_src(optlib.SRC)
    for f in sys.argv[1:] or FORMS:
        v = form(t, f)
        if os.environ.get('OUT'):
            open(os.environ['OUT'], 'w', newline='\n').write(v)
        print(f, optlib.fmt(optlib.score_text(v)))


if __name__ == '__main__':
    main()
