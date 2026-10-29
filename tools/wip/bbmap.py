"""Print bb-reorder traces with source lines and successor edges.
python tools/wip/bbmap.py <src.c> <fn> [gcc flags]
Compiles with -fdump-rtl-bbro-details and -fdump-rtl-cprop_hardreg-blocks (the
pass before bbro, so bb numbers agree with the trace listing)."""
import glob, os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TC = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin')
src, fn = sys.argv[1:3]
flags = sys.argv[3:] or ['-O3']
out = os.path.join(ROOT, 'build', 'bbmap')
os.makedirs(out, exist_ok=True)
for f in glob.glob(os.path.join(out, '*')):
    os.remove(f)
base = os.path.join(out, 'x.c')
open(base, 'w', newline='\n').write(open(src).read())
env = dict(os.environ, PATH=TC + os.pathsep + os.environ['PATH'])
subprocess.run([os.path.join(TC, 'gcc.exe'), '-S', '-fno-asynchronous-unwind-tables'] + flags +
               ['-fdump-rtl-bbro-details', '-fdump-rtl-cprop_hardreg-blocks-details', base, '-o', os.devnull],
               env=env, check=True, cwd=out)


def fnpart(path):
    t = open(path).read()
    m = re.search(r'^;; Function %s .*?(?=^;; Function |\Z)' % fn, t, re.S | re.M)
    return m.group(0)


pre = fnpart(glob.glob(os.path.join(out, '*.cprop_hardreg'))[0])
bbro = fnpart(glob.glob(os.path.join(out, '*.bbro'))[0])
srcl = open(src).read().split('\n')
bbline, succ, cur, insucc = {}, {}, None, False
for l in pre.split('\n'):
    m = re.match(r'^;; basic block (\d+),', l)
    if m:
        cur = int(m.group(1))
        continue
    m = re.match(r'^;;\s+succ:\s+(.*)$', l)
    if m and cur is not None:
        insucc = True
        succ[cur] = ' '.join('%s[%s]' % e for e in re.findall(r'(\w+) \[([\d.]+)%\]', m.group(1)))
        continue
    if l.startswith(';;   ') and cur is not None and insucc:
        succ[cur] += ' ' + ' '.join('%s[%s]' % e for e in re.findall(r'(\w+) \[([\d.]+)%\]', l))
        continue
    insucc = False
    m = re.search(r'x\.c:(\d+)', l)
    if m and cur is not None:
        bbline.setdefault(cur, set()).add(int(m.group(1)))


def desc(b):
    ls = sorted(bbline.get(b, ()))
    if not ls:
        return '?'
    return '%s %s' % (','.join(map(str, ls)), srcl[ls[-1] - 1].strip()[:46])


for l in bbro.split('\n'):
    m = re.match(r'^Trace (\d+) \(round (\d+)\):\s+(.*)$', l)
    if m:
        print('Trace %s r%s' % (m.group(1), m.group(2)))
        for b, f in re.findall(r'(\d+) \[(\d+)\]', m.group(3)):
            print('   bb%-3s %5s  %-60s -> %s' % (b, f, desc(int(b)), succ.get(int(b), '')))
    elif l.startswith('Connection') or l.startswith('Duplicated'):
        print(l)
