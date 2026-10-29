"""Relink src/xeBuild.s with everything moved and check every pointer followed.

python tools/re/shifttest.py <xeBuild.exe> <build/xeBuild.s> <build_dir>

Inserts 16 bytes before every function (ahead of its `.align 16`) and before
every data label in .data/.rdata/.bss, links build_dir/shift.exe with symbols,
and maps each original address to its new one through the nearest preceding
label (padding only goes before labels, so offsets past a label are kept).
Then, for every 4-byte window of the original image:
  absolute  value v in the image          -> new value must be M(v)
  rva       .idata/.rsrc, base+v in image -> new value must be M(base+v)-base
  pcrel     .eh_frame FDE pc_begin        -> p+v maps: M(p)+new == M(p+v)
"ok" = translated, "missed" = still the old value, "wrong" = moved elsewhere.
Windows not starting at a symbol/field are coincidences and are reported
separately only when they changed.
"""
import bisect, collections, os, re, struct, subprocess, sys

sys.path.insert(0, os.path.dirname(__file__))
from ddfix import Image

TC = os.path.join(os.path.dirname(__file__), '..', '..', 'tools', 'toolchain-4745', 'mingw32', 'bin')
LABEL = re.compile(r'^((?:FUN|\.L)_([0-9a-f]+)(?:_END)?):\s*$')
PAD_SECTIONS = ('.text', '.data', '.bss', '.section .rdata,"dr"')


def pad_source(src, dst):
    lines = open(src, encoding='utf-8').read().split('\n')
    out, sec = [], None
    for i, l in enumerate(lines):
        s = l.strip()
        if s.startswith('.section') or s in ('.text', '.data', '.bss'):
            sec = s
        if sec in PAD_SECTIONS:
            nxt = lines[i + 1].strip() if i + 1 < len(lines) else ''
            if sec == '.text' and s == '.align 16' and nxt.startswith('FUN_'):
                out.append('.skip 16')
            elif sec != '.text' and LABEL.match(s):
                out.append('.skip 16')
        out.append(l)
    open(dst, 'w', encoding='utf-8', newline='\n').write('\n'.join(out))


def run(*args):
    r = subprocess.run([os.path.abspath(args[0])] + list(args[1:]), capture_output=True, text=True)
    if r.returncode:
        sys.exit('%s failed:\n%s' % (args[0], r.stderr[:3000]))
    return r.stdout


def main():
    exe, src, bd = sys.argv[1:4]
    s, o, x = (os.path.join(bd, 'shift' + e) for e in ('.s', '.o', '.exe'))
    pad_source(src, s)
    run(os.path.join(TC, 'as.exe'), '--32', '-L', s, '-o', o)
    ld = os.path.join(os.path.dirname(__file__), 'single.ld')
    run(os.path.join(TC, 'ld.exe'), '-m', 'i386pe', '-T', ld, '--image-base', '0x400000',
        '-e', '__EntryPoint', '--subsystem', 'console', '-o', x, o)

    a, b = Image(exe), Image(x)
    anchors = {}  # original VA -> new VA
    for line in run(os.path.join(TC, 'nm.exe'), x).splitlines():
        p = line.split()
        if len(p) == 3:
            m = LABEL.match(p[2] + ':')
            if m:
                anchors[int(m.group(2), 16)] = int(p[0], 16)
    for (n, va, *_), (_, vb, *_) in zip(a.secs, b.secs):
        anchors.setdefault(va, vb)
    keys = sorted(anchors)
    secs = [(n, va, va + max(vsz, rsz)) for n, va, vsz, _, rsz in a.secs]
    sec_of = lambda v: next((n for n, lo, hi in secs if lo <= v < hi), None)

    def M(v):
        k = keys[bisect.bisect_right(keys, v) - 1]
        if sec_of(k) != sec_of(v):
            return None
        return anchors[k] + v - k

    res = collections.Counter()
    bad = collections.defaultdict(list)
    word = lambda img, v: struct.unpack('<I', img.read(v, 4))[0]
    _, eh, ehsz, _, _ = a.sec('.eh_fram')
    pcrel = set()
    off = 0
    while off < ehsz:  # FDE pc_begin fields
        ln, cid = struct.unpack('<II', a.read(eh + off, 8))
        if ln and cid:
            pcrel.add(eh + off + 8)
        off += 4 + ln if ln else 4

    # instruction extents in the original .text, to drop windows that straddle two
    # and to keep only windows whose value objdump shows as an operand
    insn, dis = {}, {}
    for l in run(os.path.join(TC, 'objdump.exe'), '-d', '--insn-width=16', '-j', '.text', exe).splitlines():
        m = re.match(r'\s+([0-9a-f]+):\t((?:[0-9a-f]{2} )+)\s*(.*)', l)
        if m:
            s0 = int(m.group(1), 16)
            dis[s0] = m.group(3)
            for k in range(len(m.group(2).split())):
                insn[s0 + k] = s0
    ok_bytes = set()
    found = []

    for name, lo, hi in secs:
        if name == '.bss':
            continue
        for p in range(lo, hi - 3):
            if name == '.text' and insn.get(p) != insn.get(p + 3):
                continue
            v, mp = word(a, p), M(p)
            if mp is None:
                continue
            if p in pcrel:
                kind, tgt, conv = 'pcrel', (p + v) & 0xffffffff, lambda t: (t - mp) & 0xffffffff
            elif name in ('.idata', '.rsrc') and a.base + 0x1000 <= a.base + v < a.base + 0x113000:
                kind, tgt, conv = 'rva', a.base + v, lambda t: t - b.base
            elif 0x401000 <= v < 0x513000:
                kind, tgt, conv = 'absolute', v, lambda t: t
            else:
                continue
            mt = M(tgt)
            if mt is None or mt == tgt and kind != 'pcrel':
                continue  # target didn't move: can't tell
            nv = word(b, mp)
            if nv == conv(mt):
                res[kind, 'ok'] += 1
                ok_bytes.update(range(p, p + 4))
            else:
                found.append((name, p, kind, v, nv, tgt, conv(mt)))
    for name, p, kind, v, nv, tgt, want in found:
        if ok_bytes.intersection(range(p, p + 4)):
            continue  # misaligned window over a pointer that did move correctly
        if name == '.text' and '0x%x' % v not in dis.get(insn.get(p), ''):
            continue  # opcode/ModRM bytes that happen to look like an address
        if name != '.text' and p % 4:
            continue  # inside strings/tables; data pointers are 4-aligned
        what = 'missed' if nv == v else 'changed'
        res[kind, what] += 1
        bad[what].append('%s %x %s v=%x new=%x want=%x' % (name, p, kind, v, nv, want))
    for k in sorted(res):
        print('%-9s %-8s %d' % (k[0], k[1], res[k]))
    rep = os.path.join(bd, 'shifttest.txt')
    with open(rep, 'w', newline='\n') as f:
        for k, v in bad.items():
            f.write('==== %s (%d)\n%s\n' % (k, len(v), '\n'.join(v)))
    print('details in', rep)


if __name__ == '__main__':
    main()
