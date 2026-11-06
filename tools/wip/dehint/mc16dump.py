"""mode_client attempt 16: bbro-details dump of mode_client only (the mode_client function
part) for A.c, written to OUT.

python tools/wip/dehint/mc16dump.py A.c OUT"""
import os, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib, mc1lib, mc12keys

t = mc1lib.read_src(sys.argv[1])
d = tempfile.mkdtemp(dir=mc1lib.BUILD, prefix='k')
open(os.path.join(d, 'mode_client.c'), 'w', newline='\n').write('#line 1 "mode_client.c"\n' + t)
subprocess.run([bdlib.GCC, '-c', '-O3', '-fdump-rtl-bbro-details', '-I' + os.path.join(bdlib.R, 'src'),
                'mode_client.c', '-o', 'o.o'], cwd=d, capture_output=True)
f = [x for x in os.listdir(d) if x.endswith('bbro')][0]
open(sys.argv[2], 'w', newline='\n').write(mc12keys.fn_part(open(os.path.join(d, f)).read()))
mc1lib.cleanup(d)
