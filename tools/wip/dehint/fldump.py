"""fldump.py <file> <dump flag> <fn> [flags..]: one function's section of a gcc dump.
Example: python fldump.py ../../../src/filelist_ini.c tree-optimized getIniBool
Dump files stay under build/filelist_ini/dump/<tag>/ (tag = FLTAG env or 'd')."""
import glob, os, re, subprocess, sys
import fllib as L

src, flag, fn = sys.argv[1:4]
fl = sys.argv[4:] or L.FLAGS
d = os.path.join(L.BD, 'dump', os.environ.get('FLTAG', 'd'))
os.makedirs(d, exist_ok=True)
for f in glob.glob(os.path.join(d, '*')):
    os.remove(f)
inp = ('#line 1 "filelist_ini.c"\n' + open(src, newline='').read()).encode()
p = subprocess.run([L.GCC, '-c'] + fl + ['-fdump-' + flag, '-I' + os.path.join(L.R, 'src'), '-x', 'c', '-', '-o', 'x.o'],
                   input=inp, cwd=d, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
fs = [f for f in glob.glob(os.path.join(d, '*')) if not f.endswith('.o')]
for f in fs:
    t = open(f, errors='replace').read()
    parts = re.split(r'(?m)^(?=;; Function )', t)
    for q in parts:
        if q.startswith(';; Function %s ' % fn):
            sys.stdout.write(q)
