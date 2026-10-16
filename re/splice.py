"""Fill a mixed object's `#@C name` markers with gcc's code for those functions.

python re/splice.py <src/obj.s> <gcc -S output> <out.s>

The .s (from split.py) holds the object's data, ident, .eh_frame and every
function not yet in C; the C file is compiled with -S and
-fno-asynchronous-unwind-tables (the .s already has the FDEs; the flag doesn't
change code).  Each function is copied from its `.p2align` to the next
function, switched to AT&T syntax around it.  Its alignment is a no-op: the
.s pads up to it as the original did.  A function that puts anything outside
.text (string literals, jump tables) can't be spliced, since its data would
not land where the original's is: give it extern names for the .s's data.
A `static` variable the .s defines (same name) can stay static in the C, so
gcc's alias analysis sees what the original's did; its `.lcomm` is dropped
and the code refers to the .s's label.
"""
import re, sys

DEF = re.compile(r'^\s*\.def\s+([^;]+);')
LABEL = re.compile(r'^([\w$.@]+):\s*$')
SECTION = re.compile(r'^\s*(\.section\b|\.text\b|\.data\b|\.bss\b|\.ident\b)')
HEAD = re.compile(r'^\s*(\.p2align|\.globl|\.def)\b')
LCOMM = re.compile(r'^\s*\.l?comm\s+([\w$.@]+),')


def functions(lines):
    """{name: [lines]} for every function gcc defined."""
    starts = []
    for k, l in enumerate(lines):
        m = LABEL.match(l)
        if m and k and DEF.match(lines[k - 1]) and DEF.match(lines[k - 1]).group(1) == m.group(1):
            s = k
            while s and HEAD.match(lines[s - 1]):
                s -= 1
            starts.append((s, m.group(1)))
    for l in lines:
        m = SECTION.match(l)
        if m and m.group(1) not in ('.text', '.ident'):
            sys.exit('splice.py: gcc put something outside .text (%r); '
                     'mixed objects keep their data in the .s' % l.strip())
    out = {}
    for j, (s, name) in enumerate(starts):
        e = starts[j + 1][0] if j + 1 < len(starts) else len(lines)
        body = lines[s:e]
        # the last one runs into the trailer (.ident, extern .defs)
        k = next((k for k, l in enumerate(body) if SECTION.match(l)), len(body))
        out[name] = body[:k]
    return out


def main():
    src, gen, dst = sys.argv[1:4]
    fns = functions(open(gen).read().split('\n'))
    lines = open(src).read().split('\n')
    defined = {m.group(1) for m in map(LABEL.match, lines) if m}
    for name, body in fns.items():
        for l in body:
            m = LCOMM.match(l)
            if m and m.group(1) not in defined:
                sys.exit('splice.py: %s defines %s, which the .s does not' % (gen, m.group(1)))
        fns[name] = [l for l in body if not LCOMM.match(l)]
    out, used = [], set()
    for l in lines:
        m = re.match(r'^#@C (\S+)$', l)
        if not m:
            out.append(l)
            continue
        name = m.group(1)
        if name not in fns:
            sys.exit('splice.py: %s is not defined in %s' % (name, gen))
        used.add(name)
        out += ['.att_syntax prefix'] + fns[name] + ['.intel_syntax noprefix']
    extra = set(fns) - used
    if extra:
        sys.exit('splice.py: %s defines %s, which the .s has no marker for (C_FUNCS)'
                 % (gen, ', '.join(sorted(extra))))
    open(dst, 'w', newline='\n').write('\n'.join(out))


if __name__ == '__main__':
    main()
