"""Attempt 4: parseOption's po_hint group.  Variants of cputemp's/gpufan's bad arms with
po_hint and no-early-inlining gone; writes build/op/po4_<name>.c and scores each.

python tools/wip/dehint/oppo4.py [names..]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

MSG = '"\\n\\n***** ERROR: parsing option \'%s\', value \'%s\' is incorrect!\\n"'
HINT = '\t\t\t\tpo_hint(&dead);\n\t\t\t\tgoto bad;\n'
COPY = '\t\t\t\tlog_printf(1, ' + MSG + ', opt, val);\n\t\t\t\treturn 0;\n'


def base():
    t = optlib.read_src(optlib.SRC)
    t = t.replace('__attribute__((optimize("no-early-inlining")))\nuint32_t parseOption', 'uint32_t parseOption')
    return t


def v_copies(t):
    return t.replace(HINT, COPY)


V = {'copies': v_copies}


def main():
    names = sys.argv[1:] or list(V)
    for n in names:
        t = V[n](base())
        p = os.path.join(optlib.BUILD, 'po4_%s.c' % n)
        open(p, 'w', newline='\n').write(t)
        print('%-10s %s' % (n, optlib.fmt(optlib.score_text(t))), flush=True)


if __name__ == '__main__':
    main()
