"""Attempt 9: every myatou32 value arm in one result-variable form (BASE, default F4) except
edramtemp, which gets each of op9rv's forms (or 'plain').

python tools/wip/dehint/op9mix.py [BASE]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib, op9rv


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else 'F4'
    t = optlib.read_src(optlib.SRC)
    rest = op9rv.SETS['-edramTemp']
    v0 = op9rv.form(t, base, rest)
    ed = op9rv.SETS['+edramTemp']
    for f in ['plain'] + list(op9rv.FORMS):
        if f == 'plain':
            v = v0
        else:
            v = v0
            d = {'f': 'edramTemp', 'n': 'EDRAMTEMP', 'p': '%d'}
            a = op9rv.ARM % d
            assert a in v
            d['l'] = op9rv.LOG % d
            v = v.replace(a, op9rv.FORMS[f] % d)
            if 'ok' in op9rv.FORMS[f] and ', ok;' not in v:
                v = v.replace('\tint i, len, vlen;\n', '\tint i, len, vlen, ok;\n', 1)
        print(base, 'edram', f, optlib.fmt(optlib.score_text(v)))


if __name__ == '__main__':
    main()
