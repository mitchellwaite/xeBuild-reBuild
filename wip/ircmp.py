"""fncmp + jcmp of one function of an image_read draft, strings as the .s's names.

python wip/ircmp.py <draft.c> <name> [gcc flags]   (default -O3)

The draft (wip/app/image_read.c or a copy of it) goes through irlit's
externize() into a temporary file, so two blocks that differ only in their
string still differ.  Prints fncmp's result (MATCH or a diff), then jcmp's
(JMATCH or a diff).  Safe to run in parallel (per-process file names).
"""
import os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from irlit import externize

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src, name = sys.argv[1:3]
flags = sys.argv[3:]
tmp = os.path.join(ROOT, 'build', 'ircmp.%d.c' % os.getpid())
open(tmp, 'w', newline='\n').write(externize(open(src).read()))
try:
    for tool in ('re/fncmp.py', 'wip/jcmp.py'):
        r = subprocess.run([sys.executable, os.path.join(ROOT, tool), tmp, name] + flags,
                           capture_output=True, text=True)
        print('== %s' % tool)
        print((r.stdout + r.stderr).rstrip())
finally:
    os.remove(tmp)
