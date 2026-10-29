"""Compare one function's gcc output with the original, before a full build.

python tools/re/fncmp.py <src/obj.c> <name> [gcc flags...]

Compiles the C file (-O3 -fno-asynchronous-unwind-tables unless flags are
given) to Intel-syntax assembly and diffs `name` (as in split.py's SYMBOLS,
without the underscore) against the original instructions from
build/xeBuild.lines.json.  Labels are compared only as labels; named symbols
(SYMBOLS) must agree.  Prints MATCH or a unified diff.  It ignores alignment
padding and doesn't check the bytes; `sh build.sh` has the last word.
FNCMP_GCCSYM=_f.constprop.0 compares that gcc function (a clone) instead.
"""
import difflib, json, os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(__file__))
from ddfix import Image
from split import SYMBOLS, IAT_NAMES
from units import units

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BIN = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin')
LOCAL = re.compile(r'(?<![\w.$])(?:\.?L_[0-9a-f]+|FUN_[0-9a-f]+|L\d+|_\w+)(?![\w$])')
NAMED = set(SYMBOLS.values()) | {v.split('@')[0] for v in IAT_NAMES.values()}
# FNCMP_LITERALS=1: a draft with string literals (tools/wip/) compares against the
# .s's named strings (`_msg_*`, `_str_*`, `_mu_*`, `_mc_*`) as plain labels
if os.environ.get('FNCMP_LITERALS'):
    NAMED = {n for n in NAMED if not re.match(r'_(msg|str|mu|ir|mc|net|bd|iw|fi)_', n)}
# condition-code spellings: gcc's (e.g. jnb) -> ddisasm's (jae)
CC = {'nb': 'ae', 'nae': 'b', 'z': 'e', 'nz': 'ne', 'nbe': 'a', 'na': 'be',
      'nl': 'ge', 'nge': 'l', 'nle': 'g', 'ng': 'le', 'c': 'b', 'nc': 'ae'}
CCOP = re.compile(r'^(j|cmov|set)(%s) ' % '|'.join(sorted(CC, key=len, reverse=True)))


def norm(lines):
    out = []
    for l in lines:
        l = l.split('#')[0].strip()
        if not l or l.endswith(':') or l.startswith('.'):
            continue
        l = re.sub(r'\s+', ' ', l).replace(', ', ',')
        l = re.sub(r'(__imp__\w+)@\d+', r'\1', l)   # stdcall imports
        l = re.sub(r'offset flat:', 'offset ', l, flags=re.I)
        # gcc: `call [dword ptr _x]`, `dword ptr _x`, `dword ptr _x[ecx*4]`;
        # ddisasm: `call dword ptr [_x]`, `dword ptr [_x]`, `dword ptr [ecx*4+_x]`
        l = re.sub(r'\[((?:byte|word|dword|qword) ptr .*)\]$', r'\1', l, flags=re.I)
        l = re.sub(r'((?:byte|word|dword|qword) ptr )([A-Za-z_][\w.]*(?:[+-]\d+)?)\[([^\]]*)\]',
                   r'\1[\2+\3]', l, flags=re.I)
        l = re.sub(r'((?:byte|word|dword|qword) ptr )([A-Za-z_][\w.]*(?:[+-]\d+)?)(?![\w.\[+-])',
                   r'\1[\2]', l, flags=re.I)
        # gcc: `lea eax,_x+8[ebx]`; ddisasm: `lea eax,[ebx+_x+8]`
        l = re.sub(r'^(lea \w+,)([A-Za-z_][\w.]*(?:[+-]\d+)?)\[([^\]]*)\]$', r'\1[\2+\3]', l, flags=re.I)
        # labels and unnamed (static) symbols compare as `L`; SYMBOLS names must agree.
        # gcc's local names: LC0 (literals), _x.2980 (function statics), _f.part.3
        l = re.sub(r'(?<![\w.$])_\w+(?:\.\w+)+', 'L', l)
        l = LOCAL.sub(lambda m: m.group(0) if m.group(0) in NAMED else 'L', l)
        l = re.sub(r'(?<![\w.$])LC\d+(?![\w$])', 'L', l)
        l = re.sub(r'(?<![\w$])L(?:\.\w+)+', 'L', l)
        # ddisasm labels data at an offset from gcc's symbol: compare as plain L
        l = re.sub(r'(?<![\w$])L\+\d+', 'L', l)
        l = l.lower()
        l = CCOP.sub(lambda m: m.group(1) + CC[m.group(2)] + ' ', l)
        l = re.sub(r'^sal ', 'shl ', l)
        l = re.sub(r'^(sh[lr]|sar|ro[lr]|rc[lr]) (\w+)$', r'\1 \2,1', l)
        l = re.sub(r'^(f\w+p) st\(1\),st$', r'\1 st(1)', l)
        l = re.sub(r'^rep[z]? ret$', 'rep ret', l)
        l = re.sub(r'^repne ', 'repnz ', l)
        l = re.sub(r'^repe ', 'repz ', l)
        l = re.sub(r'^((?:rep\w* )?(?:sto|lod|sca|mov|cmp)s[bwd]) .*\[es\].*$', r'\1', l)
        l = re.sub(r'\[([^\]]*)\]', lambda m: '[%s]' % addr_terms(m.group(1)), l)
        if l.startswith('lea '):
            l = l.replace(',dword ptr [', ',[')
        # immediates as signed, at the operand's width
        l = re.sub(r'(?<![\w$-])(\d{10})(?!\w)',
                   lambda m: str(int(m.group(1)) - (1 << 32)) if int(m.group(1)) >= 1 << 31 else m.group(1), l)
        m = re.match(r'^(.*(?: (byte|word) ptr \[[^\]]*\]| ([abcd][lh])|( [abcd]x|[ ,](?:si|di|bp))),)(\d+)$', l)
        if m:
            bits = 8 if (m.group(2) == 'byte' or m.group(3)) else 16
            v = int(m.group(5))
            if v >= 1 << (bits - 1):
                l = '%s%d' % (m.group(1), v - (1 << bits))
        l = l.rstrip()
        # alignment padding (gcc's .p2align becomes these nops)
        if l in ('nop', 'mov esi,esi', 'mov edi,edi', 'lea esi,[esi]', 'lea edi,[edi]', 'xchg ax,ax'):
            continue
        out.append(l)
    return out


def addr_terms(e):
    """[edi+ebx*1-1] and [edi-1+ebx] -> one spelling"""
    terms = re.findall(r'[+-]?[^+-]+', e)
    terms = [t if t[0] in '+-' else '+' + t for t in terms]
    terms = [t[:-2] if t.endswith('*1') else t for t in terms]
    terms = [t for t in terms if t not in ('+0', '-0')]
    if '+l' in terms:   # offsets from a label depend on where ddisasm put it
        terms = [t for t in terms if not re.match(r'^[+-]\d+$', t)]
    return ''.join(sorted(terms)).lstrip('+')


def main():
    src, name = sys.argv[1:3]
    flags = sys.argv[3:] or ['-O3']
    sym = '_' + name
    addr = next((a for a, s in SYMBOLS.items() if s == sym), None)
    if addr is None:
        sys.exit('%s is not in split.py SYMBOLS' % sym)
    size = dict(f for _, fs in units(Image(os.path.join(ROOT, 'xeBuild.exe'))) for f in fs)[addr]
    d = json.load(open(os.path.join(ROOT, 'build', 'xeBuild.lines.json')))
    rename = re.compile(r'(?<![\w.$])(?:FUN|\.?L)_(%s)(?![\w$])' % '|'.join('%x' % a for a in SYMBOLS))
    ref = []
    for l, a in zip(d['lines'], d['addr']):
        if a is None or not addr <= a < addr + size:
            continue
        # instructions ddisasm spells as bytes (to keep their encoding) carry
        # the instruction as a comment
        m = re.match(r'\s*\.byte [^#]*#\s*(.+)$', l)
        if m:
            l = m.group(1)
        # `L_x+N` is whatever is at x+N (gcc spells it `_name+N`, resolved alike)
        l = re.sub(r'(?<![\w.$])\.?L_([0-9a-f]+)\+(\d+)(?![\w])', lambda m: SYMBOLS.get(
            int(m.group(1), 16) + int(m.group(2)), 'L_%x' % (int(m.group(1), 16) + int(m.group(2)))), l)
        l = rename.sub(lambda m: SYMBOLS[int(m.group(1), 16)], l)
        # ddisasm names IAT slots by the import (`[_errno]`); gcc says __imp___errno
        l = re.sub(r'PTR \[(_\w+)\]', lambda m: 'PTR [%s]' % (m.group(1) if m.group(1) in NAMED
                                                            else '__imp__' + m.group(1)), l)
        # IAT slots split.py renames (ws2_32's: `[send]` -> `[__imp__send@16]`)
        l = re.sub(r'PTR \[(\w+)\]', lambda m: 'PTR [%s]' % IAT_NAMES.get(m.group(1), m.group(1)), l)
        ref.append(l)

    env = dict(os.environ, PATH=BIN + os.pathsep + os.environ.get('PATH', ''))
    if os.environ.get('FNCMP_ASM'):
        # FNCMP_ASM=<file.s>: compare gcc's Intel-syntax output already made
        # (a profile build), instead of compiling src
        r = subprocess.CompletedProcess([], 0, open(os.environ['FNCMP_ASM']).read(), '')
    else:
        r = subprocess.run([os.path.join(BIN, 'gcc.exe'), '-S', '-masm=intel',
                            '-fno-asynchronous-unwind-tables', '-I', os.path.dirname(src)]
                           + flags + [src, '-o', '-'], env=env, capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr)
    # a named global plus an offset (a struct field, `_xb+8`, `_xb[8+ebx*4]`)
    # is whatever ddisasm named that address: a SYMBOLS name or a label
    addr_of = {s: a for a, s in SYMBOLS.items()}
    at = lambda a: SYMBOLS.get(a, 'L_%x' % a)
    g = re.sub(r'(?<![\w.$])(_\w+)\[(\w+)\+(\d+)\]', r'\1[\3+\2]', r.stdout)
    # `_x[ecx+2+ecx]`: the displacement between the registers
    g = re.sub(r'(?<![\w.$])(_\w+)\[(\w+)\+(\d+)\+(\w+)\]', r'\1[\3+\2+\4]', g)
    # `_cpuKey[ebx-1]`: a named global indexed with a negative offset
    g = re.sub(r'(?<![\w.$])(_\w+)\[(\w+)-(\d+)(\+\w+)?\]', lambda m: m.group(0) if m.group(1) not in addr_of
               else '%s[%s%s]' % (at(addr_of[m.group(1)] - int(m.group(3))), m.group(2), m.group(4) or ''), g)
    g = re.sub(r'(?<![\w.$])(_\w+)(?:\+(\d+)(?![\w])|\[(\d+)\+)',
               lambda m: m.group(0) if m.group(1) not in addr_of else
               at(addr_of[m.group(1)] + int(m.group(2))) if m.group(2) else
               '%s[' % at(addr_of[m.group(1)] + int(m.group(3))), g)
    # `lea ebx, _x[eax]` -> `lea ebx, [_x+eax]`, as ddisasm spells it
    g = re.sub(r'(\blea\s+\w+,\s*)(_\w+)\[([^\]]*)\]', r'\1[\2+\3]', g).split('\n')
    # FNCMP_GCCSYM: compare gcc's function of another name (a clone, `_f.constprop.0`)
    sym = os.environ.get('FNCMP_GCCSYM', sym)
    if sym + ':' not in g:
        sys.exit('%s not defined (inlined, or static and unused?)' % sym)
    # the function's .text lines up to the next function (jump tables go to .rdata)
    mine, text = [], True
    for l in g[g.index(sym + ':') + 1:]:
        if re.match(r'\s*\.(def|globl|ident)\b', l):
            break
        m = re.match(r'\s*(\.section\s+([^\s,]+)|\.text|\.data|\.bss)\b', l)
        if m:
            text = (m.group(2) or m.group(1)).startswith('.text')
        elif text:
            mine.append(l)
    diff = list(difflib.unified_diff(norm(ref), norm(mine), 'original', src, lineterm='',
                                     n=int(os.environ.get('FNCMP_CONTEXT', 2))))
    print('\n'.join(diff) if diff else 'MATCH')
    sys.exit(1 if diff else 0)


if __name__ == '__main__':
    main()
