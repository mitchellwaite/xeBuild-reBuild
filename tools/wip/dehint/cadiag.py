"""Diagnostic only, never in a result: __builtin_expect on netMount at several probabilities.

python tools/wip/dehint/cadiag.py <file.c>
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
src = open(sys.argv[1]).read()
old = 'if (netMount(SYSEX, "\\\\SEP"))'
new = 'if (__builtin_expect(netMount(SYSEX, "\\\\SEP"), 1))'
assert old in src
d = os.path.join(ROOT, 'build', 'ca', 'diag')
os.makedirs(d, exist_ok=True)
p = os.path.join(d, 'm.c')
open(p, 'w', newline='\n').write(src.replace(old, new))
for prob in (51, 52, 55, 60, 65, 70, 75, 80, 85, 90, 95):
    r = subprocess.run([sys.executable, os.path.join(ROOT, 'tools/re/fncmp.py'), p, 'sendAvatarData', '-O3', '-I', os.path.join(ROOT, 'src'),
                        '--param', 'builtin-expect-probability=%d' % prob], capture_output=True, text=True)
    n = len([l for l in r.stdout.split('\n') if re.match(r'^[-+][^-+]', l)])
    print(prob, 'MATCH' if r.stdout.strip() == 'MATCH' else n)
    if len(sys.argv) > 2 and int(sys.argv[2]) == prob:
        print(r.stdout)
