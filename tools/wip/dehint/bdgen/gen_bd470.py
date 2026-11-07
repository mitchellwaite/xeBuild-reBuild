"""Attempt 35, pin_size from IRA (nopins.ira): the kit add `r105 = r197 (prephitmp) + r104 (size)` makes two shuffle
copies of equal freq, cp30 r197-r105 and cp31 r104-r105; copy_freq_compare_func breaks the tie by copy number, i.e.
operand order, so r105 threads with the prephitmp (r197 conflicts with r104, so cp31 can't merge after it) and pops
after r99's thread took esi.  The reference has r104 = r105 = ebx: the thread {r104, r105}.  So the operand order
(attempt 7) is the whole question, and it is set by PRE's names: the kit 14 lookup is the first block PRE's insert walk
reaches and takes the free list's top (prephitmp_229 < size_254).  The walk is a preorder of the dominator tree, sons
in block-index order, so this sweep changes the build-type chain's order and nesting (which arm's blocks come first)
and reports the kit sum's operand order with bdorder.py.  pin off."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun

FN = 'uint32_t calcBlAreaSize(void)\n'


def arms(t):
    i, j = bdrun.fnspan(t, FN)
    f = t[i:j]
    a = f.index('\tif (xb.type == BUILD_JTAG) {\n')
    b = f.index('\t} else if (xb.type > BUILD_DEVGL16) {\n')
    c = f.index('\t} else {\n')
    d = f.index('\t}\n\tif (size & 0x3fff)')
    J = f[a + len('\tif (xb.type == BUILD_JTAG) {\n'):b]
    K = f[b + len('\t} else if (xb.type > BUILD_DEVGL16) {\n'):c]
    R = f[c + len('\t} else {\n'):d]
    return i, j, f[:a], J, K, R, f[d + 3:]


COND = {
    'J': 'xb.type == BUILD_JTAG',
    'K': 'xb.type > BUILD_DEVGL16',
    'R': 'xb.type <= BUILD_DEVGL16',
    'nJ': 'xb.type != BUILD_JTAG',
}


def chain(order, conds, body):
    s = ''
    for n, (k, c) in enumerate(zip(order, conds)):
        if n == 0:
            s += '\tif (%s) {\n' % c
        elif c is None:
            s += '\t} else {\n'
        else:
            s += '\t} else if (%s) {\n' % c
        s += body[k]
    return s + '\t}\n'


def nested(outer, oc, inner, ic, body):
    # if (oc) outer else { if (ic) inner[0] else inner[1] }
    ind = lambda s: ''.join(('\t' + l if l.strip() else l) for l in s.splitlines(True))
    return ('\tif (%s) {\n' % oc + body[outer] + '\t} else {\n\t\tif (%s) {\n' % ic + ind(body[inner[0]]) +
            '\t\t} else {\n' + ind(body[inner[1]]) + '\t\t}\n\t}\n')


def nested2(oc, inner, ic, last, body):
    # if (oc) { if (ic) inner[0] else inner[1] } else last
    ind = lambda s: ''.join(('\t' + l if l.strip() else l) for l in s.splitlines(True))
    return ('\tif (%s) {\n\t\tif (%s) {\n' % (oc, ic) + ind(body[inner[0]]) + '\t\t} else {\n' + ind(body[inner[1]]) +
            '\t\t}\n\t} else {\n' + body[last] + '\t}\n')


def switch(body):
    ind = lambda s: ''.join(('\t' + l if l.strip() else l) for l in s.splitlines(True))
    return ('\tswitch (xb.type) {\n\tcase BUILD_JTAG:\n' + ind(body['J']) + '\t\tbreak;\n\tcase 0:\n\tcase BUILD_RETAIL:\n\tcase 3:\n'
            '\tcase BUILD_DEVGL:\n\tcase BUILD_DEVGL16:\n' + ind(body['R']) + '\t\tbreak;\n\tdefault:\n' + ind(body['K']) + '\t\tbreak;\n\t}\n')


def CASES(base):
    base = bdhints.off(base, 'pin_size')
    i, j, head, J, K, R, tail = arms(base)
    body = {'J': J, 'K': K, 'R': R}
    forms = {
        'src': chain('JKR', ['J', 'K', None], body),
        'JRK': chain('JRK', ['J', 'R', None], body),
        'KJR': chain('KJR', ['K', 'J', None], body),
        'KRJ': chain('KRJ', ['K', 'nJ', None], body),
        'nested_J_KR': nested('J', COND['J'], 'KR', COND['K'], body),
        'nested_J_RK': nested('J', COND['J'], 'RK', COND['R'], body),
        'nested_K_JR': nested('K', COND['K'], 'JR', COND['J'], body),
        'nested_K_RJ': nested('K', COND['K'], 'RJ', COND['nJ'], body),
        'nJ_KR_J': nested2(COND['nJ'], 'KR', COND['K'], 'J', body),
        'nJ_RK_J': nested2(COND['nJ'], 'RK', COND['R'], 'J', body),
        'sw': switch(body),
        # retail first, as filelist_ini spells its test
        'RJK': chain('RJK', ['xb.type != BUILD_JTAG && xb.type <= BUILD_DEVGL16', 'J', None], body),
        'RKJ': chain('RKJ', ['xb.type != BUILD_JTAG && xb.type <= BUILD_DEVGL16', 'K', None], body),
        'RJK2': chain('RJK', ['xb.type <= BUILD_DEVGL16 && xb.type != BUILD_JTAG', 'J', None], body),
        'RKJ2': chain('RKJ', ['xb.type <= BUILD_DEVGL16 && xb.type != BUILD_JTAG', 'K', None], body),
        'JRK_lt6': chain('JRK', ['J', 'xb.type < BUILD_DEVKIT', None], body),
        'JKR_ge6': chain('JKR', ['J', 'xb.type >= BUILD_DEVKIT', None], body),
    }
    labs = {'J': ['BUILD_JTAG'], 'R': ['BUILD_RETAIL', 'BUILD_GLITCH', 'BUILD_DEVGL', 'BUILD_DEVGL16'],
            'K': ['BUILD_DEVKIT', 'BUILD_DEVKIT16', 'BUILD_TESTKIT', 'BUILD_TESTKIT16']}
    ind = lambda s: ''.join(('\t' + l if l.strip() else l) for l in s.splitlines(True))
    for perm in itertools.permutations('JRK'):
        for dflt in ('R', 'K'):
            s = '\tswitch (xb.type) {\n'
            for a in perm:
                s += ''.join('\tcase %s:\n' % l for l in labs[a]) if a != dflt else '\tdefault:\n'
                s += ind(body[a]) + '\t\tbreak;\n'
            forms['sw_%s_d%s' % (''.join(perm), dflt)] = s + '\t}\n'
            # the default label inside the group's case list (before or after its cases), and R with case 0
            for pos in ('pre', 'post', 'zero'):
                s = '\tswitch (xb.type) {\n'
                for a in perm:
                    cl = ['\tcase %s:\n' % l for l in labs[a]]
                    if a == 'R' and pos == 'zero':
                        cl = ['\tcase 0:\n'] + cl
                    if a == dflt:
                        if pos == 'pre':
                            cl = ['\tdefault:\n'] + cl
                        elif pos == 'post':
                            cl = cl + ['\tdefault:\n']
                        else:
                            cl = ['\tdefault:\n']
                    s += ''.join(cl) + ind(body[a]) + '\t\tbreak;\n'
                forms['sw_%s_d%s_%s' % (''.join(perm), dflt, pos)] = s + '\t}\n'
    out = []
    for k, v in forms.items():
        if k != 'src':
            v = v.replace('\tif (xb.type == BUILD_JTAG) {', '\tif (%s) {' % COND['J'])
        # translate symbolic conds
        for s, c in COND.items():
            v = v.replace('if (%s) {' % s, 'if (%s) {' % c)
        out.append((k, base[:i] + head + v + tail + base[j:]))
    return out
