"""fo.py DIR [DIR2]: final block order of mode_update from a dump dir (build/v/mu_d1/TAG, made with mu.py -d), named from bbro RTL.
Only the part after the round-3 traces (cold tail) is shown by default, as 'bb[freq]name'.  With DIR2, prints the two side by side."""
import re
import sys
import glob


def load(d):
    s = open(glob.glob(d + '/*bbro')[0]).read()
    s = s[s.index(';; Function mode_update'):]
    asm = open(d + '/m.s').read()
    lc = {}
    for m in re.finditer(r'^(LC\d+):\n\s+\.ascii "(.*)"$', asm, re.M):
        lc[m.group(1)] = m.group(2)
    i0 = s.index('Reordered sequence:')
    i1 = s.rindex('Reordered sequence:')
    parts = re.split(r'^\(note \d+ \d+ \d+ \d+ \[bb (\d+)\] NOTE_INSN_BASIC_BLOCK\)', s[i0:i1], flags=re.M)
    mp = {}
    for m in re.finditer(r'^ (\d+) (?:bb (\d+)|duplicate of (\d+))  \[(\d+)\]$', s[i0:i1], re.M):
        mp[int(m.group(1))] = (int(m.group(2) or m.group(3)), m.group(3) is not None, int(m.group(4)))
    nm = {}
    for k in range(1, len(parts), 2):
        b = mp[int(parts[k])]
        t = parts[k + 1]
        if b[1]:
            continue
        ss = [lc.get(x, x) for x in re.findall(r'symbol_ref/f:SI \("\*(LC\d+)"', t)]
        cs = re.findall(r'symbol_ref:SI \("(\w+)"\) \[flags 0x41\]', t)
        nm[b[0]] = (ss[0].replace('\\12', '').replace('\\0', '').replace('*', '').strip()[:26] if ss else '') or (','.join(cs)[:20]) or '.'
    fr = {}
    for n, r, body in re.findall(r'^Trace (\d+) \(round (\d+)\):\s+(.*)$', s, re.M):
        for x in re.findall(r'(\d+) \[(\d+)\]', body):
            fr[int(x[0])] = (int(x[1]), int(r), int(n))
    fin = [int(x) for x in re.search(r'Final order:\n(.*)', s).group(1).split()]
    return fin, nm, fr


def show(d):
    fin, nm, fr = load(d)
    out = []
    for b in fin:
        f = fr.get(b, (0, 0, 0))
        if f[1] >= 4:
            out.append('%d[%d]%s' % (b, f[0], nm.get(b, '')))
    return out


if __name__ == '__main__':
    a = show(sys.argv[1])
    if len(sys.argv) > 2:
        b = show(sys.argv[2])
        for i in range(max(len(a), len(b))):
            print('%-44s %s' % (a[i] if i < len(a) else '', b[i] if i < len(b) else ''))
    else:
        print('\n'.join(a))
