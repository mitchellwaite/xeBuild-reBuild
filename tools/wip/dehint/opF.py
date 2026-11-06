"""Attempt 3 experiment (hints, not for landing): on the natural parseButton (opbtn noexp), raise
the xellbutton call block's frequency F with a dead feed from the block after patchsmc, to test
whether F ~ 171 (!s ~ 37 and remopower >= 18 together) is what the layout needs.

python tools/wip/dehint/opF.py [-o DIR]"""
import os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib, opbtn

PS = '\t\tOPT("patchsmc", 0x8000000, 0);\n'
CALL = '\t\t\txb.xellButton = parseButton(getIniValue("xellbutton"));\n'


def cp(n):
    return '__builtin_constant_p(xb.flags + %d)' % n


FEEDS = {
    'e0': 'if (__builtin_expect(%s, 0)) goto xcall;' % cp(71),
    'c_e0': 'if (%s) { if (__builtin_expect(%s, 0)) goto xcall; }' % (cp(71), cp(72)),
    'cc_e0': 'if (%s) { if (%s) { if (__builtin_expect(%s, 0)) goto xcall; } }' % (cp(71), cp(72), cp(73)),
    'ccc_e0': 'if (%s) { if (%s) { if (%s) { if (__builtin_expect(%s, 0)) goto xcall; } } }' % (cp(71), cp(72), cp(73), cp(74)),
    'c': 'if (%s) goto xcall;' % cp(71),
    'cc': 'if (%s) { if (%s) goto xcall; }' % (cp(71), cp(72)),
    'ccc': 'if (%s) { if (%s) { if (%s) goto xcall; } }' % (cp(71), cp(72), cp(73)),
    'e0e0': 'if (__builtin_expect(%s, 0)) { if (__builtin_expect(%s, 0)) goto xcall; }' % (cp(71), cp(72)),
}


def build(n):
    t = opbtn.build(opbtn.V['noexp'])
    assert PS in t and CALL in t
    t = t.replace(PS, PS + '\t\t' + FEEDS[n] + '\n')
    return t.replace(CALL, 'xcall:\n' + CALL)


def run(n):
    return n, optlib.fmt(optlib.score_text(build(n)))


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[:1] == ['-o']:
        os.makedirs(a[1], exist_ok=True)
        for n in FEEDS:
            open(os.path.join(a[1], n + '.c'), 'w', newline='\n').write(build(n))
    with ThreadPoolExecutor(6) as ex:
        for n, r in ex.map(run, list(FEEDS)):
            print(n, r[:200])
