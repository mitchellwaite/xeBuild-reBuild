"""mode_client with a crafted profile (tools/re/gcda.py), like tools/wip/mufdo.sh for mode_update.

python tools/wip/mcfdo.py <dir> <draft.c> [fn:src>dst=prob ...]
Copies the draft to <dir>/m.c with NOPROF on every function but PROF's
(mode_client and the clientEraseBlock it inlines), compiles it once with
-fprofile-arcs -ftest-coverage for the .gcno and the profile_estimate dump,
writes <dir>/-.gcda (counts for PROF's functions; the overrides use the
dump's bb numbers) and runs fncmp on the profile build.  Env: EXTRA (more
gcc flags), THR (gcda.py --threshold), PROF.
Prints the fncmp line count; the diff is in <dir>/fdo.diff.
As a module: prep(dir, draft) and score(dir, overrides, slot) for searches.
"""
import os, re, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BIN = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin')
FL = ['-O3', '-fno-toplevel-reorder', '-fno-ipa-profile', '-fno-reorder-functions',
      '-fno-asynchronous-unwind-tables'] + os.environ.get('EXTRA', '').split()
# functions that get counts (the rest are NOPROF); clientEraseBlock is inlined
# into mode_client, and an optimize attribute on it changes that
PROF = os.environ.get('PROF', 'mode_client,clientEraseBlock').split(',')
NOPROF = '__attribute__((optimize("no-branch-probabilities", "no-reorder-functions")))'


def noprof(src):
    """NOPROF before every function definition not in PROF"""
    out = []
    lines = src.split('\n')
    for k, l in enumerate(lines):
        if (k + 1 < len(lines) and lines[k + 1] == '{' and re.match(r'^[a-z][\w \*]*\b\w+\(', l)
                and not any(re.search(r'\b%s\(' % f, l) for f in PROF)):
            out.append(NOPROF)
        out.append(l)
    return '\n'.join(out)


def prep(d, draft):
    os.makedirs(d, exist_ok=True)
    for h in os.listdir(os.path.dirname(os.path.abspath(draft))):
        if h.endswith('.h'):
            shutil.copy(os.path.join(os.path.dirname(os.path.abspath(draft)), h), d)
    open(os.path.join(d, 'm.c'), 'w', newline='\n').write(noprof(open(draft).read()))
    env = dict(os.environ, PATH=BIN + os.pathsep + os.environ.get('PATH', ''))
    r = subprocess.run([os.path.join(BIN, 'gcc.exe'), '-S', '-I', os.path.join(ROOT, 'tools', 'wip', 'app')] + FL +
                       ['-fprofile-arcs', '-ftest-coverage', '-fdump-tree-profile_estimate-blocks-details',
                        os.path.join(d, 'm.c'), '-o', '-'], cwd=d, env=env, capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr)


def score(d, overrides, slot=None, fn='mode_client', keep=False):
    s = os.path.join(d, 'slot%s' % slot) if slot is not None else d
    os.makedirs(s, exist_ok=True)
    r = subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 're', 'gcda.py'), os.path.join(d, '-.gcno'),
                        os.path.join(d, 'm.c.042t.profile_estimate'), os.path.join(s, '-.gcda')] +
                       list(overrides) + ['--only=' + ','.join(PROF), '--threshold=' + os.environ.get('THR', '64')], capture_output=True, text=True, cwd=ROOT)
    if r.returncode:
        return 99999, r.stderr
    r = subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 're', 'fncmp.py'), os.path.join(d, 'm.c'), fn] + FL +
                       ['-fbranch-probabilities', '-fprofile-dir=' + s],
                       capture_output=True, text=True, cwd=ROOT, env=dict(os.environ, FNCMP_LITERALS='1'))
    o = r.stdout + r.stderr
    n = 0 if 'MATCH' in o else len([l for l in o.splitlines() if re.match(r'^[-+](?![-+])', l)]) or 9999
    return n, o


if __name__ == '__main__':
    d, draft = sys.argv[1:3]
    prep(d, draft)
    n, o = score(d, sys.argv[3:])
    open(os.path.join(d, 'fdo.diff'), 'w').write(o)
    print(n)
