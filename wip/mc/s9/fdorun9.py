"""Profile build of the mode_client draft with a frequency design, scored.

python fdorun.py <slot> <design.json | k=v ...> [--over 'fn:s>d=p' ...]
The design maps RTL bb numbers (of the draft's d1 build) to wanted frequencies
for the switch cases, HDD errors, the -ip.. chain and the erase/dummy blocks;
it is turned into gcda.py overrides (tree bb numbers of f1's instrumented
dump).  Extra raw overrides can be appended.  Prints fncmp lines, the
round-4 order (signatures) and the realized frequencies of the design's blocks.
"""
import json, os, re, subprocess, sys
S = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
BIN = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin')
sys.path.insert(0, os.path.join(ROOT, 'wip'))
sys.path.insert(0, S)
os.environ.setdefault('EXTRA', '--param builtin-expect-probability=50')
import mcfdo, mcvar

F1 = os.environ.get('MCFDO_DIR') or os.path.join(ROOT, 'build', 'mcfdo')   # the dir mcfdo.py prepared; compile from the same path string
# RTL bb (d1 numbering) -> (tree src, tree dst) edge of the instrumented dump whose
# target block's frequency it is; the probability is freq / src_freq
CASES = {129: 128, 107: 112, 108: 113, 109: 114, 110: 115, 113: 118, 116: 121, 119: 124, 120: 125, 121: 126, 128: 127, 132: 131}
POST = float(os.environ.get('MC_POST', '200'))   # post-loop flow (tree bb 105); set with loop-exit override


def overrides(design):
    ov = []
    d = {int(k): v for k, v in design.items()}
    cases = {rtl: d[rtl] for rtl in CASES if rtl in d}
    if cases:
        disp = sum(cases.values())
        p = 100.0 * disp / POST / 0.999
        ov.append('mode_client:105>110=%.4f' % p)
        for rtl, f in cases.items():
            ov.append('mode_client:111>%d=%.4f' % (CASES[rtl], 100.0 * f / disp))
        ov.append('mode_client:111>132=0')
        if 112 in d:
            ov.append('mode_client:115>117=%.4f' % min(50.0, 100.0 * d[112] / d[110]))
        if 115 in d:
            ov.append('mode_client:118>120=%.4f' % min(50.0, 100.0 * d[115] / d[113]))
        if 117 in d:
            ov.append('mode_client:121>122=%.4f' % (100.0 * d[117] / d[116]))
        if 130 in d:
            ov.append('mode_client:128>129=%.4f' % (100.0 * d[130] / d[129]))
    # chain: 49 (-ip test, tree 50) <- 49->50; 55 (-r, 56) <- 50->56; 61 (-w, 64) <- 56->64; 67 (-e, 72) <- 64->72; 73 (-c, 80) <- 72->80
    chain = [(49, 49, 50, 26.0), (55, 50, 56, None), (61, 56, 64, None), (67, 64, 72, None), (73, 72, 80, None), (81, 80, 88, None)]
    prev = None
    for rtl, s, t, srcf in chain:
        if rtl not in d:
            prev = d.get(rtl, prev)
            break
        src = srcf if srcf is not None else prev
        if src:
            ov.append('mode_client:%d>%d=%.4f' % (s, t, min(100.0, 100.0 * d[rtl] / src)))
        prev = d[rtl]
    # erase block (clientEraseBlock's own profile, scaled to the case-10 call site): 127 invalid <- 2->8, 126 outside <- 3->7, 125 failed <- 4->6
    if 121 in d and 126 in d:
        f121 = float(d[121])
        p_inv = 100.0 * d.get(127, 0) / f121 if f121 else 0
        f122 = f121 * (1 - p_inv / 100)
        p_out = 100.0 * d[126] / f122 if f122 else 0
        f123 = f122 * (1 - p_out / 100)
        p_fail = 100.0 * d.get(125, 0) / f123 if f123 else 0
        ov += ['clientEraseBlock:2>8=%.4f' % p_inv, 'clientEraseBlock:3>7=%.4f' % min(p_out, 50), 'clientEraseBlock:4>6=%.4f' % min(p_fail, 50)]
    return ov


def main():
    slot = sys.argv[1]
    args = sys.argv[2:]
    extra = []
    if '--over' in args:
        i = args.index('--over')
        extra = args[i + 1:]
        args = args[:i]
    if args and args[0].endswith('.json'):
        design = json.load(open(args[0]))
    else:
        design = {a.split('=')[0]: float(a.split('=')[1]) for a in args}
    ov = overrides(design) + extra
    print('overrides:', ' '.join(ov))
    n, o = mcfdo.score(F1, ov, slot=slot)
    sd = os.path.join(F1, 'slot%s' % slot)
    open(os.path.join(sd, 'fdo.diff'), 'w').write(o)
    print('fncmp', n)
    # dump compile
    env = dict(os.environ, PATH=BIN + os.pathsep + os.environ.get('PATH', ''))
    r = subprocess.run([os.path.join(BIN, 'gcc.exe'), '-S', '-masm=intel', '-fno-asynchronous-unwind-tables'] + mcfdo.FL +
                       ['-fbranch-probabilities', '-fprofile-dir=' + sd, '-fdump-rtl-bbro-details', '-fdump-rtl-compgotos-blocks',
                        os.path.join(F1, 'm.c'), '-o', '-'], cwd=sd, env=env, capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr)
    open(os.path.join(sd, 'fdo.s'), 'w').write(r.stdout)
    for dump in ('m.c.274r.bbro', 'm.c.267r.compgotos'):
        pass   # dumps land in the slot dir (cwd)
    bbro = mcvar.section(open(os.path.join(sd, 'm.c.274r.bbro')).read(), 'mode_client')
    cg = mcvar.section(open(os.path.join(sd, 'm.c.267r.compgotos')).read(), 'mode_client')
    sg = mcvar.sigs(cg, r.stdout)
    order = mcvar.order(bbro)
    o2 = [sg.get(b) for b in order]
    o2 = [s for s in o2 if s in mcvar.WANT]
    inv, pre = mcvar.score(o2)
    print('round4 inv=%d pre=%d' % (inv, pre))
    print('order (bb):', ' '.join(map(str, order)))
    freq = {}
    for m in re.finditer(r'(\d+) \[(\d+)\]', bbro[bbro.index('Trace 1 ('):]):
        freq[int(m.group(1))] = int(m.group(2))
    print('realized:', ' '.join('%s:%d/%s' % (b, freq.get(int(b), -1), design[b]) for b in design))


if __name__ == '__main__':
    main()
