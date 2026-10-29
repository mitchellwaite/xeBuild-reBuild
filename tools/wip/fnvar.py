"""Try body variants of one function in a draft and fncmp each.

python tools/wip/fnvar.py <draft.c> <fn> <forms file> [attr ...]

The forms file holds whole function bodies (from `{` to `}`) separated by
lines `=====`; write it with an editor or the Write tool (heredocs mangle
`\\n`).  Each form replaces <fn>'s attribute line and body, once per
attribute set (`-` = none, else the text inside `__attribute__((...))`),
and tools/re/fncmp.py's diff line count is printed.  Environment:
  FLAGS   gcc flags (default -O3)
  SHOW=i,j  print the diff for form i with attribute set j
  KEEP=1  keep fnvar_t.c (the last form) for dumps
  CMPFN, GCCSYM  compare against the original's CMPFN using gcc's GCCSYM
                 (a clone: CMPFN=netRecv GCCSYM=_netRecvVerbose.constprop.2)
"""
import os, re, subprocess, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
draft, fn, formfile = sys.argv[1:4]
attrs = sys.argv[4:] or ['-']
src = open(draft).read()
m = re.search(r'\n((?:__attribute__[^\n]*\n)?)([^\n;{}#]*\b%s\([^;{]*\))\n\{.*?\n\}\n' % fn, src, re.S)
forms = [f.strip('\n') for f in open(formfile).read().split('\n=====\n')]
flags = os.environ.get('FLAGS', '-O3').split()
out = os.path.join(os.path.dirname(os.path.abspath(draft)), 'fnvar_t.c')
env = dict(os.environ, FNCMP_LITERALS='1')
if os.environ.get('GCCSYM'):
    env['FNCMP_GCCSYM'] = os.environ['GCCSYM']
for i, form in enumerate(forms, 1):
    for j, a in enumerate(attrs, 1):
        attr = '' if a == '-' else '__attribute__((%s))\n' % a
        open(out, 'w', newline='\n').write(src[:m.start()] + '\n' + attr + m.group(2) + '\n' + form + '\n' + src[m.end():])
        r = subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 're', 'fncmp.py'), out,
                            os.environ.get('CMPFN', fn)] + flags, capture_output=True, text=True, cwd=ROOT, env=env)
        o = r.stdout + r.stderr
        n = 'MATCH' if 'MATCH' in o else len([l for l in o.splitlines() if re.match(r'^[-+](?![-+])', l)]) or o.strip()[:80]
        print('form %d attr %d (%s): %s' % (i, j, a, n), flush=True)
        if os.environ.get('SHOW') == '%d,%d' % (i, j):
            print(o)
if not os.environ.get('KEEP'):  # KEEP=1 leaves the last form in fnvar_t.c
    os.remove(out)
