"""Write the "Progress" section of README.md: which objects and functions are in C.

python re/progress.py [README.md]

Run after `sh build.sh` (it reads build/obj/*.o and build/xeBuild.map for the
function names).  Functions come from the reference exe's .eh_frame (one FDE
each, units.py); an object is C if src/<obj>.c exists (fully C only with no .s and no
top-level asm in the .c left), and in a mixed object
(src/<obj>.s too) only the C_FUNCS addresses are C.  Functions a .c defines
in top-level __asm__ (still assembly) aren't C.  A function still in
assembly whose SYMBOLS name is defined in a draft wip/<obj>.c counts as C
too if re/fncmp.py says it matches.  The section is replaced between the
progress:begin/end markers.
"""
import collections, os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(__file__))
from ddfix import Image
from units import units
from split import NAMES, C_FUNCS, SYMBOLS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OBJDUMP = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin', 'objdump.exe')
BEGIN, END = '<!-- progress:begin -->', '<!-- progress:end -->'
# gcc flags for re/fncmp.py on a wip draft (as build.sh would use); default -O3
WIP_FLAGS = {'app/image_write': ['-O3', '--param', 'builtin-expect-probability=50'],
             'app/net': ['-O3', '--param', 'builtin-expect-probability=65']}
SYMLINE = re.compile(r'\(sec\s+(\d+)\).*\(ty\s+20\).*0x([0-9a-f]+) (\S+)$')
MAPLINE = re.compile(r'^ (\.text(?:\.startup)?)\s+0x([0-9a-f]+)\s+0x[0-9a-f]+ build/obj/(\S+)\.o$')
# per-function state -> marker
MARK = {'C': '✅', 'wip': '☑️', 'draft': '⬜', 'asm': '⬜'}


def section_bases():
    """{obj: {section name: va}} for .text and .text.startup from the link map."""
    bases = collections.defaultdict(dict)
    for l in open(os.path.join(ROOT, 'build', 'xeBuild.map')):
        m = MAPLINE.match(l.rstrip('\n'))
        if m:
            bases[m.group(3)][m.group(1)] = int(m.group(2), 16)
    return bases


def func_names(obj, bases):
    """{va: name} for the function symbols in build/obj/<obj>.o."""
    o = os.path.join(ROOT, 'build', 'obj', obj + '.o')
    hdr = subprocess.run([OBJDUMP, '-h', o], capture_output=True, text=True, check=True).stdout
    secname = {int(m.group(1)) + 1: m.group(2)
               for m in re.finditer(r'^\s+(\d+) (\S+)', hdr, re.M)}
    syms = subprocess.run([OBJDUMP, '-t', o], capture_output=True, text=True, check=True).stdout
    names = {}
    for l in syms.splitlines():
        m = SYMLINE.search(l)
        if m:
            s = secname.get(int(m.group(1)))
            if s in bases[obj]:
                names.setdefault(bases[obj][s] + int(m.group(2), 16), m.group(3).lstrip('_'))
    return names


def asm_funcs(obj, fdes):
    """Functions a src/<obj>.c defines in top-level __asm__ (a label line `"_name:`)."""
    src = os.path.join(ROOT, 'src', obj + '.c')
    if not os.path.exists(src):
        return set()
    text = open(src, encoding='utf-8').read()
    return {a for a, _ in fdes if SYMBOLS.get(a) and '"%s:' % SYMBOLS[a] in text}


def wip_state(obj, addrs):
    """{va: 'wip' or 'draft'} for the functions wip/<obj>.c defines (matching or not)."""
    src = os.path.join('wip', obj + '.c')
    if not os.path.exists(os.path.join(ROOT, src)):
        return {}
    text = open(os.path.join(ROOT, src), encoding='utf-8').read()
    out = {}
    for a in addrs:
        name = SYMBOLS.get(a, '').lstrip('_')
        if not name or not re.search(r'^\w[^;{]*\b%s\(' % re.escape(name), text, re.M):
            continue
        r = subprocess.run([sys.executable, os.path.join(ROOT, 're', 'fncmp.py'), src, name]
                           + WIP_FLAGS.get(obj, []), capture_output=True, text=True, cwd=ROOT,
                           # drafts keep their string literals
                           env=dict(os.environ, FNCMP_LITERALS='1'))
        out[a] = 'wip' if r.stdout.strip() == 'MATCH' else 'draft'
    return out


def main():
    readme = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'README.md')
    img = Image(os.path.join(ROOT, 'xeBuild.exe'))
    bases = section_bases()
    objs = collections.OrderedDict()   # obj -> [(va, name, state)]
    asm_left = {}                      # obj -> where its remaining asm is
    for i, (_, fdes) in enumerate(units(img)):
        obj = NAMES[i][0]
        if obj.startswith('runtime/'):
            continue
        names = func_names(obj, bases)
        has_c = os.path.exists(os.path.join(ROOT, 'src', obj + '.c'))
        mixed = has_c and os.path.exists(os.path.join(ROOT, 'src', obj + '.s'))
        if mixed:
            asm_left[obj] = '`src/%s.s`' % obj
        elif has_c and re.search(r'^__asm__\s*\(', open(os.path.join(ROOT, 'src', obj + '.c'),
                                                     encoding='utf-8').read(), re.M):
            asm_left[obj] = 'top-level asm in `src/%s.c`' % obj
        built = {a for a, _ in fdes if has_c and (not mixed or a in C_FUNCS)
                 and a not in asm_funcs(obj, fdes)}
        wip = wip_state(obj, sorted(a for a, _ in fdes if a not in built))
        objs[obj] = [(a, names.get(a) or SYMBOLS.get(a, 'FUN_%x' % a).lstrip('_'), 'C' if a in built else wip.get(a, 'asm'))
                     for a, _ in sorted(fdes)]

    def n(fs, *states):
        return sum(s in states for _, _, s in fs)

    def in_c(fs):
        return n(fs, 'C', 'wip')

    # fully built from C: every function is C and no asm is left, neither a
    # src/<obj>.s nor top-level asm in the .c (data, padding, .eh_frame)
    def complete(obj):
        return obj not in asm_left and n(objs[obj], 'C') == len(objs[obj])

    def state(obj, fs):
        s = 'C' if complete(obj) else 'mixed' if n(fs, 'C') else 'asm'
        if obj in asm_left and n(fs, 'C') == len(fs):
            s += '; every function in C, data and `.eh_frame` still in %s' % asm_left[obj]
        drafted = n(fs, 'wip', 'draft')
        if drafted:
            s += '; %d of %d drafted functions match in `wip/%s.c`' % (n(fs, 'wip'), drafted, obj)
        return s

    groups = collections.OrderedDict([('app', []), ('crypto', [])])
    for obj in objs:
        groups[obj.split('/')[0]].append(obj)
    allf = [f for fs in objs.values() for f in fs]
    out = [BEGIN,
           '<!-- generated by re/progress.py; edit that, not this -->', '',
           '## Progress', '',
           'Program functions in matching C: **%d of %d** (%d built from `src/`, %d matching '
           'drafts in `wip/` that the build doesn\'t use yet); %d of %d objects fully built from C. '
           'The runtime objects (crt, libgcc, libmingw32/ex) are library code that already '
           'byte-matches and is left as assembly. Function lists come from the reference '
           "exe's `.eh_frame`; names are the C or `SYMBOLS` names, else ddisasm's `FUN_<va>`."
           % (in_c(allf), len(allf), n(allf, 'C'), n(allf, 'wip'),
              sum(map(complete, objs)), len(objs)), '',
           '| Component | Objects in C | Functions in C |', '|---|---|---|']
    for g, os_ in groups.items():
        fs = [f for o in os_ for f in objs[o]]
        out.append('| `%s/` | %d / %d | %d / %d |' % (
            g, sum(map(complete, os_)), len(os_), in_c(fs), len(fs)))

    def item(f):
        a, name, s = f
        return '- %s `%s` (0x%x)%s' % (MARK[s], name, a,
                                       ' (draft in `wip/`, no match yet)' if s == 'draft' else '')

    def details(summary, body):
        return ['<details>', '<summary>%s</summary>' % summary, ''] + body + ['', '</details>']

    done = [o for o in objs if complete(o)]
    todo = [o for o in objs if o not in done]
    out += ['', '### In progress', '',
            'Objects with functions or data still in assembly (a `src/<obj>.s` or top-level asm in the `.c`). Per-function status in address order: '
            '✅ built from C, ☑️ matching C draft in `wip/`, ⬜ assembly. '
            '"Functions in C" counts both ✅ and ☑️.', '',
            '| Object | State | Functions in C |', '|---|---|---|']
    for obj in todo:
        fs = objs[obj]
        out.append('| `%s` | %s | %d / %d |' % (obj, state(obj, fs), in_c(fs), len(fs)))
    out.append('')
    for obj in todo:
        out += details('<code>%s</code>: %d / %d in C' % (obj, in_c(objs[obj]), len(objs[obj])),
                       [item(f) for f in objs[obj]])
    out += ['', '### Completed', '',
            'Objects built entirely from C, in link order.', '',
            '| Object | Functions |', '|---|---|']
    done_app = [o for o in done if not o.startswith('crypto/')]
    done_cr = [o for o in done if o.startswith('crypto/')]
    for obj in done_app:
        out.append('| `%s` | %d |' % (obj, len(objs[obj])))
    if done_cr:
        out.append('| `crypto/*` (%d XeCrypt objects) | %d |' % (
            len(done_cr), sum(len(objs[o]) for o in done_cr)))
    out.append('')
    for obj in done_app:
        out += details('<code>%s</code>: %d functions' % (obj, len(objs[obj])),
                       [item(f) for f in objs[obj]])
    if done_cr:
        body = []
        for obj in done_cr:
            body.append('- `%s`' % obj)
            body += ['  ' + item(f) for f in objs[obj]]
        out += details('<code>crypto/*</code>: %d objects, %d functions' % (
            len(done_cr), sum(len(objs[o]) for o in done_cr)), body)
    out.append(END)

    text = open(readme, encoding='utf-8').read()
    if BEGIN in text:
        pre, rest = text.split(BEGIN, 1)
        text = pre + '\n'.join(out) + rest.split(END, 1)[1]
    else:
        # first run: insert after the Status section
        k = text.index('\n## ', text.index('\n## Status') + 1)
        text = text[:k + 1] + '\n'.join(out) + '\n\n' + text[k + 1:]
    with open(readme, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    print('%d / %d functions in C (%d built, %d matching in wip/)'
          % (in_c(allf), len(allf), n(allf, 'C'), n(allf, 'wip')))


if __name__ == '__main__':
    main()
