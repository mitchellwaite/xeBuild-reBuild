"""python tools/wip/dehint/bdrdata.py <file.c>: compile as bdlib does and list the .rdata strings whose
offset differs from build/bd/reference.o's (offset in the reference, offset in the draft, text).  Attempt 9."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib


def strings(b):
    out, i = [], 0
    for m in re.finditer(rb'[\x09\x0a\x20-\x7e]{4,}\x00', b):
        out.append((m.start(), m.group()[:-1].decode()))
    return out


def main():
    ok, o, d = bdlib.compile_src(bdlib.read_src(sys.argv[1]))
    if not ok:
        print(o)
        return
    a = strings(bdlib.ref()['sec']['.rdata'])
    b = dict((s, off) for off, s in strings(bdlib.section(o, '.rdata')))
    n = 0
    for off, s in a:
        if b.get(s) != off:
            n += 1
            print('%5x %5s %r' % (off, '%x' % b[s] if s in b else '-', s[:70]))
    print(n, 'strings moved')
    bdlib.cleanup(d)


if __name__ == '__main__':
    main()
