"""Fill a mixed object's `#@C name` markers with gcc's code for those functions.

python re/splice.py <src/obj.s> <gcc -S output> <out.s> [_name=<other -S output> ...]
python re/splice.py --whole <gcc -S output> <out.s> _name=<other -S output> ...
(an object all in C, with some functions from a second compile)

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
# an ipa-split part (`name.part.N`) goes to .text.unlikely; the .s places it
UNLIKELY = re.compile(r'^\s*\.section\s+\.text\.unlikely\b')
PART = re.compile(r'(_[\w$]+)\.part\.\d+\b')


def functions(lines, strict=True):
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
        if strict and m and m.group(1) not in (".text", ".ident") and not UNLIKELY.match(l):
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


def load(gen, lines, defined, strict=True):
    """({function: body}, {function: jump tables}) of gcc's output gen."""
    # gcc numbers the parts in an object; the .s has our names (stripped binary)
    parts = {m.group(1): m.group(0) for m in (PART.search(l) for l in lines if l.startswith('#@C ')) if m}
    gen_text = PART.sub(lambda m: parts.get(m.group(1), m.group(0)), open(gen).read())
    tables, gen_lines = jump_tables(gen_text.split('\n'))
    fns = functions(drop_rdata(gen_lines, defined), strict)
    for name, body in fns.items():
        for l in body:
            m = LCOMM.match(l)
            if m and m.group(1) not in defined:
                sys.exit('splice.py: %s defines %s, which the .s does not' % (gen, m.group(1)))
        fns[name] = [l for l in body if not LCOMM.match(l)]
    return fns, tables


def chunk(lines, name):
    """(start, end) of function name in a whole gcc -S output (unwind
    tables on): its .p2align/.globl/.def lines to its .cfi_endproc, jump
    tables included"""
    for k, l in enumerate(lines):
        m = LABEL.match(l)
        if m and m.group(1) == name and k and DEF.match(lines[k - 1]):
            s = k
            while s and HEAD.match(lines[s - 1]):
                s -= 1
            e = next(j for j in range(k, len(lines)) if lines[j].strip() == '.cfi_endproc')
            return s, e + 1
    sys.exit('splice.py: no function %s' % name)


def whole(gen, dst, subs):
    """A whole object's gcc output with the functions in subs (`_name=other.s`)
    replaced by that compile's (and so their jump tables and FDEs)"""
    lines = open(gen).read().split('\n')
    for a in subs:
        name, other = a.split('=', 1)
        olines = open(other).read().split('\n')
        s, e = chunk(olines, name)
        body = [re.sub(r'(?<![\w$.])L(\d+)\b', r'LF\1', l) for l in olines[s:e]]
        s, e = chunk(lines, name)
        lines[s:e] = body
    open(dst, 'w', newline='\n').write('\n'.join(lines))


def main():
    if sys.argv[1] == '--whole':
        return whole(sys.argv[2], sys.argv[3], sys.argv[4:])
    src, gen, dst = sys.argv[1:4]
    lines = open(src).read().split('\n')
    defined = {m.group(1) for m in map(LABEL.match, lines) if m}
    fns, tables = load(gen, lines, defined)
    # `_name=other.s`: that function from another compile (a profile build),
    # its local labels renamed LF* so they can't clash with gen's
    lf = lambda ls: [re.sub(r'(?<![\w$.])L(\d+)\b', r'LF\1', l) for l in ls]
    for a in sys.argv[4:]:
        name, other = a.split('=', 1)
        ofns, otabs = load(other, lines, defined, False)
        fns[name] = lf(ofns[name])
        tables.pop(name, None)
        if name in otabs:
            tables[name] = [lf(t) for t in otabs[name]]
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
