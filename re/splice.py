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
and the code refers to the .s's label.  Likewise a `static const char x[] =
"..."` naming one of the .s's strings (so gcc can fold strlen of it): its
.rdata copy is dropped.  So is gcc's copy of a function the .s still has in
asm, which the C keeps only so that its functions can inline it.
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


def drop_rdata(lines, defined):
    """Drop gcc's .rdata blocks whose labels the .s defines (a `static const
    char x[] = "..."` standing for the .s's string x, so that gcc can fold
    strlen of it); the code refers to the .s's label."""
    out, k = [], 0
    while k < len(lines):
        if not re.match(r'^\s*\.section\s+\.rdata\b', lines[k]):
            out.append(lines[k])
            k += 1
            continue
        e = k + 1
        while e < len(lines) and not SECTION.match(lines[e]):
            e += 1
        labels = [m.group(1) for m in map(LABEL.match, lines[k + 1:e]) if m]
        # `.lcomm`s don't switch sections: keep them for the check below
        out += [l for l in lines[k + 1:e] if LCOMM.match(l)]
        other = [l for l in lines[k + 1:e] if not LABEL.match(l) and not LCOMM.match(l)
                 and not re.match(r'^\s*$|^\s*\.(p2)?align\b|^\s*\.(ascii|string)\s', l)]
        undef = [n for n in labels if n not in defined]
        if not labels or other or undef:
            sys.exit('splice.py: gcc put data in .rdata that the .s does not define (%s)'
                     % (', '.join(undef) or (other + [''])[0].strip()))
        k = e
    return out


def main():
    src, gen, dst = sys.argv[1:4]
    lines = open(src).read().split('\n')
    defined = {m.group(1) for m in map(LABEL.match, lines) if m}
    fns = functions(drop_rdata(open(gen).read().split('\n'), defined))
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
    # a function the .s still has in asm may be in the C too, so that the C
    # functions can inline it (it doesn't match on its own yet): drop gcc's copy
    extra = set(fns) - used - defined
    if extra:
        sys.exit('splice.py: %s defines %s, which the .s has no marker for (C_FUNCS)'
                 % (gen, ', '.join(sorted(extra))))
    open(dst, 'w', newline='\n').write('\n'.join(out))


if __name__ == '__main__':
    main()
