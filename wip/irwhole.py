"""Make a whole-object src/app/image_read.c (no image_read.s) from the draft.

python wip/irwhole.py [draft.c] [out.c]   (wip/app/image_read.c, src/app/image_read.c)

Built with -fno-toplevel-reorder, which emits functions and variables in
definition order.  The string literals become `static const char ir_<addr>[]`
arrays (wip/irlit.py names), each defined just before the first function
whose part of .rdata it lies in, so .rdata comes out in the original's order
whatever order gcc expands the blocks in; literals of 31+ bytes are aligned
4, shorter ones 1 (gcc's rule; a user alignment skips gcc's bump).  The
variables go in the original's .data / .bss order.  Checks every string's
address against the original's.
"""
import os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from irlit import strings, literals, cstr

RDATA = 0x4521b8


def main():
    src_path = sys.argv[1] if len(sys.argv) > 1 else 'wip/app/image_read.c'
    out_path = sys.argv[2] if len(sys.argv) > 2 else 'src/app/image_read.c'
    src = open(src_path).read()
    first = src.index('\n/* gcc emits these in reverse */')
    end = src.index('\n\n', src.index('static struct mobile mobiles[10];'))
    head, data, rest = src[:first], src[first:end], src[end:]

    # variables: one definition per line, put in the original's order
    defs = {}
    for l in data.split('\n'):
        m = re.match(r'^(?:static )?[\w ]+?\**\b(\w+)(?:\[\w*\])?(?: = .*)?;$', l)
        if m:
            defs[m.group(1)] = l
    bss = ['mobiles', 'anchor', 'fsOffset', 'fsValid', 'fsBuf', 'dumpSize']
    dat = ['zeropair', 'mobileName', 'fs']
    assert set(defs) == set(bss + dat), set(defs) ^ set(bss + dat)
    data = ('\n/* .bss and .data in the original\'s order */\n' +
            '\n'.join(defs[n] for n in bss) + '\n' + '\n'.join(defs[n] for n in dat))

    # functions, each with what precedes it (comments)
    chunks = re.split(r'(?<=\n\})\n', rest)
    used_by = []
    body = []
    for c in chunks:
        used = set()
        body.append(literals(c, used))
        used_by.append(used)
    text = strings()
    by_addr = {a: s for s, a in text.items()}
    first_use = {}
    for k, used in enumerate(used_by):
        for a in used:
            first_use.setdefault(a, k)
    # walk .rdata in address order: a string goes before its first user, and
    # no earlier than the strings before it
    slots = {}
    cur = 0
    addr = RDATA
    for a in sorted(first_use):
        k = first_use[a]
        if k < cur:
            sys.exit('irwhole.py: ir_%x (first used in chunk %d) comes after chunk %d\'s strings'
                     % (a, k, cur))
        cur = k
        b = by_addr[a].encode('latin1')
        al = 4 if len(b) + 1 >= 31 else 1
        addr = (addr + al - 1) & ~(al - 1)
        if addr != a:
            sys.exit('irwhole.py: ir_%x would be at %x' % (a, addr))
        addr += len(b) + 1
        slots.setdefault(k, []).append(a)
    print('rdata end %x' % addr)

    def cdef(a):
        s = by_addr[a]
        lit = s.encode('unicode_escape').decode('latin1').replace('"', '\\"')
        al = 4 if len(s) + 1 >= 31 else 1
        return 'static const char ir_%x[] __attribute__((aligned(%d))) = "%s";' % (a, al, lit)

    out = []
    for k, c in enumerate(body):
        if k in slots:
            m = re.match(r'\n*', c)
            c = c[:m.end()] + '\n'.join(cdef(a) for a in slots[k]) + '\n' + c[m.end():]
        out.append(c)
    open(out_path, 'w', newline='\n').write(head + data + '\n'.join(out))


main()
