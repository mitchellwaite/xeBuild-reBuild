"""String literals in wip/app/image_read.c -> extern names for image_read.s's strings.

externize(src) returns the C text with each literal passed to a function
replaced by `ir_<address>` (the .s's string with that text) and extern
declarations for them after the struct definitions; literals gcc folds into
immediate stores (strcpy, strcat) stay.  Used by wip/irmixed.py, and to
compare a draft with re/fncmp.py without FNCMP_LITERALS (which can't tell
two blocks apart that differ only in their strings).
"""
import os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, os.path.join(ROOT, 're'))
from ddfix import Image

_text = None


def strings():
    """image_read.s's .rdata strings: text -> address"""
    global _text
    if _text is None:
        lo, hi = 0x4521b8, 0x4541f8
        d = Image(os.path.join(ROOT, 'xeBuild.exe')).read(lo, hi - lo)
        _text, i = {}, 0
        while i < len(d):
            if d[i]:
                j = d.index(0, i)
                _text.setdefault(d[i:j].decode('latin1'), lo + i)
                i = j
            i += 1
    return _text


def cstr(s):
    """C literal body -> text"""
    return s.encode('latin1').decode('unicode_escape')


def show(s):
    c = s.encode('unicode_escape').decode('latin1').replace('"', '\\"')
    return '"%s"' % c if len(c) <= 36 else '"%s..."' % c[:36]


def literals(code, used):
    """replace the literals in a piece of code; record their addresses in used"""
    text = strings()

    def lit(m):
        pre, body = m.group(1), m.group(2)
        line = code[code.rfind('\n', 0, m.start()) + 1:m.start()] + pre
        if (re.search(r'(?:strcpy|strcat)\([^,()]*, $', pre) or re.search(r'\] = $', pre)
                or '__asm__' in line or '__attribute__' in line):
            return m.group(0)
        a = text[cstr(body)]
        used.add(a)
        return pre + 'ir_%x' % a
    return re.sub(r'([^\n"]*?)"((?:[^"\\]|\\.)*)"', lit, code)


def declarations(used):
    text = strings()
    return '\n'.join('extern const char ir_%x[];\t/* %s */' % (a, show(s))
                     for s, a in sorted(text.items(), key=lambda x: x[1]) if a in used)


def externize(src):
    """the whole draft with extern names for its strings"""
    first = src.index('\n/* gcc emits these in reverse */')
    end = src.index('\n\n', src.index('static struct mobile mobiles[10];'))
    used = set()
    rest = literals(src[end:], used)
    return src[:end] + '\n\n/* strings in image_read.s */\n' + declarations(used) + rest
