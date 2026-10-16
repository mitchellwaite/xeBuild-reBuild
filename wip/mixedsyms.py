"""Rewrite an object's string names in re/split.py SYMBOLS from mixed.py's output.

python wip/mixed.py app/build fn... > syms.txt
python wip/mixedsyms.py <prefix> syms.txt

Replaces the block after the `# <obj>'s strings that its C functions use`
comment (the `0x...: '_<prefix>_...'` lines) with the listed entries, three
to a line.
"""
import re, sys

prefix, path = sys.argv[1:3]
ents = re.findall(r"0x([0-9a-f]+): '(_%s_[0-9a-f]+)'" % prefix, open(path).read())
lines = []
for k in range(0, len(ents), 3):
    lines.append('    ' + ' '.join("0x%s: '%s'," % e for e in ents[k:k + 3]))
src = open('re/split.py').read()
pat = re.compile(r"(    # \S+'s strings that its C functions use \(wip/mixed\.py\)\n)"
                 r"((?:    0x[0-9a-f]+: '_%s_[0-9a-f]+',.*\n)+)" % prefix)
m = pat.search(src)
if not m:
    sys.exit('mixedsyms.py: no string block for %s in re/split.py' % prefix)
src = src[:m.start(2)] + '\n'.join(lines) + '\n' + src[m.end(2):]
open('re/split.py', 'w', newline='\n').write(src)
print('%d names' % len(ents))
