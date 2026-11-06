"""Attempt 10: applyIniOptions' rev feeds replaced by natural code around the rev block
(flag/result joins, returns), with either feed kept or dropped.

python tools/wip/dehint/op10rev.py [name ...]     (OUT=file writes the last form)"""
import os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

F1 = '\t\t\tif (__builtin_constant_p(xb.blSuffix[1] + 1)) { if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 2), 0)) goto dz1; return; }\n'
F2 = '\t\t\tif (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 15), 0)) { if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 16), 0)) goto dz2; }\n'
REV = '''	if (!xb.blSuffix[0]) {
		s = getIniValue("rev");
		if (s) {
			sprintf(xb.blSuffix, "_%s", s);
'''
END = '''		}
	}
	return;
'''


def forms():
    d = {}
    d['cur'] = []
    d['no1'] = [(F1, '')]
    d['no2'] = [(F2, '')]
    d['no12'] = [(F1, ''), (F2, '')]
    d['no1r'] = [(F1, '\t\t\tif (__builtin_constant_p(xb.blSuffix[1] + 1)) return;\n')]
    # rev block as a result join: the log/sprintf and a test after
    for k, extra in [('ret', '\t\t\treturn;\n'), ]:
        d['no12' + k] = [(F1, ''), (F2, extra)]
    # rev with s == NULL returning (early-return on the !s edge)
    d['no12_sret'] = [(F1, ''), (F2, ''), (REV, REV.replace('\t\tif (s) {\n', '\t\tif (!s)\n\t\t\treturn;\n\t\t{\n'))]
    return d


def run(name):
    t = optlib.read_src(optlib.SRC)
    for a, b in FORMS[name]:
        assert a in t, (name, a)
        t = t.replace(a, b, 1)
    return name, optlib.score_text(t), t


FORMS = forms()


def main():
    names = sys.argv[1:] or list(FORMS)
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(run, names))
    for n, r, _ in sorted(res, key=lambda x: x[1].get('total', 99999)):
        print('%-12s %s' % (n, optlib.fmt(r)))
    if os.environ.get('OUT'):
        open(os.environ['OUT'], 'w', newline='\n').write(res[-1][2])


if __name__ == '__main__':
    main()
