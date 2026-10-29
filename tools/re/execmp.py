"""Compare a rebuilt exe against the reference: headers, section table, bytes.

python tools/re/execmp.py <reference.exe> <rebuilt.exe>
Exits 0 only when the files are identical.
"""
import sys
import pefile


def fields(pe):
    out = {}
    for hdr in (pe.FILE_HEADER, pe.OPTIONAL_HEADER):
        for k in hdr.__keys__:
            out['%s.%s' % (hdr.name, k[0])] = getattr(hdr, k[0])
    for i, d in enumerate(pe.OPTIONAL_HEADER.DATA_DIRECTORY):
        out['DIR%d %s' % (i, d.name)] = (hex(d.VirtualAddress), hex(d.Size))
    for s in pe.sections:
        n = s.Name.rstrip(b'\0').decode()
        for k in ('VirtualAddress', 'Misc_VirtualSize', 'PointerToRawData', 'SizeOfRawData', 'Characteristics'):
            out['%s.%s' % (n, k)] = hex(getattr(s, k))
    return out


def main():
    ra, rb = (open(p, 'rb').read() for p in sys.argv[1:3])
    a, b = pefile.PE(data=ra), pefile.PE(data=rb)
    fa, fb = fields(a), fields(b)
    for k in list(fa) + [k for k in fb if k not in fa]:
        if fa.get(k) != fb.get(k):
            print('%-45s ref %-22s new %s' % (k, fa.get(k), fb.get(k)))
    print('size: ref %#x new %#x' % (len(ra), len(rb)))
    for s in a.sections:
        n = s.Name.rstrip(b'\0').decode()
        t = next((x for x in b.sections if x.Name == s.Name), None)
        if t is None or not s.SizeOfRawData:
            continue
        x, y = s.get_data(), t.get_data()
        n_diff = sum(1 for i in range(min(len(x), len(y))) if x[i] != y[i])
        first = next((i for i in range(min(len(x), len(y))) if x[i] != y[i]), None)
        print('%-9s %d differing bytes%s' % (n, n_diff, '' if first is None else
              ', first at %#x' % (a.OPTIONAL_HEADER.ImageBase + s.VirtualAddress + first)))
    hdr = a.OPTIONAL_HEADER.SizeOfHeaders
    print('headers   %d differing bytes' % sum(1 for i in range(hdr) if ra[i:i + 1] != rb[i:i + 1]))
    sys.exit(ra != rb)


if __name__ == '__main__':
    main()
