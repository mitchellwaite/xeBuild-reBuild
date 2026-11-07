#!/usr/bin/env python3
"""Disassemble one function of an options object with .rdata immediates shown as strings.

python tools/wip/dehint/op18dis.py OBJ FUNC [FROM-TO]
"""
import os
import re
import subprocess
import sys

R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
TC = os.path.join(R, 'tools', 'toolchain-4745', 'mingw32', 'bin')
OBJDUMP = os.path.join(TC, 'objdump.exe')


def rdata(o):
    t = subprocess.run([OBJDUMP, '-s', '-j', '.rdata', o], capture_output=True, text=True).stdout
    b = bytearray()
    for l in t.split('\n'):
        m = re.match(r' ([0-9a-f]{4,}) ((?:[0-9a-f]{2,8} ?){1,4})', l)
        if m:
            off = int(m.group(1), 16)
            hx = m.group(2).replace(' ', '')
            if len(b) < off:
                b.extend(b'\0' * (off - len(b)))
            b[off:off + len(hx) // 2] = bytes.fromhex(hx)
    return bytes(b)


def s_at(rd, off):
    e = rd.find(b'\0', off)
    return rd[off:e].decode('latin1')[:50]


def main():
    o, fn = sys.argv[1], sys.argv[2]
    rd = rdata(o)
    t = subprocess.run([OBJDUMP, '-d', '-r', '-M', 'intel', '--no-show-raw-insn', o],
                       capture_output=True, text=True).stdout.split('\n')
    on = False
    prev = None
    out = []
    for l in t:
        m = re.match(r'[0-9a-f]+ <(.*)>:', l)
        if m:
            on = m.group(1) == fn
            continue
        if not on:
            continue
        if 'dir32\t.rdata' in l and prev is not None:
            mm = re.search(r',0x([0-9a-f]+)$', out[prev]) or re.search(r'\[0x([0-9a-f]+)\]', out[prev]) or re.search(r'0x([0-9a-f]+)', out[prev])
            if mm:
                out[prev] += '   ; "%s"' % s_at(rd, int(mm.group(1), 16)).replace('\n', '\\n')
            continue
        if re.search(r'DISP32|dir32', l):
            out[-1] += '   ; ' + l.split()[-1]
            continue
        out.append(l)
        prev = len(out) - 1
    if len(sys.argv) > 3:
        a, b = [int(x, 16) for x in sys.argv[3].split('-')]
        out = [l for l in out if re.match(r'\s*([0-9a-f]+):', l) and a <= int(re.match(r'\s*([0-9a-f]+):', l).group(1), 16) <= b]
    print('\n'.join(out))


main()
