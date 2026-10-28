"""Write src/options.prof: applyIniOptions' crafted profile.

python wip/aiodesign.py build/obj/options.fdo/-.042t.profile_estimate > src/options.prof

The dump comes from the instrumented compile build.sh does for options
(-fdump-tree-profile_estimate-blocks-details).  The original's cold blocks
were laid out by ties in gcc's fibonacci heap (identical options have
identical guessed frequencies); here every trace start gets its own
frequency instead, in the original's order, within the band of the STC
round it belongs to (wip/README.md, options.c).  Blocks are found by
content; TARGET gives block frequencies (BB_FREQ_MAX scale, entry 1815), and
the edge into each target block gets the probability that yields it, solved
to a fixpoint on gcc's guessed profile (re/gcda.py's numbers).
"""
import os, re, sys
sys.stdout.reconfigure(newline='\n')   # LF on Windows too
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 're'))
import gcda

FN = 'applyIniOptions'
DUMP = sys.argv[1]
EST = gcda.read_dump(DUMP)[0][FN]
SUCC = {b: dict(v[1]) for b, v in EST.items()}
PRED = {}
for b, ss in SUCC.items():
    for d in ss:
        PRED.setdefault(d, []).append(b)
_t = open(DUMP).read().split('\n')
_s = max(i for i, l in enumerate(_t) if l.startswith(FN + ' ()'))
BODY, _cur = {}, None
for _l in _t[_s:]:
    if _l.startswith(';; Function'):
        break
    _m = re.match(r'^;;   basic block (\d+),', _l)
    if _m:
        _cur = int(_m.group(1)); BODY[_cur] = ''; continue
    if _cur is not None:
        BODY[_cur] += _l.strip() + '\n'


def s(name):
    """a string argument as the dump prints it (literal or the .s's name)"""
    return r'(?:"%s"|&%s)' % (name, name)


def bb(pat, n=0):
    return [b for b in sorted(BODY) if re.search(pat, BODY[b])][n]


def succ_with(b, pat):
    x = [d for d in SUCC[b] if d in BODY and re.search(pat, BODY[d])]
    assert len(x) == 1, (b, pat, x)
    return x[0]


def option(name):
    """bool option blocks: T bootFlags test, O bootFlagsOff test, P perbox,
    PL perbox log, I iniBoolInvalid, G getIniBool; u32 options:
    U iniU32Invalid, GU getIniU32"""
    arg = s('str_' + name) + r'|"%s"' % name
    r = {}
    for k, pat in [('P', r'perboxExists \((%s)\)'), ('U', r'iniU32Invalid \((%s)\)'),
                   ('I', r'iniBoolInvalid \((%s)\)'), ('G', r'getIniBool \((%s), 0\)'),
                   ('GU', r'getIniU32 \((%s),')]:
        x = [b for b in sorted(BODY) if re.search(pat % arg, BODY[b])]
        if x:
            r[k] = x[0]
    if 'P' in r:
        # (olddvd: P -> Q -> I)
        r['PL'] = [x for x in SUCC[r['P']] if x != r['I'] and x not in PRED[r['I']]][0]
        p = PRED[r['P']]
        if len(p) == 1 and len(SUCC[p[0]]) == 2:
            r['O'] = p[0]
            q = PRED[r['O']]
            if len(q) == 1 and len(SUCC[q[0]]) == 2:
                r['T'] = q[0]
    return r


R = {n: option(n) for n in
     ['nomobile', 'noremap', 'noecdremap', 'nandmu', 'nosecurity', 'nosusecurity', 'smcnocheck',
      'cygnos', 'demon', 'patchsmc', 'smcnoeject', 'smcnoblink', 'nodvd', 'olddvd', 'cfldv',
      'cpufan', 'gpufan', 'cputemp', 'gputemp', 'edramtemp', 'overcputemp', 'overgputemp',
      'overedramtemp', 'avregion', 'gameregion', 'dvdregion']}


def header(name):
    """parseButton's inlined first tests: getIniValue, power, remopower,
    remox, winbutton, the part call, and the value store"""
    g = bb(r'getIniValue \(%s\)' % s('str_' + name))
    p = succ_with(g, s('str_power'))
    r = succ_with(p, s('str_remopower'))
    x = succ_with(r, s('str_remox'))
    w = succ_with(x, s('str_winbutton'))
    part = succ_with(w, r'parseButtonPart')
    st = [d for d in SUCC[p] if d != r][0]
    return g, p, r, x, w, part, st


strip = bb(r'if \(len_\d+ > i_\d+\)')
g1, p1, r1, x1, w1, part1, st1 = header('xellbutton')
g2, p2, r2, x2, w2, part2, st2 = header('xellbutton2')
g3, p3, r3, x3, w3, part3, st3 = header('dualboot')
dflt = bb(s('msg_xellDefault') + '|default console DVD eject')
alt = bb(s('msg_xellAltDisabled') + '|alternate xell button is disabled')
ign = bb(s('msg_dualbootIgnored') + '|dualboot setting ignored')
vs = bb(r'validateString \(')
warnc = bb(s('msg_iniMacidBadChars') + '|invalid characters in macid')
OVER = {}


def E(src, dst, p):
    OVER[(src, dst)] = p


# fixed edges
E(strip, succ_with(strip, r'!= 58'), 85)   # strip loop: ivopts uses the profile's trip count (<= 87%)
E(w1, part1, 45)       # winbutton's 36 is hoisted before its je (find_if_case_2: >= 50%)
E(st1, dflt, 50)       # equal: the lower-frequency default block still falls through, and the
                       # threaded constant store keeps half of the count (round 3's count test)
E(w2, part2, 71); E(w3, part3, 71)
E(p1, st1, 52)         # power match: edge under round 3's 90, so the header trace ends there
E(g2, p2, 69.8); E(g3, p3, 69.8)   # (higher loses the xor edx,edx hoist for the NULL path)
E(g1, p1, 100 - 52 * 100 / 245.0)  # xellbutton's NULL store: between the warnings and getIniU32
TARGET = {}
ETARGET = {}   # edge flows, for blocks with two preds
# label alignment threshold: freq_max / 100 must be 56 (between the padded
# and unpadded cold blocks below).  The strip loop (2535) would be the
# hottest block after the macid test loop is unrolled; a dead cycle through
# the blSuffix test (aio_never3, irreducible: aio_never4 enters its other
# block, so no preheader takes the count when it goes) leaves that test a
# stale 5650 instead.  Its rev block keeps 707
j2 = bb(r'aio_never3')
(bsfx,) = [d for d in SUCC[j2] if d in BODY and 'return' not in BODY[d]]
E(j2, bsfx, 100 * (1 - 1815 / 5650.0))
E(bb(r'aio_never4'), j2, 0.01)
TARGET[bb(r'getIniValue \(%s\)' % s('str_rev'))] = 707
mloop = bb(r'if \(_\d+ != 255\)')
if os.environ.get('AIO_MLOOP'):
    E(mloop, succ_with(mloop, r'i_\d+ = i_\d+ \+ 1'), float(os.environ['AIO_MLOOP']))
gmac = bb(r'getIniValue \(%s\)' % s('str_macid'))
smac = succ_with(gmac, r'strlen')
if os.environ.get('AIO_STRIP'):
    TARGET[gmac] = float(os.environ['AIO_STRIP']) / 0.85 * 1.0001
    TARGET[smac] = float(os.environ['AIO_STRIP'])


def opt(n, O=None, I=None, G=None):
    r = R[n]
    if O is not None:
        TARGET[r['O']] = O
        TARGET[r['P']] = O * 0.95
    if I is not None:
        TARGET[r['I']] = I
    if G is not None:
        TARGET[r['G']] = G


# round 3 (frequency 90..362): main options' O traces (plain keys) in the
# original's order; cygnos/demon/patchsmc have priority keys (their tests
# end round 1 traces), by frequency
for n, o in [('nomobile', 312), ('smcnocheck', 311), ('nosecurity', 310), ('nandmu', 309),
             ('noremap', 305), ('nosusecurity', 304), ('cygnos', 172), ('demon', 171),
             ('patchsmc', 170), ('smcnoblink', 153), ('smcnoeject', 152), ('nodvd', 73)]:
    opt(n, O=o)
# noecdremap: both of O's edges under 907, so O ends the hot trace and P gets
# a priority key: P/I/W come first in round 3 (right after the hot chain);
# W under 181 (10% of entry) so connect_traces doesn't copy the next test
ne = R['noecdremap']
TARGET[ne['O']] = 1100; TARGET[ne['P']] = 250; TARGET[ne['PL']] = 72; TARGET[ne['G']] = 14
TARGET[vs] = 165       # validateString: valid edge >= 90 (no priority for the warning), < cygnos's
TARGET[g2] = 220       # xellbutton2: power match >= 90 (no priority for the rest)
TARGET[g1] = 245       # xellbutton: its threaded constant store passes round 3's count test
b4 = PRED[g1][0]
TARGET[b4] = 600       # bootFlags & 4: keeps the header on its cold side
# round 4 (< 90): trace starts high to low, no priority keys
TARGET[R['olddvd']['PL']] = 74   # (its I and W, the rest of P, stay in round 2: >= 363)
# The original pads the dualButton test after olddvd's warning W as a loop
# label (branch > 4 x fallthru): W must be cold (65, branch 83+) and still be
# I's fallthru.  aio_never edges (wip/README.md) leave stale counts: I gets the
# Q test's count (435; I->W 390 >= round 2's 363, I->G 53 <= the threshold
# 56), and the merged `and ~4` block J a dead 250 that its jump to the test
# keeps
od = R['olddvd']
(odq,) = [x for x in PRED[od['I']]]
TARGET[od['I']] = 74
(q5,) = SUCC[od['PL']]
(odl,) = SUCC[[x for x in SUCC[od['I']] if x != od['G']][0]]
(z5,) = [x for x in PRED[q5] if x != od['PL'] and od['G'] not in PRED.get(x, [])]
ETARGET[(z5, q5)] = 250
ETARGET[(q5, odl)] = 250
(z3,) = [x for x in PRED[odq] if x != od['P']]
ETARGET[(z3, odq)] = 1      # (a dead pred keeps Q merged into I, not removed)
TARGET[warnc] = 67
# xellbutton2 header rest: 66 for its heap order, but 20 of it on a dead edge
# so its label isn't aligned (46 <= 56)
skip2 = [d for d in SUCC[p2] if d != r2][0]
ETARGET[(p2, r2)] = 46
ETARGET[(skip2, r2)] = 20
TARGET[g3] = 65        # dualboot getIniValue
TARGET[ign] = 40       # dualboot ignored (in its trace)
TARGET[R['cfldv']['GU']] = 64
TARGET[alt] = 63       # (2x < the edge past it: no "if (A) B; C" selection)
for n, i in [('nandmu', 62), ('noremap', 61), ('nomobile', 60), ('nosusecurity', 59), ('smcnocheck', 58), ('nosecurity', 57),
             ('cygnos', 40), ('demon', 39), ('smcnoblink', 18), ('patchsmc', 17), ('smcnoeject', 16), ('nodvd', 15)]:
    opt(n, I=i)
for k, n in enumerate(['gputemp', 'cputemp', 'gameregion', 'avregion', 'overedramtemp', 'overgputemp',
                       'gpufan', 'cpufan', 'overcputemp', 'edramtemp', 'dvdregion']):
    TARGET[R[n]['GU']] = 51 - k
TARGET[r3] = 19        # dualboot header rest (< 45% of its power test)
for k, n in enumerate(['noecdremap', 'noremap', 'nosusecurity', 'nomobile', 'smcnocheck', 'olddvd', 'nosecurity',
                       'nandmu', 'demon', 'patchsmc', 'smcnoblink', 'smcnoeject', 'cygnos', 'nodvd']):
    opt(n, G=14 - k)   # each below 45% of its I (W stays I's successor)


def freqs(over):
    probs = {}
    for b, ss in SUCC.items():
        for d, p in ss.items():
            probs[(b, d)] = p
    for (a, d), p in over.items():
        rest = [x for x in SUCC[a] if x != d]
        tot = sum(SUCC[a][x] for x in rest)
        for x in rest:
            probs[(a, x)] = SUCC[a][x] * (100 - p) / tot if tot else (100 - p) / len(rest)
        probs[(a, d)] = p
    x = {2: 1.0}
    for _ in range(5000):
        nx = {2: 1.0}
        for (a, d), p in probs.items():
            if d != 1:
                nx[d] = nx.get(d, 0) + x.get(a, 0) * p / 100
        done = all(abs(nx.get(k, 0) - x.get(k, 0)) < 1e-12 for k in nx)
        x = nx
        if done:
            break
    m = max(x.values())
    return {b: v * 10000 / m for b, v in x.items()}


for it in range(50):
    F = freqs(OVER)
    worst = 0
    for b, t in TARGET.items():
        (p,) = PRED[b]
        worst = max(worst, abs(F[b] - t))
        OVER[(p, b)] = round(min(99.99, max(0.01, t * 100 / F[p])), 4)
    for (a, b), t in ETARGET.items():
        worst = max(worst, abs(F[a] * OVER.get((a, b), SUCC[a][b]) / 100 - t))
        OVER[(a, b)] = round(min(99.99, max(0.01, t * 100 / F[a])), 4)
    if worst < 0.01:
        break
print("# applyIniOptions' edge probabilities (%) for its crafted profile: re/gcda.py")
print('# overrides in profile_estimate bb numbers of src/options.c.')
print('# Generated: python wip/aiodesign.py build/obj/options.fdo/-.042t.profile_estimate')
for (a, d), p in sorted(OVER.items()):
    print('%s:%d>%d=%g' % (FN, a, d, p))
