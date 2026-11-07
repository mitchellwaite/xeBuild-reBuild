"""Attempt 17: the hand-written part as a function gcc places and size-optimises itself.

Builds variants of src/options.c in which the hand-written `_parseButton.part.0` (cold,
section(".text.startup"), regparm(1), asm label) is replaced by a plain function, and
reports for each: the optlib score, gcc's expansion order (cgraph dump), the part's node
frequency after ipa-profile, and fnsplit's decisions for it.

python tools/wip/dehint/op17.py [variant ..] [-k]    (no variant: all; -k keeps dumps)
  dumps go to build/op/a17/<variant>/"""
import os, re, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib, bdlib

OUT = os.path.join(optlib.R, 'build', 'op', 'a17')
SRC = open(optlib.SRC).read()

HEAD = '''__attribute__((cold, section(".text.startup"), regparm(1)))
int parseButtonPart(const char *s) __asm__("_parseButton.part.0");
__attribute__((regparm(1))) int parseButtonPart(const char *s)
{'''
PBE = 'else if (__builtin_expect(!strnicmp(s, "winbutton", 9), 1))'
PBE0 = 'else if (!strnicmp(s, "winbutton", 9))'


def part_body(t):
    i = t.index(HEAD)
    j = t.index('\nint baseFileExists(', i)
    return t[:i], t[i:j], t[j:]


def make(head, where='first', pbe=True, edits=()):
    """head replaces HEAD (must end with '{'); where: 'first', 'last' (end of file, with a
    static prototype first), 'before:<text>' (moved before that text, prototype first)."""
    t = SRC
    a, body, b = part_body(t)
    body = body.replace(HEAD, head)
    if where == 'first':
        t = a + body + b
    else:
        proto = head.rstrip('{').rstrip() + ';\n'
        # prototype where the definition was (callers need it), definition elsewhere
        t = a + proto + b
        if where == 'last':
            t = t.rstrip('\n') + '\n\n' + body.lstrip('\n') + '\n'
        else:
            k = t.index(where[7:])
            t = t[:k] + body.lstrip('\n') + '\n' + t[k:]
    if not pbe:
        assert PBE in t
        t = t.replace(PBE, PBE0)
    for x, y in edits:
        assert x in t, x
        t = t.replace(x, y)
    return t


CP = [('{\n\tint b = 0;\n\n\tif (!strnicmp(s, "wirelessx"', '{\n\tif (!strnicmp(s, "wirelessx"'),
      ('b = parseButtonPart(s);', 'b = parseButtonPart(s, 0);')]

V = {
    # attempt 1's static cold helper (FDE order) and plain static (attempt 15)
    'st_cold': make('static __attribute__((cold)) int parseButtonPart(const char *s)\n{'),
    'st': make('static int parseButtonPart(const char *s)\n{'),
    'st_np': make('static int parseButtonPart(const char *s)\n{', pbe=False),
    'st_last': make('static int parseButtonPart(const char *s)\n{', where='last'),
    'st_cold_last': make('static __attribute__((cold)) int parseButtonPart(const char *s)\n{',
                         where='last'),
    'gl': make('int parseButtonPart(const char *s)\n{'),
    # the current trick minus section and asm label (same place in the exe?)
    'gl_cold_rp': make('__attribute__((cold, regparm(1))) int parseButtonPart(const char *s)\n{'),
    # probes: an always-0 parameter, so ipa-cp clones the part late (expansion order)
    'st_cold_cp': make('static __attribute__((cold)) int parseButtonPart(const char *s, int b)\n{',
                       edits=CP),
    'st_cp': make('static int parseButtonPart(const char *s, int b)\n{', pbe=False, edits=CP),
    # callers pass their own b (0 there): b = parseButtonPart(s, b)
    'st_cpb': make('static int parseButtonPart(const char *s, int b)\n{', pbe=False,
                   edits=[CP[0], ('b = parseButtonPart(s);', 'b = parseButtonPart(s, b);')]),
    # a def parameter copied into b
    'st_cpd': make('static int parseButtonPart(const char *s, int def)\n{', pbe=False,
                   edits=[('{\n\tint b = 0;\n\n\tif (!strnicmp(s, "wirelessx"',
                           '{\n\tint b = def;\n\n\tif (!strnicmp(s, "wirelessx"'), CP[1]]),
    # the part keeps returning 0 itself, the extra argument is the name's length limit
    'st_cp_last': make('static int parseButtonPart(const char *s, int b)\n{', pbe=False,
                       edits=CP, where='last'),
    'gl_cold': make('__attribute__((cold)) int parseButtonPart(const char *s)\n{'),
}


def gcc(text, d, extra):
    os.makedirs(d, exist_ok=True)
    src = os.path.join(d, 'o.c')
    open(src, 'w', newline='\n').write('#line 1 "options.c"\n' + text)
    r = subprocess.run([bdlib.GCC, '-c', '-O3'] + optlib.P83 + list(extra) +
                       ['-I' + os.path.join(optlib.R, 'src'), 'o.c', '-o', 'o.o'],
                       cwd=d, capture_output=True, text=True)
    return r


def info(d):
    out = []
    cg = [f for f in os.listdir(d) if f.endswith('.cgraph') and not f.endswith('000i.cgraph')]
    for f in os.listdir(d):
        p = os.path.join(d, f)
        if f.endswith('i.cgraph'):
            ex = re.findall(r'expand_all_functions:(\S+):', open(p).read())
            out.append('expand: ' + ' '.join(ex[:4]) + ' ...')
        if re.search(r'\d+i\.profile_estimate$', f):
            s = open(p).read()
            for m in re.finditer(r'Processing frequency (\S*[pP]art\S*)\n((?:  .*\n)*)', s):
                out.append('ipa-profile %s: %s' % (m.group(1), m.group(2).strip().replace('\n', '; ')))
            for m in re.finditer(r'Node (\S*[pP]art\S*) promoted to (.*)', s):
                out.append('  -> %s %s' % (m.group(1), m.group(2)))
        if f.endswith('fnsplit'):
            s = open(p).read()
            for m in re.finditer(r';; Function (\S*[pP]art\S*|parseButton) .*\n((?:.*\n)*?)(?=;; Function|\Z)', s):
                body = m.group(2)
                sp = re.search(r'Splitting function at:\nSplit point at BB (\d+)', body)
                ns = re.search(r'Not splitting: (.*)', body)
                out.append('fnsplit %s: %s' % (m.group(1), 'split at BB ' + sp.group(1) if sp
                                                 else (ns.group(1) if ns else 'no split')))
    return out


def run(name, keep=False):
    d = os.path.join(OUT, name)
    r = gcc(V[name], d, ['-fdump-ipa-cgraph', '-fdump-ipa-profile_estimate-details',
                         '-fdump-tree-fnsplit-details'])
    if r.returncode:
        print(name, 'COMPILE', r.stderr[:600])
        return
    o = os.path.join(d, 'o.o')
    nm = subprocess.run([bdlib.TC + '/nm.exe', o], capture_output=True, text=True).stdout
    for m in set(re.findall(r' (_parseButtonPart\S*)$', nm, re.M)):
        subprocess.run([bdlib.TC + '/objcopy.exe', '--redefine-sym',
                        m + '=' + ('_parseButton.part.0' if m in ('_parseButtonPart',
                        '_parseButtonPart.constprop.5') else m.replace('_parseButtonPart',
                                                                       '_parseButton.part.0')), o])
    res = optlib.report(o)
    fde = subprocess.run([bdlib.OBJDUMP, '-r', '-j', '.eh_frame', o], capture_output=True,
                         text=True).stdout
    print('    eh_frame relocs: ' + ' '.join(re.findall(r'DISP32\s+(\S+)', fde)[:4]))
    print('%-14s %s' % (name, 'IDENTICAL ' + ' '.join(res[3]) if res[0]
                        else '%d %s %s' % (res[1], res[2], ' '.join(res[3]))))
    for l in info(d):
        print('    ' + l)
    sec = subprocess.run([bdlib.OBJDUMP, '-h', os.path.join(d, 'o.o')], capture_output=True,
                         text=True).stdout
    print('    sections: ' + ' '.join(re.findall(r'^\s+\d+ (\.text\S*)', sec, re.M)))


if __name__ == '__main__':
    a = sys.argv[1:]
    keep = '-k' in a
    a = [x for x in a if x != '-k']
    for n in a or list(V):
        run(n, keep)
