"""bb-reorder traces of sendAvatarData, with each block's literal and frequency.

python tools/wip/dehint/catrace.py <file.c> [flags]
Compiles into build/ca/tr/<name>/ with -fdump-rtl-bbro-details-blocks, prints the
pop order per round and each trace, blocks named by their first string literal.
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BIN = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin')
env = dict(os.environ, PATH=BIN + os.pathsep + os.environ['PATH'])
src = os.path.abspath(sys.argv[1])
d = os.path.join(ROOT, 'build', 'ca', 'tr', os.path.basename(src))
os.makedirs(d, exist_ok=True)
a = os.path.join(d, 'a.c')
open(a, 'w', newline='\n').write(open(src).read())
r = subprocess.run([os.path.join(BIN, 'gcc.exe'), '-S', '-masm=intel', '-O3', '-I', os.path.join(ROOT, 'src'),
                    '-fno-asynchronous-unwind-tables', '-fdump-rtl-bbro-details-blocks'] + sys.argv[2:] + ['a.c', '-o', 'a.s'],
                   env=env, capture_output=True, text=True, cwd=d)
if r.returncode:
    sys.exit(r.stderr)
s = open(os.path.join(d, 'a.s')).read()
lits = dict(re.findall(r'^(LC\d+):\n\t\.ascii "([^"]*)', s, re.M))
f = next(x for x in os.listdir(d) if x.endswith('.bbro'))
t = open(os.path.join(d, f)).read()
m = re.search(r'^;; Function sendAvatarData \(', t, re.M)
t = t[m.start():t.find('\n;; Function ', m.end())]
name = {}
freq = {}
parts = re.split(r'^;; basic block (\d+), loop depth \d+, count \d+, freq (\d+)', t, flags=re.M)
for i in range(1, len(parts), 3):
    bb, fq, body = parts[i], parts[i + 1], parts[i + 2]
    freq[bb] = fq
    l = re.search(r'"\*(LC\d+)"', body)
    c = re.search(r'symbol_ref:SI \("_(\w+)"\)', body)
    if bb not in name or l or c:
        name.setdefault(bb, '')
        if not name[bb]:
            name[bb] = (lits.get(l.group(1), '?')[:22] if l else '') or (c.group(1) if c else '')
for rnd in re.findall(r'(STC - round \d|Getting bb \d+|^Trace \d+ \(round \d\):.*$)', t, re.M):
    if rnd.startswith('Getting'):
        b = rnd.split()[-1]
        print('  get', b, freq.get(b), name.get(b))
    elif rnd.startswith('Trace'):
        print(rnd, ' || ', ' '.join('%s=%s' % (b, (name.get(b) or '-')[:14]) for b in re.findall(r' (\d+) \[', rnd)))
    else:
        print(rnd)
