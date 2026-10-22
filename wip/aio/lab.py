"""Role labels for applyIniOptions blocks, original vs ours (-dA o.s).
python lab.py <o.s> [bbro dump] -> two columns of labels (name:role)"""
import os, difflib, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BITS = {0x20000000: 'nomobile', 0x40000000: 'noremap', 0x80000000: 'noecdremap', 0x10000000: 'nandmu',
        0x4000000: 'nosecurity', 0x1000000: 'nosusecurity', 0x200000: 'smcnocheck', 1: 'cygnos', 8: 'demon',
        0x8000000: 'patchsmc', 0x400000: 'smcnoeject', 0x800000: 'smcnoblink', 2: 'nodvd', 4: 'xell'}


def strings(lines, lab, val):
    t = {}
    for k, l in enumerate(lines[:-1]):
        m = re.match(lab, l)
        n = re.match(val, lines[k + 1])
        if m and n:
            t[m.group(1)] = n.group(1).replace('\\0', '').replace('\\12', '\\n')
    return t


def label(ins, st):
    """ins: list of instruction strings of one block."""
    txt = ' '.join(ins).replace('OFFSET __ImageBase', '4194304')
    names = [st[m] for m in re.findall(r'OFFSET (?:FLAT:)?([\w.]+)', txt) if m in st]
    name = next((n for n in names if re.match(r'^[a-z0-9]+$', n)), None)
    msgs = [n for n in names if not re.match(r'^[a-z0-9]+$', n)]
    calls = re.findall(r'call\s+(\S+)', txt)
    calls = [c.lstrip('_').split('.')[0] for c in calls]
    r = []
    if 'perboxExists' in calls: r.append('P')
    if 'iniBoolInvalid' in calls: r.append('I')
    if 'getIniBool' in calls: r.append('G')
    if 'iniU32Invalid' in calls: r.append('U')
    if 'getIniU32' in calls: r.append('GU')
    for m in msgs:
        if m.startswith('Using %s option (perbox'): r.append('PL')
        elif m.startswith('Using %s option (ini'): r.append('GL')
        elif m.startswith('***** WARNING: options.ini'): r.append('W')
        else: r.append('"' + m[:12] + '"')
    for c in calls:
        if c not in ('perboxExists', 'iniBoolInvalid', 'getIniBool', 'iniU32Invalid', 'getIniU32', 'log_printf'):
            r.append(c)
    if not name:
        # bit tests: bootFlagsOff byte/dword tests or ORs
        m = re.search(r'\bor\s+\w+, *(-?\w+)', txt)
        if m:
            v = int(m.group(1), 0) & 0xffffffff
            name = BITS.get(v, hex(v)); r.append('S')
        m = re.search(r'test\s+(?:BYTE|DWORD) PTR (?:\[?L_479f0([4-7])\]?|_xb\+(10[0-3])), *(\w+)', txt)
        if m:
            off = int(m.group(1)) - 4 if m.group(1) else int(m.group(2)) - 100
            v = (int(m.group(3), 0) & 0xff) << (8 * off) if 'BYTE' in txt else int(m.group(3), 0)
            name = name or BITS.get(v, hex(v)); r.append('O')
    j = [x for x in ins if re.match(r'\s*j\w+', x)]
    tail = re.match(r'\s*(j\w+)', j[-1]).group(1) if j else ('ret' if 'ret' in txt else '')
    return '%s:%s%s' % (name or '-', '+'.join(r) or '.', '/' + tail if tail else '')


def orig_blocks():
    lines = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'src', 'app', 'options.s')).read().split('\n')
    st = strings(lines, r'^(\w+):\s*$', r'\s*\.string "(.*)"')
    s = lines.index('_applyIniOptions:')
    out, cur = [], []
    for l in lines[s + 1:]:
        if l.startswith('#@C') or l.startswith('.section') or re.match(r'^_\w+:', l):
            break
        if re.match(r'^L_\w+:', l.strip()):
            if cur: out.append(cur)
            cur = []
            continue
        l = l.split('#')[0].strip()
        if not l or l.startswith('.'):
            continue
        cur.append(l)
        if re.match(r'(j\w+|ret)\b', l):
            out.append(cur); cur = []
    if cur: out.append(cur)
    return [label(b, st) for b in out]


def our_blocks(path):
    lines = open(path).read().split('\n')
    st = strings(lines, r'^(LC\d+):\s*$', r'\s*\.ascii "(.*)"')
    s = lines.index('_applyIniOptions:')
    out, ids, cur, cid = [], [], [], None
    for l in lines[s + 1:]:
        if l.startswith('\t.def'):
            break
        m = re.match(r'\s*# BLOCK (\d+)', l)
        if m:
            if cur: out.append(cur); ids.append(cid)
            cur, cid = [], int(m.group(1)); continue
        if re.match(r'^L\d+:', l) or l.strip().startswith('#') or l.strip().startswith('.'):
            continue
        if l.strip():
            cur.append(l.strip().replace('\t', ' '))
    if cur: out.append(cur); ids.append(cid)
    return [label(b, st) for b in out], ids


if __name__ == '__main__':
    o = orig_blocks()
    m, ids = our_blocks(sys.argv[1])
    for tag, a, b, c, d in difflib.SequenceMatcher(None, o, m, autojunk=False).get_opcodes():
        for k in range(max(b - a, d - c)):
            x = o[a + k] if a + k < b else ''
            y = m[c + k] if c + k < d else ''
            print('%s %-34s %-34s %s' % (' ' if tag == 'equal' else '*', x, y, ids[c + k] if c + k < d else ''))
