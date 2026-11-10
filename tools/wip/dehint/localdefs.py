"""List the file-scope declarations in src/*.c (prototypes, externs, macros, types) and say
which look redundant: also declared in a header, defined before every use, unused, or
named again in another file.  The check is syntactic; it doesn't compile anything.

python tools/wip/dehint/localdefs.py [repo]

BORDERLINE.md's "Redundant file-local definitions" section comes from this output."""
import glob, os, re, sys

R = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
cs = sorted(glob.glob(os.path.join(R, 'src', '*.c')))
hs = sorted(glob.glob(os.path.join(R, 'src', '*.h')))
PROTO = re.compile(r'^(?:static\s+)?[A-Za-z_][A-Za-z0-9_ \*]*?[ \*]([A-Za-z_][A-Za-z0-9_]*)\(([^;{]*)\)\s*(?:__asm__\s*\([^)]*\))?\s*(;?)\s*$')
DEFINE = re.compile(r'^\s*#\s*define\s+([A-Za-z_][A-Za-z0-9_]*)')
TYPE = re.compile(r'^(?:typedef\s+)?(?:struct|union|enum)\s+([A-Za-z_][A-Za-z0-9_]*)\s*\{')
TYPEDEF = re.compile(r'^typedef\b.*?\b([A-Za-z_][A-Za-z0-9_]*)\s*;\s*$')
EXTERN = re.compile(r'^extern\b.*?\b([A-Za-z_][A-Za-z0-9_]*)\s*(?:\[[^\]]*\])*\s*;')


def strip_comments(t):
    t = re.sub(r'/\*.*?\*/', lambda m: re.sub(r'[^\n]', ' ', m.group(0)), t, flags=re.S)
    return re.sub(r'//[^\n]*', '', t)


text = {f: strip_comments(open(f, encoding='utf-8', errors='replace').read()) for f in cs + hs}
lines = {f: text[f].split('\n') for f in text}
hall = '\n'.join(text[h] for h in hs)


def word_count(t, name):
    return len(re.findall(r'\b' + re.escape(name) + r'\b', t))


def where_in_headers(name, pat):
    out = []
    for h in hs:
        for i, l in enumerate(lines[h]):
            if re.search(pat % re.escape(name), l):
                out.append('%s:%d' % (os.path.basename(h), i + 1))
    return out


for f in cs:
    b = os.path.basename(f)
    ls = lines[f]
    defs = {}
    protos = []
    for i, l in enumerate(ls):
        m = PROTO.match(l)
        if not m or l.startswith(('return', 'else', 'typedef')):
            continue
        name = m.group(1)
        if m.group(3) == ';':
            protos.append((i, name, l.strip()))
        elif i + 1 < len(ls) and ls[i + 1].strip() == '{':
            defs.setdefault(name, i)
    for i, name, l in protos:
        notes = []
        hd = where_in_headers(name, r'\b%s\s*\(')
        if hd:
            notes.append('also declared in ' + ', '.join(hd))
        uses = [j for j, x in enumerate(ls) if j != i and j != defs.get(name)
                and re.search(r'\b' + re.escape(name) + r'\s*\(', x)]
        if name in defs:
            first = min(uses) if uses else None
            if first is None:
                notes.append('defined here at %d, no other use in this file' % (defs[name] + 1))
            elif defs[name] < first:
                notes.append('defined here at %d, before its first use at %d: not needed'
                             % (defs[name] + 1, first + 1))
            else:
                notes.append('defined here at %d, first use at %d: needed unless moved to a header'
                             % (defs[name] + 1, first + 1))
        else:
            other = [os.path.basename(g) for g in cs if g != f and re.search(
                r'^[A-Za-z_][A-Za-z0-9_ \*]*[ \*]' + re.escape(name) + r'\([^;]*\)\s*$', text[g], flags=re.M)]
            notes.append('defined in ' + (', '.join(other) if other else 'no src file (libc?)'))
            if not uses:
                notes.append('unused here')
        print('PROTO   %s:%d  %s  -> %s' % (b, i + 1, l[:90], '; '.join(notes)))
    for i, l in enumerate(ls):
        for kind, rx in (('MACRO', DEFINE), ('TYPE', TYPE), ('TYPEDEF', TYPEDEF), ('EXTERN', EXTERN)):
            m = rx.match(l)
            if not m:
                continue
            name = m.group(1)
            notes = []
            n = word_count(text[f], name) - 1
            notes.append('unused in this file' if n == 0 else '%d uses' % n)
            if word_count(hall, name):
                notes.append('name also in headers: ' + ', '.join(where_in_headers(name, r'\b%s\b')[:4]))
            others = [os.path.basename(g) for g in cs if g != f and word_count(text[g], name)]
            if others:
                notes.append('name also in ' + ', '.join(others[:6]))
            print('%-7s %s:%d  %s  -> %s' % (kind, b, i + 1, l.strip()[:80], '; '.join(notes)))
            break
