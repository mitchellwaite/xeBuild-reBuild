"""Make src/app/mode_update.c (mixed object) from the draft wip/app/mode_update.c.

python wip/mumixed.py fn1 fn2 ...   (the functions that match)

String literals passed to functions become extern names for mode_update.s's
strings (`mu_<address>`); literals gcc folds into immediate stores (strcpy,
strcat and array initializers) stay.  The data definitions become extern
declarations.  Prints the SYMBOLS entries for the strings used.
"""
import os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 're'))
from ddfix import Image


def cstr(s):
    """C literal body -> text"""
    return s.encode('latin1').decode('unicode_escape')


def strings():
    """mode_update.s's .rdata strings: text -> address"""
    lo, hi = 0x44c6e8, 0x44deb8
    d = Image('xeBuild.exe').read(lo, hi - lo)
    out, i = {}, 0
    while i < len(d):
        if d[i]:
            j = d.index(0, i)
            out[d[i:j].decode('latin1')] = lo + i
            i = j
        i += 1
    return out


def main():
    want = sys.argv[1:]
    src = open('wip/app/mode_update.c').read()
    text = strings()
    first = src.index('\nint useConsoleAddons = 1;')
    end = src.index('\n\n', src.index('static char path[260];'))
    head = src[:first]
    data = src[first:end]
    data = data.replace('int useConsoleAddons = 1;', 'extern int useConsoleAddons;')
    data = re.sub(r'^static ', 'extern ', data, flags=re.M)
    data = data.replace('/* gcc emits these in reverse: path comes first in .bss */',
                        "/* mode_update.s's data */")
    fns = {}
    for m in re.finditer(r'\n((?:static )?[^\n;{}#]*?\b(\w+)\([^;{]*\)\n\{.*?\n\})\n', src, re.S):
        fns[m.group(2)] = m.group(1)
    missing = [w for w in want if w not in fns]
    if missing:
        sys.exit('mumixed.py: no function %s in the draft' % ', '.join(missing))
    used = {}

    def lit(m):
        pre, body = m.group(1), m.group(2)
        if re.search(r'(?:strcpy|strcat)\([^,()]*, $|= $', pre):
            return m.group(0)
        a = text[cstr(body)]
        used[a] = 'mu_%x' % a
        return pre + used[a]
    body = []
    for name in fns:
        if name in want:
            body.append(re.sub(r'([^\n"]*?)"((?:[^"\\]|\\.)*)"',
                               lambda m: lit(m), fns[name]))

    def show(s):
        c = s.encode('unicode_escape').decode('latin1').replace('"', '\\"')
        return '"%s"' % c if len(c) <= 36 else '"%s..."' % c[:36]
    ext = ['extern const char %s[];\t/* %s */' % (used[a], show(s))
           for s, a in sorted(text.items(), key=lambda x: x[1]) if a in used]
    head = head.replace(
        ' over the network */',
        ' over the network.\n   Mixed object: the functions here are spliced into mode_update.s\n'
        '   (re/splice.py), which still holds the rest and the data, so strings\n'
        "   and variables are extern names for the .s's.  wip/app/mode_update.c\n"
        '   is the whole draft. */', 1)
    out = (head + data + '\n\n/* strings in mode_update.s */\n' + '\n'.join(ext) + '\n\n' +
           '\n\n'.join(body) + '\n')
    open('src/app/mode_update.c', 'w', newline='\n').write(out)
    print(',\n'.join("0x%x: '_%s'" % (a, n) for a, n in sorted(used.items())))


main()
