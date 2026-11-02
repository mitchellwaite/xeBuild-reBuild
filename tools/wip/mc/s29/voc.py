"""voc.py: vocabulary of zero-byte asm-goto edits for the plain mode_client compile.
An edit = (site, [targets]); a site is a statement in mode_client's post-loop code or in
clientEraseBlock, 'X<' puts the JMP before it, 'X>' after it (the statement is wrapped in braces
so the JMP stays in the same arm).  Only forward targets (label later in the source than the
site) are allowed (no new cycles).  New labels (s4, eout, einv, esucc, eerase) are always placed."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen
B = gen.BODY
N = chr(92) + 'n'
MC0 = B.index('int mode_client(int argc')
EB0 = B.index('void clientEraseBlock(')
EB1 = B.index('/* the option', EB0)
LOOP1 = B.index('\tif (NO_MODE_ARG(mode, arg))', MC0)
H4 = 'log_printf(0, "' + N + N + '***** ERROR: cannot send avatar data when a HDD does not exist!' + N + '");'
H5 = 'log_printf(0, "' + N + N + '***** ERROR: cannot send xbox compatibility data when a HDD does not exist!' + N + '");'
EOUT = 'log_printf(0, "' + N + N + '***** ERROR: Block 0x%x is outside system area!' + N + '", block);'
EFAIL = 'log_printf(0, "' + N + N + '***** ERROR: Failed to erase block 0x%x!' + N + '", block);'
EINV = 'log_printf(0, "' + N + N + '***** ERROR: Invalid arguments specified, please provide hex only for offset!' + N + '");'
ESUCC = 'log_printf(0, "Success!' + N + '");'
EERASE = 'log_printf(0, "erasing block 0x%x...", block);'
ETOP = 'uint32_t block = myatoh32(sblock, -1);'
CDEF = 'log_printf(0, "' + N + N + '***** ERROR: invalid mode specified, please inform author' + N + '");'
CALLS = {'c1': 'netDumpNand(arg);', 'c2': 'clientWrite(arg);', 'c3': 'clientKeys();', 'c8': 'clientReadBlocks(arg, start, count);',
         'c9': 'clientWriteBlocks(arg, start);', 'c10': 'clientEraseBlock(arg);', 'c11': 'clientBinPatch(arg, start);',
         'h4': H4, 'h5': H5, 's4': 'sendAvatarData(arg, cinfo->kernel);', 's5': 'sendCompatData(arg);',
         'p0': 'clientPatches(NULL);', 'p1': 'clientPatches(arg);', 'i0': 'clientInfo(NULL);', 'i1': 'clientInfo(arg);',
         'cdef': CDEF, 'rok': 'cinfo = netGetInfo();'}
EBCALLS = {'etop': ETOP, 'eerase': EERASE, 'esucc': ESUCC, 'efail': EFAIL, 'eout': EOUT, 'einv': EINV}
STMT = {}   # site base -> (start, end)
for k, a in CALLS.items():
    p = B.index(a, LOOP1); STMT[k] = (p, p + len(a), 'mc')
for k, a in EBCALLS.items():
    p = B.index(a, EB0); assert p < EB1, k; STMT[k] = (p, p + len(a), 'eb')
NEWLAB = {'s4': STMT['s4'][0], 'eout': STMT['eout'][0], 'einv': STMT['einv'][0], 'esucc': STMT['esucc'][0],
          'eerase': STMT['eerase'][0]}
LABPOS = dict(NEWLAB)
for m in re.finditer(r'AT\((\w+)\)', B):
    if m.start() > EB0: LABPOS[m.group(1)] = m.start()
_c7 = B.index('AT(c7) if (arg == dummy)', LOOP1) + 7
_c12 = B.index('AT(c12) if (arg == dummy)', LOOP1) + 8
_c6 = B.index('break;', B.index('case 6:', LOOP1))
RAW = {'c7t': (_c7, 'mc', ['c7']), 'c12t': (_c12, 'mc', ['c12']), 'c6': (_c6, 'mc', []),
       'eneg': (B.index('if (block != -1)', EB0), 'eb', []), 'elt': (B.index('if (block < cinfo', EB0), 'eb', []),
       'enet': (B.index('if (netEraseBlockU32', EB0), 'eb', ['eerase'])}
SITES = {}
for k, (p, reg, pl) in RAW.items():
    SITES[k + '<'] = (p, p, 'raw', reg)
for k, (s, e, reg) in STMT.items():
    if k != 'etop': SITES[k + '<'] = (s, e, 'pre', reg)
    SITES[k + '>'] = (s, e, 'post', reg)
MCLABS = ['u2', 'c1', 'c2', 'c3', 'hdd4', 's4', 's5', 'hdd5', 'c7', 'p0', 'p1', 'c8', 'c9', 'c10', 'c11', 'c12', 'i0', 'i1', 'cdef']
EBLABS = ['eerase', 'esucc', 'efail', 'eout', 'einv']


# labels on the path from the region entry to each site base (targets that would close a cycle)
PATHLABS = {'c1': ['c1'], 'c2': ['c2'], 'c3': ['c3'], 'c8': ['c8'], 'c9': ['c9'], 'c10': ['c10'], 'c11': ['c11'],
            'h4': ['hdd4'], 's4': ['s4'], 'h5': ['hdd5'], 's5': ['s5'], 'p0': ['c7', 'p0'], 'p1': ['c7', 'p1'],
            'i0': ['c12', 'i0'], 'i1': ['c12', 'i1'], 'cdef': ['cdef'], 'rok': [],
            'etop': [], 'eerase': ['eerase'], 'esucc': ['eerase', 'esucc'], 'efail': ['eerase', 'efail'],
            'eout': ['eout'], 'einv': ['einv']}
for _k, (_p, _r, _pl) in RAW.items(): PATHLABS[_k] = _pl
FORWARD = os.environ.get('FORWARD') == '1'


def targets_for(site):
    s, e, kind, reg = SITES[site]
    labs = MCLABS if reg == 'mc' else EBLABS
    if FORWARD:
        p = e if kind == 'post' else s
        return [l for l in labs if LABPOS[l] > p]
    bad = set(PATHLABS[site[:-1]])
    return [l for l in labs if l not in bad]


# dead-edge (bcp) injection sources (s19): '!SRC:W' sites, one target label each
ISRC = {'after': (LOOP1, 'mode', 'mc'), 'rok': (STMT['rok'][0], 'mode', 'mc'),
        'fail': (B.index('\tlog_printf(0, "' + N + N + '***** ERROR: unable to connect', MC0), 'mode', 'mc'),
        'ebtop': (STMT['etop'][1], 'block', 'eb')}
BCP = lambda v: '__builtin_constant_p(%s)' % v
IW = {'b': lambda v: BCP(v), 'p': lambda v: '(char *)%s == (char *)1' % BCP(v), 'q': lambda v: '%s == 3' % BCP(v),
      'pp': lambda v: '(char *)%s == (char *)1 && (char *)%s == (char *)1' % (BCP(v), BCP(v + ' + 1'))}
for _s in ISRC:
    for _w in IW:
        SITES['!%s:%s' % (_s, _w)] = None
ITARGETS = {'mc': [l for l in MCLABS], 'eb': EBLABS}


def itargets(site):
    s = site[1:].split(':')[0]
    reg = ISRC[s][2]
    labs = ITARGETS[reg]
    if s == 'rok': labs = [l for l in labs if l != 'u2']
    return labs


_tf = targets_for


def targets_for(site):
    if site.startswith('!'): return itargets(site)
    return _tf(site)


def dup(text):
    """keep the standalone clientEraseBlock plain and give mode_client a static copy (with this
    variant's clientEraseBlock edits) right after it: clientEraseBlockI."""
    s = text.index('void clientEraseBlock(')
    e = text.index('/* the option', s)
    edited = text[s:e]
    plain = B[EB0:EB1]
    copy = 'static ' + edited.replace('void clientEraseBlock(', 'void clientEraseBlockI(', 1)
    out = text[:s] + plain + copy + text[e:]
    c = out.index('clientEraseBlock(arg);', out.index('int mode_client(int argc'))
    return out[:c] + 'clientEraseBlockI(arg);' + out[c + len('clientEraseBlock(arg);'):]


DUP = os.environ.get('DUP') == '1'
_make = None


def make(edits, inj=(), dupl=None):
    t = make0(edits, inj)
    if dupl if dupl is not None else DUP: t = dup(t)
    return t


def make0(edits, inj=()):
    """edits: list of (site, [targets]); inj: extra (offset, text) insertions."""
    ins = []
    for k, p in NEWLAB.items():
        ins.append((p, 0, '%s: ' % k))
    for n, (site, tg) in enumerate(edits):
        if site.startswith('!'):
            s, w = site[1:].split(':')
            off, var, reg = ISRC[s]
            for t in tg:
                ins.append((off, 3, 'if (%s) goto %s;\n' % (IW[w]('%s + %d' % (var, 10 * (n + 1) + len(ins))), t)))
    for site, tg in edits:
        if site.startswith('!'): continue
        s, e, kind, reg = SITES[site]
        j = 'JMP(%s);' % ','.join(tg)
        if kind == 'raw':
            ins.append((s, 1, j + ' '))
        elif kind == 'pre':
            ins.append((s, 1, '{ ' + j + ' ')); ins.append((e, 1, ' }'))
        else:
            ins.append((s, 1, '{ ')); ins.append((e, 1, ' ' + j + ' }'))
    ins += [(p, 2, t) for p, t in inj]
    out = B
    # same offset: labels first, then braces (label: { JMP; stmt })
    for p, o, t in sorted(ins, key=lambda x: (-x[0], -x[1])):
        out = out[:p] + t + out[p:]
    return out
