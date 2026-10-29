"""Compare each section of a COFF object with the same section of the exe.

python tools/re/objcmp.py <xeBuild.exe> <file.o>

Bytes covered by a relocation are skipped (the linker fills them in), as is
anything past the exe section's virtual size (object sections are padded).
"""
import struct, sys, os

sys.path.insert(0, os.path.dirname(__file__))
from ddfix import Image


def main():
    img = Image(sys.argv[1])
    o = open(sys.argv[2], 'rb').read()
    _, nsec, _, _, _, optsz, _ = struct.unpack_from('<HHIIIHH', o, 0)
    worst = 0
    for i in range(nsec):
        h = 20 + optsz + 40 * i
        name = o[h:h + 8].rstrip(b'\0').decode()
        size, raw, rel = struct.unpack_from('<III', o, h + 16)
        nrel = struct.unpack_from('<H', o, h + 32)[0]
        if not raw:
            continue
        try:
            _, va, vsz, _, rsz = img.sec(name)
        except StopIteration:
            print('%-9s not in exe' % name)
            worst = 1
            continue
        n = min(size, vsz)
        a, b = o[raw:raw + n], img.read(va, n)
        mask = set()
        for r in range(nrel):
            off = struct.unpack_from('<I', o, rel + 10 * r)[0]
            mask.update(range(off, off + 4))
        diff = [k for k in range(n) if k not in mask and a[k] != b[k]]
        worst |= bool(diff)
        print('%-9s obj %6x exe %6x relocs %5d  diffs %d %s' % (
            name, size, vsz, nrel, len(diff), ' '.join(hex(va + k) for k in diff[:6])))
    sys.exit(worst)


if __name__ == '__main__':
    main()
