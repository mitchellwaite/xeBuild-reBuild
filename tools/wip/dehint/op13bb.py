"""Attempt 13: name applyIniOptions' blocks in a bbro dump by source line, calls and
literals (run.sh's aio.bbro), and print each trace with them.

python tools/wip/dehint/op13bb.py build/v/aio_p1/TAG [ids..]"""
import re, sys

d = sys.argv[1]
t = open(d + '/aio.bbro').read()
# block contents from the pass before bbro (same ids as bbro's traces)
pre = open(d + '/a.c.272r.cprop_hardreg').read()
pre = pre[pre.index(';; Function applyIniOptions'):]
pre = pre[:pre.index(';; Function', 10)]
blocks = {}
cur = None
for line in pre.splitlines():
    m = re.search(r'NOTE_INSN_BASIC_BLOCK', line)
    if m:
        mm = re.search(r'\[bb (\d+)\]', line)
        if mm:
            cur = int(mm.group(1))
            blocks.setdefault(cur, {'lines': [], 'calls': [], 'lcs': []})
        continue
    if cur is None:
        continue
    for x in re.findall(r'a\.c:(\d+)', line):
        if not blocks[cur]['lines'] or blocks[cur]['lines'][-1] != int(x):
            blocks[cur]['lines'].append(int(x))
    for x in re.findall(r'symbol_ref(?:/\w+)?:SI \("\*?(\w+)"\)', line):
        if x.startswith('LC'):
            blocks[cur]['lcs'].append(x)
        elif 'call' in line or True:
            if x not in ('xb',):
                blocks[cur]['calls'].append(x)

src = open(d + '/a.c').read().split('\n')
LCS = dict(re.findall(r'^(LC\d+):\n\t\.ascii "([^"]{0,14})', open(d + '/o.s').read(), re.M))


def name(b):
    i = blocks.get(b)
    if not i:
        return '?'
    ls = i['lines']
    s = ''
    if ls:
        s = '%d' % ls[0]
    cs = [c for c in i['calls'] if not c.startswith('LC')]
    if cs:
        s += ':' + ','.join(dict.fromkeys(cs))
    if i['lcs']:
        s += ':' + '|'.join(LCS.get(x, x) for x in dict.fromkeys(i['lcs']))
    return s or '-'


if len(sys.argv) > 2:
    for b in sys.argv[2:]:
        b = int(b)
        i = blocks.get(b, {})
        print(b, name(b), [src[l - 1].strip()[:70] for l in dict.fromkeys(i.get('lines', []))])
    sys.exit()
for m in re.finditer(r'^Trace (\d+) \(round (\d+)\):\s*(.*)$', t, re.M):
    items = re.findall(r'(\d+) \[(\d+)\]', m.group(3))
    print('T%-3s r%s  ' % (m.group(1), m.group(2)) + '  '.join('%s[%s]%s' % (b, f, name(int(b))) for b, f in items))
