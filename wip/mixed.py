"""Make a mixed object's src/<obj>.c from its full draft wip/<obj>.c.

python wip/mixed.py <obj> fn1 fn2 ...   (the functions that match)

Generic version of netmixed.py, set up per object in OBJS.  String literals
passed to functions become static arrays named after the .s's strings
(`<prefix>_<address>`; static arrays rather than externs so gcc still folds
strlen of them, and splice.py drops gcc's .rdata copies).  Functions not
listed get declarations: non-static ones as written, static ones with the
local calling convention gcc gave them (OBJS' `regparm`).  Prints the
SYMBOLS entries for the strings used.
"""
import os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 're'))
from ddfix import Image

OBJS = {
    'app/image_write': dict(prefix='iw', rdata=(0x451760, 0x451fb4),
                            regparm={'imgWriteStart': 3, 'imgWritePage': 3},
                            # asm still, here for their calls: imgWriteAt is
                            # gcc's ipa-cp clone of imgAdd (type 0, pad 1)
                            inline={'imgAdd', 'imgAddFile'},
                            note='bytes, writing the image to disk */',
                            # the .s keeps the object's data
                            subs=[('\nchar copyright[0x40] = "\\xa9 2004-2009 Microsoft Corporation. '
                                   'All rights reserved.";\n', '\nextern char copyright[0x40];\n'),
                                  ('\nu32 mobileOffset;\n', '\nextern u32 mobileOffset;\n')]),
}


def cstr(s):
    """C literal body -> text"""
    return s.encode('latin1').decode('unicode_escape')


class Strings(dict):
    """the .s's .rdata strings: text -> address.  ld merges a literal into
    the tail of a longer one, so a missing text is looked up as a suffix."""

    def __missing__(self, s):
        k = self.data.index(s.encode('latin1') + b'\0')
        self[s] = self.lo + k
        return self[s]


def strings(lo, hi):
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


# __attribute__((noinline, noclone)) or ((optimize("no-early-inlining"))),
# before the type or on a line of its own
AT = r'__attribute__\(\((?:[\w, ]|"[^"\n]*"|\([^()\n]*\))+\)\)[ \n]'
FN = re.compile(r'\n((?:/\*[^\n]*\*/\n)?((?:%s)?(?:static )?(?:inline )?(?:%s)?[^\n;{}#]*?\b(\w+)\([^;{]*\))\n\{.*?\n\})\n' % (AT, AT), re.S)
ATTR = re.compile(AT)
SIG = re.compile(r'(?:/\*[^\n]*\*/\n)?(.*?\))\n\{', re.S)


def main():
    obj, want = sys.argv[1], sys.argv[2:]
    cfg = OBJS[obj]
    # MIXED_SRC / MIXED_OUT: try a variant of the draft without touching src/
    src = open(os.environ.get('MIXED_SRC', 'wip/%s.c' % obj)).read()
    text = strings(*cfg['rdata'])
    first = FN.search(src)
    head = src[:first.start()]
    fns = {}
    for m in FN.finditer(src):
        fns[m.group(3)] = m.group(1)
    missing = [w for w in want if w not in fns]
    if missing:
        sys.exit('mixed.py: no function %s in the draft' % ', '.join(missing))
    used, lits = {}, {}

    def lit(m):
        pre, body = m.group(1), m.group(2)
        if '/*' in pre or re.search(r'(?:strcpy|strcat)\([^,()]*, $|= $|char [^;]*= $', pre):
            return m.group(0)
        a = text[cstr(body)]
        used[a] = '%s_%x' % (cfg['prefix'], a)
        lits[a] = body
        return pre + used[a]
    body = []
    # objects with a crafted profile for some functions (OBJS' `profiled`):
    # the others get the draft's NOPROF macro (the guessed profile in the
    # profile compile, where a function without counts would compile as
    # never executed)
    for name in list(fns):
        if 'profiled' in cfg and name not in cfg['profiled'] and name in want:
            f = fns[name]
            c = f.index('\n') + 1 if f.startswith('/*') else 0
            fns[name] = f[:c] + 'NOPROF\n' + f[c:]
    for name in fns:
        if name in want or name in cfg['inline']:
            # asm templates and constraints and attribute arguments aren't
            # strings in the .s
            body.append('\n'.join(l if '__asm__' in l or '__attribute__' in l else re.sub(r'([^\n"]*?)"((?:[^"\\]|\\.)*)"', lit, l)
                                  for l in fns[name].split('\n')))

    ext = ['static const char %s[] = "%s";' % (used[a], lits[a]) for a in sorted(used)]
    # attributes like noclone matter for the definition only
    sigs = {n: ATTR.sub('', SIG.match(fns[n]).group(1)) for n in fns}
    asm = []
    for n in fns:
        if n in want or n in cfg['inline']:
            continue
        s = sigs[n]
        if s.startswith('static'):
            if n in cfg['regparm']:
                asm.append('%s __attribute__((regparm(%d)));' % (s[len('static '):], cfg['regparm'][n]))
        else:
            asm.append('%s;' % s)
    for old, new in cfg.get('subs', []):
        if old not in head:
            sys.exit('mixed.py: %r is not in the draft' % old)
        head = head.replace(old, new, 1)
    head = head.replace(
        cfg['note'],
        cfg['note'][:-3] + '.\n   Mixed object: the functions here are spliced into %s.s\n'
        '   (re/splice.py), which still holds the rest and the data, so strings\n'
        "   name the .s's (splice.py drops gcc's copies; static arrays rather\n"
        '   than externs so that gcc still folds strlen of them).\n'
        '   wip/%s.c is the whole draft; wip/mixed.py makes this file\n'
        '   from it. */' % (os.path.basename(obj), obj), 1)
    out = (head.rstrip('\n') + '\n\n/* strings in %s.s */\n' % os.path.basename(obj) + '\n'.join(ext) +
           '\n\n/* still in %s.s */\n' % os.path.basename(obj) + '\n'.join(asm) + '\n\n' +
           '\n\n'.join(body) + '\n')
    open(os.environ.get('MIXED_OUT', 'src/%s.c' % obj), 'w', newline='\n').write(out)
    print(',\n'.join("0x%x: '_%s'" % (a, n) for a, n in sorted(used.items())))


main()
