"""Attempt 8: parseOption's two expects as result-variable / join shapes.

python tools/wip/dehint/op8po.py [-top N] [-show S,V] [-o out.c]
S = setBoolOption test form, V = vlen tail form (see SB / VT below).  The po_hint
calls and no-early-inlining stay (they are a separate group)."""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

SB_CUR = '''	if (__builtin_expect(setBoolOption(opt, val) == 1, 0)) {
		log_printf(1, "\\n");
		return 1;
	}
	if (val) {
'''
VT_CUR = '''	if (__builtin_expect(vlen, 0)) {
		log_printf(1, "\\n\\n***** ERROR: unknown option '%s' with value '%s' provided on the command line!\\n", opt, val);
		return 0;
	}
	log_printf(1, "\\n\\n***** ERROR: unknown or incomplete option '%s' provided on the command line!\\n", opt);
	return 0;
bad:
'''
L_VAL = '''log_printf(1, "\\n\\n***** ERROR: unknown option '%s' with value '%s' provided on the command line!\\n", opt, val);'''
L_INC = '''log_printf(1, "\\n\\n***** ERROR: unknown or incomplete option '%s' provided on the command line!\\n", opt);'''

SB = {
    'E': SB_CUR,
    'p1': SB_CUR.replace('__builtin_expect(setBoolOption(opt, val) == 1, 0)', 'setBoolOption(opt, val) == 1'),
    'p2': SB_CUR.replace('__builtin_expect(setBoolOption(opt, val) == 1, 0)', 'setBoolOption(opt, val)'),
    # handled: no return in the arm, the rest under else (closed in VT via ELSE)
    'r1': '''	if (setBoolOption(opt, val) == 1)
		log_printf(1, "\\n");
	else {
	if (val) {
''',
    'r2': '''	if (setBoolOption(opt, val))
		log_printf(1, "\\n");
	else {
	if (val) {
''',
    # result variable for the bool option
    'v1': '''	r = setBoolOption(opt, val);
	if (r == 1) {
		log_printf(1, "\\n");
		return r;
	}
	if (val) {
''',
    'v2': '''	r = setBoolOption(opt, val);
	if (r) {
		log_printf(1, "\\n");
		return r;
	}
	if (val) {
''',
}

VT = {
    'E': VT_CUR,
    'v1': VT_CUR.replace('__builtin_expect(vlen, 0)', 'vlen'),
    'ie': '\tif (vlen)\n\t\t' + L_VAL + '\n\telse\n\t\t' + L_INC + '\n\treturn 0;\nbad:\n',
    'ie0': '\tif (!vlen)\n\t\t' + L_INC + '\n\telse\n\t\t' + L_VAL + '\n\treturn 0;\nbad:\n',
    'ev': VT_CUR.replace('__builtin_expect(vlen, 0)', 'val'),
    'iev': '\tif (val)\n\t\t' + L_VAL + '\n\telse\n\t\t' + L_INC + '\n\treturn 0;\nbad:\n',
}


def make(base, s, v):
    t = base
    assert SB_CUR in t and VT_CUR in t
    t = t.replace(SB_CUR, SB[s])
    vt = VT[v]
    if s.startswith('r'):
        # close the else after the tail's returns: the tail ends in `return 0;` before bad:
        vt = vt.replace('\treturn 0;\nbad:\n', '\treturn 0;\n\t}\n\treturn 1;\nbad:\n')
    t = t.replace(VT_CUR, vt)
    if s.startswith('v'):
        t = t.replace('\tint i, len, vlen;\n', '\tint i, len, vlen;\n\tuint32_t r;\n', 1)
    return t


def main():
    a = sys.argv[1:]
    base = optlib.read_src(os.path.join(optlib.R, 'src', 'options.c'))
    if '-show' in a:
        s, v = a[a.index('-show') + 1].split(',')
        t = make(base, s, v)
        if '-o' in a:
            open(a[a.index('-o') + 1], 'w', newline='\n').write(t)
        optlib.vdiff(t, only='_parseOption')
        return
    keys = list(itertools.product(SB, VT))
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(lambda k: (k, optlib.score_text(make(base, *k))), keys))
    res.sort(key=lambda r: r[1].get('total', 99999) if not r[1].get('identical') else -1)
    for k, r in res:
        print('%-4s %-4s' % k, optlib.fmt(r))


if __name__ == '__main__':
    main()
