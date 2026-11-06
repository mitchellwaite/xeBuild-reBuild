"""Attempt 3: parseOption's two __builtin_expect, forms attempt 1's opend.py didn't try:
comparison operators (opcode heuristics), vlen's type and computation, the setBoolOption
test's spelling, error variable.  Scored alone and with each other.

python tools/wip/dehint/opvl.py [names..]"""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

E2 = 'if (__builtin_expect(vlen, 0)) {'
E1 = 'if (__builtin_expect(setBoolOption(opt, val) == 1, 0)) {'
VL = '''	if (len == strlen(opt))
		vlen = 0;
	else
		vlen = strlen(val);
'''
DECL = '\tint i, len, vlen;\n'

T2 = {  # replacement for E2 (and possibly other edits)
    'gt0': [(E2, 'if (vlen > 0) {')],
    'ge1': [(E2, 'if (vlen >= 1) {')],
    'ne0': [(E2, 'if (vlen != 0) {')],
    'lt0': [(E2, 'if (0 < vlen) {')],
    'sz': [(E2, 'if (vlen) {'), (DECL, '\tint i, len;\n\tsize_t vlen;\n')],
    'sz_gt0': [(E2, 'if (vlen > 0) {'), (DECL, '\tint i, len;\n\tsize_t vlen;\n')],
    'u32': [(E2, 'if (vlen) {'), (DECL, '\tint i, len;\n\tuint32_t vlen;\n')],
    'vl_ter': [(E2, 'if (vlen) {'), (VL, '\tvlen = len == strlen(opt) ? 0 : strlen(val);\n')],
    'vl_ne': [(E2, 'if (vlen) {'), (VL, '''	if (len != strlen(opt))
		vlen = strlen(val);
	else
		vlen = 0;
''')],
    'vl_init': [(E2, 'if (vlen) {'), (VL, '''	vlen = 0;
	if (len != strlen(opt))
		vlen = strlen(val);
'''), (DECL, '\tint i, len, vlen;\n')],
    'vl_val': [(E2, 'if (vlen) {'), (VL, '''	vlen = 0;
	if (val)
		vlen = strlen(val);
''')],
    'vl_val_gt': [(E2, 'if (vlen > 0) {'), (VL, '''	vlen = 0;
	if (val)
		vlen = strlen(val);
''')],
    'vl_gt_ne': [(E2, 'if (vlen > 0) {'), (VL, '''	if (len != strlen(opt))
		vlen = strlen(val);
	else
		vlen = 0;
''')],
    'vl_slen': [(E2, 'if (vlen > 0) {'), (VL, '''	if (len == strlen(opt))
		vlen = 0;
	else
		vlen = strlen(val);
''')],
    'lenne': [(E2, 'if (len != strlen(opt)) {')],
}
T1 = {
    'eq1': [(E1, 'if (setBoolOption(opt, val) == 1) {')],
    'nz': [(E1, 'if (setBoolOption(opt, val)) {')],
    'gt0': [(E1, 'if (setBoolOption(opt, val) > 0) {')],
    'ge1': [(E1, 'if (setBoolOption(opt, val) >= 1) {')],
    'ne0': [(E1, 'if (setBoolOption(opt, val) != 0) {')],
}


def apply(t, eds):
    for a, b in eds:
        if a not in t:
            return None
        t = t.replace(a, b, 1)
    return t


def variants():
    for n, e in T2.items():
        yield 'e2:' + n, e
    for n, e in T1.items():
        yield 'e1:' + n, e
    for (a, ea), (b, eb) in itertools.product(T1.items(), T2.items()):
        yield 'both:%s+%s' % (a, b), ea + eb


def run(item):
    n, e = item
    t = apply(optlib.read_src(optlib.SRC), e)
    if t is None:
        return n, 'n/a'
    return n, optlib.fmt(optlib.score_text(t))


if __name__ == '__main__':
    want = sys.argv[1:]
    items = [v for v in variants() if not want or v[0] in want]
    with ThreadPoolExecutor(6) as ex:
        for n, r in ex.map(run, items):
            print(n, r[:150])
