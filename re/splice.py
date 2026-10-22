"""Fill a mixed object's `#@C name` markers with gcc's code for those functions.

python re/splice.py <src/obj.s> <gcc -S output> <out.s> [name=<gcc -S output> ...]

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
`name=file` takes that function (and its jump tables) from another compile
of the same C file instead (one with other flags, e.g. a profile build).
"""
import re, sys

DEF = re.compile(r'^\s*\.def\s+([^;]+);')
LABEL = re.compile(r'^([\w$.@]+):\s*$')
SECTION = re.compile(r'^\s*(\.section\b|\.text\b|\.data\b|\.bss\b|\.ident\b)')
HEAD = re.compile(r'^\s*(\.p2align|\.globl|\.def)\b')
LCOMM = re.compile(r'^\s*\.l?comm\s+([\w$.@]+),')
# an ipa-split part (`name.part.N`) goes to .text.unlikely; the .s places it
UNLIKELY = re.compile(r'^\s*\.section\s+\.text\.unlikely\b')
PART = re.compile(r'(_[\w$]+)\.part\.\d+\b')


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
        if m and m.group(1) not in ('.text', '.ident') and not UNLIKELY.match(l):
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


def jump_tables(lines):
    """Take gcc's jump tables (an .rdata block of a label and `.long`s,
    inside a function) out of its output: ({function: [table lines]}, the
    rest).  The .s has a `#@J name k n` marker where the original's k-th
    table of the function is."""
    tables, out, fn, k = {}, [], None, 0
    while k < len(lines):
        m = LABEL.match(lines[k])
        if m and k and DEF.match(lines[k - 1]) and DEF.match(lines[k - 1]).group(1) == m.group(1):
            fn = m.group(1)
        if not re.match(r'^\s*\.section\s+\.rdata\b', lines[k]):
            out.append(lines[k])
            k += 1
            continue
        e = k + 1
        while e < len(lines) and not SECTION.match(lines[e]):
            e += 1
        body = [l for l in lines[k + 1:e] if not re.match(r'^\s*$|^\s*\.(p2)?align\b', l)]
        if fn and len(body) > 1 and LABEL.match(body[0]) and \
                all(re.match(r'^\s*\.long\s+L\d+\s*$', l) for l in body[1:]):
            tables.setdefault(fn, []).append(body)
            # back to .text: drop the `.text` that follows
            k = e + 1 if e < len(lines) and re.match(r'^\s*\.text\s*$', lines[e]) else e
            continue
        out.append(lines[k])
        k += 1
    return tables, out


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


def drop_sections(lines):
    """Drop every .rdata block (another compile's data, which isn't used)."""
    out, skip = [], False
    for l in lines:
        if SECTION.match(l) or re.match(r'^\s*\.section\b', l):
            skip = bool(re.match(r'^\s*\.section\s+\.rdata\b', l))
            if skip:
                continue
        if not skip:
            out.append(l)
    return out


def load(gen, parts, defined, only=None):
    """gcc -S output -> ({function: lines}, {function: jump tables}).  With
    `only`, just that function is wanted: other data is ignored, and the
    function must not refer to gcc's own literals."""
    gen_text = PART.sub(lambda m: parts.get(m.group(1), m.group(0)), open(gen).read())
    tables, gen_lines = jump_tables(gen_text.split('\n'))
    if only:
        fns = functions(drop_sections(gen_lines))
        if any(re.search(r'\bLC\d+\b', l) for l in fns.get(only, [])):
            sys.exit('splice.py: %s in %s refers to its own literals' % (only, gen))
        # its local labels would clash with the main compile's
        fns = {only: [re.sub(r'(?<![\w$.])L(\d+)\b', r'LF\1', l) for l in fns[only]]} \
            if only in fns else {}
    else:
        fns = functions(drop_rdata(gen_lines, defined))
    for name, body in fns.items():
        for l in body:
            m = LCOMM.match(l)
            if m and m.group(1) not in defined:
                sys.exit('splice.py: %s defines %s, which the .s does not' % (gen, m.group(1)))
        fns[name] = [l for l in body if not LCOMM.match(l)]
    return fns, tables


def main():
    src, gen, dst = sys.argv[1:4]
    lines = open(src).read().split('\n')
    defined = {m.group(1) for m in map(LABEL.match, lines) if m}
    # gcc numbers the parts in an object; the .s has our names (stripped binary)
    parts = {m.group(1): m.group(0) for m in (PART.search(l) for l in lines if l.startswith('#@C ')) if m}
    fns, tables = load(gen, parts, defined)
    for a in sys.argv[4:]:
        name, other = a.split('=', 1)
        ofns, otables = load(other, parts, defined, name)
        if name not in ofns:
            sys.exit('splice.py: %s is not defined in %s' % (name, other))
        fns[name] = ofns[name]
        tables.pop(name, None)
        if name in otables:
            tables[name] = otables[name]
    out, used, placed = [], set(), set()
    for l in lines:
        m = re.match(r'^#@J (\S+) (\d+) (\d+)$', l)
        if m:
            t = tables.get(m.group(1), [])
            k, n = int(m.group(2)), int(m.group(3))
            if k >= len(t) or len(t[k]) - 1 != n:
                sys.exit('splice.py: %s has no jump table %d of %d entries' % (m.group(1), k, n))
            out += t[k]
            placed.add((m.group(1), k))
            continue
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
    lost = ['%s %d' % (f, k) for f, t in tables.items() for k in range(len(t)) if (f, k) not in placed]
    if lost:
        sys.exit('splice.py: no `#@J` marker for jump table %s' % ', '.join(lost))
    open(dst, 'w', newline='\n').write('\n'.join(out))


if __name__ == '__main__':
    main()
