"""fl10a.py cfg <dumpsuffix> <fn> <tag> [src-form]: compact cfg with frequencies from a -blocks-details dump in build/filelist_ini/a10/d/<tag>.
fl10a.py freq <tag>...: frequency tables of .optimized for the four getters.
fl10a.py assign <tag> <fn>: LRA assignment lines of the first assignment pass, with a running usage table."""
import os, re, sys
import fl10lib as F

GETTERS = ['getIniBool', 'iniBoolInvalid', 'getIniU32', 'iniU32Invalid']


def blocks(part):
    # skip "Removing basic block" noise: use only lines after the function header line "name (args)\n{"
    r = []
    cur = None
    for ln in part.splitlines():
        m = re.match(r';;\s+basic block (\d+), loop depth (\d+), count \d+, freq (\d+)', ln)
        if m:
            cur = dict(bb=int(m.group(1)), depth=int(m.group(2)), freq=int(m.group(3)), st=[], succ=[])
            r.append(cur)
            continue
        if cur is None:
            continue
        m = re.match(r';;\s+(?:succ:)?\s+(\d+|EXIT) \[([0-9.]+)%\]', ln)
        if m and ('succ' in ln or (cur['succ'] and not ln.startswith(';;    pred'))):
            cur['succ'].append((m.group(1), m.group(2)))
            continue
        if ln.startswith(';;'):
            continue
        s = ln.strip()
        if s and s not in ('{', '}') and not s.startswith('goto') and not s.startswith('else'):
            cur['st'].append(s)
    return r


def cfg(d, suf, fn):
    for b in blocks(F.fn_part(d, suf, fn)):
        print('bb%-3d d%d f%-5d -> %s' % (b['bb'], b['depth'], b['freq'], ' '.join('%s:%s' % x for x in b['succ'])))
        print('     ' + ' ; '.join(b['st'])[:220])


def assign(d, fn):
    part = F.fn_part(d, 'reload', fn)
    use = {}
    for ln in part.splitlines():
        m = re.search(r'Assign (\d+) to (.*?)r(\d+) \(freq=(\d+)\)', ln)
        if m:
            hr, kind, r, fr = int(m.group(1)), m.group(2), int(m.group(3)), int(m.group(4))
            use[hr] = use.get(hr, 0) + fr
            print('r%-4d %-20s -> %d freq %-5d usage %s' % (r, kind, hr, fr, sorted(use.items())))
        if 'Reassigning non-reload' in ln:
            print('--')
            use = {}


if __name__ == '__main__':
    if sys.argv[1] == 'cfg':
        cfg(os.path.join(F.A10, 'd', sys.argv[4]), sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'freq':
        for tag in sys.argv[2:]:
            d = os.path.join(F.A10, 'd', tag)
            for fn in GETTERS:
                print(tag, fn, [b['freq'] for b in blocks(F.fn_part(d, 'optimized', fn))])
    elif sys.argv[1] == 'assign':
        assign(os.path.join(F.A10, 'd', sys.argv[2]), sys.argv[3])
