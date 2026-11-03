"""lev.py: condition-spelling levers over updateNand (no dummy block).
Each test in TESTS has forms: 0 plain `if (C)`; 1 `fN = C; if (fN > 0)` (then-edge up: PRED_TREE_OPCODE_POSITIVE); 2 `fN = !C; if (fN <= 0)` (then-edge down).
All fold to the plain test after IPA, so code stays.  gen(state, ip) builds a source; state = dict name -> form.
python lev.py sweep  -> exhaustive sweep over LIVE tests, sorted by ev."""
import itertools
import sys

import axes as a
import sw

# source fragments, from axes.BASE0 with plain reboot and plain writeImage error and form b -ip
PLAIN = a.build(a.HEAD, a.REB['plain'], a.ERRS['plain'], a.IPS['b'])

TESTS = {
    # name: (exact `if` text in PLAIN, C expression)
    'gcf': ('if (getConsoleFiles(dumpDir)) {', 'getConsoleFiles(dumpDir)'),
    'bi': ('if (!ret) {\n\t\t\tnetUnmount', '!ret'),
    'dd1': ('if (!netDumpNand(nand)) {', '!netDumpNand(nand)'),
    'nw': ('if (!noWrite) {', '!noWrite'),
    'sf': ('if (!netSendFlash(buf, size))', '!netSendFlash(buf, size)'),
    'hdd': ('if (hasHdd) {', 'hasHdd'),
    'nr': ('if (!noReboot) {', '!noReboot'),
    'ret': ('if (!ret)\n\t\t\t\t\tnetReboot', '!ret'),
    'wi': ('if (r)\n', 'r'),
}
for k, (s, c) in TESTS.items():
    assert s in PLAIN, k


def form(name, s, c, f):
    v = 'f_' + name
    tail = s[len('if (' + c + ')'):]
    if f == 1:
        return '%s = !!(%s); if (%s > 0)%s' % (v, c, v, tail)
    if f == 2:
        return '%s = !(%s); if (%s <= 0)%s' % (v, c, v, tail)
    raise ValueError


def gen(state, ip='b'):
    t = PLAIN.replace(a.IPS['b'], a.IPS[ip])
    decl = []
    for k, f in state.items():
        if not f:
            continue
        s, c = TESTS[k]
        t = t.replace(s, form(k, s, c, f))
        decl.append('f_' + k)
    if decl:
        t = t.replace('\tint ret, r;\n', '\tint ret, r;\n\tint %s;\n' % ', '.join(decl))
    return t


def name(state, ip='b'):
    return ','.join('%s%d' % (k, f) for k, f in sorted(state.items()) if f) + '_' + ip


if __name__ == '__main__':
    live = sys.argv[1].split(',')
    vs = []
    for fs in itertools.product((0, 1, 2), repeat=len(live)):
        st = dict(zip(live, fs))
        vs.append((name(st), gen(st)))
    print(len(vs))
    sw.run(vs, '-O3', save='lev', top=30)
