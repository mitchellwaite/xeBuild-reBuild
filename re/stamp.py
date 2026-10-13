"""Set a PE's TimeDateStamp and recompute its CheckSum, in place.

python re/stamp.py <file.exe> <timestamp>

binutils 2.27 can only write time() or 0 (--no-insert-timestamp) and has no
SOURCE_DATE_EPOCH support, so the original link time is applied after linking.
The checksum is recomputed the same way ld (and imagehlp) does it.
"""
import struct, sys


def checksum(d, csum_off):
    s = 0
    for i in range(0, len(d) - len(d) % 2, 2):
        if i in (csum_off, csum_off + 2):
            continue
        s += struct.unpack_from('<H', d, i)[0]
        s = (s & 0xffff) + (s >> 16)
    if len(d) % 2:
        s += d[-1]
        s = (s & 0xffff) + (s >> 16)
    return ((s & 0xffff) + (s >> 16) + len(d)) & 0xffffffff


def main():
    path, ts = sys.argv[1], int(sys.argv[2], 0)
    d = bytearray(open(path, 'rb').read())
    pe = struct.unpack_from('<I', d, 0x3c)[0]
    struct.pack_into('<I', d, pe + 8, ts)
    csum_off = pe + 24 + 64
    struct.pack_into('<I', d, csum_off, checksum(d, csum_off))
    open(path, 'wb').write(d)


if __name__ == '__main__':
    main()
