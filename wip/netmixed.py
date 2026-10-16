"""Make src/app/net.c (mixed object) from the draft wip/app/net.c.

python wip/netmixed.py fn1 fn2 ...   (the functions that match)

String literals passed to functions become static arrays named after net.s's strings
(`net_<address>`).  netInfo and netStartTime become extern declarations (the
.s's netReadInfo writes netInfo; a static nothing in the C writes would read
as 0), netSock loses its initializer (the .s has it) and netRecv, still asm,
gets a declaration with the local calling convention gcc gave it (len in
eax).  Prints the SYMBOLS entries for the strings used.
"""
import os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 're'))
from ddfix import Image


def cstr(s):
    """C literal body -> text"""
    return s.encode('latin1').decode('unicode_escape')


class Strings(dict):
    """net.s's .rdata strings: text -> address.  ld merges a literal into
    the tail of a longer one ("OK\\n" in "...: OK\\n"), so a missing text is
    looked up as a suffix."""

    def __missing__(self, s):
        k = self.data.index(s.encode('latin1') + b'\0')
        self[s] = self.lo + k
        return self[s]


def strings():
    lo, hi = 0x4574b0, 0x457a80
    d = Image('xeBuild.exe').read(lo, hi - lo)
    out, i = Strings(), 0
    out.lo, out.data = lo, d
    while i < len(d):
        if d[i]:
            j = d.index(0, i)
            out.setdefault(d[i:j].decode('latin1'), lo + i)
            i = j
        i += 1
    return out


DATA = {
    'static SOCKET netSock = INVALID_SOCKET;': 'static SOCKET netSock;',
    'static struct consoleinfo *netInfo;': 'extern struct consoleinfo *netInfo;',
    'time_t netStartTime;': 'extern time_t netStartTime;',
}


def main():
    want = sys.argv[1:]
    src = open('wip/app/net.c').read()
    text = strings()
    first = src.index('\nstatic SOCKET netSock')
    end = src.index('\n\n', first + 1)
    head = src[:first]
    data = src[first:end]
    for a, b in DATA.items():
        assert a in data, a
        data = data.replace(a, b)
    data = data.replace('\nstatic SOCKET', "\n/* net.s's data */\nstatic SOCKET", 1)
    fns = {}
    for m in re.finditer(r'\n((?:/\*[^\n]*\*/\n)?((?:static )?(?:inline )?[^\n;{}#]*?\b(\w+)\([^;{]*\))\n\{.*?\n\})\n',
                         src, re.S):
        fns[m.group(3)] = m.group(1)
    missing = [w for w in want if w not in fns]
    if missing:
        sys.exit('netmixed.py: no function %s in the draft' % ', '.join(missing))
    used, lits = {}, {}

    def lit(m):
        pre, body = m.group(1), m.group(2)
        if '/*' in pre or re.search(r'(?:strcpy|strcat)\([^,()]*, $|= $|char [^;]*= $', pre):
            return m.group(0)
        a = text[cstr(body)]
        used[a] = 'net_%x' % a
        lits[a] = body
        return pre + used[a]
    body = []
    for name in fns:
        if name in want:
            body.append(re.sub(r'([^\n"]*?)"((?:[^"\\]|\\.)*)"', lit, fns[name]))

    ext = ['static const char %s[] = "%s";' % (used[a], lits[a]) for a in sorted(used)]
    asm = ['/* still in net.s; gcc gave it the local calling convention */',
           'u8 *netRecv(int *len) __attribute__((regparm(1)));']
    sigs = {n: re.match(r'(?:/\*[^\n]*\*/\n)?([^\n]*\))', fns[n]).group(1) for n in fns}
    asm += ['%s;' % sigs[n] for n in fns
            if n not in want and n != 'netRecv' and not sigs[n].startswith('static')]
    head = head.replace(
        ' console info */',
        ' console info.\n   Mixed object: the functions here are spliced into net.s\n'
        '   (re/splice.py), which still holds the rest and the data, so strings\n'
        "   name the .s's (splice.py drops gcc's copies; static arrays rather\n"
        '   than externs so that gcc still folds strlen of them).\n'
        '   wip/app/net.c is the whole draft; wip/netmixed.py makes this file\n'
        '   from it. */', 1)
    out = (head + data + '\n\n/* strings in net.s */\n' + '\n'.join(ext) + '\n\n' +
           '\n'.join(asm) + '\n\n' + '\n\n'.join(body) + '\n')
    open('src/app/net.c', 'w', newline='\n').write(out)
    print(',\n'.join("0x%x: '_%s'" % (a, n) for a, n in sorted(used.items())))


main()
