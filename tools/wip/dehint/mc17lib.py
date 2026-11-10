"""mode_client attempt 17: compile a source text as build.sh does (plain -O3) and compare the
object with build/mc/w17/reference.o (a copy of the matching build/obj/mode_client.o of
commit e8c0b8d8; build/mc/reference.o is older: its clientManifest predates the app headers).

python tools/wip/dehint/mc17lib.py <file.c> [-v [fn]] [-l] [-d TAG]
  -v    per-function diff (- reference, + draft)
  -l    layout: mode_client's blocks in address order, named by the string or call they
        reach, side by side with the reference's (the final layout is the evidence, not a
        dump's trace order)
  -d    write bbro / profile_estimate / vrp1 dumps to build/mc/w17/d_TAG

Report: IDENTICAL when .text disassembly, .rdata, .data, .bss and relocations all match
(BYTES when the whole file does); else differing lines per function and sections."""
import difflib, os, re, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib

R = bdlib.R
BUILD = os.path.join(R, 'build', 'mc', 'w17')
REF = os.path.join(BUILD, 'reference.o')
SRC = os.path.join(R, 'src', 'mode_client.c')
SECS = ('.text', '.data', '.rdata', '.bss')
read_src = bdlib.read_src
cleanup = bdlib.cleanup


def relocs(o):
    t = subprocess.run([bdlib.OBJDUMP, '-r', o], capture_output=True, text=True).stdout
    return [l for l in t.split('\n') if l and not l.startswith(('In archive', o))]


def section(o, name):
    t = tempfile.mktemp(dir=BUILD)
    subprocess.run([bdlib.OBJCOPY, '-O', 'binary', '-j', name, o, t], capture_output=True)
    try:
        b = open(t, 'rb').read()
        os.remove(t)
    except OSError:
        b = b''
    return b


_ref = {'bytes': open(REF, 'rb').read()}
_ref['fns'], _ref['order'] = bdlib.disasm(REF)
_ref['sec'] = {s: section(REF, s) for s in SECS}
_ref['rel'] = relocs(REF)


def compile_src(text, flags=(), keep=None, extra=()):
    d = tempfile.mkdtemp(dir=BUILD, prefix='t')
    o = keep or os.path.join(d, 'o.o')
    src = '#line 1 "mode_client.c"\n' + text
    r = subprocess.run([bdlib.GCC, '-c', '-O3'] + list(flags) + list(extra) +
                       ['-I' + os.path.join(R, 'src'), '-x', 'c', '-', '-o', o],
                       input=src.encode(), cwd=d, capture_output=True)
    if r.returncode:
        return False, r.stderr.decode(errors='replace'), d
    return True, o, d


def report(o):
    r = _ref
    if open(o, 'rb').read() == r['bytes']:
        return True, 0, {}, ['BYTES']
    fns, order = bdlib.disasm(o)
    per = {}
    for n in r['order']:
        if n not in fns:
            per[n] = 9999
        else:
            k = bdlib.fdiff(r['fns'][n], fns[n])
            if k:
                per[n] = k
    notes = []
    for n in order:
        if n not in r['fns']:
            notes.append('new fn ' + n)
            per[n] = 9999
    if order != r['order'] and sorted(order) == sorted(r['order']):
        notes.append('text order differs')
    for s in SECS:
        if section(o, s) != r['sec'][s]:
            notes.append(s + ' differs')
    if relocs(o) != r['rel']:
        notes.append('relocs differ')
    return not per and not notes, sum(per.values()), per, notes


# ---- layout: the function's blocks in address order ---------------------------------

def _strings(o):
    b = section(o, '.rdata')

    def at(off):
        e = b.find(b'\0', off)
        return b[off:e].decode('latin1').replace('\n', ' ').strip()
    return at


def layout(o, fn='_mode_client'):
    """[(name, n_insns)] for the function's blocks (split at jump targets and after
    jumps), in address order.  A block's name is what it reaches: string literals (first
    words), callees, `usage(N,reg)`, `mode=N`."""
    t = subprocess.run([bdlib.OBJDUMP, '-d', '-r', '--no-show-raw-insn', o],
                       capture_output=True, text=True).stdout
    at = _strings(o)
    ins = []
    cur = False
    for l in t.split('\n'):
        m = re.match(r'^([0-9a-f]+) <(.+)>:$', l)
        if m:
            cur = m.group(2) == fn
            continue
        if not cur:
            continue
        m = re.match(r'^\s*([0-9a-f]+):\s+(\S.*)$', l)
        if not m:
            continue
        a, s = int(m.group(1), 16), m.group(2).strip()
        if re.match(r'^(dir32|DISP32)\s', s):
            ins[-1][2].append(s.split()[-1])
        else:
            ins.append([a, s, []])
    targets = set()
    for a, s, rel in ins:
        m = re.match(r'^j\w+\s+([0-9a-f]+) <', s)
        if m:
            targets.add(int(m.group(1), 16))
    blocks = []
    cur = None
    for k, (a, s, rel) in enumerate(ins):
        if cur is None or a in targets:
            cur = {'addr': a, 'tok': [], 'n': 0}
            blocks.append(cur)
        cur['n'] += 1
        if re.match(r'^(nop|xchg\s+%ax,%ax|lea\s+0x0\(%e[sd]i(,%eiz,1)?\),%e[sd]i|mov\s+%esi,%esi)$', s):
            cur['n'] -= 1
            continue
        m = re.match(r'^movl\s+\$0x([0-9a-f]+),0x4\(%esp\)$', s)
        if m and '.rdata' in rel:
            cur['tok'].append('"%s"' % at(int(m.group(1), 16))[:28])
        m = re.match(r'^movl\s+\$0x([0-9a-f]+),\(%esp\)$', s)
        if m and '.rdata' in rel:
            cur['tok'].append('"%s"' % at(int(m.group(1), 16))[:28])
        m = re.match(r'^call\s+[0-9a-f]+ <(\w+)(\+0x[0-9a-f]+)?>$', s)
        if m:
            if rel:
                cur['tok'].append(rel[0].lstrip('_') + '()')
            elif m.group(1) == '_client_usage':
                n, reg = '?', ''
                for _, s2, _ in ins[max(0, k - 3):k]:
                    m2 = re.match(r'^movl\s+\$0x([0-9a-f]+),\(%esp\)$', s2)
                    if m2:
                        n = m2.group(1)
                    m2 = re.match(r'^mov\s+(-?0x[0-9a-f]+)?\(%e[a-z]+,%(e[a-z]+),[14]\),%eax$', s2)
                    if m2:
                        reg = ',' + m2.group(2)
                cur['tok'].append('usage(%s%s)' % (n, reg))
            else:
                cur['tok'].append(m.group(1).lstrip('_') + '()')
        if s.startswith('jmp    *'):
            cur['tok'].append('switch')
        if re.match(r'^(jmp|ret)', s) or s.endswith('<_client_usage>'):
            cur = None
    # a block with no token takes the mode it sets, else `-`
    out = []
    for b in blocks:
        out.append((' '.join(b['tok']) or '-', b['n']))
    return out


def chunks(o, fn='_mode_client'):
    """layout() with token-less blocks folded into the block before them"""
    out = []
    for name, n in layout(o, fn):
        if name == '-' and out:
            out[-1] = (out[-1][0], out[-1][1] + n)
        else:
            out.append((name, n))
    return out


def laydiff(o, show=True):
    a = [x[0] for x in chunks(REF)]
    b = [x[0] for x in chunks(o)]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    moved = sum(max(i2 - i1, j2 - j1) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != 'equal')
    if show:
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == 'equal':
                for x in a[i1:i2]:
                    print('   ', x)
            else:
                for x in a[i1:i2]:
                    print('  -', x)
                for x in b[j1:j2]:
                    print('  +', x)
    return moved


def score_text(text, flags=(), extra=(), lay=False):
    ok, o, d = compile_src(text, flags, extra=extra)
    try:
        if not ok:
            return {'compile': o[-600:]}
        idn, tot, per, notes = report(o)
        r = {'identical': idn, 'total': tot, 'per': per, 'notes': notes}
        if lay:
            r['moved'] = laydiff(o, show=False)
        return r
    finally:
        cleanup(d)


def fmt(s):
    if 'compile' in s:
        return 'COMPILE ' + s['compile'].strip().split('\n')[-1][:160]
    if s['identical']:
        return 'IDENTICAL ' + ' '.join(s['notes'])
    return '%d %s %s%s' % (s['total'], s['per'], ' '.join(s['notes']),
                           ' moved=%d' % s['moved'] if 'moved' in s else '')


def vdiff(text, only=None):
    ok, o, d = compile_src(text)
    if not ok:
        print('COMPILE ERROR', o)
        return
    idn, tot, per, notes = report(o)
    print(fmt({'identical': idn, 'total': tot, 'per': per, 'notes': notes}))
    fns, _ = bdlib.disasm(o)
    for n in per:
        if only and n != only:
            continue
        a, b = _ref['fns'].get(n, []), fns.get(n, [])
        for l in difflib.unified_diff(a, b, 'ref', 'new', n=2, lineterm=''):
            print(l)
    cleanup(d)


DUMPS = ['-fdump-rtl-bbro-details-blocks', '-fdump-tree-profile_estimate-details', '-fdump-tree-vrp1-details',
         '-fdump-tree-optimized-details', '-fdump-ipa-inline-details', '-fdump-rtl-expand',
         '-fdump-tree-einline-details']


def dump(text, tag, extra=()):
    d = os.path.join(BUILD, 'd_' + tag)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'mode_client.c'), 'w', newline='\n').write('#line 1 "mode_client.c"\n' + text)
    r = subprocess.run([bdlib.GCC, '-c', '-O3'] + DUMPS + list(extra) + ['-I' + os.path.join(R, 'src'),
                        'mode_client.c', '-o', 'o.o'], cwd=d, capture_output=True)
    if r.returncode:
        print(r.stderr.decode(errors='replace')[-600:])
    return d


if __name__ == '__main__':
    a = sys.argv[1:]
    text = read_src(a[0])
    if '-d' in a:
        print(dump(text, a[a.index('-d') + 1]))
    if '-v' in a:
        k = a.index('-v')
        only = a[k + 1] if k + 1 < len(a) and not a[k + 1].startswith('-') else None
        vdiff(text, only)
    elif '-l' in a:
        ok, o, d = compile_src(text)
        if not ok:
            print('COMPILE ERROR', o)
        else:
            idn, tot, per, notes = report(o)
            m = laydiff(o)
            print(fmt({'identical': idn, 'total': tot, 'per': per, 'notes': notes}), 'moved=%d' % m)
        cleanup(d)
    else:
        print(fmt(score_text(text, lay=True)))
