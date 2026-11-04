"""python tools/wip/dehint/iw10a.py [probe ...]: attempt 10, pin_hdr's (A).  Mechanism probes, not candidates: which block's frequency
flips r187/r192?  Each probe edits src minus the pin with an expect placed somewhere other than the ECC test (--param value in the table),
then prints finalizeImage's line count, the pseudos' registers (reference: r187 di=5, r192 si=4) and the block freqs that matter."""
import glob, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib

PIN = '			__asm__("" :: "a"(xb.hdr));\n'
D0 = '		if (data[i] != 0xff)\n			return 0;\n	for (i = 0; i < 16; i++)\n		if (spare[i] != 0xff)\n			return 0;\n	return 1;\n}\n\nint blockErased'
def d(a, b):
    return D0.replace('if (data[i] != 0xff)', 'if (' + a + ')').replace('if (spare[i] != 0xff)', 'if (' + b + ')')
DE, SE = 'data[i] != 0xff', 'spare[i] != 0xff'
P = {
 'none': ([], None),
 'd60': ([(D0, d('__builtin_expect(%s, 1)' % DE, SE))], 60),
 'd70': ([(D0, d('__builtin_expect(%s, 1)' % DE, SE))], 70),
 'd80': ([(D0, d('__builtin_expect(%s, 1)' % DE, SE))], 80),
 'd90': ([(D0, d('__builtin_expect(%s, 1)' % DE, SE))], 90),
 'd95': ([(D0, d('__builtin_expect(%s, 1)' % DE, SE))], 95),
 'd99': ([(D0, d('__builtin_expect(%s, 1)' % DE, SE))], 99),
 's60': ([(D0, d(DE, '__builtin_expect(%s, 1)' % SE))], 60),
 's80': ([(D0, d(DE, '__builtin_expect(%s, 1)' % SE))], 80),
 's90': ([(D0, d(DE, '__builtin_expect(%s, 1)' % SE))], 90),
 's99': ([(D0, d(DE, '__builtin_expect(%s, 1)' % SE))], 99),
}


def run(name, edits, par):
    t = open(os.path.join(iwlib.R, 'src', 'image_write.c'), newline='').read().replace('\r\n', '\n').replace(PIN, '')
    for a, b in edits:
        assert a in t, a
        t = t.replace(a, b)
    wd = os.path.join(iwlib.BUILD, 'a10', 'p_' + name)
    os.makedirs(wd, exist_ok=True)
    for f in glob.glob(os.path.join(wd, 'a.c*')):
        os.remove(f)
    open(os.path.join(wd, 'a.c'), 'w', newline='\n').write(t)
    fl = ['--param', 'builtin-expect-probability=%d' % par] if par else []
    subprocess.run([iwlib.GCC, '-c', '-O3'] + fl + ['-I' + os.path.join(iwlib.R, 'src'), '-fdump-rtl-ira-all', 'a.c', '-o', 'a.o'], cwd=wd, check=True)
    idn, tot, per, notes = iwlib.report(os.path.join(wd, 'a.o'))
    b = open(glob.glob(os.path.join(wd, 'a.c.*ira'))[0], errors='replace').read()
    b = re.search(r'^;; Function finalizeImage \(.*?(?=^;; Function |\Z)', b, re.S | re.M).group(0)
    pops = re.findall(r'Popping a\d+\(r(\d+),l5\)  -- assign reg (\d+)', b)
    cp = re.findall(r'cp\d+:a\d+\(r(\d+)\)<->a\d+\(r(\d+)\)@(\d+):move', b)
    frs = [int(x[1]) for x in re.findall(r'^;; basic block (\d+), loop depth 2, count 0, freq (\d+)', b, re.M)]
    print(name, 'fi', per.get('_finalizeImage', 0), 'head?', max(frs) if frs else None, 'pops', pops[:6], 'movecp', cp[:6], flush=True)


def runfile(path):
    """the same report for a source file, plain -O3, plus every depth 2 block's freq"""
    t = open(path, newline='').read().replace('\r\n', '\n')
    wd = os.path.join(iwlib.BUILD, 'a10', 'p_file')
    os.makedirs(wd, exist_ok=True)
    for f in glob.glob(os.path.join(wd, 'a.c*')):
        os.remove(f)
    open(os.path.join(wd, 'a.c'), 'w', newline='\n').write(t)
    subprocess.run([iwlib.GCC, '-c', '-O3', '-I' + os.path.join(iwlib.R, 'src'), '-fdump-rtl-ira-all', 'a.c', '-o', 'a.o'], cwd=wd, check=True)
    idn, tot, per, notes = iwlib.report(os.path.join(wd, 'a.o'))
    b = open(glob.glob(os.path.join(wd, 'a.c.*ira'))[0], errors='replace').read()
    b = re.search(r'^;; Function finalizeImage \(.*?(?=^;; Function |\Z)', b, re.S | re.M).group(0)
    pops = re.findall(r'Popping a\d+\(r(\d+),l5\)  -- assign reg (\d+)', b)
    cp = re.findall(r'cp\d+:a\d+\(r(\d+)\)<->a\d+\(r(\d+)\)@(\d+):move', b)
    fr = re.findall(r'^;; basic block (\d+), loop depth (\d+), count 0, freq (\d+)', b, re.M)
    print(os.path.basename(path), 'identical' if idn else (tot, per), 'pops', pops[:6], 'movecp', [c for c in cp if int(c[2]) > 20][:3])
    print(' freqs', ' '.join('%s:%s' % (x[0], x[2]) for x in fr if int(x[1]) >= 2)[:500])


if __name__ == '__main__':
    for n in (sys.argv[1:] or P):
        if n in P:
            run(n, *P[n])
        else:
            runfile(n)
