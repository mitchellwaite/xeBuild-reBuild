"""python tools/wip/dehint/iw11inl.py <file.c> ...: the inliner's numbers for calls into imgAdd's clones from writeInitialHeader (-fdump-ipa-inline-details): badness lines, `time w/o inlining`, caller time."""
import glob, os, re, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib

for path in sys.argv[1:]:
    d = tempfile.mkdtemp(dir=iwlib.BUILD, prefix='inl')
    open(os.path.join(d, 'a.c'), 'w', newline='\n').write(open(path, newline='').read().replace('\r\n', '\n'))
    subprocess.run([iwlib.GCC, '-c', '-O3', '-I' + os.path.join(iwlib.R, 'src'), '-fdump-ipa-inline-details', 'a.c', '-o', 'a.o'], cwd=d, stdin=subprocess.DEVNULL)
    t = open(glob.glob(os.path.join(d, 'a.c.*inline'))[0], errors='replace').read()
    print('==', path)
    for m in re.finditer(r'Badness calculation for writeInitialHeader/\d+ -> (\S+)\n\s+size growth (-?\d+), time (\d+)\s*(\w*)\n\s+\S+ guessed profile\. frequency ([\d.]+).*?time w/o inlining ([\d.]+), time w inlining ([\d.]+)', t):
        a, b = float(m.group(6)), float(m.group(7))
        print('  %s %s %s freq %s  %.1f -> %.1f  saved %.1f = %.2f%%' % (m.group(1), m.group(2), m.group(4), m.group(5), a, b, a - b, 100 * (a - b) / a))
    for m in re.finditer(r'Inlined into writeInitialHeader which now has time (\d+) and size (\d+)', t):
        print('  inlined: time', m.group(1), 'size', m.group(2))
    for f in os.listdir(d):
        os.remove(os.path.join(d, f))
    os.rmdir(d)
