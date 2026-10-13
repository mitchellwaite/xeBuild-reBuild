"""Parse a GNU ld -Map file into input-section contributions.

python re/mapparse.py <file.map> [section ...]   -> compact listing
"""
import re, sys, os

LINE = re.compile(r'^ (\S+)?\s+0x([0-9a-f]+)\s+0x([0-9a-f]+)\s+(.+)$')
OUT = re.compile(r'^(\.\S+)\s+0x([0-9a-f]+)\s+0x([0-9a-f]+)')
FILL = re.compile(r'^ \*fill\*\s+0x([0-9a-f]+)\s+0x([0-9a-f]+)')
SYM = re.compile(r'^\s+0x([0-9a-f]+)\s+([A-Za-z_.$@?][^\s=]*)\s*$')


def short(path):
    m = re.search(r'([^/\\]+\.a)\(([^)]+)\)$', path)
    if m:
        return '%s(%s)' % (m.group(1), m.group(2))
    return os.path.basename(path)


def parse(path):
    """Return {output_section: [entries]} where entry = dict(kind, sec, addr, size, obj, syms)."""
    out = {}
    cur = None
    pending = None
    started = False
    for raw in open(path, encoding='utf-8', errors='replace'):
        line = raw.rstrip('\n')
        if line.startswith('Linker script and memory map'):
            started = True
            continue
        if not started:
            continue
        m = OUT.match(line)
        if m:
            cur = m.group(1)
            out.setdefault(cur, [])
            continue
        if cur is None:
            continue
        m = FILL.match(line)
        if m:
            out[cur].append(dict(kind='fill', sec='*fill*', addr=int(m.group(1), 16), size=int(m.group(2), 16), obj='', syms=[]))
            continue
        # input section name may be on its own line when long
        if pending is not None:
            m2 = re.match(r'^\s+0x([0-9a-f]+)\s+0x([0-9a-f]+)\s+(.+)$', line)
            if m2:
                out[cur].append(dict(kind='in', sec=pending, addr=int(m2.group(1), 16), size=int(m2.group(2), 16), obj=short(m2.group(3)), syms=[]))
                pending = None
                continue
            pending = None
        m = LINE.match(line)
        if m and m.group(1):
            out[cur].append(dict(kind='in', sec=m.group(1), addr=int(m.group(2), 16), size=int(m.group(3), 16), obj=short(m.group(4)), syms=[]))
            continue
        m = re.match(r'^ (\.\S+|COMMON)\s*$', line)
        if m:
            pending = m.group(1)
            continue
        m = SYM.match(line)
        if m and out[cur]:
            out[cur][-1]['syms'].append((int(m.group(1), 16), m.group(2)))
    return out


if __name__ == '__main__':
    mp = parse(sys.argv[1])
    secs = sys.argv[2:] or list(mp)
    for s in secs:
        print('==', s)
        for e in mp.get(s, []):
            if e['size'] == 0 and not e['syms']:
                continue
            print('  %08x %6x %-14s %s %s' % (e['addr'], e['size'], e['sec'], e['obj'],
                                          ' '.join(n for _, n in e['syms'][:4])))
