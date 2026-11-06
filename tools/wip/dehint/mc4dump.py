"""mode_client attempt 4: compile a source with gcc dumps into build/mc4/<tag>/.

python tools/wip/dehint/mc4dump.py FILE.c TAG [dump flags ...]
default dumps: -fdump-tree-profile_estimate-details -fdump-rtl-bbro-details"""
import os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib, mc1lib

a = sys.argv[1:]
src, tag = a[0], a[1]
flags = a[2:] or ['-fdump-tree-profile_estimate-details', '-fdump-rtl-bbro-details']
d = os.path.join(bdlib.R, 'build', 'mc4', tag)
os.makedirs(d, exist_ok=True)
text = '#line 1 "mode_client.c"\n' + mc1lib.read_src(src)
open(os.path.join(d, 'mode_client.c'), 'w', newline='\n').write(text)
r = subprocess.run([bdlib.GCC, '-c', '-O3'] + mc1lib.P50 + flags +
                   ['-I' + os.path.join(bdlib.R, 'src'), 'mode_client.c', '-o', 'o.o'],
                   cwd=d, capture_output=True, text=True)
print(r.returncode, r.stderr[-800:])
print(d)
