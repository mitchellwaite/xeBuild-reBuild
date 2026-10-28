"""Make a whole-object src/app/mode_client.c (no mode_client.s) from the draft.

src/app/mode_client.c was made with it from the draft plus the BUILD_FDO
macros (NOPROF, AT, JUMP, NO_MODE_ARG; wip/mc/s18/match) and its padding;
edit that file now rather than regenerating it.

python wip/mcwhole.py [draft.c] [out.c]   (wip/app/mode_client.c, src/app/mode_client.c)

Built with -fno-toplevel-reorder (the draft's functions match with it too),
which emits functions and variables in definition order.  As in
wip/irwhole.py the string literals become `static const char mc_<addr>[]`
arrays, each defined just before the first function that uses it, so .rdata
comes out in the original's order; literals of 31+ bytes are aligned 4,
shorter ones 1.  client_usage's switch table is emitted with the function,
after the arrays defined before it.  Checks every string's address against
the original's.
"""
import os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, os.path.join(ROOT, 're'))
from ddfix import Image

RDATA, RDATA_END = 0x44e10c, 0x44fb1c
# client_usage's switch table: (address, size)
TABLE = (0x44eba8, 24)


def strings():
    """mode_client.s's .rdata strings: text -> address"""
    d = Image(os.path.join(ROOT, 'xeBuild.exe')).read(RDATA, RDATA_END - RDATA)
    out, i = {}, 0
    while i < len(d):
        if d[i]:
            j = d.index(0, i)
            out.setdefault(d[i:j].decode('latin1'), RDATA + i)
            i = j
        i += 1
    return out


def cstr(s):
    """C literal body -> text"""
    return s.encode('latin1').decode('unicode_escape')


def main():
    src_path = sys.argv[1] if len(sys.argv) > 1 else 'wip/app/mode_client.c'
    out_path = sys.argv[2] if len(sys.argv) > 2 else 'src/app/mode_client.c'
    src = open(src_path).read()
    text = strings()
    by_addr = {a: s for s, a in text.items()}
    first = src.index('\nstatic struct consoleinfo *cinfo;')
    end = src.index('\n\n', first + 1)
    head, rest = src[:end], src[end:]

    def literals(code, used):
        def lit(m):
            pre, body = m.group(1), m.group(2)
            line = code[code.rfind('\n', 0, m.start()) + 1:m.start()] + pre
            if (re.search(r'(?:strcpy|strcat)\([^,()]*, $', pre) or re.search(r'= $', pre)
                    or '__asm__' in line or '__attribute__' in line):
                return m.group(0)
            a = text[cstr(body)]
            used.add(a)
            return pre + 'mc_%x' % a
        return re.sub(r'([^\n"]*?)"((?:[^"\\]|\\.)*)"', lit, code)

    # functions, each with what precedes it (comments)
    chunks = re.split(r'(?<=\n\})\n', rest)
    used_by, body = [], []
    for c in chunks:
        used = set()
        body.append(literals(c, used))
        used_by.append(used)
    usage = next(k for k, c in enumerate(chunks) if re.search(r'\nvoid client_usage\(', c))
    first_use = {}
    for k, used in enumerate(used_by):
        for a in used:
            first_use.setdefault(a, k)

    # walk .rdata in address order: a string goes before its first user, and
    # no earlier than the strings before it; the table follows the strings
    # defined before client_usage
    slots = {}
    cur = 0
    addr = RDATA
    table = False
    for a in sorted(first_use):
        k = first_use[a]
        if k < cur:
            sys.exit('mcwhole.py: mc_%x (first used in chunk %d) comes after chunk %d\'s strings'
                     % (a, k, cur))
        if k > usage and not table:
            addr = (addr + 3) & ~3
            if addr != TABLE[0]:
                sys.exit('mcwhole.py: the switch table would be at %x' % addr)
            addr += TABLE[1]
            table = True
        cur = k
        b = by_addr[a].encode('latin1')
        al = 4 if len(b) + 1 >= 31 else 1
        addr = (addr + al - 1) & ~(al - 1)
        if addr != a:
            sys.exit('mcwhole.py: mc_%x would be at %x' % (a, addr))
        addr += len(b) + 1
        slots.setdefault(k, []).append(a)
    print('rdata end %x (original %x)' % (addr, RDATA_END))

    def cdef(a):
        s = by_addr[a]
        lit = s.encode('unicode_escape').decode('latin1').replace('"', '\\"')
        al = 4 if len(s) + 1 >= 31 else 1
        return 'static const char mc_%x[] __attribute__((aligned(%d))) = "%s";' % (a, al, lit)

    out = []
    for k, c in enumerate(body):
        if k in slots:
            m = re.match(r'\n*', c)
            c = c[:m.end()] + '\n'.join(cdef(a) for a in slots[k]) + '\n' + c[m.end():]
        out.append(c)
    open(out_path, 'w', newline='\n').write(head + '\n'.join(out))


main()
