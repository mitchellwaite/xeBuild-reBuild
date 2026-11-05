"""python tools/wip/dehint/ir64.py <hexaddr> <size> : the older Linux xeBuild64's function from
tmp/x64.dis (read-only, structure cross-check, gcc 4.9), immediates that point into .rodata
replaced by their strings.  Addresses from tmp/strs/match.txt ("L addr size -> W addr")."""
import os, re, struct, sys

R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
elf = open(os.path.join(R, 'tmp', 'xeBuild64'), 'rb').read()
shoff = struct.unpack_from('<Q', elf, 0x28)[0]
shnum = struct.unpack_from('<H', elf, 0x3c)[0]
secs = []
for i in range(shnum):
    s = struct.unpack_from('<IIQQQQ', elf, shoff + i * 64)
    secs.append((s[3], s[4], s[5]))


def string(a):
    for addr, off, size in secs:
        if addr and addr <= a < addr + size:
            o = off + a - addr
            e = elf.find(b'\0', o, o + 200)
            if e > o:
                b = elf[o:e]
                if all(32 <= c < 127 or c in (9, 10) for c in b) and len(b) >= 4:
                    return b.decode().replace('\n', '\\n')
    return None


start = int(sys.argv[1], 16)
end = start + int(sys.argv[2])
for l in open(os.path.join(R, 'tmp', 'x64.dis'), errors='replace'):
    m = re.match(r'^\s*([0-9a-f]+):\t(?:[0-9a-f ]+\t)?(.*)$', l.rstrip('\n'))
    if not m:
        continue
    a = int(m.group(1), 16)
    if start <= a < end:
        t = m.group(2)
        for x in re.findall(r'0x([0-9a-f]{5,8})', t):
            s = string(int(x, 16))
            if s:
                t += '   ; "' + s[:60] + '"'
        print('%x: %s' % (a, t))
