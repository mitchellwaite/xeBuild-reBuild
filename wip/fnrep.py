"""Try variants of one function against the original.

python wip/fnrep.py <base.c> <variants.c> <name> [-v] [gcc flags...]

variants.c holds whole definitions of <name> separated by lines of
'=====' (write it with a generator or the Write tool; shell heredocs mangle
backslash escapes).  Each variant replaces <name>'s definition in base.c,
is written to build/fnrep/repN.c and compared with re/fncmp.py.  Prints the
number of differing lines per variant (MATCH for none); -v also prints
the diffs.  -b scores by wip/blk.py's block-order diff instead.  -c=<other> compares <other> instead of <name> (to see how a
change to an inlined function shows up in its caller).  Compile errors are reported as ERROR, never as a match.
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base, vfile, fn = sys.argv[1:4]
verbose = '-v' in sys.argv
blk = '-b' in sys.argv
cmp = next((a[3:] for a in sys.argv[4:] if a.startswith('-c=')), fn)
flags = [a for a in sys.argv[4:] if a not in ('-v', '-b') and not a.startswith('-c=')]
s = open(base).read()
m = re.search(r'^[^\n]*\b%s\([^)]*\)\n\{.*?^\}\n' % fn, s, re.S | re.M)
if not m:
    sys.exit('%s: no definition of %s' % (base, fn))
outdir = os.path.join(ROOT, 'build', 'fnrep')
os.makedirs(outdir, exist_ok=True)
for k, v in enumerate(open(vfile).read().split('=====\n')):
    out = os.path.join(outdir, 'rep%d.c' % k)
    open(out, 'w', newline='\n').write(s[:m.start()] + v.strip('\n') + '\n' + s[m.end():])
    tool = os.path.join(ROOT, 'wip', 'blk.py') if blk else os.path.join(ROOT, 're', 'fncmp.py')
    r = subprocess.run([sys.executable, tool, out, cmp] + flags,
                       capture_output=True, text=True, cwd=ROOT)
    o = (r.stdout + r.stderr).strip()
    if blk and r.returncode == 0:
        o = o if re.search(r'^[-+][^-+]', o, re.M) else 'MATCH'
    if o != 'MATCH' and not o.startswith('---'):
        print('variant %d: ERROR' % k, o[:300])
        continue
    n = 0 if o == 'MATCH' else len([l for l in o.split('\n') if re.match(r'^[-+][^-+]', l)])
    print('variant %d: %s' % (k, 'MATCH' if n == 0 else n), out if n == 0 else '')
    if verbose and n:
        print(o)
