#!/usr/bin/env python3
"""Print one function of tmp/xeBuild64 (Linux v1.16) with string immediates resolved.

python tools/wip/dehint/op6dis.py 0x40d9c0 [names]

names: comma list addr=name for callees (defaults below, guessed for options).
Uses tmp/strs/x64.dis and tmp/strs/fdes.txt like iw13x64.py.
"""
import bisect
import re
import struct
import sys

ELF = 'tmp/xeBuild64'
DIS = 'tmp/strs/x64.dis'
FDE = 'tmp/strs/fdes.txt'

NAMES = {
    0x401370: 'log_printf', 0x40b700: 'perboxExists', 0x40c9b0: 'optIniBool',
    0x40cac0: 'parseButton', 0x40d200: 'parseOption', 0x40d9c0: 'applyIniOptions',
    0x4238d0: 'getIniValue?', 0x423cb0: 'iniU32Invalid?', 0x423bc0: 'getIniU32?',
    0x423ab0: 'iniBoolInvalid?', 0x4239a0: 'getIniBool?', 0x400340: 'strnicmp?',
    0x400380: 'stricmp?', 0x456440: 'strlen?',
}


def main():
    d = open(ELF, 'rb').read()
    phoff = struct.unpack_from('<Q', d, 32)[0]
    phsz, phn = struct.unpack_from('<HH', d, 54)
    segs = []
    for i in range(phn):
        t, fl, off, va, pa, fsz = struct.unpack_from('<IIQQQQ', d, phoff + i * phsz)
        if t == 1:
            segs.append((off, va, fsz))

    def va2s(v):
        for off, va, fsz in segs:
            if va <= v < va + fsz:
                o = off + v - va
                e = d.find(b'\0', o)
                s = d[o:e]
                if 3 <= len(s) < 200 and all(32 <= c < 127 or c in (9, 10) for c in s):
                    return s.decode().replace('\n', '\\n')
        return None

    fs = []
    for l in open(FDE):
        a, b = l.split()
        fs.append((int(a, 16), int(b, 16)))
    fs.sort()
    starts = [f[0] for f in fs]
    a = int(sys.argv[1], 16)
    if len(sys.argv) > 2:
        for kv in sys.argv[2].split(','):
            k, v = kv.split('=')
            NAMES[int(k, 16)] = v
    i = bisect.bisect_right(starts, a) - 1
    lo, hi = fs[i]
    pat = re.compile(r'^\s*([0-9a-f]+):\t(?:[0-9a-f ]+)\t(.*)$')
    for l in open(DIS, errors='replace'):
        m = pat.match(l)
        if not m:
            continue
        ad = int(m.group(1), 16)
        if not lo <= ad < hi:
            continue
        t = m.group(2).rstrip()
        t = re.sub(r'\s+<[^>]*>', '', t)
        note = []
        for mm in re.finditer(r'0x([0-9a-f]+)', t):
            v = int(mm.group(1), 16)
            if v in NAMES:
                note.append(NAMES[v])
            elif v > 0x400000:
                s = va2s(v)
                if s:
                    note.append('"%s"' % s[:70])
        print('%x: %s%s' % (ad, t, ('   ; ' + ' '.join(note)) if note else ''))


main()
