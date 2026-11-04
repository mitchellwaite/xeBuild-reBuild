"""keysdump.py <fn> <pass> <file|-> [site,site..]: print one gcc dump's section for fn.

pass is a dump flag such as tree-profile_estimate-details or rtl-bbro-details.  The
whole dump stays at build/keys/v/dump/.  Flags come from KEYSFLAGS if set."""
import glob, os, re, subprocess, sys
import keyslib as K
import keyssubset as S

fn, pas, f = sys.argv[1:4]
s = K.base() if f == '-' else open(f, newline='').read()
if len(sys.argv) > 4 and sys.argv[4]:
    for x in sys.argv[4].split(','):
        w, n = x.split(':')
        for name, old, new in S.SITES[w]:
            if name == n:
                assert old in s, old
                s = s.replace(old, new)
d = os.path.join(K.OUT, 'dump')
os.makedirs(d, exist_ok=True)
for x in glob.glob(os.path.join(d, '*')):
    os.remove(x)
fl = os.environ.get('KEYSFLAGS')
fl = fl.split() if fl else list(K.FLAGS)
inp = ('#line 1 "keys.c"\n' + s).encode()
subprocess.run([K.GCC, '-c'] + fl + ['-f' + 'dump-' + pas, '-I' + os.path.join(K.R, 'src'), '-x', 'c', '-',
                '-o', os.path.join(d, 'x.o')], input=inp, cwd=d)
for x in glob.glob(os.path.join(d, '*')):
    if x.endswith('.o'):
        continue
    t = open(x, errors='replace').read()
    parts = re.split(r'(?m)^(?=;; Function )', t)
    for p in parts:
        if p.startswith(';; Function ' + fn + ' '):
            print(p)
