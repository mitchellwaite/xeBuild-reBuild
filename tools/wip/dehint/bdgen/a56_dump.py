"""Attempt 56: compile a variant with every tree dump (blocks, details) plus expand, jump2 and bbro
into <outdir>.  python tools/wip/dehint/bdgen/a56_dump.py <variant.c> <outdir> [gcc dump flags]"""
import os, sys, subprocess
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\dehint')
import bdlib
src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
t = '#line 1 "build.c"\n' + open(src, newline='').read()
open(os.path.join(out, 'build.c'), 'w', newline='\n').write(t)
fl = sys.argv[3:] or ['-fdump-tree-all-blocks-details', '-fdump-rtl-expand-details', '-fdump-rtl-jump2-details', '-fdump-rtl-bbro-details']
r = subprocess.run([bdlib.GCC, '-c', '-O3', '--param', 'builtin-expect-probability=99'] + fl + ['-I' + os.path.join(bdlib.R, 'src'), 'build.c', '-o', 'o.o'], cwd=out, capture_output=True)
print(r.returncode, r.stderr.decode()[:500])
