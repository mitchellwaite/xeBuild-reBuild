"""Knob-based mode_client tail generator, scored with mcvar (cold order) + fncmp (hot layout).
python gen2.py [filter-substring] [--head er] ; env FLAGS overrides gcc flags.
Knobs (name parts): pre{0,1} test{a,n,o} fail{g,r,e} tail{c,d} hint{0,1}
  pre1  : `if (!(mode && arg) && !reboot) client_usage(2, NULL);` before the if/else (usage check first)
  test a: if (mode && arg) {S} else {R}   n: if (!(mode && arg)) {R} else {S}   o: if (!mode || !arg) {R} else {S}
  fail g: `goto fail` (shared label at the end)  r: inline `{ log; return 0; }`  e: `else log` with a common return
  tail c: common `if (reboot) netReboot; netDisconnect; return 0`   d: duplicated in both arms
  hint1 : the draft's hints (rok/fail cold labels, E(reboot)) where they apply
"""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tailvar
from tailvar import head, UNABLE, sw, HEADS, mcvar
SP = os.path.dirname(os.path.abspath(__file__))


def ind(text, n):
    return '\n'.join(('\t' * n + l) if l else l for l in text.split('\n'))


def build(pre, test, fail, tail, hint):
    E = 'E(reboot)' if hint else 'reboot'
    rok = '\t\t\trok: __attribute__((cold));\n' if hint else ''
    faillab = 'fail: __attribute__((cold));' if hint else 'fail:'
    # S: switch path body (after a successful connect), R: reboot path body (after a successful connect)
    S_ok = 'cinfo = netGetInfo();\n' + sw('')
    R_ok = (rok.strip() + '\n' if rok else '') + 'cinfo = netGetInfo();'
    common = 'if (%s)\n\tnetReboot(reboot);\nnetDisconnect();\nreturn 0;' % E
    if tail == 'd':
        S_ok += '\n' + common
        R_ok += '\nnetReboot(reboot);\nnetDisconnect();\nreturn 0;'
    def connect(ok_body):
        if fail == 'g':
            return 'if (netConnect(ip)) {\n%s\n} else\n\tgoto fail;' % ind(ok_body, 1)
        if fail == 'r':
            return 'if (!netConnect(ip)) {\n\t%s\n\treturn 0;\n}\n%s' % (UNABLE, ok_body)
        return 'if (netConnect(ip)) {\n%s\n} else\n\t%s' % (ind(ok_body, 1), UNABLE)
    S = connect(S_ok)
    R = connect(R_ok)
    out = ''
    if pre:
        out += 'if (!(mode && arg) && !reboot)\n\tclient_usage(2, NULL);\n'
        Rfull = R
    else:
        Rfull = 'if (reboot) {\n%s\n} else\n\tclient_usage(2, NULL);' % ind(R, 1)
    if test == 'a':
        out += 'if (mode && arg) {\n%s\n} else {\n%s\n}\n' % (ind(S, 1), ind(Rfull, 1))
    elif test == 'n':
        out += 'if (!(mode && arg)) {\n%s\n} else {\n%s\n}\n' % (ind(Rfull, 1), ind(S, 1))
    else:
        out += 'if (!mode || !arg) {\n%s\n} else {\n%s\n}\n' % (ind(Rfull, 1), ind(S, 1))
    if tail == 'c':
        out += common + '\n'
    if fail == 'g':
        out += faillab + '\n' + UNABLE + '\nreturn 0;\n'
    body = ind(out.rstrip('\n'), 1) + '\n}\n'
    # the `else if (reboot)` form reads better and is what an author would write; keep the nested form
    return body


def variants():
    for pre, test, fail, tail, hint in itertools.product((0, 1), 'ano', 'gre', 'cd', (0, 1)):
        if pre and test != 'a':
            pass
        name = 'pre%d_test%s_fail%s_tail%s_hint%d' % (pre, test, fail, tail, hint)
        yield name, build(pre, test, fail, tail, hint)


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    hk = ''
    if '--head' in sys.argv:
        hk = '_' + sys.argv[sys.argv.index('--head') + 1]
    flt = args[0] if args else ''
    flags = os.environ.get('FLAGS', '-O3 --param builtin-expect-probability=50').split()
    rows = []
    for name, body in variants():
        if flt and flt not in name:
            continue
        p = os.path.join(SP, 'var', 'g2', name + hk + '.c')
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'w', newline='\n').write(HEADS[hk] + body)
        res, err = mcvar.run(p, flags, fncmp=True)
        if res is None:
            print(name, 'ERROR', err[-300:]); continue
        o = ' '.join(s.replace('strnicmp:', '').replace('log:', '')[:8] for s in res['order'])
        rows.append((res['fncmp'], res['inv'], -res['pre'], name, o))
        print('%-28s fncmp=%3d inv=%2d pre=%2d  %s' % (name, res['fncmp'], res['inv'], res['pre'], o), flush=True)
    print('== best by fncmp')
    for r in sorted(rows)[:12]:
        print('%-28s fncmp=%3d inv=%2d pre=%2d' % (r[3], r[0], r[1], -r[2]))
