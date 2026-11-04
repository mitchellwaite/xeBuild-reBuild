#!/usr/bin/env python3
"""Find image_write's functions in tmp/xeBuild64 (Linux v1.16, stripped).

python tools/wip/dehint/iw13x64.py            list: function extents around
                                              image_write's strings, with their
                                              strings and callees
python tools/wip/dehint/iw13x64.py 0x41abcd   print that function's disassembly

Uses tmp/strs/x64.dis (objdump -d -M intel) and tmp/strs/fdes.txt (.eh_frame
extents), both from an earlier scratch run.
"""
import bisect
import re
import struct
import sys

ELF = 'tmp/xeBuild64'
DIS = 'tmp/strs/x64.dis'
FDE = 'tmp/strs/fdes.txt'

STRS = [
    'adding as %s at raw offset', 'adding %s will exceed', 'adding Mobile%c.dat will exceed',
    'adding Mobile%c.dat as type', 'adding smc config to offset', 'Inserting netKd',
    'offset 0x%x len 0x4000', 'fixing up big block LBA', 'fixing up big block controller',
    'calculating ECD', 'dest block is empty', 'remapping %d blocks', 'flash header build',
    'reset smc load', 'patch slot offset', 'copying anchor block', 'writing image to disk',
    'adding %s at raw offset', 'final truncated', 'cfldv was not set', 'SMC size 0x%x',
]


def load_elf():
    d = open(ELF, 'rb').read()
    phoff = struct.unpack_from('<Q', d, 32)[0]
    phsz, phn = struct.unpack_from('<HH', d, 54)
    segs = []
    for i in range(phn):
        t, fl, off, va, pa, fsz = struct.unpack_from('<IIQQQQ', d, phoff + i * phsz)
        if t == 1:
            segs.append((off, va, fsz))
    return d, segs


def off2va(segs, o):
    for off, va, fsz in segs:
        if off <= o < off + fsz:
            return va + o - off
    return None


def strings_at():
    d, segs = load_elf()
    res = {}
    for s in STRS:
        o = d.find(s.encode())
        while o >= 0:
            # walk back to the string's start
            st = o
            while d[st - 1] != 0:
                st -= 1
            res[off2va(segs, st)] = s
            o = d.find(s.encode(), o + 1)
    return res


def fdes():
    out = []
    for l in open(FDE):
        a, b = l.split()
        out.append((int(a, 16), int(b, 16)))
    out.sort()
    return out


def dis_lines():
    out = []
    pat = re.compile(r'^\s*([0-9a-f]+):\t(?:[0-9a-f ]+)\t(.*)$')
    for l in open(DIS, errors='replace'):
        m = pat.match(l)
        if m:
            out.append((int(m.group(1), 16), m.group(2).rstrip()))
    return out


def main():
    fs = fdes()
    starts = [f[0] for f in fs]
    if len(sys.argv) > 1:
        a = int(sys.argv[1], 16)
        i = bisect.bisect_right(starts, a) - 1
        lo, hi = fs[i]
        for ad, t in dis_lines():
            if lo <= ad < hi:
                print('%x: %s' % (ad, t))
        return
    sa = strings_at()
    lines = dis_lines()
    refs = {}
    calls = {}
    for ad, t in lines:
        for m in re.finditer(r'0x([0-9a-f]+)', t):
            v = int(m.group(1), 16)
            if v in sa:
                i = bisect.bisect_right(starts, ad) - 1
                refs.setdefault(fs[i][0], set()).add(sa[v])
        if t.startswith('call'):
            m = re.search(r'0x([0-9a-f]+)', t)
            if m:
                i = bisect.bisect_right(starts, ad) - 1
                calls.setdefault(fs[i][0], []).append(int(m.group(1), 16))
    for a in sorted(refs):
        i = bisect.bisect_left(starts, a)
        print('%x-%x %d: %s' % (a, fs[i][1], fs[i][1] - a, sorted(refs[a])))
    if refs:
        lo = min(refs) - 0x3000
        hi = max(refs) + 0x3000
        print('--- all functions in range, with callees')
        for a, b in fs:
            if lo <= a <= hi:
                print('%x-%x %5d %s' % (a, b, b - a, ' '.join('%x' % c for c in calls.get(a, []))))


main()
