"""Make src/app/image_read.c (mixed object) from the draft wip/app/image_read.c.

python wip/irmixed.py fn1 fn2 ...   (the functions that match)

String literals passed to functions become extern names for image_read.s's
strings (`ir_<address>`, wip/irlit.py); literals gcc folds into immediate
stores (strcpy, strcat) stay.  The data definitions become extern
declarations, except statics that a function here writes: those stay static
(re/splice.py drops their .lcomm), so gcc's alias analysis matches the
original's.  A static only the .s's code writes would look constant to gcc.
A static function gets noinline: with fewer callers in the mixed file gcc
would otherwise inline it away, and the .s still calls it.
"""
import os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from irlit import literals, declarations

STATIC = {'fsBuf', 'fsValid', 'fsOffset', 'anchor', 'mobiles'}


def main():
    want = sys.argv[1:]
    src = open('wip/app/image_read.c').read()
    first = src.index('\n/* gcc emits these in reverse */')
    end = src.index('\n\n', src.index('static struct mobile mobiles[10];'))
    head = src[:first]
    data = src[first:end]
    data = re.sub(r'^static (.*?\b(\w+)(?:\[\w*\])?;)', lambda m: m.group(0) if m.group(2) in STATIC
                  else 'extern ' + m.group(1), data, flags=re.M)
    data = re.sub(r'^(struct \w+ \*?\w+) = [^;]*;', r'extern \1;', data, flags=re.M)
    data = re.sub(r'^char (\w+)\[(\d*)\] = [^;]*;', r'extern char \1[\2];', data, flags=re.M)
    data = data.replace('/* gcc emits these in reverse */', "/* image_read.s's data */")
    fns = {}
    for m in re.finditer(r'\n((?:__attribute__\(\([^\n]*?\)\) )?(?:static )?(?:inline )?[^\n;{}#(]*?\b(\w+)\([^;{]*\)\n\{.*?\n\})\n', src, re.S):
        fns[m.group(2)] = m.group(1)
    missing = [w for w in want if w not in fns]
    if missing:
        sys.exit('irmixed.py: no function %s in the draft' % ', '.join(missing))
    used = set()
    body = []
    for name in fns:
        if name in want:
            f = literals(fns[name], used)
            f = re.sub(r'^static ', 'static __attribute__((noinline)) ', f)
            body.append(f)
    head = head.replace(
        ' smc.bin */',
        ' smc.bin.\n   Mixed object: the functions here are spliced into image_read.s\n'
        '   (re/splice.py), which still holds the rest and the data, so strings\n'
        "   and variables are the .s's.  wip/app/image_read.c is the whole\n"
        '   draft; wip/irmixed.py makes this file from it. */', 1)
    out = (head + data + '\n\n/* strings in image_read.s */\n' + declarations(used) + '\n\n' +
           '\n\n'.join(body) + '\n')
    open('src/app/image_read.c', 'w', newline='\n').write(out)


main()
