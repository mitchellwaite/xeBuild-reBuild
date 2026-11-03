"""python tools/wip/dehint/nrdump.py <dir> <src.c> [flags]: dumps for one source; prints for netRecvVerbose and
its clone: bb freqs and edge probs after profile_estimate-derived (bbro) order, IRA threads and pops.
Keeps the dumps in <dir>."""
import os, re, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BIN = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin')
d, src = sys.argv[1], os.path.abspath(sys.argv[2])
flags = sys.argv[3:] or ['-O3']
os.makedirs(d, exist_ok=True)
shutil.copy(src, os.path.join(d, 'a.c'))
env = dict(os.environ, PATH=BIN + os.pathsep + os.environ['PATH'])
subprocess.run([os.path.join(BIN, 'gcc.exe'), '-S', '-masm=intel', '-I', os.path.join(ROOT, 'src'),
                '-fno-asynchronous-unwind-tables', '-fdump-rtl-ira', '-fdump-rtl-bbro-details-blocks',
                '-fdump-tree-profile_estimate-details-blocks', '-fdump-tree-optimized-blocks', '-fdump-ipa-cp-details'] + flags + ['a.c', '-o', 'a.s'],
               cwd=d, env=env, check=True)


def fn(t, name):
    out = []
    for m in re.finditer(r'^;; Function (\S+)', t, re.M):
        if m.group(1) == name or m.group(1).startswith(name + '.constprop'):
            e = t.find('\n;; Function ', m.end())
            out.append((m.group(1), t[m.start():e if e > 0 else len(t)]))
    return out


for f in sorted(os.listdir(d)):
    if f.endswith('r.ira'):
        t = open(os.path.join(d, f)).read()
        for n, s in fn(t, 'netRecvVerbose'):
            print('== IRA', n)
            names = {}
            for m in re.finditer(r'\(reg(?:/\w+)*:\w+ (\d+)(?: \[ ([^\]]*) \])?', s):
                if m.group(2):
                    names.setdefault(m.group(1), m.group(2).strip())
            info = {}
            for m in re.finditer(r'a(\d+)\(r(\d+),l0\) costs:.*?MEM:(-?\d+)', s):
                info[m.group(2)] = m.group(3)
            for l in s.split('\n'):
                if 'Result (freq' in l:
                    print(l.strip())
            for m in re.finditer(r'Pushing a(\d+)\(r(\d+),l0\)([^\n]*)', s):
                print('push a%s r%s %s %s' % (m.group(1), m.group(2), names.get(m.group(2), '?'), m.group(3)))
            for m in re.finditer(r'Popping a(\d+)\(r(\d+),l0\)\s+--\s+(.*)', s):
                print('r%-4s %-14s mem=%-7s %s' % (m.group(2), names.get(m.group(2), '?'), info.get(m.group(2)), m.group(3)))
    if f.endswith('r.bbro'):
        t = open(os.path.join(d, f)).read()
        for n, s in fn(t, 'netRecvVerbose'):
            print('== BBRO', n)
            i = s.find('Reordering with the STC')
            freq = {}
            for m in re.finditer(r'^;; bb (\d+) .*|basic block (\d+), loop depth \d+, count \d+, freq (\d+)', s, re.M):
                if m.group(2):
                    freq.setdefault(m.group(2), m.group(3))
            order = re.findall(r'Getting bb (\d+)|(STC - round \d)', s[i:]) if i >= 0 else []
            print(' '.join('[%s]' % r[-1] if r else '%s:%s' % (b, freq.get(b, '?')) for b, r in order))
