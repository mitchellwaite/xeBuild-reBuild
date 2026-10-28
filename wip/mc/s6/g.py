"""6th session: python g.py NAME 'old'=>'new' ... ; writes v6_NAME.c from draft, prints mcvar+fncmp"""
import sys, subprocess, os
os.chdir(r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix')
src = open('wip/app/mode_client.c').read()
name = sys.argv[1]
for rep in sys.argv[2:]:
    o, n = rep.split('=>')
    o = o.encode().decode('unicode_escape'); n = n.encode().decode('unicode_escape')
    assert o in src, o
    src = src.replace(o, n, 1)
out = 'wip/mc/s6/v_%s.c' % name
os.makedirs('wip/mc/s6', exist_ok=True)
open(out, 'w', newline='\n').write(src)
r = subprocess.run([sys.executable, 'wip/mc/mcvar.py', out, '-O3', '--param', 'builtin-expect-probability=50'], env=dict(os.environ, FNCMP='1'), capture_output=True, text=True)
print(name, (r.stdout + r.stderr).strip()[:600])
